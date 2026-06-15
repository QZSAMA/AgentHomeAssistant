# AgentHomeAssistant

基于 Apple 生态 + 小米智能家居 + Hermes Agent 的个人家庭助理自动化方案

## 核心特性

- 🤖 **Agent 驱动**：使用 Hermes Agent 作为智能核心，支持自然语言交互
- 🔧 **自然语言配置**：通过对话即可创建、修改场景，无需手动编辑配置
- 🔄 **灵活可扩展**：Agent 可自由替换，适配器模式解耦 Home Assistant
- ⚙️ **YAML + Web UI**：核心配置版本化管理，可视化配置灵活调整

## 网络架构

### 双路由方案

采用主路由器 + 副路由器双路由架构，实现家庭网络与工作网络的物理隔离，通过切换 WiFi 即可切换网络出口。

```
互联网
  │
  ▼
┌──────────────────┐
│   光猫 (桥接模式)  │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────┐
│   主路由器 (原厂固件)          │
│   192.168.1.1                │
│   DHCP: 192.168.1.100-200    │
│   WiFi: "Home"               │
└────────┬─────────────────────┘
         │
    ┌────┴──────────────────────┐
    │  主网络 192.168.1.0/24     │
    │  NAS / Mac / 智能家居设备   │
    │                            │
    │  ┌────────────────────────┐│
    │  │ 副路由器 (OpenWrt)      ││
    │  │ WAN: DHCP → 192.168.1.x││
    │  │ LAN: 192.168.2.1       ││
    │  │ WiFi: "Work"           ││
    │  │ + WireGuard 隧道        ││
    │  │ + avahi-daemon 中继     ││
    │  │ + NAT (MASQUERADE)      ││
    │  └────────┬───────────────┘│
    │           │                │
    │  工作子网 192.168.2.0/24    │
    │  工作设备 (切换 WiFi 即可)   │
    └────────────────────────────┘
```

### 设计原则

| 原则 | 说明 |
|------|------|
| 主路由零改动 | 主路由器保持原厂固件，不做任何配置变更 |
| 网络隔离 | 工作流量与家庭流量完全隔离，VPN 故障不影响家庭网络 |
| 切换便捷 | 切换 WiFi 即可切换网络出口，无需额外操作 |
| NAS 互通 | 工作网络通过 NAT 穿透访问主网络 NAS |
| 设备发现 | 通过 avahi-daemon mDNS 中继实现跨子网 AirPlay/HomeKit |

### 数据流路径

| 场景 | 流量路径 |
|------|---------|
| 工作设备 → 公司网络 | 设备 → 副路由器 → WireGuard 隧道 → 公司网络 |
| 工作设备 → NAS | 设备 → 副路由器 NAT → 主网络 → NAS |
| 工作设备 → AirPlay | 设备 mDNS → avahi 中继 → 主网络 AirPlay 设备 → 副路由器 NAT → 设备 |
| 家庭设备 → 互联网 | 设备 → 主路由器 → 互联网（不经过副路由器） |

### 副路由器配置详情

#### 硬件选型

| 型号 | SoC | WiFi | 网口 | OpenWrt | 价格 | 备注 |
|------|-----|------|------|---------|------|------|
| 小米 AX3000T (RD03) | MT7981B | WiFi 6 AX3000 | 4× 千兆 | 23.05+ | ~¥130 | 性价比首选，**必须 RD03 版本** |
| GL.iNet MT3000 | MT7981B | WiFi 6 AX3000 | 1× 2.5G + 1× 千兆 | 原生 | ~¥300 | 开箱即用 |
| CMCC RAX3000M | MT7981B | WiFi 6 AX3000 | 4× 千兆 + USB | 官方 | ~¥200 | 均衡之选 |

#### OpenWrt 配置步骤

**1. 基础网络配置**

```uci
# /etc/config/network

config interface 'lan'
    option device 'br-lan'
    option proto 'static'
    option ipaddr '192.168.2.1'
    option netmask '255.255.255.0'

config interface 'wan'
    option device 'wan'
    option proto 'dhcp'    # 从主路由器获取 192.168.1.x
```

**2. DHCP 服务**

```uci
# /etc/config/dhcp

config dhcp 'lan'
    option interface 'lan'
    option start '100'
    option limit '100'
    option leasetime '12h'
```

**3. 防火墙配置**

```uci
# /etc/config/firewall

config zone
    option name 'lan'
    list network 'lan'
    option input 'ACCEPT'
    option output 'ACCEPT'
    option forward 'ACCEPT'

config zone
    option name 'wan'
    list network 'wan'
    list network 'wan6'
    option input 'REJECT'
    option output 'ACCEPT'
    option forward 'REJECT'
    option masq '1'        # NAT 穿透，使工作设备可访问主网络
    option mtu_fix '1'     # MSS Clamping，避免双 NAT 分片问题

config forwarding
    option src 'lan'
    option dest 'wan'      # 允许 LAN → WAN 流量
```

**4. WireGuard 隧道**

```uci
# /etc/config/network

config interface 'wg0'
    option proto 'wireguard'
    option private_key '<YOUR_CLIENT_PRIVATE_KEY>'
    option mtu '1420'
    list addresses '10.x.x.x/24'     # VPN 分配的 IP
    list dns '1.1.1.1'

config wireguard_wg0
    option description 'Company-VPN'
    option public_key '<SERVER_PUBLIC_KEY>'
    option preshared_key '<PRESHARED_KEY>'
    option endpoint_host '<VPN_SERVER_IP>'
    option endpoint_port '51820'
    list allowed_ips '0.0.0.0/0'       # 所有流量走 VPN
    option route_allowed_ips '1'
    option persistent_keepalive '25'    # 保持 NAT 穿透状态
```

```uci
# /etc/config/firewall - 添加 WireGuard 区域

config zone
    option name 'wg'
    list network 'wg0'
    option input 'REJECT'
    option output 'ACCEPT'
    option forward 'REJECT'
    option masq '1'
    option mtu_fix '1'

config forwarding
    option src 'lan'
    option dest 'wg'         # LAN 流量 → VPN 隧道
```

**5. mDNS 中继 (avahi-daemon)**

```bash
# 安装
opkg update && opkg install avahi-daemon

# 禁用默认 umdns（避免冲突）
/etc/init.d/umdns stop && /etc/init.d/umdns disable
```

```ini
# /etc/avahi/avahi-daemon.conf

[server]
use-ipv4=yes
use-ipv6=no
allow-interfaces=br-lan,eth0    # LAN 和 WAN 接口
check-response-ttl=no
use-iff-running=no

[publish]
disable-publishing=no
publish-workstation=no

[reflector]
enable-reflector=yes
reflect-ipv6=no
reflect-filters=_airplay._tcp,_raop._tcp,_ipp._tcp,_hap._tcp
reflector-quick-join=yes

[rlimits]
rlimit-core=0
rlimit-data=4194304
rlimit-nofile=30
rlimit-stack=4194304
rlimit-nproc=3
```

```bash
# 启动并设置开机自启
/etc/init.d/avahi-daemon enable
/etc/init.d/avahi-daemon start
```

### 已知限制与缓解

| 限制 | 影响 | 缓解措施 |
|------|------|---------|
| HomeKit 偶发"无响应" | 跨子网 mDNS 公告可能超时 | 首次配对在主网完成；avahi 服务过滤减少噪声 |
| AirPlay 发现延迟 5-15 秒 | 首次发现比同网段慢 | 启用 reflector-quick-join；可接受 |
| 主网络无法主动访问工作子网 | NAT 导致单向可访问 | 当前需求不需要反向访问 |
| HomeKit 首次配对需同网段 | 跨子网配对可能失败 | 新设备先在主网配对后再使用 |

> 详细可行性分析见 [docs/dual-router-feasibility-analysis.md](docs/dual-router-feasibility-analysis.md)

## 设备清单

### 已接入设备

#### 智能家居设备
- 米家激光投影仪
- Apple TV 4K
- 小米踢脚线暖风机
- 小米空气净化器
- iPhone (苹果手机)

#### 计算基础设施

| 设备 | 角色 | 主要功能 | 网络位置 |
|------|------|----------|----------|
| Mac Studio | 本地大模型 | 本地 LLM 推理 (Ollama/LocalAI) | 主网络 |
| Mac Mini | Agent 控制节点 | 运行 Hermes Agent 实现自动化控制 | 主网络 (安全隔离) |
| NAS (数据中心) | 文件存储 + 媒体服务 | 照片备份、文件共享、媒体库、备份服务 | 主网络 |
| 副路由器 (OpenWrt) | 工作网络网关 | WireGuard 隧道、mDNS 中继、NAT 穿透 | 桥接主网络 / 工作子网 |

#### Mac Studio 配置说明

Mac Studio 作为核心算力设备，承担以下职责：

**本地大模型**
- 运行 Ollama / llama.cpp 等本地 LLM 推理引擎
- 支持模型: Llama 3, Mistral, CodeLlama 等
- 通过 API 对外提供服务，供 Hermes Agent 调用
- 与 Home Assistant 集成，提供语义理解能力

#### Mac Mini 配置说明

Mac Mini 作为独立的 Agent 控制节点：

**Agent 运行环境**
- 运行 Hermes Agent 实例
- 专门负责智能家居自动化决策
- 通过 Home Assistant API 控制设备
- 日志和敏感操作记录隔离存储

**安全隔离策略**
```
┌─────────────────┐      主网络       ┌─────────────────┐
│    Mac Studio    │◄────────────────►│     Mac Mini     │
│   (本地 LLM)     │                  │  (Agent 控制)    │
└─────────────────┘                  └─────────────────┘
        │                                     │
        │                                     │
        ▼                                     ▼
┌─────────────────────────────────────────────────────────────┐
│                      Home Assistant                         │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│   │  传感器  │  │   灯光   │  │   暖风  │  │  净化器  │     │
│   └─────────┘  └─────────┘  └─────────┘  └─────────┘     │
└─────────────────────────────────────────────────────────────┘
```

#### NAS 配置建议

| 服务 | 推荐用途 |
|------|----------|
| Time Machine | Mac 设备备份 |
| SMB / NFS | 文件共享 |
| Plex / Jellyfin | 媒体库服务 |
| Nextcloud | 私有云盘 |
| 数据库备份 | SQLite / PostgreSQL 备份 |

### 设备别名映射

系统支持设备名称到 Home Assistant Entity ID 的映射：

| 自然语言 | Home Assistant Entity ID |
|----------|---------------------------|
| 灯光 / 客厅灯 | `light.living_room` |
| 窗帘 / 客厅窗帘 | `cover.living_room_curtain` |
| 投影仪 / 投影 | `media_player.xiaomi_projector` |
| 暖风机 | `climate.xiaomi_heater` |
| 净化器 / 空气净化器 | `air_quality.xiaomi_air_purifier` |

## 系统架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              用户层                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                     │
│  │  Web UI     │    │  语音输入    │    │  自然语言    │                     │
│  │  (可视化配置) │    │  (Siri等)   │    │  (对话交互)  │                     │
│  └─────────────┘    └─────────────┘    └─────────────┘                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Agent 层                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐   │
│  │                    Hermes Agent (可替换)                               │   │
│  │                                                                       │   │
│  │   • 自然语言理解 (NLU)                                                 │   │
│  │   • 意图识别 (Intent Recognition)                                      │   │
│  │   • 对话管理 (Dialogue Management)                                     │   │
│  │   • 语义记忆 (Semantic Memory)                                        │   │
│  │                                                                       │   │
│  │   ┌───────────────────────────────────────────────────────────────┐   │   │
│  │   │  核心意图                                                        │   │   │
│  │   │  • define_scene    (定义场景) ← 自然语言创建场景                 │   │   │
│  │   │  • modify_scene    (修改场景)                                  │   │   │
│  │   │  • activate_scene  (激活场景)                                  │   │   │
│  │   │  • control_device  (控制设备)                                  │   │   │
│  │   │  • query_state     (查询状态)                                  │   │   │
│  │   └───────────────────────────────────────────────────────────────┘   │   │
│  │                                                                       │   │
│  │   ┌─────────────┐                                                     │   │
│  │   │  AgentBridge │  ◄── 适配器层，支持替换不同 Agent                  │   │
│  │   └─────────────┘                                                     │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ 标准协议 (HTTP/WebSocket)
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Middleware 层                                      │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                         API 网关                                      │   │
│   │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────┐ │   │
│   │   │  Agent API   │  │  Config API  │  │  State API   │  │ Scene  │ │   │
│   │   │  (对话接口)   │  │  (配置接口)   │  │  (状态接口)   │  │ Parser │ │   │
│   │   └──────────────┘  └──────────────┘  └──────────────┘  │  (新增) │ │   │
│   │                                                       └────────┘ │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                         核心引擎                                      │   │
│   │   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐          │   │
│   │   │    意图路由     │  │    场景编排     │  │    场景解析     │          │   │
│   │   │  Intent Router │  │ Scene Engine   │  │ Scene Parser   │          │   │
│   │   └────────────────┘  └────────────────┘  └────────────────┘          │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│          ┌─────────────────────────┼─────────────────────────┐                │
│          ▼                         ▼                         ▼                │
│   ┌─────────────┐           ┌─────────────┐           ┌─────────────┐        │
│   │ Config      │           │   State     │           │    HA      │        │
│   │ Manager     │           │   Store     │           │  Adapter   │        │
│   │ (YAML+DB)   │           │ (状态记录)   │           │            │        │
│   └─────────────┘           └─────────────┘           └─────────────┘        │
│          │                                                     │                │
│          ▼                                                     ▼                │
│   ┌─────────────┐                                   ┌─────────────────────┐  │
│   │ YAML 配置   │                                   │  Device Alias       │  │
│   │ (版本控制)   │                                   │  Registry           │  │
│   └─────────────┘                                   │  (设备别名映射)      │  │
│                                                    └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Home Assistant                                     │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│   │   米家设备   │  │   传感器    │  │   灯光      │  │   空调/暖风  │        │
│   └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          计算基础设施层                                       │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                        主网络 192.168.1.0/24                         │   │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
│   │  │ Mac Studio  │  │  Mac Mini   │  │     NAS     │                  │   │
│   │  │ (本地 LLM)  │  │ (Agent节点) │  │  (存储/备份) │                  │   │
│   │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
│   │                              │                                      │   │
│   │              ┌───────────────┴───────────────┐                      │   │
│   │              │    副路由器 (OpenWrt)           │                      │   │
│   │              │    WireGuard + mDNS 中继        │                      │   │
│   │              └───────────────┬───────────────┘                      │   │
│   │                              │                                      │   │
│   └──────────────────────────────┼──────────────────────────────────────┘   │
│                                  │                                          │
│   ┌──────────────────────────────┼──────────────────────────────────────┐   │
│   │               工作子网 192.168.2.0/24                                │   │
│   │              工作设备 (通过 WiFi "Work" 接入)                         │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 组件说明

### Agent 层

| 组件 | 职责 | 可替换性 |
|------|------|----------|
| Hermes Agent | 自然语言理解、意图识别、对话管理 | ✅ 可替换 |
| AgentBridge | 适配器层，统一接口协议 | ✅ 可替换 |

### Middleware 层

| 组件 | 职责 | 类型 |
|------|------|------|
| Agent API | 对话接口，接收用户输入 | 对外接口 |
| Config API | 配置接口，管理设备/场景 | 对外接口 |
| State API | 状态接口，查询设备状态 | 对外接口 |
| Scene Parser | 解析自然语言场景定义 | 核心引擎 |
| Intent Router | 将意图路由到对应服务 | 核心引擎 |
| Scene Engine | 编排多设备场景执行 | 核心引擎 |
| Config Manager | 加载/验证/管理 YAML 配置 | 内部组件 |
| State Store | 记录设备状态、执行历史 | 内部组件 |
| Device Alias Registry | 设备名称 ↔ Entity ID 映射 | 内部组件 |
| HA Adapter | 封装 Home Assistant API | 可替换适配器 |

### 数据流示例

```
用户："观影模式的意思是，灯光调到最暗，拉上窗帘并且打开投影仪"
        │
        ▼
Hermes Agent
  └─► 识别意图: define_scene
        │
        ▼
AgentBridge → Middleware
        │
        ▼
Scene Parser
  ├─► Device Alias Registry 解析设备名称
  │     ├─► "灯光" → light.living_room
  │     ├─► "窗帘" → cover.living_room_curtain
  │     └─► "投影仪" → media_player.xiaomi_projector
  │
  └─► 解析操作并生成 SceneConfig
        │
        ▼
Config Manager → 保存到 YAML
        │
        ▼
返回确认给用户
```

## 配置管理

### 配置存储方式

| 配置类型 | 存储方式 | 版本控制 |
|----------|----------|----------|
| 设备注册 | YAML | ✅ Git 管理 |
| 场景定义 | YAML | ✅ Git 管理 |
| 设备别名 | YAML | ✅ Git 管理 |
| 用户偏好 | 数据库 | ❌ 运行时存储 |
| 设备状态 | 内存/缓存 | ❌ 实时数据 |

### 场景定义示例

```yaml
# scenes/movie_mode.yaml
name: "观影模式"
description: "自动开启观影环境"
source: "natural_language"  # 自然语言创建

devices:
  - entity_id: "light.living_room"
    service: "turn_on"
    data:
      brightness: 0

  - entity_id: "cover.living_room_curtain"
    service: "close_cover"

  - entity_id: "media_player.xiaomi_projector"
    service: "turn_on"
```

### 操作映射示例

| 自然语言描述 | 解析结果 |
|-------------|----------|
| 调暗 / 调到最暗 | `brightness: 0` |
| 调亮 / 调到最亮 | `brightness: 100` |
| 拉上窗帘 / 关窗帘 | `service: close_cover` |
| 打开投影仪 / 开投影 | `service: turn_on` |
| 调高温 / 调高温度 | `temperature: +2` |
| 调低温 / 调低温度 | `temperature: -2` |

## 使用示例

### 自然语言创建场景

```
用户：观影模式的意思是，灯光调到最暗，拉上窗帘并且打开投影仪

Agent：我理解了，观影模式包括：
       1. 客厅灯 - 亮度调至最暗
       2. 窗帘 - 拉上
       3. 投影仪 - 打开

       保存中...
       [保存成功]

       观影模式已创建完成。需要我现在执行一次吗？
```

### 执行场景

```
用户：打开观影模式

Agent：好的，正在启动观影模式...

       ✓ 客厅灯已调至最暗
       ✓ 窗帘已拉上
       ✓ 投影仪已打开

       观影模式已就绪！
```

### 修改场景

```
用户：把观影模式的灯光调亮一点

Agent：我理解了，观影模式灯光从最暗调整到50%亮度。
       [保存成功]

       观影模式已更新，灯光现在会调到50%亮度。
```

### 查询状态

```
用户：现在客厅温度多少？

Agent：当前客厅温度是 24°C，湿度 45%。
       暖风机目前处于关闭状态。
```

## 技术栈

- **Agent**: Hermes Agent (可替换)
- **Home Assistant**: 智能家居核心平台
- **API 网关**: FastAPI / Flask
- **配置存储**: YAML + SQLite
- **设备集成**: Home Assistant REST API / WebSocket
- **工作网络**: OpenWrt + WireGuard + avahi-daemon

## 后续建议补充的设备

### 智能家居设备
- **Aqara 人体存在传感器**：实现人来自动开设备，人走自动关闭节能
- **温湿度传感器**：给暖风机提供更准确的温度数据，自动调节
- **PM2.5 传感器**：如果空气净化器不带，可以额外添加给自动化决策
- **智能开关面板**：实现物理按键 + 自动化双重控制灯光
- **智能窗帘电机**：支持自动拉上/拉开窗帘

### 网络与基础设施
- **Home Assistant 运行设备**：树莓派 / Mac Mini / NAS 虚拟机，建议与 Agent 节点分离
- **UPS 不间断电源**：保护 Mac Studio、Mac Mini、NAS 免受电力波动影响
- **网络交换机**：2.5G/10G 交换机，用于 NAS 与主机高速传输

## 下一步计划

- [ ] 采购副路由器 (推荐小米 AX3000T RD03)
- [ ] 刷 OpenWrt 固件
- [ ] 配置副路由器基础网络 (WAN/LAN/DHCP)
- [ ] 配置 WireGuard 隧道连接公司网络
- [ ] 配置 avahi-daemon mDNS 中继
- [ ] 测试 NAS 跨子网访问
- [ ] 测试 AirPlay 跨子网投屏
- [ ] 测试 HomeKit 跨子网控制
- [ ] 确定集成方案
- [ ] 搭建运行环境 (决定是跑在本地还是 Docker)
- [ ] 开发 Middleware 核心服务
  - [ ] Config Manager 配置管理
  - [ ] State Store 状态存储
  - [ ] HA Adapter Home Assistant 适配器
  - [ ] Scene Parser 场景解析器
  - [ ] Scene Engine 场景编排引擎
- [ ] 配置设备别名映射
- [ ] 接入 Home Assistant
- [ ] 集成 Hermes Agent
- [ ] 开发 Web UI 可视化配置界面
- [ ] 测试基础设备控制
- [ ] 测试自然语言场景创建
- [ ] 编写场景自动化
- [ ] 端到端测试优化

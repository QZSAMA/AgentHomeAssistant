# AgentHomeAssistant - Code Wiki

> 基于 Apple 生态 + 小米智能家居 + Hermes Agent 的个人家庭助理自动化方案

---

## 目录

1. [项目概述](#1-项目概述)
2. [项目结构](#2-项目结构)
3. [系统架构](#3-系统架构)
4. [核心模块职责](#4-核心模块职责)
5. [关键组件说明](#5-关键组件说明)
6. [网络架构](#6-网络架构)
7. [数据流与交互](#7-数据流与交互)
8. [配置管理](#8-配置管理)
9. [设备集成](#9-设备集成)
10. [技术栈与依赖](#10-技术栈与依赖)
11. [项目运行方式](#11-项目运行方式)
12. [已知限制与风险](#12-已知限制与风险)
13. [开发路线图](#13-开发路线图)

---

## 1. 项目概述

AgentHomeAssistant 是一个智能家居自动化方案，核心设计理念是：

- **Agent 驱动**：使用 Hermes Agent 作为智能核心，支持自然语言交互
- **自然语言配置**：通过对话即可创建、修改场景，无需手动编辑配置
- **灵活可扩展**：Agent 可自由替换，适配器模式解耦 Home Assistant
- **YAML + Web UI**：核心配置版本化管理，可视化配置灵活调整

项目处于**规划与设计阶段**，尚未进入实际编码开发。当前仓库包含完整的架构设计文档和网络方案可行性分析。

---

## 2. 项目结构

```
AgentHomeAssistant/
├── README.md                              # 项目主文档，包含架构设计和使用说明
├── docs/
│   └── dual-router-feasibility-analysis.md # 双路由网络方案可行性分析报告
└── CODE_WIKI.md                           # 本文档 - Code Wiki
```

### 文件说明

| 文件 | 职责 | 内容概要 |
|------|------|----------|
| `README.md` | 项目主入口文档 | 系统架构、组件说明、配置管理、使用示例、设备清单、技术栈 |
| `docs/dual-router-feasibility-analysis.md` | 网络方案技术报告 | 双路由架构可行性评估、硬件选型、风险评估、替代方案对比 |

---

## 3. 系统架构

系统采用**四层架构**设计，自上而下分别为：

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户层 (User Layer)                       │
│   Web UI │ 语音输入 (Siri) │ 自然语言对话                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Agent 层 (Agent Layer)                     │
│   Hermes Agent (可替换) ← AgentBridge 适配器                     │
│   · NLU · 意图识别 · 对话管理 · 语义记忆                         │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP / WebSocket
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Middleware 层 (Middleware Layer)                │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ API 网关: Agent API │ Config API │ State API │ Scene Parser│   │
│   └──────────────────────────┬──────────────────────────────┘   │
│                              ▼                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ 核心引擎: Intent Router │ Scene Engine │ Scene Parser    │   │
│   └──────────────────────────┬──────────────────────────────┘   │
│              ┌───────────────┼───────────────┐                  │
│              ▼               ▼               ▼                  │
│   Config Manager      State Store      HA Adapter               │
│   (YAML + DB)         (状态记录)        (HA API 封装)            │
│       │                                    │                    │
│       ▼                                    ▼                    │
│   YAML 配置                         Device Alias Registry       │
│   (版本控制)                         (设备别名映射)              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│               Home Assistant 层 (Device Layer)                   │
│   米家设备 │ 传感器 │ 灯光 │ 空调/暖风 │ 投影仪                  │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              计算基础设施层 (Infrastructure Layer)                │
│   Mac Studio (本地 LLM) │ Mac Mini (Agent 节点) │ NAS (存储)     │
│   副路由器 OpenWrt (WireGuard + mDNS 中继)                       │
└─────────────────────────────────────────────────────────────────┘
```

### 架构设计原则

| 原则 | 说明 |
|------|------|
| 适配器模式 | Agent 和 Home Assistant 均通过适配器层解耦，支持替换 |
| 标准协议通信 | 层间通过 HTTP/WebSocket 等标准协议交互 |
| 配置即代码 | 核心配置使用 YAML 格式，支持 Git 版本管理 |
| 自然语言优先 | 场景创建/修改优先通过自然语言对话完成 |

---

## 4. 核心模块职责

### 4.1 Agent 层

| 组件 | 职责 | 可替换性 |
|------|------|----------|
| **Hermes Agent** | 自然语言理解 (NLU)、意图识别 (Intent Recognition)、对话管理 (Dialogue Management)、语义记忆 (Semantic Memory) | 可替换 |
| **AgentBridge** | 适配器层，统一 Agent 接口协议，屏蔽不同 Agent 实现差异 | 可替换 |

#### 核心意图定义

| 意图 | 标识 | 说明 |
|------|------|------|
| 定义场景 | `define_scene` | 通过自然语言创建新场景 |
| 修改场景 | `modify_scene` | 修改已有场景的设备配置 |
| 激活场景 | `activate_scene` | 执行某个场景的所有设备操作 |
| 控制设备 | `control_device` | 直接控制单个设备 |
| 查询状态 | `query_state` | 查询设备或环境状态 |

### 4.2 Middleware 层

Middleware 层是系统的核心，分为 **API 网关**、**核心引擎** 和 **内部组件** 三个子层。

#### API 网关

| 组件 | 职责 | 类型 |
|------|------|------|
| **Agent API** | 对话接口，接收用户自然语言输入，返回 Agent 响应 | 对外接口 |
| **Config API** | 配置接口，管理设备注册、场景定义、别名映射 | 对外接口 |
| **State API** | 状态接口，查询设备实时状态和历史记录 | 对外接口 |
| **Scene Parser** | 解析自然语言场景定义为结构化配置 | 对外接口 |

#### 核心引擎

| 组件 | 职责 | 说明 |
|------|------|------|
| **Intent Router** | 意图路由 | 将 Agent 识别的意图路由到对应的服务处理 |
| **Scene Engine** | 场景编排引擎 | 编排多设备场景的执行顺序和状态管理 |
| **Scene Parser** | 场景解析器 | 将自然语言场景描述解析为结构化 SceneConfig |

#### 内部组件

| 组件 | 职责 | 存储方式 |
|------|------|----------|
| **Config Manager** | 加载/验证/管理 YAML 配置文件 | YAML + SQLite |
| **State Store** | 记录设备状态、执行历史 | 内存/缓存 |
| **Device Alias Registry** | 设备自然语言名称 ↔ Home Assistant Entity ID 映射 | YAML |
| **HA Adapter** | 封装 Home Assistant REST API / WebSocket 接口 | 可替换适配器 |

### 4.3 Home Assistant 层

Home Assistant 作为智能家居核心平台，负责：

- 设备接入与协议转换（Zigbee、WiFi、蓝牙等）
- 设备状态管理
- 提供 REST API 和 WebSocket 接口供上层调用

### 4.4 计算基础设施层

| 设备 | 角色 | 主要功能 | 网络位置 |
|------|------|----------|----------|
| **Mac Studio** | 本地大模型 | 运行 Ollama/LocalAI，提供本地 LLM 推理服务 | 主网络 192.168.1.0/24 |
| **Mac Mini** | Agent 控制节点 | 运行 Hermes Agent 实例，负责自动化决策 | 主网络 (安全隔离) |
| **NAS** | 数据中心 | 文件存储、媒体服务、数据库备份 | 主网络 |
| **副路由器 (OpenWrt)** | 工作网络网关 | WireGuard 隧道、mDNS 中继、NAT 穿透 | 桥接主网络/工作子网 |

---

## 5. 关键组件说明

### 5.1 Scene Parser（场景解析器）

**职责**：将自然语言场景描述解析为结构化的 `SceneConfig`。

**解析流程**：

```
"灯光调到最暗，拉上窗帘并且打开投影仪"
        │
        ▼
  分词 & 意图提取
        │
        ├── "灯光调到最暗" → entity: light.living_room, service: turn_on, brightness: 0
        ├── "拉上窗帘"     → entity: cover.living_room_curtain, service: close_cover
        └── "打开投影仪"   → entity: media_player.xiaomi_projector, service: turn_on
        │
        ▼
  生成 SceneConfig (YAML)
```

**操作映射规则**：

| 自然语言描述 | 解析结果 |
|-------------|----------|
| 调暗 / 调到最暗 | `brightness: 0` |
| 调亮 / 调到最亮 | `brightness: 100` |
| 拉上窗帘 / 关窗帘 | `service: close_cover` |
| 打开投影仪 / 开投影 | `service: turn_on` |
| 调高温 / 调高温度 | `temperature: +2` |
| 调低温 / 调低温度 | `temperature: -2` |

### 5.2 Device Alias Registry（设备别名注册表）

**职责**：维护自然语言设备名称到 Home Assistant Entity ID 的映射关系。

| 自然语言 | Entity ID |
|----------|-----------|
| 灯光 / 客厅灯 | `light.living_room` |
| 窗帘 / 客厅窗帘 | `cover.living_room_curtain` |
| 投影仪 / 投影 | `media_player.xiaomi_projector` |
| 暖风机 | `climate.xiaomi_heater` |
| 净化器 / 空气净化器 | `air_quality.xiaomi_air_purifier` |

### 5.3 HA Adapter（Home Assistant 适配器）

**职责**：封装 Home Assistant 的 REST API 和 WebSocket 接口，提供统一的上层调用接口。

**关键接口**（规划）：

| 接口 | 方法 | 说明 |
|------|------|------|
| 设备控制 | `POST /api/services/{domain}/{service}` | 调用 HA 服务控制设备 |
| 状态查询 | `GET /api/states/{entity_id}` | 查询设备当前状态 |
| 事件订阅 | `WebSocket` | 实时监听设备状态变化 |

### 5.4 Config Manager（配置管理器）

**职责**：加载、验证和管理 YAML 配置文件，支持 Git 版本控制。

**配置类型**：

| 配置类型 | 存储方式 | 版本控制 |
|----------|----------|----------|
| 设备注册 | YAML | Git 管理 |
| 场景定义 | YAML | Git 管理 |
| 设备别名 | YAML | Git 管理 |
| 用户偏好 | 数据库 (SQLite) | 运行时存储 |
| 设备状态 | 内存/缓存 | 实时数据 |

---

## 6. 网络架构

### 6.1 双路由方案

采用主路由器 + 副路由器双路由架构，实现家庭网络与工作网络的物理隔离。

```
互联网
  │
  ▼
光猫 (桥接模式)
  │
  ▼
主路由器 (原厂固件, 192.168.1.1, WiFi: "Home")
  │
  ├── 主网络 192.168.1.0/24
  │   ├── NAS / Mac Studio / Mac Mini / 智能家居设备
  │   │
  │   └── 副路由器 (OpenWrt)
  │       ├── WAN: DHCP → 192.168.1.x
  │       ├── LAN: 192.168.2.1
  │       ├── WiFi: "Work"
  │       ├── WireGuard 隧道 (连接公司网络)
  │       ├── avahi-daemon (mDNS 中继)
  │       └── NAT (MASQUERADE, 穿透访问主网络)
  │
  └── 工作子网 192.168.2.0/24
      └── 工作设备 (切换 WiFi 即可接入)
```

### 6.2 数据流路径

| 场景 | 流量路径 |
|------|---------|
| 工作设备 → 公司网络 | 设备 → 副路由器 → WireGuard 隧道 → 公司网络 |
| 工作设备 → NAS | 设备 → 副路由器 NAT → 主网络 → NAS |
| 工作设备 → AirPlay | 设备 mDNS → avahi 中继 → 主网络 AirPlay 设备 → 副路由器 NAT → 设备 |
| 工作设备 → 智能家居 (Agent) | 设备 → HA API (TCP) → 副路由器 NAT → 主网络 HA → 智能家居 |
| 家庭设备 → 互联网 | 设备 → 主路由器 → 互联网（不经过副路由器） |

### 6.3 副路由器配置要点

| 配置项 | 关键参数 |
|--------|----------|
| LAN 接口 | `192.168.2.1/24` |
| WAN 接口 | DHCP，从主路由获取 `192.168.1.x` |
| DHCP 服务 | 范围 `192.168.2.100-200`，租期 12h |
| 防火墙 | WAN 区域开启 `masq` (NAT) + `mtu_fix` (MSS Clamping) |
| WireGuard | `persistent_keepalive 25`，`allowed_ips 0.0.0.0/0` |
| avahi-daemon | reflector 模式，过滤 `_airplay._tcp,_raop._tcp,_ipp._tcp,_hap._tcp` |

### 6.4 硬件选型

| 型号 | SoC | 价格 | 备注 |
|------|-----|------|------|
| 小米 AX3000T (RD03) | MT7981B | ~¥130 | 性价比首选，**必须 RD03 版本** |
| GL.iNet MT3000 | MT7981B | ~¥300 | 开箱即用，原生 OpenWrt |
| CMCC RAX3000M | MT7981B | ~¥200 | 均衡之选，4 千兆口 + USB |

---

## 7. 数据流与交互

### 7.1 自然语言创建场景（完整流程）

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
  │     ├─► "灯光"   → light.living_room
  │     ├─► "窗帘"   → cover.living_room_curtain
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

### 7.2 执行场景

```
用户："打开观影模式"
        │
        ▼
Hermes Agent → 识别意图: activate_scene
        │
        ▼
Intent Router → Scene Engine
        │
        ▼
Scene Engine 加载场景配置
  ├─► HA Adapter: light.living_room → turn_on (brightness: 0)
  ├─► HA Adapter: cover.living_room_curtain → close_cover
  └─► HA Adapter: media_player.xiaomi_projector → turn_on
        │
        ▼
State Store 记录执行结果
        │
        ▼
返回执行结果给用户
```

### 7.3 控制体系优先级

| 优先级 | 控制方式 | 协议 | 跨子网可靠性 |
|--------|---------|------|-------------|
| 1 (最高) | Agent 系统 | HTTP/WebSocket (TCP) | 完全可靠 |
| 2 | Home Assistant | HTTP/WebSocket (TCP) | 完全可靠 |
| 3 (最低) | HomeKit | mDNS + Bonjour | 依赖 mDNS 中继，偶发问题 |

---

## 8. 配置管理

### 8.1 场景定义格式

```yaml
# scenes/movie_mode.yaml
name: "观影模式"
description: "自动开启观影环境"
source: "natural_language"  # 标记为自然语言创建

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

### 8.2 配置存储策略

| 配置类型 | 存储方式 | 版本控制 | 说明 |
|----------|----------|----------|------|
| 设备注册 | YAML | Git | 设备元信息和能力描述 |
| 场景定义 | YAML | Git | 场景名称、描述、设备操作列表 |
| 设备别名 | YAML | Git | 自然语言 ↔ Entity ID 映射 |
| 用户偏好 | SQLite | 无 | 运行时动态数据 |
| 设备状态 | 内存/缓存 | 无 | 实时状态数据 |

---

## 9. 设备集成

### 9.1 已接入设备

| 品牌/设备 | 类型 | 集成方式 |
|-----------|------|----------|
| 绿米 (Aqara) 传感器/开关/窗帘电机 | 智能家居 | HomeKit 原生 + HA 集成 |
| 欧瑞博 (ORVIBO) 智能面板/照明 | 智能家居 | HA 集成 |
| 米家激光投影仪 | 媒体设备 | HA 集成 |
| Apple TV 4K | 囆媒体设备 | HomeKit 原生 |
| 小米踢脚线暖风机 | 环境控制 | HA 集成 |
| 小米空气净化器 | 环境控制 | HA 集成 |
| iPhone | 移动设备 | HomeKit / Siri 控制 |

### 9.2 建议补充设备

| 设备 | 用途 |
|------|------|
| Aqara 人体存在传感器 | 人来自动开设备，人走自动关闭节能 |
| 温湿度传感器 | 为暖风机提供准确温度数据 |
| PM2.5 传感器 | 为空气净化器提供决策数据 |
| 智能开关面板 | 物理按键 + 自动化双重控制 |
| UPS 不间断电源 | 保护核心设备免受电力波动影响 |

---

## 10. 技术栈与依赖

### 10.1 核心技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| Agent | Hermes Agent | 可替换的智能 Agent |
| 智能家居平台 | Home Assistant | 设备接入与状态管理 |
| API 网关 | FastAPI / Flask | RESTful API 服务 |
| 配置存储 | YAML + SQLite | 版本化配置 + 运行时数据 |
| 设备集成 | HA REST API / WebSocket | 与 Home Assistant 通信 |
| 本地 LLM | Ollama / LocalAI | Mac Studio 上运行的推理引擎 |
| 工作网络 | OpenWrt + WireGuard + avahi-daemon | VPN 隧道 + mDNS 中继 |

### 10.2 依赖关系图

```
Hermes Agent
    │
    ├──► 本地 LLM (Ollama/LocalAI on Mac Studio)
    │       语义理解、意图识别
    │
    └──► AgentBridge
            │
            └──► Middleware (FastAPI/Flask)
                    │
                    ├──► Config Manager ──► YAML 文件 (Git)
                    ├──► State Store ─────► SQLite / 内存缓存
                    ├──► HA Adapter ──────► Home Assistant API
                    └──► Device Alias Registry ──► YAML 文件
```

### 10.3 外部服务依赖

| 依赖 | 用途 | 必要性 |
|------|------|--------|
| Home Assistant | 智能家居控制核心 | 必需 |
| WireGuard 服务端 | 公司网络 VPN 接入 | 工作网络必需 |
| avahi-daemon | mDNS 跨子网中继 | HomeKit/AirPlay 跨子网必需 |
| Ollama/LocalAI | 本地 LLM 推理 | Agent 智能能力必需 |

---

## 11. 项目运行方式

> **注意**：项目目前处于规划与设计阶段，以下为规划的运行方式。

### 11.1 环境要求

| 组件 | 要求 |
|------|------|
| Home Assistant | 已部署并运行，设备已接入 |
| Mac Mini | 运行 Hermes Agent 实例 |
| Mac Studio | 运行本地 LLM (Ollama/LocalAI) |
| Python | 3.10+ (Middleware 服务) |
| NAS | 文件存储和备份服务 |

### 11.2 规划的部署方式

**方案一：本地直接运行**

```bash
# Middleware 服务
pip install -r requirements.txt
python -m middleware.main  # 启动 API 网关

# Hermes Agent (Mac Mini)
python -m agent.hermes  # 启动 Agent 服务
```

**方案二：Docker 部署**

```bash
docker-compose up -d  # 一键启动所有服务
```

### 11.3 副路由器配置步骤

1. 刷 OpenWrt 固件
2. 配置基础网络 (WAN/LAN/DHCP)
3. 配置防火墙 (NAT + MSS Clamping)
4. 配置 WireGuard 隧道
5. 安装并配置 avahi-daemon mDNS 中继
6. 测试 NAS 跨子网访问
7. 测试 AirPlay / HomeKit 跨子网功能

---

## 12. 已知限制与风险

### 12.1 技术限制

| 限制 | 影响 | 缓解措施 |
|------|------|---------|
| HomeKit 跨子网偶发"无响应" | mDNS 公告超时导致 | 优先使用 Agent/HA 控制 (TCP)；HomeKit 仅作备用 |
| AirPlay 发现延迟 5-15 秒 | 首次发现比同网段慢 | 启用 reflector-quick-join；可接受 |
| 主网络无法主动访问工作子网 | NAT 导致单向可访问 | 当前需求不需要反向访问 |
| HomeKit 首次配对需同网段 | 跨子网配对可能失败 | 所有设备在主网配对完成后再使用 |

### 12.2 风险矩阵

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| HomeKit 间歇性"无响应" | 高 | 低 | 主要控制路径为 Agent/HA (TCP) |
| WireGuard 隧道断线 | 低 | 高 | `persistent_keepalive 25` + Watchdog |
| 副路由器硬件故障 | 低 | 中 | 不影响家庭网络；更换成本低 |
| avahi-daemon 与 umdns 冲突 | 中 | 低 | 安装后禁用 umdns |
| 双 NAT 导致 MTU 问题 | 低 | 中 | 开启 `mtu_fix` |
| 小米 AX3000T 买错版本 | 中 | 高 | 购买前确认 RD03 版本 |

---

## 13. 开发路线图

### 阶段一：网络基础设施

- [ ] 采购副路由器 (推荐小米 AX3000T RD03)
- [ ] 刷 OpenWrt 固件
- [ ] 配置副路由器基础网络 (WAN/LAN/DHCP)
- [ ] 配置 WireGuard 隧道连接公司网络
- [ ] 配置 avahi-daemon mDNS 中继
- [ ] 测试 NAS 跨子网访问
- [ ] 测试 AirPlay / HomeKit 跨子网功能

### 阶段二：Middleware 核心服务开发

- [ ] 确定集成方案
- [ ] 搭建运行环境 (本地 / Docker)
- [ ] 开发 Config Manager 配置管理
- [ ] 开发 State Store 状态存储
- [ ] 开发 HA Adapter Home Assistant 适配器
- [ ] 开发 Scene Parser 场景解析器
- [ ] 开发 Scene Engine 场景编排引擎
- [ ] 开发 API 网关 (Agent API / Config API / State API)

### 阶段三：Agent 集成与测试

- [ ] 配置设备别名映射
- [ ] 接入 Home Assistant
- [ ] 集成 Hermes Agent
- [ ] 测试基础设备控制
- [ ] 测试自然语言场景创建

### 阶段四：UI 与优化

- [ ] 开发 Web UI 可视化配置界面
- [ ] 编写场景自动化
- [ ] 端到端测试优化

---

## 附录：参考文档

- [双路由网络方案可行性分析](docs/dual-router-feasibility-analysis.md) - 详细的技术可行性评估报告，包含硬件选型、性能基准、替代方案对比

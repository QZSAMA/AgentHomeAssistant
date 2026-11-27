# AgentHomeAssistant - Code Wiki

> **当前网络与影音（2026-11-26，v1.6）**：Apple TV仅已有1台，放大厅接客厅ES206；投影仪主放主卧、可移动，Wi-Fi接入不插网线。电竞房ES210的2.5G口仅分配Fusion上联、PC×2、Mac mini，**用4余4**；10G电口给Mac Studio、SFP+留未来NAS。Fusion四LAN分别接中央/电竞/电脑墙口A/B，中央SFP+10G连客厅；中央四AP/两M200 PoE，客厅五铜口含Apple TV和J3455全满。当前[拓扑与端口](docs/network-topology.md)、[施工清单](docs/network-placement-and-cabling-plan.md)、[影音规划](docs/av-and-gaming-layout.md)为当前接线依据。

> **光猫接入决定（2026-11-18）**：武汉电信 1,000 Mbps，当前采用运营商光猫 Internet 桥接 → Fusion 2.5G 普通版 PPPoE 拨号，尚未实施/验收。XG-PON 仅为备用研究假设，实际制式/原光猫型号待核；旧规划上行 30 Mbps 未实测。见[当前接入与验收](docs/wan-bridge-plan.md)、[替换设备/案例/视频备用研究](docs/ont-replacement-backup-research.md)。本轮不采购新光猫、猫棒或 MC420L；Omada 已下单 7 台、另待购 Fusion 的状态与同一家庭 LAN 方案不变。
> 当前网络订单为 ES206×1、ES210×2、EAP775-Wall×3、EAP772×1；现行摆位为客厅ES206、中央/电竞ES210各1，7台已下单待到货验收，商品 $828、总额 $901.49；Fusion 不在本单。见[订单](docs/network-order-20261118.md)和[现行拓扑](docs/network-topology.md)。

> **2026-11-21智能配件更新**：原绿米19,324元签字单不变。[设备增补Excel](outputs/aqara-supplement-20261118/全屋智能新增设备清单.xlsx)已补型号、官方/购买链接及核验状态，保留31条记录（独立门铃已取消、电竞房独立温湿度计暂不买），备选不叠加数量。两卫改选奥普米家版，完整SKU待定，拟经HA Xiaomi Home联动；米家不等于直连Aqara。门锁要求可视猫眼，当前官网较早猫眼款仅待核候选。见[型号核验](docs/aqara-model-verification-20261121.md)、[详细计划](docs/aqara-supplement-plan-20261118.md)与[全屋查漏](docs/smart-home-supplement-audit-20261118.md)。次卧照明不加、窗户仅检测，两卫FP310复用；欧瑞博仍覆盖空调/新风/地暖/热水器。未下单，实际库存待核。

## 装修图纸与核心网络位置（2026-11-27整理）

**吊顶/布线补充**：用户确认大厅及入户过道有吊顶或局部吊顶，[设备点位与埋线草案](docs/network-placement-and-cabling-plan.md)已给出当前9条远端铜缆、中央—客厅光纤与本地支线表。公共区走顶、房内沿允许墙面下引；点位、标高、穿墙和长度仍待现场签认，硬件订单数量不变，按现行逐线表交底。

[装修布置图、尺寸标注图与点位记录](docs/floorplan-and-network-locations.md)已归档。弱电箱在**入户门左侧**，光猫、Fusion及中央ES210XPP-M2规划在该箱或附近通风核心柜，9条在用远端铜缆与客厅光纤从此汇聚。原箱容量、散热、插座、完整电气点位与实际管线路径仍须现场核验；图示房间尺寸不是线缆下料长度。当前已确认订单数量与金额不变。

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

> 下图为旧架构示例，不是当前采购或接入清单；本轮奥普米家版例外按独立型号核验记录，不由下图授权其他米家设备。本文出现的 `xiaomi_*` 实体 ID 均是仓库旧示例/Mock 数据，不是当前设备登记或部署配置；真实接入须以获选设备及验收记录为准。

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

### 4.4 计算基础设施层（历史规划，未核验）

> **⚠️ 不代表已购买或已部署**：设备角色和网络位置仅用于早期架构讨论。

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

当前物理方案为 [v1.6](docs/network-topology.md)：光猫桥接 → Fusion；Fusion 的四个 LAN 接中央 ES210、电竞房 ES210、两个普通电脑墙口。中央以 10G SFP+ 光纤级联客厅 ES206，四台 AP 和两台 M200 独立回中央 PoE。J3455 与唯一 Apple TV 规划放在客厅，投影仪通过 Wi-Fi 移动使用。

全部设备在同一家庭 LAN，Fusion 保留主网关、唯一 DHCP 和普通 DNS。少量指定终端手动选择 J3455 OpenWrt，失败时切回普通参数；不按早期双路由示例另建工作子网。以[已批准设计](docs/superpowers/specs/2026-11-05-home-device-rule-routing-design.md)及[实施计划](docs/superpowers/plans/2026-11-05-home-device-rule-routing.md)为准。

当前设备已下单/待购状态见[订单](docs/network-order-20261118.md)与[采购 BOM](docs/purchase-bom.md)，现场端口、供电和恢复仍待验收。

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

### 9.1 历史设备清单（未核验）

> **⚠️ 未核验 / 禁止按此采购或视为已部署**：当前品牌方向以台账为准，Aqara/绿米为主；ORVIBO/欧瑞博只评估具体空调型号，不采购本文旧的面板/照明。

| 品牌/设备 | 类型 | 集成方式 |
|-----------|------|----------|
| 绿米 (Aqara) 传感器/开关/窗帘电机（历史候选） | 智能家居 | 具体型号的 HomeKit/HA 兼容性待验证 |
| 欧瑞博 (ORVIBO) 通用面板/照明（历史候选，当前不采购） | 智能家居 | 2026-11-18更新为空调/新风/地暖/热水器四类方案，具体SKU及接入待核 |
| 米家激光投影仪（用户确认已有） | 媒体设备 | 现有设备复用，主卧为主、可移动，Wi-Fi接入不插网线；不新增采购，HA集成待实机核验 |
| Apple TV 4K | 囆媒体设备 | HomeKit 原生 |
| 小米踢脚线暖风机（历史示例，当前排除） | 环境控制 | 旧集成示例，未核验；不代表已有 |
| 小米空气净化器（历史示例，当前排除） | 环境控制 | 旧集成示例，未核验；不代表已有 |
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
| Home Assistant | 规划依赖，尚无部署/设备接入验收记录 |
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

### 11.3 家庭网络部署

执行[同一 LAN 按设备选用 OpenWrt 实施计划](docs/superpowers/plans/2026-11-05-home-device-rule-routing.md)，按[验收与应急单](docs/validation/home-device-rule-routing.md)逐项记录结果。设备部署仍未完成。

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
| 小米 AX3000T 买错版本（历史风险） | 中 | 高 | 当前已排除该品牌，不再形成采购待办 |

---

## 13. 开发路线图

### 阶段一：网络基础设施

- [ ] 完成已下单7台Omada设备到货验收，并核实Fusion购买。
- [ ] 按[v1.6拓扑](docs/network-topology.md)与[当前实施计划](docs/superpowers/plans/2026-11-05-home-device-rule-routing.md)配置同一家庭LAN及指定终端分流。
- [ ] 按[验收单](docs/validation/home-device-rule-routing.md)验证访问、双栈与故障切回，现场项仍未运行。

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

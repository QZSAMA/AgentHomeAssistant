# AgentHomeAssistant

> **2026-10-20 当前暂定定稿：3A三频。** 普通Fusion×1、ES206XPP-M2×2（中央/大厅）、ES210XPP-M2×1（电竞房）、EAP775-Wall×2（主卧/电竞房）、EAP772×1（大厅吊顶）。次卧只保留Cat6A/RJ45。双频725×2+723×1保留预算备选。网络设备Amazon参考$1,229.93，双频$1,059.93（10/20页面价，不含税运与施工）。[当前BOM](docs/purchase-bom.md)、[最新拓扑](docs/network-topology.md)、[方案比较](docs/network-cost-optimization.md)、[链接核对记录](docs/network-link-audit.md)维护现行信息；以下旧日期的四AP/中央ES210与旧预算是历史方案。

<details>
<summary>2026-10-19及以前的项目说明（历史，非当前采购/施工口径）</summary>

> **2026-10-19 第三版成本优化（用户确认网络采购主案）**：[Omada成本优化Excel](outputs/network-value-20261019/基础网络采购与装修交底_第三版Omada成本优化.xlsx)已按最新决定改为交换机直接PoE，不买独立供电器或SM5310-T。用户确认3A：Fusion 2.5G普通版 + 中央ES206XPP-M2 + 工作室ES210XPP-M2 + 大厅ES206XPP-M2；Amazon条件预算$1,229.20。3B用Fusion 2.5G PoE取代普通Fusion与中央交换机，Amazon $1,242.07，仅保留为比较。两种拓扑、端口、PoE、施工和验收边界见[第三版说明](docs/network-cost-optimization.md)。725-Wall仍须书面确认US V2四下联口；设备均未购买或部署。

> **2026-10-19 双频备选**：[不含6GHz的Wi-Fi 7对照Excel](outputs/network-dualband-20261019/基础网络采购与装修交底_双频WiFi7对照版.xlsx)已另存，含拓扑、BOM、施工与差价。四AP按今日Amazon页面价省$215、官方商城省$220；725-Wall必须先确认US V2四下联口及对应报价。原三频版保留，尚未批准换型。详见[差价与版本核验](docs/ap-6ghz-selection-price-comparison.md)。

> **2026-10-16 当前采购/装修范围**：[基础网络采购与装修交底 Excel](outputs/network-renovation-20261016/基础网络采购与装修交底.xlsx)覆盖网络硬件、材料、逐条布线、端口/PoE、配置和分阶段验收。高速NAS、UPS搬入后再考虑，不作为入住前必购；NAS要求自带10G SFP+，不买网卡，介质待实物确认。Mac走原生10G RJ45；Apple TV 4K旧款、米家激光投影仪、树莓派均已有，不重复购买。壁挂屏先试已有杂牌安卓，不合适再选二手iPad mini/便宜iPad，暂未定。J3455已确认PCIe 2.0 x1，TX201为兼容性待验的首选候选。下方较早的固定DAC与UPS入住前要求由本条更新；不改四主干/两房间箱/三面板一吊顶。

基于 Apple 生态 + Aqara（绿米）智能家居 + Hermes Agent 的个人家庭助理自动化方案

> **当前基础设施事实源**：[家庭基础设施登记与实施台账](docs/home-infrastructure-register.md)。
> **采购与报价（2026-10-15）**：[完整采购BOM](docs/purchase-bom.md)区分已确认、暂选与未决；NAS已确认靠近工作室交换机，当前用兼容SFP+ DAC短线。四区域不额外预埋光纤，保留可抽换弱电管/牵引线。
> **核心设备最新状态（2026-10-15）**：用户暂定 **Fusion 2.5G 普通版 ×1（非 PoE 版）**作为主路由，使用其内置 Omada 控制器；ER707-M2 和 J3455 上的 Omada Linux VM 撤出当前计划，OC200 不采购。大厅 ES206XPP-M2 选型保留；中央仍推荐 ES210XPP-M2（90W/口、200W总PoE），待用户确认。Home Assistant 继续在现有 J3455/Proxmox 上新增独立 HAOS VM，尚未实施，须核资源、SSD、备份与 UPS。Fusion 未购/未部署，保留运营商光猫桥接；普通版无 PoE、无 SFP，不替代中央 PoE 交换机。功能、价格与电源证据见[网络调研](docs/tplink-network-research.md#25-fusion-25g-普通版暂定与电源核验2026-10-15)。
> **J3455与协调器补充（2026-10-15）**：J3455现为1GbE，用户计划升级2.5G网卡，仍使用电竞房已分配的同一个交换机端口；型号、Proxmox驱动与桥接迁移待验证。HA经LAN连接有线网关/以太网协调器，不默认使用USB直通；Aqara网关集成与HA直管协调器是不同路径，具体型号和协议仍待选，见[智能家居接法](docs/smart-home-topology.md#21-各协议的实际接法)。
> **PoE 与端口复核（2026-10-15）**：中央推荐ES210XPP-M2两卧室AP保守规划117W/200W，未来PoE可按需增加独立ES206XPP-M2。用户确认电竞房不扩交换机；继续使用单台ES210XPP-M2。工作室EAP775-Wall除上联外还有1×2.5G+3×1G数据下联，Apple TV/投影可改接两个1G口，从而释放两个ES210端口；J3455/HA、Mac、NAS和PC保持交换机直连，不使用AP PoE Out。见[网络拓扑](docs/network-topology.md#22-交换机-poe-与端口复核2026-10-15)及[BOM](docs/device-selection-list.md#63-交换机与-poe-预算)。
> **6GHz 专项研究（2026-10-13）**：[中国大陆 Wi-Fi 7 / 6GHz 调研报告](docs/wifi7-6ghz-mainland-china-research.md)已记录官方限制、公开成功/失败案例与配置方法。存在特定组合的技术成功自述，但未发现大陆普通住宅 WLAN 开放依据；Apple 官方不支持在大陆使用 6GHz，EAP775-Wall 未经本项目实测。保留暂选型号，6GHz 不计入部署保证能力。
> **AP 优先级确认（2026-10-14）**：支持6GHz的三频设备保持第一优先，主卧/次卧/工作室各暂选 **EAP775-Wall ×1**，大厅 **EAP772 ×1** 为第一优先候选，均按2.5G有线回程。[BOM](docs/device-selection-list.md#64-按最新拓扑更新的候选购买清单)与v1.2拓扑型号/数量不变；[AP有无6GHz选型与价格对比报告](docs/ap-6ghz-selection-price-comparison.md)保存美国官方/Amazon报价、725版本差异及快速更新流程，双频725/723仅留备选。地区合规、发货版本及PoE仍须核验，不代表已购买或大陆6GHz可启用。
> **Apple设备最新决定（2026-10-15）**：大厅 **Apple HomeView非壁挂／桌面版×1已确认**，通过大厅AP Wi-Fi，使用随箱电源，不买壁挂版/底座。壁挂另用平板电脑或iPad，型号/数量/点位/供电待选。HomeView美国预购$299、11月13日供货；三房mini 2建议各1，美$149/大陆¥1,099、10月30日供货，代际/数量/地区仍待确认。用户接受英语Siri AI，大陆服务/账户/配套设备仍待验；未购/未部署，不改四主干/AP PoE。见[官方核验与建议](docs/apple-home-devices-2026.md)。
> README 中较早的设备状态和网络方案用于背景参考；采购、户型、AP布点、Apple HomeView和模型计划以台账为准。
> **当前品牌范围（用户已确认）**：Apple 生态、Aqara/绿米为主；网络设备选择 TP-Link；ORVIBO/欧瑞博仅考虑空调。**不新增小米/米家、华为设备**；用户已有米家激光投影仪继续复用，不重复采购。其他旧小米设备示例不视为已有。
> **网络拓扑 v1.2（2026-10-14）：四条主干2.5G，仅电竞房Mac/NAS本地10G**。网络采购方向为 **TP-Link Omada**；主卧/次卧各一条Cat6A/2.5G直达EAP775-Wall，不设设备箱/交换机，电脑等有线设备接AP下联（1×2.5G+3×1G）；电竞房/大厅各保留一箱一交换机。电竞房已选 **ES210XPP-M2 ×1**，10G RJ45给Mac Studio、10G SFP+给未来高速NAS；J3455及其他关键终端接电竞房交换机。完整直连表会占用八个2.5G口和两个10G口；Apple TV、投影改接工作室AP的两个1G下联后可释放两个交换机2.5G口，AP仍余1×2.5G+1×1G。现有1G/100M终端按实际接口；核心网络仍在弱电箱附近机柜，中央至少两口需匹配卧室AP PoE。规格与采购入口见 [TP-Link 网络产品调研](docs/tplink-network-research.md)。

> 最新候选购买 BOM 见 [设备清单第6.4节](docs/device-selection-list.md#64-按最新拓扑更新的候选购买清单)：电竞房只用一台ES210XPP-M2，不增加交换机；完整直连表可占满十口，但工作室AP下联可承载Apple TV/投影等低带宽终端。中央五连接，建议≥8×2.5G且至少两口匹配EAP775-Wall PoE输入/功率。两卧室无交换机/箱，三台面板AP均有1×2.5G+3×1G下联；不启用AP PoE Out。Omada 使用暂定 Fusion 的内置控制器，不另占交换机端口；HA 通过 J3455 的既有接入口联网（现1G，计划2.5G）。
>
> **⚠️ 历史内容警告（2026-10）**：本文下方的“双路由/副路由”、千兆交换机、ORVIBO面板/照明和“已接入设备”均为历史或未核验记录，禁止据此采购/施工。当前基线是 **AC（主路由器/网关）→ 中央匹配PoE的2.5G交换机 → 两卧室Wall AP（直达）/电竞房与大厅交换机 → 有线AP/终端**；AC不是无线控制器，也不是空调。

</details>

## 当前方案与图纸入口（2026-10-20）

| 文档 | 内容 |
|---|---|
| [装修原图与网络设备位置](docs/floorplan-and-network-locations.md) | 两张用户装修原图、局部尺寸边界；弱电箱在入户门左侧，四条Cat6A汇聚起点及现场核验清单 |
| [Apple HomeView / mini 2官方核验](docs/apple-home-devices-2026.md) | HomeView桌面版×1已确认、mini 2待选；官方规格/报价与地区限制，壁挂平板或iPad待选，不买HomeView壁挂底座 |
| [采购BOM与未决清单](docs/purchase-bom.md) | 当前3A三频七台设备、六列采购清单、10/20核验的Amazon入口/单价、双频备选、装修辅材与后置设备 |
| [全屋网络拓扑图](docs/network-topology.md) | 四条主干目标2.5G；主卧775、次卧RJ45预留、电竞房ES210/大厅ES206各一箱，电竞房775及大厅772交换机PoE直供；Mac/NAS本地10G |
| [大厅—电竞房影音与游戏连接规划](docs/av-and-gaming-layout.md) | 大厅电视、电竞房投影、Switch 双底座、PS5/PS TV Remote Play；两条约10m反向光纤 HDMI AOC 与复尺/施工要求 |
| [智能家居与 Thread 拓扑图](docs/smart-home-topology.md) | 可编辑 Mermaid 接入图；四个主要区域和两卫生间的 Wi-Fi、Zigbee、Matter over Thread 规划及 Apple Home/HA 控制关系 |
| [基础设施台账](docs/home-infrastructure-register.md) | 当前决定、已有/计划设备、模型计划与待验证事项的事实源 |
| [Wi-Fi 7 / 6GHz 大陆可用性研究](docs/wifi7-6ghz-mainland-china-research.md) | 法规与 Apple/Intel/Omada 限制、公开案例证据、正常配置与非官方方法边界、采购/验收门槛 |
| [AP 有无 6GHz 选型与价格对比](docs/ap-6ghz-selection-price-comparison.md) | 三频暂定定稿、双频保留备选；同三AP/同交换机，Amazon相差$170，US V2风险另核 |
| [设备选型清单](docs/device-selection-list.md) / [施工需求](docs/renovation-wiring-requirements.md) | 四条2.5G主干、两面板一吊顶、次卧RJ45预留、两房间箱、电源与分阶段验收；NAS/UPS后置 |
| [Hermes × HA 隔离实验指南](examples/hermes-ha-lab/README.md) / [验收记录](docs/validation/hermes-ha-lab.md) | 当前软件入口：固定官方插件、独立 profile、虚拟实体、只读 REST 探测与预期断言；真实联调仍为 `not_run` |

软件实验底座及只读断言已合入 `main`。可先运行 `python -m unittest discover -s tests/ha_lab -v` 复跑离线测试；这不安装 Hermes/HA、不连接真实家居，也不代表旧 Middleware 或真实集成已通过验收。准备隔离测试环境后，按实验指南逐项验证，不执行下方历史部署步骤。

房屋约 **100㎡、单层**，已收到并归档[装修布置图与尺寸标注图](docs/floorplan-and-network-locations.md)。**弱电箱在入户门左侧**，光猫、Fusion和中央交换机规划在该箱或附近通风核心柜，四条Cat6A由此汇聚。大厅/入户过道已确认有吊顶或局部吊顶，新增[设备点位与埋线草案](docs/network-placement-and-cabling-plan.md)及标注图；箱体、完整电气点位、实际管线路径与逐线长度仍待现场签认，Excel尚未写回该草案。计划宽带 **1000Mbps 下载 / 30Mbps 上传**。图纸是方案，不代表已安装。已有J3455：**16GB内存、10TB存储、千兆网口、Proxmox**，运行非官方群晖影音NAS与家庭代理/转发容器；最新规划接电竞房交换机、箱外摆放，未执行迁移。已决定在其 Proxmox 上新增独立 HAOS VM，尚未部署或完成资源验收；Omada 改用暂定 Fusion 的内置控制器。

Mac Studio采购目标为 **M5 Ultra、512GB统一内存、4TB内置SSD**，接电竞房原生10G RJ45，Apple美国配置页2026-10-15写512GB选项10月下旬提供，目标整机报价待开放后核验。未来高速NAS若新增，已确定放交换机附近，接同台交换机10G SFP+兼容DAC短线，NAS自带SFP+且不买网卡；介质待入住后选型。Mac↔NAS与Apple TV↔J3455在同VLAN内本地交换，不占2.5G中央上联；其他房间访问共享该上联，NAS磁盘/CPU和自身网口仍需验收。大厅HomeView已确认非壁挂／桌面版×1，Wi-Fi接大厅AP，未购/部署，大陆服务/账户/配套设备仍待验；壁挂另选平板或iPad，型号/数量/点位与供电待定。

UPS入住后再评估，装修先留位置、电源与通风；原至少1小时仅为后续评估目标，不作入住前购买/验收条件。当前只有主卧AP计中央PoE，电竞房/大厅AP由本地交换机供电；AP下联电脑不随PoE保活。后续按实测负载、分散供电位置及安全关机要求选UPS，不通过密封机柜隔音。

## 早期项目状态（历史记录，非最新验收）

> 更新时间：2026-06

### 项目时间线

| 阶段 | 时间 | 状态 | 说明 |
|------|------|------|------|
| 软件开发（阶段1） | 2026.06 - 2026.09 | 🟡 进行中 | 纯软件开发，无硬件依赖，Mock 测试 |
| 房屋交房 | 2026.09 | ⏳ 待定 | 交房后启动装修 |
| 装修协调期（阶段2） | 2026.09 - 2026.12 | ⏳ 待定 | 弱电布线、设备选型确认 |
| 设备安装与网络部署（阶段3） | 2026.12 - 2027.03 | ⏳ 待定 | HA 部署、设备接入、网络配置 |
| 系统集成与上线（阶段4） | 2027.03 - 2027.04 | ⏳ 待定 | 端到端测试、正式上线 |

### 设备现状

| 类别 | 设备 | 状态 | 备注 |
|------|------|------|------|
| 智能家居设备 | Apple TV 4K | ✅ 已有 | 可用于 HomeKit 测试 |
| 智能家居设备 | 投影仪 | ✅ 已有 | 待接入 HA |
| 计算设备 | MacBook | ✅ 已有 | 暂代 Mac Studio 做开发测试 |
| 计算设备 | Mac Studio | ⏳ 计划购买 | 最新：M5 Ultra，512GB统一内存+4TB SSD、10GbE接工作室交换机；Apple美国配置页2026-10-15写512GB选项10月下旬提供，目标整机精确报价待开放后核验 |
| 计算设备 / 现有 NAS | J3455 自建服务器 | ✅ 用户确认已有；HA 部署位置已定 | 16GB/10TB/现1GbE、计划2.5G/Proxmox，影音NAS及代理服务保留；计划电竞房箱外，未迁移；新增独立 HAOS VM 尚未部署/验收；Omada 由暂定 Fusion 承载 |
| 计算设备（本轮接入计划） | Mac Mini | 1G终端，部署状态待核 | 电竞房已分配1个铜口，不因接入规划追加整机采购 |
| 存储设备（未来扩购） | 高速 NAS | ⏳ 待评估，非必购 | 与J3455区分；电竞房10G SFP+预留，型号/磁盘入住后再选，自带SFP+且不另买网卡，不再规划中央接入 |
| 网络设备（历史候选） | 副路由器 | ⏳ 未核验 | 不属于当前 AP 主干；禁止按此行采购 |
| 智能家居设备（历史合并项） | 绿米/欧瑞博 | ⏳ 未核验 | 当前方向以台账为准：Aqara 为主，ORVIBO 仅评估空调 |

### 软件开发进度

| 模块 | 状态 | 说明 |
|------|------|------|
| 架构设计 | ✅ 完成 | 四层架构、组件职责、网络方案 |
| Middleware 核心框架 | 🟡 开发中 | Config Manager、Scene Parser 等模块开发中 |
| HA Adapter | 🟡 Mock 模式 | 抽象接口已定义，真实实现待 HA 部署 |
| Agent 集成 | ⏳ 待开始 | Hermes Agent 调研中 |
| 测试基础设施 | ⏳ 待开始 | 单元测试 + Mock 全链路测试 |

> 早期开发时序文档未随仓库保留。当前设备、网络和部署待办见[家庭基础设施登记与实施台账](docs/home-infrastructure-register.md)。

## 核心特性

- 🤖 **Agent 驱动**：使用 Hermes Agent 作为智能核心，支持自然语言交互
- 🔧 **自然语言配置**：通过对话即可创建、修改场景，无需手动编辑配置
- 🔄 **灵活可扩展**：Agent 可自由替换，适配器模式解耦 Home Assistant
- ⚙️ **YAML + Web UI**：核心配置版本化管理，可视化配置灵活调整

## 网络架构

### 双路由方案（历史规划/可选工作网络）

> **⚠️ 历史规划 / 未核验 / 禁止按此采购施工**：本节只记录可选的工作网络叠加方案，不是当前家庭 AP 主干拓扑。副路由器、旧千兆设备和本节的地址/配置必须经过台账与现场验证后才能采用。

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
| 工作设备 → 智能家居 (Agent) | 设备 → Home Assistant API (TCP) → 副路由器 NAT → 主网络 HA → 智能家居 |
| 家庭设备 → 互联网 | 设备 → 主路由器 → 互联网（不经过副路由器） |

### 副路由器配置详情

#### 硬件选型（历史候选，不符合当前 2.5G+ 有线 AP 基线）

> **⚠️ 不得作为当前采购清单**：以下型号仅用于旧双路由方案的背景比较。

| 型号 | SoC | WiFi | 网口 | OpenWrt | 价格 | 备注 |
|------|-----|------|------|---------|------|------|
| 小米 AX3000T (RD03，已排除) | MT7981B | WiFi 6 AX3000 | 4× 千兆 | 23.05+ | ~¥130 | 历史比较项；不在当前采购/部署范围 |
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
| HomeKit 跨子网偶发"无响应" | mDNS 公告超时导致 | 优先使用 Home Assistant / Agent 控制（TCP，完全可靠）；HomeKit 仅作备用 |
| AirPlay 发现延迟 5-15 秒 | 首次发现比同网段慢 | 启用 reflector-quick-join；可接受 |
| 主网络无法主动访问工作子网 | NAT 导致单向可访问 | 当前需求不需要反向访问 |
| HomeKit 首次配对需同网段 | 跨子网配对可能失败 | 所有设备在主网配对完成后再使用（当前已是如此） |

> **核心结论**：由于 Agent 系统和 Home Assistant 均基于 TCP 协议，跨子网控制智能家居完全可靠。HomeKit 的 mDNS 限制仅影响直接通过 Siri/家庭 App 控制的场景，不影响主要控制路径。

> 详细可行性分析见 [docs/dual-router-feasibility-analysis.md](docs/dual-router-feasibility-analysis.md)

## 设备清单与历史接入记录

> **⚠️ 历史规划 / 接入未核验 / 禁止按此采购**：本节的 Home Assistant/品牌接入措辞没有验收记录支持；已存在的硬件以当前状态表和台账为准。当前品牌方向以台账为准：Aqara/绿米为主；ORVIBO/欧瑞博仅评估具体空调型号，本文出现的 ORVIBO 面板/照明不得采购。

### 历史接入示例（HA 未核验）

#### 智能家居设备

**历史品牌规划（不代表当前决策）**
- **绿米 (Aqara)**：传感器、开关面板、窗帘电机等（兼容性须按具体型号验证）
- **欧瑞博 (ORVIBO)**：旧规划中的智能面板、照明（当前不作为采购项；只保留具体空调型号评估）

**控制体系（旧方案假设，未验收；优先级从高到低）**

| 控制方式 | 协议 | 跨子网可靠性 | 说明 |
|---------|------|-------------|------|
| Agent 系统 | HTTP/WebSocket (TCP) | ✅ 完全可靠 | 通过 Home Assistant API 控制，不依赖 mDNS |
| Home Assistant | HTTP/WebSocket (TCP) | ✅ 完全可靠 | Web UI / App 远程控制，基于 TCP 单播 |
| HomeKit | mDNS + Bonjour | ⚠️ 依赖 mDNS 中继 | 跨子网偶发"无响应"，主网内完全正常 |

> 以上是旧双路由方案的设计假设，不是当前部署事实；设备配网、跨 VLAN/mDNS 和 Home Assistant 控制必须以台账中的 PoC/验收记录为准。

**历史接入示例（HA 状态未核验；不作为采购清单）**
- 绿米 (Aqara) 传感器 / 开关 / 窗帘电机
- 欧瑞博 (ORVIBO) 智能面板 / 照明（当前不采购）
- 米家激光投影仪（历史示例，当前品牌范围排除；不代表已有）
- Apple TV 4K
- 小米踢脚线暖风机（历史示例，当前品牌范围排除；不代表已有）
- 小米空气净化器（历史示例，当前品牌范围排除；不代表已有）
- iPhone (苹果手机)

#### 计算基础设施（历史规划，未核验）

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

> 本文出现的 `xiaomi_*` 实体 ID 属于仓库旧示例/Mock 数据，保留用于解释现有代码；不是当前设备登记或部署配置，接入实物时必须按实际 Aqara 等获选设备替换并验收。

| 自然语言 | Home Assistant Entity ID |
|----------|---------------------------|
| 灯光 / 客厅灯 | `light.living_room` |
| 窗帘 / 客厅窗帘 | `cover.living_room_curtain` |
| 投影仪 / 投影 | `media_player.xiaomi_projector` |
| 暖风机 | `climate.xiaomi_heater` |
| 净化器 / 空气净化器 | `air_quality.xiaomi_air_purifier` |

## 系统架构

> 下图为旧架构示例，“米家设备”已被当前品牌范围排除，不是采购或接入目标。

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

## 下一步计划（历史路线，不是当前执行清单）

> **⚠️ 请勿按本节直接采购或施工**：本节保留早期软件/副路由路线；当前网络、设备、房间点位、Apple HomeView和模型部署以[家庭基础设施登记与实施台账](docs/home-infrastructure-register.md)为准。

- 历史副路由器采购项已取消：小米 AX3000T RD03 不在当前品牌范围；不得按本条采购或部署。
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

# 全屋智能家居接入拓扑 v1.2

> **更新日期**：2026-10-15
>
> **状态**：设计规划，不代表已采购、已安装或已验收。图中的设备类别、数量、协议和位置均须按最终型号及现场点位复核。
>
> **采购与介质（2026-10-15）**：[集中采购BOM](purchase-bom.md)。NAS确定靠近工作室交换机，采用兼容10G SFP+ DAC短线，整机/网卡/长度待选；四主干仍为Cat6A，不每房另埋光纤，保留可抽换管路。
>
> **关联文档**：[家庭基础设施登记与实施台账](home-infrastructure-register.md)、[家庭网络拓扑](network-topology.md)、[设备选型清单](device-selection-list.md)

## 1. 接入原则

- 全屋以 Aqara/绿米为主要选型方向，目标接入 Apple Home 和 Home Assistant（HA），**不考虑任何小米、华为设备**；不是所有 Aqara 产品都使用同一种协议，也不是所有型号都能完整接入两个平台。
- 住宅约 **100㎡**、一层矩形，目前无正式设计图，房间关系已知但覆盖、点位及数量须复尺。宽带计划 **1000Mbps 下载 / 30Mbps 上传**，局域网/本地自动化能力不由 WAN 标称速度保证。
- 网络拓扑 **v1.2** 的基线已确定：四区域各一条Cat6A星型回中央；主卧/次卧仅Wall AP，电竞房/大厅各一台交换机。电竞房单台 **ES210XPP-M2**，不增加交换机；10G RJ45给Mac、10G SFP+给NAS。三台EAP775-Wall均有1×2.5G+3×1G数据下联，工作室Apple TV/投影可改接其中两个1G口；J3455、Mac、NAS和PC保持ES210直连。不使用AP PoE Out。
- AP 形态已确认：主卧、次卧、工作室各暂定一台 **EAP775-Wall 三频 Wi-Fi 7 面板 AP**，大厅候选一台 **EAP772 Wi-Fi 7 吊顶（吸顶）AP**，共 3+1 台、2.5G 上联。面板装箱外墙面，大厅 AP 装顶面可见位置，不藏吊顶内部；地区频段/发货版本/供电验收见 [BOM](device-selection-list.md#64-按最新拓扑更新的候选购买清单)。三房mini优先推荐mini 2，代际待确认；大厅Apple HomeView已发布，Wi-Fi接法不变。两款官方列Wi-Fi 6E，但大陆6GHz不计保证；Thread仍独立于Wi-Fi，不能把美版频段规格当本户可用性。
- Wi-Fi 终端接 AP；Zigbee 设备接 Zigbee 网关/协调器；Matter over Thread 设备通过 Thread 网络和边界路由器进入家庭 LAN。**Matter 是应用层互通标准，Thread 与 Wi-Fi 才是这里的网络接入方式。**
- Apple Home与HA属于控制层，不是串在交换机、AP与终端之间的网络转发设备。**HomeView非壁挂／桌面版×1已确认**，支持Wi-Fi/Thread及HomeKit/Matter，经大厅AP Wi-Fi接入，使用随箱电源；大陆服务/账户/配套设备和配网待验。壁挂另用平板电脑或iPad，具体型号/数量/点位/供电与网络方式待选，作为交互终端记录，不替代HA主机、家庭中枢或Thread边界路由器；不先增加网口/PoE或物理图节点。详见[Apple官方核验](apple-home-devices-2026.md)。
- 用户同时需要 **HomePod/Siri 家居控制**与**各房间同 Mac 本地模型对话**，两类需求都保留，具体语音终端/接入方案未定。不能默认 HomePod 的麦克风能作为任意本地模型前端，HomeView/Siri AI也不等于Mac本地模型，官网未承诺开放原始麦克风流。
- 已确认 **Mac 留工作室；未来高速 NAS 与现有 J3455 规划在工作室箱外通风存储位，核心网络设备仍放弱电箱附近机柜**，不把服务器塞入密闭网络小箱。J3455 为现有 16GB / 10TB / 1GbE / Proxmox 主机，已运行独立黑群晖 VM 和代理/转发容器，拟迁入工作室而非已搬迁；2026-10-15继续计划新增独立 HAOS VM，尚未部署；主路由暂定Fusion 2.5G普通版，Omada由其内置控制器承载。未来高速 NAS 接电竞房交换机的 10G SFP+，需兼容SFP+接口/网卡与近距离DAC短线；已确定靠近交换机摆放，整机/长度待选，未采购。

## 2. Wi-Fi、Zigbee、有线设备与控制层

本图表示逻辑接入关系；两卧室AP由中央交换机有线PoE直连，电竞房/大厅AP经各自房间交换机接入LAN。虚线表示无线连接、规划候选或控制/集成关系，边上文字区分。三房各预留一台HomePod mini（优先推荐mini 2，代际待确认），大厅已确认一台Apple HomeView桌面版（非壁挂，未购/未部署）。壁挂平板/iPad待选，尚未确定点位及网络方式，不按占位节点施工。三处交换机的 PoE 数量与瓦数核算见[网络拓扑第 2.2 节](network-topology.md#22-交换机-poe-与端口复核2026-10-15)。

```mermaid
flowchart TB
    LAN["家庭 LAN<br/>中央PoE推荐ES210XPP-M2（待确认）<br/>+ 电竞房/大厅交换机<br/>两卧室仅 Wall AP"]

    subgraph MASTER["主卧 · 规划"]
        AP1["AP-MASTER · EAP775-Wall 暂定<br/>Wi-Fi 7 面板 AP · 主卧墙面<br/>无房间箱/独立交换机"]
        PC1["主卧电脑 / 有线设备"]
        HP1["HomePod mini<br/>优先推荐mini 2 · 待确认"]
        W1["主卧 Wi-Fi 设备<br/>具体灯具、传感器等逐型号确认"]
        AP1 -. "Wi-Fi" .-> HP1
        AP1 -. "Wi-Fi" .-> W1
        AP1 -->|"下联 1×2.5G + 3×1G<br/>不使用 PoE Out"| PC1
    end

    subgraph SECOND["次卧 · 规划"]
        AP2["AP-SECOND · EAP775-Wall 暂定<br/>Wi-Fi 7 面板 AP · 次卧墙面<br/>无房间箱/独立交换机"]
        PC2["次卧电脑 / 有线设备"]
        HP2["HomePod mini<br/>优先推荐mini 2 · 待确认"]
        W2["次卧 Wi-Fi 设备<br/>具体灯具、传感器等逐型号确认"]
        AP2 -. "Wi-Fi" .-> HP2
        AP2 -. "Wi-Fi" .-> W2
        AP2 -->|"下联 1×2.5G + 3×1G<br/>不使用 PoE Out"| PC2
    end

    subgraph STUDIO["工作室 / 电竞房 · 规划"]
        SW3["ES210XPP-M2 ×1<br/>8×2.5G PoE++ / 200W<br/>中央上联 2.5G · 不增加交换机"]
        AP3["AP-STUDIO · EAP775-Wall 暂定<br/>Wi-Fi 7 面板 AP · 箱外墙面"]
        HP3["HomePod mini<br/>优先推荐mini 2 · 待确认"]
        W3["工作室 Wi-Fi 设备<br/>具体灯具、传感器等逐型号确认"]
        MAC["计划 Mac Studio，留工作室箱外<br/>512GB 统一内存 / 4TB SSD<br/>本地模型，10G RJ45 接房间交换机"]
        NAS["未来高速 NAS · 未采购<br/>工作室箱外、靠近交换机<br/>兼容10G SFP+接口/网卡 + DAC短线"]
        J["现有 J3455 · 拟迁入，未搬迁<br/>箱外通风存储位 · 16GB / 10TB<br/>现1GbE，计划2.5GbE / Proxmox<br/>黑群晖VM + 代理/转发"]
        WIRED["PC ×2：现 1G / 未来 2.5G<br/>Mac Mini：1G"]
        MEDIA["Apple TV / 投影仪<br/>有线，速率按实物"]
        SW3 -->|"2.5G + PoE++"| AP3
        SW3 -->|"10G RJ45 / Cat6A"| MAC
        SW3 -->|"10G SFP+ / 兼容DAC短线"| NAS
        SW3 -->|"现1G → 升级后2.5G；同一端口"| J
        SW3 -->|"各占独立铜口<br/>按实际接口降速"| WIRED
        SW3 -->|"当前可直连"| MEDIA
        AP3 -. "可选：1G数据下联<br/>不使用PoE Out" .-> MEDIA
        AP3 -. "Wi-Fi" .-> HP3
        AP3 -. "Wi-Fi" .-> W3
    end

    subgraph HALL["大厅 · 规划"]
        SW4["ES206XPP-M2 ×1<br/>5×2.5G，其中4×PoE++ / 120W<br/>中央上联 2.5G"]
        AP4["AP-HALL · EAP772 候选<br/>Wi-Fi 7 吊顶 AP · 顶面可见"]
        FUTURE["Apple HomeView 桌面版 ×1<br/>型号已确认 · 未购 · Wi-Fi / Thread<br/>大陆服务 / 账户待验"]
        W4["大厅 Wi-Fi 设备<br/>具体灯具、传感器等逐型号确认"]
        HALLGW["HALL-IOT-GW · 大厅墙面信息口<br/>网关 / 协调器接入位<br/>PoE按最终型号；旁置普通插座"]
        TV4["大厅电视 · 有线"]
        SW4 -->|"2.5G + 802.3at PoE+；最大25.4W"| AP4
        SW4 -->|"HALL-IOT-GW · 有线数据"| HALLGW
        SW4 -->|"有线"| TV4
        AP4 -. "Wi-Fi · 用户意向" .-> FUTURE
        AP4 -. "Wi-Fi" .-> W4
    end

    LAN -->|"中央直达：一条 Cat6A / 2.5G + 匹配 PoE"| AP1
    LAN -->|"中央直达：一条 Cat6A / 2.5G + 匹配 PoE"| AP2
    LAN -->|"单条 Cat6A / 2.5G 主干"| SW3
    LAN -->|"单条 Cat6A / 2.5G 主干"| SW4

    subgraph CENTRAL["弱电箱附近核心网络机柜 · 规划"]
        FUSION["AC：Fusion 2.5G 普通版 · 暂定<br/>主路由 / 5×2.5G / 无PoE<br/>未购 / 未部署"]
        OMC["Fusion 内置 Omada 控制器<br/>同一物理设备，无独立VM/网口"]
        FUSION -. "内置管理应用" .-> OMC
    end
    FUSION -->|"2.5G LAN；经中央PoE交换机"| LAN

    Z["全屋 Zigbee 设备规划<br/>主卧、次卧、工作室、大厅、两卫生间<br/>灯 / 开关 / 传感器 / 窗帘等"]
    Z -. "方案 A：配对 Aqara 网关" .-> G["Aqara 有线 Zigbee 网关<br/>箱外，型号与位置依覆盖确定"]
    G -. "方案A；以太网" .-> HALLGW
    Z -. "方案 B：改为配对 HA 协调器" .-> C["HA Zigbee 以太网协调器<br/>型号待选；与方案 A 对同一设备二选一"]
    C -. "方案B；以太网" .-> HALLGW

    SW4 -. "大厅剩余一口候选；功耗待核" .-> CAM["PoE 摄像头候选<br/>点位待确认，不默认部署在卧室"]

    subgraph CONTROL["控制层 · 非转发串联"]
        HA["Home Assistant<br/>J3455上的独立HAOS VM<br/>位置已定，尚未部署"]
        APPLE["Apple Home<br/>家庭控制与成员权限"]
        HA -. "可选 HomeKit Bridge：选定实体" .-> APPLE
    end
    J -. "Proxmox 虚拟实例" .-> HA
    HA -. "方案B：经LAN使用ZHA或Zigbee2MQTT<br/>核芯片、固件与网络接口兼容" .-> C
    HA -. "经 LAN 控制已集成设备" .-> LAN
    OMC -. "经 LAN 管理 Omada 设备；不转发业务流量" .-> LAN
    APPLE -. "经 LAN 控制兼容设备" .-> LAN
    FUTURE -. "Apple Home家庭中枢 / 交互" .-> APPLE
```

### 2.1 各协议的实际接法

| 设备类别 | 接入路径 | 必须核验的边界 |
|---|---|---|
| Aqara Zigbee 灯、开关、传感器、窗帘等 | Zigbee → Aqara 网关 → LAN；或改为 Zigbee → HA 协调器 → HA | **单台设备不能同时配对两个独立 Zigbee 网络**。选择网关路径时，核对 HomeKit/Matter 桥接及 HA 集成实际暴露的实体；选择 HA 路径时，核对具体设备支持与功能差异。 |
| Matter over Wi-Fi 设备 | 所在区域 AP → LAN → 支持的 Matter 控制器 | 按支持情况使用 Matter 多管理员接入 Apple Home 和 HA；共享控制不等于任何品牌私有功能都可用。 |
| 非 Matter 的 Wi-Fi 设备 | 所在区域 AP → LAN → 该型号支持的集成 | 核对 HomeKit/HA 支持、本地或云端依赖、离线行为；Wi-Fi 本身不是兼容性保证。 |
| 普通灯具 + 智能开关/继电器 | 市电 → 智能开关/继电器 → 普通灯；开关的智能控制走 Zigbee、Thread 或 Wi-Fi | 灯本身不接网线。零火线、负载、调光、盒深及防潮要求由电气设计确认，交合格电工施工。 |
| PoE摄像头 | 从有余量的中央/大厅PoE交换机拉独立支线 → 摄像头；录像经LAN到NVR/NAS/录像服务 | 两卧室不设独立交换机；电竞房完整直连时无备用，Apple TV/投影改接AP后最多释放两个交换机口，但尚未分配给摄像头。当前不使用Wall AP下游PoE；核逐口/总功率、布线、RTSP/ONVIF、本地录像与HA集成，不自动等于Apple Home/HKSV支持。 |

Zigbee 的覆盖目标是**全屋六个区域**，不是只覆盖大厅；网关与中继能力依实际设备确定，电池传感器通常不承担 Zigbee 路由扩展。两卫生间的 Wi-Fi 设备由覆盖实测合适的邻近 AP 服务，不预先锁定某一台 AP，也不默认增加卫生间 AP。

**协调器接入澄清（2026-10-15）**：本项目预留固定路径 `大厅箱外网关／协调器 → HALL-IOT-GW 墙面口 → 大厅 ES206XPP-M2 → TRUNK-HALL → LAN → 电竞房 J3455 上的 HA`，不默认让HA通过Proxmox USB直通，也不占电竞房已满的交换机口。若使用Aqara有线网关，接法为`Zigbee设备 → Aqara网关 → LAN → HA支持的集成`；不能把它当作任意ZHA/Zigbee2MQTT可直接控制的通用协调器。若选择HA直接管理Zigbee，则使用兼容的以太网协调器，经LAN由ZHA或Zigbee2MQTT其中一个管理同一协调器；两条路径对同一设备二选一，型号与软件路径尚未选定，不额外默认采购两台。网关放箱外、按射频覆盖定位，只有最终型号支持PoE才从大厅交换机供电，否则使用墙口旁的普通插座；其负载需在确定型号后加入大厅120W预算。使用DHCP保留地址、受控LAN访问，并将所选网关与沿途交换机纳入UPS与重连测试；百兆以太网通常足够Zigbee控制，不需要协调器本身2.5G。

Thread走受支持的HomePod mini等Thread边界路由器接入LAN，再由HA的Matter集成控制，按实际型号与配网测试确认；不是所有Thread设备都可用一个Zigbee协调器接入，也不默认需要另一只USB棒。

**J3455网卡计划**：当前为1G，计划升级2.5G，仍占电竞房同一端口；升级后HA/黑群晖/代理共享2.5G物理上联；Omada由Fusion承载，现有千兆瓶颈描述仅适用于升级前。网卡、Proxmox驱动和桥接迁移尚未实施，不能标为已测速或已部署。

J3455 的 10TB 尚未区分原始/可用容量，盘数、冗余、备份、硬盘健康和运行余量仍须核实；现有服务不因本图更新而被迁移或改装。HAOS VM继续规划在J3455上，尚未创建或验收；它与黑群晖共用宿主、供电和物理网口（现1G、计划2.5G），须验证资源、SSD、备份、UPS和宿主重启恢复。Omada改用暂定Fusion的内置控制器，取消J3455上的控制器VM与Java/MongoDB部署；Fusion整机重启会同时影响主路由和网络管理，配置备份与中央UPS须落实。Mac↔未来高速 NAS 在同交换机、同 VLAN 时为本地 10G，不经中央 2.5G 主干；有线 Apple TV↔J3455 同条件下也本地转发，但受自身网口/存储性能限制。其他房间访问工作室设备共享该房 2.5G 上联；跨 VLAN 若经网关需核实际三层路径，不能直接套用本地 10G。Apple TV 的以太网接法与是否具备 Thread 边界路由器能力是两个事项，后者按具体型号确认，本图不因有线连接新增 Thread 角色。

## 3. 全屋 Matter over Thread 规划

下图把四个主要区域和两个卫生间都纳入 Thread 类别规划。**这是可选协议与点位规划，不是六个区域已确定采购 Thread 设备**；尤其 Aqara 各型号可能使用 Zigbee、Wi-Fi 或 Thread，采购后必须按实际协议归类，不应把现有 Zigbee 候选直接标成 Thread。

```mermaid
flowchart TB
    TM["主卧 Thread 终端候选<br/>灯 / 开关 / 温湿度 / 门窗"]
    TS["次卧 Thread 终端候选<br/>灯 / 开关 / 温湿度 / 门窗"]
    TW["工作室 / 电竞房 Thread 终端候选<br/>灯 / 开关 / 插座 / 传感器"]
    TH["大厅 Thread 终端候选<br/>灯 / 开关 / 门窗 / 传感器"]
    TB1["卫生间 A Thread 终端候选<br/>水浸 / 温湿度 / 照明控制"]
    TB2["公共卫生间 Thread 终端候选<br/>水浸 / 温湿度 / 照明控制"]

    MESH["目标：全屋同一 Thread Mesh<br/>共享 Thread 网络凭据 + 覆盖连通<br/>电池终端通常不转发"]
    TM -. "Matter over Thread" .-> MESH
    TS -. "Matter over Thread" .-> MESH
    TW -. "Matter over Thread" .-> MESH
    TH -. "Matter over Thread" .-> MESH
    TB1 -. "Matter over Thread" .-> MESH
    TB2 -. "Matter over Thread" .-> MESH

    MESH -. "可用边界出口" .-> HP1["主卧 HomePod mini<br/>Thread 边界路由器"]
    MESH -. "可用边界出口" .-> HP2["次卧 HomePod mini<br/>Thread 边界路由器"]
    MESH -. "可用边界出口" .-> HP3["工作室 HomePod mini<br/>Thread 边界路由器"]

    HP1 -. "Wi-Fi" .-> AP1["AP-MASTER · EAP775-Wall 暂定<br/>Wi-Fi 7 面板 AP"]
    HP2 -. "Wi-Fi" .-> AP2["AP-SECOND · EAP775-Wall 暂定<br/>Wi-Fi 7 面板 AP"]
    HP3 -. "Wi-Fi" .-> AP3["AP-STUDIO · EAP775-Wall 暂定<br/>Wi-Fi 7 面板 AP"]
    AP1 -->|"一条 Cat6A / 2.5G，中央 PoE 直供"| LAN["家庭 LAN"]
    AP2 -->|"一条 Cat6A / 2.5G，中央 PoE 直供"| LAN
    AP3 -->|"有线，经工作室交换机"| LAN

    HUB["Apple HomeView 桌面版 ×1 · 未购<br/>Thread已核，配网 / 大陆服务待验"] -. "Wi-Fi · 原计划不变" .-> AP4["AP-HALL · EAP772 候选<br/>Wi-Fi 7 吊顶 AP"]
    MESH -. "额外边界出口候选；非串联" .-> HUB
    AP4 -->|"有线，经大厅交换机"| LAN
```

- 三房HomePod mini与大厅HomeView均可规划Thread边界出口，不是四台串联或每房必经本房mini；同一网络凭据、多边界路由器和恢复须配网实测。HomeView已确认桌面版×1；三房mini仍暂各1台，mini 2代际/数量/地区未获最终确认。壁挂平板不按Thread边界路由器计数。
- 同一 Thread 网络需要共享网络凭据并保持覆盖连通；**不要假定所有品牌的边界路由器会自动并为一个 Mesh**。Matter 多管理员共享控制与 Thread 网络凭据共享是不同事项。
- 只有具备 Thread 路由能力的常电设备才可扩展 Mesh；不能把所有常电设备或电池传感器都当作中继。两卫生间需结合墙体、防潮和现场信号实测选点。
- Thread 边界路由器承担 IP 网络连通，Matter 控制器承担设备管理；两种角色可能由同一产品承载，但概念与验收项不同。Thread 支持也不自动等于 Matter/Apple Home/HA 兼容。

## 4. 设备箱、供电与验收边界

1. 保持四条中央 **2.5G** 主干；仅电竞房/大厅各一房间箱/交换机。电竞房单台ES210XPP-M2、不增加第二台，10G RJ45给Mac、10G SFP+给NAS。完整直连表可占满8个2.5G口；Apple TV/投影可改接工作室EAP775-Wall的1G数据下联，释放两个ES210端口。J3455/HA、Mac、NAS和PC保持交换机直连。
2. 主卧/次卧Wall AP经中央PoE直供；工作室EAP775-Wall由ES210XPP-M2供电。三台面板AP的下联均可传数据，但不使用PoE Out。摄像头只接有余量且供电匹配的中央/大厅交换机。任何接在AP下联的设备都会随AP重启、故障或断电而离线，因此关键服务保持交换机直连。
3. 用户要求停电后 **NAS、Mac 与全屋网络继续运行，UPS目标至少1小时**。覆盖光猫/网关/中央交换机、电竞房/大厅交换机及四AP、NAS/J3455和Mac完整供电路径；中央UPS须计两卧室AP PoE负载，**取消两卧室独立网络UPS点**。但本地市电大厅/电竞房交换机、卧室电脑/HomePod不因中央UPS自动保活。按中央、电竞房、大厅三处实测功耗/峰值/策略/电池曲线核算UPS或合规后备回路，不能宣称已达成。HomePod、Aqara网关、HA等控制节点按停电时所需功能另核，AP有电不代表控制层可用。
4. 首期优先验证同一可信网络中的发现、配网、控制和离线自动化；之后再隔离访客、摄像头或 IoT。跨 VLAN 要另验收 IPv6、mDNS/Bonjour、组播和访问规则，不能以“能上网”代替智能家居联通验收。
5. 最终逐设备登记型号、区域版本、协议、供电、所在区域、所属网关/Thread 网络、Apple Home/HA 集成方式及离线测试结果。摄像头点位和隐私边界单独确认，不默认在卧室或卫生间部署。
6. 中央核心机柜仍放弱电箱附近；NAS/J3455规划工作室箱外通风存储位，未迁移/采购。工作室后备供电覆盖ES210XPP-M2、其AP、Mac、NAS/J3455及必要排风；中央UPS按中央核心设备和两卧室AP PoE负载计算，不把工作室存储误计中央；大厅本地交换机/AP另核后备供电。三处都不是已完成安装/隔声工程；静音/隔声由用户另行考虑，通风柜不等于隔音柜。承重/散热/维护空间仍核；约定实际负载下验收至少1小时续航、安全关机与来电恢复，无正式设计图/负载数据时不锁尺寸或UPS型号。

## 5. 变更记录

- **2026-10-15（HomeView安装决定）**：用户确认大厅HomeView非壁挂／桌面版×1，英语Siri AI可接受，Wi-Fi/原装电源不变；壁挂另用平板或iPad，型号/数量/点位/供电待选，不买HomeView壁挂版/底座，不新增主干、端口或PoE负载。mini代际/数量/地区继续待选，产品地区服务仍须验收。

- **2026-10-15（Apple产品更正）**：大厅目标为Apple HomeView，美国已发布/开放预购，官方Wi-Fi/Thread已核；现行图更名并补Thread边界出口候选。三房新购优先推荐mini 2，代际/数量及HomeView桌面/壁挂/大陆体验待用户确认；四主干/AP PoE与HA在J3455不变，不视为Mac模型开放麦克风。

- **2026-10-15（电竞房端口）**：用户确认不增加电竞房交换机。EAP775-Wall下联为1×2.5G+3×1G，并非只有两个；Apple TV/投影可改接两个1G数据口，J3455/HA、Mac、NAS和PC保持ES210直连，不使用AP PoE Out。
- **2026-10-15（较早方案，已被下条取代）**：Home Assistant与Omada部署位置确定为现有J3455/Proxmox上的两个独立VM：HAOS VM和Linux软件控制器VM；黑群晖VM及代理服务保留，两个新VM尚未部署。OC200退出当前BOM，中央物理连接从6减为5。Omada采用Java 17 + MongoDB 4.4兼容路径，记录无AVX、数据库EOL、管理面隔离与迁移风险。
- **2026-10-15（采购一致性）**：NAS已确定放工作室交换机附近，两张现行拓扑统一为10G SFP+ DAC；四条Cat6A、两处房间箱、中央五连接与AP 3+1不变。新增集中采购BOM，已确认/暂选/未决分表，不自动追加中央交换机或改变HomePod代际。
- **2026-10-15（Fusion暂定）**：用户暂定Fusion 2.5G普通版作为主路由并使用内置Omada控制器；ER707-M2/J3455 Omada VM退出当前计划。HA仍在J3455独立HAOS VM，未部署；四条2.5G主干、中央PoE供电、电竞房Mac/NAS本地10G与端口数量沿用。
- **2026-10-14 / v1.2**：两卧室取消设备箱/独立交换机/网络UPS点；各自一条Cat6A/2.5G由中央PoE直达EAP775-Wall，电脑/有线设备用1×2.5G+3×1G下联。大厅汇聚提议未采纳。电竞房/大厅保留箱与交换机，电竞房十口与Mac/NAS本地10G不变；中央仍六连接但新增两路PoE及两台保守117W预算，中央UPS重算。同步Wi-Fi/Thread图和AP故障边界，全屋智能设备类别/协议规划不变，未采购/施工。
- **2026-10-14 / v1.1（历史，卧室箱/交换机已被v1.2替代）**：确认全屋2.5G主干，工作室单台ES210XPP-M2，本地Mac/NAS两个10G口；八个2.5G口全占。J3455/未来高速NAS改为工作室箱外通风存储位，未迁移/未采购。同步逻辑图、端口、PoE及UPS边界，Thread规划不变，Apple TV仅新增有线接入事实，不预设其Thread能力。
- **2026-10-13 / v1.0（历史，已替代）**：工作室主干10G、NAS/J3455中央机柜布局及工作室至少第三个10G备用口要求不再适用当前设计；AP形态、三台HomePod mini及Thread逻辑保留。

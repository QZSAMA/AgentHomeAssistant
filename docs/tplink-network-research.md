# TP-Link 全屋多千兆网络：产品调研与候选采购清单

> **2026-10-20 当前网络方案：3A三频，暂定定稿。** 普通Fusion ×1、中央及大厅ES206XPP-M2各1、电竞房ES210XPP-M2 ×1、主卧/电竞房EAP775-Wall ×2、大厅吊顶EAP772 ×1。双频725×2+723×1保留预算备选。次卧只施工Cat6A/RJ45，已有TL-7DR3630可选有线复用。四条2.5G主干、两房间设备箱、Mac/NAS本地双10G与交换机PoE直供保持。设备未购/未部署。
>
> 当前型号/数量/链接/预算见[采购BOM](purchase-bom.md)与[方案比较](network-cost-optimization.md)，商品链接已于2026-10-20逐项核对；[核对记录](network-link-audit.md)。下方带旧日期的三面板一吊顶、次卧AP或中央ES210建议仅用于追溯。

<details>
<summary>较早版本说明与核验日期</summary>

> **2026-10-19 最新结论**：[第三版成本优化](network-cost-optimization.md)确认四台AP由Omada交换机/PoE网关直接供电，不采用独立供电器。3A以中央ES206XPP-M2替代较大的中央ES210XPP，工作室ES210XPP与大厅ES206XPP保留；3B为Fusion 2.5G PoE替代普通Fusion和中央交换机。当前Amazon条件预算3A更低。725-Wall仍须US V2四下联口书面确认，PoE实际协商和满载必须验收。本条覆盖下方较早的“中央ES210推荐”和注入器回退讨论。

> **2026-10-16 当前采购/装修范围**：[基础网络采购与装修交底 Excel](../outputs/network-renovation-20261016/基础网络采购与装修交底.xlsx)覆盖网络硬件、材料、逐条布线、端口/PoE、配置和分阶段验收。高速NAS、UPS搬入后再考虑，不作为入住前必购；NAS要求自带10G SFP+，不买网卡，介质待实物确认。Mac走原生10G RJ45；Apple TV 4K旧款、米家激光投影仪、树莓派均已有，不重复购买。壁挂屏先试已有杂牌安卓，不合适再选二手iPad mini/便宜iPad，暂未定。J3455已确认PCIe 2.0 x1，TX201为兼容性待验的首选候选。下方较早的固定DAC与UPS入住前要求由本条更新；不改四主干/两房间箱/三面板一吊顶。

> 调研更新日期：2026-10-15（保留较早条目的原始核验日期）。住宅位于中国大陆；用户偏好美国版设备，购买入口优先美国 Amazon，补充已核验的美国官方商城。
> 本文是研究与建议，不代表已购买、已部署或最终施工批准。**2026-10-15已核Fusion、ES210、ES206、EAP775-Wall、EAP772的精确Amazon商品与新机购买栏**，报价/卖家统一见[集中采购BOM](purchase-bom.md)；2026-10-14四款AP历史价格见[对比报告](ap-6ghz-selection-price-comparison.md)。跨境配送、当地认证、保修及最终发货硬件版仍待核。
> 当前需求事实见 [家庭基础设施台账](home-infrastructure-register.md)，布线交底见 [施工需求](renovation-wiring-requirements.md)，图示见 [网络拓扑](network-topology.md) 与 [全屋智能家居拓扑](smart-home-topology.md)。
> **AP 优先级确认（2026-10-14）**：支持6GHz的三频设备保持第一优先，主卧/次卧/工作室各1台 **EAP775-Wall（第一优先暂选）**，大厅1台 **EAP772（第一优先候选）**，合计 **3+1**。[对比报告](ap-6ghz-selection-price-comparison.md)保留双频EAP725-Wall/EAP723为非默认备选，附报价日期、版本区别及未来更新流程；不替换当前BOM。地区合规、6GHz实际可用性、下单时库存、跨境发货及保修仍待核，本方案不使用AP PoE Out。
> **核心设备更新（2026-10-15）**：用户暂定 **Fusion 2.5G 普通版 ×1（非PoE版）**作为主路由并使用内置Omada控制器；ER707-M2/J3455 Omada Linux VM撤出当前计划，OC200不采购。大厅ES206XPP-M2保留，中央推荐ES210XPP-M2待确认；Home Assistant继续计划J3455独立HAOS VM。Fusion未购/未部署，HA VM未创建/验收；控制器随Fusion纳入中央UPS，不另占端口，功能/价格/电源证据见第2.5节。
> **v1.2用户已确认：四条主干2.5G，两卧室仅Wall AP，电竞房/大厅各一箱一交换机。** 电竞房继续单台ES210XPP-M2，不增加交换机；Mac原生RJ45/NAS SFP+本地10G。EAP775-Wall另有1×2.5G+3×1G下联，Apple TV/投影可改接两个1G口；J3455/HA、Mac、NAS和PC保持ES210直连，不使用AP PoE Out。

</details>

## 1. 结论与稳定性边界

> 下文是2026-10-15及以前的研究快照，包含已撤销的四AP数量和中央ES210建议，供追溯规格与依据；不得据其“当前/推荐”措辞下单。现行采购仅以文首所链2026-10-20的BOM、拓扑和采购数据为准。

**6GHz专项研究已完成（文献层面）**：见[中国大陆Wi-Fi 7/6GHz报告](wifi7-6ghz-mainland-china-research.md)。存在特定设备/驱动的成功自述与实际频段截图，但没有本项目EAP775-Wall的完整大陆复现证据，也未发现普通住宅WLAN开放依据；Apple明确在大陆不能使用6GHz。保留3+1暂选BOM，6GHz不计入部署保证；具体认证/硬件版/固件/保修与实机仍待核。Omada AFC指南还区分EAP772硬件版本，不可只凭型号名套用能力。

TP-Link Omada方向适合本项目约100㎡一层住宅、四个AP预留点及Apple Home/HA场景；品牌统一不等于所有型号都支持Omada。网络保持TP-Link，Apple/Aqara方向不变，运营商光猫、UPS、线缆和箱体不强求同品牌，但同样排除小米/米家、华为。工作室已选 ES210XPP-M2 ×1，不恢复 TL-SX1008/SX3206HPP 或两台组合；中央及其他房间型号继续核验供货、版本和管理能力。

这一判断依据是端口、PoE、统一管理和拓扑能力，不是故障率统计或本户实测。不能凭品牌承诺不掉线、无延迟或所有功能开启后满速。长期质量仍取决于固件、线材、散热、供电、无线干扰、终端兼容性和运营商质量。

用户所说的小弱电箱是**可开门维护、有供电/通风的设备位置**，不是封墙。v1.2仅电竞房/大厅各一箱一交换机，共2个房间箱；主卧/次卧取消箱/交换机，仅保留面板AP安装位。AP/无线网关在箱外，不能用金属箱包住AP。

主卧/次卧电脑与有线设备改为接Wall AP下联口；墙口若采用，回接AP下联而非新增中央回线。**主卧/次卧/工作室必须面板AP，大厅吊顶AP，均Wi-Fi 7/上联2.5G**。EAP775-Wall有1×2.5G+3×1G下联，不是4个2.5G；单口EAP772/EAP773仅适合大厅候选，不能替代两卧室的扩口功能。面板墙面安装、大厅顶面安装，不藏箱/吊顶腔内。

## 2. 当前确定的布线基线与历史方案

| 状态 | 连接方式 | 优点 | 代价/适用条件 |
|---|---|---|---|
| **v1.2：两卧室Wall AP + 两区域交换机** | 中央→两卧室各1条Cat6A/2.5G+匹配PoE→Wall AP→下联终端；另两主干→电竞房/大厅交换机→AP/终端 | 主干仍4条、房间箱/交换机减至2；电竞房Mac/NAS本地10G不变 | 卧室AP下联1×2.5G+3×1G，共享2.5G回程；AP故障影响该卧室有线/无线；中央需两路匹配PoE |
| 历史v1.1，不再按其卧室数量采购 | 四区域各1条Cat6A/2.5G→本地交换机→AP/终端，共4箱/4交换机 | 电竞房Mac/NAS本地10G已定 | 主卧/次卧交换机、设备箱与网络箱UPS已被v1.2取消 |
| 历史 v1.0，不再采用 | 工作室上联10G，NAS/J3455接中央柜 | 当时集中存储设备 | 被本次电竞房本地10G方案取代，不沿用中央八连接或主干铜模块预算 |
| 历史候选，当前不采用：集中供电/双回线 | 中央 PoE → AP；另一路中央 → 墙口/房间交换机 → 电脑 | AP 可统一由中央 UPS 保活；AP 与电脑不抢同一房间上联 | 每房间至少两条独立回线，不符合用户最新单主干要求 |

当前共**4条中央Cat6A主干、2台房间交换机/2个设备箱**，不增第二回线、Mac独立回线或大厅AP中央线；当前不每房额外预埋光纤，保留可抽换空管/牵引线，不影响运营商入户光纤。NAS已确定靠近工作室交换机，使用兼容10G SFP+ DAC短线。两卧室AP下联与两区域交换机到墙口/终端均另需本地支线，电竞房/大厅到各自AP也各1条支线；1条主干只限制中央线路。

Mac Studio 的10GbE接 ES210XPP-M2 原生10G RJ45，高速NAS接10G SFP+；中央上联占一个2.5G RJ45，不占这两个10G口。完整直连时，其余七个2.5G口给 PC×2、Mac Mini、J3455、有线Apple TV、投影和EAP775-Wall，十口正好全占；Apple TV/投影改接EAP775-Wall的两个1G下联后，交换机可释放两个2.5G口。ES206XPP-M2仅一个10G SFP+且总口数不足，不能替代本方案。柜体需按电源、网线弯曲和维护空间复尺；普通通风不等于隔音。

此前大厅交换机汇聚两卧室AP不作为当前布局；v1.2由中央各一条主干直接到两卧室AP，保留四条星型主干，仅取消两卧室设备箱/交换机。

### 2.1 当前布局与候选状态

```text
入户光纤 → 运营商光猫（桥接待确认）→ Fusion 2.5G 普通版（用户暂定；主路由 + 内置Omada控制器）
                                      │
                    中央 Omada 2.5G PoE交换机（建议≥8铜口；至少2口匹配卧室AP供电，SKU待核）
                      ├─ 1条Cat6A / 2.5G + PoE → 主卧EAP775-Wall → 1×2.5G+3×1G下联 → 电脑/墙口
                      ├─ 1条Cat6A / 2.5G + PoE → 次卧EAP775-Wall → 1×2.5G+3×1G下联 → 电脑/墙口
                      ├─ 1 条 Cat6A / 2.5G → 大厅 ES206XPP-M2（选型已确认）→ EAP772吊顶AP / 电视 / HALL-IOT-GW墙面口
                      ├─ 1 条 Cat6A / 2.5G → 工作室 ES210XPP-M2 ×1（完整直连可占满；AP改接可释放两口）
                      │                        ├─ 原生10G RJ45 → Mac Studio
                      │                        ├─ 10G SFP+ / 兼容DAC短线 → 附近高速NAS（未购，接口/网卡待选）
                      │                        ├─ 2.5G + 匹配bt PoE → EAP775-Wall 面板 AP
                      │                        ├─ 两个2.5G口 → PC×2（现1G，计划2.5G）
                      │                        ├─ 1G → Mac Mini
                      │                        ├─ 现1G → 计划2.5G → J3455 / Proxmox / 黑群晖VM / HAOS VM / 代理转发
                      │                        ├─ 有线，速率按型号 → Apple TV
                      │                        └─ 有线，接口待核 → 投影仪
```

这里 AC 指主路由，不是 Omada 控制器。主路由LAN到中央目标2.5G；当前暂定Fusion把主路由与Omada控制器集成在同一物理设备；主路由串接光猫与交换机，内置控制器应用经LAN管理设备，不另占端口。NAS/J3455改为电竞房接入是用户设计决定，尚未执行迁移；核心机柜位置继续沿用。

AP仍**EAP775-Wall ×3 + EAP772 ×1**，四条主干不变；两卧室主干直接接Wall AP，电竞房/大厅各1条本地AP支线。卧室电脑接AP下联，电竞房终端接本房交换机。摄像头后续按点位/空余PoE口另审，不默认用卧室AP PoE Out或电竞房已有端口，当前不使用AP转供。

中央现为5连接：网关、两卧室AP、电竞房/大厅交换机，建议≥8×2.5G；**至少2口匹配卧室AP PoE输入/单口功率**，10G非必需。无转供功耗未核清前按45W/台和bt口保守预留，总预算至少 `2×45×1.3=117W` 加其他实际PoE负载。非PoE ES210X-M2不再满足直接供电；SG2210XMP-M2为30W/口at，仅在具体无转供模式/功耗证明后条件候选。2026-10-14核验后推荐中央ES210XPP-M2×1，2.5G bt口/90W单口/200W总预算满足保守规划，详见第2.3.1节；仍待用户确认，不将已确认电竞房采购数量自动改为全屋2台。最终SKU/Fusion内置控制器兼容待核。中央当前不采购注入器。大厅现在规划上联、AP、电视、`HALL-IOT-GW`四个2.5G口，另留一口未来候选；网关/摄像头型号确定后重算PoE。电竞房完整直连时无备用；Apple TV/投影改接AP后，ES210可释放两个2.5G口。

用户已说明J3455为16GB内存、10TB存储、1GbE、Proxmox，已运行独立黑群晖VM及家庭代理/转发容器；现有服务保留。2026-10-15继续计划新增独立HAOS VM，尚未部署；Omada改用暂定Fusion内置控制器，取消J3455控制器VM，先核宿主CPU/RAM余量、SSD、磁盘健康、备份及UPS。10TB的盘数/容量口径/冗余/备份另核；新高速NAS仍非必购。Mac↔高速NAS和Apple TV↔J3455的同VLAN本地流量都留在电竞房交换机内；跨房访问共享2.5G，J3455仍受自身千兆口和存储限制。

### 2.2 为什么撤下原来的两套工作室方案

旧A用TL-SX1008单台八口满足NAS也在工作室时的六连接，但有调速风扇且不能被Omada管理；旧B用SX3206HPP+ES206X-M2管理扩口，需要两台且有风扇。当时用户不接受此工作室取舍，并确认NAS集中到机柜，因此**两套均退出当前采购**。2026-10-15曾因ES210完整直连会占满十口而研究“ES210XPP-M2 + 无风扇ES206X-M2”扩口；用户随后决定不扩交换机，改用EAP775-Wall下联承载Apple TV/投影，该候选也退出当前采购。第3.4节只保留旧方案历史核算。

v1.1确认的电竞房ES210XPP-M2单台与Mac/NAS两个10G口在v1.2保持。2026-10-14讨论过SX3206HPP + ES210XPP-M2双机与SX3832MPP大型单机，均未采用，不列当前采购；v1.2仅取消两卧室交换机/箱，不恢复旧电竞房组合。

### 2.3 ES210XPP-M2 最新选型与端口验证（2026-10-14）

[美国官方规格](https://www.omadanetworks.com/us/business-networking/omada-switch-agile/es210xpp-m2/)已核：8×2.5G RJ45（均802.3af/at/bt）、1×10G RJ45、1×10G SFP+；无风扇、226×131.2×35mm，外置适配器输入100–240VAC。单PoE口最高90W、全机200W；交换容量80Gbps、转发率59.52Mpps，端口全双工带宽合计为 `2×(8×2.5+10+10)=80Gbps`，不把它当单一2.5G共享总线，但并发实际性能仍要实测。

| 接口预算 | 去向 | 限制 |
|---|---|---|
| 10G RJ45 ×1 | Mac Studio | 原生铜口、Cat6A本地10G |
| 10G SFP+ ×1 | 高速 NAS | NAS靠近交换机，需兼容SFP+接口/网卡与DAC短线；不另配铜模块/光模块 |
| 2.5G RJ45 ×1 | 中央上联 | 所有跨房/对外流量共享2.5G |
| 2.5G RJ45 ×2 | PC 1/2 | 现1G、计划升级2.5G |
| 2.5G RJ45 ×1 | Mac Mini | 终端1G |
| 2.5G RJ45 ×1 | J3455 | 现1G，计划升级2.5G；复用本口，未实施 |
| 2.5G RJ45 ×1 | Apple TV，或改接AP 1G下联 | 保持有线；改接后本交换机口空闲，型号未核 |
| 2.5G RJ45 ×1 | 投影仪，或改接AP 1G下联 | 保持有线；改接后本交换机口空闲，接口与速率待实机核验 |
| 2.5G PoE++ RJ45 ×1 | EAP775-Wall | 2.5G、匹配bt供电，不使用AP转供 |

完整直连基线会占满十口，NAS未购也保留其SFP+口，不计为空闲余量。EAP775-Wall另有1×2.5G+3×1G下联；Apple TV与投影改接两个1G口后，ES210释放两个2.5G口，AP仍余1×2.5G+1×1G。Mac↔NAS与Apple TV↔J3455同VLAN本地流量不走中央上联；后者改接AP时会经过AP的2.5G上联，但仍不经过中央主干。多个客户端访问同一NAS仍共享NAS网口与磁盘性能。跨VLAN若由主路由转发，会经过2.5G上联及网关，不能据此保证10G剪辑；初期保持所需本地数据路径在同一可信LAN。

**历史兼容研究（已被Fusion内置控制器取代）**：本项目曾计划采用J3455上的官方Linux软件控制器，尚未部署即撤出计划。2026-10-15核对官方6.3.0.45 `.deb`：控制器包为`Architecture: all`，依赖Java 17及MongoDB `>=3.0,<8.1`；TP-Link官方指南说明v5.15.20+支持MongoDB 4.4～8，而MongoDB 5.0+在x86_64需要AVX。J3455没有AVX，因此当时的兼容组合为**Omada 6.3 + Java 17 + MongoDB 4.4**，不是MongoDB 8。MongoDB 4.4已于2024-02-29结束上游支持，故仅开放受控管理网络、固定数据库版本、定期导出控制器配置并保留迁移路径。页面脚注限定 port-based/802.1p/DSCP QoS 仅独立模式；PoE Auto Recovery仅独立模式，控制器模式为手动Recovery，不把简易管理型功能等同完整L2+能力。

2026-10-15 [美国官方商城](https://store.omadanetworks.com/products/omada-8-port-2-5g-2-port-10g-easy-managed-switch-with-8-port-poe-es210xpp-m2)与[Amazon精确商品B0HB17QTKX](https://www.amazon.com/dp/B0HB17QTKX)均核为$229.99；Amazon产品信息Mfr Part Number明确ES210XPP-M2，Blazing Network US销售、Amazon发货，显示有货。不同于非PoE的ES210X-M2；价格/卖家证据集中见[采购BOM](purchase-bom.md)，不保证下单时库存/跨境/当地保修。

### 2.3.1 中央 PoE 交换机推荐：ES210XPP-M2（2026-10-14，待用户确认）

用户暂定Fusion 2.5G普通版主路由及内置Omada控制器，大厅ES206XPP-M2保留；ER707-M2/J3455 Omada VM撤出计划，OC200不采购。**建议中央也采用 ES210XPP-M2 ×1**，与电竞房同款但位于不同位置，不改变电竞房只用一台的决定。此处是研究推荐，不是用户已确认新增采购；若后续采纳，全屋该型号才由电竞房已选 1 台变为中央 1 台 + 电竞房 1 台，共 2 台。

本轮重新读取了[美国官方规格](https://www.omadanetworks.com/us/business-networking/omada-switch-agile/es210xpp-m2/#specifications)及[美国官方商城](https://store.omadanetworks.com/products/omada-8-port-2-5g-2-port-10g-easy-managed-switch-with-8-port-poe-es210xpp-m2)：

| 核对项 | 官方规格 / 本项目核算 |
|---|---|
| 数据与供电口 | 8×2.5G RJ45，全部支持 IEEE 802.3af/at/bt PoE++；另有 1×10G RJ45、1×10G SFP+ |
| 单口 / 总预算 | 单个 PoE 口最高 90W，所有 PoE 口合计 200W；不是 8 口可同时各输出 90W |
| 两卧室 AP 预算 | 沿用已归档 EAP775-Wall 45W/台最高值（含 25W PoE Out）保守预留：`2×45W×1.3=117W`，低于交换机标称 200W；当前不使用 AP PoE Out，117W 不是两个裸 AP 的实测用电 |
| 其余供电 | 200−117=83W 仅为相对于上述规划预算的余量；其他新增受电设备须另计，核实实际 PoE 分级/分配、线损和温度，不把所有余量承诺为可用扩容 |
| 中央端口示例 | 2.5G 口 1/2 接两卧室 AP，3 接 Fusion LAN，4/5 接电竞房/大厅交换机；余 3 个 2.5G 口及 2 个 10G 接口。Omada内置于Fusion，不另占端口；大厅/电竞房交换机依旧本地市电，不靠中央 PoE 供电 |
| 尺寸 / 电源 | 无风扇；226×131.2×35mm；随箱 AC/DC 适配器输入 100–240V、输出 54V/4.16A，适配器及网线弯曲空间另算；无风扇仍需散热 |
| 控制器 | 暂定Fusion 2.5G普通版内置Omada控制器；不部署J3455 Linux VM，核全套设备adoption/固件兼容、配置导出与恢复 |
| 美国报价快照 | 2026-10-14 官方商城显示 $229.99/台、有 Add to cart 按钮；不含税运、进口成本，不保证跨境配送/保修及后续库存，不据此下单 |

**推荐依据**：端口数量满足中央五连接并保留余量，bt 单口与总预算能覆盖当前保守规划，无需依赖尚未澄清的 EAP775-Wall 仅 at 供电功耗模式。原 SG2210XMP-M2 的 160W 总预算不是主要疑点，单口 30W/at 与 AP 在相应模式的功耗/功能才需要另证；不能断言该型号一定无法带不转供的 AP，也不将其当作无需验证的等价替代。

ES210XPP-M2 属于 Easy Managed，而非完整 L2+/三层交换机。官网列有 802.1Q VLAN（最多 32 组）、IGMP Snooping 等；部分 QoS 仅独立模式可用，控制器模式 PoE Recovery 为手动。当前基础 VLAN/集中管理方向可评估采用，后续高级 ACL、组播/IPv6、跨 VLAN 发现须按实际功能验证。它的额外 10G 口只是余量，不把四条 2.5G 主干改为 10G。200W 是输出预算而非恒定耗电，UPS 应按交换机自身加实际受电负载测算，避免重复计算。

上述中央推荐沿用第2.4节已归档的45W/at/bt证据；2026-10-15的价格刷新不新增裸机功耗或供电实测结论。中央选择仍待用户确认、发货SKU与上电负载验收。

### 2.3.2 三处交换机 PoE 复核（2026-10-15）

按当前 AP 最大功耗乘 1.3 保守规划：中央推荐 ES210XPP-M2 的两台 EAP775-Wall 为 `2×45×1.3=117W / 200W`；电竞房同型一台为 `45×1.3=58.5W / 200W`，完整直连会占满交换机十口，Apple TV/投影改接AP后可释放两个2.5G口；大厅 ES206XPP-M2 的 EAP772 为 `25.4×1.3≈33W / 120W`。逐口输出上限均为90W，足以覆盖对应AP标称最大功耗；**90W/口不可相加成总预算**。EAP775-Wall 45W包含25W PoE Out，当前不转供且不是裸机实测；保守预算也不代表UPS实际输入功率。

[ES210XPP-M2 美国官方规格](https://www.omadanetworks.com/us/business-networking/omada-switch-agile/es210xpp-m2/)列8个2.5G af/at/bt PoE++口、200W总预算，另有两个不供PoE的10G口；[ES206XPP-M2 美国官方规格](https://www.omadanetworks.com/us/business-networking/omada-switch-agile/es206xpp-m2/)列5个2.5G口中仅4个 af/at/bt PoE++口、120W总预算。[EAP772 美国官方规格](https://www.omadanetworks.com/us/business-networking/omada-wifi-ceiling-mount/eap772/)为802.3at PoE+、25.4W最大功耗；[EAP775-Wall 美国官方规格](https://www.omadanetworks.com/us/business-networking/omada-wifi-wall-plate/eap775-wall/)列at/bt输入、45W含下游输出，官网称PoE Out需bt输入。本项目不启用AP PoE Out，也未实测各设备。下单时以对应地区/硬件版本再次确认。

大厅 `HALL-IOT-GW` 是从ES206XPP-M2到箱外墙面的本地网口，不是新增中央主干；Aqara有线网关和HA以太网协调器对同一批Zigbee设备二选一。仅最终型号支持PoE时才启用该口供电，否则使用墙口旁的普通插座。网关/协调器功耗和未来摄像头均未计入当前约87W余量，选型后须重算单口及总预算；上联、普通终端和闲置口关闭PoE。大厅五口中上联、AP、电视、网关口占四口，留一口未来候选；物理PoE口映射以实物为准，须保证AP及未来受电设备接真正PoE口。详见[网络拓扑的大厅端口表](network-topology.md#22-交换机-poe-与端口复核2026-10-15)。

### 2.3.3 未来 PoE 与扩口交换机评估（2026-10-15）

中央 ES210XPP-M2 两台 EAP775-Wall 的保守规划为 117W/200W，账面余量约83W；这对少量摄像头通常够用，但不是无限扩展额度。智能灯、开关和电池传感器通常不占PoE，摄像头、门铃和部分网关才占。最终设备必须按最大功耗×1.3及端口标准复核；例如4台12W规划功耗设备约62.4W，5台约78W，后者已经几乎耗尽余量。

中央住宅首选按需扩展：保留ES210XPP-M2，并在核心机柜预留一个2.5G口、插座、UPS功率和安装空间；确定摄像头/门铃后，增加 [ES206XPP-M2](https://www.omadanetworks.com/us/business-networking/omada-switch-agile/es206xpp-m2/#specifications) 作为下游专用PoE交换机。它用一个2.5G上联口，提供4个PoE++终端口和独立120W预算，无风扇；四路摄像头共享2.5G上联，须按码率和录像服务器位置验算。这样摄像头负载不挤占卧室AP所在的200W。

大型单机候选为 [SG3218XP-M2](https://www.omadanetworks.com/us/business-networking/omada-switch-access-pro/sg3218xp-m2/#specifications)：16×2.5G RJ45（4×PoE++、12×PoE+）、2×10G SFP+、240W总PoE、2个风扇。它适合明确超过4个新增PoE端口、必须单机汇聚或长期需要大量数据口的情况；但PoE总预算只比ES210XPP-M2多40W，并非端口翻倍后功率也翻倍。当前未把它替换进已选BOM。

用户随后确认电竞房不扩交换机，因此ES206X-M2双机和SG3218XP-M2替代方案退出当前候选。EAP775-Wall官方规格为1×2.5G上联、1×2.5G+3×1G下联；需要释放ES210端口时，将Apple TV/投影改接两个1G数据口。AP下联共享2.5G上联并继承AP故障边界，因此J3455/HA、Mac、NAS和PC不迁移到AP后面；本方案不启用PoE Out。

### 2.4 EAP775-Wall 暂选规格、供电边界与采购入口

2026-10-13暂选**EAP775-Wall ×3 / EAP772 ×1**，2026-10-14用户确认支持6GHz的三频硬件仍第一优先，v1.2形态/数量不变。两卧室改中央直接接AP并使用数据下联，电竞房单机本地Mac/NAS 10G、对外2.5G保持，不能沿用原中央NAS或四箱采购数量。双频备选及价差见[对比报告](ap-6ghz-selection-price-comparison.md)，仅在后续重新核验并确认后换型。

| 项目 | 美国官方规格与当前采用方式 |
|---|---|
| 无线与形态 | BE11000，2.4/5/6GHz 三频 Wi‑Fi 7，墙面面板形态；装在房间设备箱外 |
| 端口 | 上联 1×2.5GbE；下联 1×2.5GbE + 3×1GbE。全部下联共享 AP 上联，不是独立中央链路；不把三个千兆口当成 ≥2.5G 电脑口 |
| 输入供电 | 802.3at/bt；主卧/次卧由中央至少2个匹配PoE口供电，保守按45W/台需兼容bt与两AP合计117W预算；at须先核具体无转供模式/功耗。工作室由ES210XPP-M2匹配bt口直接供电，90W/口、200W全机 |
| 功耗口径 | 官网最高功耗 **45W（含 25W PoE Out）**。不能当作裸 AP 功耗，也不能由 45−25 推断裸机保证为 20W；无转供独立功耗/功能需进一步核验 |
| PoE Out 限制 | 官网概览称需 **802.3bt** 输入，规格表又写需 **802.3at**，存在内在矛盾；当前 **不启用 AP PoE Out**，不将其作为摄像头供电路径。若后续启用，先获得对应硬件/固件的明确官方条件并重算预算 |
| 工作室注入器 | **数量0**，ES210XPP-M2直接供电；POE260S及旧60W注入器占位不列当前电竞房采购 |
| 尺寸、温度与附件 | **172.9×91.2×41.3mm，0–40℃**；官方列有随箱墙面安装套件及可涂装盖板。实际底盒孔距、深度、线缆弯曲、墙体及发货配件核验后再补购，不能按机身尺寸直接订底盒 |
| 数量与渠道 | **3 台**：主卧、次卧、工作室各 1；[美国官方规格](https://www.omadanetworks.com/us/business-networking/omada-wifi-wall-plate/eap775-wall/#specifications)、[官方商城](https://store.omadanetworks.com/products/omada-be11000-tri-band-wall-plate-wi-fi-7-access-point-eap775-wall)、[美国 Amazon](https://www.amazon.com/dp/B0G88FG4QH) |

官网 BUY NOW 指向 Amazon ASIN **B0G88FG4QH**；已核标题为 **“Omada 7 Pro Wall, BE11000 Wireless Access Point, Paintable(EAP775-Wall)”**，副标题标明 Tri-Band/2.5G。2026-10-13仅核入口/标题，2026-10-14补核的购买栏报价/卖家/库存保存在[对比报告](ap-6ghz-selection-price-comparison.md)，不保证后续库存、具体发货硬件版、跨境发货或保修。美国三频规格解决了旧 EAP725-Wall 无 6GHz 的规格缺口，**不代表已确认在中国大陆可合法启用 6GHz**，地区认证与固件功能仍是采购前门槛。

### 2.5 Fusion 2.5G 普通版暂定与电源核验（2026-10-15）

用户在了解产品后明确“暂定fusion”，按本次推荐记录为 **Fusion 2.5G普通版×1（非PoE版）**，未购/未部署。该设备替换ER707-M2及J3455上的独立Omada控制器VM；HA继续使用J3455独立HAOS VM。中央/电竞房/大厅PoE交换机、四条2.5G主干、电竞房Mac RJ45与NAS SFP+本地10G沿用，中央仍5个连接；内置控制器不另占端口或独立硬件数量。

| 项目 | 本对话核验结果 | 规划含义 |
|---|---|---|
| 定位与接口 | 主路由 + 内置Omada Network管理应用；1×2.5G WAN + 4×2.5G LAN/WAN RJ45，最多4条同时WAN；无Wi-Fi、无PoE、无SFP | 光猫→Fusion→中央PoE交换机；普通版不能给卧室AP供电，保留中央交换机 |
| 管理规模 | 官方建议30台Omada管理设备、300客户端 | 当前三处交换机及4台AP在建议设备规模内；最终固件/adoption需验收 |
| 性能 | 官方IPS吞吐2183Mbps；不同VPN协议吞吐不同 | 实验室参数不等于本户PPPoE/IPv6/IPS/VPN实测，仍按1000/30Mbps套餐验收 |
| 普通版价格 | [美国官方商城](https://store.omadanetworks.com/products/omada-all-in-one-gateway-fusion-2-5g)：2026-10-15现价$169.99，划线价$184.99；同日ER707-M2 $99.99 | 快照未含税运/进口费用；普通版为本次暂定型号，价格非后续承诺 |
| PoE版区别 | [Fusion 2.5G PoE官方商城](https://store.omadanetworks.com/products/omada-gateway-controller-in-one-with-poe-fusion-2-5g-poe)：$349.99、预售；9×2.5G，8个PoE+口，110W总预算 | 非当前暂定型号；110W未覆盖现有两卧室AP的117W保守预留，不能据此删除中央PoE交换机 |
| 普通版电源 | [官方规格](https://www.tp-link.com/productpages/spec/116210-3.html)：USB-C适配器输入100–240V AC、50/60Hz，输出5V/3A；整机最大8.18W（含适配器） | 支持大陆220V，不需降压变压器；随箱美国SKU插头形状仍待卖家确认，必要时选合规转接头或明确支持5V/3A的国标USB-C电源 |
| 故障与维护 | 主路由与内置控制器共享Fusion整机、供电、重启和配置恢复边界 | J3455维护不再直接中断网络管理；Fusion重启须验证路由与控制器恢复，纳入中央UPS并导出配置 |

旧J3455 Omada Linux VM未实施，撤出当前计划后无需在J3455维护Java/MongoDB；之前无AVX/MongoDB 4.4兼容和EOL研究仅保留追溯，不要求按旧路径另行部署控制器。

**本套Omada设备的电压与插头记录：**

| 设备 | 已核供电规格 | 大陆使用与附件 |
|---|---|---|
| Fusion 2.5G普通版 | 100–240V、50/60Hz；USB-C 5V/3A | 电压支持；插头形状按实际美国发货SKU确认 |
| ES210XPP-M2 | [官方规格](https://www.omadanetworks.com/us/business-networking/omada-switch-agile/es210xpp-m2/#specifications)：适配器输入100–240V AC、输出54V/4.16A；随箱含电源适配器和电源线 | 电压支持；保留原装电源砖，按实物交流输入接口选择合规国标线，不预设C5/C7/C13 |
| ES206XPP-M2 | [官方规格](https://www.omadanetworks.com/us/business-networking/omada-switch-agile/es206xpp-m2/#specifications)：适配器输入100–240V AC、输出53.5V/2.43A；随箱含适配器和电源线 | 电压支持；国标线型/接地按实物确认 |
| EAP775-Wall×3 | [官方规格](https://www.omadanetworks.com/us/business-networking/omada-wifi-wall-plate/eap775-wall/#specifications)：802.3at/bt PoE | 当前由交换机供电，无独立市电插头/适配器采购 |
| EAP772×1 | [官方规格](https://www.omadanetworks.com/us/business-networking/omada-wifi-ceiling-mount/eap772/#specifications)：802.3at PoE，另可12V/2.5A DC但不附DC适配器 | 当前走大厅PoE，无需另买DC适配器 |
| 旧ER707-M2（已撤出） | 官方仅明确12V/1.5A适配器输出，本次未核交流输入范围 | 保留历史，不根据DC输出推定其随箱适配器支持220V |

美国渠道应核美标Type A/B与实际国标插座的匹配；本次官方资料未逐SKU锁定随箱插头，不能把通用或EU包装图当作美国发货证据。转换插头只改变形状，不改变电压；可拆电源线优先按实物换合规国标线，需要接地的连接保留接地。对确认100–240V输入的设备无需另购降压变压器。

## 3. 原方案产品规格记录：并非当前整套采购单

以下数量保留的是**NAS/J3455在工作室时的旧方案**，用于追溯型号与端口核验；不能按此表合并下单。TL-SX1008/双交换机组合均已撤出当前工作室采购，铜模块不再固定1/2个；**旧四台 EAP772 和工作室换 EAP773 的 AP 形态/数量已被房间面板 ×3 + 大厅吊顶 ×1 取代**。最新数量/状态见设备清单6.4；四台的信道、功率与覆盖按安装后实测调优，不把下面的历史数量当当前采购。

| 角色 | 型号 | 暂估数量 | 官方关键规格与用途 | 美国 Amazon |
|---|---|---:|---|---|
| 历史主路由/网关（已被暂定Fusion取代） | **ER707-M2** | 历史1台，当前不购 | 1×2.5G WAN + 1×2.5G WAN/LAN；另有千兆接口。WAN 与中央 LAN 必须用两个 2.5G 口；无风扇 | [商品页](https://www.amazon.com/dp/B0C238XMVV) |
| 中央 PoE 交换机 | **SG2210XMP-M2** | 1 | 8×2.5G PoE+、2×10G SFP+；160W 总 PoE、30W/口；无风扇；226×131×35mm | [商品页](https://www.amazon.com/dp/B0D5Z3NMG9) |
| 历史主卧/次卧/大厅小箱PoE交换机 | **ES206XPP-M2** | 历史3台；v1.2仅大厅1台，选型已确认 | 5×2.5G RJ45（4×PoE++）+1×10G SFP+；120W总预算/90W单口，无风扇、209×126×26mm。主卧/次卧两台已退出BOM，不按历史3台采购；不足电竞房十连接/多10G要求 | [商品页](https://www.amazon.com/dp/B0GKQ5SD2L) |
| 工作室 10G 交换机（同 LAN 条件） | **TL-SX1008** | 1 | 8×100M/1/2.5/5/10G RJ45；六连接后余两口；**非管理型、无 PoE**；1 个调速风扇；294×180×44mm；AC 100–240V 直接供电。需接受工作室不能配置端口 VLAN/Omada adoption | [商品页](https://www.amazon.com/dp/B0916BNNML) |
| 工作室 AP 本地 PoE 注入器 | **POE260S / TL-POE260S** | 1，与 TL-SX1008 配套 | 2.5G 数据/PoE 接口，802.3af/at、30W；供 EAP772；使用本地市电，不为 AP 增加中央回线 | [商品页](https://www.amazon.com/dp/B0C54CPVXV?th=1) |
| 三频 Wi-Fi 7 AP | **EAP772** | 最多 4 | 2.4/5/6GHz 三频；1×2.5G 上联；IEEE 802.3at PoE+；官方 PoE 最大功耗 25.4W；安装在箱外 | [商品页](https://www.amazon.com/dp/B0D2M26NYW) |
| 历史Omada软件控制器（已撤出计划） | **现有J3455/Proxmox上的独立Linux VM** | 旧计划1个实例，未部署；当前使用Fusion内置控制器 | 官方Linux控制器 + Java 17 + MongoDB 4.4；J3455无AVX，不升级至MongoDB 5+。MongoDB 4.4上游EOL，限制管理面访问、定期配置备份并保留迁移/OC200回退路径 | [官方Linux安装指南](https://www.omadanetworks.com/en/support/faq/3272/) |
| 中央至工作室主干 10G 铜模块（有条件） | **SM5310-T** | 单交换机方案共 1，中央侧 | SFP+ 转 1/2.5/5/10G RJ45；10G 使用 Cat6A 或更高等级，**整条铜通道上限 30m，含跳线**。TL-SX1008 一端为原生 RJ45，不另买模块；管理型组合在工作室端另需 1 个，合计 2 个 | [商品页](https://www.amazon.com/dp/B0B12N5SJN) |

### 3.1 房间交换机的使用规则

- 本节上表中的3台是历史数量；v1.2 ES206XPP-M2仅大厅1台，用户已确认选型、未购/未部署，主卧/次卧取消。大厅用1个RJ45作2.5G上联、1个匹配PoE口接EAP772，余3个铜口再按电视/网关/其他终端实数分配，不能在已计设备后仍称余3口。标准PoE识别受电设备，普通电脑可接PoE口。
- 120W 是全机总预算，不是四个端口同时各提供 90W。大厅 EAP772 可沿用已有 25.4W 记录做候选预算；EAP775-Wall 的 45W **包含 25W PoE Out**，不能套用 EAP772 功耗或称其为裸 AP 功耗。当前不转供；无转供功耗未核清前可用 45W 保守预留并注明假设，获得相应版本证据后细化。每台交换机按实际所供设备总负载 ×1.3 留量并核单口上限，不重复计算已包含的下游功耗。
- 该交换机由**本地外置适配器**供电，不靠中央交换机 PoE 受电。中央 UPS 不能自动保障房间交换机/AP。
- 使用 10G SFP+ 上联时，五个 RJ45 仍然只有 2.5G。不能把一个 SFP+ 口同时算作 10G 上联和 Mac Studio 的第二个 10G 接口。
- ES206XPP-M2仍不作为工作室交换机：v1.1的Mac/NAS需两个同时可用10G接口，另需八个2.5G端口，它只有一个SFP+和五个铜口。
- ES206XPP-M2 已列入官方 Omada SDN 兼容清单，支持硬件/软件控制器；需使用相互支持的软件控制器版本与交换机固件并做 adoption 验收，不能保证任意旧固件即插即管。

### 3.2 网关速率不能只看端口

**旧ER707-M2性能研究，现已改暂定Fusion**：ER707-M2官方实验室数据为PPPoE NAT约2347/2348Mbps；IPS TCP约1552Mbps、UDP约1206Mbps。用户计划1000Mbps下行/30Mbps上行，2026-10-14曾确认ER707-M2、未购/未部署；2026-10-15改为暂定Fusion普通版，不因局域网10G加购10G路由；仍验PPPoE/IPv6、IPS/VPN及实际套餐表现。30Mbps上行理论约3.75MB/s，异地备份/远程文件受限，不影响本地10G；不能将该套餐描述成国内所有线路的上行上限。

Mac Studio/NAS 在同一局域网交换 10G 数据，不需要路由器或所有 AP 都是 10G。跨 VLAN 的大流量要另验网关/三层交换性能；工作室 10G 本地链路不等于互联网 10G。

### 3.2.1 光口拨号能否替代光猫（2026-10-14）

用户准备在**电信或联通**中选择，运营商及具体线路尚未确定。此前“普通光口不能替代光猫”应理解为接口与协议限制，**不是所有形态下都必须保留一个独立光猫盒子**。

| 功能 / 设备 | 能否由现选主路由直接承担 |
|---|---|
| PPPoE 拨号、NAT、防火墙、DHCP | 光猫桥接、运营商允许且参数齐全时，当前暂定Fusion可承担；部分线路用DHCP/IPoE，按实际业务确认 |
| PON 光接入、OLT 注册及运营商管理 | 普通以太网 SFP 模块与 PPPoE 不能承担；仍需兼容的 ONU/ONT 功能 |
| 带 ONU 的 SFP 猫棒 / 内置 PON 的路由设备 | 技术上可把独立光猫的功能合入模块或主机，前提是运营商认可及完整链路兼容；并非“无光猫功能” |
| 运营商交付的是以太网光口而非 PON | 匹配以太网光模块的路由器可按该交付方式接入，但不能据此推定本户电信/联通住宅线路也是以太网光交付 |

**旧ER707-M2的具体限制（当前已改暂定Fusion）**：[美国官方商城规格正文](https://store.omadanetworks.com/products/omada-multi-gigabit-vpn-gateway-two-2-5g-ports)列出 1×2.5G RJ45 WAN、1×2.5G RJ45 WAN/LAN、**1×Gigabit SFP WAN/LAN**、4×Gigabit RJ45 WAN/LAN。因此它的 SFP 是 **1G**，不是 2.5G/10G SFP+；即使某 ONU 模块能够工作，经过此口的有效数据吞吐仍受千兆接口及协议开销限制，不能利用另外两个 2.5G 网口的速率宣传来替代。当前未找到 ER707-M2 与 ONU 猫棒的官方兼容声明，不能承诺插入即可使用。

**官方原理证据**：TP-Link [XM60A](https://www.tp-link.com/us/service-provider/gpon/xm60a/)明确为 GPON ONU SFP Module，包含 GPON/OMCI 功能，支持 2.5G/1G Ethernet UNI；PON侧标称下行2.488Gbps、上行1.244Gbps。它证明了厂商确有“把ONU做进SFP模块”的产品，而非普通光电转换模块。这不是本项目推荐采购项，未验证其与 ER707-M2 或中国电信/联通的兼容性。其 GPON 规格也不能套用到 EPON、XG-PON 或 XGS-PON。MikroTik 的[已停产 SFPONU](https://mikrotik.com/product/SFPONU)同样明确含 GPON OMCI Stack，仅作原理交叉证据，不进入 BOM。

在考虑任何替代前，向最终运营商确认：

1. 本户实际为 GPON、EPON、XG-PON、XGS-PON 或其他交付方式；套餐名“千兆”不能确定 PON 制式。
2. 是否支持用户自备 ONU/ONT、如何正式注册；具体可能涉及 SN、LOID、PLOAM 密码等认证方式，并核 OLT/OMCI 业务兼容。不同线路未必使用全部字段，不把 PPPoE 账号当作 PON 注册凭据。
3. 路由器 SFP 主机侧速率/电气模式、模块固件、供电、温度、光纤连接器及光功率是否匹配；PON侧速率和主机侧以太网速率分开核验。
4. Internet VLAN、IPv6、IPTV/语音业务、远程维护和故障报修是否仍正常；保留原光猫回退，不在未获认可时擅自替换在线接入设备。

当前建议保持 `入户PON光纤 → 运营商认可的光猫/ONT（桥接）→ RJ45 → Fusion 2.5G WAN`。当前暂定Fusion普通版只有RJ45网口，无SFP/ONU功能，不能直接插PON光纤或猫棒。优先核带2.5G LAN的ONT；仅有1G光猫网口时记录其链路/实际吞吐边界。上面的ER707-M2与猫棒资料保留历史研究，当前不采购猫棒、不删除光猫BOM；未操作运营商线路或现网设备。

### 3.3 10G 接口与距离限制

Mac使用电竞房交换机原生10G RJ45，NAS使用10G SFP+。中央到四房的主干均为2.5G RJ45 Cat6A，**无需主干10G铜模块**。Mac本地合格Cat6A原生10GBASE-T完整通道上限100m（永久链路通常90m+跳线合计10m），实际端接和长度须认证；NAS已确定靠近工作室交换机，当前用兼容SFP+ DAC短线，按实际两端兼容/长度验收，不把Cat6A规格套给SFP+链路，也不埋DAC入墙。

SM5310-T的10G铜通道上限30m仅是旧模块方案的限制，不是当前2.5G主干限制。若后续NAS只带RJ45，需要另审接口方案、模块兼容/散热/距离后才购买，当前不默认加入铜模块。

最新布局中Mac/NAS接同一电竞房交换机，同VLAN10G流量不走2.5G主干。10GbE理论约1.25GB/s，实际受磁盘/CPU/协议制约。J3455目前为千兆影音NAS/代理服务器，用户计划升级2.5G，尚未实施；不是10G NAS或可随意改装的空闲主机。升级复用电竞房已分配端口，不改变四条主干或十口占用；先核主板接口、网卡与Proxmox驱动和桥接迁移，验收实际吞吐/重连。下文现1G限制仅针对升级前，网卡升级不消除磁盘/CPU瓶颈。

### 3.4 工作室两种互斥组合与端口表

**本小节为历史方案存档：A/B均已撤出当前工作室采购。下列六连接、模块1/2个与扩口只描述旧布局，不是当前建议。v1.1确认的电竞房ES210XPP-M2十口方案/NAS与J3455在电竞房/上联2.5G由v1.2继续保留；两卧室箱/交换机另已取消。旧工作室EAP772/EAP773及全屋四台EAP772已被三面板一吊顶取代。**

**方案 A：维持图中一台工作室交换机。** TL-SX1008 ×1 + POE260S ×1，配 SG2210XMP-M2 时 SM5310-T 全屋共 1 个。这是第一阶段同一可信 LAN 的候选，不是已批准购买；若要求工作室端口 VLAN 或完整 Omada 管理，应选方案 B 或继续寻找合适的单台管理型产品。不能假定非管理型交换机已经验证了 VLAN 标签透传。

| TL-SX1008 端口 | 连接设备 | 规划速率/供电 |
|---|---|---|
| 1 | 中央唯一 Cat6A 主干 | 10G；中央侧铜模块的 30m 限制仍适用 |
| 2 | Mac Studio | 10G |
| 3 | 未来 NAS 预留 | 10G；NAS 尚未购买 |
| 4 | POE260S → EAP772 | 2.5G，注入器提供 802.3at PoE+ |
| 5 | 现有 J3455 | 按实际网卡速率，不默认 2.5G/10G |
| 6 | 电竞电脑 | ≥2.5G；网卡支持时可协商 10G |
| 7–8 | 备用 | 两个原生 10G RJ45 |

TL-SX1008 官方为一个调速风扇，并非无风扇；最大功耗 31.2W，工作温度 0–50℃。工作室箱按 294×180×44mm 机身加电源线、插头、配线弯曲、注入器和检修空间测量，不能套用卧室薄型小箱或承诺静音。

**方案 B：需要 Omada/VLAN 时的管理型扩口组合。** SX3206HPP ×1 + ES206X-M2 ×1，替换方案 A 的 TL-SX1008 和 POE260S，不是叠加采购；配原中央交换机时 SM5310-T 全屋共 2 个。这会让工作室变成两台交换机、房间侧总数变为五台，**偏离当前一箱一交换机图示，须接受新增设备/空间/风扇噪声后再采用**，不增加任何中央主干。

| 设备/端口 | 分配 | 限制 |
|---|---|---|
| SX3206HPP SFP+ 1 | SM5310-T → 中央 Cat6A 10G 主干 | 模块兼容与整条铜通道 ≤30m；中央侧也需模块 |
| SX3206HPP RJ45 1、2 | Mac、未来 NAS | 各 10G |
| SX3206HPP RJ45 3 | EAP772 | 2.5G + 匹配 PoE；选 EAP773 时可用原生 10G PoE 链路 |
| SX3206HPP RJ45 4 | ES206X-M2 RJ45 上联 | 2.5G |
| SX3206HPP SFP+ 2 | 备用 SFP+ | **不计为已可用的额外铜口** |
| ES206X-M2 其余 RJ45 | 电竞电脑、J3455，另余两口 | 电竞电脑最高 2.5G；两设备跨此分支共享 2.5G 上联 |

SX3206HPP 是 **4×多速率 10G RJ45 + 2×10G SFP+**，不是六个铜口；四个铜口支持 af/at/bt（type 3），60W/口、200W 总预算，无需 AP 注入器。官方推荐 **只使用一个 SM5310-T 模块**，因此不能默认把两个 SFP+ 都插铜模块来实现六个 RJ45。其有两个风扇，294×180×44mm，AC 100–240V；另加 ES206X-M2 及其电源的箱体空间一起核算。

历史升级设想曾在方案B把工作室EAP772换EAP773，即EAP772×3+EAP773×1；该设想已撤销，不满足面板要求。v1.1大厅保持EAP772、AP链路2.5G，不按旧设想升级10G。旧研究的六连接/四连接与余量缺口不再用于当前十口布局。

## 4. 按需替代与升级项

| 型号 | 适用情形/限制 | 美国 Amazon |
|---|---|---|
| **TL-SX105** | 5×10G RJ45、无风扇、非管理型、无PoE；不足当前电竞房十连接，且不满足Omada管理，仅留历史 | [商品页](https://www.amazon.com/dp/B09CYNHL4S) |
| **SX3206HPP + ES206X-M2** | 历史方案B见第3.4节，因工作室噪声/两台限制已撤下。产品可另作机柜研究，但不按旧房间拓扑直接采购；四铜/两SFP+不可当六铜口，SX推荐只用一个铜模块 | [SX3206HPP 商品页](https://www.amazon.com/dp/B0BPDHZ9S9)、[ES206X-M2 商品页](https://www.amazon.com/dp/B0GRCDJJTC) |
| **ES210X-M2（无PP）** | 8×2.5G + 2×10G SFP+、无PoE；**v1.2不能直接给两卧室AP供电，退出当前直接供电候选**。如另审中央2.5G/匹配PoE注入器回退可评估，但不自动增加配件。不是电竞房型号 | [商品页](https://www.amazon.com/dp/B0GKPNRFGF) |
| **ES210XPP-M2** | **电竞房已选1台**，8×2.5G PoE++ + 1×10G RJ45(Mac) + 1×10G SFP+(NAS)；2.5G上联。完整直连会占满十口，Apple TV/投影改接AP后可释放两个2.5G口。美国规格和官方商城已核，采购前复核版本/库存/跨境保修 | [精确商品B0HB17QTKX](https://www.amazon.com/dp/B0HB17QTKX)，2026-10-15 $229.99；[官方商城](https://store.omadanetworks.com/products/omada-8-port-2-5g-2-port-10g-easy-managed-switch-with-8-port-poe-es210xpp-m2)同价，见[集中BOM](purchase-bom.md) |
| **POE260S** | 旧非PoE方案配件，2.5G、af/at、30W；不能直接保证EAP775-Wall含转供45W工况。当前电竞房注入器数量0，不购买；其他房间若改非PoE再单独核验 | [历史商品页](https://www.amazon.com/dp/B0C54CPVXV?th=1) |
| **ES206X-M2** | 5×2.5G + 1×10G SFP+、无PoE；仅大厅如改用匹配本地注入器时另审，**主卧/次卧不采购交换机**。不增加中央AP回线，也不满足电竞房十连接/多10G要求 | [商品页](https://www.amazon.com/dp/B0GRCDJJTC) |
| **TL-SG105-M2** | 简单同网段的经济型房间数据交换机；5×2.5G，**非管理型、无 PoE**，不作为房间 VLAN 管理方案 | [商品页](https://www.amazon.com/dp/B08ZHGT2ZP) |
| **EAP773** | **仅大厅吊顶条件升级**：AP 到交换机确实采用 10G 且有需求时，可替换大厅 EAP772，不额外加购；三频 Wi-Fi 7、1×10G 上联，已有官方记录为 802.3at、25.4W。接 2.5G 交换机/注入器仍受其限制，不能作为主卧/次卧/工作室面板 AP 替代 | [商品页](https://www.amazon.com/dp/B0CTL1Y9YR) |
| **EAP725-Wall（非默认双频备选）** | Wi-Fi 7、2.4/5GHz、2.5G上联；**US V1.20下联1×2.5G+2×1G，US V2下联1×2.5G+3×1G**。2026-10-14报价商品描述与V1.20端口一致但不证明发货版本，不能保证买到V2；先核两卧室端口/PoE/底盒。三频775仍第一优先，不计入当前BOM，见[对比报告](ap-6ghz-selection-price-comparison.md) | [备选商品页](https://www.amazon.com/dp/B0FB1W85FN) |
| **EAP723（非默认双频备选）** | 仅用于大厅吊顶替代评估；Wi-Fi 7、2.4/5GHz、1×2.5G上联、无电脑下联。官方商城标V2，Amazon硬件版待核；PoE/安装件/地区支持需复核。三频772仍第一优先，不计入当前BOM | [备选商品页](https://www.amazon.com/dp/B0DT4YP2GX) |
| **ER8411** | WAN 超过 2.5G或网关重载时另做性能选型的 10G 网关候选；不是 Mac/NAS 局域网 10G 的前提 | [商品页](https://www.amazon.com/dp/B0BK9T1P5F) |

未采用 SG2008P-M2：本轮没有确认其美国官方产品和购买入口；不要凭名称采购。能核验的 SG2008P（不含 -M2）是千兆，不能替代本项目多千兆房间链路。

### 4.1 必须纳入预算的配线、箱体与电源

本节按当前机柜布局更新；用户未设预算上限，不等于应购买所有备选或未经核算的大容量UPS。

这些是网络设备之外的施工/供电项目；品牌不强求 TP-Link。长度、面板和电源配件先复尺，未核验具体商品，不编造 Amazon 型号或把施工服务算成已采购设备。

| 项目 | 数量基线 | 采购/施工要求 |
|---|---|---|
| Cat6A实芯纯铜主干 | 4条，米数实测 | 2条直接到卧室AP、2条到电竞房/大厅交换机，均2.5G；卧室主干匹配PoE，拒CCA，100m通道认证，无主干10G模块 |
| Cat6A房内分支 | 电竞房面板AP/大厅顶面AP各1条本地支线；卧室AP下联电脑/墙口和其他终端另计 | 电竞房另到Mac/PC×2/Mini/J3455/AppleTV/投影，Mac原生RJ45本地10G；附近NAS用SFP+ DAC短线，不计Cat6A，卧室3个1G口不视为2.5G |
| NAS 10G SFP+网卡/接口与链路 | 网卡是否需另购依NAS配置；一条本地链路 | NAS已确定靠近交换机，兼容DAC短线×1，型号/长度待NAS选型；不另买光模块对/光纤 |
| Cat6A 端接模块、配线架/支架、墙面板 | 仅四主干两端都模块端接时为8模块；直达AP可合规MPTL端接，按端接表核数量，分支另计 | 适配实芯Cat6A与PoE，按通道或MPTL方案认证；屏蔽系统连续接地，不只看线皮类别 |
| Cat6A 成品纯铜跳线 | 仅四主干两端均模块端接时共8条；直达AP现场插头方案据实扣减，设备与分支另计 | 按新端口表计，不沿用旧SX↔ES互联或注入器跳线；附近NAS使用SFP+ DAC，电竞房无第二台交换机 |
| 面板 AP 底盒/安装板配套 | 3 套，主卧/次卧/工作室各 1 | EAP775-Wall 随箱含墙面安装套件/可涂装盖板；以 172.9×91.2×41.3mm 机身核现场孔距、底盒深度、线缆弯曲及维护，只补缺件，不重复购买已含安装板，不把房间交换机箱当 AP 底盒 |
| 大厅吊顶 AP 支架/固定件 | 1 套 | 核吊顶/楼板结构、承重、维护及随箱支架；已有附件不重复购买，AP 装顶面而非藏吊顶内 |
| 可维护房间箱与核心机柜/设备位 | 房间箱2个（电竞房/大厅），主卧/次卧设备箱取消；中央核心网络1处，电竞房箱外存储位另测 | ES210XPP-M2适配器/配线另量，Mac/NAS/J3455不塞箱；中央/电竞房/大厅分别核供电/散热/维护，通风不保证隔音 |
| 电源插座/排插/电源线 | 中央及电竞房/大厅网络位置核算；卧室AP不单列市电适配器 | 两卧室AP中央PoE供电，卧室其他用电设备独立预留；100–240V设备不代表UPS适用，按当地电压/接地选，不套美国120V版本 |
| UPS及后备供电 | 中央含两卧室PoE AP；电竞房Mac/存储/交换机/AP；大厅交换机/AP | 至少1小时目标，取消卧室网络箱专用UPS；下联电脑不随AP数据口供电，需保活者另核。必要排风同计，按实测/续航曲线选，不仅看VA，低电量安全关机 |
| 空管、牵引线、标签、理线/安装辅件 | 四条主干及各分支逐点统计 | 不默认再铺第二条中央网线；标出 TRUNK 编号、端口号和 PoE 供电位置 |
| 布线认证与交付记录 | 四主干 + 所有实际支线 | 保存长度、线序及 Cat6A 性能测试；协商到 10G 不等于完成线缆认证 |

网卡仅在现有电脑接口不足时补购 ≥2.5G/10G 型号，先核 PCIe/USB/Thunderbolt 与驱动；J3455 不因画在图上就必须升级 10G。未来NAS、摄像头仍待选；大厅HomeView非壁挂／桌面版×1已确认（Wi-Fi/Thread已核，未购；大陆服务/账户/配套设备待验），三房新购优先推荐mini 2但代际待用户确认。见[Apple官方核验](apple-home-devices-2026.md)，不为占位图购买重复设备，HomeView保持大厅Wi-Fi及随箱电源，不采购壁挂版/PoE底座。壁挂另选平板或iPad，型号/数量/点位/供电与接入方式待定，不先追加端口/PoE。

## 5. 小弱电箱、无线与验收

### 5.1 箱体与供电

- ES206XPP-M2 的 209×126×26mm 仅是机身尺寸；箱体还需容纳外置电源、插座、网线插头、Cat6A 弯曲余量和手部维护空间，不能按机身尺寸直接订箱。
- 使用可打开的门板、通风路径与防尘措施；无风扇不等于不发热。ES206XPP-M2 官方工作温度上限为 40℃，关闭门板、夏季负载时也须满足。
- ES206XPP-M2/ES210XPP-M2外置适配器按100–240VAC输入复核，核随箱电源、插头/接地及强弱电分隔；不因旧TL-SX1008/SX3206HPP参数购买当前配件。电竞房ES210XPP-M2机身226×131.2×35mm，适配器、弯曲和操作空间另加，工作温度上限40℃，无风扇仍需通风。
- 两卧室AP由中央匹配PoE供电，随中央UPS核负载；电竞房/大厅AP由当地交换机供电，另核后备。NAS/Mac/全网络至少1小时目标不变，取消两卧室网络箱UPS，不代表HomePod/下联电脑市电设备自动保活。UPS不强求TP-Link但排除小米/华为，不增第二数据主干或未经设计后备电路。
- 仅电竞房/大厅两箱核电源/配线/散热，卧室仅面板安装位。Mac/NAS/J3455电竞房箱外，电竞房UPS计存储/Mac负载，中央UPS不覆盖；电竞房交换机故障影响本房互联，主干故障影响跨房/外网而不必然断同VLAN本地转发，服务依赖须测。卧室AP故障会同时断本房无线及其有线下联。

### 5.2 无线与智能家居

- AP 有线回程，不把无线 Mesh 当作主干。按用户要求配置房间面板 ×3 + 大厅吊顶 ×1，四台不等于全部满功率开启；按户型墙材、家具和覆盖实测调优信道、功率与无线启用策略，不在未确认时改动 3+1 BOM。
- 三间房面板EAP775-Wall与大厅EAP772为三频第一优先，双频仅在[对比报告](ap-6ghz-selection-price-comparison.md)留备选。实际可启用频段仍受地区法规、硬件/固件版本与终端能力约束，美国销售规格不等于在中国大陆合法可用。
- HomePod mini 和大量 IoT 不会因为 AP 标称 Wi-Fi 7 就获得 6GHz/多千兆能力。为 Aqara/老设备保留兼容 2.4GHz SSID；6GHz 网络与安全设置另按终端支持情况验收。
- 第一阶段 Apple Home、HomePod、HA、Aqara 网关在同一可信网络完成配网和端到端控制。若以后分 VLAN，验证 mDNS/Bonjour、IPv6、组播和最小必要 ACL；不要默认 VLAN 开完就能无障碍控制。
- 住宅在中国大陆，按用户偏好保留美国版候选；[6GHz专项报告](wifi7-6ghz-mainland-china-research.md)已完成公开资料研究，当前按真实地区与合规2.4/5GHz部署，不把6GHz计入保证能力。地区SKU认证、固件行为和跨境保修仍未验收；不从网友修改国家码的成功自述推定本项目可用。

### 5.3 建议验收门槛

1. 保存Fusion与全套设备的最终SKU、硬件/固件版本及回滚方法；验证Fusion内置控制器识别并管理所有交换机/AP，导出配置并测试恢复。稳定固件先小范围升级；不在J3455部署控制器或MongoDB。
2. 四条Cat6A中央主干均验收2.5G，房间分支另计；Mac本地RJ45和NAS本地SFP+协商10G，附近NAS链路记录兼容DAC型号/长度。完成线材认证和并发吞吐测试，不把协商速率当文件拷贝成绩。
3. 进行 24–72 小时负载验收：并发下载/局域网拷贝、模型/视频主机负载、游戏延迟、HomePod 播放、HA 控制与断连日志；记录箱内温度。
4. 在卧室—工作室—大厅移动验证漫游；客户端决定切换，不能承诺任何终端都无缝零丢包。不要只测测速软件最高分。
5. 断电/网关/控制器/AP重启后验证恢复；中央UPS覆盖两卧室PoE AP，不覆盖AP下联电脑；电竞房/大厅普通交换机不透传中央PoE，分别测当地UPS/Apple Home/HA恢复。
6. 电竞房ES210XPP-M2按完整直连表会占满十口；将Apple TV/投影改接AP后应验收两个ES210端口空闲、AP仍余1×2.5G+1×1G，并记录实际端口映射。中央五连接另留余量；Mac↔NAS/AppleTV↔J3455同VLAN本地并发与2.5G跨房访问分别测试。J3455/Mini/现PC仍为1G，AppleTV/投影按实机。旧A/B及v1.0不按其数量验收；UPS按新位置实测至少1小时后记通过，并验证黑群晖、HAOS VM有序关机/恢复及Fusion内置控制器重启恢复。
7. AP仍3面板EAP775-Wall+1吊顶EAP772，上联2.5G；卧室下联验1×2.5G+3×1G及有线/无线并发共享回程。45W含25W转供不推定裸机；本方案使用数据下联但不转供。中央2口匹配PoE/总预算，电竞房匹配bt/200W本地预算，注入器0；地区/6GHz/版本单独验收。

- [Fusion 2.5G美国官方商城](https://store.omadanetworks.com/products/omada-all-in-one-gateway-fusion-2-5g)、[官方规格正文](https://www.tp-link.com/productpages/spec/116210-3.html)：本对话2026-10-15核验，普通版主路由+内置控制器、5×2.5G及宽压USB-C供电，见第2.5节。

## 6. 官方证据与采购前未决事项

### 官方资料

- [ER707-M2](https://www.tp-link.com/us/business-networking/omada-router-wired-router/er707-m2/)、[ER8411](https://www.tp-link.com/us/business-networking/omada-router-wired-router/er8411/)。
- [SG2210XMP-M2](https://www.omadanetworks.com/us/business-networking/omada-switch-access-pro/sg2210xmp-m2/)。
- [ES206XPP-M2](https://www.tp-link.com/us/business-networking/omada-switch-agile/es206xpp-m2/)、[ES206X-M2](https://www.tp-link.com/us/business-networking/omada-switch-agile/es206x-m2/)、[Omada 兼容清单](https://www.tp-link.com/us/omada-sdn/product-list/)。
- [EAP775-Wall 美国官方规格](https://www.omadanetworks.com/us/business-networking/omada-wifi-wall-plate/eap775-wall/#specifications)、[官方商城](https://store.omadanetworks.com/products/omada-be11000-tri-band-wall-plate-wi-fi-7-access-point-eap775-wall)：2026-10-13 核验，三频/2.5G/尺寸及随箱附件见第2.4节；PoE Out 的 at/bt 条件在同页存在矛盾，未据此承诺转供能力。
- [EAP772](https://www.tp-link.com/us/business-networking/omada-wifi-ceiling-mount/eap772/)、[EAP773](https://www.tp-link.com/us/business-networking/omada-wifi-ceiling-mount/eap773/)、[EAP725-Wall（非默认双频备选，须区分版本）](https://www.tp-link.com/us/business-networking/omada-wifi-wall-plate/eap725-wall/)；725指定版本与723商城证据、四款AP报价见[对比报告参考资料](ap-6ghz-selection-price-comparison.md#6-参考资料)。
- [Omada软件控制器Linux安装指南](https://www.omadanetworks.com/en/support/faq/3272/)：官方列出Java、MongoDB版本兼容和AVX要求；[官方下载页](https://support.omadanetworks.com/us/download/software/omada-controller/)提供Linux `.deb`/`.tar.gz`；[MongoDB生命周期](https://www.mongodb.com/legal/support-policy/lifecycles)用于确认4.4已EOL。[OC200](https://www.tp-link.com/us/business-networking/omada-controller-hardware/oc200/)仅保留为历史/回退候选。
- [TL-SX1008](https://www.tp-link.com/us/business-networking/unmanaged-switch/tl-sx1008/)、[TL-SX105](https://www.tp-link.com/us/business-networking/unmanaged-switch/tl-sx105/)、[TL-SG105-M2](https://www.tp-link.com/us/business-networking/unmanaged-switch/tl-sg105-m2/)。
- [SX3206HPP](https://www.tp-link.com/us/business-networking/omada-switch-access-max/sx3206hpp/)：四个 RJ45、两个 SFP+，官方建议只使用一个 SM5310-T 铜模块。
- [ES210X-M2](https://www.tp-link.com/us/business-networking/omada-switch-agile/es210x-m2/)、[ES210XPP-M2](https://www.omadanetworks.com/us/business-networking/omada-switch-agile/es210xpp-m2/)：二者10G接口不同，不混用；后者官方规格/商城当次可售已核，见第2.3节。
- [POE260S](https://www.omadanetworks.com/us/business-networking/omada-accessory-power-poe/poe260s/)、[SM5310-T](https://www.omadanetworks.com/us/business-networking/omada-accessory-module-cable/sm5310-t/)。

既有研究保留原日期。2026-10-15已核5款现行Omada精确Amazon商品/价格与官方商城，ES210XPP-M2的ASIN为B0HB17QTKX，产品信息型号明确；完整报价/卖家/数量边界见[集中BOM](purchase-bom.md)。价格/库存随时变化，不承诺跨境、当地认证、保修或所有硬件版本参数一致。软件/PoE/DAC须按最终发货版本验收。

### 下单前需要锁定

- 宽带目标1000/30Mbps；主路由暂定Fusion 2.5G普通版，未购/未部署。运营商、桥接/PPPoE/IPv6/CGNAT与IPS/VPN配置待验；大厅ES206XPP-M2保留，中央PoE推荐型号待确认；ER707-M2/J3455 Omada VM/OC200不进入当前采购部署。
- v1.2四条2.5G主干：两卧室直达Wall AP并利用1×2.5G+3×1G下联、无箱/交换机，电竞房/大厅各一箱一交换机。电竞房单台ES210XPP-M2、Mac RJ45/NAS SFP+本地10G；完整直连会占满十口，Apple TV/投影改接AP后释放两个2.5G口，复核实际端口映射、固件/NAS网卡/介质。中央5连接/建议≥8铜口且2口匹配卧室AP PoE/功率，SKU/总预算待核；不购旧铜模块/电竞房注入器，不采用大厅汇聚卧室AP。
- J3455基本配置与已有黑群晖VM/代理服务已登记；HAOS VM位置已定但尚未实施，先核盘数/容量口径/健康/备份与空闲资源。Omada由暂定Fusion内置控制器承载，核全套adoption、配置导出/恢复与中央UPS；未来高速NAS尚未采购。
- AP 已暂选 **EAP775-Wall 面板 ×3 + EAP772 吊顶 ×1**；地区版本/6GHz 合法使用、供货和保修待核。房屋约100㎡、设计图未出，墙材、三个面板安装位及大厅顶面支线/固定方式、信道和功率待实测；不由面积推断线长或机柜尺寸。核 EAP775-Wall 45W 含转供的功耗口径、无转供独立功能/功耗及工作室供电；当前不启用 AP PoE Out，官网 at/bt 转供条件矛盾待官方澄清。核底盒/支架和随箱附件，不重复购买。
- NAS/Mac/全屋网络至少1小时后备供电目标已确认；UPS型号/容量按各位置实际负载、Mac工况、必要排风与厂家曲线锁定，另验有序关机/恢复。
- 最终发货版本、官方兼容清单、固件、卖家、退换货和价格；本轮未采购或配置设备。文档的 Git 提交、远端同步及合并状态以仓库实际交付记录为准，不把型号暂选视为已下单。

### 2026-10-14 设计变更追溯

同日用户曾确认ER707-M2主路由×1、ES206XPP-M2大厅交换机×1、OC200独立控制器×1；OC200未购买，并于2026-10-15被J3455上的软件控制器方案取代。中央推荐ES210XPP-M2×1、待用户确认，详见第2.3.1节。用户考虑电信或联通、运营商未定；光猫桥接和猫棒条件见第3.2.1节，当前不取消光猫。

### 2026-10-15 控制器与HA主机决定（较早方案，已被Fusion取代）
> 同日最新决定为暂定Fusion 2.5G普通版及其内置控制器，下段保留较早的J3455方案与兼容性研究，不再作为实施要求。

用户决定由现有J3455/Proxmox分别承载独立HAOS VM和独立Omada Linux VM，保留黑群晖VM及代理/转发服务。官方Linux控制器本体没有AVX要求；官方指南确认v5.15.20+可使用MongoDB 4.4～8，而MongoDB 5+在x86_64需要AVX，因此无AVX的J3455采用MongoDB 4.4。该数据库已经上游EOL，故此选择附带管理面隔离、固定版本、配置备份及未来迁移要求。OC200退出当前BOM，中央物理连接由6减至5；尚未创建VM、修改现有服务或完成验收。

本次用户明确放弃电竞房双交换机，选择 ES210XPP-M2 单台；当时按全部终端直连交换机记录为零备用口。随后确认EAP775-Wall还有1×2.5G+3×1G下联，Apple TV/投影改接后可释放两个ES210口，因此“零备用”只描述完整直连基线，不再是唯一接法。10G RJ45专给Mac、SFP+专给高速NAS，替代2026-10-13 v1.0的中央NAS与工作室10G上联。旧A/B、SX3206HPP+ES210XPP双机建议和SX3832MPP大型单机均未采用，不合并下单；NAS/J3455位置、UPS与施工点位跟随新台账核算。

同日v1.2用户取消主卧/次卧设备箱与ES206XPP-M2两台，改中央各1条Cat6A/2.5G直达EAP775-Wall并由匹配PoE口供电；AP的4个下联为1×2.5G+3×1G，用于有线电脑/终端。四主干不变、房间箱/交换机由4减2，中央仍6连接但新增2个实际PoE负载；卧室AP随中央UPS、取消卧室网络箱UPS。v1.1四箱与上表历史数量不用于当前采购。

### 2026-10-15 Fusion暂定（最新）

用户暂定Fusion 2.5G普通版×1，使用内置Omada控制器；ER707-M2与J3455 Omada VM退出当前计划，OC200不采购，HA继续在J3455独立HAOS VM。Fusion未购/未部署；保留光猫与中央PoE交换机，四条2.5G主干、中央5连接、电竞房Mac/NAS本地10G及现有端口分配沿用。规格、价格、电压/插头证据见第2.5节。

### 2026-10-15 采购一致性与NAS介质

新增[集中采购BOM](purchase-bom.md)，已确认/暂选/未决分开；刷新Fusion/ES210/ES206/775/772精确Amazon与官方报价，未将中央推荐自动加到已选数量。NAS靠近工作室交换机，现行图/采购统一兼容SFP+ DAC短线，不每房另埋光纤；四Cat6A/两箱/中央五连接保持。模块/跳线只在两端模块方案下估8+8，MPTL据实核算；修正Fusion小节位置，不改变既有锚点。

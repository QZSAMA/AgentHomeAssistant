# TP-Link Omada：已选设备规格与到货验收

整理日期：2026-11-27。本文收敛为已确认订单和 v1.6 所需的规格依据，删去已取消的替代采购组合。规格来源沿用原核验日期，本次未重新查询价格或设备固件。

**已下单 7 台**：ES210XPP-M2×2、ES206XPP-M2×1、EAP775-Wall×3、EAP772×1；商品 $828，运费 $0，预计税费 $73.49，总额 **$901.49**。均待到货验收，未安装/部署。**Fusion 2.5G 普通版×1购买未确认**，完整网络计划共8台。成交金额以[订单](network-order-20261118.md)为准，待购项见[采购BOM](purchase-bom.md)。

## 1. 当前接线与设备角色

[网络拓扑 v1.6](network-topology.md)为唯一现行接线口径：武汉电信光纤 → 运营商光猫Internet桥接 → Fusion PPPoE。Fusion四个2.5G LAN分别接中央ES210、电竞房ES210、普通电脑墙口A/B；中央通过10G SFP+光纤连接客厅ES206。原Fusion→客厅铜缆只可端接备用，不与光上联同时连通。

| 位置 | 当前设备与分配 | 剩余容量 |
|---|---|---|
| 中央主路由 | Fusion普通版：WAN接光猫；LAN接中央、电竞及电脑墙口A/B | 无空闲铜口，无SFP/PoE/无线 |
| 中央交换机 | ES210：2.5G上联Fusion＋四AP＋两M200；SFP+光连客厅 | 2.5G用7/8；独立10G RJ45空闲 |
| 电竞房交换机 | ES210：2.5G上联Fusion、PC×2、Mac mini；10G RJ45接Mac Studio、SFP+留未来NAS | 2.5G用4/8；本地PoE关闭 |
| 客厅交换机 | ES206：电视、唯一Apple TV、Switch、PS、J3455；SFP+光连中央 | 5个铜口全满；本地PoE关闭 |
| 无线与网关 | 三房775×3、大厅772×1、M200×2均独立回中央PoE | AP只做无线，不接数据下联，关闭PoE Out |

J3455规划在客厅箱外通风位，西数金盘无RAID、现1G，确认升级2.5G但未购/未实施；HAOS/OpenWrt仍在该宿主部署方向。未来高速NAS在电竞房，型号和10G SFP+介质待选。已有投影仪以主卧为主要位置、移动Wi-Fi使用，不接网线；用户提供802.11 a/b/g/n/ac，按Wi-Fi 5登记。

全部设备同一家庭LAN；Fusion保持唯一DHCP和普通DNS，指定终端手动选择J3455 OpenWrt的[逻辑方案](superpowers/specs/2026-11-05-home-device-rule-routing-design.md)不变。Omada使用Fusion内置控制器，不另设控制器主机。

## 2. 已选设备规格

### 2.1 ES210XPP-M2 与 ES206XPP-M2

| 核验项 | ES210XPP-M2 | ES206XPP-M2 |
|---|---|---|
| 2.5G铜口 | 8口，均支持af/at/bt PoE++ | 5口，其中4口支持af/at/bt PoE++ |
| 10G接口 | 独立10G RJ45×1、10G SFP+×1，可分别使用 | 10G SFP+×1 |
| PoE | 单口最高90W，全机200W | 单PoE口最高90W，全机120W |
| 机身 | 无风扇，226×131.2×35mm | 无风扇，209×126×26mm |
| 本户角色 | 中央与电竞房各1台 | 客厅1台 |

来源：[ES210官方规格](https://www.omadanetworks.com/us/business-networking/omada-switch-agile/es210xpp-m2/#specifications)、[ES206官方规格](https://www.omadanetworks.com/us/business-networking/omada-switch-agile/es206xpp-m2/#specifications)，原规格核验2026-10-14/15。不要把无PP的同名系列参数套用到已购型号。

ES210标称80Gbps交换容量按全双工合计：`2×(8×2.5+10+10)=80Gbps`。同一交换机内多台2.5G终端可以并发访问10G服务器，但仍共享服务器网口、存储与CPU；跨电竞房的路径共享其2.5G上联。标称交换容量和协商速率均不是本户文件吞吐测试结果。

ES210属于Easy Managed，不等于完整L2+/三层设备。既有官方记录包含802.1Q VLAN、IGMP Snooping；部分QoS仅独立模式，PoE Recovery在控制器模式为手动。当前不新增VLAN，固件、接管、组播/IPv6和Apple Home发现能力以实机验收为准。

### 2.2 EAP775-Wall 与 EAP772

| 核验项 | EAP775-Wall×3 | EAP772×1 |
|---|---|---|
| 无线/上联 | 三频Wi-Fi 7、2.5G上联 | 三频Wi-Fi 7、2.5G上联 |
| 安装位置 | 主卧/次卧/电竞房各1台，墙面安装 | 大厅吊顶可见面 |
| 供电 | 802.3at/bt，全部中央直供 | 802.3at，中央直供 |
| 功耗依据 | at模式26W含最多6W PoE Out；bt最高45W含最多25W PoE Out | 最大约25.4W |
| 本户使用 | 不使用1×2.5G＋3×1G数据下联，关闭PoE Out | 只作无线接入 |

来源：[775官方规格](https://www.omadanetworks.com/us/business-networking/omada-wifi-wall-plate/eap775-wall/#specifications)、[772官方规格](https://www.omadanetworks.com/us/business-networking/omada-wifi-ceiling-mount/eap772/)。775机身172.9×91.2×41.3mm、工作温度0–40℃，随箱墙面安装套件/可涂装盖板。机身尺寸不等于底盒孔距或开孔尺寸；按美国实际发货版本、墙体、底盒深度、线缆弯曲和维护空间核验，仅补缺件。

当前四台AP均已下单；无线信道、功率与漫游策略由到货后的覆盖测试确定。三频美国规格不构成中国大陆6GHz的交付保证；保留[地区与终端研究](wifi7-6ghz-mainland-china-research.md)，不将其他型号的成功自述当作本户实测。

### 2.3 Fusion 2.5G 普通版

[官方规格](https://www.tp-link.com/productpages/spec/116210-3.html)与[美国商城](https://store.omadanetworks.com/products/omada-all-in-one-gateway-fusion-2-5g)的既有核验记录：普通版为5×2.5G RJ45，内置Omada Network管理应用，无Wi-Fi、PoE或SFP；官方建议管理30台设备/300客户端。当前3台交换机与4台AP在建议规模内，最终adoption、配置导出及恢复仍须验收。

官方IPS吞吐2183Mbps为实验室参数，不能当作本户PPPoE/IPv6/IPS/VPN实测。武汉电信下行1000Mbps已明确，上行30Mbps仅旧规划待核。原光猫型号、PON制式、交付口、认证、WAN VLAN和附属业务见[桥接验收](wan-bridge-plan.md)。Fusion无ONU功能，普通光电转换器不能完成PON注册；[替换光猫研究](ont-replacement-backup-research.md)仍属独立待适配资料，当前不新增采购。

Fusion的路由与控制器共享整机、供电和重启边界；导出配置并验证断电恢复。J3455承载HA/OpenWrt的角色与Omada网络管理分开。

## 3. 集中PoE与电源

中央ES210的6个PD为775×3、772×1、M200×2，规划参考 `3×26+25.4+2×12=127.4W`，加30%为 **165.62W / 200W**。M200按12W/台暂估，最终按具体版本/铭牌核验；次网关升级采购及差价仍待核，不把原绿米¥19,324合同改为已含M200×2。

这是功率预算参考，不是交换机已分配或实测功率。关闭775 PoE Out不等于自动切at模式或只预留26W，不能用45−25推断裸机实测。需核单口分配、at/bt协商、线损和六台同时冷启动；Fusion上联、空闲口及电竞/客厅全部PoE关闭。FP400尚未核实电源/接口，不加入已确认负载或端口。

| 设备 | 已核供电规格 | 大陆使用与附件 |
|---|---|---|
| Fusion 2.5G普通版 | 100–240V、50/60Hz；USB-C 5V/3A | 电压支持；插头形状按实际美国发货SKU确认 |
| ES210XPP-M2 | [官方规格](https://www.omadanetworks.com/us/business-networking/omada-switch-agile/es210xpp-m2/#specifications)：适配器输入100–240V AC、输出54V/4.16A；随箱含电源适配器和电源线 | 电压支持；保留原装电源砖，按实物交流输入接口选择合规国标线，不预设C5/C7/C13 |
| ES206XPP-M2 | [官方规格](https://www.omadanetworks.com/us/business-networking/omada-switch-agile/es206xpp-m2/#specifications)：适配器输入100–240V AC、输出53.5V/2.43A；随箱含适配器和电源线 | 电压支持；国标线型/接地按实物确认 |
| EAP775-Wall×3 | [官方规格](https://www.omadanetworks.com/us/business-networking/omada-wifi-wall-plate/eap775-wall/#specifications)：802.3at/bt PoE | 当前由交换机供电，无独立市电插头/适配器采购 |
| EAP772×1 | [官方规格](https://www.omadanetworks.com/us/business-networking/omada-wifi-ceiling-mount/eap772/#specifications)：802.3at PoE，另可12V/2.5A DC但不附DC适配器 | 当前走中央PoE，无需另买DC适配器 |

以上电源记录原核验日期为2026-10-15，按实际发货铭牌复核。美国插头形状、交流输入接口和接地以实物为准，不凭EU包装图推定；转换插头只改变形状，不改变电压。已确认100–240V输入的设备不需要额外降压变压器。

## 4. 布线、箱体与后备供电

- 当前9条在用远端铜缆：中央至四AP/两M200共6条，Fusion至电脑A/B共2条，Fusion至电竞交换机1条。中央—客厅另1条10G光纤，Fusion—中央为本地短跳线；端接备用线不占当前口数。
- 铜缆首选康普3091B / 760105122 Cat6A实芯铜，飞利浦具体型号仍待核。A/B均按2.5G验收；Cat6模块与Cat6A线混用不能标成完整Cat6A通道，实际长度、八芯端接、跳线及完整通道须测试。
- 客厅光链路先核光纤单/多模、芯数、SC端面与模块兼容，按双芯LR或单芯配对BiDi等实际条件选型；两个SFP+模块和匹配跳线尚未采购。SC/LC是接头形态，不决定千兆上限，APC与UPC不直接对接。
- Mac Studio用电竞房原生10G RJ45；未来NAS要求自带10G SFP+，近距离兼容DAC或光纤按NAS实物确定，不另买NAS网卡，不把该预留口算空闲扩展口。
- 中央核心位、电竞房/客厅两处设备箱须计入电源砖、插座、Cat6A弯曲和手部维护空间；AP装箱外/顶面，无风扇仍需通风。Mac/未来NAS在电竞房箱外，J3455在客厅箱外。
- UPS入住后按实测负载选型，至少1小时为评估目标。中央计核心设备和六路PoE；电竞计交换机、Mac及未来NAS；客厅计交换机、J3455及HA/OpenWrt恢复。200W为PoE输出预算，不是恒定墙端功率；下联电脑不会因数据链路或AP供电自动保活。

详细端接/线量、柜体和施工验收以[布线要求](renovation-wiring-requirements.md)、[点位计划](network-placement-and-cabling-plan.md)为准。

## 5. 到货与现场验收

1. 清点7台订单设备的型号、数量、地区/硬件版本、原装电源及3套墙装/1套吊顶附件。Fusion购买后核固件兼容、全套接管、配置备份与恢复。
2. 核Fusion四个LAN同属家庭LAN，逐口验证当前分配：中央7/8、电竞4/8、客厅5/5；AP无数据下联，房间交换机PoE关闭。
3. 记录每条铜缆及光纤的标签、长度、端接/模块、协商速率与错误计数；测试2.5G回程/电脑墙口、中央—客厅10G、电竞本地10G和跨房并发，区分协商速率与文件吞吐。
4. 六个中央PD同时冷启动，检查PSE预留和实际输出、重启及持续负载。柜门关闭、夏季负载工况核温度；无需因已购PoE交换机在客厅而开启无负载端口。
5. 进行24–72小时并发下载、局域网拷贝、游戏/影音及家庭控制测试；主卧投影移动到实际使用点后验证播放，记录无线协议与信号，不把Wi-Fi 7 AP能力赋予旧终端。
6. 断电和光猫/Fusion/交换机/AP/J3455分别重启后，验证普通上网、Apple Home发现与控制、HA/OpenWrt恢复及手动回退。UPS按实测续航后才能记录通过。

全部现场项目尚未执行。品牌统一不能保证零故障、零丢包或所有功能满速；最终结果受固件、终端、线材、散热、供电和运营商共同影响。

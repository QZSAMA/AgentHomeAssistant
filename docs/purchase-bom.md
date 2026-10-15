# 家庭基础设施采购 BOM 与未决清单

> 核验日期：**2026-10-15**。货币：**美元 USD**。美国 Amazon 新机购买栏价，不含销售税、运费、转运/进口和施工费用；不是中国到岸价。
> 本文集中维护采购状态、精确商品入口与报价；需求与已有设备事实源为[家庭基础设施台账](home-infrastructure-register.md)，连接关系见[网络拓扑](network-topology.md)和[智能家居拓扑](smart-home-topology.md)，施工门槛见[施工需求](renovation-wiring-requirements.md)。
> **“已确认”指用户已选定型号/需求，不代表已购、已安装或批准立即下单。** Fusion、AP 保留暂选状态；中央交换机型号等未决项不混入已确认数量。海外 SKU 的当地认证、售后、固件与底盒适配仍须下单前核验；**6GHz 不计入中国大陆可合法使用或本户保证能力**。

> **Apple设备当前决定（同日补充）**：用户已确认大厅 **Apple HomeView非壁挂／桌面版 ×1**，通过大厅AP Wi-Fi接入，官方参考$299、11月13日起供货；型号/安装版本已确认，未购/未部署，大陆服务仍待验。壁挂控制屏改用**平板电脑或iPad**，具体型号、数量、点位与供电方式待选，不采购HomeView壁挂版或其底座。mini 2大陆官网¥1,099、美版$149，10月30日供货；三房各1仍是建议，代际/数量/地区未获最终确认。详见[官方核验与采购建议](apple-home-devices-2026.md)。
> **语言偏好已确认**：用户接受英语Siri AI，中文支持不再作为采购门槛；大陆服务/账户和配套设备可用性仍待验。HomeView桌面版已按最新决定纳入确定型号小计；mini 2与壁挂平板不并入。

## 1. 已确认具体型号：采购主表

| 角色 | 型号 | 暂估数量 | 官方关键规格与用途 | 美国 Amazon | 价格 |
|---|---|---:|---|---|---:|
| 工作室/电竞房唯一交换机 | **Omada ES210XPP-M2** | **1 台** | [官方规格](https://www.omadanetworks.com/us/business-networking/omada-switch-agile/es210xpp-m2/#specifications)：8×2.5G PoE++，单口最高90W、总200W；1×10G RJ45给Mac Studio，1×10G SFP+给附近NAS；80Gbps交换容量，无风扇。完整直连十口占满，Apple TV/投影可改接AP释放两口 | [B0HB17QTKX](https://www.amazon.com/dp/B0HB17QTKX) | **$229.99/台** |
| 大厅交换机 | **Omada ES206XPP-M2** | **1 台** | [官方规格](https://www.omadanetworks.com/us/business-networking/omada-switch-agile/es206xpp-m2/#specifications)：5×2.5G中4口PoE++，单PoE口最高90W、总120W；另1×10G SFP+，无风扇。接中央上联、EAP772、电视及HALL-IOT-GW，预留1个2.5G口 | [B0GKQ5SD2L](https://www.amazon.com/dp/B0GKQ5SD2L) | **$173.91/台** |
| 大厅Apple家庭中枢/屏幕 | **Apple HomeView桌面版（非壁挂）** | **1 台，已确认；未购** | [官方规格](https://www.apple.com/apple-homeview/specs/)：A18、7英寸屏、Wi-Fi 6E、Thread、HomeKit/Matter、四麦克风。通过大厅AP Wi-Fi接入；随箱1.5m USB-C线及30W适配器（100–240V），不另买壁挂/PoE底座。11月13日起供货；英语Siri AI已接受，大陆服务/账户/配套设备仍待验 | 未核精确Amazon；[Apple官方配置页](https://www.apple.com/shop/buy-home/apple-homeview) | **Apple官方$299/台**，未含税运 |

**本表小计：3台、$702.90**（两台交换机Amazon $403.90 + HomeView Apple官方$299，混合渠道参考），不是全屋系统总价。大厅交换机同日[美国官方商城](https://store.omadanetworks.com/products/omada-5-port-2-5g-base-t-and-1-port-10ge-sfp-easy-managed-switch-with-4-port-poe-es206xpp-m2)为$169.99，较Amazon便宜$3.92，配送/保修另核。

## 2. 当前暂定型号：单列，不升级为最终确认

| 角色 | 型号 | 暂估数量 | 官方关键规格与用途 | 美国 Amazon | 价格 |
|---|---|---:|---|---|---:|
| AC：主路由 + 内置Omada控制器 | **Fusion 2.5G 普通版（非PoE版）** | **1 台，用户暂定** | [官方规格](https://www.tp-link.com/productpages/spec/116210-3.html)：1×2.5G WAN + 4×2.5G WAN/LAN；无Wi-Fi、无PoE、无SFP。内置控制器建议管理30台设备/300客户端；接光猫和中央交换机，不代替光猫/PoE交换机 | [B0H4P7XX8G](https://www.amazon.com/dp/B0H4P7XX8G) | **$169.99/台** |
| 三房Wi-Fi 7面板AP | **EAP775-Wall** | **3 台，第一优先暂选** | [官方规格](https://www.omadanetworks.com/us/business-networking/omada-wifi-wall-plate/eap775-wall/#specifications)：BE11000三频；1×2.5G上联，另1×2.5G + 3×1G下联；802.3at/bt，最大45W含25W PoE Out；本方案不转供PoE。主卧、次卧、工作室各1台，装箱外墙面 | [B0G88FG4QH](https://www.amazon.com/dp/B0G88FG4QH) | **$179.99/台；3台$539.97** |
| 大厅Wi-Fi 7吊顶AP | **EAP772** | **1 台，第一优先候选** | [官方规格](https://www.omadanetworks.com/us/business-networking/omada-wifi-ceiling-mount/eap772/#specifications)：BE11000三频，1×2.5G，802.3at，最大25.4W；由大厅交换机供电，装在吊顶可见面，不藏顶内；不另买DC适配器 | [B0D2M26NYW](https://www.amazon.com/dp/B0D2M26NYW) | **$169.99/台** |

本表参考小计 **$879.95**。仅Omada网络设备为 **7台、Amazon参考$1,283.85**；加上已确认HomeView桌面版后，第1、2表合计 **8台、$1,582.85**（Omada Amazon + Apple官网混合渠道）。以上均**不含中央交换机、Mac、NAS、HomePod、壁挂平板、UPS、线材、箱体和施工**，不能称为完整可开机预算。

## 3. 已确认需求：仍需补齐可下单SKU/辅材长度

以下需求已确认，但尚无完整具体商品或精确价格；不编造Amazon链接，不把“待报价”当作零元。

| 角色 | 型号 | 暂估数量 | 官方关键规格与用途 | 美国 Amazon | 价格 |
|---|---|---:|---|---|---|
| 主计算设备 | **Mac Studio M5 Ultra / 512GB统一内存 / 4TB SSD / 原生10GbE** | **1 台，采购目标已确认** | [Apple技术规格](https://www.apple.com/mac-studio/specs/)列512GB对应M5 Ultra 36核CPU/80核GPU，10GbE RJ45支持1/2.5/5/10G；模型、剪辑与开发。**HA主实例在J3455，不在Mac上** | 未核到目标配置的精确商品；优先[Apple配置页](https://www.apple.com/shop/buy-mac/mac-studio) | **目标配置待报价**；官网写512GB选项10月下旬提供，$5,499是M5 Ultra起价，不是本配置价格 |
| 中央星型铜主干 | Cat6A实芯纯铜，具体品牌/长度待施工复尺 | **4条链路，米数待定** | 主卧/次卧各直达面板AP并供PoE；工作室/大厅各到交换机，当前均2.5G；合格Cat6A原生10GBASE-T完整通道可达100m，不等于任意端接均能达标；禁CCA | 待选，不用虚构商品链接 | 待复尺报价 |
| 房内数据支线与跳线 | Cat6A，具体SKU/长度待定 | **按实际端口和端接计** | 已明确工作室AP、大厅吊顶AP、HALL-IOT-GW各1条本地支线；另计Mac的10G铜链路、PC/Mini/J3455/电视/影音及卧室AP下联分支；NAS不算铜网线 | 待选 | 待报价 |
| Cat6A端接/配线与墙口 | 匹配实芯线及PoE的模块、配线架/支架、面板、现场端接插头 | 按最终端接表计 | **只有四主干两端都模块端接时，才是8模块+8跳线**；直达AP可采用合规MPTL现场插头，模块/跳线数量随方案变化。全部链路认证，屏蔽系统正确接地 | 待施工端接方案，非默认8套采购 | 待报价 |
| 工作室近距离NAS互联 | **兼容10G SFP+被动DAC短线**，具体型号/长度待NAS选型 | **NAS实施时1条** | 用户已确认NAS放交换机附近；核两端接口、兼容编码、长度/弯曲半径。DAC两端带接头，**不再额外买两只光模块/光纤**；NAS无SFP+时先选兼容网卡 | 待NAS接口确定后选精确商品 | 待报价 |
| 房间设备箱 | 可维护、通风，尺寸待实物复尺 | **2个：工作室、大厅** | 放交换机、原装电源砖和配线；卧室无箱。Mac/NAS/J3455在箱外通风设备位，不塞小箱；不把通风柜当隔音柜 | 待尺寸确认；可本地采购 | 待报价 |
| 中央核心网络位置 | 弱电箱附近通风机柜/设备位，规格与复用待定 | **1处** | 光猫、Fusion、中央交换机、电源、配线及后备电源；预留弯曲/检修/散热/承重，暂不锁U数 | 待复尺；可本地采购 | 待报价 |
| AP安装缺件 | 面板底盒/现场固定件；不重复买随箱安装套件 | **3个面板位+1个吊顶位** | EAP775-Wall机身172.9×91.2×41.3mm不等于底盒开孔；核中美底盒孔距、深度、维护；大厅核支架/承重 | 只按现场缺件补购 | 待报价 |
| 本地电源/配电附件 | 合规国标线/插座/必要转接、理线标签、空管牵引线 | 按实机与点位计 | 网络设备适配器电压见第7节；HALL-IOT-GW旁预留普通插座×1。弱电管可抽换，不按每房额外光纤采购；不买降压器替代插头核验 | 不预设电源线接口；建议合规本地采购 | 待报价 |
| 施工与验收服务 | 铜缆认证、配线标识、安装/调试、断电恢复测试 | 1套工程，非设备 | 四主干及支线保存线序/长度/性能报告，分别测试Mac/NAS本地10G、跨房共享2.5G、PoE及UPS目标；不是买测试仪的指令 | 不适用 | 按工程报价 |

**光纤范围**：保留运营商入户光纤与光猫；当前**不需每房额外预埋光纤**，也不把DAC埋入墙内。优先保留可维护空管、牵引线和转弯空间。以后布局/距离/速率需求变更再评估OS2光纤，不因此增加当前BOM。

## 4. 尚未确定：请用户决定后再并入正式采购

| 角色 | 型号 | 暂估数量 | 官方关键规格与用途 | 美国 Amazon | 价格 |
|---|---|---:|---|---|---|
| **中央PoE交换机（该角色必需，型号未确认）** | **推荐ES210XPP-M2**；不是已确认第2台 | 推荐1台 | 8×2.5G PoE++、90W/口、200W总；网关+四区域主干共5个2.5G连接。两卧室AP保守规划117W/200W。确认后全屋此型号才变成2台 | [候选B0HB17QTKX](https://www.amazon.com/dp/B0HB17QTKX) | **候选$229.99**，不计第1、2表 |
| 高速NAS整机、SSD/HDD与备份 | 型号、盘位、容量、阵列、存储介质均待选 | 1套规划，未锁采购 | 为Mac剪辑、PC/Mini游戏库；**位置已确定靠近工作室交换机**，不等于整机已购。原生或另配10G SFP+；按素材码率/随机读写和备份验收，不以10G接口保证磁盘满速 | 待选 | 待预算/容量 |
| NAS 10G SFP+网卡 | 型号/是否另购取决NAS | 0或1张 | 与NAS PCIe/系统驱动及DAC兼容；原生支持时不重复买，RJ45网卡不当SFP+替代 | 待选 | 待报价 |
| **UPS/后备供电（已要求，不能忽略）** | 合规220V型号、容量/电池待实测 | 覆盖中央/工作室/大厅3个供电位置；台数待方案 | **网络、Mac、NAS至少1小时目标**；含J3455/HA和必要排风。中央UPS不经网线给房间交换机/Mac供电。若要停电仍有Siri/Thread控制，HomePod/网关也须另保活；按W、峰值、续航曲线与降载/关机策略选，不能套美国120V UPS | 不先推荐美国120V SKU | 待负载核算 |
| J3455升级2.5G网卡 | 接口/型号待主板核验 | 1张升级目标 | PCIe/USB等不预设，核Proxmox驱动、散热、稳定性和bridge迁移；复用原交换机端口 | 待选 | 待报价 |
| PC升级2.5G网卡 | 接口/型号待PC配置核验 | 最多2张，可分期 | 用户有升级意向，升级前两PC仍为1G；不因全屋2.5G自动升级 | 待选 | 待报价 |
| 三房Siri/Thread终端 | **优先推荐HomePod mini 2**；代际/地区/颜色待用户确认 | 暂按3台，各房1台，不增数量 | [官方规格](https://www.apple.com/homepod-mini/specs/)：Wi-Fi 6E/802.11ax、Thread、蓝牙6、温湿度、Apple Home中枢；随箱20W适配器100–240V、9V/2.22A。10月30日起供货；大陆有普通中文Siri，美国Siri AI待后续更新，不视为大陆AI承诺 | 未核精确Amazon；[美国Apple](https://www.apple.com/shop/buy-homepod/homepod-mini) / [大陆Apple](https://www.apple.com.cn/homepod-mini/) | **美$149/台，3台$447；大陆¥1,099/台，3台¥3,297**；待确认计价 |
| 壁挂控制屏 | **平板电脑或iPad**；品牌/型号/尺寸待选，不采用HomeView壁挂版 | 数量、点位待定 | 作为显示/交互终端；iPad可规划家庭App或HA面板，其他平板按平台核HA客户端/网页及kiosk支持，不保证原生Apple家庭App。支架、长期充电、散热与可拆维护、网络方式待定；不替代HA主机或Thread边界路由器，不先计PoE负载 | 待选，不编商品链接 | 待报价，不计确定小计 |
| Zigbee接入路径 | Aqara有线网关（如M3候选）**或**HA以太网协调器 | 同一批设备先按1条路径，不双买 | 接HALL-IOT-GW墙口，Zigbee设备不能同时配对两个网络；最终型号决定PoE/本地集成/Apple Home暴露能力。不自动另加Thread USB棒 | 待选择路径和区域SKU | 待报价 |
| HA主机存储/备份 | HAOS VM使用的SSD/备份介质 | 先核已有资源，再决定增购 | J3455已有16GB/10TB，**10TB不是已确认的可用SSD**；建议初始VM 2vCPU/4GB/64GB SSD按资源复核。无需新买Pi/独立HA主机 | 待资源核验 | 待报价 |
| Aqara照明/开关/传感器/窗帘及Thread节点 | 具体区域SKU/协议待定 | 按照明/家具/门窗图统计 | 四区域+两卫生间均预留；分清Zigbee、Matter over Thread、Wi-Fi，不按每房买一套网关，不重复买同功能候选；零火线与潮湿环境条件先确认 | 待图纸/选型 | 待数量 |
| 摄像头/门铃/录像 | 型号/点位/录像存储待定 | 待定 | PoE走中央/大厅有余量端口，追加PoE预算与支线；不使用AP PoE Out，不默认卧室/卫生间安装；本地录像、HA与HKSV分别验收 | 待定 | 待报价 |
| 空调 | ORVIBO仅空调，型号/控制路径待定 | 待定 | 是否本地接入HA及桥接Apple Home需验证；不新增ORVIBO面板/照明系统 | 待定 | 待报价 |
| 本地模型自由对话收音终端 | 型号/方案未选 | 待各房间语音设计 | Siri控制与本地模型对话是两条链路；不把HomePod麦克风直接当作通用AI输入，若需独立HA Assist等硬件再确认 | 待定 | 待报价 |
| 电视/Apple TV/投影仪 | 型号及是否新增待核 | 仅有接入规划，不擅自增加采购 | 电视接大厅交换机；Apple TV/投影保持有线，可直连工作室ES210或接AP两个1G数据口；型号决定接口速率 | 待确认是否采购 | 不计新增设备费用 |
| 运营商光猫 | 电信/联通提供型号与桥接权限待定 | 1台接入角色 | PON接入/认证必须保留，优先桥接；LAN速率/IPv6/公网IP与套餐核验。Fusion无ONU功能，不能直接替代 | 通常随宽带业务，不盲买ONU棒 | 运营商业务费用待核 |

Apple子系统中，**HomeView桌面版×1、$299已计入第1表**；三台mini 2建议另加$447，若以后确认则两者美国官方参考共**$746**，不能再将整笔$746重复加总。大陆mini报价¥3,297单列，不与美元直接相加。用户接受英语Siri AI，大陆服务/账户/配套设备仍待验。壁挂控制屏另选平板或iPad，不采购HomeView壁挂版、支架或USB-C/AC/PoE底座；平板未定项不计价格、网口或PoE负载。详情见[Apple核验](apple-home-devices-2026.md)。

如后续确认中央再加一台ES210（候选$229.99），Omada网络Amazon参考小计为 **$1,513.84**；连同已确认HomeView桌面版的混合渠道参考为 **$1,812.84**。这仍不含Mac/NAS/UPS/其他智能设备/壁挂平板/辅材，不是完整系统总价。

## 5. 复用与明确不重复购买

- **已有复用**：J3455（16GB/10TB/1G/Proxmox，黑群晖VM及代理服务保留）、M1 Mac mini 16GB（全天开机跑Hermes，1G）和两台PC；不据此购买新整机。
- **HA**：J3455上独立HAOS VM，位置已定、尚未部署；Mac mini给Hermes直接操作macOS，HA不与其共宿主。
- **网络管理**：Fusion内置控制器；**不买OC200、树莓派/独立控制器主机，不部署J3455 Omada Linux VM**，ER707-M2已退出当前方案。
- **不买**：第二台工作室交换机、两卧室交换机/设备箱/网络箱UPS、独立AP注入器、SM5310-T铜模块、NAS光模块对及额外每房预埋光纤。未来因摄像头而新增中央ES206等只留扩展研究，不默认采购。
- **AP附件**：原装电源砖、已含安装套件不再单独计购；当前AP全部PoE供电，无另购AP市电适配器。电池传感器/普通灯具并不自动占PoE口。
- **HomeView**：桌面版随箱电源/线材不重复购买；不买HomeView壁挂版或配套壁挂/PoE底座。平板/iPad及其安装/供电附件待选后另计，不因墙面安装意向自动增线或增PoE预算。
- 不采用小米/米家、华为设备；Aqara为主，ORVIBO仅空调。

## 6. 报价证据、卖家和版本边界

核价方法：读取美国官方规格与商城商品信息、Amazon精确商品的型号/购买栏；不以搜索摘要计价，未加购物车或结账。Amazon当次默认美国Brooklyn 11204地址，不能据其“In Stock”推定可直邮中国或当地保修。

| 型号/渠道 | 查询日期 | 当次新机价格 | 当次销售/发货 | 核验说明 |
|---|---|---:|---|---|
| Fusion / Amazon | 2026-10-15 | $169.99 | Blazing Network US / Amazon；有货 | B0H4P7XX8G，普通版非PoE |
| ES210 / Amazon | 2026-10-15 | $229.99 | Blazing Network US / Amazon；有货 | **B0HB17QTKX**，产品信息Mfr Part Number明确ES210XPP-M2；不误用ES210X-M2 |
| ES206 / Amazon | 2026-10-15 | $173.91 | Amazon.com / Amazon.com；有货 | B0GKQ5SD2L |
| EAP775-Wall / Amazon | 2026-10-15 | $179.99 | Blazing Network US / Amazon；有货 | B0G88FG4QH，发货硬件版待卖家确认 |
| EAP772 / Amazon | 2026-10-15 | $169.99 | Amazon.com / Amazon.com；有货 | B0D2M26NYW，硬件版/AFC差异另核 |
| [Fusion官方商城](https://store.omadanetworks.com/products/omada-all-in-one-gateway-fusion-2-5g) | 2026-10-15 | $169.99 | 美国官方商城 | 不用划线价作为当前单价 |
| [ES210官方商城](https://store.omadanetworks.com/products/omada-8-port-2-5g-2-port-10g-easy-managed-switch-with-8-port-poe-es210xpp-m2) | 2026-10-15 | $229.99 | 美国官方商城 | 中央候选与电竞房已选分开计数 |
| [ES206官方商城](https://store.omadanetworks.com/products/omada-5-port-2-5g-base-t-and-1-port-10ge-sfp-easy-managed-switch-with-4-port-poe-es206xpp-m2) | 2026-10-15 | $169.99 | 美国官方商城 | 与Amazon不是同一报价 |
| [EAP775官方商城](https://store.omadanetworks.com/products/omada-be11000-tri-band-wall-plate-wi-fi-7-access-point-eap775-wall) | 2026-10-15 | $189.99 | 美国官方商城 | 不同于Amazon $179.99 |
| [EAP772官方商城](https://store.omadanetworks.com/products/omada-be11000-ceiling-mount-tri-band-wi-fi-7-access-point-with-1x2-5g-port) | 2026-10-15 | $169.99 | 美国官方商城 | 单AP不是全屋设备价格 |

2026-10-14 AP历史报价与双频备用研究保留在[原对比报告](ap-6ghz-selection-price-comparison.md)，不把旧日期改成新查询。以上价格是快照而非购买保证；税运/汇率/返修/进口合规和最终硬件版本仍须确认。

## 7. 供电与PoE采购核对

- Fusion随箱USB-C电源输出5V/3A，输入100–240V、50/60Hz；ES210适配器100–240V、54V/4.16A；ES206适配器100–240V、53.5V/2.43A。**三者电压适用大陆220V**，无需降压器。
- 美国发货SKU的Type A/B插头/电源线接口未逐台锁定；插头形状不等于电压。保留交换机原装电源砖，按实物补合规国标交流线并保留接地，不先猜C5/C7/C13；转接头不变压。
- EAP775×3与EAP772×1均由各自交换机PoE供电，独立注入器数量0，PoE Out关闭。
- 按AP官方上限×1.3保守规划：中央两775 **117W/200W（若采用推荐ES210）**，工作室一775 **58.5W/200W**，大厅772 **约33W/120W**；单口标准/预算足够。775的45W包含25W下游输出，不视为裸机实测，也不以45−25推定20W。
- 摄像头/网关尚未确定功耗，不在余量内默认放入若干台；新增后重算端口与功率。UPS按整机实际交流输入测量，不能把PoE在交换机输入和AP两处重复加总。详见[网络拓扑PoE复核](network-topology.md#22-交换机-poe-与端口复核2026-10-15)。

## 8. 本轮一致性检查结果

本轮同步需求、选型、两张拓扑和施工要求，保留历史草案的历史标签，不将其作为当前采购：

1. 当前中央为**五个物理连接**，Fusion控制器不独占网口；HA固定J3455独立HAOS VM，非Mac主实例。
2. 工作室**一台ES210**不扩机；完整直连占满十口，但Apple TV/投影经AP数据口可释放两个2.5G口，不再绝对写“零扩展位”。
3. NAS靠近交换机，当前**10G SFP+ DAC短线**；不再在现行图和采购中并列光纤二选一。四Cat6A主干、两房间箱、三面板一吊顶保持一致。
4. 补上ES210的精确Amazon型号/ASIN；统一当日报价入口，AP旧报价保留日期；Mac与HomePod新品信息不自动升级采购状态。
5. Cat6A端接数量按施工方案而非无条件8模块/8跳线；修正旧辅材表列数，Fusion电源附件与AP随箱附件不重复购。
6. HomeView已确认桌面版×1；中央型号、UPS、NAS、mini代际、壁挂平板与其他智能终端仍待选。**这是一份完整的采购范围登记，不是假装已得到整套可一键下单的确定SKU。**

此前验证记录（2026-10-15，Apple安装选择更新前）：10份相关文档的本地文件链接、36处锚点引用均有效；98张Markdown表格列数一致；网络/智能家居共4段Mermaid图源通过Mermaid 11解析；报价算术及`git diff --check`通过。仅更新文档，未采购、配置设备或提交/推送Git。


同日最新决定：用户确认HomeView非壁挂／桌面版×1，接受英语Siri AI；移入确定型号表，增加Apple官方$299，Omada网络小计不变。壁挂另选平板/iPad，型号/数量/点位/供电待定；mini 2代际/数量/地区继续待确认。拓扑与施工同步桌面版，不改变四主干或AP PoE预算；此前“未来产品/Thread未知”仅历史记录保留。

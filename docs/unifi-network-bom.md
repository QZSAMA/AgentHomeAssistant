# UniFi 基础网络设备 BOM 与适配分析

核验日期：**2026-10-30**。状态：**已评估、不采用，仅保留研究记录**。用户于同日明确决定不使用 UniFi，原因为**成本过高**。继续采用现行 [Omada 3A 三频 BOM](purchase-bom.md)、[拓扑](network-topology.md)和采购 Excel；下列 UniFi 型号、数量与布局不进入采购或施工清单。

## 结论与适配边界

UniFi 能实现四条 Cat6A 星型主干、全屋 2.5G 接入、工作室 Mac/NAS 独立 10G、三台含 6GHz 的 Wi-Fi 7 AP，并由网关内置的 UniFi Network 统一管理。但**不能直接按现有 Omada 面板 AP 一对一替换**：

- **U7 Pro Wall**：三频 Wi-Fi 7、一个 2.5G 上联网口，没有给电脑使用的下联网口。
- **U7 Pro XG Wall**：同样只有一个网口，升级为 10G 上联也不增加下联。
- **U7 In-Wall**：一个上联、两个 2.5G 下联，但只有 2.4/5GHz，不能满足当前三频要求。
- **U6 Enterprise In-Wall** 虽有 6GHz 和四口交换功能，但属于 Wi-Fi 6E，不满足 Wi-Fi 7 要求。

下表为了保留主卧的有线扩展，**额外加入一台主卧小交换机**。它通过原来的一条 Cat6A 同时接收数据和 PoE++，再供电给壁挂 AP，不增加中央到主卧的埋线，也不需要独立 PoE 注入器；但增加主卧设备，与此前“卧室只放 Wall AP、不放交换机”的偏好不符。这一布局随 UniFi 方案一并不采用，仅作比较记录。若这条偏好不可变，当前核验到的 UniFi 产品没有满足全部条件的直接替代组合。

## 价格与 BOM

价格来自 **Ubiquiti 美国官方商城**。页面同时显示基础标价与部分产品的 `Surcharge incl.`；下表预算单价采用后者，未显示附加费的配件采用页面单价。附加费不是销售税，合计仍**不含销售税、运费、进口、辅材、布线或施工**。此次使用可核对型号的官网商品页，没有将未核实的 Amazon ASIN 放入表内。

| 角色 | 型号及官方购买页 | 数量 | 关键规格及用途 | 基础单价 USD | 预算单价 USD | 预算小计 USD |
|---|---|---:|---|---:|---:|---:|
| 主路由与控制器 | [Cloud Gateway Max / UCG-Max-NS](https://store.ui.com/us/en/products/ucg-max-ns) | 1 | 无存储版本；5×2.5G；内置 UniFi Network；标称 IDS/IPS 2.3Gbps；随箱电源 | 199 | 219 | 219 |
| 中央与大厅 PoE 交换机 | [Flex 2.5G PoE / USW-Flex-2.5G-8-PoE](https://store.ui.com/us/en/category/switching-utility/products/usw-flex-2-5g-8-poe) | 2 | 每处一台；8×2.5G PoE++，另有一个 10G 电/光二选一接口；使用下列电源时每台 PoE 总预算 196W | 199 | 219 | 438 |
| 主卧新增交换机 | [Flex 2.5G PoE / USW-Flex-2.5G-8-PoE](https://store.ui.com/us/en/category/switching-utility/products/usw-flex-2-5g-8-poe) | 1 | 从中央获得 PoE++，下游可用 46W；接主卧 AP 和电脑等有线终端；须增加开放、通风设备位置 | 199 | 219 | 219 |
| 中央、大厅交换机电源 | [AC Adapter 210W / UACC-Adapter-AC-210W](https://store.ui.com/us/en/products/uacc-adapter-ac-210w) | 2 | Flex 电源另售，不能漏算；100–240V AC，输出 54V DC，C14 电源入口；主卧通过网线取电，不再买第三只 | 79 | 79 | 158 |
| 电竞房交换机 | [Pro XG 8 PoE / USW-Pro-XG-8-PoE](https://store.ui.com/us/en/category/switching-utility/products/usw-pro-xg-8-poe) | 1 | 8×10G RJ45 PoE++，支持 2.5G/1G；2×独立 10G SFP+；155W PoE；含 210W 电源；Mac 使用原生 10G 电口 | 499 | 549 | 549 |
| 电竞房中央上联转接模块 | [UACC-CM-RJ45-MG](https://store.ui.com/us/en/products/uacc-cm-rj45-mg) | 1 | 将第二个 SFP+ 转为铜缆上联，Cat6A 侧协商 2.5G，主机侧工作于 10G；另一个 SFP+ 留给 NAS | 65 | 65 | 65 |
| 主卧、电竞房壁挂 AP | [U7 Pro Wall / U7-Pro-Wall](https://store.ui.com/us/en/products/u7-pro-wall) | 2 | 2.4/5/6GHz 三频 Wi-Fi 7；单个 2.5G 网口；PoE+；每台最大 22W；无下联口 | 199 | 219 | 438 |
| 大厅吊顶 AP | [U7 Pro / U7-Pro](https://store.ui.com/us/en/products/u7-pro) | 1 | 2.4/5/6GHz 三频 Wi-Fi 7；2.5G 网口；PoE+；最大 21W；含标准安装件 | 189 | 208 | 208 |
| **合计** | **1 网关、4 交换机、3 AP，另加 2 电源和 1 模块** | | | **基础标价合计 2,105** | | **2,294** |

UCG-Max-NS 核验时显示 **Sold out Oct 30 / Expected Restock Nov 6**。预计补货不是交付承诺，其余页面价格也不是锁价或库存保证。不需要为基础网络另买 CloudKey、SSD 或在 J3455 上再部署 UniFi 控制器。可选 CyberSecure、延保及电话支持不计入基础预算。

## 连接与端口数量核对

建议比较结构如下；房间相对位置、入户门左侧核心位和公共区吊顶主干路线沿用[原施工草案](network-placement-and-cabling-plan.md)，新增主卧交换机位置需要另行落实。

```text
光纤 → 光猫 → UCG-Max → 中央 Flex 2.5G PoE（本地 210W 电源）
                         ├─ 主卧 Cat6A / 2.5G + PoE++
                         │    └─ 主卧 Flex（PoE 取电）→ U7 Pro Wall + 有线终端
                         ├─ 次卧 Cat6A → 预留 RJ45，暂不购 AP
                         ├─ 大厅 Cat6A / 2.5G
                         │    └─ 大厅 Flex（本地 210W 电源）→ U7 Pro + 电视 + M200 吊顶网关
                         └─ 电竞房 Cat6A / 2.5G
                              └─ 铜模块 → Pro XG 8 PoE 的第二个 SFP+
                                   ├─ 原生 10G RJ45 → Mac Studio
                                   ├─ 第一个 SFP+ → 未来 NAS
                                   ├─ PoE+ → 电竞房 U7 Pro Wall
                                   └─ PC×2 / Mac mini / J3455 / Apple TV / 投影
```

| 电竞房接口 | 设备 | 目标/实际速率 |
|---|---|---|
| RJ45 1 | Mac Studio | 10G |
| RJ45 2、3 | PC 1、PC 2 | 当前 1G，升级后 2.5G |
| RJ45 4 | Mac mini | 1G |
| RJ45 5 | J3455 | 当前 1G，升级后 2.5G |
| RJ45 6 | 已有 Apple TV | 以实机以太网速率为准 |
| RJ45 7 | 已有米家投影 | 以实机以太网速率为准 |
| RJ45 8 | 电竞房 U7 Pro Wall | 2.5G + PoE+ |
| SFP+ 1 | 未来自带 SFP+ 的 NAS | 10G；NAS 与介质后置采购 |
| SFP+ 2 | UACC-CM-RJ45-MG → 中央主干 | 主机侧 10G，铜侧 2.5G |

全部设备直连时共有 **9 个铜缆连接、1 个 NAS SFP+ 连接**。Pro XG 8 只有 8 个原生铜口，所以模块确实需要；U7 Pro Wall 没有下联口，不能再套用 Omada 方案的“把 Apple TV/投影移到 AP 下联”来释放端口。未来如增加设备，还需重新分配接口。

Mac 与 NAS 在同交换机、同 VLAN 时，本地交换不经过中央 2.5G 上联；跨房间和跨 VLAN 经网关的流量另受上联/路由能力限制。局部链路为 10G 并不保证磁盘、协议或应用持续跑满 10G。

Flex 的 10G RJ45 和 SFP+ 是 **combo 二选一**，不能分别接 Mac 和 NAS。因此不将它用作电竞房双 10G 设备的替代交换机。Pro XG 8 的两个 SFP+ 则可独立使用。

## PoE 与安装核对

| 位置 | 本方案供电方式 | 官方可用下游 PoE 总预算 | 已知负载与判断 |
|---|---|---:|---|
| 中央 Flex | 另购 210W AC 电源 | 196W | 给主卧 Flex 提供 PoE++；单口最高 64W，足够该条已知分支；其他房间交换机使用本地电源，数据口不必开 PoE |
| 主卧 Flex | 中央 PoE++ → 10G RJ45 PoE 输入端 | 46W | 主卧 AP 最大 22W，账面余量 24W；给电脑的数据口不需要 PoE |
| 大厅 Flex | 另购 210W AC 电源 | 196W | U7 Pro 最大 21W；按仓库已归档的绿米签字方案另计 M200 约 12W，合计约 33W，仍有余量；到货核实功耗与协商 |
| 电竞房 Pro XG 8 | 随箱 210W AC 电源 | 155W | 壁挂 AP 最大 22W，余量充足；单口支持 60W PoE++ |

主卧必须协商到 **PoE++ 输入**：Flex 若只收到 PoE+，下游预算仅 16W，不足以覆盖 22W AP 的标称最大功耗。按标准 PoE 协商，不使用被动强制供电；到货验证冷启动、线缆认证和控制器功率分配。这里是规格预算核对，不是已完成现场供电测试。

提交时已同步远程的 [2026-10-26 绿米最终签字方案](aqara-final-quote-20261026.md)：大厅网关已选 M200，吊顶 PoE 支线建议 2 根 Cat6A（1 用 1 备），原 HALL-IOT-GW 墙口转备用；本记录据此修正网关接入说明。M200 属于独立绿米采购，不加入本表 UniFi 美元设备总价。

Flex 尺寸约 212.9×99.4×33.5mm；Pro XG 8 约 210.4×173.8×43.7mm，另计电源、插头弯曲和散热空间。主卧新增交换机可考虑通风桌侧位置，但不能声称原有 AP 底盒可以容纳它。U7 Pro Wall 自带标准墙装件；可刷漆盖、齐平嵌入件等另售，不在预算中，原 EAP 面板预留须重新核安装孔与墙盒兼容。

UCG-Max 与另购 AC Adapter 210W 已核官方 100–240V AC。后者是 C14 入口，可选合规中国插头至 IEC C13 的电源线；美国发货插头、Pro XG 随箱适配器铭牌及整套随箱线材仍应下单/到货核对，不能把页面 DC 电压当中国市电直连规格。

## 两种预算变化与选择建议

| 方案 | 含官网已显示附加费、不含税运的设备预算 | 差异 |
|---|---:|---|
| 本文：保留主卧有线扩展 | **$2,294** | 主卧增一台 PoE 供电的小交换机；完整保留三频、三 AP、房间单主干及工作室 10G |
| 主卧只用 Wi-Fi，取消其有线扩展 | **$2,075** | 减主卧 Flex $219，主卧 AP 改中央直供；不符合原先主卧有线扩展要求，不是等效替换 |
| 本文全部设备，路由改 [Cloud Gateway Fiber 无存储版](https://store.ui.com/us/en/products/ucg-fiber) | **$2,382** | 比 UCG-Max 多 $88；5Gbps 标称 IDS/IPS、更多 10G 接口；保留中央交换机，无需为当前 1G 宽带强制升级 |

现行 Omada 三频方案在 **2026-10-20** 的 Amazon 快照为 **$1,229.93**，官方商城快照为 **$1,314.93**。与本文完整 UniFi 预算分别相差 **$1,064.07 / $979.07**；仅作历史预算参照，**此次未刷新 Omada 报价，且新增主卧交换机导致设备结构不同**。不要把它解释为相同日期、相同渠道、完全同规格的实时价差。

对于目前“主卧不增加交换机、三频面板还能接电脑、单台电竞房交换机直接提供 10G 电口和光口”的偏好，现行 Omada 组合更贴合且历史预算更低。不能仅由品牌推断速度、覆盖或稳定性一定更好。**本次决定：因成本过高，不采用 UniFi；继续使用已确认的 Omada 方案。** 本文保留价格、规格与适配差异，供追溯，不作为待采购备选。

## 不计入本次硬件总价的项目

- Cat6A、两端模块/面板、短跳线、机柜与安装辅材、认证和施工；沿用原先范围但数量/长度需现场确认。
- NAS 与其短 DAC 或光模块/光纤、UPS，继续入住后再选；不新增 NAS 网卡，不增加各房间埋纤。
- J3455 / PC 升级网卡、Mac Studio、HomeView、HomePod、平板及独立绿米采购中的灯具、传感器、摄像头和 M200/M1S 网关；后续 HA 协调器仍仅属演进备选。
- AP 装饰盖与专用齐平安装件、可选云服务/安全订阅/延保；基础网络控制器已经在网关中。

次卧保留 RJ45，可按原方案复用 TL-7DR3630；它仍需要独立管理，不能因换成 UniFi 就被统一接管。HA 继续规划在 J3455 上，与网络管理控制器分开。

美版 AP 的 6GHz 硬件规格不等于中国大陆可合法启用或终端可用；沿用[既有地区核验结论](wifi7-6ghz-mainland-china-research.md)。按实际地区配置，不以更换品牌解决频段许可问题。

## 核验来源与可复算数据

商品价格与型号入口见 BOM，各参数以这些官方规格页核验：

- [UCG-Max](https://techspecs.ui.com/unifi/cloud-gateways/ucg-max)、[UCG-Fiber](https://techspecs.ui.com/unifi/cloud-gateways/ucg-fiber)。
- [Flex 2.5G PoE](https://techspecs.ui.com/unifi/switching/usw-flex-2-5g-8-poe)、[Pro XG 8 PoE](https://techspecs.ui.com/unifi/switching/usw-pro-xg-8-poe)。
- [U7 Pro Wall](https://techspecs.ui.com/unifi/wifi/u7-pro-wall)、[U7 Pro](https://techspecs.ui.com/unifi/wifi/u7-pro)、[U7 Pro XG Wall](https://techspecs.ui.com/unifi/wifi/u7-pro-xg-wall)、[U7 In-Wall](https://techspecs.ui.com/unifi/wifi/u7-iw)。
- 配件参数见 [210W 电源](https://store.ui.com/us/en/products/uacc-adapter-ac-210w)、[SFP+ 转电口模块](https://store.ui.com/us/en/products/uacc-cm-rj45-mg)。
- 研究用型号、数量、基础价、预算价和变体合计存放于 [UniFi 比较数据](../config/unifi-procurement-comparison.json)，与当前 Omada 采购数据分开维护。

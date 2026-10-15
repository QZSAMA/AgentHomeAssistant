# Apple HomeView 与 HomePod mini 2：官方核验与采购建议

> 核验日期：**2026-10-15**。核对Apple美国/中国大陆产品页、技术规格、美国HomeView配置页及Apple Intelligence支持说明；使用agent-browser读取页面，未购买或修改账户。
> 更正：此前“未来Apple Home Hub、型号与Thread能力待确认”已过时。正式产品为 **Apple HomeView**，已发布并开放美国预购；**发布/预购不等于已经交货，也不等于大陆全部功能可用**。
> 本文记录产品事实与建议；用户已确认大厅 **HomeView非壁挂／桌面版×1**，壁挂控制屏另选平板电脑或iPad。mini的最终代际/数量/地区及壁挂平板具体型号/数量/点位仍待定；已确认不代表已购买或授权立即下单。
> **用户偏好补充（2026-10-15）**：用户明确接受**英语Siri AI**，中文支持不再是购买前置条件或选型障碍。HomeView桌面版也已确认；mini代际仍待选，中国大陆服务、Apple账户与配套设备仍需验证。

## 1. 核验结果

| 项目 | Apple HomeView | HomePod mini 2 |
|---|---|---|
| 美国价格/供货 | 桌面版$299；壁挂版$299；预购，**11月13日起供货** [1]、[3] | $149；预购，**10月30日起供货** [4] |
| 大陆价格/供货 | 本次大陆产品URL未找到页面；美国规格页明确美国销售。**未核到大陆正式售价/供货或大陆可用性保证**，不推断永久不售 [2] | 大陆官网**¥1,099/台**，10月30日发售，已提供预购入口 [6] |
| 接入 | 内置Wi-Fi 6E（802.11ax）MIMO、蓝牙6、Thread；本项目沿用大厅AP Wi-Fi，不新增主干 [2] | Wi-Fi 6E/802.11ax、蓝牙6、Thread；三房接各自AP Wi-Fi，无须交换机端口或PoE [5]、[7] |
| Apple Home角色 | 官网明确智能家居中枢、家庭App、HomeKit/Matter配件控制及Thread能力；配网/地区与故障恢复仍待实机验证 [1]、[2] | 家庭中枢、HomeKit/Matter控制、Thread、广播和房间语音入口 [4]、[5][6] |
| 交互/硬件 | 7英寸1088×1088 Liquid Retina、A18、12MP摄像头、4麦克风；最多6人识别；画面/摄像头总览、对讲与音频 [1]、[2] | 3麦克风、360度音频、温湿度传感器；美国页列Sound Glow和新的Mac音频/环绕声用途，部分能力有软件/地区/配套要求 [4]、[5] |
| 电源 | 桌面版随箱1.5m USB-C线与30W适配器；100–240V AC。壁挂版不含支架、USB-C线或适配器；普通USB-C供电方案至少20W [2]、[3] | 随箱20W适配器；100–240V、50/60Hz，所需输出9V/2.22A [5]、[7] |
| Siri AI边界 | 产品页写**首发英语**；HomeView软件27.2的Siri AI为Beta，个人上下文需要兼容且启用AI的iPhone/iPad；系统要求iOS/iPadOS 27.2或更高 [1]、[2] | 美国页面写Siri AI在**后续免费软件更新**提供；大陆页面宣传普通Siri与中文控制，不把美国Siri AI宣传视为大陆承诺 [4]、[5][6] |

Wi-Fi 6E与AP的Wi-Fi 7相容，**不要求换AP/加有线端口，也不需要靠6GHz才能工作**；大陆6GHz不能按美国规格作为保证能力。HomeView/mini支持Thread不等于支持Zigbee，不能删除Aqara有线网关或HA协调器的待选角色。

## 2. 对本项目的建议

| 位置/角色 | 建议 | 数量/采购状态 |
|---|---|---|
| 大厅公共屏幕与Apple Home交互中枢 | **HomeView桌面版（非壁挂）已确认**：替代大厅HomePod，通过大厅AP Wi-Fi接入；使用随箱USB-C线和30W适配器，不买壁挂/PoE底座 | **1台，型号/安装版本已确认**；未购/未部署，大陆服务/账户/配套设备仍待验 |
| 壁挂控制屏 | 平板电脑或iPad；作为交互终端另行选型，不再选择HomeView壁挂版。iPad可规划家庭App/HA界面，其他平台的HA客户端/网页和kiosk能力逐型号核验 | 方向已确认；品牌/型号/尺寸、数量、点位、支架、供电与网络方式待定，不计价格/PoE |
| 主卧 | 新购时优先HomePod mini 2；方便床边语音/广播/音频并补Thread边界覆盖 | 建议1台，原三房数量不增加，代际待用户确认 |
| 次卧 | 同上；不能指望大厅HomeView隔门可靠拾音 | 建议1台，代际待用户确认 |
| 工作室 | 同上；保留房间语音入口，不因Mac已有扬声器或HomeView在大厅而默认取消 | 建议1台；若无需本房Siri/音频，可后补，代际待用户确认 |
| 已有一代mini（若用户实际已有） | 若稳定运行且只需基础Apple Home/Thread，不因新品强制淘汰；本项目未记录用户已有mini | 不新增替换数量 |
| 大厅大HomePod/更多HomeView/立体声对 | 当前需求不要求；不因新品推出额外买音响或凑环绕声 | 不进入BOM |

**HomeView桌面版×1已确认，官方参考$299，已计入[确定型号BOM](purchase-bom.md#1-已确认具体型号采购主表)。** 若以后确认三台mini 2，Apple子系统美国参考共$746（$299+3×$149），其中仅$447为mini建议增量，不能重复加HomeView。均不含税运/跨境；mini在大陆购买则3台¥3,297，不与美元直接相加。壁挂平板另选、暂不计价，mini的代际/数量/地区与颜色仍待用户选择。

若目的仅是让Apple Home/Thread运行，HomeView并非额外必需：mini本身可担任家庭中枢。HomeView的主要价值是用户已经提出的**大厅公共屏幕/操作入口**，不是代替J3455上的HA、Aqara Zigbee网络、Fusion网络管理或Mac模型服务器。

## 3. 必须保留的限制

1. **语言已接受，地区与服务仍待验**：用户接受英语Siri AI，不再将缺少中文作为阻碍。[Apple支持页][8]说明大陆购买的受支持设备目前不能使用Apple Intelligence；海外购买设备在大陆且Apple账户地区也为大陆时，目前同样不能使用。该文不是HomeView大陆兼容性验收，不据此保证改语言/账户地区即可解决。HomeView所需软件版本、个人上下文配套设备，以及mini的后续Siri AI更新仍需分别确认。
2. **不是Mac本地模型的开放麦克风**：官方未确认可把HomeView/mini的原始麦克风流直接交给任意HA Assist/Hermes/MLX模型。Siri AI不等于用户Mac上运行的Qwen等模型，本地自由对话链路继续单独设计。
3. **不是通用HA触控面板保证**：HomeView列有Safari和特定第三方音视频能力，但本次未核可安装HA客户端、长期运行HA kiosk面板或任意第三方App。可通过受支持HomeKit/Matter路径展示设备，实际实体/操作/离线行为另验。
4. **温湿度传感不自动替代所有Aqara传感器**：适合设备所在房间，优化区间约15–30℃/30–70%RH；放置、音频发热会影响精度，HA是否能读取这些实体需实测。卫生间、防水位置、精准空调联动和独立HA实体需求仍按专用传感器规划，不自动减BOM。
5. **停电控制链**：HomeView/mini为本地市电供电，不因AP的PoE UPS自动保活。若要停电仍有Siri/Thread/屏幕控制，需将这些电源和Aqara网关/J3455/沿途LAN纳入对应UPS策略。30W/20W是适配器能力，不是恒定耗电，按实测负载核续航。
6. **HomeView壁挂产品差异（非当前采购）**：Apple配置页另列Schneider Home的USB-C、AC硬接线及**PoE Wired（供电+直接联网）**底座 [3]；不是$299机身自带，也不等于本体原生RJ45/PoE。用户已选HomeView桌面版、壁挂改用平板/iPad，**这些HomeView壁挂底座不进入BOM**，不改变大厅Wi-Fi、端口或PoE预算。平板的供电/安装须按具体机型另设计，兼顾长期充电、散热和可拆维护，不默认需要PoE。

## 4. 当前BOM/拓扑处理

- 大厅“未来Apple Home Hub”改为 **Apple HomeView桌面版（非壁挂）×1，型号/安装版本已确认，未购；大陆服务/账户/配套设备待验**；已核Wi-Fi/Thread能力，物理Wi-Fi路径不变。
- 壁挂控制屏另记为平板电脑/iPad待选项，非HA主机或Thread边界路由器替代；型号/数量/点位/网络与供电方式未定，不画成每房一台，不擅加Cat6A主干、网口或PoE负载。
- 三房仍暂按各1台HomePod mini，新增 **mini 2优先推荐**与美/大陆官方报价；未获用户确认前不升级为确定代际，也不与旧mini重复计数。
- 智能家居Thread图补HomeView的Thread候选连接，注明配网/合规/恢复待实机验收；HomeView与mini不是串联必经链路。
- 网络/施工不改四Cat6A主干、两个房间箱、三面板一吊顶、AP PoE预算或NAS DAC。不因美国Wi-Fi 6E规格改变大陆频段边界。
- Amazon精确商品未核，不虚构ASIN；提供Apple官方购买入口。HomeView的$299加入确定型号参考小计，Omada网络小计保持不变；未定mini/壁挂平板不计确定价格。

## 5. 官方来源（均于2026-10-15读取）

[1]: https://www.apple.com/apple-homeview/
[2]: https://www.apple.com/apple-homeview/specs/
[3]: https://www.apple.com/shop/buy-home/apple-homeview
[4]: https://www.apple.com/homepod-mini/
[5]: https://www.apple.com/homepod-mini/specs/
[6]: https://www.apple.com.cn/homepod-mini/
[7]: https://www.apple.com.cn/homepod-mini/specs/
[8]: https://support.apple.com/en-us/121115

- [HomeView产品与价格/供货][1]、[技术规格与附件][2]、[官方购买配置][3]。
- [mini 2美国产品页][4]、[美国规格][5]、[大陆产品/价格][6]、[大陆规格][7]。
- [Apple Intelligence地区与系统限制][8]。部分功能受后续软件、语言、账户、服务与地区条件影响，采购前再次核对。

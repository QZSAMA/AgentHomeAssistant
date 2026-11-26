# 米家激光投影仪（2019款）无线规格核验

更新：2026-11-26。用户确认已有米家激光投影仪为2019款、2400 ANSI流明，并提供无线规格 **802.11 a/b/g/n/ac**。主卧为主要使用位置，可移动，Wi-Fi接入、不插网线。本轮未连接或改动实机。

## 当前结论

**按用户提供的完整无线规格，这台投影仪最高支持Wi-Fi 5（802.11ac），不支持Wi-Fi 6（802.11ax）。** 该结论以用户提供的规格为依据，不冒称已从该型号的原厂规格页独立核验。此前“ac/ax未确认”的记录由本次补充取代。

| 项目 | 当前记录 | 依据与边界 |
|---|---|---|
| 产品 | 米家激光投影仪2019款、2400 ANSI流明 | 用户2026-11-26最新确认，亮度不是本户实测 |
| 无线标准 | IEEE 802.11a/b/g/n/ac | 用户提供的规格原文 |
| 最高Wi-Fi代际 | **Wi-Fi 5 / 802.11ac** | ac对应Wi-Fi 5；规格没有ax，按不支持Wi-Fi 6记录 |
| 频段 | **2.4GHz和5GHz** | b/g属于2.4GHz，a/ac属于5GHz；不支持由此推定6GHz |
| 空间流、信道宽度、最大协商速率 | 待核 | 未提供1×1/2×2等信息，不臆定433/866Mbps或千兆实际吞吐 |
| WPA3 | 待核 | ac协议清单不能证明具体认证方式 |
| 完整铭牌型号 | 待实机补录 | L185JCN / fengmi.projector.l185仅保留为查找线索，不标为用户已确认型号 |

## 对现有网络方案的影响

EAP775-Wall官方规格包含IEEE 802.11a/b/g/n/ac/ax/be，可支持旧代际终端。投影仪可按双方共同支持的协议接入，不要求它也支持Wi-Fi 6/7；换成Wi-Fi 7 AP不会把投影仪自身升级为Wi-Fi 7。具体认证方式及连接稳定性仍需实机验收。

本户优先尝试主卧日常5GHz网络播放J3455上的实际影视文件；移动位置后重新验证覆盖和播放稳定性。若5GHz覆盖不足，再比较2.4GHz的实际体验。Wi-Fi代际和协商速率都不等于真实播放吞吐，不能仅凭Wi-Fi 5保证任意高码率视频无卡顿。

网络路径：投影仪 → 所在区域覆盖合适的AP（Wi-Fi）→ 中央ES210 → 客厅ES206 → J3455。不新增以太网、PoE或固定吊装；电竞房2.5G口用4余4、客厅5/5、中央PoE预算和Fusion分配不变。

## 待现场验证

1. 补录机身铭牌完整型号，避免混用米家超短焦、4K、1S或LED投影机参数。
2. 若AP/控制器可显示客户端协议，记录5GHz接入时的ac、信号和协商速率；该记录用于实测连接，不替代终端规格清单。
3. 用实际影视文件测试播放、拖动进度和移动摆放位置；确认所用播放器能访问J3455共享，必要时核解码和码率。全部现场项目仍为未运行。

## 来源与核验边界

- **用户直接提供（2026-11-26）**：2019款；最新确认2400 ANSI流明；无线规格原文“802.11 a/b/g/n/ac”。本户协议和Wi-Fi代际结论的主要依据。
- [TP-Link无线代际说明](https://www.tp-link.com/us/wifi/)：802.11n对应Wi-Fi 4、802.11ac对应Wi-Fi 5、802.11ax对应Wi-Fi 6；用于解释协议名称，不证明投影仪具体型号。
- [EAP775-Wall官方规格](https://www.omadanetworks.com/us/business-networking/omada-wifi-wall-plate/eap775-wall/)：Wireless Standards列出IEEE 802.11 a/b/g/n/ac/ax/be；只用于核对AP接入能力。
- [米家官方产品信息接口](https://home.mi.com/cgi-op/api/v1/baike/v2/product?model=fengmi.projector.l185)返回“米家激光投影仪”及fengmi.projector.l185标识，但没有无线协议参数；[官方说明入口](https://home.mi.com/views/introduction.html?region=cn&pdid=67260&model=fengmi.projector.l185)的说明内容接口本轮返回空正文，因此不把它作为ac/ax的独立证据。
- 搜索中另一[米家投影仪参数页](https://www.mi.com/projector/specs)对应TYY01ZM、800 ANSI LED机型，未将其2×2等参数移用于本户投影仪。

相关记录：[影音规划](av-and-gaming-layout.md)、[设备台账](home-infrastructure-register.md)、[网络拓扑](network-topology.md)。

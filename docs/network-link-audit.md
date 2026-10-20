# 网络采购链接核对记录

核对日期：2026-10-20。已逐页检查 Amazon 的商品标题、所选型号/款式、ASIN、端口特征和页面价格；官方商城另核对应商品 SKU 与价格。当前方案是 **3A 三频，暂定定稿**。双频方案保留为预算备选，按相同三台 AP、相同交换机配置比较。

## 已核对的型号与入口

| 型号 | 正确 Amazon ASIN | 2026-10-20 页面价 USD | 核对结果 |
|---|---|---:|---|
| Fusion 2.5G 普通版 | [B0H4P7XX8G](https://www.amazon.com/dp/B0H4P7XX8G) | $169.99 | 标题为 Fusion 2.5G Multi-WAN Wired VPN Router，五个2.5G口 |
| ES210XPP-M2 | [B0HB17QTKX](https://www.amazon.com/dp/B0HB17QTKX) | $229.99 | 页面列8×2.5G PoE++、1×10G RJ45、1×10G SFP+、200W，与[官方ES210XPP-M2](https://www.omadanetworks.com/us/business-networking/omada-switch-agile/es210xpp-m2/)匹配 |
| ES206XPP-M2 | [B0GKQ5SD2L](https://www.amazon.com/dp/B0GKQ5SD2L) | $149.99 | 选中5 Port / 2.5G PoE++ 120W，标题明确ES206XPP-M2；中央与大厅各一台 |
| EAP775-Wall | [B0G88FG4QH](https://www.amazon.com/dp/B0G88FG4QH) | $179.99 | 标题明确EAP775-Wall，三频，页面列2个2.5G口（含上联）与3个1G口 |
| EAP772 | [B0D2M26NYW](https://www.amazon.com/dp/B0D2M26NYW) | $169.99 | 标题/型号为EAP772，三频6GHz、2.5G上联 |
| EAP725-Wall，双频备选 | [B0FB1W85FN](https://www.amazon.com/dp/B0FB1W85FN) | $134.99 | 型号正确；商品页仍写三个下联口，**不能据此确认US V2四下联口或其报价** |
| EAP723，双频备选 | [B0DT4YP2GX](https://www.amazon.com/dp/B0DT4YP2GX) | $89.99 | 标题明确EAP723，双频Wi-Fi 7、2.5G上联 |
| Fusion 2.5G PoE，3B比较 | [B0HKQ8ZPML](https://www.amazon.com/dp/B0HKQ8ZPML) | $349.99 | 标题为PoE版，9个2.5G口、8口PoE+、110W；未选用 |

完整官方商城链接、官方单价、核对日期和方案数量存于 [采购数据](../config/network-procurement.json)。Amazon 的库存、卖家、地区配送和优惠可能变化，以上为页面价快照，不含税运、进口、辅材及施工。

## 修正内容

- 最新工作簿 `总览采购!P9` 原来指向 `B0GKPNRFGF`。实际商品是 **ES210X-M2**，无PoE且是两个SFP+；已修正为ES210XPP-M2的 `B0HB17QTKX`，与Mac所需原生10G RJ45口及AP供电一致。
- `总览采购!P10` 原来保留 `B0GRCDJJTC`，已统一到核验过的ES206XPP-M2 `B0GKQ5SD2L`。中央、大厅同型号使用同一个采购入口和单价。
- `总览采购!P11/P12` 已从旧双频725/723的入口改为三频775/772的入口。
- `来源定义!B26/B27/B34` 原来存在“显示网址已经改了、实际点击目标仍是旧网址”的情况；同时修正显示内容和链接关系。
- 采购表的型号、商品入口与单价从同一份型号数据生成，避免以后换型号时只改名称、漏改链接。网址使用原生超链接，导出后逐项核对实际点击目标。
- 双频备选同步为3A、两面板一吊顶。旧四AP、中央ES210、独立注入器等方案保留为明确标注的历史记录。

## 本次预算变化

| 方案 | Amazon USD | 官方商城 USD | 状态 |
|---|---:|---:|---|
| 3A三频：775×2 + 772×1 | $1,229.93 | $1,314.93 | 当前暂定定稿 |
| 3A双频：725×2 + 723×1 | $1,059.93 | $1,139.93 | 保留备选，725的US V2发货版本待核 |
| 3B三频：PoE Fusion替代普通Fusion与中央交换机 | $1,259.94 | $1,309.94 | 互斥整合比较 |

三频相对相同配置双频增加 **Amazon $170 / 官方 $175**。3A三频Amazon总价较2026-10-19的$1,264.21减少$34.28，原因是两台ES206XPP-M2的单价由$167.13刷新为$149.99，未改变硬件数量。3A比3B的当前Amazon价低$30.01。

## 核验范围

检查两份现行Excel的九张表、型号/数量、公式、采购链接、来源链接及主要版面。保留四条Cat6A、两处房间设备箱、工作室Mac原生10G RJ45与未来NAS的10G SFP+、三台AP交换机PoE直供。设备未采购或部署；Fusion与实际版本的adoption/PoE协商仍须到货验收。6GHz当地可用性沿用[专项研究](wifi7-6ghz-mainland-china-research.md)的边界。

导出后检查结果：两份文件各9张表、各48个原生超链接；网址单元格的点击目标与网址一致。采购合计与独立按型号/数量计算一致，无公式错误或未实现函数输出。已测试ES206单价增加$1使两台合计增加$2、AP单价为零仍保留合法零报价，测试后恢复原值；原有下拉验证、合并、冻结窗格及条件格式未改变。12份相关文档的本地文件链接和章节锚点均可解析。

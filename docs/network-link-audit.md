# 网络采购链接核对记录

2026-11-27 整理，仅保留当前所选型号的来源。下表链接/报价核验日期仍为 **2026-10-20**，本次未重新查询在售价格或库存，不将历史页面价当作订单成交价。

当前 Omada 订单为 ES206×1、ES210×2、EAP775-Wall×3、EAP772×1，共7台，订单总额 $901.49；Fusion 普通版×1购买未确认。金额和数量见[订单](network-order-20261118.md)及[采购 BOM](purchase-bom.md)，摆位与端口见[v1.6 拓扑](network-topology.md)。

## 已选型号与历史核验入口

| 型号 | Amazon ASIN | 2026-10-20 页面价 USD | 核对结果 |
|---|---|---:|---|
| Fusion 2.5G 普通版 | [B0H4P7XX8G](https://www.amazon.com/dp/B0H4P7XX8G) | $169.99 | 标题为 Fusion 2.5G Multi-WAN Wired VPN Router，五个2.5G口 |
| ES210XPP-M2 | [B0HB17QTKX](https://www.amazon.com/dp/B0HB17QTKX) | $229.99 | 页面列8×2.5G PoE++、1×10G RJ45、1×10G SFP+、200W，与[官方ES210XPP-M2](https://www.omadanetworks.com/us/business-networking/omada-switch-agile/es210xpp-m2/)匹配 |
| ES206XPP-M2 | [B0GKQ5SD2L](https://www.amazon.com/dp/B0GKQ5SD2L) | $149.99 | 选中5 Port / 2.5G PoE++ 120W，标题明确ES206XPP-M2；当前订单为客厅一台 |
| EAP775-Wall | [B0G88FG4QH](https://www.amazon.com/dp/B0G88FG4QH) | $179.99 | 标题明确EAP775-Wall，三频，页面列2个2.5G口（含上联）与3个1G口 |
| EAP772 | [B0D2M26NYW](https://www.amazon.com/dp/B0D2M26NYW) | $169.99 | 标题/型号为EAP772，三频6GHz、2.5G上联 |

官方商城链接、各自核对日期及当前数量保存在[采购数据](../config/network-procurement.json)。页面价不含税运、进口、辅材和施工；后续购买 Fusion 时仍需复核实际报价、地区配送与版本。

## 到货与接入核验

- ES210XPP-M2 含 PoE、独立10G RJ45和SFP+；不要误购无PoE的ES210X-M2。ES206XPP-M2按完整型号核对。
- Fusion 内置控制器须验证对本批交换机/AP的接管与配置恢复；AP的实际PoE协商、发货版本及冷启动供电按[拓扑验收](network-topology.md)执行。
- 6GHz仍沿用[专项研究](wifi7-6ghz-mainland-china-research.md)的证据边界。
- WAN来源核验保持2026-11-18日期：[当前桥接方案](wan-bridge-plan.md)、[光猫备用研究](ont-replacement-backup-research.md)及[32条来源记录](research/ont-replacement-20261118/sources.json)。本户光猫兼容性待实机核验。

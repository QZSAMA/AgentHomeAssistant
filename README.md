# AgentHomeAssistant

家庭网络、装修与智能家居的方案资料，软件主路线为 **Hermes Agent＋Home Assistant**。仓库保留隔离集成实验、独立只读探测器和三维户型示例；当前事实以台账、已确认订单和各专项验收记录为准。

## 当前状态

- **网络**：Omada ES210×2、ES206×1、EAP775-Wall×3、EAP772×1共7台已下单，订单总额 **$901.49**，待到货验收；Fusion 2.5G普通版×1购买未确认，完整计划8台，尚未安装/部署。见[订单](docs/network-order-20261118.md)与[采购BOM](docs/purchase-bom.md)。
- **接线**：采用[v1.6](docs/network-topology.md)：Fusion四LAN接中央、电竞及电脑墙口A/B；中央10G光纤接客厅，四AP与两M200集中PoE。光纤配件待核；同一家庭LAN，指定终端按[批准方案](docs/superpowers/specs/2026-11-05-home-device-rule-routing-design.md)选择OpenWrt。
- **位置**：J3455规划在客厅；Apple TV仅大厅一台；投影仪主卧为主、移动Wi-Fi使用。当前端口与施工数量统一查[逐线计划](docs/network-placement-and-cabling-plan.md)，现场未实施。
- **智能家居**：原绿米签字合同 **¥19,324** 与后续增补分开管理；M200×2为升级计划，差价、订单及交付待核。设备采购状态和集成待办见[基础设施台账](docs/home-infrastructure-register.md)。
- **软件**：采用Hermes官方HA插件接入Home Assistant；自研Middleware原型已退役。保留[隔离实验](examples/hermes-ha-lab/README.md)、独立REST探测器及离线测试、[三维户型模拟](examples/home-twin-3d/README.md)。真实联调尚未完成，运行入口见[Code Wiki](CODE_WIKI.md)。
- **办公**：使用Windows App直接连接公司AVD，不需要家庭工作子网或长期连接公司VPN的副路由。

## 方案与施工入口

| 主题 | 文档 |
|---|---|
| 当前事实、采购与选型 | [基础设施台账](docs/home-infrastructure-register.md) · [采购BOM](docs/purchase-bom.md) · [设备选型](docs/device-selection-list.md) · [网络订单](docs/network-order-20261118.md) |
| 网络与施工 | [拓扑及端口](docs/network-topology.md) · [逐线/点位计划](docs/network-placement-and-cabling-plan.md) · [施工需求](docs/renovation-wiring-requirements.md) · [Omada规格与验收](docs/tplink-network-research.md) |
| 宽带与分流 | [原光猫桥接](docs/wan-bridge-plan.md) · [同一LAN批准设计](docs/superpowers/specs/2026-11-05-home-device-rule-routing-design.md) · [实施计划](docs/superpowers/plans/2026-11-05-home-device-rule-routing.md) · [验收与应急单](docs/validation/home-device-rule-routing.md) |
| 装修图纸 | [原图与位置记录](docs/floorplan-and-network-locations.md) · [水电定位讨论稿](docs/electrical-network-positioning-draft-20261121.md)，点位、路径、标高和米数待现场签认 |
| 智能家居 | [接入拓扑](docs/smart-home-topology.md) · [绿米签字清单](docs/aqara-final-quote-20261026.md) · [增补计划](docs/aqara-supplement-plan-20261118.md) · [型号核验](docs/aqara-model-verification-20261121.md) · [全屋查漏](docs/smart-home-supplement-audit-20261118.md) |
| 影音与Apple终端 | [影音规划](docs/av-and-gaming-layout.md) · [投影仪Wi-Fi记录](docs/mijia-laser-projector-2019-wifi.md) · [Apple设备核验记录](docs/apple-home-devices-2026.md)，原查询日期和未验收边界沿用各页 |
| 文件产物 | [输出文件索引](outputs/README.md) · [智能设备增补Excel](outputs/aqara-supplement-20261118/全屋智能新增设备清单.xlsx) |

设备尚未到货、线路尚未施工或集成尚未验收的项目，均不能仅凭图纸、商品规格或文档提交记录标为完成。

## 软件与交互示例

### 三维户型与模拟灯光

[home-twin-3d](examples/home-twin-3d/README.md)提供CAD派生户型、旋转查看、设计参考配色、四盏模拟灯及场景切换，并包含NeonPlan原生导入备份。完成范围与限制见[交付核验](examples/home-twin-3d/docs/delivery-check.md)。

在仓库根目录运行：

```text
python examples/home-twin-3d/serve.py
```

打开 [本机预览](http://127.0.0.1:8776/)。这是模拟示例，没有连接真实Home Assistant；实体映射需后续逐个绑定与验收。

### Hermes / Home Assistant隔离实验

[实验指南](examples/hermes-ha-lab/README.md)包含固定版本、独立profile、虚拟helper和人工联调步骤；[验收记录](docs/validation/hermes-ha-lab.md)区分资料交付、离线测试与尚未执行的真实联调。独立REST探测器仅执行GET请求，不控制设备。

离线测试入口（不需要安装Hermes或连接家中HA）：

```text
python -m unittest discover -s tests/ha_lab -v
```

这条命令复验探测器契约；测试通过也不代表插件、模型、helper控制或真实设备已接通。Hermes实验和3D工具的职责、入口及边界见[Code Wiki](CODE_WIKI.md)。

## 保留的专项研究

以下是证据资料或待核事项，不自动进入采购和现场实施：

- [光猫替换研究](docs/ont-replacement-backup-research.md)、[6GHz地区与终端研究](docs/wifi7-6ghz-mainland-china-research.md)、[J3455游戏存储评估](docs/j3455-iscsi-game-library.md)。
- [Fusion按设备分流能力](docs/fusion-third-party-and-device-routing.md)、[Fusion官方功能核验](docs/fusion-domain-routing-capability-research.md)、[社区案例与可靠性](docs/home-routing-community-and-reliability.md)：当前执行范围以已批准的同一LAN方案为准。
- 楼宇对讲：[接入研究](docs/building-intercom-integration-research.md) · [型号/手册](docs/legrand-intercom-identification-and-manuals.md) · [ESP桥接调查](docs/legrand-esp-intercom-bridge-research.md) · [S6819161续篇](docs/legrand-s6819161-investigation-plan.md)。原室内机接口、视频和控制路径仍待核验。

资料入口整理于2026-11-27。已取消的网络备选和重复旧接线表可从Git历史追溯。

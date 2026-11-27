# AgentHomeAssistant · 工具与示例说明

整理日期：2026-11-27。当前软件路线为 **Hermes Agent＋Home Assistant**，通过Hermes官方HA插件验证家居查询与控制。自研Middleware原型已退役；仓库维护独立探测器、隔离联调资料及三维户型示例。家庭设备、采购、网络与施工事实查[README](README.md)及专项文档。

## 1. 软件组成与状态

| 部分 | 已有内容 | 当前边界 |
|---|---|---|
| [Hermes/HA实验](examples/hermes-ha-lab/README.md) | 固定版本说明、独立profile、HA helper/script配置片段与人工联调步骤 | 主集成路线；真实联调以[验收单](docs/validation/hermes-ha-lab.md)为准，尚未完成 |
| [只读REST探测器](scripts/ha_probe.py) | 标准库CLI、输入校验、GET请求、版本/实体状态断言与结构化结果 | 独立工具；不控制设备，探测通过不证明Hermes联调完成 |
| [探测器离线测试](tests/ha_lab/) | 本机HTTP夹具、模拟错误与CLI契约检查 | 不连接用户家中HA，不依赖Hermes安装 |
| [三维户型示例](examples/home-twin-3d/README.md) | CAD派生户型、本机预览、模拟灯光、NeonPlan导入备份 | 保留的交互示例；尚未连接真实HA，实体映射与控制需另行验收 |

## 2. Hermes＋HA联调入口

沿[隔离实验设计](docs/superpowers/specs/2026-10-13-hermes-ha-lab-design.md)和[实验指南](examples/hermes-ha-lab/README.md)实施。版本、插件commit与隔离条件在实验指南集中维护，本页不复制另一套版本表。

| 路径 | 用途 |
|---|---|
| [Hermes实验配置](examples/hermes-ha-lab/hermes/config.fragment.yaml) | 独立实验profile使用的配置片段 |
| [实验指令](examples/hermes-ha-lab/hermes/lab-instructions.md) | CLI允许的工具、实验实体和人工操作范围 |
| [HA配置片段](examples/hermes-ha-lab/homeassistant/configuration.fragment.yaml) | 启用实验packages的合并参考，不能覆盖完整HA配置 |
| [实验helper与script](examples/hermes-ha-lab/homeassistant/packages/aha_lab.yaml) | 虚拟开关和只操作该开关的脚本 |
| [联调验收记录](docs/validation/hermes-ha-lab.md) | 分别记录资料交付、离线检查、真实工具调用与状态回读 |

先在独立HA测试实例与Hermes实验profile验证“查询→控制helper→读回→调用script→读回”。安装和控制步骤按实验指南人工执行；目前没有真实设备、语音入口或长期运行服务的验收结果。

## 3. 只读探测器与离线测试

在仓库根目录运行：

```text
python scripts/ha_probe.py --help
python -m unittest discover -s tests/ha_lab -v
```

探测器仅用Python标准库；不需要安装根目录应用包。测试使用本机夹具和模拟传输，验证输入、HTTP响应、断言、输出与退出码。根目录[pyproject.toml](pyproject.toml)仅把可选pytest的发现范围限定为`tests/ha_lab`，不定义应用包、依赖、服务入口或覆盖率门槛；主要复验入口仍是上面的标准库unittest命令。Hermes与3D工具各按自己的指南管理。

准备好隔离测试HA及指南要求的环境变量后，可按需运行连接探测：

```text
python scripts/ha_probe.py --entity-id input_boolean.aha_lab_light --entity-id script.aha_lab_work_mode --json
```

脚本只GET API、配置及显式指定的实体；`--expect-version`检查版本，`--expect-state entity=on/off`检查观察到的helper状态。退出码`0`表示本次探测范围通过，`1`表示连接、响应或断言失败，`2`表示输入或配置无效。输出不包含Token或原始响应。

一次状态读取不能证明某次Hermes请求导致状态变化；插件加载、模型工具调用、控制动作及回读分别记录在[验收单](docs/validation/hermes-ha-lab.md)。离线测试也不能替代真实联调。

## 4. 三维户型与模拟灯光

在仓库根目录运行：

```text
python examples/home-twin-3d/serve.py
```

访问[本机预览](http://127.0.0.1:8776/)。页面提供旋转查看、设计参考配色和四盏模拟灯光交互；NeonPlan原生备份及其外观表达范围见[示例说明](examples/home-twin-3d/README.md)和[交付核验](examples/home-twin-3d/docs/delivery-check.md)。

预览使用本地模拟状态；导入文件、原始CAD派生数据、设计参考与许可证均保留在示例目录。完整几何/导出/浏览器测试按示例README运行，其依赖与Hermes实验分别管理。

## 5. 网络资料与办公接入

[结构化采购数据](config/network-procurement.json)维护订单、设备计划和物理接线事实；它不是HA实体配置。[同一LAN批准设计](docs/superpowers/specs/2026-11-05-home-device-rule-routing-design.md)、[实施计划](docs/superpowers/plans/2026-11-05-home-device-rule-routing.md)及[验收单](docs/validation/home-device-rule-routing.md)保留指定终端手动选用OpenWrt的计划，物理接线以[v1.6拓扑](docs/network-topology.md)为准。

办公使用Windows App直接连接公司AVD，不需要家庭工作子网或VPN副路由。家庭规则分流、Hermes/HA集成与办公远程桌面分别按各自需求验证。

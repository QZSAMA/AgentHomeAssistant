# Hermes ↔ HA 实验验收记录

记录日期：2026-10-13。关联 [runbook](../../examples/hermes-ha-lab/README.md)、[design](../superpowers/specs/2026-10-13-hermes-ha-lab-design.md)、[plan](../superpowers/plans/2026-10-13-hermes-ha-lab.md)。

本轮产出是软件实验准备与离线探测器；未安装 Hermes/HA/插件，未启动服务、接入 Token、操作真实 HA 或设备。状态只能是 `not_run`、`passed`、`failed`；没有真实运行不得改成 `passed`。

## 版本基线

| 组件 | 预期版本/来源 | 实装核对 |
| --- | --- | --- |
| Hermes | `v0.21.7` / `71d34bad1045610252eda02ee79549436896e784` | `not_run` |
| 官方 HA plugin | `homeassistant` `2.0.1` / `NousResearch/hermes-official-plugins` 的 `homeassistant` 子目录 | `not_run` |
| Plugin pin | `682b22d019a1109421faa62efe43e16b23c2ebef` | `not_run` |
| Home Assistant | `2026.10.1` | `not_run` |
| Python 实验基线 | `3.14` | `passed`：本机解释器为 `3.14.0`，仅用于离线探测器/unittest；不是 HA 或 Hermes 实装核对 |

这里的版本是实验约束；静态查看 release catalog 不能填成“实装核对通过”。之后执行时另填实际版本与差异。

## 准备/离线检查

| ID | 检查范围 | 状态 | 证据与限制 |
| --- | --- | --- | --- |
| S1 | Hermes release 命令与插件 pin 静态源码核对 | `passed` | 已对照 `v0.21.7` profile/plugins parser 与 install/catalog/metadata 实现；源链接和函数名见 runbook §6。未执行本机 Hermes 命令。裸名安装使用 live catalog，因此固定完整官方 repo URI、`#homeassistant`、`--ref`，并增加 source/revision gate。 |
| S2 | HA package/helper/script 示例静态语法核对 | `passed` | 对照官方 packages/input_boolean/script 文档；没有 HA schema 加载、`check_config` 或实例执行。 |
| S3 | 独立 REST 探测器离线 unittest | `passed` | 2026-10-13，Python 3.14.0，最终执行 `python -m unittest discover -s tests/ha_lab -v`：29 tests，3.384s，OK。本机回环 HTTP fixture 与注入错误不证明真实 HA 可用，也不替代旧 pytest 基线。另以 `-B -W error::ResourceWarning` 运行同一测试集通过。 |
| S4 | Git 空白与变更范围检查 | `passed` | 已执行 `git diff --check` 与 `git diff --cached --check`，无空白错误；暂存变更仅为本阶段 12 个文件，未纳入原工作区未提交文档。 |
| S5 | 旧 pytest 基线 | `failed` | 已执行 `python -m pytest --no-cov`，解释器报告 `No module named pytest`。这是当前环境依赖缺失，不能推断旧测试通过/失败；本轮不安装恢复。 |
| S6 | 独立代码／安全／文档复核 | `passed` | 29 项测试另行回归通过，无未解决阻断项。复核发现的畸形重定向 `Location` 异常已用失败测试复现并修复；实体发现、歧义拒绝和 HA 独立运行验收项已补齐。 |

## 独立 HA 与 Hermes 人工验收

| ID | 检查范围 | 状态 | 通过标准/未执行原因 |
| --- | --- | --- | --- |
| I1 | 测试环境与 Token 隔离 | `not_run` | 确认独立 HA 无真实集成/设备/生产备份/生产凭据，独立 `aha-lab` profile，测试 origin 可达范围受控。 |
| I2 | 版本与插件 provenance gate | `not_run` | 实装版本匹配；profile `plugins/.install-metadata.json` 的完整 SHA、`pinned`、官方 source 与 manifest 2.0.1 均符合 runbook。 |
| I3 | HA 配置检查与加载 | `not_run` | 操作者手动合并配置片段，HA 自己的配置检查与加载通过；仅写出 YAML 不算通过。 |
| I4 | helper/script 准备 | `not_run` | `input_boolean.aha_lab_light` 实际初态 `off`，`script.aha_lab_work_mode` 存在，脚本唯一动作是操控 helper。 |
| I5 | HA REST probe | `not_run` | `ha_probe.py` 退出码 0，`scope: ha_rest_probe`，API/config/两个显式实体检查通过；记录实际 HA 版本。只读探测不证明 on/off 或 Hermes 链路。 |
| I6 | Hermes 插件加载与工具选择 | `not_run` | 独立 profile 提供预期四个工具，CLI 仅选择 HA toolset，gateway/events 保持关闭。 |
| I7 | Hermes 发现实验实体 | `not_run` | `ha_list_entities` 分别按 `input_boolean` / `script` domain 过滤，发现两个精确测试实体 ID；不无过滤枚举全屋。 |
| I8 | Hermes 读初态 | `not_run` | `ha_get_state` 实际读回 helper `off`。 |
| I9 | Hermes 直接控制 helper | `not_run` | `input_boolean.turn_on` 后再次 `ha_get_state` 实际读回 `on`；随后 turn_off 并读回 `off`。HTTP success 单独不算。 |
| I10 | Hermes 调用 HA script | `not_run` | 调用 `script.aha_lab_work_mode` 后 helper 另一次读回 `on`；不使用 script 瞬时状态作为替代。 |
| I11 | 目标不明确时澄清/不执行 | `not_run` | 新无指代上下文会话请求“帮我打开那个设备。”；Hermes 澄清，不调用控制服务/猜测目标/虚构成功；核对工具记录及 HA UI helper 仍为 `off`。 |
| I12 | 错误与未确认状态处理 | `not_run` | 连接/认证/实体不可用/状态不符时停止，不自动重试，不改目标，不谎报动作已完成；仅在隔离实例人工验证。 |
| I13 | 停止 Hermes 后 HA 独立运行 | `not_run` | 所有实验 Hermes CLI 停止、无 gateway/计划任务后，HA UI 开关 helper 和原生 script 均能独立工作；UI 读回逐次确认，最后恢复 `off`。 |
| I14 | 恢复与清理 | `not_run` | helper 读回 `off`，退出 CLI 后禁用/移除实验插件，撤销 Token，确认路径后删除实验 profile，清除本轮凭据/环境变量与实验 package。 |
| I15 | 物理灯具、`light` 域、语音、事件、旧 Middleware | `not_run` | 本轮明确不在范围；不得从 helper/script 或 REST probe 成功推导通过。 |

即便 I5 是 `passed`，I6–I14 仍要逐项实际运行；不得把 REST 探测结果整体改名为 Hermes E2E。

下一阶段门槛：I1–I14 均实际 `passed` 后，才另行请求批准接入第一盏真实 Aqara 灯。本轮软件准备不是物理接入授权；Apple Home、ORVIBO、语音、跨 VLAN、自然语言长期自动化均不包含在本轮。

## 执行记录模板

每次执行追加脱敏记录，不提交原始 Token、`.env`、HA 全配置、全实体列表或完整聊天日志。

```text
时间与操作者：
验收 ID / scope：
状态：not_run | passed | failed
实际 Hermes tag/commit：
实际 plugin version / full revision / source gate：
实际 HA/Python 版本：
命令或工具名（不含凭据/内部 URL）：
显式测试实体：
最小证据（退出码、reason、预期状态与实际读回是否一致）：
失败原因或未执行原因：
恢复/清理结果：
```

## 旧仓库基线问题（仅记录）

- `src/middleware/main.py` 导入 `middleware.core.engine`，仓库没有对应模块；本轮没有修复入口。
- `src/middleware/adapters/ha_adapter.py` 的 `RealHAAdapter` 尚为 `NotImplementedError`；官方插件实验不经过该适配器。
- 旧 pytest 基线缺少 pytest 环境，见 S5；独立标准库 unittest 不能替代该基线。
- 本轮无安装、服务启动、真实集成或 push；离线检查的具体结果以实际执行记录为准。本地 Git 提交不代表集成验收通过。

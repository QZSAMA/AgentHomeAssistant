# Hermes × Home Assistant 第一阶段设计

日期：2026-10-13。状态：用户已批准，实施范围以同期[开发计划](../plans/2026-10-13-hermes-ha-lab.md)为准。

## 目标与边界

交付可复现的配置、只读检查工具、离线测试及真实联调清单。Hermes 使用官方 Home Assistant 插件直接连接 HA，不为旧 Mock 中间件增加控制接口。

本阶段不安装 Docker、不部署服务、不接入真实家居、不推送远端，也不修复旧中间件。开发完成不等于集成完成：离线测试只能验证底座；Hermes／HA 端到端行为必须另行验收。

开发基于本地 `main` 的独立 Git worktree，原工作区全部未提交内容留在原处，不复制、不覆盖、不纳入本阶段变更。网络、设备、布线台账维持原有事实源。

## 版本基线

| 组件 | 固定基线 | 来源 |
| --- | --- | --- |
| Hermes | `v0.21.7`，commit `71d34bad1045610252eda02ee79549436896e784` | [发布标签](https://github.com/NousResearch/hermes-agent/releases/tag/v0.21.7) |
| 官方 HA 插件 | `2.0.1`，revision `682b22d019a1109421faa62efe43e16b23c2ebef` | [该发布版插件目录](https://github.com/NousResearch/hermes-agent/blob/v0.21.7/plugin-catalog/homeassistant.yaml) |
| 后续测试 HA | `2026.10.1` | [HA 发布标签](https://github.com/home-assistant/core/releases/tag/2026.10.1) |
| 本机检查器与测试 | Python `3.14`，仅标准库 | 本机解释器；不要求安装本仓库旧依赖 |

插件来源是 `NousResearch/hermes-official-plugins` 的 `homeassistant` 子目录。不能因插件版本号相同，就跳过 revision 核对。不得静默改用 `main` 或最新插件目录。

## 配置结构

`examples/hermes-ha-lab/` 保存无凭据环境变量模板、HA package 及操作说明。

HA package 仅定义：

- `input_boolean.aha_lab_light`：虚拟开关，模拟开／关。
- `script.aha_lab_work_mode`：HA 原生脚本，仅调用该虚拟开关。

这不是物理灯具或 `light` 域兼容性验证。配置必须由操作者手动合入专用测试 HA；不得替换现有 `configuration.yaml`，不得覆盖同名实体／脚本。第一阶段不启用事件驱动 Agent。

Hermes 使用独立测试 profile，并配置 `HASS_URL`、`HASS_TOKEN`。长期 Token 不进入仓库、命令行参数、截图或验收日志。

测试 HA 必须不包含真实设备。官方插件的危险服务黑名单和提示词只是纵深防护，不是实体级权限隔离；独立 profile 也不改变 HA Token 的授权范围。

## 只读检查器接口

```powershell
python scripts/ha_probe.py --entity-id input_boolean.aha_lab_light --json
```

`scripts/ha_probe.py` 独立于 `src/middleware`，不启动或导入旧应用，仅使用标准库。

输入从环境变量取得 URL 和 Token；不接受命令行 Token。`--entity-id` 可重复，不指定则只检查 API 认证和 HA 版本。全部输入先校验；缺失配置、非法 URL／实体 ID 直接退出，不发请求。

仅发送以下 GET：

1. `/api/`：认证与 API 可达性。
2. `/api/config`：读取版本，输出只保留必要信息。
3. `/api/states/{entity_id}`：仅逐个读取明确指定实体，不枚举全屋状态。

每次请求超时 5 秒，无自动重试、无重定向，HTTPS 保持正常证书验证。任何失败不输出认证头、Token、原始响应或原始异常。

退出码约定：`0` 全部检查通过；`1` 连接／认证／API／实体检查失败；`2` 输入配置错误。

JSON 明确标注 `scope: ha_rest_probe`，包括检查范围、总体结果、HA 版本、逐项结果及固定脱敏原因。文本与 JSON 使用同一结果语义。不能把 `ha_rest_probe` 通过描述为 Hermes 端到端通过。

## 验证与状态管理

离线测试放在 `tests/ha_lab/`，运行：

```powershell
python -m unittest discover -s tests/ha_lab -v
```

覆盖输入校验、正常响应、401／403、实体不存在／不可用、超时／连接失败、非 JSON／结构错误、重定向拒绝、文本／JSON／退出码一致、错误脱敏及 GET-only。测试不连接真实 HA。

验收结果仅允许 `not_run`、`passed`、`failed`；未运行不填通过。文档将开发检查与真实联调分表记录。旧中间件测试单独记录，不宣称全量测试通过。

## 后续真实联调门槛

通过隔离测试 HA 验证实体发现、状态查询、文本开关并回读、原生脚本并回读、失败不虚构成功、Hermes 停止后 HA 仍能独立工作，才考虑接入第一盏真实 Aqara 灯。

官方 `ha_call_service` 返回成功只代表请求层面的成功，不能直接证明设备已执行。必须回读目标状态，并记录期望、实际及结论。

Apple Home、ORVIBO 空调、语音、跨 VLAN、自然语言创建长期自动化，以及生产 HA 部署选型，均不纳入本阶段。

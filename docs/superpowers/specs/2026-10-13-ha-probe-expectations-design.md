# HA 只读探针：预期版本与状态断言

日期：2026-10-13。用户已确认先开发只读验收增强，并要求完成后推送远程，以便后续有环境时验证。

## 范围

在已有 `scripts/ha_probe.py` 增加可选断言；不引入控制 API、插件管理器、CI、部署或真实 HA 操作。沿用 Python 3.14 标准库、现有隔离分支 `codex/hermes-ha-lab`。原工作区未提交内容不复制、不提交。

本次推送该开发分支至 `origin`（`QZSAMA/AgentHomeAssistant`），包含上一阶段底座与本轮增强；不直接合并或推送 `main`，不强推。

## CLI 与行为

```powershell
python scripts/ha_probe.py --expect-version 2026.10.1 --expect-state input_boolean.aha_lab_light=on --json
```

- `--expect-version VERSION`：可选，只允许提供一次，严格复用已有 HA 版本格式；按字符串精确比较，不做宽松版本归一化。
- `--expect-state ENTITY_ID=on|off`：可重复，状态值只接受小写 `on`、`off`。同一个实体重复声明（即使值相同）视为配置错误，避免无声覆盖。
- 每个状态断言本身就是一个显式读取目标，无需重复写 `--entity-id`。按原 `--entity-id` 顺序读取，再按声明顺序补入尚未选中的断言实体；不因额外断言重复读取已选中的实体。原先显式重复 `--entity-id` 的行为保持不变。
- 所有参数和合并后的实体 ID 在任何网络请求前完成校验。非法格式、重复断言、非法实体均退出 `2`，不反射输入内容。
- 不给新参数时，现有 JSON 结构、请求顺序、默认只检查 API／版本的行为不变。

## 执行与结果

保持 GET-only、5 秒 socket 操作超时、无重试、禁代理与重定向、正常 HTTPS 证书验证及 1 MiB 响应限制。

1. 检查 `/api/` 和 `/api/config`，沿用认证／响应结构校验。
2. 若指定版本断言，安全解析实际版本后新增 `version_expectation` 检查项：`version_matches` 或 `version_mismatch`。不匹配时退出 `1`，不继续读取实体；安全的实际版本仍在 `ha_version` 字段。
3. 实体响应先做既有结构／可用性校验，再精确比较 `state`。指定断言的 `entity_state` 项使用 `state_matches`／`state_mismatch`；未指定仍为 `entity_available`。单个实体失败不隐藏后续显式实体的检查。
4. 认证／HTTP／结构错误／`unknown`／`unavailable` 优先保留原失败原因，不伪装成状态不符或通过。

总体通过退出 `0`，请求／断言失败退出 `1`，输入错误退出 `2`。JSON／文本使用相同检查结果，范围始终为 `ha_rest_probe`。新参数不输出原始预期值或实际状态；输出固定 reason，防止误填凭据或响应反射泄露。

## 验收含义

断言只说明本次 GET 观察到的值是否符合预期。它不证明状态由某次 Hermes 操作导致，不验证插件调用链，也不验证物理设备。官方插件控制后仍需通过实际工具记录与回读完成真实验收；状态传播可能有延迟，本工具不会轮询或重发控制指令。

## 离线测试

沿用本机回环 HTTP fixture 和必要的传输故障注入；不用真实 URL 或 Token。覆盖匹配／不匹配、版本失败短路、多实体混合、参数校验零网络、重复声明、严格大小写／空白、不可用／无效响应优先、JSON／文本／退出码一致、脱敏、GET-only、CLI 帮助和原 29 项回归。

真实 HA／Hermes 验收继续保持 `not_run`；远程推送不是集成验收。

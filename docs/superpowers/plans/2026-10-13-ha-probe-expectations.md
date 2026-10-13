# HA Probe Expectations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 HA 只读探针添加可选预期版本与 on/off 断言，离线验证后推送开发分支。

**Architecture:** 在现有参数校验与 GET 响应处理间增加纯参数解析及断言，复用现有脱敏报告。操作说明记录新用法及局限，独立复核后仅提交本轮相关文件。

**Tech Stack:** Python 3.14 标准库、unittest、现有回环 HTTP fixture、Git。

## Global Constraints

- 设计：[ha-probe-expectations-design](../specs/2026-10-13-ha-probe-expectations-design.md)。
- 仅修改隔离工作区 `D:\Repo\qz\.worktrees\AgentHomeAssistant-hermes-ha-lab`，分支 `codex/hermes-ha-lab`，基线 `ab7f4e3`。
- 不安装依赖、不启动 HA/Hermes、不连接真实设备、不修旧中间件。
- 保持 GET-only、5 秒 socket 操作超时、无重试、禁代理／重定向、正常 TLS、响应上限。
- 不输出 Token、URL、原始错误／响应、预期参数原文或实体实际状态。
- 所有真实联调项 `not_run`；离线通过不代表 Hermes E2E。
- 本次用户已授权完成后推送 `origin` 开发分支，不强推、不改远端 `main`。

---

### Task 1: 断言与回归测试

**Files:**
- Modify: `scripts/ha_probe.py`
- Modify: `tests/ha_lab/test_ha_probe.py`

**Interfaces:**
- Consumes: `main(argv: list[str] | None = None) -> int`、既有 `VERSION_PATTERN`、`InputError`、`validate_settings`、`add_check`、回环 fixture 的 `run_probe`。
- Produces: `parse_expectations(versions: list[str], states: list[str]) -> tuple[str | None, dict[str, str]]`；`probe(base_url, token, entities, expected_version=None, expected_states=None)`，保留前三参数兼容。

- [x] 基线运行 `python -m unittest discover -s tests/ha_lab -v`，29 tests passed。
- [x] 先写并运行失败测试：匹配版本 `2026.10.1` 返回 `version_matches`；不匹配返回 `version_mismatch`／退出 1，只有 `/api/`、`/api/config` 请求。
- [x] 先写状态断言失败测试，复用已有 fixture：

```python
def test_expected_state_matches(self):
    code, report = self.run_probe([
        "--expect-state", "input_boolean.aha_poc_light=off"
    ])
    self.assertEqual(code, 0)
    self.assertEqual(report["checks"][-1]["reason"], "state_matches")
    self.assertEqual(self.server.requests[-1][1],
                     "/api/states/input_boolean.aha_poc_light")

def test_expected_state_mismatch(self):
    code, report = self.run_probe([
        "--expect-state", "input_boolean.aha_poc_light=on"
    ])
    self.assertEqual(code, 1)
    self.assertEqual(report["checks"][-1]["reason"], "state_mismatch")
```

- [x] 增补负向和兼容用例：重复版本、非法版本、缺 `=`、空 ID／状态、多个 `=`、大写／空白、重复实体断言、非法实体、token 注入、响应结构错误／不可用／HTTP失败、混合实体顺序和不重复附加、无新参数的完整报告不变。每项断言具体 reason、exit、请求记录或固定输出，不测试 mock 自身。
- [x] 执行上述完整命令观察 RED，确认失败来自新参数／行为尚不存在，而非测试语法错误。
- [x] 实现纯参数解析，错误内容固定：

```python
def parse_expectations(versions: list[str], states: list[str]) -> tuple[str | None, dict[str, str]]:
    if len(versions) > 1 or any(not VERSION_PATTERN.fullmatch(v) for v in versions):
        raise InputError("invalid_expected_version")
    expected_states = {}
    for specification in states:
        entity_id, separator, state = specification.partition("=")
        if not separator or not entity_id or state not in {"on", "off"}:
            raise InputError("invalid_expected_state")
        if entity_id in expected_states:
            raise InputError("duplicate_expected_state")
        expected_states[entity_id] = state
    return (versions[0] if versions else None), expected_states
```

- [x] `main` 新增两个 `action="append", default=[]` 参数；合并实体后交给 `validate_settings`，整个流程仍在 `InputError` 保护内。核心接线：

```python
expected_version, expected_states = parse_expectations(options.expect_version, options.expect_state)
entities = list(options.entity_id)
entities.extend(entity_id for entity_id in expected_states if entity_id not in entities)
base_url = validate_settings(os.environ.get("HASS_URL", ""), token, entities)
report = probe(base_url, token, entities, expected_version, expected_states)
```

- [x] `probe` 读取安全实际版本后执行以下断言；实体检查在原始错误／不可用判断之后精确匹配，不改变 transport：

```python
if expected_version is not None:
    matches = version == expected_version
    add_check(report, "version_expectation", "version_matches" if matches else "version_mismatch", matches)
    if not matches:
        return report

# After the existing entity response checks:
expected_state = (expected_states or {}).get(entity_id)
if reason is None and expected_state is not None and state["state"] != expected_state:
    reason = "state_mismatch"
success_reason = "state_matches" if expected_state is not None else "entity_available"
add_check(report, "entity_state", reason or success_reason, reason is None, entity_id)
```

- [x] 再运行完整测试集为 GREEN；补文本与 JSON 一致性、独立 CLI 帮助／新参数及资源警告回归。

### Task 2: 联调用法与记录

**Files:**
- Modify: `examples/hermes-ha-lab/README.md`
- Modify: `docs/validation/hermes-ha-lab.md`

**Interfaces:**
- Consumes: Task 1 的 CLI、固定 reason 与 exit 0/1/2。
- Produces: 可在未来测试环境直接运行的命令和诚实验收记录。

- [x] 保留无断言用法，新增如下版本／状态检查例子，并说明 `on`、`off` 的适用步骤：

```powershell
python scripts/ha_probe.py --expect-version 2026.10.1 --expect-state input_boolean.aha_lab_light=on --json
python scripts/ha_probe.py --expect-version 2026.10.1 --expect-state input_boolean.aha_lab_light=off --json
```

- [x] 说明状态断言隐式选中该明确实体、重复声明拒绝、严格比较、版本失败短路、无自动重试，默认探针仍不判断 on/off；GET 观察不能证明 Hermes 因果关系。
- [x] 验收记录新增本轮离线测试结果，不改历史第一阶段测试数；真实新增断言／Hermes验收继续 `not_run`。
- [x] 用 `rg -n 'expect-version|expect-state|not_run|推送' examples/hermes-ha-lab/README.md docs/validation/hermes-ha-lab.md` 对照实现；修正文档中“本轮不推送”的当前描述，保留第一阶段历史事实。

### Task 3: 独立复核、提交与推送

**Files:**
- Review: Tasks 1–2 所有文件及本设计／计划。

- [x] 独立 reviewer 检查默认兼容、预校验、固定脱敏 reason、无控制请求、版本短路、真实验收仍未运行；发现缺陷必须先补失败测试再修复。
- [x] 最终运行 `python -m unittest discover -s tests/ha_lab -v` 与 `python -B -W error::ResourceWarning -m unittest discover -s tests/ha_lab -v`；应全部通过。
- [x] `git diff --check`、逐个暂存本轮文件，执行 `git diff --cached --check` 与 `git diff --cached --stat`，排除原工作区改动和秘密文件。
- [x] `git commit -m "feat: add read-only HA version and state expectations"`。
- [x] 只读核对远端 `git ls-remote --heads origin refs/heads/codex/hermes-ha-lab`；存在非快进冲突时停止，不强推。
- [x] `git push --set-upstream origin codex/hermes-ha-lab`，仅在本地验证完成后执行。
- [x] 再次读取远端 ref，与本地 `git rev-parse HEAD` 一致才报告推送完成；附远程分支链接与后续拉取／验证命令。真实联调状态不因推送改变。

## 执行结果

- 50 项离线测试通过（原 29 项 + 新 21 项），严格资源警告测试和独立复核通过。
- 实现提交 `4bcdbdeeba1da77ac1d005b831d3ba94caae9ec1` 已推送并核对远端 ref；远端 `main` 未变。
- 使用现有仓库授权完成推送，仅作用于该次 Git 进程；未改变全局默认账号、未将令牌写入仓库。
- 交付与真实验收状态见 [validation](../../validation/hermes-ha-lab.md)；真实联调仍为 `not_run`。

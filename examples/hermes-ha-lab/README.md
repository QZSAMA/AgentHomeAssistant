# Hermes ↔ Home Assistant 隔离软件实验

目标是用官方 HA 插件验证“查询 → 控制 helper → 读回 → 调用 script → 读回”的最小链路，不经过旧 Middleware，不接真实设备。本目录提供配置片段与人工 runbook，**没有安装、启动或真实联调完成的含义**。当前验收记录见 [validation](../../docs/validation/hermes-ha-lab.md)，设计与实施边界见 [design](../../docs/superpowers/specs/2026-10-13-hermes-ha-lab-design.md)。

## 1. 固定版本与安全边界

| 组件 | 本实验基线 |
| --- | --- |
| Hermes Agent | `v0.21.7`，commit `71d34bad1045610252eda02ee79549436896e784` |
| 官方 HA 插件 | `homeassistant` `2.0.1`，`NousResearch/hermes-official-plugins` 的 `homeassistant` 子目录 |
| 插件 immutable commit | `682b22d019a1109421faa62efe43e16b23c2ebef` |
| Home Assistant | `2026.10.1` |
| Python | `3.14`（独立 REST 探测器仅使用标准库） |

版本是待部署的实验基线，不是本机已安装清单。若实装不一致，先记录差异并停止验收，不自动升级或用 `main` 替代。

必须新建独立 HA 测试实例及 Hermes `aha-lab` profile。测试 HA 不得连接真实集成/设备、生产备份、生产账号或生产 HA Token；检查并禁用发现后添加集成，不启用任何自动发现的真实设备。实例应仅在本机回环或明确隔离、受信任的实验网络可达，不开放公网。`HASS_URL` 必须显式填写该实例 origin，不依赖 `homeassistant.local` 自动发现。

HA 长效 Token 不提供本实验所需的逐实体 allowlist。插件屏蔽 `shell_command`、`command_line`、`python_script`、`pyscript`、`hassio`、`rest_command` 等域，也不等于逐实体权限。CLI 工具选择和自然语言约定同样不是安全沙箱；所以不能仅靠“只操作两个实体”的提示来安全连接生产 HA。

本轮只使用：

- `input_boolean.aha_lab_light`：状态 `on` / `off` 的 helper，不是 `light` 域灯具。
- `script.aha_lab_work_mode`：唯一动作是开启上述 helper。
- Hermes CLI 的四个工具：`ha_list_entities`、`ha_get_state`、`ha_list_services`、`ha_call_service`。

**Gateway、HA 事件订阅、定时任务、物理设备与语音入口均不启用。** 本轮没有 `hermes gateway` 启动步骤。

## 2. 人工准备测试 HA

以下步骤供操作者之后手动执行；仓库维护本身不执行安装、配置修改或服务启动。

1. 准备独立 `2026.10.1` HA 测试实例，确认无真实集成/设备。记录版本与部署方式，不记录 Token。
2. 备份该测试实例的配置。阅读 [HA fragment](homeassistant/configuration.fragment.yaml)，手动把 `packages` 配置合并到现有 `homeassistant:` 节点；**绝不能用本片段替换整个 `configuration.yaml`**，也不能重复根节点或 `packages` 键。
3. 如果已有 `packages` include，沿用其结构。示例包适配 `!include_dir_named packages`；若使用 `!include_dir_merge_named`，必须按官方文档调整包名层级，不能直接照抄。
4. 手动把 [aha_lab.yaml](homeassistant/packages/aha_lab.yaml) 放入该测试实例对应的包目录。检查是否存在同名 entity/script，若有冲突则停止，不覆盖。
5. 使用该部署方式支持的 HA 配置检查方式，确认配置通过后再按其流程重新加载/重启。此仓库没有替你运行 HA `check_config` 或加载验证。
6. 在 HA 状态工具中确认两个实体存在，helper 初始为 `off`，script 可用。helper 配置了 `initial: false`，HA 重启会重新置 `off`，不应依赖跨重启恢复状态。
7. 仅在该测试 HA 的用户 Profile → Long-Lived Access Tokens 创建专用临时 Token。保持服务器与 Token 的使用范围仅限实验；结束后撤销。

## 3. 人工准备独立 Hermes profile 与固定插件

命令语法静态核对自 `v0.21.7` release 源码，未在本机执行 Hermes 安装/运行。先确认实际 Hermes 安装的 tag/commit 和 Python 版本，不执行自动更新。不改用户现有 profile，不调用 `profile use`，不使用 `--clone` / `--clone-all` / `--clone-from`。

```text
hermes profile list
hermes profile create aha-lab --no-alias --no-skills
hermes profile show aha-lab
```

若 `aha-lab` 已存在，停止并检查归属，不复用/清空未知 profile。`--no-alias` 不创建全局包装命令；`--no-skills` 不同步内置 skills。全新 profile 仍可能从当前 profile 种入 model 配置块，操作者须检查其模型/提供商设置，不复制用户的聊天平台、事件、MCP、凭据或工作文件。

直接固定官方 repo、子目录与完整 SHA，安装后保持禁用：

```text
hermes -p aha-lab plugins install "https://github.com/NousResearch/hermes-official-plugins.git#homeassistant" --ref 682b22d019a1109421faa62efe43e16b23c2ebef --no-enable
hermes -p aha-lab plugins list --json
hermes -p aha-lab plugins show homeassistant
```

这属于显式 Git 来源安装，CLI 可能标为 custom source；虽然 SHA 与 `v0.21.7` release catalog 记录相同，也不能伪称本次通过 live catalog-reviewed 安装。裸名 `plugins install homeassistant` 会访问 live catalog，**不是保证只读 release 内 catalog**；仅加 `--ref` 也未固定来源，所以本实验不以裸名命令作为可复现安装步骤。

若被安全策略拒绝，先停止，不绕过扫描、kill list 或安装确认。不要在已安装副本上用 `--force` 覆盖；重新检查 profile 状态再决定。依赖/安全提示需人工审查，插件依赖为 `aiohttp >=3.9,<4` 并受 Hermes 自身约束；不要添加自动同意/忽略扫描的参数。

### 启用前的 revision gate

以 `hermes profile show aha-lab` 显示的实际 profile 路径为准；默认一般为 `~/.hermes/profiles/aha-lab`，但自定义 Hermes 根目录可以不同。

- 权威安装记录：`<profile>/plugins/.install-metadata.json` 的 `homeassistant` 条目。
- 必须核对完整 `revision` 为固定 40 位 SHA、`pinned` 为 `true`、`source` 精确为 `https://github.com/NousResearch/hermes-official-plugins.git#homeassistant`。该值来自 release 的 `_canonical_source(git_url, subdir)`，包含 `#homeassistant`。
- 插件 manifest：`<profile>/plugins/homeassistant/plugin.yaml`，确认 `name: homeassistant`、`version: 2.0.1`。
- `plugins list --json` 的 source 只显示短 SHA/注释，不能替代完整 SHA 核验；插件目录内 `.hermes-catalog.json` 也不是权威 provenance。

可手动检查以上非秘密字段，或在 PowerShell 使用以下只读 gate。先把路径改为已确认的实际 profile；不要指向当前用户默认 profile：

```powershell
$labProfilePath = 'C:\Users\<you>\.hermes\profiles\aha-lab'
$labRecord = (Get-Content -LiteralPath (Join-Path $labProfilePath 'plugins/.install-metadata.json') -Raw | ConvertFrom-Json).homeassistant
if ($labRecord.revision -cne '682b22d019a1109421faa62efe43e16b23c2ebef' -or
    $labRecord.pinned -ne $true -or
    $labRecord.source -cne 'https://github.com/NousResearch/hermes-official-plugins.git#homeassistant') {
    throw 'Plugin source/revision gate failed; leave the plugin disabled.'
}
Get-Content -LiteralPath (Join-Path $labProfilePath 'plugins/homeassistant/plugin.yaml')
```

上面只验证安装元数据与显示 manifest，不能证明目录没有后来被人工修改。若来源、版本、文件完整性或扫描结果不可信，停止，不启用。启用前人工确认 manifest 版本，再继续。

### 凭据、工具与模型配置

把 [.env.example](.env.example) 的两个键手动合并进 **aha-lab 自己的 `.env`**：填入测试 HA origin 和临时 Token。不要覆盖已有 `.env`，不要把值放进命令参数/聊天/日志。探测脚本不自动加载 `.env`；运行它的进程还需安全地设置同名环境变量。远程连接使用验证有效证书的 HTTPS，测试 Token 不应用于明文跨不可信网络。

把 [Hermes fragment](hermes/config.fragment.yaml) 手动合并到 **aha-lab 的 `config.yaml`**，保留已有 model 配置，不重复 YAML 根键。该片段显式禁用 HA gateway/events，并把 CLI toolset 限为 `homeassistant`；`HASS_TOKEN` 虽使工具可用，不应隐式开启 gateway。再人工配置实验模型提供商/端点与必要凭据，模型生命周期与 HA 独立；本目录不包含模型安装或语音方案。

核对上述配置与安全提示后才启用插件：

```text
hermes -p aha-lab plugins enable homeassistant
hermes -p aha-lab tools list --platform cli
```

确认只为本实验提供预期 HA 工具、无事件通道；不要因为工具列表出现就声称 HA 连接成功。不运行 `plugins update`、不改 SHA、不启动 gateway。

## 4. 分层验收

### A. 只读 REST 探测

在仓库根目录，以测试实例的 `HASS_URL` / `HASS_TOKEN` 环境变量运行：

```text
python scripts/ha_probe.py --entity-id input_boolean.aha_lab_light --entity-id script.aha_lab_work_mode --json
```

脚本仅 `GET /api/`、`GET /api/config` 和显式指定实体的 `GET /api/states/{entity_id}`，不枚举全屋实体、不 POST、不订阅事件。固定 5 秒 socket/单次网络操作超时（不是所有检查合计的总截止时间），无重试，不跟随重定向、不解析其 Location；仅接受不超过 1 MiB 的响应，最多读取 1 MiB + 1 字节以检测溢出。探测器禁用环境代理，不通过 `HTTP_PROXY` / `HTTPS_PROXY` 等代理变量转发 HA Token。URL 仅接受 `http(s)` origin（可带一个末尾 `/`），不接受 userinfo、其他 path/query/fragment、空白或控制字符。

JSON 的 `scope` 固定为 `ha_rest_probe`，包含 `status`、`exit_code`、`ha_version` 和逐项 `checks`；每项带 `name`、`status`、`reason`，实体项带显式 `entity_id`。不输出 Token、URL、原始响应、实体属性、状态值或预期参数原文。退出码 `0`=该探测范围全通过，`1`=连接/响应或预期断言失败，`2`=输入或配置无效。文本输出与 JSON 使用相同检查结果。

不传断言参数时，脚本仍只检查实体响应结构和非 `unknown` / `unavailable`，**不判断 helper 是 on 还是 off**；不指定任何实体时，只检查 API 与 HA 版本响应，不读取实体。默认 JSON 结构与请求顺序保持不变。REST probe `passed` 不能证明 Hermes 已安装、插件已加载、模型工具调用成功、script 正确控制 helper、真实灯具或 `light` 域成功；未使用版本断言时，HA 版本仍需与固定基线人工核对。

#### 可选：预期版本与 helper 状态断言

在后续隔离环境中，可以增加一次性只读断言。下面是不同验收时点使用的两个命令，不是控制操作，也不要不分阶段地连续执行：

```text
python scripts/ha_probe.py --expect-version 2026.10.1 --expect-state input_boolean.aha_lab_light=on --json
python scripts/ha_probe.py --expect-version 2026.10.1 --expect-state input_boolean.aha_lab_light=off --json
```

`on` 适合在 B2 直接开启或 B4 调用 script 后补充观察；`off` 适合 B1 初态、B3/B5 恢复后观察。它们不替代 B 节的 Hermes 工具调用记录与 `ha_get_state` 回读。尤其不能因为 helper 已经是 `on`，就推断某次 Hermes 请求导致了它开启。

- `--expect-version VERSION` 只能提供一次，即使重复值相同也拒绝。格式沿用 HA 版本校验；按完整字符串精确比较，不去空白、不做版本归一化。
- `--expect-state ENTITY_ID=on|off` 可为不同实体重复提供，状态仅接受小写 `on` 或 `off`。同一实体重复声明全部拒绝，即使期望值相同也不覆盖；多余空白、缺少/多出 `=`、非法 ID 或状态均为输入错误。
- 状态断言本身就是一个明确读取目标，不必再写 `--entity-id`。先按原 `--entity-id` 顺序读取，再按断言声明顺序补入尚未选中的实体；新增断言不会重复附加已有目标。原先手动重复 `--entity-id` 的行为不变。
- 全部参数与合并后的实体 ID 在网络请求前校验；输入错误退出 `2`，不发请求，也不回显错误参数原文。

读取 `/api/`、`/api/config` 后，版本断言新增 `version_expectation` 检查项：匹配为 `version_matches`；不匹配为 `version_mismatch`、退出 `1`，并**停止后续实体读取**。安全解析出的实际版本仍保留在 `ha_version`，但不回显预期版本参数原文。

实体先通过原有结构和可用性检查，再比较预期状态：断言项返回 `state_matches` 或 `state_mismatch`，没有断言的实体仍为 `entity_available`。单个实体不符或失败不会跳过后续明确目标；总体只要有失败就退出 `1`。认证/HTTP/结构错误或 `unknown` / `unavailable` 保留各自原失败原因，不把它们伪装成普通 `state_mismatch`。

范围仍为 `ha_rest_probe`：断言只证明**这一次 GET 观察**是否符合预期，不证明 Hermes 因果链、插件成功或物理设备成功。状态传播可能有延迟；本工具不轮询、不重试、不发送 POST，也不补发控制指令。发生不匹配应停止并人工检查原因，不因脚本失败自动再次控制设备。

### B. Hermes CLI → helper → script

仅在 A 完成、隔离条件确认、版本与插件 gate 完成后人工启动 `hermes -p aha-lab chat`。先粘贴 [lab-instructions](hermes/lab-instructions.md)，再按下表逐步发出明确请求。每一步等待结果，不批量自动执行；失败后停止，不自动重试。

| 步骤 | 工具/参数参考 | 通过条件 |
| --- | --- | --- |
| B0 发现实验实体 | 两次 `ha_list_entities`，分别传 `{"domain":"input_boolean"}` 与 `{"domain":"script"}` | 返回结果分别包含精确 ID `input_boolean.aha_lab_light` 与 `script.aha_lab_work_mode`；仅在独立测试实例按 domain 过滤，不无过滤枚举全屋 |
| B1 查询服务与初态 | `ha_list_services`，`{"domain":"input_boolean"}`；`ha_get_state`，`{"entity_id":"input_boolean.aha_lab_light"}` | 所需服务存在，helper 实际读回 `off` |
| B2 直接开启 helper | `ha_call_service`，`{"domain":"input_boolean","service":"turn_on","entity_id":"input_boolean.aha_lab_light","data":"{}"}` | 工具无错误；随后另一次 `ha_get_state` 实际读回 `on` |
| B3 恢复起始状态 | `ha_call_service`，`{"domain":"input_boolean","service":"turn_off","entity_id":"input_boolean.aha_lab_light","data":"{}"}` | 再次读回 `off` |
| B4 调用工作场景 | `ha_call_service`，`{"domain":"script","service":"turn_on","entity_id":"script.aha_lab_work_mode","data":"{}"}` | 随后查询 helper，实际读回 `on`，不能用 script 自己瞬时状态替代 |
| B5 清理状态 | 与 B3 相同 | helper 再次读回 `off` |

插件工具的 `data` 参数是 **JSON 字符串**，所以示例是 `"data":"{}"`，不是 `"data":{}`。模型可能先选择工具；记录它实际使用的工具名/目标与读回结果，若调用了非实验对象则立即停止。

插件 HTTP service 成功可返回 `success: true`，甚至没有 affected entities；不能据此报告动作已完成。只有后续 `ha_get_state` 的实际 helper 状态匹配预期才通过。初态不是 `off` 时先人工确认原因并用受控恢复步骤置 `off`，重新读取后才开始计次。

### C. 目标不明确的负向用例

先确认 helper 已恢复 `off`。退出已有交互，开启没有此前指代上下文的新实验 CLI 会话，粘贴同一操作约定，然后只说“帮我打开那个设备。”，不指定实体、房间或场景。

通过条件：Hermes 先提问澄清目标，不猜对象、不调用 `ha_call_service`，也不声称已经打开。检查实际工具调用记录，并在 HA UI 独立确认 helper 仍为 `off`。只看自然语言回复不足以通过；若发生控制调用，即便最终 helper 没变，也应记 `failed` 并停止。此用例验证模型行为，不将其当作实体权限隔离的证明。

### D. 停止 Hermes 后 HA 仍独立工作

完成上述步骤后退出 **所有 aha-lab CLI 会话**，确认没有该实验的 Hermes 进程、gateway 或计划任务在运行。此时尚不删除 HA package，执行以下人工验收：

1. 在测试 HA UI 把 helper 开启，再关闭，分别查看其实际 `on` / `off` 状态；不经过 Hermes 或模型。
2. 保持 Hermes 停止，在 HA UI 手动运行原生 `script.aha_lab_work_mode`，独立读回 helper 为 `on`。
3. 在 HA UI 关闭 helper，读回 `off`，再进入清理步骤。

通过条件：Hermes 停止后，HA UI 控制和原生 script 仍独立成功。记录 UI 与 script 两项结果；关闭 Hermes 但未实际操作 HA 不算通过。该测试只证明本实验 helper/script 的生命周期独立性，不证明物理设备、高可用或断网能力。

### E. 记录规则

更新 [validation](../../docs/validation/hermes-ha-lab.md)，每项只用 `not_run` / `passed` / `failed`。填写执行时间、操作者、版本、范围、最小结果与失败原因。没有运行则保持 `not_run`，不能用源码阅读或 mock/unittest 替代真实验收。只保留脱敏结果；不复制 `.env`、长效 Token、完整 HA 配置、全实体列表或原始模型对话。

只有 validation 中 I1–I14 的隔离真实联调门槛均实际 `passed` 后，才可另行请求批准接入第一盏真实 Aqara 灯；本轮软件底座完成不构成物理接入授权。Apple Home、ORVIBO、语音、跨 VLAN、自然语言长期自动化均不在本轮范围，不能因本轮 helper 实验成功而自动推进。

## 5. 恢复与退出

任何连接错误、读回不符、非预期目标或隔离条件失效时，停止交互，不重试/换目标，先在测试 HA UI 确认 helper 状态。必要时通过测试 HA UI 手动关掉 helper；仅在明确测试实例中操作。确认离线状态后修复配置/版本，再从最初读回重新验收，不保留“部分成功”作为全链路通过。

实验结束先退出该 CLI 会话（禁用插件只对后续会话生效，不能撤销正在运行的工具），再执行：

```text
hermes -p aha-lab plugins disable homeassistant
hermes -p aha-lab plugins remove homeassistant
hermes profile show aha-lab
hermes profile delete aha-lab
```

删除前再次确认 profile 名称/路径仅为本实验且无需保留的数据；不加自动确认参数。随后在测试 HA 撤销临时 Token，从本轮设置的进程环境移除 `HASS_URL`/`HASS_TOKEN`，清理本地 `.env`。若保留测试实例，手动移除本实验 package 并仅撤销本轮新增 include 配置，运行配置检查后按部署流程重新加载；不要删已有 packages 或替换全配置。删除测试实例本身需操作者另外确认准确路径/容器，不在本 runbook 提供递归删除命令。

仓库忽略 `.env*` 并例外保留 `.env.example`，但忽略规则不是保密措施，也不能隐藏已被追踪的秘密。提交前检查暂存 diff 与已追踪文件；若曾暴露 Token，优先撤销再清理历史，不能仅删文件后继续使用。

## 6. 静态核对依据与既有缺陷

核对日期：2026-10-13。下列核验只证明文档命令/字段与发布源码或官方说明相符，不证明本机部署运行：

- [v0.21.7 catalog](https://github.com/NousResearch/hermes-agent/blob/v0.21.7/plugin-catalog/homeassistant.yaml)：插件 2.0.1 与固定 SHA；不是旧研究中“内置无需安装”的路径。
- [profile parser](https://github.com/NousResearch/hermes-agent/blob/v0.21.7/hermes_cli/subcommands/profile.py)、[profiles implementation](https://github.com/NousResearch/hermes-agent/blob/v0.21.7/hermes_cli/profiles.py)：`create --no-alias --no-skills`、独立目录与 model seed 行为。
- [plugins parser](https://github.com/NousResearch/hermes-agent/blob/v0.21.7/hermes_cli/subcommands/plugins.py)、[install](https://github.com/NousResearch/hermes-agent/blob/v0.21.7/hermes_cli/plugins_cmd_install.py) 的 `cmd_install`、[catalog](https://github.com/NousResearch/hermes-agent/blob/v0.21.7/hermes_cli/plugins_cmd_catalog.py) 的 `resolve_catalog_name` / `install_catalog_entry`：live catalog 与显式 `--ref`。
- [source resolver](https://github.com/NousResearch/hermes-agent/blob/v0.21.7/hermes_cli/plugins_cmd.py) 的 `_resolve_git_url`、[git metadata](https://github.com/NousResearch/hermes-agent/blob/v0.21.7/hermes_cli/plugins_cmd_git.py) 的 `_install_metadata_path` / `_canonical_source`：`#subdir`、profile-local metadata 与完整 SHA 字段。
- [listing](https://github.com/NousResearch/hermes-agent/blob/v0.21.7/hermes_cli/plugins_cmd_listing.py)、[tools parser](https://github.com/NousResearch/hermes-agent/blob/v0.21.7/hermes_cli/subcommands/tools.py)、[config](https://github.com/NousResearch/hermes-agent/blob/v0.21.7/hermes_cli/config.py)、[chat entrypoint](https://github.com/NousResearch/hermes-agent/blob/v0.21.7/hermes_cli/main.py)：`list --json`、CLI toolset 字段和 chat。
- 插件固定 revision 的 [README](https://github.com/NousResearch/hermes-official-plugins/blob/682b22d019a1109421faa62efe43e16b23c2ebef/homeassistant/README.md)、[registration](https://github.com/NousResearch/hermes-official-plugins/blob/682b22d019a1109421faa62efe43e16b23c2ebef/homeassistant/__init__.py)、[tools](https://github.com/NousResearch/hermes-official-plugins/blob/682b22d019a1109421faa62efe43e16b23c2ebef/homeassistant/tools.py)：环境变量、toolset、事件开关、`data` 字符串与 HTTP success 局限。
- HA 官方 [packages](https://www.home-assistant.io/docs/configuration/packages/)、[input_boolean](https://www.home-assistant.io/integrations/input_boolean/)、[script](https://www.home-assistant.io/integrations/script/)：仅静态对照配置语法，未运行 HA 配置检查/启动加载。

旧 Middleware 入口 `src/middleware/main.py` 引用不存在的 `middleware.core.engine`，且 `RealHAAdapter` 仍抛出 `NotImplementedError`。本实验不绕过或修复这两项，也不以官方插件实验的成功替代旧 Middleware 验收。旧 pytest 基线当前失败于 `No module named pytest`；未安装依赖恢复其基线。独立 REST 探测器的离线 unittest 与真实 Hermes/HA 集成分别记录。

## 7. 后续拉取开发分支验证

本次只读断言增强已推送至 [codex/hermes-ha-lab](https://github.com/QZSAMA/AgentHomeAssistant/tree/codex/hermes-ha-lab) 开发分支，包含第一阶段底座；已核对的实现提交为 `4bcdbdeeba1da77ac1d005b831d3ba94caae9ec1`，交付记录见 validation E5。尚未合并 `main`。

在未来实验机器的合适目录运行以下命令；先确认目标 `AgentHomeAssistant-lab` 不存在，不覆盖已有 checkout：

```powershell
git clone --branch codex/hermes-ha-lab --single-branch https://github.com/QZSAMA/AgentHomeAssistant.git AgentHomeAssistant-lab
cd AgentHomeAssistant-lab
python -m unittest discover -s tests/ha_lab -v
```

使用 Python 3.14。拉取代码或离线通过不会安装/启动 Hermes 或 HA。之后仍需按本 runbook 人工准备隔离环境，在正确阶段运行 A 节只读命令并填写验收记录。当前真实 HA、Hermes 和新增断言的在线验收均为 `not_run`，远程推送不改变这些状态。

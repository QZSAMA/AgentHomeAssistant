# AgentHomeAssistant · Code Wiki

本文按2026-11-27仓库源码静态核对，说明软件职责、运行入口和实现边界。家庭设备、采购、网络与施工事实统一查[README](README.md)及其所链专项文档；本页不维护第二份设备清单。

## 1. 软件组成与状态

| 部分 | 已有内容 | 当前边界 |
|---|---|---|
| [只读REST探测器](scripts/ha_probe.py) | 标准库CLI、输入校验、限定GET请求、版本/实体状态断言、结构化结果 | 独立工具，不导入Middleware；不控制设备、不证明Hermes联调完成 |
| [Hermes/HA实验](examples/hermes-ha-lab/README.md) | 固定版本说明、独立profile、HA helper/script片段、人工runbook | 真实联调状态以[验收单](docs/validation/hermes-ha-lab.md)为准；不接生产设备 |
| [三维户型示例](examples/home-twin-3d/README.md) | 本机预览、模拟灯光交互、NeonPlan导入备份 | 没有真实HA连接；映射与真实控制待后续适配 |
| [Middleware](src/middleware/) | FastAPI路由、场景/别名YAML、场景引擎、规则解析器、内存状态、Mock适配器 | 开发原型；入口存在导入阻塞，真实HA适配和Hermes接入未完成 |
| [Agent包](src/agent/) | 包占位 | 没有独立Hermes启动模块；实验使用官方Hermes CLI，步骤在实验指南 |

源码和测试存在不等于服务已部署或现场验收通过。本次文档整理没有运行测试、安装依赖或连接设备。

## 2. 目录与职责

| 路径 | 用途 |
|---|---|
| [src/middleware/main.py](src/middleware/main.py) | 创建FastAPI应用，装配配置、内存状态、Mock HA与AgentBridge，挂载API |
| [src/middleware/api/v1](src/middleware/api/v1/) | 对话、场景配置、别名和状态查询路由 |
| [src/middleware/core](src/middleware/core/) | IntentRouter、SceneEngine、独立SceneParser |
| [src/middleware/adapters](src/middleware/adapters/) | HA抽象接口/Mock/真实适配占位，AgentBridge规则占位 |
| [src/middleware/internal](src/middleware/internal/) | YAML配置管理、内存状态与执行日志 |
| [config/device_aliases.yaml](config/device_aliases.yaml) · [config/scenes](config/scenes/) | Middleware的演示别名与场景数据；不是家庭资产登记 |
| [scripts/ha_probe.py](scripts/ha_probe.py) · [tests/ha_lab](tests/ha_lab/) | 独立只读探测器及离线契约测试 |
| [tests](tests/) | 另含配置管理、HA Mock、场景引擎、解析器、状态存储的单元测试 |
| [pyproject.toml](pyproject.toml) | Python版本、包依赖、可选开发依赖、入口点、测试/格式配置 |

`config/network-procurement.json`是采购资料，与Middleware的设备别名和场景配置分开；文档清理不据此删除演示配置或测试夹具。

## 3. Middleware实现

| 组件 | 现有行为 | 限制 |
|---|---|---|
| [ConfigManager](src/middleware/internal/config_manager.py) | 读写`config/scenes/*.yaml`与别名文件，内存缓存，场景增删及别名查询/更新 | 当前YAML持久化；没有SQLite用户偏好存储，也没有完整场景schema校验 |
| [SceneParser](src/middleware/core/scene_parser.py) | 按标点/连接词分句、匹配别名与正则操作，生成结构化场景 | 独立规则解析；当前AgentBridge/SceneEngine没有调用它 |
| [IntentRouter](src/middleware/core/intent_router.py) | 分发`define_scene`、`modify_scene`、`activate_scene`、`control_device`、`query_state` | 接收意图字符串与参数，不负责LLM推理 |
| [SceneEngine](src/middleware/core/scene_engine.py) | 保存/修改场景，顺序调用适配器执行操作，记录执行结果 | 当前由Mock适配器承接；不代表真实动作成功 |
| [StateStore](src/middleware/internal/state_store.py) | 内存字典保存状态，deque保存历史和执行记录 | 进程结束即丢失；未连接HA事件流或自动状态同步 |
| [MockHAAdapter](src/middleware/adapters/ha_adapter.py) | 模拟设备状态与调用日志，供开发测试 | `subscribe_events`不做实际订阅 |
| [RealHAAdapter](src/middleware/adapters/ha_adapter.py) | 定义REST/WebSocket适配方向 | 构造及方法抛`NotImplementedError`，尚不可用于真实HA |
| [AgentBridge](src/middleware/adapters/agent_bridge.py) | 按关键词生成有限意图，调用路由器并组装回复 | 未接Hermes或模型；场景定义只传description，没有连接完整解析流程 |

当前调用关系：API → AgentBridge/ConfigManager/StateStore；AgentBridge → IntentRouter → SceneEngine → MockHAAdapter。SceneParser是独立模块；HA探测器与官方插件实验也独立于这条原型链路。

### 演示实体与配置

`xiaomi_*`等实体ID出现在Mock适配器、默认别名、YAML场景和相关测试中，表示测试数据，不证明用户拥有设备或已接入HA。实体替换需要同时核对配置、Mock与测试；不能因采购方案清理而单独删掉这些记录。

现有场景文件使用`name`、`description`、`source`、`devices`字段，每个操作包含`entity_id`、`service`与可选`data`。示例见[movie_mode.yaml](config/scenes/movie_mode.yaml)和[sleep_mode.yaml](config/scenes/sleep_mode.yaml)，不在Wiki再维护一份副本。

### 已定义的API

以下路径由源码挂载规则推导，尚不是已通过启动或端到端验收的服务承诺：

| 方法与路径 | 作用 |
|---|---|
| `GET /health` | 应用存活响应 |
| `POST /api/v1/agent/chat` | 将`message`与可选`session_id`交给AgentBridge |
| `GET /api/v1/config/scenes` | 列出场景 |
| `GET /api/v1/config/scenes/{scene_name}` | 查询场景 |
| `POST /api/v1/config/scenes` | 保存场景配置 |
| `DELETE /api/v1/config/scenes/{scene_name}` | 删除场景 |
| `GET /api/v1/config/devices/aliases` | 列出别名 |
| `GET /api/v1/state/devices/{entity_id}` | 读取StateStore；没有记录时404，不直接向HA查询 |
| `GET /api/v1/state/devices/{entity_id}/history` | 查询内存状态历史 |
| `GET /api/v1/state/execution-log` | 查询场景执行记录 |

路由中的Pydantic请求模型与状态码见[API源码](src/middleware/api/v1/)。当前没有独立Web UI、SQLite数据库或Flask实现；这些不列为已完成能力。

## 4. 独立实验入口

### 只读探测器与离线测试

在仓库根目录运行：

```text
python scripts/ha_probe.py --help
python -m unittest discover -s tests/ha_lab -v
```

探测器只使用Python标准库；实验固定版本要求见[实验指南](examples/hermes-ha-lab/README.md)。离线测试通过本地夹具与模拟传输验证契约，不连接用户家中HA。

显式准备隔离测试HA及其环境变量后，才按指南运行连接探测：

```text
python scripts/ha_probe.py --entity-id input_boolean.aha_lab_light --entity-id script.aha_lab_work_mode --json
```

该脚本仅GET API、配置与显式实体；`--expect-version`可检查版本，`--expect-state entity=on/off`可检查helper状态。退出码0表示该探测范围通过，1表示响应/连接/断言失败，2表示输入或配置无效。即使返回通过，也不能推断某次Hermes请求导致状态变化；控制与回读仍须按[验收单](docs/validation/hermes-ha-lab.md)分别记录。

### 三维示例

```text
python examples/home-twin-3d/serve.py
```

访问[本机预览](http://127.0.0.1:8776/)。操作方式、模拟状态、NeonPlan文件及复验范围以[示例README](examples/home-twin-3d/README.md)和[交付核验](examples/home-twin-3d/docs/delivery-check.md)为准。

## 5. Middleware开发环境与阻塞

[pyproject.toml](pyproject.toml)声明Python≥3.10，构建后端为Hatchling；核心依赖包括FastAPI、Uvicorn、Pydantic、PyYAML、httpx、websockets和jsonschema，开发依赖在`dev`组。`ollama`仅为可选依赖，不代表已有模型集成。

需要继续开发原型时，可在独立Python环境安装包与开发依赖：

```text
python -m pip install -e ".[dev]"
```

**当前服务启动有源码阻塞**：`main.py`从不存在的`middleware.core.engine`导入IntentRouter和SceneEngine；实际类分别在`core/intent_router.py`与`core/scene_engine.py`。`middleware/__init__.py`会导入main，因此相关包导入及单元测试收集也受影响。另有两个类型检查导入沿用旧路径；本次只记录，不修改代码。

`pyproject.toml`定义的`aha-server`入口指向`middleware.main:run`，但在上述问题解决并完成启动检查前，不把它当作可用部署命令。仓库没有`requirements.txt`、`agent.hermes`启动模块或Compose部署文件。

现有Middleware单元测试包括`test_config_manager.py`、`test_ha_adapter.py`、`test_scene_engine.py`、`test_scene_parser.py`、`test_state_store.py`。解除导入阻塞后使用项目的pytest配置检查；不能用独立探测器测试结果代替这组测试或API验收。持续开发还需接通场景解析、真实适配和状态同步，再另做隔离端到端验证。

## 6. 家庭网络与保留研究

家庭网络执行[同一LAN批准设计](docs/superpowers/specs/2026-11-05-home-device-rule-routing-design.md)、[实施计划](docs/superpowers/plans/2026-11-05-home-device-rule-routing.md)及[验收单](docs/validation/home-device-rule-routing.md)，物理接线见[v1.6拓扑](docs/network-topology.md)。这些资料不由软件Mock实体决定。

[旧公司VPN工作网络需求待确认](docs/dual-router-feasibility-analysis.md)；其双子网、WireGuard与mDNS设想不作为当前家庭网络或Middleware的运行依赖。

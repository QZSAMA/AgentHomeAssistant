# Hermes Agent Home Assistant 集成调研报告

> **调研日期**：2026-06-16
> **关键发现**：Hermes Agent 原生支持 Home Assistant 集成，可大幅简化方案

---

## 一、调研结论

Hermes Agent **原生提供完整的 Home Assistant 集成**，包括：

1. **内置 HA 工具集**：开箱即用，仅需配置 `HASS_TOKEN` 和 `HASS_URL`
2. **MCP Server 集成**：通过 ha-mcp 服务器，功能更强大
3. **两种集成模式**：Tool mode（命令控制） + Event mode（事件触发）
4. **跨会话记忆系统**：三层记忆（Session / Persistent / Skill）

**这意味着我们之前设计的 Middleware 层可能需要重新评估**。

---

## 二、Hermes Agent HA 集成详情

### 2.1 两种集成路径

| 对比维度 | Hermes 内置 HA 工具 | MCP Server 集成 (ha-mcp) |
|----------|---------------------|-------------------------|
| **实现方式** | Hermes 原生支持，开箱即用 | 通过外部 MCP Server 接入 |
| **配置复杂度** | 极低（仅需 Token + URL） | 中等（需安装 MCP 服务器） |
| **功能边界** | 基础设备控制 | 自动化创建、脚本调用、历史追踪等高级能力 |
| **扩展性** | 有限 | 高（支持社区扩展） |
| **社区维护** | Hermes 官方维护 | Home Assistant 社区维护 |

### 2.2 内置 HA 工具集（4 个核心工具）

| 工具 | 功能 | 参数 |
|------|------|------|
| `ha_list_entities` | 列出实体，可按 domain/area 过滤 | `domain`, `area` |
| `ha_get_state` | 查询实体详细状态（含所有属性） | `entity_id` |
| `ha_list_services` | 列出可用服务（动作） | `domain` |
| `ha_call_service` | 调用服务控制设备 | `domain`, `service`, `entity_id`, `data` |

### 2.3 两种集成模式

**Tool Mode（工具模式）**：
- 用于直接命令和查询
- 例如："打开客厅灯"、"查询空调温度"

**Event Mode（事件模式）**：
- 设备状态变化触发 Agent 工作流
- 例如：门打开 → Agent 执行安全检查
- 需要配置 `watch_domains` / `watch_entities` / `watch_all` 过滤器

### 2.4 配置方式

```bash
# ~/.hermes/.env
HASS_TOKEN=your-long-lived-access-token
HASS_URL=http://192.168.1.100:8123  # 可选，默认 homeassistant.local:8123

# 启动 Gateway
hermes gateway
```

---

## 三、Hermes Agent 核心能力

### 3.1 三层记忆系统

| 层级 | 说明 | 存储 |
|------|------|------|
| Session Memory | 当前会话上下文 | 内存 |
| Persistent Memory | 跨会话持久记忆 | FTS5 全文搜索 + LLM 总结 |
| Skill Memory | 自动沉淀的技能 | Markdown 文件 |

**关键优势**：Hermes 会记住用户的偏好和历史行为，实现个性化控制。

### 3.2 自动技能沉淀

- 完成任务后自动创建 Skill 文件
- Skill 可被后续任务复用
- 支持手动创建和编辑自定义 Skill

**示例场景 Skill**：
```markdown
# ~/.hermes/skills/movie_mode.md

## 触发条件
用户说 "观影模式" 或 "看电影"

## 执行步骤
1. 调用 ha_call_service(domain="light", service="turn_on", entity_id="light.living_room", data={"brightness": 0})
2. 调用 ha_call_service(domain="cover", service="close_cover", entity_id="cover.living_room_curtain")
3. 调用 ha_call_service(domain="media_player", service="turn_on", entity_id="media_player.xiaomi_projector")
```

### 3.3 多平台支持

Hermes Gateway 支持 14+ 平台：

| 类别 | 平台 |
|------|------|
| 命令行 | CLI Terminal |
| 即时通讯 | Telegram, Discord, Slack, WhatsApp, Signal |
| 邮件 | Email |
| 智能家居 | Home Assistant |
| 国内平台 | 飞书, 企业微信, 微信, QQ |

**这意味着**：你可以通过 Telegram/微信等平台直接控制智能家居。

### 3.4 模型自由

支持多种 LLM 后端：

| 提供商 | 模型 |
|--------|------|
| OpenRouter | GPT-4, Claude, Llama 3, Mistral 等 |
| Anthropic | Claude 系列 |
| OpenAI | GPT 系列 |
| 国内模型 | GLM, Kimi, MiniMax 等 |
| 本地模型 | Ollama, LocalAI |

---

## 四、方案对比与建议

### 4.1 三种方案对比

| 方案 | 描述 | 开发工作量 | 灵活性 | 记忆系统 |
|------|------|------------|--------|----------|
| **A: 纯 Hermes** | 直接使用 Hermes 原生 HA 集成 | 极低 | 中 | 内置三层记忆 |
| **B: 纯 Middleware** | 自己开发完整 Middleware + Hermes 作为 LLM 后端 | 高 | 高 | 需自建 |
| **C: 混合方案** | Hermes 为主 + 仅在需要时开发自定义模块 | 中 | 高 | Hermes 内置 |

### 4.2 方案 A（纯 Hermes）的优劣

**优点**：
- ✅ 开箱即用，配置极简（仅需 Token + URL）
- ✅ 内置三层记忆系统，无需自建
- ✅ 自动技能沉淀，场景定义可自动生成
- ✅ 多平台支持（Telegram、微信等）
- ✅ 社区活跃（GitHub 10万+ Stars），更新及时
- ✅ Event Mode 支持设备状态触发 Agent 工作流

**缺点**：
- ⚠️ 场景解析能力有限（依赖 LLM 的自然语言理解）
- ⚠️ 设备别名依赖 HA 的 `friendly_name`，不够灵活
- ⚠️ 无法自定义 Scene Parser 的解析规则
- ⚠️ 状态持久化依赖 Hermes 内部机制（无法用 SQLite）

### 4.3 方案 B（纯 Middleware）的优劣

**优点**：
- ✅ 完全自定义场景解析逻辑（精确控制解析规则）
- ✅ 灵活的设备别名映射（模糊匹配、多语言支持）
- ✅ 可扩展的 API 网关（支持 Web UI）
- ✅ 状态管理可定制（SQLite + 缓存）

**缺点**：
- ❌ 开发工作量大（需开发完整 Middleware）
- ❌ 需自建记忆系统
- ❌ 需维护两套系统（Middleware + Hermes）
- ❌ 复用了 Hermes 已有的功能

### 4.4 方案 C（混合方案）- **推荐**

**核心思路**：以 Hermes Agent 原生 HA 集成为基础，仅在需要高级功能时开发自定义模块。

| 功能模块 | 使用 Hermes 内置 | 开发自定义 | 原因 |
|----------|-----------------|------------|------|
| 设备控制 | ✅ `ha_call_service` | ❌ | Hermes 内置足够 |
| 状态查询 | ✅ `ha_get_state` | ❌ | Hermes 内置足够 |
| 实体列表 | ✅ `ha_list_entities` | ❌ | Hermes 内置足够 |
| 记忆系统 | ✅ 三层记忆 | ❌ | Hermes 内置足够 |
| 技能沉淀 | ✅ 自动 Skill | ❌ | Hermes 内置足够 |
| **场景解析** | ⚠️ 依赖 LLM | ✅ 可选 | 如需精确解析规则，可开发 Scene Parser |
| **设备别名** | ⚠️ 依赖 friendly_name | ✅ 可选 | 如需模糊匹配/多语言，可开发 Alias Registry |
| **状态持久化** | ⚠️ Hermes 内部 | ✅ 可选 | 如需 SQLite 历史记录，可开发 State Store |
| **Web UI** | ❌ Hermes CLI/IM | ✅ 需要 | Hermes 无 Web UI，需开发 |

---

## 五、更新后的架构方案

### 5.1 简化后的架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户层                                    │
│   Telegram │ Discord │ Slack │ 微信 │ CLI │ Web UI（可选）       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Hermes Agent Gateway                          │
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                    内置能力                              │   │
│   │   • 三层记忆系统（Session/Persistent/Skill）             │   │
│   │   • 自动技能沉淀                                         │   │
│   │   • 多平台接入                                           │   │
│   │   • 模型切换                                             │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │               Home Assistant 工具集                      │   │
│   │   ha_list_entities │ ha_get_state │ ha_list_services     │   │
│   │   ha_call_service                                        │   │
│   │                                                          │   │
│   │   Tool Mode: 命令控制                                     │   │
│   │   Event Mode: 状态触发工作流                              │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │            可选自定义模块（如需高级功能）                  │   │
│   │   • Scene Parser（精确场景解析）                          │   │
│   │   • Alias Registry（灵活别名映射）                        │   │
│   │   • State Store（SQLite 持久化）                          │   │
│   └─────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │ REST API / WebSocket
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Home Assistant                             │
│   绿米设备 │ 欧瑞博设备 │ 投影仪 │ 暖风机 │ Apple TV             │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 更新后的开发路线图

#### 阶段 1（现在 - 2026.09）：Hermes Agent 配置与测试

| 任务 | 说明 | 依赖 |
|------|------|------|
| Hermes Agent 安装 | 安装 Hermes Agent CLI | 无 |
| Home Assistant Container | MacBook 上 Docker 部署 HA（测试用） | 无 |
| HA 生成 Token | 创建 Long-Lived Access Token | HA 部署 |
| Hermes 配置 | 配置 `HASS_TOKEN` + `HASS_URL` | HA Token |
| 测试基础控制 | 测试 ha_call_service 控制虚拟设备 | Hermes + HA |
| 测试 Skill 沉淀 | 测试场景自动生成 Skill | Hermes |
| 测试 Event Mode | 测试设备状态触发工作流 | Hermes + HA |

#### 阶段 2（2026.09 - 2026.12）：装修协调期

- 确认 Hermes Agent 满足需求，决定是否开发自定义模块
- 如需 Web UI，开始开发

#### 阶段 3（2026.12 - 2027.03）：设备接入

- Hermes Agent 连接真实 Home Assistant
- 测试真实设备控制
- 测试跨子网控制

---

## 六、具体建议

### 6.1 立即可做的工作

1. **安装 Hermes Agent**：
   ```bash
   pip install hermes-agent
   # 或
   git clone https://github.com/NousResearch/hermes-agent
   ```

2. **部署 Home Assistant Container**（测试用）：
   ```bash
   docker run -d \
     --name homeassistant \
     -p 8123:8123 \
     -v ~/.homeassistant:/config \
     homeassistant/home-assistant:stable
   ```

3. **配置 Hermes Agent HA 集成**：
   - 在 HA Profile 中生成 Long-Lived Access Token
   - 配置 `~/.hermes/.env`：
     ```
     HASS_TOKEN=eyJhbGciOi...
     HASS_URL=http://localhost:8123
     ```
   - 启动 Gateway：`hermes gateway`

4. **测试基础控制**：
   - 在 Hermes CLI 中："列出所有灯光"
   - "打开客厅灯"
   - "查询空调状态"

### 6.2 需要评估的问题

| 问题 | 评估方法 | 决策 |
|------|----------|------|
| Hermes 的场景解析是否足够精确？ | 测试自然语言场景定义 | 如不够，开发 Scene Parser |
| 设备别名是否够用？ | 测试多语言/模糊匹配 | 如不够，开发 Alias Registry |
| 状态历史是否需要 SQLite？ | 评估 Hermes 日志能力 | 如需要，开发 State Store |
| 是否需要 Web UI？ | 评估用户需求 | 如需要，开发 Web UI |

---

## 七、参考资源

- [Hermes Agent Home Assistant Integration](https://hermes-agent.ai/integrations/home-assistant)
- [Hermes Agent 官方文档](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/homeassistant)
- [ha-mcp MCP Server](https://github.com/homeassistant-ai/ha-mcp) - GitHub 3183 Stars
- [CSDN Hermes + HA 集成全攻略](https://blog.csdn.net/RickyIT/article/details/160503882)
- [Home Assistant Community Discussion](https://community.home-assistant.io/t/openclaw-hermes/1011458)
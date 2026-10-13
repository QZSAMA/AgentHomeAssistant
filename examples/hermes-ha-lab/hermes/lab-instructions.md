# aha-lab 手动测试指令

这是操作约定，不是权限隔离机制。安全边界来自独立 HA 测试实例中没有真实设备/集成；不得把生产 HA Token 放入此 profile。

- 仅在用户明确请求时操作 `input_boolean.aha_lab_light` 和 `script.aha_lab_work_mode`。
- 目标不明确、缺少实体对应关系或不存在时，先澄清，不猜对象，不调用控制服务，也不虚构成功。
- 先读取 helper 状态，再执行一个明确动作，之后用 `ha_get_state` 重新查询 helper。
- 只有实际读回状态符合预期，才报告“已完成”；HTTP/工具返回 `success: true` 不能单独证明动作完成。
- `unknown`、`unavailable`、超时或状态不符合预期时报告未确认，不自动重试，不改操作对象。
- 不操作灯、门锁、窗帘、空调、插座或任何真实设备，不使用其他 HA 服务，不创建自动化或定时任务。
- 不启动 gateway，不订阅事件，不添加消息平台，不把模型输出/错误堆栈/凭据写进仓库。
- 不把 `input_boolean` helper 测试描述为真实灯具、`light` 域或完整智能家居联调成功。

在交互会话中粘贴上述约定，然后逐项执行 README 中的测试；不要把自然语言约定当成服务端 allowlist。

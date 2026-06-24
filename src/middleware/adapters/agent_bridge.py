"""AgentBridge - Agent 适配器层，统一 Agent 接口协议。"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from middleware.core.engine import IntentRouter


class AgentBridge:
    """Agent 适配器，将 Agent 输出转换为 Intent Router 调用。

    当前为占位实现，待 Hermes Agent 集成后替换为真实 Agent 交互。
    """

    def __init__(self, intent_router: IntentRouter) -> None:
        self._router = intent_router
        self._sessions: dict[str, dict] = {}

    async def process(
        self, message: str, session_id: str | None = None
    ) -> dict:
        """处理用户消息，返回 Agent 响应。

        Args:
            message: 用户自然语言输入
            session_id: 会话 ID（可选）

        Returns:
            {"reply": str, "intent": str | None, "session_id": str}
        """
        if session_id is None:
            session_id = str(uuid.uuid4())

        # TODO: 接入 Hermes Agent 进行意图识别
        # 当前为占位逻辑，待 Agent 集成后替换
        intent, params = self._mock_intent_recognition(message)

        if intent:
            result = await self._router.route(intent, params)
            reply = self._generate_reply(intent, result)
        else:
            reply = "抱歉，我暂时无法理解您的请求。"

        return {"reply": reply, "intent": intent, "session_id": session_id}

    def _mock_intent_recognition(self, message: str) -> tuple[str | None, dict]:
        """Mock 意图识别（待 Hermes Agent 替换）。"""
        if "的意思是" in message:
            return "define_scene", {"description": message}
        if "打开" in message and "模式" in message:
            scene_name = message.replace("打开", "").replace("模式", "").strip()
            return "activate_scene", {"scene_name": scene_name + "模式"}
        if "温度" in message or "状态" in message:
            return "query_state", {"entity_id": "climate.xiaomi_heater"}
        return None, {}

    def _generate_reply(self, intent: str, result: dict) -> str:
        """根据意图和执行结果生成回复。"""
        if intent == "define_scene":
            if result.get("success"):
                return f"场景已创建成功：{result.get('scene', '')}"
            return f"场景创建失败：{result.get('error', '未知错误')}"
        if intent == "activate_scene":
            if result.get("success"):
                return "场景已执行完成，所有设备已就绪。"
            return "场景执行部分失败，请检查设备状态。"
        if intent == "query_state":
            state = result.get("state", {})
            return f"当前状态：{state}"
        return "操作完成。"

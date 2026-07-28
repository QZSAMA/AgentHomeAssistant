"""Agent API - 对话接口，接收用户自然语言输入。"""

from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

router = APIRouter()


class ChatRequest(BaseModel):
    """对话请求。"""

    message: str = Field(..., description="用户自然语言输入")
    session_id: str | None = Field(default=None, description="会话 ID")


class ChatResponse(BaseModel):
    """对话响应。"""

    reply: str = Field(..., description="Agent 回复")
    intent: str | None = Field(default=None, description="识别的意图")
    session_id: str = Field(..., description="会话 ID")


@router.post("/chat", response_model=ChatResponse)
async def chat(request: Request, body: ChatRequest) -> ChatResponse:
    """处理用户对话输入，返回 Agent 响应。"""
    agent_bridge = request.app.state.agent_bridge
    result = await agent_bridge.process(message=body.message, session_id=body.session_id)
    return ChatResponse(
        reply=result["reply"],
        intent=result.get("intent"),
        session_id=result["session_id"],
    )

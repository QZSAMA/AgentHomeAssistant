"""意图路由器 - 将 Agent 识别的意图路由到对应服务。"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from middleware.core.engine import SceneEngine


class Intent(str, Enum):
    """核心意图枚举。"""

    DEFINE_SCENE = "define_scene"
    MODIFY_SCENE = "modify_scene"
    ACTIVATE_SCENE = "activate_scene"
    CONTROL_DEVICE = "control_device"
    QUERY_STATE = "query_state"


class IntentRouter:
    """意图路由器，根据识别的意图分发到对应处理器。"""

    def __init__(self, scene_engine: SceneEngine) -> None:
        self._scene_engine = scene_engine
        self._handlers: dict[Intent, callable] = {
            Intent.DEFINE_SCENE: self._handle_define_scene,
            Intent.MODIFY_SCENE: self._handle_modify_scene,
            Intent.ACTIVATE_SCENE: self._handle_activate_scene,
            Intent.CONTROL_DEVICE: self._handle_control_device,
            Intent.QUERY_STATE: self._handle_query_state,
        }

    async def route(
        self, intent: str, params: dict
    ) -> dict:
        """路由意图到对应处理器。"""
        try:
            intent_enum = Intent(intent)
        except ValueError:
            return {"success": False, "error": f"未知意图: {intent}"}

        handler = self._handlers.get(intent_enum)
        if handler is None:
            return {"success": False, "error": f"意图 '{intent}' 无处理器"}

        return await handler(params)

    async def _handle_define_scene(self, params: dict) -> dict:
        """处理定义场景意图。"""
        return await self._scene_engine.define_scene(params)

    async def _handle_modify_scene(self, params: dict) -> dict:
        """处理修改场景意图。"""
        return await self._scene_engine.modify_scene(params)

    async def _handle_activate_scene(self, params: dict) -> dict:
        """处理激活场景意图。"""
        scene_name = params.get("scene_name", "")
        return await self._scene_engine.activate_scene(scene_name)

    async def _handle_control_device(self, params: dict) -> dict:
        """处理控制设备意图。"""
        return await self._scene_engine.control_device(params)

    async def _handle_query_state(self, params: dict) -> dict:
        """处理查询状态意图。"""
        return await self._scene_engine.query_state(params)

"""场景引擎 - 编排多设备场景执行与状态管理。"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from middleware.adapters.ha_adapter import HAAdapter
    from middleware.internal.config_manager import ConfigManager
    from middleware.internal.state_store import StateStore


class SceneEngine:
    """场景编排引擎，负责场景的定义、修改、激活和设备控制。"""

    def __init__(
        self,
        config_manager: ConfigManager,
        state_store: StateStore,
        ha_adapter: HAAdapter,
    ) -> None:
        self._config = config_manager
        self._state = state_store
        self._ha = ha_adapter

    async def define_scene(self, params: dict) -> dict:
        """定义新场景并保存配置。"""
        scene_config = {
            "name": params.get("name", ""),
            "description": params.get("description", ""),
            "source": "natural_language",
            "devices": params.get("devices", []),
        }
        self._config.save_scene(scene_config)
        return {"success": True, "scene": scene_config["name"]}

    async def modify_scene(self, params: dict) -> dict:
        """修改已有场景配置。"""
        scene_name = params.get("name", "")
        existing = self._config.get_scene(scene_name)
        if existing is None:
            return {"success": False, "error": f"场景 '{scene_name}' 不存在"}

        existing.update(params)
        self._config.save_scene(existing)
        return {"success": True, "scene": scene_name}

    async def activate_scene(self, scene_name: str) -> dict:
        """激活场景，执行所有设备操作。"""
        scene = self._config.get_scene(scene_name)
        if scene is None:
            return {"success": False, "error": f"场景 '{scene_name}' 不存在"}

        results = []
        for device_op in scene.get("devices", []):
            entity_id = device_op.get("entity_id", "")
            service = device_op.get("service", "")
            data = device_op.get("data", {})
            result = await self._ha.control_device(entity_id, service, data)
            results.append({"entity_id": entity_id, "success": result["success"]})

        self._state.record_execution(scene_name, results)
        all_success = all(r["success"] for r in results)
        return {"success": all_success, "results": results}

    async def control_device(self, params: dict) -> dict:
        """直接控制单个设备。"""
        entity_id = params.get("entity_id", "")
        service = params.get("service", "")
        data = params.get("data", {})
        return await self._ha.control_device(entity_id, service, data)

    async def query_state(self, params: dict) -> dict:
        """查询设备状态。"""
        entity_id = params.get("entity_id", "")
        state = self._ha.query_state(entity_id)
        return {"entity_id": entity_id, "state": state}

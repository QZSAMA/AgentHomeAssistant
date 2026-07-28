"""Home Assistant 适配器 - 抽象接口与 Mock 实现。"""

from __future__ import annotations

import abc
from typing import Any


class HAAdapter(abc.ABC):
    """Home Assistant 适配器抽象接口。"""

    @abc.abstractmethod
    async def control_device(
        self, entity_id: str, service: str, data: dict[str, Any]
    ) -> dict:
        """控制设备。

        Args:
            entity_id: Home Assistant Entity ID
            service: 服务名称 (如 turn_on, turn_off, close_cover)
            data: 服务参数

        Returns:
            {"success": bool, "entity_id": str, "service": str}
        """

    @abc.abstractmethod
    def query_state(self, entity_id: str) -> dict | None:
        """查询设备状态。

        Args:
            entity_id: Home Assistant Entity ID

        Returns:
            设备状态字典，或 None
        """

    @abc.abstractmethod
    async def subscribe_events(self, entity_id: str, callback: callable) -> None:
        """订阅设备状态变化事件。"""


class MockHAAdapter(HAAdapter):
    """Mock 实现，用于无 HA 环境下的开发测试。"""

    def __init__(self) -> None:
        self._mock_states: dict[str, dict] = {
            "light.living_room": {"state": "off", "brightness": 0},
            "cover.living_room_curtain": {"state": "open"},
            "media_player.xiaomi_projector": {"state": "off"},
            "climate.xiaomi_heater": {"state": "off", "temperature": 22},
            "air_quality.xiaomi_air_purifier": {"state": "off", "pm25": 15},
        }
        self._call_log: list[dict] = []

    async def control_device(
        self, entity_id: str, service: str, data: dict[str, Any]
    ) -> dict:
        """模拟设备控制。"""
        if entity_id not in self._mock_states:
            return {"success": False, "entity_id": entity_id, "error": "设备不存在"}

        state = self._mock_states[entity_id]
        if service == "turn_on":
            state["state"] = "on"
            state.update(data)
        elif service == "turn_off":
            state["state"] = "off"
        elif service == "close_cover":
            state["state"] = "closed"
        elif service == "open_cover":
            state["state"] = "open"
        elif service == "set_temperature":
            temp = data.get("temperature", 0)
            if isinstance(temp, str) and temp.startswith(("+", "-")):
                state["temperature"] += int(temp)
            else:
                state["temperature"] = int(temp)

        self._call_log.append({
            "entity_id": entity_id,
            "service": service,
            "data": data,
            "result": "success",
        })

        return {"success": True, "entity_id": entity_id, "service": service}

    def query_state(self, entity_id: str) -> dict | None:
        """查询模拟设备状态。"""
        return self._mock_states.get(entity_id)

    async def subscribe_events(self, entity_id: str, callback: callable) -> None:
        """Mock 订阅，不做实际操作。"""
        pass

    def get_call_log(self) -> list[dict]:
        """获取调用日志（测试用）。"""
        return self._call_log.copy()

    def reset(self) -> None:
        """重置 Mock 状态（测试用）。"""
        self._call_log.clear()


class RealHAAdapter(HAAdapter):
    """真实 Home Assistant 适配器（待 HA 部署后实现）。

    TODO: 待 Home Assistant 部署后，基于 httpx 实现真实 API 调用。
    - control_device: POST /api/services/{domain}/{service}
    - query_state: GET /api/states/{entity_id}
    - subscribe_events: WebSocket /api/websocket
    """

    def __init__(self, base_url: str, token: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._token = token
        raise NotImplementedError("RealHAAdapter 待 HA 部署后实现")

    async def control_device(
        self, entity_id: str, service: str, data: dict[str, Any]
    ) -> dict:
        raise NotImplementedError

    def query_state(self, entity_id: str) -> dict | None:
        raise NotImplementedError

    async def subscribe_events(self, entity_id: str, callback: callable) -> None:
        raise NotImplementedError

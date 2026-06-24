"""状态存储 - 记录设备状态与执行历史。"""

from __future__ import annotations

from collections import deque
from time import time


class StateStore:
    """内存状态存储，记录设备状态和场景执行历史。"""

    def __init__(self, max_history: int = 500) -> None:
        self._device_states: dict[str, dict] = {}
        self._device_history: dict[str, deque] = {}
        self._execution_log: deque = deque(maxlen=max_history)
        self._max_history = max_history

    def get_state(self, entity_id: str) -> dict | None:
        """获取设备当前状态。"""
        return self._device_states.get(entity_id)

    def set_state(self, entity_id: str, state: dict) -> None:
        """更新设备状态并记录历史。"""
        state_record = {**state, "timestamp": time()}
        self._device_states[entity_id] = state_record

        if entity_id not in self._device_history:
            self._device_history[entity_id] = deque(maxlen=self._max_history)
        self._device_history[entity_id].append(state_record)

    def get_history(self, entity_id: str, limit: int = 50) -> list[dict]:
        """获取设备状态历史。"""
        history = self._device_history.get(entity_id, deque())
        return list(history)[-limit:]

    def record_execution(self, scene_name: str, results: list[dict]) -> None:
        """记录场景执行日志。"""
        self._execution_log.append({
            "scene": scene_name,
            "results": results,
            "timestamp": time(),
            "success": all(r.get("success", False) for r in results),
        })

    def get_execution_log(self, limit: int = 50) -> list[dict]:
        """获取场景执行日志。"""
        return list(self._execution_log)[-limit:]

    def clear(self) -> None:
        """清空所有状态和日志。"""
        self._device_states.clear()
        self._device_history.clear()
        self._execution_log.clear()

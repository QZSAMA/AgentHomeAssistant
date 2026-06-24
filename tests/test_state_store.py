"""State Store 单元测试。"""

from __future__ import annotations

from middleware.internal.state_store import StateStore


class TestStateStore:
    """State Store 测试。"""

    def test_set_and_get_state(self):
        """测试设置和获取设备状态。"""
        store = StateStore()
        store.set_state("light.living_room", {"state": "on", "brightness": 50})

        state = store.get_state("light.living_room")
        assert state is not None
        assert state["state"] == "on"
        assert state["brightness"] == 50
        assert "timestamp" in state

    def test_get_state_not_found(self):
        """测试获取不存在的设备状态。"""
        store = StateStore()
        assert store.get_state("light.unknown") is None

    def test_history(self):
        """测试状态历史记录。"""
        store = StateStore()
        for i in range(5):
            store.set_state("light.living_room", {"state": "on", "brightness": i * 20})

        history = store.get_history("light.living_room")
        assert len(history) == 5
        assert history[0]["brightness"] == 0
        assert history[-1]["brightness"] == 80

    def test_history_limit(self):
        """测试历史记录限制。"""
        store = StateStore()
        for i in range(10):
            store.set_state("light.test", {"state": "on", "index": i})

        history = store.get_history("light.test", limit=3)
        assert len(history) == 3
        assert history[-1]["index"] == 9

    def test_execution_log(self):
        """测试执行日志记录。"""
        store = StateStore()
        store.record_execution("观影模式", [
            {"entity_id": "light.living_room", "success": True},
            {"entity_id": "cover.living_room_curtain", "success": True},
        ])

        log = store.get_execution_log()
        assert len(log) == 1
        assert log[0]["scene"] == "观影模式"
        assert log[0]["success"] is True

    def test_execution_log_with_failure(self):
        """测试执行日志记录失败情况。"""
        store = StateStore()
        store.record_execution("测试场景", [
            {"entity_id": "light.living_room", "success": True},
            {"entity_id": "cover.unknown", "success": False},
        ])

        log = store.get_execution_log()
        assert log[0]["success"] is False

    def test_clear(self):
        """测试清空存储。"""
        store = StateStore()
        store.set_state("light.test", {"state": "on"})
        store.record_execution("场景", [{"success": True}])

        store.clear()
        assert store.get_state("light.test") is None
        assert len(store.get_execution_log()) == 0

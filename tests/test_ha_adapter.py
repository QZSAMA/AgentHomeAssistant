"""MockHAAdapter 单元测试。"""

from __future__ import annotations

import pytest

from middleware.adapters.ha_adapter import MockHAAdapter


@pytest.fixture
def adapter():
    """创建 Mock 适配器。"""
    return MockHAAdapter()


class TestMockHAAdapter:
    """MockHAAdapter 测试。"""

    @pytest.mark.asyncio
    async def test_control_light_on(self, adapter):
        """测试开灯。"""
        result = await adapter.control_device("light.living_room", "turn_on", {"brightness": 50})
        assert result["success"] is True

        state = adapter.query_state("light.living_room")
        assert state["state"] == "on"
        assert state["brightness"] == 50

    @pytest.mark.asyncio
    async def test_control_light_off(self, adapter):
        """测试关灯。"""
        await adapter.control_device("light.living_room", "turn_on", {"brightness": 80})
        result = await adapter.control_device("light.living_room", "turn_off", {})
        assert result["success"] is True

        state = adapter.query_state("light.living_room")
        assert state["state"] == "off"

    @pytest.mark.asyncio
    async def test_control_cover_close(self, adapter):
        """测试关窗帘。"""
        result = await adapter.control_device("cover.living_room_curtain", "close_cover", {})
        assert result["success"] is True

        state = adapter.query_state("cover.living_room_curtain")
        assert state["state"] == "closed"

    @pytest.mark.asyncio
    async def test_control_projector_on(self, adapter):
        """测试开投影仪。"""
        result = await adapter.control_device("media_player.xiaomi_projector", "turn_on", {})
        assert result["success"] is True

        state = adapter.query_state("media_player.xiaomi_projector")
        assert state["state"] == "on"

    @pytest.mark.asyncio
    async def test_control_unknown_device(self, adapter):
        """测试控制未知设备。"""
        result = await adapter.control_device("light.unknown", "turn_on", {})
        assert result["success"] is False
        assert "error" in result

    @pytest.mark.asyncio
    async def test_set_temperature_relative(self, adapter):
        """测试相对温度调节。"""
        await adapter.control_device("climate.xiaomi_heater", "set_temperature", {"temperature": "+2"})
        state = adapter.query_state("climate.xiaomi_heater")
        assert state["temperature"] == 24  # 22 + 2

    @pytest.mark.asyncio
    async def test_call_log(self, adapter):
        """测试调用日志。"""
        await adapter.control_device("light.living_room", "turn_on", {"brightness": 50})
        await adapter.control_device("cover.living_room_curtain", "close_cover", {})

        log = adapter.get_call_log()
        assert len(log) == 2
        assert log[0]["entity_id"] == "light.living_room"
        assert log[1]["entity_id"] == "cover.living_room_curtain"

    def test_query_state(self, adapter):
        """测试查询状态。"""
        state = adapter.query_state("light.living_room")
        assert state is not None
        assert state["state"] == "off"

    def test_query_state_not_found(self, adapter):
        """测试查询不存在的设备。"""
        assert adapter.query_state("light.unknown") is None

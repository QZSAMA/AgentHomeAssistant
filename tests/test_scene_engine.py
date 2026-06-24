"""Scene Engine 单元测试。"""

from __future__ import annotations

import pytest

from middleware.adapters.ha_adapter import MockHAAdapter
from middleware.core.scene_engine import SceneEngine
from middleware.internal.config_manager import ConfigManager
from middleware.internal.state_store import StateStore


@pytest.fixture
def engine(tmp_path):
    """创建场景引擎。"""
    config_manager = ConfigManager(config_dir=str(tmp_path / "config"))
    state_store = StateStore()
    ha_adapter = MockHAAdapter()
    return SceneEngine(
        config_manager=config_manager,
        state_store=state_store,
        ha_adapter=ha_adapter,
    )


class TestSceneEngine:
    """Scene Engine 测试。"""

    @pytest.mark.asyncio
    async def test_define_scene(self, engine):
        """测试定义场景。"""
        result = await engine.define_scene({
            "name": "观影模式",
            "description": "观影环境",
            "devices": [
                {"entity_id": "light.living_room", "service": "turn_on", "data": {"brightness": 0}},
            ],
        })
        assert result["success"] is True
        assert result["scene"] == "观影模式"

    @pytest.mark.asyncio
    async def test_activate_scene(self, engine):
        """测试激活场景。"""
        await engine.define_scene({
            "name": "观影模式",
            "devices": [
                {"entity_id": "light.living_room", "service": "turn_on", "data": {"brightness": 0}},
                {"entity_id": "cover.living_room_curtain", "service": "close_cover"},
            ],
        })

        result = await engine.activate_scene("观影模式")
        assert result["success"] is True
        assert len(result["results"]) == 2

    @pytest.mark.asyncio
    async def test_activate_nonexistent_scene(self, engine):
        """测试激活不存在的场景。"""
        result = await engine.activate_scene("不存在的场景")
        assert result["success"] is False

    @pytest.mark.asyncio
    async def test_modify_scene(self, engine):
        """测试修改场景。"""
        await engine.define_scene({
            "name": "测试场景",
            "devices": [{"entity_id": "light.living_room", "service": "turn_on"}],
        })

        result = await engine.modify_scene({
            "name": "测试场景",
            "description": "更新后的描述",
        })
        assert result["success"] is True

    @pytest.mark.asyncio
    async def test_modify_nonexistent_scene(self, engine):
        """测试修改不存在的场景。"""
        result = await engine.modify_scene({"name": "不存在"})
        assert result["success"] is False

    @pytest.mark.asyncio
    async def test_control_device(self, engine):
        """测试直接控制设备。"""
        result = await engine.control_device({
            "entity_id": "light.living_room",
            "service": "turn_on",
            "data": {"brightness": 50},
        })
        assert result["success"] is True

    @pytest.mark.asyncio
    async def test_query_state(self, engine):
        """测试查询状态。"""
        result = await engine.query_state({"entity_id": "light.living_room"})
        assert result["entity_id"] == "light.living_room"
        assert result["state"] is not None

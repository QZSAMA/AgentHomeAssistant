"""Config Manager 单元测试。"""

from __future__ import annotations

import pytest

from middleware.internal.config_manager import ConfigManager


@pytest.fixture
def config_manager(tmp_path):
    """创建临时配置管理器。"""
    return ConfigManager(config_dir=str(tmp_path / "config"))


class TestConfigManager:
    """Config Manager 测试。"""

    def test_default_aliases_loaded(self, config_manager):
        """测试默认别名映射已加载。"""
        aliases = config_manager.list_device_aliases()
        assert "灯光" in aliases
        assert aliases["灯光"] == "light.living_room"
        assert "窗帘" in aliases
        assert aliases["窗帘"] == "cover.living_room_curtain"

    def test_get_entity_id(self, config_manager):
        """测试根据别名查询 Entity ID。"""
        assert config_manager.get_entity_id("灯光") == "light.living_room"
        assert config_manager.get_entity_id("不存在的别名") is None

    def test_save_and_get_scene(self, config_manager):
        """测试保存和获取场景。"""
        scene = {
            "name": "观影模式",
            "description": "自动开启观影环境",
            "source": "natural_language",
            "devices": [
                {"entity_id": "light.living_room", "service": "turn_on", "data": {"brightness": 0}},
                {"entity_id": "cover.living_room_curtain", "service": "close_cover"},
            ],
        }
        config_manager.save_scene(scene)

        loaded = config_manager.get_scene("观影模式")
        assert loaded is not None
        assert loaded["name"] == "观影模式"
        assert len(loaded["devices"]) == 2

    def test_list_scenes(self, config_manager):
        """测试列出所有场景。"""
        config_manager.save_scene({"name": "场景A", "devices": []})
        config_manager.save_scene({"name": "场景B", "devices": []})

        scenes = config_manager.list_scenes()
        assert len(scenes) == 2
        names = [s["name"] for s in scenes]
        assert "场景A" in names
        assert "场景B" in names

    def test_delete_scene(self, config_manager):
        """测试删除场景。"""
        config_manager.save_scene({"name": "待删除", "devices": []})
        assert config_manager.delete_scene("待删除") is True
        assert config_manager.get_scene("待删除") is None
        assert config_manager.delete_scene("不存在") is False

    def test_add_alias(self, config_manager):
        """测试添加新别名。"""
        config_manager.add_alias("客厅空调", "climate.living_room_ac")
        assert config_manager.get_entity_id("客厅空调") == "climate.living_room_ac"

    def test_reload(self, config_manager):
        """测试热重载。"""
        config_manager.save_scene({"name": "重载测试", "devices": []})
        config_manager.reload()
        assert config_manager.get_scene("重载测试") is not None

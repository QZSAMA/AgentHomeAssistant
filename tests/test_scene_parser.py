"""Scene Parser 单元测试。"""

from __future__ import annotations

import pytest

from middleware.core.scene_parser import SceneParser
from middleware.internal.config_manager import ConfigManager


@pytest.fixture
def parser(tmp_path):
    """创建场景解析器。"""
    config_manager = ConfigManager(config_dir=str(tmp_path / "config"))
    return SceneParser(config_manager=config_manager)


class TestSceneParser:
    """Scene Parser 测试。"""

    def test_parse_movie_mode(self, parser):
        """测试解析观影模式场景。"""
        text = "观影模式的意思是，灯光调到最暗，拉上窗帘并且打开投影仪"
        result = parser.parse(text)

        assert result["name"] == "观影模式"
        assert result["source"] == "natural_language"
        assert len(result["devices"]) == 3

        # 灯光调到最暗
        assert result["devices"][0]["entity_id"] == "light.living_room"
        assert result["devices"][0]["service"] == "turn_on"
        assert result["devices"][0]["data"]["brightness"] == 0

        # 拉上窗帘
        assert result["devices"][1]["entity_id"] == "cover.living_room_curtain"
        assert result["devices"][1]["service"] == "close_cover"

        # 打开投影仪
        assert result["devices"][2]["entity_id"] == "media_player.xiaomi_projector"
        assert result["devices"][2]["service"] == "turn_on"

    def test_parse_brightness_max(self, parser):
        """测试解析调到最亮。"""
        text = "灯光调到最亮"
        result = parser.parse(text)

        assert len(result["devices"]) == 1
        assert result["devices"][0]["data"]["brightness"] == 100

    def test_parse_temperature(self, parser):
        """测试解析温度调节。"""
        text = "调高暖风机温度"
        result = parser.parse(text)

        assert len(result["devices"]) == 1
        assert result["devices"][0]["entity_id"] == "climate.xiaomi_heater"
        assert result["devices"][0]["service"] == "set_temperature"

    def test_parse_multiple_separators(self, parser):
        """测试多种分隔符。"""
        text = "灯光调到最暗，拉上窗帘然后打开投影仪"
        result = parser.parse(text)
        assert len(result["devices"]) == 3

    def test_extract_scene_name(self, parser):
        """测试场景名称提取。"""
        text = "睡眠模式的意思是，关闭灯光"
        result = parser.parse(text)
        assert result["name"] == "睡眠模式"

    def test_parse_unknown_device(self, parser):
        """测试未知设备。"""
        text = "打开未知设备"
        result = parser.parse(text)
        assert len(result["devices"]) == 0

"""场景解析器 - 将自然语言场景描述解析为结构化 SceneConfig。"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from middleware.internal.config_manager import ConfigManager


# 操作映射规则：自然语言 → 结构化操作
OPERATION_PATTERNS: list[dict] = [
    {
        "pattern": r"(调暗|调到最暗|最暗)",
        "service": "turn_on",
        "data": {"brightness": 0},
    },
    {
        "pattern": r"(调亮|调到最亮|最亮)",
        "service": "turn_on",
        "data": {"brightness": 100},
    },
    {
        "pattern": r"(拉上窗帘|关窗帘|关闭窗帘)",
        "service": "close_cover",
        "data": {},
    },
    {
        "pattern": r"(拉开窗帘|开窗帘|打开窗帘)",
        "service": "open_cover",
        "data": {},
    },
    {
        "pattern": r"(打开投影仪|开投影|打开投影)",
        "service": "turn_on",
        "data": {},
    },
    {
        "pattern": r"(关闭投影仪|关投影|关闭投影)",
        "service": "turn_off",
        "data": {},
    },
    {
        "pattern": r"(调高温|调高温度|升高温度)",
        "service": "set_temperature",
        "data": {"temperature": "+2"},
    },
    {
        "pattern": r"(调低温|调低温度|降低温度)",
        "service": "set_temperature",
        "data": {"temperature": "-2"},
    },
    {
        "pattern": r"(打开|开启)(?!投影)",
        "service": "turn_on",
        "data": {},
    },
    {
        "pattern": r"(关闭|关)(?!投影)",
        "service": "turn_off",
        "data": {},
    },
]


class SceneParser:
    """场景解析器，将自然语言描述解析为结构化场景配置。"""

    def __init__(self, config_manager: ConfigManager) -> None:
        self._config = config_manager

    def parse(self, text: str, scene_name: str | None = None) -> dict:
        """解析自然语言场景描述。

        Args:
            text: 自然语言场景描述，如 "灯光调到最暗，拉上窗帘并且打开投影仪"
            scene_name: 可选的场景名称

        Returns:
            结构化场景配置字典
        """
        # 分割为多个操作子句
        clauses = self._split_clauses(text)

        devices = []
        for clause in clauses:
            device_op = self._parse_clause(clause)
            if device_op:
                devices.append(device_op)

        return {
            "name": scene_name or self._extract_scene_name(text) or "未命名场景",
            "description": text,
            "source": "natural_language",
            "devices": devices,
        }

    def _split_clauses(self, text: str) -> list[str]:
        """将文本分割为操作子句。"""
        # 按逗号、句号、并且、然后、并且、和 分割
        separators = r"[，,。.；;]|并且|然后|而且|以及|和"
        clauses = re.split(separators, text)
        return [c.strip() for c in clauses if c.strip()]

    def _parse_clause(self, clause: str) -> dict | None:
        """解析单个操作子句。"""
        # 查找匹配的设备别名
        alias_map = self._config.list_device_aliases()
        entity_id = self._match_device(clause, alias_map)
        if entity_id is None:
            return None

        # 查找匹配的操作
        for pattern_def in OPERATION_PATTERNS:
            if re.search(pattern_def["pattern"], clause):
                return {
                    "entity_id": entity_id,
                    "service": pattern_def["service"],
                    "data": pattern_def["data"].copy(),
                }

        return None

    def _match_device(self, clause: str, alias_map: dict) -> str | None:
        """从子句中匹配设备别名。"""
        for alias, eid in alias_map.items():
            if alias in clause:
                return eid
        return None

    def _extract_scene_name(self, text: str) -> str | None:
        """从文本中提取场景名称。"""
        # 匹配 "XXX模式的意思是" 或 "XXX的意思是"
        match = re.match(r"(.+?)(?:模式)?的意思是", text)
        if match:
            return match.group(1) + "模式"
        return None

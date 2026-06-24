"""配置管理器 - 加载、验证、管理 YAML 配置文件。"""

from __future__ import annotations

import os
from pathlib import Path

import yaml


class ConfigManager:
    """YAML 配置管理器，负责场景配置和设备别名的加载与持久化。"""

    def __init__(self, config_dir: str = "config") -> None:
        self._config_dir = Path(config_dir)
        self._scenes_dir = self._config_dir / "scenes"
        self._aliases_file = self._config_dir / "device_aliases.yaml"
        self._scenes_cache: dict[str, dict] = {}
        self._aliases_cache: dict[str, str] = {}

        self._ensure_dirs()
        self._load_all()

    def _ensure_dirs(self) -> None:
        """确保配置目录存在。"""
        self._scenes_dir.mkdir(parents=True, exist_ok=True)
        if not self._aliases_file.exists():
            self._aliases_file.write_text(
                "# 设备别名映射: 自然语言名称 -> Home Assistant Entity ID\n"
                "灯光: light.living_room\n"
                "客厅灯: light.living_room\n"
                "窗帘: cover.living_room_curtain\n"
                "客厅窗帘: cover.living_room_curtain\n"
                "投影仪: media_player.xiaomi_projector\n"
                "投影: media_player.xiaomi_projector\n"
                "暖风机: climate.xiaomi_heater\n"
                "净化器: air_quality.xiaomi_air_purifier\n"
                "空气净化器: air_quality.xiaomi_air_purifier\n",
                encoding="utf-8",
            )

    def _load_all(self) -> None:
        """加载所有配置到缓存。"""
        self._load_scenes()
        self._load_aliases()

    def _load_scenes(self) -> None:
        """加载所有场景配置。"""
        self._scenes_cache.clear()
        for yaml_file in self._scenes_dir.glob("*.yaml"):
            scene = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
            if scene and "name" in scene:
                self._scenes_cache[scene["name"]] = scene

    def _load_aliases(self) -> None:
        """加载设备别名映射。"""
        if self._aliases_file.exists():
            data = yaml.safe_load(self._aliases_file.read_text(encoding="utf-8"))
            if data:
                self._aliases_cache = data

    # ---- 场景管理 ----

    def list_scenes(self) -> list[dict]:
        """列出所有场景。"""
        return list(self._scenes_cache.values())

    def get_scene(self, name: str) -> dict | None:
        """获取指定场景。"""
        return self._scenes_cache.get(name)

    def save_scene(self, scene: dict) -> None:
        """保存场景配置到 YAML 文件。"""
        name = scene.get("name", "unnamed")
        filename = self._scenes_dir / f"{name}.yaml"
        yaml.safe_dump(scene, filename.open("w", encoding="utf-8"), allow_unicode=True)
        self._scenes_cache[name] = scene

    def delete_scene(self, name: str) -> bool:
        """删除场景。"""
        if name not in self._scenes_cache:
            return False
        filename = self._scenes_dir / f"{name}.yaml"
        if filename.exists():
            filename.unlink()
        del self._scenes_cache[name]
        return True

    # ---- 设备别名管理 ----

    def list_device_aliases(self) -> dict[str, str]:
        """列出所有设备别名映射。"""
        return self._aliases_cache.copy()

    def get_entity_id(self, alias: str) -> str | None:
        """根据别名查询 Entity ID。"""
        return self._aliases_cache.get(alias)

    def add_alias(self, alias: str, entity_id: str) -> None:
        """添加设备别名。"""
        self._aliases_cache[alias] = entity_id
        self._save_aliases()

    def _save_aliases(self) -> None:
        """持久化别名映射。"""
        yaml.safe_dump(
            self._aliases_cache,
            self._aliases_file.open("w", encoding="utf-8"),
            allow_unicode=True,
            sort_keys=True,
        )

    def reload(self) -> None:
        """重新加载所有配置（热重载）。"""
        self._load_all()

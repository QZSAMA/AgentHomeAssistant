"""Config API - 配置接口，管理设备/场景/别名。"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

router = APIRouter()


class SceneConfig(BaseModel):
    """场景配置。"""

    name: str = Field(..., description="场景名称")
    description: str = Field(default="", description="场景描述")
    source: str = Field(default="manual", description="创建来源")
    devices: list[dict] = Field(default_factory=list, description="设备操作列表")


@router.get("/scenes")
async def list_scenes(request: Request) -> list[dict]:
    """列出所有场景配置。"""
    config_manager = request.app.state.config_manager
    return config_manager.list_scenes()


@router.get("/scenes/{scene_name}")
async def get_scene(request: Request, scene_name: str) -> dict:
    """获取指定场景配置。"""
    config_manager = request.app.state.config_manager
    scene = config_manager.get_scene(scene_name)
    if scene is None:
        raise HTTPException(status_code=404, detail=f"场景 '{scene_name}' 不存在")
    return scene


@router.post("/scenes")
async def create_scene(request: Request, body: SceneConfig) -> dict:
    """创建新场景。"""
    config_manager = request.app.state.config_manager
    config_manager.save_scene(body.model_dump())
    return {"status": "ok", "scene": body.name}


@router.delete("/scenes/{scene_name}")
async def delete_scene(request: Request, scene_name: str) -> dict:
    """删除场景。"""
    config_manager = request.app.state.config_manager
    if not config_manager.delete_scene(scene_name):
        raise HTTPException(status_code=404, detail=f"场景 '{scene_name}' 不存在")
    return {"status": "ok"}


@router.get("/devices/aliases")
async def list_device_aliases(request: Request) -> dict:
    """列出所有设备别名映射。"""
    config_manager = request.app.state.config_manager
    return config_manager.list_device_aliases()

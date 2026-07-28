"""State API - 状态接口，查询设备状态和历史。"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, Request

router = APIRouter()


@router.get("/devices/{entity_id}")
async def get_device_state(request: Request, entity_id: str) -> dict:
    """查询设备当前状态。"""
    state_store = request.app.state.state_store
    state = state_store.get_state(entity_id)
    if state is None:
        raise HTTPException(status_code=404, detail=f"设备 '{entity_id}' 无状态记录")
    return state


@router.get("/devices/{entity_id}/history")
async def get_device_history(
    request: Request,
    entity_id: str,
    limit: int = Query(default=50, ge=1, le=500),
) -> list[dict]:
    """查询设备状态历史。"""
    state_store = request.app.state.state_store
    return state_store.get_history(entity_id, limit=limit)


@router.get("/execution-log")
async def get_execution_log(
    request: Request,
    limit: int = Query(default=50, ge=1, le=500),
) -> list[dict]:
    """查询场景执行日志。"""
    state_store = request.app.state.state_store
    return state_store.get_execution_log(limit=limit)

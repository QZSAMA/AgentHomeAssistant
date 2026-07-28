"""API 网关层 - 对外接口路由。"""

from __future__ import annotations

from fastapi import APIRouter

from middleware.api.v1 import agent, config, state

router = APIRouter()
router.include_router(agent.router, prefix="/agent", tags=["agent"])
router.include_router(config.router, prefix="/config", tags=["config"])
router.include_router(state.router, prefix="/state", tags=["state"])

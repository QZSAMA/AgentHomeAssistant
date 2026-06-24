"""Middleware 主入口 - FastAPI 应用与启动逻辑。"""

from __future__ import annotations

from fastapi import FastAPI

from middleware.api import router as api_router
from middleware.core.engine import IntentRouter, SceneEngine
from middleware.internal.config_manager import ConfigManager
from middleware.internal.state_store import StateStore
from middleware.adapters.ha_adapter import MockHAAdapter
from middleware.adapters.agent_bridge import AgentBridge


def create_app() -> FastAPI:
    """创建并配置 FastAPI 应用实例。"""
    app = FastAPI(
        title="AgentHomeAssistant Middleware",
        description="智能家居助理 Middleware 层 API",
        version="0.1.0",
    )

    # 初始化内部组件
    config_manager = ConfigManager(config_dir="config")
    state_store = StateStore()
    ha_adapter = MockHAAdapter()

    # 初始化核心引擎
    scene_engine = SceneEngine(
        config_manager=config_manager,
        state_store=state_store,
        ha_adapter=ha_adapter,
    )
    intent_router = IntentRouter(scene_engine=scene_engine)

    # 初始化 Agent 适配器
    agent_bridge = AgentBridge(intent_router=intent_router)

    # 注入依赖
    app.state.config_manager = config_manager
    app.state.state_store = state_store
    app.state.ha_adapter = ha_adapter
    app.state.scene_engine = scene_engine
    app.state.intent_router = intent_router
    app.state.agent_bridge = agent_bridge

    # 注册路由
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/health")
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()


def run() -> None:
    """启动 API 服务。"""
    import uvicorn

    uvicorn.run(
        "middleware.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    run()

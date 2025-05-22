"""
Endpoints implementation for Backend.
"""

from fastapi import FastAPI

##### Health check ######
from .health import HealthRouterV1

##### Property Models ######
from .openai import OpenAIRouterV1

##### Open-source Models ######
from .lgai import LGAIRouterV1
from .deepseek import DeepSeekRouterV1



__all__ = ["configure_routers"]


def configure_routers(app: FastAPI) -> FastAPI:
    routers = [
        HealthRouterV1(),
        OpenAIRouterV1(),
        LGAIRouterV1(),
        DeepSeekRouterV1(),
    ]
    for router in routers:
        router = router.configure()
        app.include_router(router)
    return app

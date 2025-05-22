"""
from .health import HealthRouterV1
# from .register import register_router
# from .apikey import apikey_router
# from .session import session_router
# from .well_known import well_known
from .v1 import v1_router

routes = [
    HealthRouterV1, 
    OpenAIRouterV1,
    # register_router, 
    # apikey_router, 
    # session_router, 
    # well_known, 
    v1_router
]

"" "
엔드포인트 구현
"""

from fastapi import FastAPI

from .health import HealthRouterV1
from .openai import OpenAIRouterV1

__all__ = ["configure_routers"]

def configure_routers(app: FastAPI) -> FastAPI:
    routers = [
        HealthRouterV1(),
        OpenAIRouterV1(),
    ]
    for router in routers:
        router = router.configure()
        app.include_router(router)
    return app

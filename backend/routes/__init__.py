from .health import health
from .register import register_router
from .apikey import apikey_router
from .session import session_router
from .well_known import well_known
from .v1 import v1_router

routes = [health, register_router, apikey_router, session_router, well_known, v1_router]

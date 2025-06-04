from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from routes import configure_routers
from utils import load_allowed_origins


app = FastAPI()

# IP/도메인 화이트리스트 미들웨어
# from fastapi import Request
# from fastapi.responses import JSONResponse
# from starlette.middleware.base import BaseHTTPMiddleware

# class OriginWhitelistMiddleware(BaseHTTPMiddleware):
#     def __init__(self, app, allowed_origins):
#         super().__init__(app)
#         self.allowed_origins = set(allowed_origins)

#     async def dispatch(self, request: Request, call_next):
#         origin = request.headers.get("origin")
#         client_host = request.client.host
#         if origin:
#             if origin not in self.allowed_origins:
#                 return JSONResponse(status_code=403, content={"detail": f"Origin '{origin}' not allowed."})
#         else:
#             # origin 헤더가 없는 모든 요청도 차단
#             return JSONResponse(status_code=403, content={"detail": "No Origin header. Request not allowed."})
#         return await call_next(request)

# allowed_origins = load_allowed_origins(raw=False)
# app.add_middleware(OriginWhitelistMiddleware, allowed_origins=allowed_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=load_allowed_origins(),  # 허용된 origin 리스트를 불러옵니다.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/_debug/app_config")
def debug_app_config():
    cors = [m.kwargs for m in app.user_middleware if m.cls.__name__ == "CORSMiddleware"]
    return {
        "user_middleware": [str(m) for m in app.user_middleware],
        "cors": cors,
        "routes": [route.path for route in app.routes],
    }

# @app.middleware("http")
# async def add_cors_headers(request, call_next):
#     response = await call_next(request)
#     response.headers["Access-Control-Allow-Origin"] = load_allowed_origins(raw=False)
#     return response

@app.get("/test")
def test_endpoint():
    msg = load_allowed_origins()
    return {"load_allowed_origins": msg}

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse, tags=["Home UI"], description="Home UI for the users who enter the base URL.")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app = configure_routers(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

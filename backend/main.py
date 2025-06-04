from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import configure_routers


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app = configure_routers(app)

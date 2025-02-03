import os
import asyncio
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi_admin.resources import Model
from fastapi_admin.site import Site
from fastapi_admin.depends import get_current_admin
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi_admin.models import AbstractAdmin
from sqlmodel import SQLModel, Field
from starlette.middleware.sessions import SessionMiddleware

DATABASE_URL = "sqlite+aiosqlite:///db/service.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Admin(AbstractAdmin, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="3800dd81f8d208a3ef387a58a07c2f6e")

@app.on_event("startup")
async def startup():
    await admin_app.init(
        admin_secret="3800dd81f8d208a3ef387a58a07c2f6e",
        site=Site(title="Admin Panel"),
        login_provider=UsernamePasswordProvider(),
    )
    app.mount("/admin", admin_app)

@app.on_event("shutdown")
async def shutdown():
    await admin_app.close()

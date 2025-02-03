from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from utils.models import User
from utils.models import get_user_db


login_router = APIRouter(prefix="/login", tags=["Login"])



class LoginRequest(BaseModel):
    username: str
    password: str


@login_router.post("/")
def login(
    request: LoginRequest,
    user_db: Session = Depends(get_user_db)
):
    user = user_db.query(User).filter(User.username == request.username, User.password == request.password).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {"message": "Login successful"}


__all__ = ["login_router"]

from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from utils.models import User, get_user_db
from utils.auth import hash_password, verify_password
from utils.session import create_access_token


register_router = APIRouter(prefix="/register", tags=["Register"])

class RegisterRequest(BaseModel):
    # Account Information
    userid: str
    password: str
    # Personal Information
    username: str
    resident_id: str

class LoginRequest(BaseModel):
    userid: str
    password: str

@register_router.post("/")
def register(
    request: RegisterRequest,
    user_db: Session = Depends(get_user_db)
):
    existing_user = user_db.query(User).filter(User.userid == request.userid).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(request.password)
    hashed_resident_id = hash_password(request.resident_id)
    new_user = User(userid=request.userid, 
                    password=hashed_password, 
                    username=request.username, 
                    resident_id=hashed_resident_id)
    user_db.add(new_user)
    user_db.commit()
    user_db.refresh(new_user)

    return {"status": "User registered successfully"}

@register_router.post("/login")
def login(request: LoginRequest, user_db: Session = Depends(get_user_db)):
    user = user_db.query(User).filter(User.userid == request.userid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # JWT 토큰 발급
    access_token = create_access_token({"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}

@register_router.get("/{userid}")
def get_user(userid: str, user_db: Session = Depends(get_user_db)):
    user = user_db.query(User).filter(User.userid == userid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.userid, "username": user.username}

@register_router.put("/{userid}")
def update_user_password(request: LoginRequest, user_db: Session = Depends(get_user_db)):
    user = user_db.query(User).filter(User.userid == request.userid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.password = hash_password(request.password)
    user_db.commit()
    
    return {"detail": "Password updated successfully"}

@register_router.delete("/{userid}")
def delete_user(request: LoginRequest, user_db: Session = Depends(get_user_db)):
    user = user_db.query(User).filter(User.userid == request.userid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user_db.delete(user)
    user_db.commit()
    
    return {"detail": "User deleted successfully"}

__all__ = ["register_router"]

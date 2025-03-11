from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import secrets

from utils.models import Service, get_service_db, User, get_user_db
from utils.auth import verify_password

apikey_router = APIRouter(prefix="/apikey", tags=["API Key"])


class APIKeyCreateRequest(BaseModel):
    userid: str
    password: str


@apikey_router.post("/")
def create_api_key(
    request: APIKeyCreateRequest,
    user_db: Session = Depends(get_user_db),
    apikey_db: Session = Depends(get_service_db)
):
    user = user_db.query(User).filter(User.userid == request.userid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    existing_apikey = apikey_db.query(Service).filter(Service.user_id == user.id).first()
    if existing_apikey:
        raise HTTPException(status_code=400, detail="API Key already exists for this user")
    
    api_key = secrets.token_hex(16)
    new_apikey = Service(user_id=user.id, api_key=api_key)
    apikey_db.add(new_apikey)
    apikey_db.commit()
    
    return {"api_key": api_key}


@apikey_router.get("/{user_id}")
def get_api_key(user_id: int, apikey_db: Session = Depends(get_service_db)):
    apikey = apikey_db.query(Service).filter(Service.user_id == user_id).first()
    if not apikey:
        raise HTTPException(status_code=404, detail="API Key not found")
    return {"api_key": apikey.api_key}


@apikey_router.put("/{user_id}")
def regenerate_api_key(user_id: int, apikey_db: Session = Depends(get_service_db)):
    apikey = apikey_db.query(Service).filter(Service.user_id == user_id).first()
    if not apikey:
        raise HTTPException(status_code=404, detail="API Key not found")
    
    new_api_key = secrets.token_hex(16)
    apikey.api_key = new_api_key
    apikey_db.commit()
    
    return {"api_key": new_api_key}


@apikey_router.delete("/{user_id}")
def delete_api_key(user_id: int, apikey_db: Session = Depends(get_service_db)):
    apikey = apikey_db.query(Service).filter(Service.user_id == user_id).first()
    if not apikey:
        raise HTTPException(status_code=404, detail="API Key not found")
    
    apikey_db.delete(apikey)
    apikey_db.commit()
    
    return {"detail": "API Key deleted successfully"}


__all__ = ["apikey_router"]

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import secrets
from datetime import datetime

from utils.models import SessionTable, User, get_user_db, get_service_db

session_router = APIRouter(prefix="/session", tags=["Session"])

@session_router.post("/login")
def login(username: str, password: str, user_db: Session = Depends(get_user_db), session_db: Session = Depends(get_service_db)):
    user = user_db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 새로운 세션 토큰 발급
    session_token = secrets.token_hex(32)
    new_session = SessionTable(user_id=user.id, session_token=session_token, created_at=datetime.utcnow())
    session_db.add(new_session)
    session_db.commit()
    
    return {"session_token": session_token}
    
@session_router.get("/validate")
def validate_session(session_token: str, session_db: Session = Depends(get_service_db)):
    session = session_db.query(SessionTable).filter(SessionTable.session_token == session_token).first()
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session token")
    return {"status": "Valid session"}

@session_router.delete("/logout")
def logout(session_token: str, session_db: Session = Depends(get_service_db)):
    session = session_db.query(SessionTable).filter(SessionTable.session_token == session_token).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session_db.delete(session)
    session_db.commit()
    return {"detail": "Session deleted"}

__all__ = ["session_router"]

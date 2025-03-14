from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .db import *


class SessionTable(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_token = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="sessions")

# 1️⃣ 사용자 정보 테이블 (users.db)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    username = Column(String, index=True)
    resident_id = Column(Integer, unique=True, index=True)
    sessions = relationship("SessionTable", back_populates="user")

# 2️⃣ Service 테이블 (service.db)
class Service(Base):
    __tablename__ = "service"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    api_key = Column(String, unique=True, index=True)
    usage_count = Column(Integer, default=100)  # API 사용 가능 횟수

# 3️⃣ 로그 테이블 (logs.db)
class LogEntry(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, ForeignKey("service.api_key"))
    action = Column(String)
    timestamp = Column(String)

# 각 데이터베이스에 테이블 생성
Base.metadata.create_all(bind=user_engine)
Base.metadata.create_all(bind=service_engine)
Base.metadata.create_all(bind=log_engine)

__all__ = ["User", "Service"]
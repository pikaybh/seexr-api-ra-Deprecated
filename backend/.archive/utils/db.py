from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# 데이터베이스 설정
USER_DB_URL = "sqlite:///db/users.db"
SERVICE_DB_URL = "sqlite:///db/service.db"
LOG_DB_URL = "sqlite:///db/logs.db"

# 각 DB에 대한 엔진 생성
user_engine = create_engine(USER_DB_URL, connect_args={"check_same_thread": False})
service_engine = create_engine(SERVICE_DB_URL, connect_args={"check_same_thread": False})
log_engine = create_engine(LOG_DB_URL, connect_args={"check_same_thread": False})

# 세션 생성
UserSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=user_engine)
ServiceSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=service_engine)
LogSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=log_engine)

# 공통 베이스 모델
Base = declarative_base()

# DB 세션 제공 함수
def get_user_db():
    db = UserSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_service_db():
    db = ServiceSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_log_db():
    db = LogSessionLocal()
    try:
        yield db
    finally:
        db.close()

__all__ = ["Base", "get_user_db", "get_service_db", "get_log_db", "user_engine", "service_engine", "log_engine"]
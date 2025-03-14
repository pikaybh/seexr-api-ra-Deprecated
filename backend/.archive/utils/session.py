import datetime
import jwt
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET", "your-default-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    """ JWT 액세스 토큰 발급 """
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    """ JWT 토큰 검증 """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # payload 안에 `sub` 키를 사용하여 사용자 정보 저장 가능
    except jwt.ExpiredSignatureError:
        return None  # 만료된 토큰
    except jwt.InvalidTokenError:
        return None  # 유효하지 않은 토큰


__all__ = ["create_access_token", "verify_access_token"]
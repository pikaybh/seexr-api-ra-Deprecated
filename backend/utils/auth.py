import bcrypt
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수에서 pepper 값 가져오기
PEPPER = os.getenv("PEPPER_SECRET")
if PEPPER is None:
    raise ValueError("PEPPER_SECRET environment variable is not set!")

def hash_password(password: str) -> str:
    """ 비밀번호에 pepper를 추가하고, bcrypt로 해싱하는 함수 """
    salted_password = (password + PEPPER).encode()  # 비밀번호 + pepper 결합
    salt = bcrypt.gensalt()  # salt 생성
    hashed_password = bcrypt.hashpw(salted_password, salt)  # bcrypt 해싱
    return hashed_password.decode()

def verify_password(password: str, hashed_password: str) -> bool:
    """ 사용자가 입력한 비밀번호 + pepper를 해싱하여 기존 해시와 비교 """
    salted_password = (password + PEPPER).encode()
    return bcrypt.checkpw(salted_password, hashed_password.encode())


__all__ = ["hash_password", "verify_password"]

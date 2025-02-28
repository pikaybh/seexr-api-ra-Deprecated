# 더 가벼운 Python 이미지 사용 (기존 langchain/langchain 이미지보다 훨씬 작음)
FROM python:3.12

# 작업 디렉토리 설정
WORKDIR /app/backend

# 의존성 파일 먼저 복사하여 Docker 캐시 활용
COPY requirements.txt /app/backend/

# 패키지 설치 (캐시 정리 포함)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . /app/backend


# OS 패키지 설치 후 캐시 정리
RUN apt-get update && apt-get install -y sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# 포트 문서용 노출 (실제 사용 시 -p 8000:8000 필요)
EXPOSE 8000

# FastAPI 실행 (최적화된 설정)
# CMD ["uvicorn", "main:app", "--reload"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]

FROM python:3.12

WORKDIR /app/backend

COPY requirements.txt /app/backend/

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /app/backend

RUN apt-get update \
    && apt-get install -y sqlite3 \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

# FastAPI 실행 (최적화된 설정)
# CMD ["uvicorn", "main:app", "--reload"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
# RUN uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2

# FROM nginx:latest
# 
# COPY nginx.conf /etc/nginx/conf.d/default.conf
# 
# COPY --from=build /app/dist /usr/share/nginx/html
# 
# # Add nginx config
# # COPY nginx.conf /temp/prod.conf
# # RUN envsubst /app < /temp/prod.conf > /etc/nginx/conf.d/default.conf
# 
# CMD ["nginx", "-g", "daemon off;"]
# 
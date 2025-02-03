# ==============================
# 1. Clone Repository (Base Image)
# ==============================
FROM python:3.12 AS base
WORKDIR /app
RUN apt-get update && apt-get install -y git
RUN git clone "https://github.com/pikaybh/fullstack-risk-assessment-vllm.git" /app

# ==============================
# 2. Build Frontend
# ==============================
FROM node:18 AS frontend-build
WORKDIR /app/frontend

# Copy frontend files from the cloned repository
COPY --from=base /app/frontend /app/frontend

# Install dependencies and build
RUN npm install
RUN npm run build

# ==============================
# 3. Build Backend
# ==============================
FROM python:3.12 AS backend-build
WORKDIR /app/backend

# Copy backend files from the cloned repository (excluding assets & db)
COPY --from=base /app/backend /app/backend

# Remove existing assets & db (they will be mounted as volumes)
RUN rm -rf /app/backend/assets /app/backend/db

# Install backend dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ==============================
# 4. Final Image (Production)
# ==============================
FROM python:3.12
WORKDIR /app

# Copy backend and frontend artifacts
COPY --from=backend-build /app/backend /app/backend
COPY --from=frontend-build /app/frontend/dist /app/backend/public

# Ensure external directories exist
RUN mkdir -p /app/backend/assets /app/backend/db

# Set assets & db as volumes to persist data outside container
VOLUME ["/app/backend/assets", "/app/backend/db"]

# Expose backend port
EXPOSE 8000

# Run the backend service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

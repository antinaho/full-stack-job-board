# FRONTEND
FROM node:20-slim AS frontend
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# BACKEND
FROM python:3.13-slim
WORKDIR /app
COPY backend/ ./backend

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./ 

COPY --from=frontend /frontend/dist ./backend/static
RUN uv sync --frozen --no-cache

EXPOSE 8080
CMD ["uv", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
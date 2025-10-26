# FRONTEND
FROM node:20-slim AS frontend
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# BACKEND
FROM python:3.13-slim
WORKDIR /backend
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY backend/ ./
COPY --from=frontend /frontend/dist ./static
RUN uv sync --frozen --no-cache

EXPOSE 8000

CMD ["/backend/.venv/bin/fastapi", "run", "main.py", "--port", "8000", "--host", "0.0.0.0"]
#CMD ["python", "-m", "fastapi_cli", "run", "main.py"]
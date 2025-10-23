FROM node:20-slim AS frontend
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.13-slim
WORKDIR /backend

RUN apt-get update && \
    apt-get install -y cron && \
    rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./

COPY --from=frontend /frontend/dist ./static

RUN echo "0 0 * * * root python /backend/web_scraping/scraper.py >> /var/log/cron.log 2>&1" > /etc/cron.d/myjob && \
    chmod 0644 /etc/cron.d/myjob

RUN echo '#!/bin/bash\n\
service cron start\n\
exec python -m fastapi_cli run main.py' > /backend/start.sh && \
    chmod +x /backend/start.sh

EXPOSE 8000

CMD ["/backend/start.sh"]
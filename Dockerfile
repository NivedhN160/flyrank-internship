# Production Multi-Stage Dockerfile for FlyRank Backend & AI Services
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt || pip install --no-cache-dir --user fastapi uvicorn pydantic httpx reportlab beautifulsoup4 cryptography

FROM python:3.11-slim AS runner

WORKDIR /app

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

COPY . .

EXPOSE 8000

CMD ["python", "run_all_capstones.py"]

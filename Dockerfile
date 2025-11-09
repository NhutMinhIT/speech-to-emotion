# ─────────────
# Base stage
# ─────────────
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# OS deps: ffmpeg (pydub), libsndfile1 (soundfile), git (optional), curl (healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg libsndfile1 git curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements trước để cache layer install
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip \
    && pip install -r /app/requirements.txt

# Copy source code
# Lưu ý: nếu models lớn, dùng volume ở compose thay vì COPY để đỡ bake vào image
COPY . /app

# Uvicorn default envs
ENV HOST=0.0.0.0 \
    PORT=8000

# ─────────────
# Dev stage
# ─────────────
FROM base AS dev
# Thêm dev tools nếu cần (watchfiles đã có trong uvicorn[standard])
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "app"]

# ─────────────
# Prod stage
# ─────────────
FROM base AS prod
# Worker và timeout có thể chỉnh bằng ENV
ENV UVICORN_WORKERS=2
EXPOSE 8000
# Healthcheck HTTP
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -fsS http://127.0.0.1:8000/healthz || exit 1

CMD ["bash", "-lc", "uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers ${UVICORN_WORKERS}"]

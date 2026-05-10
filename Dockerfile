FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

ENV PYTHONUNBUFFERED=1

# Cloud Run sets PORT at runtime — must bind to $PORT (not only a fixed 8080 in exec-form JSON).
# Use uvicorn from the synced venv; avoids “uv run” cold-start overhead/timeouts on Cloud Run.
CMD ["/bin/sh", "-c", "exec /app/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir uv

# pyproject + lock + README (HATCHNEK KELL!)
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen

# app kód
COPY mcp_server ./mcp_server

CMD ["uv", "run", "uvicorn", "mcp_server.mcp_server:app", "--host", "0.0.0.0", "--port", "8000"]

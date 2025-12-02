FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY mcp_server.py .
COPY README.md .

RUN pip install --no-cache-dir .

EXPOSE 8000

CMD ["dora-mcp-server"]

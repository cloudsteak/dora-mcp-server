# ---------
# CONFIG
# ---------

APP_NAME = mcp_server.mcp_server:app
PORT = 8000


# ---------
# UV basics
# ---------

## Sync dependencies (install venv + uv.lock alapján)
sync:
	uv sync

## Run the local dev server (auto reload)
run:
	uv run uvicorn $(APP_NAME) --host 0.0.0.0 --port $(PORT) --reload

## Run without reload (production-like local run)
run-prod:
	uv run uvicorn $(APP_NAME) --host 0.0.0.0 --port $(PORT)


# ---------
# CODE QUALITY (opcionális, de profi)
# ---------

## Format code with ruff
format:
	uv run ruff format .

## Lint code
lint:
	uv run ruff check .


# ---------
# TESTING (ha majd kell)
# ---------

test:
	uv run pytest -q


# ---------
# DOCKER
# ---------

IMAGE = dora-mcp-server:latest

docker-build:
	docker build -t $(IMAGE) .

docker-run:
	docker run --rm -p $(PORT):$(PORT) $(IMAGE)


# ---------
# CLEANUP
# ---------

clean:
	rm -rf .uv .pytest_cache __pycache__ */__pycache__

set shell := ["pwsh", "-NoLogo", "-Command"]

server := "tartuffe@192.168.0.150"
server_dir := "~/qr_generator"

# List all available recipes
help:
    @just --list

# Install all dependencies including dev group
install:
    uv sync

# Run all linters (ruff check, ty, codespell, bandit)
lint:
    uv run ruff check .
    uv run ty check
    uv run codespell
    uv run bandit -r . -c pyproject.toml -q

# Format code and auto-fix lint issues
format:
    uv run ruff format .
    uv run ruff check --fix .

# Start Flask development server
runserver:
    uv run python app.py

# Run all tests excluding slow
test:
    uv run pytest -m "not slow"

# Run only unit tests
test-unit:
    uv run pytest -m unit -v

# Run only integration tests
test-integration:
    uv run pytest -m integration -v

# Start Docker services (build)
docker-up:
    docker-compose up -d --build

# Stop Docker services
docker-down:
    docker-compose down

# Start Docker services with Traefik (local)
docker-up-traefik:
    docker-compose -f docker-compose-traefik.yml up -d --build

# Stop Docker services with Traefik (local)
docker-down-traefik:
    docker-compose -f docker-compose-traefik.yml down

# Deploy to home server: git pull + docker compose up
deploy:
    ssh {{server}} "cd {{server_dir}} && git pull && docker compose -f docker-compose-traefik.yml up -d --build"

# Stop deployment on home server
deploy-down:
    ssh {{server}} "cd {{server_dir}} && docker compose -f docker-compose-traefik.yml down"

# Stream live logs from home server
deploy-logs:
    ssh {{server}} "docker logs -f qr_web"

# Run pre-commit hooks on all files
git-precommit:
    uv run pre-commit run --all-files

# Commit with pre-commit checks and commitizen
commit:
    uv run pre-commit run && uv run cz commit

# Bump version using commitizen
git-bump:
    uv run cz bump

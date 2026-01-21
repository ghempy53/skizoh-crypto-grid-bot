# =============================================================================
# Skizoh Grid Bot v2.0 - Makefile
# =============================================================================

.PHONY: help build run stop restart logs shell test clean status

help:
	@echo ""
	@echo "Skizoh Grid Bot v2.0 Commands"
	@echo "=============================="
	@echo ""
	@echo "  make build     Build Docker image"
	@echo "  make run       Start bot in background"
	@echo "  make stop      Stop the bot"
	@echo "  make restart   Restart the bot"
	@echo "  make logs      View live logs"
	@echo "  make shell     Open shell in container"
	@echo "  make test      Test API connection"
	@echo "  make status    Show container status"
	@echo "  make clean     Remove container and image"
	@echo ""

build:
	@echo "Building Docker image..."
	DOCKER_BUILDKIT=1 docker compose build
	@docker images skizoh-grid-bot:2.0 --format "Image size: {{.Size}}"

run:
	@echo "Starting Grid Bot..."
	docker compose up -d
	@echo "Bot started! View logs: make logs"

stop:
	@echo "Stopping Grid Bot..."
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f --tail=100

shell:
	docker compose exec gridbot /bin/bash

test:
	docker compose run --rm gridbot test-api

status:
	@docker compose ps
	@echo ""
	@docker stats --no-stream skizoh-gridbot 2>/dev/null || echo "Container not running"

clean:
	docker compose down -v --rmi local 2>/dev/null || true
	@echo "Cleanup complete"

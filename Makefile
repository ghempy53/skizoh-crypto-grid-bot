# =============================================================================
# Skizoh Grid Bot - Docker Makefile
# Convenient commands for managing the bot on Raspberry Pi
# =============================================================================

.PHONY: help build run stop restart logs shell test-api tax-summary clean status

# Default target
help:
	@echo ""
	@echo "Skizoh Grid Bot - Docker Commands"
	@echo "=================================="
	@echo ""
	@echo "  make build        Build the Docker image"
	@echo "  make run          Start the bot (detached)"
	@echo "  make stop         Stop the bot"
	@echo "  make restart      Restart the bot"
	@echo "  make logs         View live logs"
	@echo "  make shell        Open shell in container"
	@echo "  make test-api     Test API connection"
	@echo "  make tax-summary  Generate tax summary"
	@echo "  make status       Show container status"
	@echo "  make clean        Remove container and image"
	@echo ""

# Build the Docker image
build:
	@echo "Building Docker image..."
	docker-compose build

# Run the bot in detached mode
run:
	@echo "Starting Grid Bot..."
	docker-compose up -d
	@echo ""
	@echo "Bot started! View logs with: make logs"

# Stop the bot
stop:
	@echo "Stopping Grid Bot..."
	docker-compose down

# Restart the bot
restart:
	@echo "Restarting Grid Bot..."
	docker-compose restart

# View live logs
logs:
	docker-compose logs -f

# Open shell in running container
shell:
	docker-compose exec gridbot /bin/bash

# Test API connection
test-api:
	docker-compose run --rm gridbot test-api

# Generate tax summary
tax-summary:
	docker-compose run --rm gridbot tax-summary $(YEAR)

# Show container status
status:
	@echo ""
	@echo "Container Status:"
	@echo "-----------------"
	@docker-compose ps
	@echo ""
	@echo "Resource Usage:"
	@echo "---------------"
	@docker stats --no-stream skizoh-gridbot 2>/dev/null || echo "Container not running"
	@echo ""

# Clean up everything
clean:
	@echo "Stopping and removing containers..."
	docker-compose down -v --rmi local
	@echo "Cleanup complete"

# Initial setup helper
setup:
	@echo "Setting up Grid Bot..."
	@mkdir -p data
	@if [ ! -f config.json ]; then \
		echo "Creating config.json from template..."; \
		cp src/priv/config.json.template config.json 2>/dev/null || \
		echo '{"api_key": "YOUR_BINANCE_US_API_KEY", "api_secret": "YOUR_BINANCE_US_API_SECRET"}' > config.json; \
		echo ""; \
		echo "⚠️  IMPORTANT: Edit config.json with your API keys!"; \
		echo ""; \
	fi
	@echo "Setup complete. Next steps:"
	@echo "  1. Edit config.json with your API credentials"
	@echo "  2. Run: make build"
	@echo "  3. Run: make test-api"
	@echo "  4. Run: make run"

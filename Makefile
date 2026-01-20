# =============================================================================
# Skizoh Grid Bot - Docker Makefile
# Optimized for Raspberry Pi deployment
# =============================================================================
#
# Quick Reference:
#   make build     - Build Docker image
#   make run       - Start bot in background
#   make logs      - View live logs
#   make status    - Show resource usage
#   make pi-health - Check Pi system health
#
# =============================================================================

.PHONY: help build run stop restart logs shell test-api tax-summary clean status \
        pi-health pi-optimize backup restore update prune monitor

# Default target
help:
	@echo ""
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║     Skizoh Grid Bot - Docker Commands (Pi Optimized)        ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "  Build & Run:"
	@echo "    make build        Build Docker image (optimized for Pi)"
	@echo "    make run          Start bot in background"
	@echo "    make stop         Stop the bot"
	@echo "    make restart      Restart the bot"
	@echo ""
	@echo "  Monitoring:"
	@echo "    make logs         View live logs"
	@echo "    make status       Show container resource usage"
	@echo "    make monitor      Continuous resource monitoring"
	@echo "    make pi-health    Check Raspberry Pi system health"
	@echo ""
	@echo "  Maintenance:"
	@echo "    make shell        Open shell in container"
	@echo "    make test-api     Test API connection"
	@echo "    make tax-summary  Generate tax report"
	@echo "    make backup       Backup data directory"
	@echo "    make prune        Clean up Docker resources"
	@echo "    make clean        Remove container and image"
	@echo ""
	@echo "  Pi Specific:"
	@echo "    make pi-optimize  Apply Pi performance optimizations"
	@echo "    make pi-temp      Show CPU temperature"
	@echo ""

# =============================================================================
# Build Commands
# =============================================================================

# Build the Docker image with BuildKit for faster builds
build:
	@echo "🔨 Building Docker image (this may take 5-15 minutes on Pi)..."
	@echo ""
	DOCKER_BUILDKIT=1 docker compose build --progress=plain
	@echo ""
	@echo "✅ Build complete!"
	@docker images skizoh-grid-bot:latest --format "Size: {{.Size}}"

# Build with no cache (clean rebuild)
build-fresh:
	@echo "🔨 Fresh build (no cache)..."
	DOCKER_BUILDKIT=1 docker compose build --no-cache --progress=plain

# =============================================================================
# Run Commands
# =============================================================================

# Run the bot in detached mode
run:
	@echo "🚀 Starting Grid Bot..."
	@docker compose up -d
	@echo ""
	@echo "✅ Bot started!"
	@echo ""
	@echo "📊 View logs with: make logs"
	@echo "📈 Check status with: make status"

# Run in foreground (for debugging)
run-fg:
	@echo "🚀 Starting Grid Bot (foreground mode)..."
	@docker compose up

# Run with specific scenario (non-interactive)
run-scenario:
	@if [ -z "$(SCENARIO)" ]; then \
		echo "Usage: make run-scenario SCENARIO=Balanced"; \
		echo ""; \
		echo "Available scenarios:"; \
		echo "  Conservative, Balanced, Aggressive, Low Volatility,"; \
		echo "  High Volatility, Micro Scalping, Swing Trading, Night Mode"; \
	else \
		echo "🚀 Starting with scenario: $(SCENARIO)"; \
		GRIDBOT_SCENARIO=$(SCENARIO) GRIDBOT_NONINTERACTIVE=true docker compose up -d; \
	fi

# Stop the bot
stop:
	@echo "🛑 Stopping Grid Bot..."
	@docker compose down
	@echo "✅ Stopped"

# Restart the bot
restart:
	@echo "🔄 Restarting Grid Bot..."
	@docker compose restart
	@echo "✅ Restarted"

# =============================================================================
# Monitoring Commands
# =============================================================================

# View live logs
logs:
	@docker compose logs -f --tail=100

# View last N lines of logs
logs-tail:
	@docker compose logs --tail=$(or $(N),50)

# Search logs for errors
logs-errors:
	@echo "🔍 Searching for errors in logs..."
	@docker compose logs 2>&1 | grep -i "error\|failed\|exception" | tail -20 || echo "No errors found"

# Show container status with resource usage
status:
	@echo ""
	@echo "═══════════════════════════════════════════════════════════════"
	@echo "                    CONTAINER STATUS"
	@echo "═══════════════════════════════════════════════════════════════"
	@docker compose ps
	@echo ""
	@echo "═══════════════════════════════════════════════════════════════"
	@echo "                    RESOURCE USAGE"
	@echo "═══════════════════════════════════════════════════════════════"
	@docker stats --no-stream skizoh-gridbot 2>/dev/null || echo "Container not running"
	@echo ""

# Continuous monitoring (updates every 5 seconds)
monitor:
	@echo "📊 Monitoring resources (Ctrl+C to stop)..."
	@watch -n 5 'docker stats --no-stream skizoh-gridbot 2>/dev/null && echo "" && df -h /home | tail -1'

# =============================================================================
# Utility Commands
# =============================================================================

# Open shell in running container
shell:
	@docker compose exec gridbot /bin/bash

# Test API connection
test-api:
	@echo "🔌 Testing API connection..."
	@docker compose run --rm gridbot test-api

# Generate tax summary
tax-summary:
	@echo "📊 Generating tax summary..."
	@docker compose run --rm gridbot tax-summary $(YEAR)

# =============================================================================
# Pi-Specific Commands
# =============================================================================

# Check Pi system health
pi-health:
	@echo ""
	@echo "═══════════════════════════════════════════════════════════════"
	@echo "                RASPBERRY PI HEALTH CHECK"
	@echo "═══════════════════════════════════════════════════════════════"
	@echo ""
	@echo "🌡️  CPU Temperature:"
	@vcgencmd measure_temp 2>/dev/null || echo "   (vcgencmd not available)"
	@echo ""
	@echo "📊 Memory Usage:"
	@free -h | head -2
	@echo ""
	@echo "💾 Disk Usage:"
	@df -h / | tail -1
	@echo ""
	@echo "🔧 CPU Governor:"
	@cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null || echo "   (not available)"
	@echo ""
	@echo "📈 Load Average:"
	@uptime
	@echo ""
	@echo "🐳 Docker Status:"
	@docker system df 2>/dev/null
	@echo ""

# Show CPU temperature only
pi-temp:
	@vcgencmd measure_temp 2>/dev/null || echo "vcgencmd not available"

# Apply Pi performance optimizations (run once)
pi-optimize:
	@echo "🔧 Applying Raspberry Pi optimizations..."
	@echo ""
	@echo "1. Setting CPU governor to 'ondemand'..."
	@echo "ondemand" | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null || true
	@echo ""
	@echo "2. Reducing swap usage..."
	@echo 10 | sudo tee /proc/sys/vm/swappiness 2>/dev/null || true
	@echo ""
	@echo "3. Enabling Docker to start on boot..."
	@sudo systemctl enable docker 2>/dev/null || true
	@echo ""
	@echo "✅ Optimizations applied!"
	@echo ""
	@echo "Note: For persistent settings, add to /etc/sysctl.conf:"
	@echo "  vm.swappiness=10"

# =============================================================================
# Maintenance Commands
# =============================================================================

# Backup data directory
backup:
	@echo "📦 Creating backup..."
	@mkdir -p backups
	@tar -czvf backups/gridbot-backup-$$(date +%Y%m%d_%H%M%S).tar.gz data/ config.json 2>/dev/null || \
		tar -czvf backups/gridbot-backup-$$(date +%Y%m%d_%H%M%S).tar.gz data/
	@echo "✅ Backup created in backups/"
	@ls -la backups/*.tar.gz | tail -1

# Restore from backup
restore:
	@if [ -z "$(BACKUP)" ]; then \
		echo "Usage: make restore BACKUP=backups/gridbot-backup-YYYYMMDD_HHMMSS.tar.gz"; \
		echo ""; \
		echo "Available backups:"; \
		ls -la backups/*.tar.gz 2>/dev/null || echo "  No backups found"; \
	else \
		echo "🔄 Restoring from $(BACKUP)..."; \
		make stop; \
		tar -xzvf $(BACKUP); \
		echo "✅ Restore complete"; \
	fi

# Clean up Docker resources (prune)
prune:
	@echo "🧹 Cleaning up Docker resources..."
	@docker system prune -f
	@echo ""
	@echo "💾 Space recovered:"
	@docker system df

# Remove container and image completely
clean:
	@echo "🗑️  Removing container and image..."
	@docker compose down -v --rmi local 2>/dev/null || true
	@echo "✅ Cleanup complete"

# Update bot (pull latest and rebuild)
update:
	@echo "🔄 Updating Grid Bot..."
	@git pull 2>/dev/null || echo "⚠️  Not a git repository, skipping pull"
	@make stop
	@make build
	@make run
	@echo "✅ Update complete!"

# =============================================================================
# Setup Commands
# =============================================================================

# Initial setup helper
setup:
	@echo "🔧 Setting up Grid Bot..."
	@echo ""
	@mkdir -p data backups
	@if [ ! -f config.json ]; then \
		echo "📝 Creating config.json from template..."; \
		cp src/priv/config.json.template config.json 2>/dev/null || \
		echo '{"api_key": "YOUR_BINANCE_US_API_KEY", "api_secret": "YOUR_BINANCE_US_API_SECRET", "symbol": "ETH/USDT"}' > config.json; \
		chmod 600 config.json; \
		echo ""; \
		echo "⚠️  IMPORTANT: Edit config.json with your API keys!"; \
		echo "   nano config.json"; \
		echo ""; \
	else \
		echo "✅ config.json already exists"; \
	fi
	@echo "Setup complete! Next steps:"
	@echo "  1. Edit config.json with your API credentials"
	@echo "  2. Run: make build"
	@echo "  3. Run: make test-api"
	@echo "  4. Run: make run"

# Check if everything is configured correctly
check:
	@echo "🔍 Checking configuration..."
	@echo ""
	@echo "Config file:"
	@test -f config.json && echo "  ✅ config.json exists" || echo "  ❌ config.json missing"
	@test -f config.json && (grep -q "YOUR_" config.json && echo "  ❌ API keys not configured" || echo "  ✅ API keys configured")
	@echo ""
	@echo "Docker:"
	@docker --version >/dev/null 2>&1 && echo "  ✅ Docker installed" || echo "  ❌ Docker not installed"
	@docker compose version >/dev/null 2>&1 && echo "  ✅ Docker Compose installed" || echo "  ❌ Docker Compose not installed"
	@echo ""
	@echo "Directories:"
	@test -d data && echo "  ✅ data/ exists" || echo "  ⚠️  data/ will be created"
	@test -d src && echo "  ✅ src/ exists" || echo "  ❌ src/ missing"
	@echo ""

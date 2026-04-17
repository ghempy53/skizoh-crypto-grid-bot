#!/bin/bash

##############################################################################
# Skizoh Grid Bot v2.0 - Docker Helper Script for Raspberry Pi
# Comprehensive Docker management with diagnostics and troubleshooting
# Usage: ./docker-helper.sh [command] [options]
##############################################################################

set -euo pipefail

# Color codes for pretty output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Configuration - must match docker-compose.yml
SCRIPT_VERSION="2.0.0"
CONTAINER_NAME="skizoh-gridbot"
IMAGE_NAME="skizoh-grid-bot"
IMAGE_TAG="2.0"
COMPOSE_FILE="docker-compose.yml"
SERVICE_NAME="gridbot"
CONFIG_FILE="./src/priv/config.json"
CONFIG_TEMPLATE="./src/priv/config.json.template"
DATA_DIR="./data"
BACKUP_DIR="./backups"

# BuildKit is deliberately NOT forced on here. On Raspberry Pi OS Lite with
# IPv6 disabled, BuildKit's internal Go resolver ignores /etc/gai.conf and
# fails to fall back from AAAA → A when the kernel rejects IPv6 sockets,
# producing "address family not supported by protocol" errors during pulls.
# The legacy builder (dockerd's built-in) handles this correctly.
#
# Users on networks with working IPv6 can override by running:
#   DOCKER_BUILDKIT=1 ./docker-helper.sh build
#
# fix-ipv6 also sets {"features": {"buildkit": false}} in daemon.json so
# the daemon default matches.
export DOCKER_BUILDKIT="${DOCKER_BUILDKIT:-0}"

# Ensure we run from the script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

##############################################################################
# Helper Functions
##############################################################################

print_header() {
    echo ""
    echo -e "${CYAN}+==============================================================+${NC}"
    echo -e "${CYAN}|${NC}     ${BOLD}${BLUE}SKIZOH GRID BOT v2.0 - DOCKER HELPER${NC}                    ${CYAN}|${NC}"
    echo -e "${CYAN}+==============================================================+${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_section() {
    echo ""
    echo -e "${BOLD}${BLUE}─── $1 ───${NC}"
}

print_step() {
    echo -e "${MAGENTA}→${NC} $1"
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        echo ""
        echo "  Try: sudo systemctl start docker"
        exit 1
    fi
}

# Check if docker compose is available
check_compose() {
    if ! docker compose version > /dev/null 2>&1; then
        print_error "Docker Compose (v2) is not available."
        echo ""
        echo "  Install: sudo apt install docker-compose-plugin"
        exit 1
    fi
}

# Check if container exists
container_exists() {
    docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"
}

# Check if container is running
container_running() {
    docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"
}

# Validate config.json
validate_config() {
    local errors=0

    # Check config file exists
    if [[ ! -f "$CONFIG_FILE" ]] || [[ -d "$CONFIG_FILE" ]]; then
        print_error "Config file not found: $CONFIG_FILE"
        if [[ -f "$CONFIG_TEMPLATE" ]]; then
            echo "  Create from template:"
            echo "    cp $CONFIG_TEMPLATE $CONFIG_FILE"
            echo "    chmod 600 $CONFIG_FILE"
            echo "    nano $CONFIG_FILE  # Add your API keys"
        fi
        return 1
    fi

    # Check if config file is empty (Docker bind mount of missing file creates empty file)
    if [[ ! -s "$CONFIG_FILE" ]]; then
        print_error "Config file is empty: $CONFIG_FILE"
        echo "  This usually happens when Docker auto-creates the file."
        if [[ -f "$CONFIG_TEMPLATE" ]]; then
            echo "  Fix: cp $CONFIG_TEMPLATE $CONFIG_FILE && chmod 600 $CONFIG_FILE"
        fi
        return 1
    fi

    # Validate JSON syntax
    if command -v python3 &> /dev/null; then
        if ! python3 -c "import json; json.load(open('$CONFIG_FILE'))" 2>/dev/null; then
            print_error "Invalid JSON in $CONFIG_FILE"
            errors=1
        fi
    elif command -v jq &> /dev/null; then
        if ! jq empty "$CONFIG_FILE" 2>/dev/null; then
            print_error "Invalid JSON in $CONFIG_FILE"
            errors=1
        fi
    else
        print_warning "Cannot validate JSON (install python3 or jq)"
    fi

    # Check API key
    local api_key=""
    if command -v python3 &> /dev/null; then
        api_key=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('api_key', ''))" 2>/dev/null || echo "")
    elif command -v jq &> /dev/null; then
        api_key=$(jq -r '.api_key // ""' "$CONFIG_FILE" 2>/dev/null || echo "")
    fi

    if [[ "$api_key" == "YOUR_BINANCE_US_API_KEY" || -z "$api_key" ]]; then
        print_warning "api_key is not configured in $CONFIG_FILE"
        errors=1
    fi

    # Check API secret
    local api_secret=""
    if command -v python3 &> /dev/null; then
        api_secret=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('api_secret', ''))" 2>/dev/null || echo "")
    elif command -v jq &> /dev/null; then
        api_secret=$(jq -r '.api_secret // ""' "$CONFIG_FILE" 2>/dev/null || echo "")
    fi

    if [[ "$api_secret" == "YOUR_BINANCE_US_API_SECRET" || -z "$api_secret" ]]; then
        print_warning "api_secret is not configured in $CONFIG_FILE"
        errors=1
    fi

    # Check file permissions
    local perms=""
    if [[ "$(uname)" == "Darwin" ]]; then
        perms=$(stat -f "%Lp" "$CONFIG_FILE" 2>/dev/null || echo "")
    else
        perms=$(stat -c "%a" "$CONFIG_FILE" 2>/dev/null || echo "")
    fi

    if [[ -n "$perms" && "$perms" != "600" ]]; then
        print_warning "Config file permissions are $perms (should be 600)"
        echo "  Fix: chmod 600 $CONFIG_FILE"
    fi

    if [[ $errors -eq 1 ]]; then
        return 1
    fi
    return 0
}

# Check system resources
check_resources() {
    print_info "System Resources:"

    # Memory
    if command -v free &> /dev/null; then
        local total_mem avail_mem
        total_mem=$(free -m | awk '/^Mem:/{print $2}')
        avail_mem=$(free -m | awk '/^Mem:/{print $7}')
        echo "  Memory: ${avail_mem}MB available / ${total_mem}MB total"

        if [[ $avail_mem -lt 256 ]]; then
            print_warning "Very low memory! Grid bot needs at least 128MB."
        fi
    fi

    # Disk space
    local disk_avail
    disk_avail=$(df -h . | awk 'NR==2 {print $4}')
    echo "  Disk: ${disk_avail} available"

    # CPU
    if command -v nproc &> /dev/null; then
        echo "  CPUs: $(nproc)"
    fi

    # CPU temperature (Raspberry Pi)
    if [[ -f /sys/class/thermal/thermal_zone0/temp ]]; then
        local temp_raw temp_c
        temp_raw=$(cat /sys/class/thermal/thermal_zone0/temp)
        temp_c=$((temp_raw / 1000))
        echo "  CPU Temp: ${temp_c}°C"
        if [[ $temp_c -gt 80 ]]; then
            print_warning "CPU temperature is high! Consider adding a heatsink/fan."
        fi
    fi

    # Pi model detection
    if [[ -f /proc/cpuinfo ]]; then
        local pi_model
        pi_model=$(grep -i "model" /proc/cpuinfo | tail -1 | cut -d: -f2 | xargs 2>/dev/null || echo "")
        if [[ -n "$pi_model" ]]; then
            echo "  Model: $pi_model"
        fi
    fi
}

##############################################################################
# Commands
##############################################################################

# Show help
cmd_help() {
    print_header
    echo "Usage: $0 <command> [options]"
    echo ""
    echo -e "${CYAN}Basic Operations:${NC}"
    echo "  build              Build the Docker image"
    echo "  build-verbose      Build with full output (no cache)"
    echo "  start              Start the bot container"
    echo "  stop               Stop the bot container"
    echo "  restart            Restart the bot container"
    echo "  rebuild            Full rebuild (stop, build --no-cache, start)"
    echo ""
    echo -e "${CYAN}Monitoring:${NC}"
    echo "  logs               Follow container logs (live)"
    echo "  logs-tail [N]      Show last N log lines (default: 50)"
    echo "  logs-error         Show only error/exception lines"
    echo "  status             Container status and resource usage"
    echo "  health             Healthcheck status details"
    echo "  stats              Live resource monitoring"
    echo ""
    echo -e "${CYAN}Bot Commands:${NC}"
    echo "  test-api           Test Binance.US API connection"
    echo "  tax-summary [args] Generate tax report"
    echo ""
    echo -e "${CYAN}Maintenance:${NC}"
    echo "  shell              Open bash shell in container"
    echo "  exec <cmd>         Run command in container"
    echo "  backup             Backup data, config, and compose file"
    echo "  clean              Remove container and image"
    echo "  clean-all          Remove ALL Docker artifacts (nuclear)"
    echo "  update             Pull latest code and rebuild"
    echo ""
    echo -e "${CYAN}Troubleshooting:${NC}"
    echo "  diagnose           Run full system diagnostics"
    echo "  fix-ipv6           Fix Docker IPv6 connectivity issues"
    echo "  fix-permissions    Fix file permissions"
    echo "  validate           Validate configuration and prerequisites"
    echo ""
    echo -e "${CYAN}Other:${NC}"
    echo "  version            Show version information"
    echo "  help               Show this help message"
    echo ""
}

# Build image
cmd_build() {
    print_header
    print_section "Building Grid Bot"

    validate_config || print_warning "Continuing anyway, but bot may fail to start..."
    echo ""

    print_step "Building with Docker BuildKit..."
    docker compose -f "$COMPOSE_FILE" build
    local build_status=$?

    printf "\n"
    stty sane 2>/dev/null || true

    if [[ $build_status -eq 0 ]]; then
        print_success "Build completed!"
        docker images "${IMAGE_NAME}:${IMAGE_TAG}" --format "  Image: {{.Repository}}:{{.Tag}} | Size: {{.Size}}" 2>/dev/null || true
        echo ""
    else
        print_warning "BuildKit build failed, trying without BuildKit..."
        DOCKER_BUILDKIT=0 docker compose -f "$COMPOSE_FILE" build
        build_status=$?

        printf "\n"
        stty sane 2>/dev/null || true

        if [[ $build_status -eq 0 ]]; then
            print_success "Build completed!"
            echo ""
        else
            print_error "Build failed! Check the error messages above."
            echo ""
            echo "  Common fixes:"
            echo "    $0 diagnose     Run diagnostics"
            echo "    $0 fix-ipv6     Fix IPv6 issues"
            echo "    journalctl -u docker -n 50   Check Docker logs"
            exit 1
        fi
    fi
}

# Build with verbose output
cmd_build_verbose() {
    print_header
    print_section "Building Grid Bot (verbose)"

    validate_config || print_warning "Continuing anyway..."
    echo ""

    # --progress=plain is BuildKit-only; only pass it when BuildKit is on.
    local progress_flag=()
    if [[ "${DOCKER_BUILDKIT:-0}" == "1" ]]; then
        progress_flag=(--progress=plain)
    fi

    docker compose -f "$COMPOSE_FILE" build --no-cache "${progress_flag[@]}"
    local build_status=$?

    printf "\n"
    stty sane 2>/dev/null || true

    if [[ $build_status -eq 0 ]]; then
        print_success "Build completed!"
        docker images "${IMAGE_NAME}:${IMAGE_TAG}" --format "  Image: {{.Repository}}:{{.Tag}} | Size: {{.Size}}" 2>/dev/null || true
        echo ""
    else
        print_error "Build failed!"
        echo ""
        echo "  If the error mentions IPv6 ('address family not supported by"
        echo "  protocol'), run: $0 fix-ipv6 && sudo reboot"
        exit 1
    fi
}

# Start container
cmd_start() {
    print_header
    print_section "Starting Grid Bot"

    # Auto-create config from template if missing
    if [[ ! -f "$CONFIG_FILE" || -d "$CONFIG_FILE" ]]; then
        if [[ -d "$CONFIG_FILE" ]]; then
            # Docker may have created a directory for the missing bind mount
            print_warning "Removing empty directory at $CONFIG_FILE (created by Docker)"
            rmdir "$CONFIG_FILE" 2>/dev/null || rm -rf "$CONFIG_FILE"
        fi

        if [[ -f "$CONFIG_TEMPLATE" ]]; then
            print_info "Config file not found. Creating from template..."
            cp "$CONFIG_TEMPLATE" "$CONFIG_FILE"
            chmod 600 "$CONFIG_FILE"
            print_success "Created $CONFIG_FILE from template"
            echo ""
            print_warning "You MUST edit the config with your Binance.US API keys before the bot will work:"
            echo ""
            echo "    nano $CONFIG_FILE"
            echo ""
            echo "  Replace these placeholders:"
            echo "    YOUR_BINANCE_US_API_KEY    -> your actual API key"
            echo "    YOUR_BINANCE_US_API_SECRET -> your actual API secret"
            echo ""
            exit 1
        fi
    fi

    # Handle empty config file (created by Docker bind mount of missing file)
    if [[ -f "$CONFIG_FILE" && ! -s "$CONFIG_FILE" ]]; then
        print_warning "Config file is empty (likely auto-created by Docker)."
        if [[ -f "$CONFIG_TEMPLATE" ]]; then
            print_info "Replacing with template..."
            cp "$CONFIG_TEMPLATE" "$CONFIG_FILE"
            chmod 600 "$CONFIG_FILE"
            print_success "Replaced empty config with template"
            echo ""
            print_warning "You MUST edit the config with your Binance.US API keys before the bot will work:"
            echo ""
            echo "    nano $CONFIG_FILE"
            echo ""
            exit 1
        fi
    fi

    if ! validate_config; then
        print_error "Cannot start without proper configuration."
        exit 1
    fi
    echo ""

    docker compose -f "$COMPOSE_FILE" up -d

    echo ""
    print_success "Grid Bot started!"
    echo ""

    # Wait and check if container stays running
    sleep 3
    if container_running; then
        print_info "Container is running. Initial logs:"
        echo ""
        docker compose -f "$COMPOSE_FILE" logs --tail=20
        echo ""
        echo "  View full logs: $0 logs"
    else
        print_error "Container stopped unexpectedly!"
        echo ""
        echo "  Recent logs:"
        docker compose -f "$COMPOSE_FILE" logs --tail=50
        echo ""
        echo "  Run '$0 diagnose' for troubleshooting."
        exit 1
    fi
}

# Stop container
cmd_stop() {
    print_header
    print_step "Stopping Grid Bot..."

    docker compose -f "$COMPOSE_FILE" down
    print_success "Grid Bot stopped!"
}

# Restart container
cmd_restart() {
    print_header
    print_step "Restarting Grid Bot..."

    docker compose -f "$COMPOSE_FILE" restart

    sleep 3
    if container_running; then
        print_success "Grid Bot restarted!"
        echo ""
        echo "  View logs: $0 logs"
    else
        print_error "Container failed to restart!"
        docker compose -f "$COMPOSE_FILE" logs --tail=30
        exit 1
    fi
}

# Rebuild from scratch
cmd_rebuild() {
    print_header
    print_section "Rebuilding Grid Bot from scratch"

    print_step "Stopping container..."
    docker compose -f "$COMPOSE_FILE" down --remove-orphans 2>/dev/null || true

    print_step "Removing old image..."
    docker rmi "${IMAGE_NAME}:${IMAGE_TAG}" 2>/dev/null || true

    print_step "Cleaning build cache..."
    docker builder prune -f --filter "until=1h" 2>/dev/null || true

    echo ""
    cmd_build_verbose
    echo ""
    cmd_start
}

# Show logs (follow)
cmd_logs() {
    docker compose -f "$COMPOSE_FILE" logs -f --tail=100
}

# Show last N lines
cmd_logs_tail() {
    local lines="${1:-50}"
    docker compose -f "$COMPOSE_FILE" logs --tail="$lines"
}

# Show error logs
cmd_logs_error() {
    print_header
    print_section "Error Logs"
    docker compose -f "$COMPOSE_FILE" logs --tail=500 2>&1 \
        | grep -iE "(error|exception|fatal|traceback|fail|crash)" \
        || echo "  No error logs found in last 500 lines."
}

# Show status
cmd_status() {
    print_header
    print_section "Container Status"
    docker compose -f "$COMPOSE_FILE" ps
    echo ""

    if container_running; then
        print_section "Resource Usage"
        docker stats "$CONTAINER_NAME" --no-stream --format \
            "  Memory: {{.MemUsage}}\n  CPU: {{.CPUPerc}}\n  Network: {{.NetIO}}" 2>/dev/null \
            || echo "  Stats not available"
        echo ""

        print_section "Uptime"
        docker inspect --format='  Started: {{.State.StartedAt}}' "$CONTAINER_NAME" 2>/dev/null || true
    else
        print_warning "Container is not running"
    fi
}

# Show health status
cmd_health() {
    print_header
    print_section "Health Check"

    if container_running; then
        print_success "Container is running"

        local status health
        status=$(docker inspect --format='{{.State.Status}}' "$CONTAINER_NAME" 2>/dev/null || echo "unknown")
        echo "  Status: $status"

        health=$(docker inspect --format='{{.State.Health.Status}}' "$CONTAINER_NAME" 2>/dev/null || echo "not configured")
        echo "  Health: $health"

        # Last health check output
        local last_check
        last_check=$(docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' "$CONTAINER_NAME" 2>/dev/null | tail -1)
        if [[ -n "$last_check" ]]; then
            echo "  Last check: $last_check"
        fi

        # Failing streak
        local failing
        failing=$(docker inspect --format='{{.State.Health.FailingStreak}}' "$CONTAINER_NAME" 2>/dev/null || echo "0")
        echo "  Failing streak: $failing"
    else
        print_error "Container is not running"
    fi

    echo ""
    print_section "Resource Usage"
    if container_running; then
        docker stats "$CONTAINER_NAME" --no-stream --format \
            "  Memory: {{.MemUsage}}\n  CPU: {{.CPUPerc}}\n  Network: {{.NetIO}}" 2>/dev/null \
            || echo "  Stats not available"
    else
        echo "  Container not running"
    fi

    echo ""
    check_resources
}

# Live stats
cmd_stats() {
    docker stats "$CONTAINER_NAME"
}

# Test API connection
cmd_test_api() {
    print_header
    print_section "Testing API Connection"

    if ! validate_config; then
        print_error "Cannot test without valid configuration."
        exit 1
    fi
    echo ""

    docker compose -f "$COMPOSE_FILE" run --rm "$SERVICE_NAME" test-api
}

# Generate tax summary
cmd_tax_summary() {
    print_header
    print_section "Generating Tax Summary"

    docker compose -f "$COMPOSE_FILE" run --rm "$SERVICE_NAME" tax-summary "$@"
}

# Open shell in container
cmd_shell() {
    if ! container_running; then
        print_error "Container is not running. Start it first: $0 start"
        exit 1
    fi
    docker compose -f "$COMPOSE_FILE" exec "$SERVICE_NAME" /bin/bash
}

# Execute command in container
cmd_exec() {
    if ! container_running; then
        print_error "Container is not running. Start it first: $0 start"
        exit 1
    fi

    if [[ $# -eq 0 ]]; then
        print_error "No command specified."
        echo "  Usage: $0 exec <command>"
        exit 1
    fi

    docker compose -f "$COMPOSE_FILE" exec "$SERVICE_NAME" "$@"
}

# Backup data and config
cmd_backup() {
    print_header
    print_section "Creating Backup"

    local timestamp backup_file
    timestamp=$(date +%Y%m%d_%H%M%S)
    backup_file="${BACKUP_DIR}/skizoh-gridbot-backup-${timestamp}.tar.gz"

    mkdir -p "$BACKUP_DIR"

    # Build list of paths to back up
    local paths=()
    if [[ -d "$DATA_DIR" ]]; then
        paths+=("$DATA_DIR")
        print_success "Including data/"
    fi
    if [[ -f "$CONFIG_FILE" ]]; then
        paths+=("$CONFIG_FILE")
        print_success "Including src/priv/config.json"
    fi
    if [[ -f "$COMPOSE_FILE" ]]; then
        paths+=("$COMPOSE_FILE")
        print_success "Including docker-compose.yml"
    fi

    if [[ ${#paths[@]} -eq 0 ]]; then
        print_warning "Nothing to back up!"
        return 1
    fi

    echo ""
    tar -czf "$backup_file" "${paths[@]}"

    local size
    size=$(du -h "$backup_file" | cut -f1)
    print_success "Backup created: $backup_file ($size)"
    echo ""
    print_warning "Backup may contain API keys. Store securely!"
}

# Clean up container and image
cmd_clean() {
    print_header
    print_warning "This will remove the Grid Bot container and image."
    echo ""
    echo "  What will be removed:"
    echo "    - Container: $CONTAINER_NAME"
    echo "    - Image: ${IMAGE_NAME}:${IMAGE_TAG}"
    echo "    - Docker volumes for this project"
    echo "    - Dangling images"
    echo ""
    read -p "Are you sure? (y/N): " confirm

    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        echo ""

        print_step "Stopping and removing container..."
        docker compose -f "$COMPOSE_FILE" down -v --rmi local 2>/dev/null || true

        print_step "Removing dangling images..."
        docker image prune -f 2>/dev/null || true

        print_step "Cleaning build cache..."
        docker builder prune -f --filter "until=24h" 2>/dev/null || true

        echo ""
        print_success "Cleanup complete!"
        echo ""
        print_info "Note: Base images (python:3.11-slim) preserved."
        echo "  Use 'clean-all' to remove everything."
    else
        echo "Cancelled."
    fi
}

# Nuclear cleanup
cmd_clean_all() {
    print_header
    print_error "WARNING: This will perform a COMPLETE Docker cleanup!"
    echo ""
    echo "  What will be removed:"
    echo "    - Container and ALL related containers"
    echo "    - ${IMAGE_NAME} image AND base images (python:3.11, etc.)"
    echo "    - ALL dangling and unused images"
    echo "    - ALL Docker volumes (including persistent data)"
    echo "    - ALL build cache and buildx builders"
    echo "    - ALL unused networks"
    echo ""
    print_error "This CANNOT be undone! Data in volumes will be LOST!"
    echo ""
    read -p "Are you REALLY sure? (type 'yes' to confirm): " confirm

    if [[ "$confirm" == "yes" ]]; then
        echo ""

        print_step "Stopping and removing container with volumes..."
        docker compose -f "$COMPOSE_FILE" down -v --rmi all 2>/dev/null || true
        docker stop "$CONTAINER_NAME" 2>/dev/null || true
        docker rm "$CONTAINER_NAME" 2>/dev/null || true

        print_step "Removing images..."
        docker rmi "${IMAGE_NAME}:${IMAGE_TAG}" 2>/dev/null || true
        docker rmi "${IMAGE_NAME}:latest" 2>/dev/null || true

        print_step "Removing all unused images..."
        docker image prune -af 2>/dev/null || true

        print_step "Removing dangling volumes..."
        docker volume prune -f 2>/dev/null || true

        print_step "Cleaning all build cache..."
        docker builder prune -af 2>/dev/null || true

        print_step "Removing buildx builders..."
        docker buildx rm ipv4builder 2>/dev/null || true
        docker buildx prune -af 2>/dev/null || true

        print_step "Removing unused networks..."
        docker network prune -f 2>/dev/null || true

        echo ""
        print_success "Complete Docker cleanup finished!"
        echo ""
        print_info "Remaining Docker resources:"
        echo "  Images:     $(docker images -q 2>/dev/null | wc -l)"
        echo "  Containers: $(docker ps -aq 2>/dev/null | wc -l)"
        echo "  Volumes:    $(docker volume ls -q 2>/dev/null | wc -l)"
    else
        echo "Cancelled."
    fi
}

# Update and rebuild
cmd_update() {
    print_header
    print_section "Updating Grid Bot"

    print_step "Stopping container..."
    docker compose -f "$COMPOSE_FILE" down 2>/dev/null || true

    print_step "Saving local changes..."
    git stash 2>/dev/null || true

    print_step "Pulling latest code..."
    if ! git pull --rebase origin main; then
        print_warning "Git pull failed. Trying to resolve..."
        git fetch origin
        git reset --hard origin/main
    fi

    git stash pop 2>/dev/null || true

    echo ""
    cmd_build
    echo ""
    cmd_start
    print_success "Update completed!"
}

# Run diagnostics
cmd_diagnose() {
    print_header
    print_section "Running Diagnostics"

    local issues=0

    # Docker
    print_step "Checking Docker..."
    if docker info > /dev/null 2>&1; then
        print_success "Docker is running"
        echo "  $(docker --version)"
    else
        print_error "Docker is not running"
        ((issues++))
    fi
    echo ""

    # Docker Compose
    print_step "Checking Docker Compose..."
    if docker compose version > /dev/null 2>&1; then
        print_success "Docker Compose is available"
        echo "  Version: $(docker compose version --short 2>/dev/null || echo 'unknown')"
    else
        print_error "Docker Compose is not available"
        ((issues++))
    fi
    echo ""

    # BuildKit
    print_step "Checking Docker BuildKit..."
    if docker buildx version > /dev/null 2>&1; then
        print_success "Docker BuildKit is available"
        echo "  $(docker buildx version 2>/dev/null | head -1)"
    else
        print_warning "Docker BuildKit not available (builds may be slower)"
    fi
    echo ""

    # Configuration
    print_step "Checking config.json..."
    if validate_config; then
        print_success "Configuration is valid"

        # Show non-sensitive config info
        if command -v python3 &> /dev/null; then
            local symbol default_scenario scenarios_count
            symbol=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('symbol', 'unknown'))" 2>/dev/null || echo "unknown")
            default_scenario=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('default_scenario', 'unknown'))" 2>/dev/null || echo "unknown")
            scenarios_count=$(python3 -c "import json; print(len(json.load(open('$CONFIG_FILE')).get('config_data', [])))" 2>/dev/null || echo "?")
            echo "  Symbol: $symbol"
            echo "  Default scenario: $default_scenario"
            echo "  Scenarios: $scenarios_count configured"
        fi
    else
        print_error "Configuration has issues"
        ((issues++))
    fi
    echo ""

    # Compose file
    print_step "Checking docker-compose.yml..."
    if [[ -f "$COMPOSE_FILE" ]]; then
        if docker compose -f "$COMPOSE_FILE" config > /dev/null 2>&1; then
            print_success "docker-compose.yml is valid"
        else
            print_error "docker-compose.yml has syntax errors"
            docker compose -f "$COMPOSE_FILE" config 2>&1 | head -10
            ((issues++))
        fi
    else
        print_error "docker-compose.yml not found"
        ((issues++))
    fi
    echo ""

    # Dockerfile
    print_step "Checking Dockerfile..."
    if [[ -f "Dockerfile" ]]; then
        print_success "Dockerfile exists"
    else
        print_error "Dockerfile not found"
        ((issues++))
    fi
    echo ""

    # Docker image
    print_step "Checking Docker image..."
    if docker images "${IMAGE_NAME}:${IMAGE_TAG}" --format "{{.Size}}" 2>/dev/null | grep -q .; then
        local img_size
        img_size=$(docker images "${IMAGE_NAME}:${IMAGE_TAG}" --format "{{.Size}}" 2>/dev/null)
        print_success "Image exists: ${IMAGE_NAME}:${IMAGE_TAG} ($img_size)"
    else
        print_info "Image not built yet"
    fi
    echo ""

    # Data directory
    print_step "Checking data directory..."
    if [[ -d "$DATA_DIR" ]]; then
        print_success "data/ exists"
        for file in grid_bot.log position_state.json tax_transactions.csv position_state_archive.csv; do
            if [[ -f "$DATA_DIR/$file" ]]; then
                local fsize
                fsize=$(du -h "$DATA_DIR/$file" | cut -f1)
                echo "  $file ($fsize)"
            fi
        done
    else
        print_info "data/ does not exist yet (created on first run)"
    fi
    echo ""

    # System resources
    print_step "Checking system resources..."
    check_resources
    echo ""

    # Network connectivity
    print_step "Checking network connectivity..."
    if ping -c 1 -W 3 8.8.8.8 > /dev/null 2>&1; then
        print_success "Internet connectivity OK"
    else
        print_warning "Cannot reach internet (may affect builds and trading)"
        ((issues++))
    fi

    if ping -c 1 -W 3 pypi.org > /dev/null 2>&1; then
        print_success "Python package registry reachable"
    else
        print_warning "Cannot reach Python package registry (pypi.org)"
    fi

    # DNS check
    if command -v nslookup &> /dev/null; then
        if nslookup api.binance.us > /dev/null 2>&1; then
            print_success "Binance.US DNS resolution OK"
        else
            print_warning "Cannot resolve api.binance.us (check DNS settings)"
        fi
    fi
    echo ""

    # Container status
    print_step "Checking container status..."
    if container_exists; then
        if container_running; then
            print_success "Container is running"

            local error_count
            error_count=$(docker compose -f "$COMPOSE_FILE" logs --tail=100 2>&1 | grep -ciE "(error|exception|fatal)" || true)
            if [[ $error_count -gt 0 ]]; then
                print_warning "Found $error_count error(s) in recent logs"
                echo "  Run '$0 logs-error' to see details"
            fi
        else
            print_warning "Container exists but is not running"
        fi
    else
        print_info "Container does not exist (not started yet)"
    fi
    echo ""

    # Summary
    echo "========================================"
    if [[ $issues -eq 0 ]]; then
        print_success "No critical issues found!"
    else
        print_error "Found $issues issue(s) that need attention"
    fi
    echo ""
}

# Fix IPv6 issues (comprehensive: gai.conf + sysctl.d + cmdline.txt + daemon.json + buildx)
cmd_fix_ipv6() {
    print_header
    print_section "Comprehensive Docker IPv6 Fix (Pi OS Lite)"

    echo "This will apply ALL fixes needed to resolve Docker build/pull IPv6 errors"
    echo "on Raspberry Pi OS Lite:"
    echo ""
    echo "  1. /etc/gai.conf             → prefer IPv4 in glibc name resolution"
    echo "  2. /etc/sysctl.d/            → disable IPv6 on all interfaces (persistent)"
    echo "  3. /boot/firmware/cmdline.txt → ipv6.disable=1 at kernel level"
    echo "  4. /etc/docker/daemon.json   → disable IPv6 + force IPv4 DNS + legacy builder"
    echo "  5. systemd drop-ins          → GODEBUG=netdns=cgo+1 for dockerd & containerd"
    echo "                                  (the fix most guides miss — Go's default resolver"
    echo "                                   ignores gai.conf, so dockerd pulls still try IPv6)"
    echo "  6. resolv.conf + dhcpcd hook → 'options no-aaaa' so nothing resolves to IPv6"
    echo "  7. docker buildx             → remove stale IPv6 builders"
    echo "  8. Restart Docker/containerd and verify with a real pull"
    echo ""
    print_warning "Requires sudo. A reboot is needed if cmdline.txt is modified."
    echo ""
    read -p "Continue? (y/N): " confirm

    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        exit 0
    fi

    local needs_reboot=0

    # ------------------------------------------------------------------------
    # Step 1: /etc/gai.conf — make glibc prefer IPv4 (critical for BuildKit)
    # ------------------------------------------------------------------------
    echo ""
    print_step "1/8 Configuring /etc/gai.conf to prefer IPv4..."

    if [[ ! -f /etc/gai.conf ]]; then
        sudo touch /etc/gai.conf
    fi

    # The 'precedence ::ffff:0:0/96 100' line tells glibc's getaddrinfo to
    # rank IPv4-mapped addresses above native IPv6, so AAAA lookups don't
    # get tried first. Docker/BuildKit inherit this behaviour.
    if grep -qE '^[[:space:]]*precedence[[:space:]]+::ffff:0:0/96[[:space:]]+100' /etc/gai.conf; then
        print_info "gai.conf already prefers IPv4"
    else
        # Remove any commented/duplicate variants of the same line first
        sudo sed -i -E '/^[[:space:]]*#?[[:space:]]*precedence[[:space:]]+::ffff:0:0\/96/d' /etc/gai.conf
        echo "precedence ::ffff:0:0/96  100  # prefer IPv4 (Grid Bot helper)" | \
            sudo tee -a /etc/gai.conf > /dev/null
        print_success "gai.conf updated — IPv4 now preferred over IPv6"
    fi

    # ------------------------------------------------------------------------
    # Step 2: /etc/sysctl.d/99-disable-ipv6.conf (modern Debian drop-in)
    # ------------------------------------------------------------------------
    echo ""
    print_step "2/8 Writing /etc/sysctl.d/99-disable-ipv6.conf..."

    # Clean up the old /etc/sysctl.conf appendage from previous versions of
    # this script so we have a single source of truth.
    if sudo grep -q "Disable IPv6 for Docker compatibility (added by Grid Bot helper)" /etc/sysctl.conf 2>/dev/null; then
        print_info "Removing legacy sysctl.conf block from previous script version..."
        sudo sed -i '/# Disable IPv6 for Docker compatibility (added by Grid Bot helper)/,/net.ipv6.conf.lo.disable_ipv6 = 1/d' /etc/sysctl.conf
    fi

    sudo tee /etc/sysctl.d/99-disable-ipv6.conf > /dev/null << 'EOF'
# Disable IPv6 for Docker compatibility (managed by docker-helper.sh)
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
EOF
    print_success "sysctl drop-in written"

    # Apply immediately (--system reads all drop-ins, plain -p does not)
    sudo sysctl --system > /dev/null 2>&1 || true
    print_success "sysctl applied"

    # ------------------------------------------------------------------------
    # Step 3: /boot/firmware/cmdline.txt (kernel-level IPv6 disable)
    # ------------------------------------------------------------------------
    echo ""
    print_step "3/8 Updating kernel cmdline..."

    local cmdline_file=""
    if [[ -f /boot/firmware/cmdline.txt ]]; then
        cmdline_file=/boot/firmware/cmdline.txt
    elif [[ -f /boot/cmdline.txt ]]; then
        cmdline_file=/boot/cmdline.txt
    fi

    if [[ -z "$cmdline_file" ]]; then
        print_info "No Pi cmdline.txt found — skipping (not running on Raspberry Pi OS?)"
    elif grep -q "ipv6.disable=1" "$cmdline_file" 2>/dev/null; then
        print_info "ipv6.disable=1 already present in $cmdline_file"
    else
        # cmdline.txt MUST be a single line. Back up, then append on same line.
        sudo cp "$cmdline_file" "${cmdline_file}.bak-$(date +%Y%m%d%H%M%S)"

        # Read line, strip trailing newline/whitespace, append flag, restore newline.
        # Using a temp file to avoid partial writes on power loss.
        local tmp
        tmp=$(mktemp)
        # shellcheck disable=SC2002
        sudo cat "$cmdline_file" | tr -d '\n' | sed -E 's/[[:space:]]+$//' > "$tmp"
        echo " ipv6.disable=1" | sudo tee -a "$tmp" > /dev/null
        sudo install -m 0755 "$tmp" "$cmdline_file"
        rm -f "$tmp"
        print_success "Appended ipv6.disable=1 to $cmdline_file"
        print_warning "A REBOOT is required for this kernel change to take effect."
        needs_reboot=1
    fi

    # ------------------------------------------------------------------------
    # Step 4: /etc/docker/daemon.json
    # ------------------------------------------------------------------------
    echo ""
    print_step "4/8 Configuring /etc/docker/daemon.json..."
    sudo mkdir -p /etc/docker

    # Merge with existing valid JSON when possible (preserves user's other keys)
    local merge_script
    merge_script='
import json, os, sys
target = "/etc/docker/daemon.json"
desired = {
    "ipv6": False,
    "dns": ["8.8.8.8", "1.1.1.1"],
    "dns-opts": ["ndots:0", "single-request"],
    # Force the legacy builder. BuildKit runs in its own container with a Go
    # resolver that ignores /etc/gai.conf and does not fall back from AAAA
    # to A when the kernel rejects IPv6 sockets, so it fails with
    # "address family not supported by protocol" on IPv6-disabled hosts.
    "features": {"buildkit": False}
}
existing = {}
if os.path.exists(target) and os.path.getsize(target) > 0:
    try:
        with open(target) as f:
            existing = json.load(f)
    except Exception:
        existing = {}
# Strip any prior IPv6 keys that cause trouble on newer Docker versions
for k in ("fixed-cidr-v6", "ip6tables", "experimental"):
    existing.pop(k, None)
# Deep-merge features so we do not clobber other feature flags
features = dict(existing.get("features") or {})
features.update(desired["features"])
existing.update(desired)
existing["features"] = features
print(json.dumps(existing, indent=2))
'
    if command -v python3 &> /dev/null; then
        if [[ -f /etc/docker/daemon.json ]]; then
            sudo cp /etc/docker/daemon.json "/etc/docker/daemon.json.bak-$(date +%Y%m%d%H%M%S)"
        fi
        python3 -c "$merge_script" | sudo tee /etc/docker/daemon.json > /dev/null
        print_success "daemon.json written (existing keys preserved where safe)"
    else
        # Fallback: overwrite (python3 ships with Pi OS Lite, so this is rare)
        if [[ -f /etc/docker/daemon.json ]]; then
            sudo cp /etc/docker/daemon.json "/etc/docker/daemon.json.bak-$(date +%Y%m%d%H%M%S)"
        fi
        sudo tee /etc/docker/daemon.json > /dev/null << 'EOF'
{
  "ipv6": false,
  "dns": ["8.8.8.8", "1.1.1.1"],
  "dns-opts": ["ndots:0", "single-request"],
  "features": {"buildkit": false}
}
EOF
        print_success "daemon.json written (python3 unavailable — overwrote)"
    fi

    # ------------------------------------------------------------------------
    # Step 5: Force cgo resolver for dockerd + containerd via systemd drop-ins
    # ------------------------------------------------------------------------
    # Go's default netgo resolver ignores /etc/gai.conf and returns AAAA
    # records in their natural order, so dockerd/containerd try IPv6 first
    # when pulling registry blobs. Even with ipv6.disable=1 that surfaces as
    # `socket: address family not supported by protocol` inside
    # `httpReadSeeker: failed open`. Forcing GODEBUG=netdns=cgo+1 makes them
    # route through glibc's getaddrinfo, which honours the gai.conf priority
    # rule we set in step 1 and returns IPv4 first.
    echo ""
    print_step "5/8 Forcing IPv4-first DNS in dockerd and containerd..."

    for unit in docker containerd; do
        if ! systemctl list-unit-files "${unit}.service" 2>/dev/null | grep -q "${unit}.service"; then
            print_info "${unit}.service not installed — skipping"
            continue
        fi
        local dropin_dir="/etc/systemd/system/${unit}.service.d"
        sudo mkdir -p "$dropin_dir"
        sudo tee "${dropin_dir}/10-ipv4-resolver.conf" > /dev/null << 'EOF'
# Managed by docker-helper.sh (fix-ipv6)
# Force Go's cgo resolver so /etc/gai.conf (prefer IPv4) is honoured.
# Without this, image pulls over the containerd content fetcher try AAAA
# records first and fail with EAFNOSUPPORT on IPv6-disabled kernels.
[Service]
Environment=GODEBUG=netdns=cgo+1
EOF
        print_success "${unit}.service drop-in written"
    done

    sudo systemctl daemon-reload
    print_success "systemd reloaded"

    # ------------------------------------------------------------------------
    # Step 6: DNS resolver — drop AAAA entirely (glibc 2.31+, Pi OS Bookworm+)
    # ------------------------------------------------------------------------
    # `options no-aaaa` tells glibc's stub resolver to skip AAAA lookups
    # completely, so nothing upstream ever sees an IPv6 address for
    # registry-1.docker.io. `single-request` forces sequential A/AAAA queries
    # (harmless with no-aaaa, useful if no-aaaa is unsupported by an older
    # glibc). We persist the option via /etc/resolvconf.conf (read by the
    # openresolv/resolvconf package) AND drop it straight into
    # /etc/resolv.conf so it applies immediately, even before the next DHCP
    # lease refresh.
    echo ""
    print_step "6/8 Configuring DNS to drop AAAA records..."

    # Persist across dhcpcd/resolvconf rewrites
    if [[ -f /etc/resolvconf.conf ]] || command -v resolvconf &> /dev/null; then
        sudo touch /etc/resolvconf.conf
        if grep -qE '^[[:space:]]*resolv_conf_options=' /etc/resolvconf.conf 2>/dev/null; then
            # Replace existing line rather than duplicating
            sudo sed -i -E \
                's|^[[:space:]]*resolv_conf_options=.*|resolv_conf_options="single-request no-aaaa"  # Grid Bot helper|' \
                /etc/resolvconf.conf
        else
            echo 'resolv_conf_options="single-request no-aaaa"  # Grid Bot helper' | \
                sudo tee -a /etc/resolvconf.conf > /dev/null
        fi
        print_success "/etc/resolvconf.conf persisted"

        if command -v resolvconf &> /dev/null; then
            sudo resolvconf -u 2>/dev/null || true
        fi
    else
        print_info "resolvconf not installed — persistence handled via dhcpcd hook below"
    fi

    # dhcpcd (Pi OS Lite default): ship a hook that re-applies the options
    # after every DHCP lease (dhcpcd rewrites /etc/resolv.conf on renewal).
    if [[ -d /lib/dhcpcd/dhcpcd-hooks ]] || [[ -d /etc/dhcp/dhcpcd-hooks ]] || command -v dhcpcd &> /dev/null; then
        local hook_dir="/lib/dhcpcd/dhcpcd-hooks"
        [[ -d "$hook_dir" ]] || hook_dir="/etc/dhcp/dhcpcd-hooks"
        [[ -d "$hook_dir" ]] || hook_dir="/lib/dhcpcd/dhcpcd-hooks"
        sudo mkdir -p "$hook_dir"
        sudo tee "${hook_dir}/99-no-aaaa" > /dev/null << 'EOF'
# Managed by docker-helper.sh (fix-ipv6).
# Re-append IPv4-only resolver options after dhcpcd rewrites resolv.conf.
if [ -f /etc/resolv.conf ] && ! grep -qE '^options .*no-aaaa' /etc/resolv.conf; then
    printf 'options single-request no-aaaa\n' >> /etc/resolv.conf
fi
EOF
        sudo chmod 0644 "${hook_dir}/99-no-aaaa"
        print_success "dhcpcd hook installed at ${hook_dir}/99-no-aaaa"
    fi

    # Apply immediately to the live /etc/resolv.conf. Handle the common case
    # where it's a symlink (systemd-resolved stub) by editing the target.
    local live_resolv=/etc/resolv.conf
    if [[ -L /etc/resolv.conf ]]; then
        live_resolv=$(readlink -f /etc/resolv.conf || echo /etc/resolv.conf)
    fi
    if [[ -w "$live_resolv" ]] || sudo test -w "$live_resolv"; then
        if ! sudo grep -qE '^[[:space:]]*options[[:space:]]+.*no-aaaa' "$live_resolv" 2>/dev/null; then
            # Remove any prior partial 'options' we wrote previously
            sudo sed -i -E '/^[[:space:]]*options[[:space:]]+.*# Grid Bot helper$/d' "$live_resolv" 2>/dev/null || true
            echo 'options single-request no-aaaa  # Grid Bot helper' | \
                sudo tee -a "$live_resolv" > /dev/null
            print_success "$live_resolv updated with 'options single-request no-aaaa'"
        else
            print_info "$live_resolv already contains no-aaaa"
        fi
    else
        print_warning "$live_resolv is not writable (managed by systemd-resolved?) — relying on GODEBUG=cgo+gai.conf"
    fi

    # ------------------------------------------------------------------------
    # Step 7: Reset buildx builders that may have cached IPv6 state
    # ------------------------------------------------------------------------
    echo ""
    print_step "7/8 Resetting Docker buildx builders..."

    if docker buildx version > /dev/null 2>&1; then
        # Remove any leftover custom builders from prior attempts
        docker buildx rm ipv4builder 2>/dev/null || true
        docker buildx rm gridbot-builder 2>/dev/null || true
        # Recreate the default builder fresh so it picks up the new daemon config
        docker buildx prune -af > /dev/null 2>&1 || true
        print_success "buildx state cleaned"
    else
        print_info "buildx not installed — skipping"
    fi

    # ------------------------------------------------------------------------
    # Step 8: Restart services and verify with a real pull
    # ------------------------------------------------------------------------
    echo ""
    print_step "8/8 Restarting Docker + containerd and verifying..."
    # Restart containerd first so dockerd connects to a freshly-configured peer
    sudo systemctl restart containerd 2>/dev/null || true
    sudo systemctl restart docker

    # Give dockerd a moment to come back up
    local tries=0
    until docker info > /dev/null 2>&1; do
        ((tries++))
        if [[ $tries -gt 15 ]]; then
            print_error "Docker failed to restart. Check: sudo journalctl -u docker -n 50"
            exit 1
        fi
        sleep 1
    done
    print_success "Docker is back up"

    # Verify daemon picked up ipv6=false
    local daemon_ipv6
    daemon_ipv6=$(docker info --format '{{json .}}' 2>/dev/null | \
        python3 -c 'import json,sys;d=json.load(sys.stdin);print("on" if d.get("IPv6",False) else "off")' 2>/dev/null || echo "unknown")
    echo "  Daemon IPv6: $daemon_ipv6"

    # Verify GODEBUG was applied to the running dockerd
    if sudo tr '\0' '\n' < /proc/$(pidof dockerd 2>/dev/null | awk '{print $1}')/environ 2>/dev/null | grep -q '^GODEBUG=.*netdns=cgo'; then
        print_success "dockerd is using cgo resolver (GODEBUG=netdns=cgo+1)"
    else
        print_warning "Could not confirm GODEBUG=netdns=cgo+1 on dockerd (may need reboot)"
    fi

    # Real test: pull the exact base image the Dockerfile needs. This is the
    # layer that was failing before, so success here means rebuild will work.
    echo ""
    print_step "Test: docker pull python:3.11-slim-bookworm"
    if timeout 180 docker pull python:3.11-slim-bookworm; then
        print_success "Base image pulled successfully over IPv4"
    else
        print_error "Test pull failed."
        echo ""
        echo "  Check the output above. If it still shows a [2xxx:...] IPv6"
        echo "  address, reboot so the kernel cmdline, systemd drop-in and"
        echo "  resolv.conf changes all take effect together:"
        echo ""
        echo "    sudo reboot"
        echo ""
        echo "  After reboot, re-run: $0 fix-ipv6"
        echo ""
        exit 1
    fi

    # ------------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------------
    echo ""
    echo "========================================"
    print_success "IPv6 fix applied."
    echo ""
    echo "  Changes made:"
    echo "    • /etc/gai.conf                                 (prefer IPv4 in glibc)"
    echo "    • /etc/sysctl.d/99-disable-ipv6.conf            (runtime IPv6 off)"
    [[ -n "$cmdline_file" ]] && echo "    • $cmdline_file  (kernel IPv6 off)"
    echo "    • /etc/docker/daemon.json                       (ipv6=false, buildkit=false)"
    echo "    • /etc/systemd/system/docker.service.d/         (GODEBUG=cgo+1)"
    echo "    • /etc/systemd/system/containerd.service.d/     (GODEBUG=cgo+1)"
    echo "    • /etc/resolv.conf + /etc/resolvconf.conf       (no-aaaa)"
    echo "    • dhcpcd hook 99-no-aaaa                        (survives DHCP renewal)"
    echo "    • Docker restarted, buildx cache cleared"
    echo ""
    echo "  Why each piece matters:"
    echo "    • Kernel ipv6.disable=1     — no IPv6 sockets, so IPv6 dials EAFNOSUPPORT"
    echo "    • gai.conf prefer IPv4      — glibc returns A records first"
    echo "    • GODEBUG=netdns=cgo+1      — dockerd/containerd actually USE glibc"
    echo "                                   (Go's default netgo ignores gai.conf)"
    echo "    • resolv.conf no-aaaa       — belt & suspenders: never resolve AAAA"
    echo "    • BuildKit off              — legacy builder falls back to IPv4 cleanly"
    echo ""

    if [[ $needs_reboot -eq 1 ]]; then
        print_warning "REBOOT REQUIRED for the kernel cmdline change to take effect:"
        echo ""
        echo "    sudo reboot"
        echo ""
        echo "  After reboot, verify with:"
        echo "    ip -6 addr         # should show no global IPv6 addresses"
        echo "    $0 rebuild         # rebuild the image"
    else
        echo "  Next step:"
        echo "    $0 rebuild         # rebuild the image"
    fi
    echo ""
}

# Fix file permissions
cmd_fix_permissions() {
    print_header
    print_section "Fixing Permissions"

    # Config files
    if [[ -f "$CONFIG_FILE" ]]; then
        chmod 600 "$CONFIG_FILE" && print_success "Set config.json to 600"
    fi
    if [[ -f "./src/priv/config.json" ]]; then
        chmod 600 "./src/priv/config.json" && print_success "Set src/priv/config.json to 600"
    fi

    # Data directory
    if [[ -d "$DATA_DIR" ]]; then
        chmod 755 "$DATA_DIR" && print_success "Set data/ to 755"
    fi

    # Scripts + the portfolio CLI (it has a shebang and is meant to be run directly)
    for script in docker-helper.sh docker-entrypoint.sh run_bot.sh monitor_bot.sh test_setup.sh portfolio.py; do
        if [[ -f "$script" ]]; then
            chmod +x "$script" && print_success "Made $script executable"
        fi
    done

    # Template should be world-readable (not secret), regular mode 644
    if [[ -f ./src/priv/config.json.template ]]; then
        chmod 644 ./src/priv/config.json.template && \
            print_success "Set config.json.template to 644"
    fi

    # Ensure data dir exists before attempting chmod (fresh clones lack it)
    if [[ ! -d "$DATA_DIR" ]]; then
        mkdir -p "$DATA_DIR" && chmod 755 "$DATA_DIR" && \
            print_success "Created $DATA_DIR (755)"
    fi

    echo ""
    print_success "Permissions fixed!"
}

# Validate everything
cmd_validate() {
    print_header
    print_section "Validating Configuration"

    local valid=1

    # Docker
    print_step "Checking Docker..."
    if docker info > /dev/null 2>&1; then
        print_success "Docker is running"
    else
        print_error "Docker is not running"
        valid=0
    fi
    echo ""

    # Docker Compose
    print_step "Checking Docker Compose..."
    if docker compose version > /dev/null 2>&1; then
        print_success "Docker Compose available"
    else
        print_error "Docker Compose not available"
        valid=0
    fi
    echo ""

    # Compose file
    print_step "Validating docker-compose.yml..."
    if [[ -f "$COMPOSE_FILE" ]]; then
        if docker compose -f "$COMPOSE_FILE" config > /dev/null 2>&1; then
            print_success "docker-compose.yml is valid"
        else
            print_error "docker-compose.yml validation failed:"
            docker compose -f "$COMPOSE_FILE" config 2>&1
            valid=0
        fi
    else
        print_error "docker-compose.yml not found"
        valid=0
    fi
    echo ""

    # Config file
    print_step "Validating config.json..."
    if validate_config; then
        print_success "config.json is valid"
    else
        valid=0
    fi
    echo ""

    # Dockerfile
    print_step "Checking Dockerfile..."
    if [[ -f "Dockerfile" ]]; then
        print_success "Dockerfile exists"
    else
        print_error "Dockerfile not found"
        valid=0
    fi
    echo ""

    # Docker entrypoint
    print_step "Checking docker-entrypoint.sh..."
    if [[ -f "docker-entrypoint.sh" ]]; then
        if [[ -x "docker-entrypoint.sh" ]]; then
            print_success "docker-entrypoint.sh exists and is executable"
        else
            print_warning "docker-entrypoint.sh exists but is not executable"
            echo "  Fix: chmod +x docker-entrypoint.sh"
        fi
    else
        print_error "docker-entrypoint.sh not found"
        valid=0
    fi
    echo ""

    # Requirements
    print_step "Checking requirements.txt..."
    if [[ -f "requirements.txt" ]]; then
        print_success "requirements.txt exists"
        echo "  $(cat requirements.txt | grep -v '^#' | grep -v '^$' | tr '\n' ', ' | sed 's/,$//')"
    else
        print_error "requirements.txt not found"
        valid=0
    fi
    echo ""

    if [[ $valid -eq 1 ]]; then
        echo ""
        print_success "All validations passed!"
    else
        echo ""
        print_error "Some validations failed - fix issues above before building"
        exit 1
    fi
}

# Show version information
cmd_version() {
    print_header
    echo "  Script Version:  $SCRIPT_VERSION"

    if [[ -f "src/main.py" ]] && command -v python3 &> /dev/null; then
        local app_ver
        app_ver=$(grep -oP 'v\d+\.\d+' src/main.py 2>/dev/null | head -1 || echo "unknown")
        echo "  Bot Version:     $app_ver"
    fi

    echo ""
    docker --version 2>/dev/null || echo "  Docker: not installed"
    docker compose version 2>/dev/null || echo "  Docker Compose: not installed"

    if docker images "${IMAGE_NAME}:${IMAGE_TAG}" --format "{{.Size}}" 2>/dev/null | grep -q .; then
        echo ""
        echo "  Image: ${IMAGE_NAME}:${IMAGE_TAG}"
        docker images "${IMAGE_NAME}:${IMAGE_TAG}" --format "  Size: {{.Size}}  Created: {{.CreatedSince}}" 2>/dev/null || true
    fi
}

##############################################################################
# Main
##############################################################################

check_docker

case "${1:-help}" in
    build)
        cmd_build
        ;;
    build-verbose)
        cmd_build_verbose
        ;;
    start)
        cmd_start
        ;;
    stop)
        cmd_stop
        ;;
    restart)
        cmd_restart
        ;;
    rebuild)
        cmd_rebuild
        ;;
    logs)
        cmd_logs
        ;;
    logs-tail)
        shift
        cmd_logs_tail "${1:-50}"
        ;;
    logs-error)
        cmd_logs_error
        ;;
    status)
        cmd_status
        ;;
    health)
        cmd_health
        ;;
    stats)
        cmd_stats
        ;;
    test-api)
        cmd_test_api
        ;;
    tax-summary)
        shift
        cmd_tax_summary "$@"
        ;;
    shell)
        cmd_shell
        ;;
    exec)
        shift
        cmd_exec "$@"
        ;;
    backup)
        cmd_backup
        ;;
    clean)
        cmd_clean
        ;;
    clean-all)
        cmd_clean_all
        ;;
    update)
        cmd_update
        ;;
    diagnose)
        cmd_diagnose
        ;;
    fix-ipv6)
        cmd_fix_ipv6
        ;;
    fix-permissions)
        cmd_fix_permissions
        ;;
    validate)
        cmd_validate
        ;;
    version)
        cmd_version
        ;;
    help|--help|-h)
        cmd_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        cmd_help
        exit 1
        ;;
esac

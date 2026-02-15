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
CONFIG_FILE="./config.json"
CONFIG_TEMPLATE="./src/priv/config.json.template"
DATA_DIR="./data"
BACKUP_DIR="./backups"

# Enable BuildKit for faster builds with better caching
export DOCKER_BUILDKIT=1

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
    if [[ ! -f "$CONFIG_FILE" ]]; then
        print_error "Config file not found: $CONFIG_FILE"
        if [[ -f "$CONFIG_TEMPLATE" ]]; then
            echo "  Create from template:"
            echo "    cp $CONFIG_TEMPLATE $CONFIG_FILE"
            echo "    chmod 600 $CONFIG_FILE"
            echo "    nano $CONFIG_FILE  # Add your API keys"
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

    docker compose -f "$COMPOSE_FILE" build --no-cache --progress=plain
    local build_status=$?

    printf "\n"
    stty sane 2>/dev/null || true

    if [[ $build_status -eq 0 ]]; then
        print_success "Build completed!"
        docker images "${IMAGE_NAME}:${IMAGE_TAG}" --format "  Image: {{.Repository}}:{{.Tag}} | Size: {{.Size}}" 2>/dev/null || true
        echo ""
    else
        print_error "Build failed!"
        exit 1
    fi
}

# Start container
cmd_start() {
    print_header
    print_section "Starting Grid Bot"

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
        print_success "Including config.json"
    fi
    if [[ -f "./src/priv/config.json" ]]; then
        paths+=("./src/priv/config.json")
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

# Fix IPv6 issues
cmd_fix_ipv6() {
    print_header
    print_warning "This will modify Docker daemon settings to disable IPv6."
    echo ""
    echo "  This fix is common for Raspberry Pi Docker networking issues."
    echo "  It requires sudo access."
    echo ""
    read -p "Continue? (y/N): " confirm

    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        exit 0
    fi

    echo ""
    print_step "Disabling IPv6..."

    # Check if already configured
    if grep -q "net.ipv6.conf.all.disable_ipv6 = 1" /etc/sysctl.conf 2>/dev/null; then
        print_info "IPv6 already disabled in sysctl.conf"
    else
        sudo tee -a /etc/sysctl.conf > /dev/null << 'EOF'

# Disable IPv6 for Docker compatibility (added by Grid Bot helper)
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
EOF
        print_success "Added IPv6 disable settings to sysctl.conf"
    fi

    sudo sysctl -p 2>/dev/null || true
    print_success "Applied sysctl settings"

    # Configure Docker daemon
    print_step "Configuring Docker daemon..."
    sudo mkdir -p /etc/docker

    if [[ -f /etc/docker/daemon.json ]]; then
        print_warning "Docker daemon.json already exists, backing up..."
        sudo cp /etc/docker/daemon.json /etc/docker/daemon.json.bak
    fi

    sudo tee /etc/docker/daemon.json > /dev/null << 'EOF'
{
    "ipv6": false,
    "ip6tables": false,
    "dns": ["8.8.8.8", "8.8.4.4"]
}
EOF
    print_success "Configured Docker daemon"

    print_step "Restarting Docker..."
    sudo systemctl restart docker

    sleep 2
    if docker info > /dev/null 2>&1; then
        print_success "Docker restarted successfully"
    else
        print_error "Docker failed to restart. Check: sudo journalctl -u docker -n 50"
        exit 1
    fi

    echo ""
    print_success "IPv6 disabled. You may need to rebuild: $0 rebuild"
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

    # Scripts
    for script in docker-helper.sh docker-entrypoint.sh run_bot.sh monitor_bot.sh test_setup.sh; do
        if [[ -f "$script" ]]; then
            chmod +x "$script" && print_success "Made $script executable"
        fi
    done

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

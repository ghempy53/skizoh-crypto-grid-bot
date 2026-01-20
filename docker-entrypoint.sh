#!/bin/bash
# =============================================================================
# Skizoh Grid Bot - Docker Entrypoint
# Optimized for Raspberry Pi with better error handling
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Version
VERSION="14.2"

print_banner() {
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}     ${GREEN}SKIZOH CRYPTO GRID TRADING BOT v${VERSION}${NC}                     ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}     ${GREEN}Raspberry Pi Optimized${NC}                                   ${CYAN}║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
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

# Check system resources (Pi-specific)
check_resources() {
    # Check available memory
    if command -v free &> /dev/null; then
        AVAIL_MEM=$(free -m | awk '/^Mem:/ {print $7}')
        if [ -n "$AVAIL_MEM" ] && [ "$AVAIL_MEM" -lt 100 ]; then
            print_warning "Low memory available: ${AVAIL_MEM}MB"
            print_info "Consider closing other applications"
        fi
    fi
}

check_config() {
    CONFIG_FILE="/app/src/priv/config.json"
    
    if [ ! -f "$CONFIG_FILE" ]; then
        print_error "Config file not found!"
        echo ""
        echo "  Mount your config.json to: /app/src/priv/config.json"
        echo ""
        echo "  Example:"
        echo "    docker run -v /path/to/config.json:/app/src/priv/config.json ..."
        echo ""
        exit 1
    fi
    
    # Validate JSON syntax
    if ! python3 -c "import json; json.load(open('$CONFIG_FILE'))" 2>/dev/null; then
        print_error "config.json is not valid JSON!"
        echo ""
        echo "  Check for syntax errors (missing commas, quotes, brackets)"
        exit 1
    fi
    
    # Check if API keys are configured
    API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('api_key', ''))" 2>/dev/null)
    
    if [ "$API_KEY" = "YOUR_BINANCE_US_API_KEY" ] || [ -z "$API_KEY" ]; then
        print_error "API key not configured in config.json"
        exit 1
    fi
    
    print_success "Configuration validated"
}

check_data_dir() {
    # Ensure data directory exists and is writable
    if [ ! -d "/app/data" ]; then
        print_warning "Data directory missing, creating..."
        mkdir -p /app/data 2>/dev/null || {
            print_error "Cannot create /app/data directory"
            exit 1
        }
    fi
    
    # Test write access
    if ! touch /app/data/.write_test 2>/dev/null; then
        print_error "Cannot write to /app/data"
        echo "  Ensure the volume is mounted with write permissions"
        exit 1
    fi
    rm -f /app/data/.write_test
    
    print_success "Data directory ready"
}

# Show memory-efficient Python settings
show_optimization_info() {
    echo ""
    print_info "Pi Optimizations Active:"
    echo "    • NumPy threads: ${OMP_NUM_THREADS:-1}"
    echo "    • Python optimize: ${PYTHONOPTIMIZE:-0}"
    echo "    • Unbuffered output: ${PYTHONUNBUFFERED:-0}"
    echo ""
}

run_bot() {
    print_banner
    check_resources
    check_config
    check_data_dir
    show_optimization_info
    
    echo -e "${GREEN}Starting Grid Trading Bot...${NC}"
    echo ""
    
    cd /app/src
    
    # Use exec to replace shell with Python (proper signal handling)
    exec python3 main.py
}

run_test_api() {
    print_banner
    check_config
    
    print_info "Running API connection test..."
    echo ""
    
    cd /app/src
    python3 test_api.py
    EXIT_CODE=$?
    
    echo ""
    if [ $EXIT_CODE -eq 0 ]; then
        print_success "API test passed!"
    else
        print_error "API test failed (exit code: $EXIT_CODE)"
    fi
    
    exit $EXIT_CODE
}

run_tax_summary() {
    print_banner
    check_data_dir
    
    print_info "Generating tax summary..."
    echo ""
    
    cd /app/src
    python3 tax_summary.py "$@"
}

show_help() {
    print_banner
    echo "Usage: docker run [options] skizoh-grid-bot [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  run          Start the trading bot (default)"
    echo "  test-api     Test API connection"
    echo "  tax-summary  Generate tax summary report"
    echo "  shell        Start an interactive shell"
    echo "  health       Run health check"
    echo "  help         Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  GRIDBOT_SCENARIO       Set trading scenario (e.g., 'Balanced')"
    echo "  GRIDBOT_NONINTERACTIVE Set to 'true' for non-interactive mode"
    echo "  TZ                     Set timezone (default: UTC)"
    echo ""
    echo "Examples:"
    echo ""
    echo "  # Run the bot"
    echo "  docker run -d --name gridbot \\"
    echo "    -v ./config.json:/app/src/priv/config.json:ro \\"
    echo "    -v ./data:/app/data \\"
    echo "    skizoh-grid-bot"
    echo ""
    echo "  # Run with specific scenario"
    echo "  docker run -d --name gridbot \\"
    echo "    -e GRIDBOT_SCENARIO=Conservative \\"
    echo "    -e GRIDBOT_NONINTERACTIVE=true \\"
    echo "    -v ./config.json:/app/src/priv/config.json:ro \\"
    echo "    -v ./data:/app/data \\"
    echo "    skizoh-grid-bot"
    echo ""
    echo "  # Test API connection"
    echo "  docker run --rm \\"
    echo "    -v ./config.json:/app/src/priv/config.json:ro \\"
    echo "    skizoh-grid-bot test-api"
    echo ""
    echo "  # Generate tax summary for 2025"
    echo "  docker run --rm \\"
    echo "    -v ./data:/app/data \\"
    echo "    skizoh-grid-bot tax-summary 2025"
    echo ""
}

run_health_check() {
    # Simple health check for Docker HEALTHCHECK
    python3 -c "import ccxt; import numpy; print('healthy')" && exit 0 || exit 1
}

# =============================================================================
# Main command handling
# =============================================================================
case "${1:-run}" in
    run)
        run_bot
        ;;
    test-api|test_api|testapi)
        run_test_api
        ;;
    tax-summary|tax_summary|taxsummary)
        shift
        run_tax_summary "$@"
        ;;
    shell|bash|sh)
        exec /bin/bash
        ;;
    health|healthcheck)
        run_health_check
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac

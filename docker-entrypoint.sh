#!/bin/bash
# =============================================================================
# Skizoh Grid Bot v2.0 - Docker Entrypoint
# Optimized for Raspberry Pi
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

VERSION="2.0"

print_banner() {
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}     ${GREEN}SKIZOH GRID TRADING BOT v${VERSION} - PROFIT OPTIMIZED${NC}          ${CYAN}║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

check_config() {
    CONFIG_FILE="/app/src/priv/config.json"
    
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${RED}✗${NC} Config not found: $CONFIG_FILE"
        echo "  Mount: -v /path/to/config.json:/app/src/priv/config.json"
        exit 1
    fi
    
    if ! python3 -c "import json; json.load(open('$CONFIG_FILE'))" 2>/dev/null; then
        echo -e "${RED}✗${NC} Invalid JSON in config"
        exit 1
    fi
    
    API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('api_key', ''))" 2>/dev/null)
    if [ "$API_KEY" = "YOUR_BINANCE_US_API_KEY" ] || [ -z "$API_KEY" ]; then
        echo -e "${RED}✗${NC} API key not configured"
        exit 1
    fi
    
    echo -e "${GREEN}✓${NC} Config validated"
}

check_data_dir() {
    if [ ! -d "/app/data" ]; then
        mkdir -p /app/data 2>/dev/null || exit 1
    fi
    
    if ! touch /app/data/.test 2>/dev/null; then
        echo -e "${RED}✗${NC} Cannot write to /app/data"
        exit 1
    fi
    rm -f /app/data/.test
    echo -e "${GREEN}✓${NC} Data directory ready"
}

run_bot() {
    print_banner
    check_config
    check_data_dir
    
    echo -e "${GREEN}Starting Grid Bot...${NC}"
    echo ""
    
    cd /app/src
    exec python3 main.py
}

run_test_api() {
    print_banner
    check_config
    
    echo "Testing API connection..."
    cd /app/src
    python3 test_api.py
}

run_tax_summary() {
    print_banner
    check_data_dir
    
    echo "Generating tax summary..."
    cd /app/src
    python3 tax_summary.py "$@"
}

show_help() {
    print_banner
    echo "Usage: docker run [options] skizoh-grid-bot [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  run          Start trading bot (default)"
    echo "  test-api     Test API connection"
    echo "  tax-summary  Generate tax report"
    echo "  shell        Interactive shell"
    echo "  help         Show this help"
    echo ""
    echo "Environment Variables:"
    echo "  GRIDBOT_SCENARIO       Set trading scenario"
    echo "  GRIDBOT_NONINTERACTIVE Enable non-interactive mode"
    echo ""
}

case "${1:-run}" in
    run)
        run_bot
        ;;
    test-api|test_api)
        run_test_api
        ;;
    tax-summary|tax_summary)
        shift
        run_tax_summary "$@"
        ;;
    shell|bash)
        exec /bin/bash
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        show_help
        exit 1
        ;;
esac

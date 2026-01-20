#!/bin/bash
# =============================================================================
# Skizoh Grid Bot - Docker Entrypoint
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_banner() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}     ${GREEN}SKIZOH CRYPTO GRID TRADING BOT v14.1${NC}                     ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}     ${GREEN}Docker Container${NC}                                         ${BLUE}║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

check_config() {
    CONFIG_FILE="/app/src/priv/config.json"
    
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${RED}✗ ERROR: Config file not found!${NC}"
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
        echo -e "${RED}✗ ERROR: config.json is not valid JSON!${NC}"
        exit 1
    fi
    
    # Check if API keys are configured
    API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('api_key', ''))" 2>/dev/null)
    
    if [ "$API_KEY" = "YOUR_BINANCE_US_API_KEY" ] || [ -z "$API_KEY" ]; then
        echo -e "${RED}✗ ERROR: API key not configured in config.json${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Configuration validated${NC}"
}

check_data_dir() {
    # Ensure data directory exists and is writable
    if [ ! -d "/app/data" ]; then
        echo -e "${YELLOW}⚠ Data directory missing, creating...${NC}"
        mkdir -p /app/data
    fi
    
    # Test write access
    if ! touch /app/data/.write_test 2>/dev/null; then
        echo -e "${RED}✗ ERROR: Cannot write to /app/data${NC}"
        echo "  Ensure the volume is mounted with write permissions"
        exit 1
    fi
    rm -f /app/data/.write_test
    
    echo -e "${GREEN}✓ Data directory ready${NC}"
}

run_bot() {
    print_banner
    check_config
    check_data_dir
    
    echo ""
    echo -e "${GREEN}Starting Grid Trading Bot...${NC}"
    echo ""
    
    cd /app/src
    exec python3 main.py
}

run_test_api() {
    print_banner
    check_config
    
    echo -e "${BLUE}Running API connection test...${NC}"
    echo ""
    
    cd /app/src
    python3 test_api.py
}

run_tax_summary() {
    print_banner
    check_data_dir
    
    echo -e "${BLUE}Generating tax summary...${NC}"
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
    echo "  help         Show this help message"
    echo ""
    echo "Examples:"
    echo "  # Run the bot"
    echo "  docker run -d --name gridbot \\"
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

# Main command handling
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
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac

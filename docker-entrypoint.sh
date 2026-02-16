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
    CONFIG_TEMPLATE="/app/src/priv/config.json.template"

    # Check if config file exists (Docker may create an empty dir for missing bind mounts)
    if [ ! -f "$CONFIG_FILE" ] || [ -d "$CONFIG_FILE" ]; then
        echo -e "${RED}✗${NC} Config not found: $CONFIG_FILE"
        echo ""
        if [ -f "$CONFIG_TEMPLATE" ]; then
            echo "  Your config.json is missing. Create it from the template:"
            echo ""
            echo "    cp src/priv/config.json.template src/priv/config.json"
            echo "    nano src/priv/config.json   # Add your Binance API keys"
            echo "    chmod 600 src/priv/config.json"
            echo ""
            echo "  Then restart: ./docker-helper.sh restart"
        else
            echo "  Mount your config: -v /path/to/config.json:/app/src/priv/config.json"
        fi
        exit 1
    fi

    # Check if config file is empty (happens when Docker bind-mounts a missing file)
    if [ ! -s "$CONFIG_FILE" ]; then
        echo -e "${RED}✗${NC} Config file is empty: $CONFIG_FILE"
        echo ""
        echo "  This usually happens when Docker creates an empty file because"
        echo "  config.json didn't exist before the container started."
        echo ""
        echo "  Fix:"
        echo "    1. Stop the bot:  ./docker-helper.sh stop"
        echo "    2. Remove the empty file:  rm src/priv/config.json"
        echo "    3. Create from template:   cp src/priv/config.json.template src/priv/config.json"
        echo "    4. Add your API keys:      nano src/priv/config.json"
        echo "    5. Secure it:              chmod 600 src/priv/config.json"
        echo "    6. Start the bot:          ./docker-helper.sh start"
        exit 1
    fi

    # Check if config file is readable by this user (catches bind-mount permission issues)
    if [ ! -r "$CONFIG_FILE" ]; then
        echo -e "${RED}✗${NC} Config file not readable: $CONFIG_FILE"
        echo ""
        echo "  The container user ($(whoami), UID $(id -u)) cannot read the"
        echo "  bind-mounted config file. This is a file permission mismatch"
        echo "  between your host user and the container user."
        echo ""
        echo "  Quick fix (on the host):"
        echo "    chmod 644 src/priv/config.json"
        echo ""
        echo "  Or rebuild the image (sets container UID to match Pi user):"
        echo "    ./docker-helper.sh rebuild"
        echo ""
        echo "  Then recreate the container:"
        echo "    ./docker-helper.sh stop && ./docker-helper.sh start"
        exit 1
    fi

    # Validate JSON syntax with helpful error details
    # NOTE: Use 'if !' pattern so set -e does not silently kill the script
    # before the error message can be displayed.
    if ! JSON_ERROR=$(python3 -c "import json; json.load(open('$CONFIG_FILE'))" 2>&1); then
        echo -e "${RED}✗${NC} Invalid JSON in config: $CONFIG_FILE"
        echo ""
        echo "  Parse error: $JSON_ERROR"
        echo ""
        echo "  Common issues:"
        echo "    - Trailing commas after the last item in a list/object"
        echo "    - Missing quotes around keys or string values"
        echo "    - Comments (JSON doesn't support // or /* */ comments)"
        echo ""
        echo "  Validate online: https://jsonlint.com/"
        exit 1
    fi

    # NOTE: Use 'if !' pattern here too for the same set -e reason.
    if ! API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('api_key', ''))" 2>&1); then
        echo -e "${RED}✗${NC} Failed to read API key from config: $CONFIG_FILE"
        echo ""
        echo "  Error: $API_KEY"
        exit 1
    fi

    if [ "$API_KEY" = "YOUR_BINANCE_US_API_KEY" ] || [ -z "$API_KEY" ]; then
        echo -e "${RED}✗${NC} API key not configured in $CONFIG_FILE"
        echo ""
        echo "  Edit the config and replace the placeholder API key/secret"
        echo "  with your actual Binance.US API credentials."
        echo ""
        echo "    nano src/priv/config.json"
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

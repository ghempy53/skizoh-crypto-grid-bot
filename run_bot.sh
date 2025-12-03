#!/bin/bash

##############################################################################
# Skizoh Crypto Grid Trading Bot v14.1 - Startup Script
# Enhanced with v14.1 feature checks, improved validation, and bug fixes
##############################################################################

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Color codes for pretty output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Configuration - Updated for v14.1
# IMPORTANT: All scripts must use the same BOT_DIR
BOT_DIR="$HOME/skizoh-crypto-grid-bot"
SRC_DIR="$BOT_DIR/src"
PRIV_DIR="$SRC_DIR/priv"
DATA_DIR="$BOT_DIR/data"
VENV_DIR="$BOT_DIR/venv"
MAIN_SCRIPT="$SRC_DIR/main.py"
CONFIG_FILE="$PRIV_DIR/config.json"
CONFIG_TEMPLATE="$PRIV_DIR/config.json.template"
LOG_FILE="$DATA_DIR/grid_bot.log"
TAX_FILE="$DATA_DIR/tax_transactions.csv"
POSITION_STATE_FILE="$DATA_DIR/position_state.json"

# v14.1 version info
BOT_VERSION="14.1"
BOT_NAME="Skizoh Smart Grid Bot"

##############################################################################
# Functions
##############################################################################

print_header() {
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}     ${BOLD}${BLUE}SKIZOH CRYPTO GRID TRADING BOT v${BOT_VERSION}${NC}                     ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}     ${BOLD}Smart Automated Trading with Risk Management${NC}            ${CYAN}║${NC}"
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

print_section() {
    echo ""
    echo -e "${BOLD}${BLUE}─── $1 ───${NC}"
}

# Check if running in bot directory
check_directory() {
    if [ ! -d "$BOT_DIR" ]; then
        print_error "Bot directory not found: $BOT_DIR"
        echo ""
        echo "To set up the bot, run:"
        echo "  mkdir -p $BOT_DIR/{src/priv,data,venv}"
        echo "  # Then extract v14.1 files to $BOT_DIR"
        exit 1
    fi
    cd "$BOT_DIR" || exit 1
    print_success "Bot directory: $BOT_DIR"
}

# Check directory structure
check_structure() {
    local missing=0
    
    if [ ! -d "$SRC_DIR" ]; then
        print_error "Source directory missing: $SRC_DIR"
        missing=1
    fi
    
    if [ ! -d "$PRIV_DIR" ]; then
        print_error "Private config directory missing: $PRIV_DIR"
        echo "  Create with: mkdir -p $PRIV_DIR"
        missing=1
    fi
    
    if [ ! -d "$DATA_DIR" ]; then
        print_warning "Data directory missing, creating..."
        mkdir -p "$DATA_DIR"
        print_success "Created: $DATA_DIR"
    fi
    
    if [ $missing -eq 1 ]; then
        exit 1
    fi
    
    print_success "Directory structure verified"
}

# Check virtual environment
check_virtualenv() {
    if [ ! -d "$VENV_DIR" ]; then
        print_warning "Virtual environment not found"
        echo ""
        read -p "  Create virtual environment now? (y/N): " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Creating virtual environment..."
            if python3 -m venv "$VENV_DIR"; then
                print_success "Virtual environment created"
                # Activate and install dependencies
                # shellcheck disable=SC1091
                source "$VENV_DIR/bin/activate"
                print_info "Installing dependencies..."
                pip install --upgrade pip > /dev/null 2>&1
                pip install numpy ccxt > /dev/null 2>&1
                print_success "Dependencies installed (numpy, ccxt)"
            else
                print_error "Failed to create virtual environment"
                exit 1
            fi
        else
            print_error "Virtual environment required"
            echo "  Create manually: python3 -m venv $VENV_DIR"
            exit 1
        fi
    else
        print_success "Virtual environment found"
    fi
}

# Activate virtual environment
activate_venv() {
    if [ ! -f "$VENV_DIR/bin/activate" ]; then
        print_error "Virtual environment activation script not found"
        exit 1
    fi
    
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"
    
    if [ -z "${VIRTUAL_ENV:-}" ]; then
        print_error "Failed to activate virtual environment"
        exit 1
    fi
    print_success "Virtual environment activated"
}

# Check Python dependencies
check_dependencies() {
    local missing=0
    
    # Check NumPy
    if python3 -c "import numpy" 2>/dev/null; then
        NUMPY_VER=$(python3 -c "import numpy; print(numpy.__version__)" 2>/dev/null)
        print_success "NumPy $NUMPY_VER"
    else
        print_error "NumPy not installed"
        missing=1
    fi
    
    # Check CCXT
    if python3 -c "import ccxt" 2>/dev/null; then
        CCXT_VER=$(python3 -c "import ccxt; print(ccxt.__version__)" 2>/dev/null)
        print_success "CCXT $CCXT_VER"
    else
        print_error "CCXT not installed"
        missing=1
    fi
    
    if [ $missing -eq 1 ]; then
        echo ""
        print_info "Install missing packages with:"
        echo "  pip install numpy ccxt"
        exit 1
    fi
}

# Check bot files
check_bot_files() {
    local missing=0
    
    # Required files
    local required_files=(
        "$MAIN_SCRIPT:main.py"
        "$SRC_DIR/grid_bot.py:grid_bot.py"
        "$SRC_DIR/market_analysis.py:market_analysis.py"
        "$SRC_DIR/config_manager.py:config_manager.py"
    )
    
    for file_entry in "${required_files[@]}"; do
        local filepath="${file_entry%%:*}"
        local filename="${file_entry##*:}"
        
        if [ -f "$filepath" ]; then
            print_success "$filename"
        else
            print_error "$filename not found"
            missing=1
        fi
    done
    
    # Optional files
    if [ -f "$SRC_DIR/tax_summary.py" ]; then
        print_success "tax_summary.py (optional)"
    fi
    
    if [ -f "$SRC_DIR/test_api.py" ]; then
        print_success "test_api.py (optional)"
    fi
    
    if [ $missing -eq 1 ]; then
        print_error "Missing required files. Please reinstall v14.1."
        exit 1
    fi
}

# Check config file
check_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        if [ -f "$CONFIG_TEMPLATE" ]; then
            print_warning "Config file not found"
            echo ""
            read -p "  Copy from template? (y/N): " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                cp "$CONFIG_TEMPLATE" "$CONFIG_FILE"
                chmod 600 "$CONFIG_FILE"
                print_success "Config file created from template"
                print_warning "You MUST edit $CONFIG_FILE with your API keys!"
                echo ""
                read -p "  Edit config now? (Y/n): " -n 1 -r
                echo ""
                if [[ ! $REPLY =~ ^[Nn]$ ]]; then
                    ${EDITOR:-nano} "$CONFIG_FILE"
                fi
            else
                print_error "Config file required"
                exit 1
            fi
        else
            print_error "Neither config.json nor template found!"
            exit 1
        fi
    fi
    
    # Validate JSON
    if ! python3 -c "import json; json.load(open('$CONFIG_FILE'))" 2>/dev/null; then
        print_error "config.json is not valid JSON!"
        echo "  Check for syntax errors (missing commas, quotes, etc.)"
        exit 1
    fi
    print_success "config.json valid"
    
    # Check if API keys are configured
    API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('api_key', ''))" 2>/dev/null)
    
    if [ "$API_KEY" = "YOUR_BINANCE_US_API_KEY" ] || [ -z "$API_KEY" ]; then
        print_error "API key not configured!"
        echo "  Edit: $CONFIG_FILE"
        exit 1
    fi
    print_success "API credentials configured"
    
    # Check permissions (handle both Linux and macOS stat syntax)
    if command -v stat &> /dev/null; then
        CONFIG_PERMS=$(stat -c %a "$CONFIG_FILE" 2>/dev/null || stat -f %A "$CONFIG_FILE" 2>/dev/null || echo "unknown")
        
        if [ "$CONFIG_PERMS" != "600" ] && [ "$CONFIG_PERMS" != "unknown" ]; then
            print_warning "Fixing config permissions ($CONFIG_PERMS → 600)"
            chmod 600 "$CONFIG_FILE"
        fi
    fi
    print_success "Config permissions secure (600)"
}

# Check internet connectivity
check_internet() {
    if ping -c 1 -W 3 8.8.8.8 &> /dev/null; then
        print_success "Internet connection OK"
    else
        print_error "No internet connection"
        exit 1
    fi
    
    # Test Binance.US connectivity
    if command -v curl &> /dev/null; then
        if curl -s --max-time 5 "https://api.binance.us/api/v3/ping" > /dev/null 2>&1; then
            print_success "Binance.US API reachable"
        else
            print_warning "Cannot reach Binance.US API (may be temporary)"
        fi
    fi
}

# Check for running instances
check_running_instance() {
    # Get all matching PIDs
    local pids
    pids=$(pgrep -f "python3.*main.py" 2>/dev/null || true)
    
    if [ -n "$pids" ]; then
        print_warning "Bot may already be running!"
        echo ""
        echo "  Running processes:"
        for pid in $pids; do
            if ps -p "$pid" > /dev/null 2>&1; then
                ps -p "$pid" -o pid=,pcpu=,pmem=,etime= 2>/dev/null | awk '{print "    PID: "$1" | CPU: "$2"% | MEM: "$3"% | Time: "$4}'
            fi
        done
        echo ""
        read -p "  Continue anyway? (y/N): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        fi
    fi
}

# Show system info
show_system_info() {
    echo ""
    print_info "System Status:"
    
    # Date/Time
    echo "  Time: $(date '+%Y-%m-%d %H:%M:%S %Z')"
    
    # Memory
    if command -v free &> /dev/null; then
        MEM_USED=$(free -h | awk '/^Mem:/ {print $3}')
        MEM_TOTAL=$(free -h | awk '/^Mem:/ {print $2}')
        echo "  Memory: $MEM_USED / $MEM_TOTAL"
    fi
    
    # Disk
    DISK_USAGE=$(df -h "$BOT_DIR" 2>/dev/null | awk 'NR==2 {print $5 " used (" $4 " free)"}')
    if [ -n "$DISK_USAGE" ]; then
        echo "  Disk: $DISK_USAGE"
    fi
    
    # CPU Temp (Raspberry Pi) - only if bc is available
    if [ -f /sys/class/thermal/thermal_zone0/temp ] && command -v bc &> /dev/null; then
        TEMP=$(cat /sys/class/thermal/thermal_zone0/temp 2>/dev/null)
        if [ -n "$TEMP" ]; then
            TEMP_C=$(echo "scale=1; $TEMP/1000" | bc 2>/dev/null || echo "N/A")
            echo "  CPU Temp: ${TEMP_C}°C"
        fi
    fi
    
    # Log file size
    if [ -f "$LOG_FILE" ]; then
        LOG_SIZE=$(du -h "$LOG_FILE" 2>/dev/null | cut -f1)
        echo "  Log size: $LOG_SIZE"
    fi
    
    # v14.1: Position state file
    if [ -f "$POSITION_STATE_FILE" ]; then
        print_success "Position state file: Present"
    else
        print_info "Position state file: Will be created on first run"
    fi
}

# Backup and rotate logs
manage_logs() {
    if [ -f "$LOG_FILE" ]; then
        LOG_SIZE=$(stat -c%s "$LOG_FILE" 2>/dev/null || stat -f%z "$LOG_FILE" 2>/dev/null || echo "0")
        
        # If log > 10MB, rotate
        if [ -n "$LOG_SIZE" ] && [ "$LOG_SIZE" -gt 10485760 ]; then
            BACKUP_NAME="$DATA_DIR/grid_bot_$(date +%Y%m%d_%H%M%S).log"
            
            # Use numfmt if available, otherwise show raw bytes
            if command -v numfmt &> /dev/null; then
                print_warning "Log file large ($(numfmt --to=iec "$LOG_SIZE"))"
            else
                print_warning "Log file large (${LOG_SIZE} bytes)"
            fi
            
            mv "$LOG_FILE" "$BACKUP_NAME"
            gzip "$BACKUP_NAME" 2>/dev/null || true
            print_success "Log rotated: ${BACKUP_NAME}.gz"
        fi
    fi
}

# Show v14.1 features
show_v14_features() {
    echo ""
    echo -e "${BOLD}v14.1 Features Active:${NC}"
    echo "  • FIFO Position Tracking (accurate P&L)"
    echo "  • Position State Persistence (survives restarts)"
    echo "  • ADX Trend Filter (pauses in strong trends)"
    echo "  • Fee-Aware Grid Spacing"
    echo "  • Position Exposure Limits"
    echo "  • Wilder's RSI (industry standard)"
    echo "  • Enhanced Drawdown Protection"
    echo "  • Improved Input Validation"
}

# Pre-flight checklist
preflight_checklist() {
    print_header
    
    print_section "Directory & Environment"
    check_directory
    check_structure
    check_virtualenv
    activate_venv
    
    print_section "Dependencies"
    check_dependencies
    
    print_section "Bot Files"
    check_bot_files
    
    print_section "Configuration"
    check_config
    
    print_section "Connectivity"
    check_internet
    check_running_instance
    
    print_section "System"
    manage_logs
    show_system_info
    
    show_v14_features
    
    echo ""
    print_success "All pre-flight checks passed!"
}

# Start the bot
start_bot() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${NC}              ${BOLD}STARTING GRID BOT v${BOT_VERSION}...${NC}                       ${GREEN}║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    print_info "Bot is starting. Press Ctrl+C to stop."
    print_info "Log file: $LOG_FILE"
    echo ""
    echo -e "${YELLOW}TIP: Monitor in another terminal:${NC}"
    echo "  tail -f $LOG_FILE"
    echo ""
    
    # Run the bot
    cd "$SRC_DIR" || exit 1
    python3 main.py
    
    EXIT_CODE=$?
    echo ""
    
    if [ $EXIT_CODE -eq 0 ]; then
        print_success "Bot exited cleanly"
    else
        print_error "Bot exited with error code: $EXIT_CODE"
        print_info "Check log: $LOG_FILE"
    fi
    
    deactivate 2>/dev/null || true
}

# Cleanup handler
cleanup() {
    echo ""
    print_info "Cleaning up..."
    deactivate 2>/dev/null || true
}

##############################################################################
# Main Script
##############################################################################

trap cleanup EXIT

# Parse arguments
case "${1:-}" in
    --skip-checks)
        print_header
        check_directory
        check_virtualenv
        activate_venv
        start_bot
        ;;
    --help|-h)
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --skip-checks  Skip pre-flight checks (faster startup)"
        echo "  --help, -h     Show this help message"
        echo ""
        echo "Default: Run full pre-flight checks before starting"
        exit 0
        ;;
    *)
        # Run full checks
        preflight_checklist
        
        echo ""
        echo -e "${BOLD}Ready to start. Confirm settings:${NC}"
        echo "  • Binance.US API"
        echo "  • Smart Grid Trading v14.1"
        echo "  • ADX Trend Filter: Active"
        echo "  • FIFO P&L Tracking: Active"
        echo "  • Position State Persistence: Active"
        echo "  • Position Limits: Active"
        echo ""
        read -p "Start the bot now? (Y/n): " -n 1 -r
        echo ""
        
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            start_bot
        else
            print_info "Cancelled by user"
        fi
        ;;
esac

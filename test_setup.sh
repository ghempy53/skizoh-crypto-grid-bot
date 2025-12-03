#!/bin/bash

##############################################################################
# Skizoh Crypto Grid Trading Bot v14.1 - Testing & Validation Script
# Comprehensive setup verification and API testing
##############################################################################

set -uo pipefail  # Exit on undefined vars, pipe failures (not -e for interactive)

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Configuration - MUST match run_bot.sh and monitor_bot.sh
BOT_DIR="$HOME/skizoh-grid-bot-v14"
SRC_DIR="$BOT_DIR/src"
PRIV_DIR="$SRC_DIR/priv"
DATA_DIR="$BOT_DIR/data"
VENV_DIR="$BOT_DIR/venv"
CONFIG_FILE="$PRIV_DIR/config.json"
CONFIG_TEMPLATE="$PRIV_DIR/config.json.template"
POSITION_STATE_FILE="$DATA_DIR/position_state.json"

BOT_VERSION="14.1"

##############################################################################
# Functions
##############################################################################

print_header() {
    clear
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}     ${BOLD}${BLUE}GRID BOT v${BOT_VERSION} - SETUP TESTING & VALIDATION${NC}           ${CYAN}║${NC}"
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
    echo -e "${BOLD}${CYAN}━━━ $1 ━━━${NC}"
    echo ""
}

# Basic checks
check_directory() {
    if [ ! -d "$BOT_DIR" ]; then
        print_error "Bot directory not found: $BOT_DIR"
        exit 1
    fi
    cd "$BOT_DIR" || exit 1
    print_success "Working directory: $BOT_DIR"
}

check_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        print_error "Virtual environment not found: $VENV_DIR"
        echo "  Create with: python3 -m venv $VENV_DIR"
        return 1
    fi
    print_success "Virtual environment found"
    return 0
}

activate_venv() {
    if [ ! -f "$VENV_DIR/bin/activate" ]; then
        print_error "Virtual environment activation script not found"
        return 1
    fi
    
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"
    
    if [ -z "${VIRTUAL_ENV:-}" ]; then
        print_error "Failed to activate virtual environment"
        return 1
    fi
    print_success "Virtual environment activated"
    return 0
}

# Test Python environment
test_python() {
    print_section "Python Environment"
    
    # Python version
    PYTHON_VERSION=$(python3 --version 2>&1)
    print_success "$PYTHON_VERSION"
    
    # Pip version
    PIP_VERSION=$(pip --version 2>&1 | head -n 1)
    print_success "pip: $(echo "$PIP_VERSION" | awk '{print $2}')"
    
    # Check packages
    echo ""
    print_info "Checking required packages:"
    
    # NumPy
    if python3 -c "import numpy" 2>/dev/null; then
        NUMPY_VER=$(python3 -c "import numpy; print(numpy.__version__)")
        print_success "NumPy $NUMPY_VER"
    else
        print_error "NumPy NOT installed"
        echo "  Install: pip install numpy"
    fi
    
    # CCXT
    if python3 -c "import ccxt" 2>/dev/null; then
        CCXT_VER=$(python3 -c "import ccxt; print(ccxt.__version__)")
        print_success "CCXT $CCXT_VER"
        
        # Check if Binance.US is supported
        if python3 -c "import ccxt; ccxt.binanceus()" 2>/dev/null; then
            print_success "  └─ Binance.US exchange supported"
        else
            print_warning "  └─ Binance.US support may be limited"
        fi
    else
        print_error "CCXT NOT installed"
        echo "  Install: pip install ccxt"
    fi
}

# Check directory structure
test_structure() {
    print_section "Directory Structure"
    
    local all_ok=0
    
    # Required directories
    local dirs=(
        "$BOT_DIR:Bot root"
        "$SRC_DIR:Source code"
        "$PRIV_DIR:Private config"
        "$DATA_DIR:Data/logs"
    )
    
    for dir_entry in "${dirs[@]}"; do
        local dirpath="${dir_entry%%:*}"
        local dirname="${dir_entry##*:}"
        
        if [ -d "$dirpath" ]; then
            print_success "$dirname: $dirpath"
        else
            print_error "$dirname: $dirpath (MISSING)"
            all_ok=1
        fi
    done
    
    return $all_ok
}

# Check files
test_files() {
    print_section "Required Files"
    
    local all_ok=0
    
    # Core files
    local files=(
        "$SRC_DIR/main.py:main.py (entry point)"
        "$SRC_DIR/grid_bot.py:grid_bot.py (trading engine)"
        "$SRC_DIR/market_analysis.py:market_analysis.py (indicators)"
        "$SRC_DIR/config_manager.py:config_manager.py (config)"
    )
    
    for file_entry in "${files[@]}"; do
        local filepath="${file_entry%%:*}"
        local filename="${file_entry##*:}"
        
        if [ -f "$filepath" ]; then
            print_success "$filename"
        else
            print_error "$filename (MISSING)"
            all_ok=1
        fi
    done
    
    echo ""
    print_info "Optional files:"
    
    if [ -f "$SRC_DIR/tax_summary.py" ]; then
        print_success "tax_summary.py"
    else
        print_warning "tax_summary.py (not found)"
    fi
    
    if [ -f "$SRC_DIR/test_api.py" ]; then
        print_success "test_api.py"
    else
        print_warning "test_api.py (not found)"
    fi
    
    return $all_ok
}

# Validate config
test_config() {
    print_section "Configuration"
    
    # Check file exists
    if [ ! -f "$CONFIG_FILE" ]; then
        if [ -f "$CONFIG_TEMPLATE" ]; then
            print_warning "config.json not found (template available)"
            echo "  Copy template: cp $CONFIG_TEMPLATE $CONFIG_FILE"
        else
            print_error "config.json not found (no template either!)"
        fi
        return 1
    fi
    print_success "config.json exists"
    
    # Validate JSON syntax
    if python3 -c "import json; json.load(open('$CONFIG_FILE'))" 2>/dev/null; then
        print_success "JSON syntax valid"
    else
        print_error "JSON syntax INVALID"
        echo "  Check for missing commas, quotes, brackets"
        return 1
    fi
    
    # Check API credentials
    API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('api_key', ''))" 2>/dev/null)
    API_SECRET=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('api_secret', ''))" 2>/dev/null)
    
    if [ "$API_KEY" = "YOUR_BINANCE_US_API_KEY" ] || [ -z "$API_KEY" ]; then
        print_warning "API key: NOT CONFIGURED"
    else
        KEY_PREFIX="${API_KEY:0:8}..."
        print_success "API key: Configured ($KEY_PREFIX)"
    fi
    
    if [ "$API_SECRET" = "YOUR_BINANCE_US_API_SECRET" ] || [ -z "$API_SECRET" ]; then
        print_warning "API secret: NOT CONFIGURED"
    else
        print_success "API secret: Configured (hidden)"
    fi
    
    # Check permissions (handle both Linux and macOS)
    CONFIG_PERMS=$(stat -c %a "$CONFIG_FILE" 2>/dev/null || stat -f %A "$CONFIG_FILE" 2>/dev/null || echo "unknown")
    if [ "$CONFIG_PERMS" = "600" ]; then
        print_success "Permissions: 600 (secure)"
    elif [ "$CONFIG_PERMS" = "unknown" ]; then
        print_warning "Permissions: Could not determine"
    else
        print_warning "Permissions: $CONFIG_PERMS (should be 600)"
        echo "  Fix: chmod 600 $CONFIG_FILE"
    fi
    
    # Show key config values
    echo ""
    print_info "Configuration values:"
    
    SYMBOL=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('symbol', 'N/A'))" 2>/dev/null)
    FEE_RATE=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('fee_rate', 0.001))" 2>/dev/null)
    MAX_POS=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('max_position_percent', 75))" 2>/dev/null)
    
    echo "  Symbol: $SYMBOL"
    
    # FIXED: Check if bc is available for percentage calculation
    if command -v bc &> /dev/null; then
        FEE_PCT=$(echo "$FEE_RATE * 100" | bc 2>/dev/null || echo "N/A")
        echo "  Fee rate: ${FEE_RATE} (${FEE_PCT}%)"
    else
        echo "  Fee rate: ${FEE_RATE}"
    fi
    
    echo "  Max position: ${MAX_POS}%"
    
    # Count scenarios
    NUM_SCENARIOS=$(python3 -c "import json; print(len(json.load(open('$CONFIG_FILE')).get('config_data', [])))" 2>/dev/null)
    echo "  Scenarios: $NUM_SCENARIOS available"
    
    return 0
}

# Test internet
test_internet() {
    print_section "Network Connectivity"
    
    # Basic internet
    if ping -c 1 -W 3 8.8.8.8 &> /dev/null; then
        print_success "Internet: Connected"
    else
        print_error "Internet: No connection"
        return 1
    fi
    
    # DNS
    if ping -c 1 -W 3 google.com &> /dev/null; then
        print_success "DNS: Working"
    else
        print_warning "DNS: May have issues"
    fi
    
    # Binance.US API
    if command -v curl &> /dev/null; then
        PING_RESULT=$(curl -s --max-time 5 "https://api.binance.us/api/v3/ping" 2>/dev/null)
        if [ "$PING_RESULT" = "{}" ]; then
            print_success "Binance.US API: Responding"
        else
            print_warning "Binance.US API: No response (may be temporary)"
        fi
        
        # Get server time
        SERVER_TIME=$(curl -s --max-time 5 "https://api.binance.us/api/v3/time" 2>/dev/null)
        if [ -n "$SERVER_TIME" ]; then
            print_success "Binance.US Time Sync: OK"
        fi
    else
        print_warning "curl not installed - cannot test API"
    fi
    
    return 0
}

# Run API test
run_api_test() {
    print_section "API Connection Test"
    
    if [ ! -f "$SRC_DIR/test_api.py" ]; then
        print_error "test_api.py not found"
        return 1
    fi
    
    print_info "Running API connection test..."
    echo ""
    
    cd "$SRC_DIR" || return 1
    python3 test_api.py
    
    local exit_code=$?
    echo ""
    
    if [ $exit_code -eq 0 ]; then
        print_success "API test PASSED"
    else
        print_error "API test FAILED (exit code: $exit_code)"
    fi
    
    return $exit_code
}

# Test v14.1 specific features
test_v14_features() {
    print_section "v14.1 Feature Verification"
    
    # Check for v14.1 specific code
    print_info "Checking v14.1 components..."
    
    # Position tracker
    if grep -q "class PositionTracker" "$SRC_DIR/grid_bot.py" 2>/dev/null; then
        print_success "FIFO Position Tracker: Present"
    else
        print_warning "FIFO Position Tracker: Not found"
    fi
    
    # v14.1: State persistence
    if grep -q "_load_state\|_save_state" "$SRC_DIR/grid_bot.py" 2>/dev/null; then
        print_success "Position State Persistence: Present (v14.1)"
    else
        print_warning "Position State Persistence: Not found"
    fi
    
    # ADX calculation
    if grep -q "calculate_adx" "$SRC_DIR/market_analysis.py" 2>/dev/null; then
        print_success "ADX Trend Filter: Present"
    else
        print_warning "ADX Trend Filter: Not found"
    fi
    
    # Wilder's RSI
    if grep -q "calculate_rsi_wilder" "$SRC_DIR/market_analysis.py" 2>/dev/null; then
        print_success "Wilder's RSI: Present"
    else
        print_warning "Wilder's RSI: Not found"
    fi
    
    # Exposure limits
    if grep -q "check_exposure_limits" "$SRC_DIR/grid_bot.py" 2>/dev/null; then
        print_success "Exposure Limits: Present"
    else
        print_warning "Exposure Limits: Not found"
    fi
    
    # Bollinger Bands
    if grep -q "calculate_bollinger_bands" "$SRC_DIR/market_analysis.py" 2>/dev/null; then
        print_success "Bollinger Bands: Present"
    else
        print_warning "Bollinger Bands: Not found"
    fi
    
    # Fee validation
    if grep -q "_validate_grid_spacing" "$SRC_DIR/grid_bot.py" 2>/dev/null; then
        print_success "Fee-Aware Spacing: Present"
    else
        print_warning "Fee-Aware Spacing: Not found"
    fi
    
    # v14.1: Config validation
    if grep -q "_validate_config\|_validate_scenario" "$SRC_DIR/grid_bot.py" 2>/dev/null; then
        print_success "Config Validation: Present (v14.1)"
    else
        print_warning "Config Validation: Not found"
    fi
    
    # Check position state file
    echo ""
    print_info "Data files:"
    if [ -f "$POSITION_STATE_FILE" ]; then
        print_success "Position state file: Present"
    else
        print_info "Position state file: Will be created on first trade"
    fi
}

# System information
show_system_info() {
    print_section "System Information"
    
    # OS
    if [ -f /etc/os-release ]; then
        OS_NAME=$(grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '"')
        echo "  OS: $OS_NAME"
    elif [ "$(uname)" = "Darwin" ]; then
        echo "  OS: macOS $(sw_vers -productVersion 2>/dev/null || echo 'unknown')"
    fi
    
    # Hardware (Pi detection)
    if [ -f /proc/cpuinfo ]; then
        MODEL=$(grep "Model" /proc/cpuinfo 2>/dev/null | head -n 1 | cut -d: -f2 | xargs)
        if [ -n "$MODEL" ]; then
            echo "  Hardware: $MODEL"
        fi
    fi
    
    # CPU
    CPU_CORES=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo "?")
    echo "  CPU Cores: $CPU_CORES"
    
    # Memory
    if command -v free &> /dev/null; then
        MEM_TOTAL=$(free -h | awk '/^Mem:/ {print $2}')
        MEM_AVAIL=$(free -h | awk '/^Mem:/ {print $7}')
        echo "  Memory: $MEM_AVAIL available / $MEM_TOTAL total"
    fi
    
    # Disk
    DISK_FREE=$(df -h "$BOT_DIR" 2>/dev/null | awk 'NR==2 {print $4}')
    DISK_USED=$(df -h "$BOT_DIR" 2>/dev/null | awk 'NR==2 {print $5}')
    if [ -n "$DISK_FREE" ]; then
        echo "  Disk: $DISK_FREE free ($DISK_USED used)"
    fi
    
    # Temperature (Pi) - only if bc is available
    if [ -f /sys/class/thermal/thermal_zone0/temp ] && command -v bc &> /dev/null; then
        TEMP=$(cat /sys/class/thermal/thermal_zone0/temp 2>/dev/null)
        if [ -n "$TEMP" ]; then
            TEMP_C=$(echo "scale=1; $TEMP/1000" | bc 2>/dev/null)
            echo "  CPU Temp: ${TEMP_C}°C"
        fi
    fi
    
    # Python
    PYTHON_PATH=$(which python3)
    echo "  Python: $PYTHON_PATH"
}

# Run all tests
run_all_tests() {
    local total_tests=0
    local passed_tests=0
    
    test_structure
    [ $? -eq 0 ] && ((passed_tests++))
    ((total_tests++))
    
    test_python
    ((total_tests++))
    ((passed_tests++))  # Python test doesn't return failure
    
    test_files
    [ $? -eq 0 ] && ((passed_tests++))
    ((total_tests++))
    
    test_config
    [ $? -eq 0 ] && ((passed_tests++))
    ((total_tests++))
    
    test_internet
    [ $? -eq 0 ] && ((passed_tests++))
    ((total_tests++))
    
    test_v14_features
    ((total_tests++))
    ((passed_tests++))
    
    show_system_info
    
    # Summary
    print_section "Test Summary"
    echo -e "  Tests passed: ${GREEN}$passed_tests${NC} / $total_tests"
    
    if [ $passed_tests -eq $total_tests ]; then
        echo ""
        print_success "All tests passed! Ready for API test."
    else
        echo ""
        print_warning "Some tests had issues. Review above."
    fi
}

# Interactive menu
show_menu() {
    echo ""
    echo -e "${BOLD}Select Test:${NC}"
    echo ""
    echo "  [1] Run ALL tests (recommended)"
    echo "  [2] Test Python packages only"
    echo "  [3] Validate config.json"
    echo "  [4] Test network connectivity"
    echo "  [5] Run API connection test"
    echo "  [6] Check v14.1 features"
    echo "  [7] Show system info"
    echo ""
    echo "  [Q] Quit"
    echo ""
}

# Cleanup
cleanup() {
    deactivate 2>/dev/null || true
}

##############################################################################
# Main Script
##############################################################################

trap cleanup EXIT

print_header

# Basic setup
check_directory

if ! check_venv; then
    exit 1
fi

if ! activate_venv; then
    exit 1
fi

# Handle command line arguments
case "${1:-}" in
    --all|-a)
        run_all_tests
        echo ""
        read -p "Run API test now? (y/N): " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            run_api_test
        fi
        ;;
    --api)
        run_api_test
        ;;
    --config|-c)
        test_config
        ;;
    --network|-n)
        test_internet
        ;;
    --system|-s)
        show_system_info
        ;;
    --v14|--v14.1)
        test_v14_features
        ;;
    --help|-h)
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --all, -a      Run all tests"
        echo "  --api          Run API connection test only"
        echo "  --config, -c   Validate configuration"
        echo "  --network, -n  Test network connectivity"
        echo "  --system, -s   Show system information"
        echo "  --v14, --v14.1 Check v14.1-specific features"
        echo "  --help, -h     Show this help"
        echo ""
        echo "No arguments: Interactive menu"
        exit 0
        ;;
    *)
        # Interactive mode
        while true; do
            show_menu
            read -p "Choice: " -n 1 -r
            echo ""
            
            case $REPLY in
                1)
                    run_all_tests
                    echo ""
                    read -p "Run API test? (y/N): " -n 1 -r
                    echo ""
                    if [[ $REPLY =~ ^[Yy]$ ]]; then
                        run_api_test
                    fi
                    ;;
                2)
                    test_python
                    ;;
                3)
                    test_config
                    ;;
                4)
                    test_internet
                    ;;
                5)
                    run_api_test
                    ;;
                6)
                    test_v14_features
                    ;;
                7)
                    show_system_info
                    ;;
                [Qq])
                    print_info "Goodbye!"
                    exit 0
                    ;;
                *)
                    print_error "Invalid option"
                    ;;
            esac
            
            echo ""
            read -p "Press Enter to continue..."
            print_header
        done
        ;;
esac

echo ""
print_info "Testing complete!"

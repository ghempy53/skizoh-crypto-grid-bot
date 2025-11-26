#!/bin/bash

##############################################################################
# Crypto Grid Trading Bot - Testing Script
# Tests API connection and validates setup
##############################################################################

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
BOT_DIR="$HOME/crypto_bot"
VENV_DIR="$BOT_DIR/venv"
TEST_SCRIPT="$BOT_DIR/test_api.py"
CONFIG_FILE="$BOT_DIR/config.json"

##############################################################################
# Functions
##############################################################################

print_header() {
    clear
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}   SETUP TESTING & VALIDATION${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if running in correct directory
check_directory() {
    if [ ! -d "$BOT_DIR" ]; then
        print_error "Bot directory not found: $BOT_DIR"
        exit 1
    fi
    cd "$BOT_DIR" || exit 1
    print_success "Working directory: $BOT_DIR"
}

# Check virtual environment
check_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        print_error "Virtual environment not found"
        echo "Create it with: python3 -m venv $VENV_DIR"
        exit 1
    fi
    print_success "Virtual environment found"
}

# Activate virtual environment
activate_venv() {
    print_info "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
    
    if [ -z "$VIRTUAL_ENV" ]; then
        print_error "Failed to activate virtual environment"
        exit 1
    fi
    print_success "Virtual environment activated"
}

# Test Python and dependencies
test_python() {
    echo ""
    print_info "Testing Python environment..."
    
    # Check Python version
    PYTHON_VERSION=$(python3 --version 2>&1)
    print_success "Python version: $PYTHON_VERSION"
    
    # Check pip
    PIP_VERSION=$(pip --version 2>&1 | head -n 1)
    print_success "Pip version: $PIP_VERSION"
    
    echo ""
    print_info "Checking required packages..."
    
    # Test NumPy
    if python3 -c "import numpy" 2>/dev/null; then
        NUMPY_VERSION=$(python3 -c "import numpy; print(numpy.__version__)")
        print_success "NumPy $NUMPY_VERSION - installed"
    else
        print_error "NumPy - NOT installed"
        echo "Install with: pip install numpy"
        exit 1
    fi
    
    # Test CCXT
    if python3 -c "import ccxt" 2>/dev/null; then
        CCXT_VERSION=$(python3 -c "import ccxt; print(ccxt.__version__)")
        print_success "CCXT $CCXT_VERSION - installed"
    else
        print_error "CCXT - NOT installed"
        echo "Install with: pip install ccxt"
        exit 1
    fi
}

# Check file existence
check_files() {
    echo ""
    print_info "Checking required files..."
    
    if [ -f "$TEST_SCRIPT" ]; then
        print_success "test_api.py found"
    else
        print_error "test_api.py not found"
        exit 1
    fi
    
    if [ -f "$CONFIG_FILE" ]; then
        print_success "config.json found"
    else
        print_error "config.json not found"
        exit 1
    fi
    
    if [ -f "$BOT_DIR/grid_bot.py" ]; then
        print_success "grid_bot.py found"
    else
        print_warning "grid_bot.py not found (needed to run bot)"
    fi
    
    if [ -f "$BOT_DIR/tax_summary.py" ]; then
        print_success "tax_summary.py found"
    else
        print_warning "tax_summary.py not found (optional)"
    fi
}

# Validate config.json
validate_config() {
    echo ""
    print_info "Validating configuration..."
    
    # Check if config is valid JSON
    if python3 -c "import json; json.load(open('$CONFIG_FILE'))" 2>/dev/null; then
        print_success "config.json is valid JSON"
    else
        print_error "config.json is not valid JSON!"
        echo "Check for syntax errors (missing commas, quotes, etc.)"
        exit 1
    fi
    
    # Check if API keys are set
    API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('api_key', ''))")
    
    if [ "$API_KEY" = "YOUR_BINANCE_US_API_KEY" ] || [ -z "$API_KEY" ]; then
        print_warning "API key not configured in config.json"
        echo "You need to add your real API keys before running the bot"
    else
        print_success "API key is configured"
    fi
    
    # Check permissions
    CONFIG_PERMS=$(stat -c %a "$CONFIG_FILE" 2>/dev/null || stat -f %A "$CONFIG_FILE")
    
    if [ "$CONFIG_PERMS" = "600" ]; then
        print_success "config.json permissions are secure (600)"
    else
        print_warning "config.json permissions: $CONFIG_PERMS (should be 600)"
        print_info "Fixing permissions..."
        chmod 600 "$CONFIG_FILE"
        print_success "Permissions set to 600"
    fi
}

# Test internet connectivity
test_internet() {
    echo ""
    print_info "Testing internet connectivity..."
    
    if ping -c 1 8.8.8.8 &> /dev/null; then
        print_success "Internet connection OK"
    else
        print_error "No internet connection"
        echo "The bot requires internet to connect to Binance.US"
        exit 1
    fi
    
    # Test DNS
    if ping -c 1 binance.us &> /dev/null; then
        print_success "Can reach binance.us"
    else
        print_warning "Cannot reach binance.us (might be firewall/DNS issue)"
    fi
}

# Run API connection test
run_api_test() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}   RUNNING API CONNECTION TEST${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    python3 "$TEST_SCRIPT"
    
    TEST_EXIT_CODE=$?
    
    echo ""
    if [ $TEST_EXIT_CODE -eq 0 ]; then
        print_success "API test completed successfully!"
        return 0
    else
        print_error "API test failed (exit code: $TEST_EXIT_CODE)"
        return 1
    fi
}

# System information
show_system_info() {
    echo ""
    print_info "System Information:"
    
    # CPU info (Raspberry Pi)
    if [ -f /proc/cpuinfo ]; then
        MODEL=$(cat /proc/cpuinfo | grep "Model" | head -n 1 | cut -d: -f2 | xargs)
        if [ ! -z "$MODEL" ]; then
            echo "  Hardware: $MODEL"
        fi
    fi
    
    # Memory
    MEM_TOTAL=$(free -h | awk '/^Mem:/ {print $2}')
    MEM_AVAIL=$(free -h | awk '/^Mem:/ {print $7}')
    echo "  Memory: $MEM_AVAIL available / $MEM_TOTAL total"
    
    # Disk space
    DISK_FREE=$(df -h "$BOT_DIR" | awk 'NR==2 {print $4}')
    echo "  Disk Space: $DISK_FREE free"
    
    # Temperature (Pi specific)
    if [ -f /sys/class/thermal/thermal_zone0/temp ]; then
        TEMP=$(cat /sys/class/thermal/thermal_zone0/temp)
        TEMP=$(echo "scale=1; $TEMP/1000" | bc)
        echo "  CPU Temp: ${TEMP}°C"
    fi
}

# Main menu
show_menu() {
    echo ""
    echo -e "${YELLOW}========================================${NC}"
    echo -e "${YELLOW}   TESTING OPTIONS${NC}"
    echo -e "${YELLOW}========================================${NC}"
    echo ""
    echo "  [1] Run full system check (recommended first)"
    echo "  [2] Run API connection test only"
    echo "  [3] Validate config.json"
    echo "  [4] Check Python packages"
    echo "  [5] Show system information"
    echo "  [6] Run all tests"
    echo "  [Q] Quit"
    echo ""
}

# Cleanup
cleanup() {
    deactivate 2>/dev/null
}

##############################################################################
# Main Script
##############################################################################

trap cleanup EXIT

print_header

# Always do basic checks
check_directory
check_venv
activate_venv

# If no arguments, show menu
if [ $# -eq 0 ]; then
    show_menu
    read -p "Choose option: " -n 1 -r
    echo ""
    
    case $REPLY in
        1)
            test_python
            check_files
            validate_config
            test_internet
            show_system_info
            echo ""
            print_success "System check complete!"
            echo ""
            read -p "Run API test now? (y/N): " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                run_api_test
            fi
            ;;
        2)
            run_api_test
            ;;
        3)
            validate_config
            ;;
        4)
            test_python
            ;;
        5)
            show_system_info
            ;;
        6)
            test_python
            check_files
            validate_config
            test_internet
            show_system_info
            run_api_test
            ;;
        [Qq])
            print_info "Exiting..."
            exit 0
            ;;
        *)
            print_error "Invalid option"
            exit 1
            ;;
    esac
else
    # If arguments provided, run specific tests
    case $1 in
        --api)
            run_api_test
            ;;
        --full)
            test_python
            check_files
            validate_config
            test_internet
            show_system_info
            run_api_test
            ;;
        --system)
            show_system_info
            ;;
        *)
            echo "Usage: $0 [--api|--full|--system]"
            echo "  --api    : Run API connection test only"
            echo "  --full   : Run all tests"
            echo "  --system : Show system information"
            echo "  (no args): Interactive menu"
            exit 1
            ;;
    esac
fi

echo ""
print_info "Testing complete!"

#!/bin/bash

#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  ÆÆÆÆÆÆÆÆ   #  #  #  #  #  #  #  #  #  #  #  #                            
#                                                          ÆÆÆÆÆÆÆÆÆÆÆÆÆ                                #
# ÆÆÆÆÆÆÆÆÆÆÆÆÆÆ    ÆÆÆÆÆ    ÆÆÆÆÆÆ  ÆÆÆÆÆ   ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ          ÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ   ÆÆÆÆÆ   ÆÆÆÆÆÆ   ÆÆÆÆÆ   ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ   ÆÆÆÆÆÆÆÆÆÆÆÆ      ÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ   ÆÆÆÆÆ   ÆÆÆÆÆ    ÆÆÆÆÆ   ÆÆÆÆÆÆÆÆÆÆÆÆÆ ÆÆÆÆÆ        ÆÆÆÆÆÆÆÆÆÆ    ÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆ     ÆÆÆÆ    ÆÆÆÆÆ  ÆÆÆÆÆÆ    ÆÆÆÆÆ          ÆÆÆÆÆÆ ÆÆÆÆÆ           ÆÆÆÆÆÆÆÆÆ  ÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆ     ÆÆÆ     ÆÆÆÆÆ ÆÆÆÆÆÆ     ÆÆÆÆÆ         ÆÆÆÆÆÆ  ÆÆÆÆÆ     ÆÆ  ÆÆ    ÆÆÆÆÆÆ ÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆ     Æ       ÆÆÆÆÆ ÆÆÆÆÆ      ÆÆÆÆÆ         ÆÆÆÆÆ   ÆÆÆÆÆ     ÆÆ  ÆÆÆ    ÆÆÆÆÆ ÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆÆÆ           ÆÆÆÆÆÆÆÆÆÆ       ÆÆÆÆÆ        ÆÆÆÆÆÆ   ÆÆÆÆÆ     ÆÆÆ ÆÆÆ     ÆÆÆÆÆÆÆÆÆÆÆ     ÆÆÆÆÆ  #
#  ÆÆÆÆÆÆÆ          ÆÆÆÆÆÆÆÆÆÆ       ÆÆÆÆÆ       ÆÆÆÆÆÆ    ÆÆÆÆÆ     ÆÆÆ ÆÆÆ  Æ  ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ  #
#    ÆÆÆÆÆÆÆ        ÆÆÆÆÆÆÆÆÆ        ÆÆÆÆÆ       ÆÆÆÆÆÆ    ÆÆÆÆÆ ÆÆÆÆ        ÆÆ  ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ  #
#      ÆÆÆÆÆÆÆ      ÆÆÆÆÆÆÆÆÆ        ÆÆÆÆÆ      ÆÆÆÆÆÆ     ÆÆÆÆÆ  ÆÆÆ       ÆÆÆ  ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ  #
#       ÆÆÆÆÆÆÆÆ    ÆÆÆÆÆÆÆÆÆÆ       ÆÆÆÆÆ      ÆÆÆÆÆ      ÆÆÆÆÆ   ÆÆÆ     ÆÆÆ   ÆÆÆÆÆÆÆÆÆÆÆ     ÆÆÆÆÆ  #
#         ÆÆÆÆÆÆÆ   ÆÆÆÆÆÆÆÆÆÆÆ      ÆÆÆÆÆ     ÆÆÆÆÆÆ       ÆÆÆÆÆ   ÆÆÆÆÆÆÆ ÆÆÆ  ÆÆÆÆÆÆÆÆÆÆÆ     ÆÆÆÆÆ  #
#    ÆÆ     ÆÆÆÆÆ   ÆÆÆÆÆ ÆÆÆÆÆÆ     ÆÆÆÆÆ    ÆÆÆÆÆÆ        ÆÆÆÆÆ        ÆÆÆÆÆÆ  ÆÆÆÆÆÆÆÆÆÆÆ     ÆÆÆÆÆ  #
#  ÆÆÆÆ     ÆÆÆÆÆ   ÆÆÆÆÆ  ÆÆÆÆÆÆ    ÆÆÆÆÆ   ÆÆÆÆÆÆ          ÆÆÆÆÆ        ÆÆÆÆÆ  ÆÆÆÆÆÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆ     ÆÆÆÆÆ   ÆÆÆÆÆ   ÆÆÆÆÆ    ÆÆÆÆÆ   ÆÆÆÆÆÆ          ÆÆÆÆÆÆÆÆÆÆÆ    ÆÆÆ  ÆÆÆÆ ÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ   ÆÆÆÆÆ   ÆÆÆÆÆÆ   ÆÆÆÆÆ  ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ   ÆÆÆÆÆÆÆÆÆÆÆÆÆ      ÆÆÆÆ ÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ   ÆÆÆÆÆ    ÆÆÆÆÆÆ  ÆÆÆÆÆ  ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ    ÆÆÆÆÆÆÆÆÆÆÆÆÆ    ÆÆÆÆÆ ÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆÆÆÆÆÆÆÆÆÆ    ÆÆÆÆÆ     ÆÆÆÆÆÆ ÆÆÆÆÆ  ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ     ÆÆÆÆÆÆÆÆÆÆÆÆÆ   ÆÆÆÆÆ ÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ   ÆÆÆÆÆ    ÆÆÆÆÆÆÆÆÆÆ   ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ  #
# ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ  ÆÆÆÆÆÆÆÆ ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ  #
# ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ  #
#                                                                     ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ                  #
#                                                                       ÆÆÆ  ÆÆÆÆÆÆÆ                    #    
#                                                                        ÆÆÆÆ   ÆÆÆ                     #
#                                                                         ÆÆÆÆÆÆÆÆ                      #
#                                                                          ÆÆÆÆÆÆ                       #
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #   ÆÆÆÆ   #  #  #  #  #  #  #  #

##############################################################################
# Crypto Grid Trading Bot - Startup Script
# This script handles all the setup needed to run the bot safely
##############################################################################

# Color codes for pretty output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BOT_DIR="$HOME/skizoh-crypto-grid-bot"
VENV_DIR="$BOT_DIR/venv"
BOT_SCRIPT="$BOT_DIR/src/grid_bot.py"
CONFIG_FILE="$BOT_DIR/config.json"
LOG_FILE="$BOT_DIR/logs/grid_bot.log"

##############################################################################
# Functions
##############################################################################

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}   SKIZOH CRYPTO GRID BOT STARTUP${NC}"
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

# Check if running in bot directory
check_directory() {
    if [ ! -d "$BOT_DIR" ]; then
        print_error "Bot directory not found: $BOT_DIR"
        echo "Please create it with: mkdir -p $BOT_DIR"
        exit 1
    fi
    cd "$BOT_DIR" || exit 1
    print_success "Changed to bot directory: $BOT_DIR"
}

# Check if virtual environment exists
check_virtualenv() {
    if [ ! -d "$VENV_DIR" ]; then
        print_error "Virtual environment not found: $VENV_DIR"
        echo "Please create it with: python3 -m venv $VENV_DIR"
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
    print_success "Virtual environment activated: $VIRTUAL_ENV"
}

# Check if required Python packages are installed
check_dependencies() {
    print_info "Checking Python dependencies..."
    
    # Check NumPy
    python3 -c "import numpy" 2>/dev/null
    if [ $? -ne 0 ]; then
        print_error "NumPy not installed"
        echo "Install with: pip install numpy"
        exit 1
    fi
    print_success "NumPy is installed"
    
    # Check CCXT
    python3 -c "import ccxt" 2>/dev/null
    if [ $? -ne 0 ]; then
        print_error "CCXT not installed"
        echo "Install with: pip install ccxt"
        exit 1
    fi
    print_success "CCXT is installed"
}

# Check if bot script exists
check_bot_files() {
    if [ ! -f "$BOT_SCRIPT" ]; then
        print_error "Bot script not found: $BOT_SCRIPT"
        exit 1
    fi
    print_success "Bot script found"
    
    if [ ! -f "$CONFIG_FILE" ]; then
        print_error "Config file not found: $CONFIG_FILE"
        exit 1
    fi
    print_success "Config file found"
}

# Check config file permissions
check_permissions() {
    CONFIG_PERMS=$(stat -c %a "$CONFIG_FILE" 2>/dev/null || stat -f %A "$CONFIG_FILE")
    
    if [ "$CONFIG_PERMS" != "600" ]; then
        print_warning "Config file permissions are $CONFIG_PERMS (should be 600)"
        print_info "Fixing permissions..."
        chmod 600 "$CONFIG_FILE"
        print_success "Permissions fixed to 600"
    else
        print_success "Config file permissions are secure (600)"
    fi
}

# Check internet connectivity
check_internet() {
    print_info "Checking internet connectivity..."
    
    if ping -c 1 8.8.8.8 &> /dev/null; then
        print_success "Internet connection OK"
    else
        print_error "No internet connection detected"
        echo "The bot requires internet to connect to Binance.US"
        exit 1
    fi
}

# Check if another instance is running
check_running_instance() {
    if pgrep -f "python3.*grid_bot.py" > /dev/null; then
        print_warning "Bot may already be running!"
        echo ""
        echo "Running bot processes:"
        ps aux | grep "python3.*grid_bot.py" | grep -v grep
        echo ""
        read -p "Do you want to continue anyway? (y/N): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Exiting..."
            exit 0
        fi
    fi
}

# Display system info
show_system_info() {
    echo ""
    print_info "System Information:"
    echo "  Hostname: $(hostname)"
    echo "  Date/Time: $(date)"
    echo "  Uptime: $(uptime -p)"
    
    # Memory
    MEM_TOTAL=$(free -h | awk '/^Mem:/ {print $2}')
    MEM_USED=$(free -h | awk '/^Mem:/ {print $3}')
    MEM_FREE=$(free -h | awk '/^Mem:/ {print $4}')
    echo "  Memory: $MEM_USED used / $MEM_TOTAL total ($MEM_FREE free)"
    
    # Disk
    DISK_USAGE=$(df -h "$BOT_DIR" | awk 'NR==2 {print $5}')
    echo "  Disk Usage: $DISK_USAGE"
    
    # CPU Temperature (Raspberry Pi specific)
    if [ -f /sys/class/thermal/thermal_zone0/temp ]; then
        TEMP=$(cat /sys/class/thermal/thermal_zone0/temp)
        TEMP=$(echo "scale=1; $TEMP/1000" | bc)
        echo "  CPU Temperature: ${TEMP}°C"
    fi
    echo ""
}

# Backup existing log if too large
backup_log() {
    if [ -f "$LOG_FILE" ]; then
        LOG_SIZE=$(stat -c%s "$LOG_FILE" 2>/dev/null || stat -f%z "$LOG_FILE")
        # If log is larger than 10MB (10485760 bytes)
        if [ "$LOG_SIZE" -gt 10485760 ]; then
            BACKUP_NAME="$BOT_DIR/grid_bot_$(date +%Y%m%d_%H%M%S).log"
            print_warning "Log file is large ($(numfmt --to=iec $LOG_SIZE))"
            print_info "Backing up to: $BACKUP_NAME"
            mv "$LOG_FILE" "$BACKUP_NAME"
            print_success "Log backed up and reset"
        fi
    fi
}

# Display pre-flight checklist
preflight_checklist() {
    echo ""
    print_header
    echo -e "${YELLOW}PRE-FLIGHT CHECKLIST:${NC}"
    echo ""
    
    check_directory
    check_virtualenv
    activate_venv
    check_dependencies
    check_bot_files
    check_permissions
    check_internet
    check_running_instance
    backup_log
    show_system_info
    
    print_success "All pre-flight checks passed!"
    echo ""
}

# Start the bot
start_bot() {
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  STARTING SKIZOH CRYPTO GRID BOT...${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    
    print_info "Bot is now running. Press Ctrl+C to stop."
    print_info "Logs are being written to: $LOG_FILE"
    echo ""
    echo -e "${YELLOW}TIP: Open another terminal and run 'tail -f $LOG_FILE' to watch live logs${NC}"
    echo ""
    
    # Run the bot
    python3 "$BOT_SCRIPT"
    
    # This only runs if bot exits
    EXIT_CODE=$?
    echo ""
    if [ $EXIT_CODE -eq 0 ]; then
        print_success "Bot exited cleanly"
    else
        print_error "Bot exited with error code: $EXIT_CODE"
        print_info "Check the log file for details: $LOG_FILE"
    fi
    
    # Deactivate virtual environment
    deactivate 2>/dev/null
}

# Handle cleanup on exit
cleanup() {
    echo ""
    print_info "Cleaning up..."
    deactivate 2>/dev/null
    print_success "Goodbye!"
}

##############################################################################
# Main Script
##############################################################################

# Set up trap to handle cleanup on exit
trap cleanup EXIT

# Run pre-flight checks
preflight_checklist

# Final confirmation
echo -e "${YELLOW}Ready to start bot. Confirm your settings:${NC}"
echo "  • Using Binance.US API"
echo "  • Trading on spot market (no leverage)"
echo "  • Stop loss: 20%"
echo "  • Volatility filter: Active"
echo ""
read -p "Start the bot now? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    start_bot
else
    print_info "Start cancelled by user"
    exit 0
fi

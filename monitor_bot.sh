#!/bin/bash

##############################################################################
# Skizoh Crypto Grid Trading Bot v14.1 - Monitor Script
# Quick status check for your running bot
##############################################################################

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# FIXED: Use same directory as run_bot.sh and test_setup.sh
BOT_DIR="$HOME/skizoh-crypto-grid-bot"
SRC_DIR="$BOT_DIR/src"
DATA_DIR="$BOT_DIR/data"
VENV_DIR="$BOT_DIR/venv"
LOG_FILE="$DATA_DIR/grid_bot.log"
POSITION_STATE_FILE="$DATA_DIR/position_state.json"
TAX_FILE="$DATA_DIR/tax_transactions.csv"

BOT_VERSION="14.1"

##############################################################################
# Functions
##############################################################################

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

show_header() {
    clear
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}     ${BOLD}${BLUE}GRID BOT v${BOT_VERSION} - STATUS MONITOR${NC}                        ${CYAN}║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

show_bot_status() {
    echo -e "${BOLD}Bot Process Status:${NC}"
    echo ""
    
    # FIXED: Handle multiple PIDs properly
    local pids
    pids=$(pgrep -f "python3.*main.py" 2>/dev/null || true)
    
    if [ -n "$pids" ]; then
        echo -e "${GREEN}✓ Bot Status: RUNNING${NC}"
        echo ""
        
        # Loop through each PID
        local count=0
        for pid in $pids; do
            ((count++))
            if ps -p "$pid" > /dev/null 2>&1; then
                local uptime cpu mem
                uptime=$(ps -p "$pid" -o etime= 2>/dev/null | xargs || echo "N/A")
                cpu=$(ps -p "$pid" -o %cpu= 2>/dev/null | xargs || echo "N/A")
                mem=$(ps -p "$pid" -o %mem= 2>/dev/null | xargs || echo "N/A")
                
                if [ $count -gt 1 ]; then
                    print_warning "Multiple instances detected!"
                fi
                echo "  Instance #$count:"
                echo "    PID: $pid"
                echo "    Uptime: $uptime"
                echo "    CPU Usage: ${cpu}%"
                echo "    Memory Usage: ${mem}%"
                echo ""
            fi
        done
        
        if [ $count -gt 1 ]; then
            echo ""
            print_warning "WARNING: $count bot instances running. Consider stopping extras."
            echo "  Stop all: pkill -f 'python3.*main.py'"
        fi
    else
        echo -e "${RED}✗ Bot Status: NOT RUNNING${NC}"
        echo ""
        echo "  Start with: ./run_bot.sh"
    fi
}

show_log_preview() {
    echo ""
    echo -e "${BOLD}Recent Activity (last 10 lines):${NC}"
    echo "─────────────────────────────────"
    
    if [ -f "$LOG_FILE" ]; then
        tail -n 10 "$LOG_FILE"
        echo "─────────────────────────────────"
        
        # Show log file size
        local log_size
        log_size=$(du -h "$LOG_FILE" 2>/dev/null | cut -f1 || echo "unknown")
        echo "  Log size: $log_size"
    else
        print_warning "No log file found at $LOG_FILE"
    fi
}

show_position_status() {
    echo ""
    echo -e "${BOLD}Position State (v14.1):${NC}"
    
    if [ -f "$POSITION_STATE_FILE" ]; then
        if command -v python3 &> /dev/null; then
            python3 -c "
import json
try:
    with open('$POSITION_STATE_FILE') as f:
        state = json.load(f)
    qty = state.get('total_quantity', 0)
    cost = state.get('total_cost', 0)
    realized = state.get('realized_pnl', 0)
    fees = state.get('total_fees_paid', 0)
    positions = len(state.get('positions', []))
    avg = cost / qty if qty > 0 else 0
    
    print(f'  Total Quantity: {qty:.8f}')
    print(f'  Total Cost: \${cost:.2f}')
    print(f'  Average Cost: \${avg:.2f}')
    print(f'  Realized P&L: \${realized:.2f}')
    print(f'  Total Fees: \${fees:.2f}')
    print(f'  Open Positions: {positions}')
except Exception as e:
    print(f'  Error reading state: {e}')
" 2>/dev/null || print_warning "Could not parse position state"
        else
            print_warning "Python3 not available for parsing"
        fi
    else
        print_info "No position state file (will be created on first trade)"
    fi
}

show_menu() {
    echo ""
    echo -e "${BOLD}Quick Actions:${NC}"
    echo ""
    echo "  [1] View live logs (tail -f)"
    echo "  [2] View full log file"
    echo "  [3] Show last 50 lines"
    echo "  [4] Check for errors"
    echo "  [5] Generate tax summary"
    echo "  [6] View position state"
    echo "  [7] Refresh status"
    echo ""
    echo "  [S] Stop bot (graceful)"
    echo "  [K] Kill bot (force)"
    echo "  [Q] Quit"
    echo ""
}

stop_bot_graceful() {
    local pids
    pids=$(pgrep -f "python3.*main.py" 2>/dev/null || true)
    
    if [ -z "$pids" ]; then
        print_warning "Bot is not running"
        return
    fi
    
    print_info "Sending SIGTERM (graceful shutdown)..."
    for pid in $pids; do
        kill -TERM "$pid" 2>/dev/null && echo "  Sent SIGTERM to PID $pid"
    done
    
    echo "  Waiting for bot to exit..."
    sleep 3
    
    # Check if still running
    pids=$(pgrep -f "python3.*main.py" 2>/dev/null || true)
    if [ -z "$pids" ]; then
        print_success "Bot stopped successfully"
    else
        print_warning "Bot still running. Use [K] to force kill."
    fi
}

stop_bot_force() {
    local pids
    pids=$(pgrep -f "python3.*main.py" 2>/dev/null || true)
    
    if [ -z "$pids" ]; then
        print_warning "Bot is not running"
        return
    fi
    
    echo ""
    read -p "Force kill all bot processes? (y/N): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Sending SIGKILL (force)..."
        for pid in $pids; do
            kill -9 "$pid" 2>/dev/null && echo "  Killed PID $pid"
        done
        print_success "Bot processes killed"
    else
        print_info "Cancelled"
    fi
}

run_tax_summary() {
    # FIXED: Verify directories exist before changing
    if [ ! -d "$SRC_DIR" ]; then
        print_error "Source directory not found: $SRC_DIR"
        return 1
    fi
    
    if [ ! -f "$SRC_DIR/tax_summary.py" ]; then
        print_error "tax_summary.py not found"
        return 1
    fi
    
    # FIXED: Use absolute path for venv activation
    if [ ! -f "$VENV_DIR/bin/activate" ]; then
        print_error "Virtual environment not found: $VENV_DIR"
        return 1
    fi
    
    echo ""
    print_info "Generating tax summary..."
    echo ""
    
    (
        cd "$SRC_DIR" || exit 1
        # shellcheck disable=SC1091
        source "$VENV_DIR/bin/activate"
        python3 tax_summary.py
        deactivate 2>/dev/null || true
    )
}

view_position_state() {
    if [ ! -f "$POSITION_STATE_FILE" ]; then
        print_warning "No position state file found"
        return
    fi
    
    echo ""
    echo -e "${BOLD}Full Position State:${NC}"
    echo "─────────────────────────────────"
    
    if command -v python3 &> /dev/null; then
        python3 -c "
import json
with open('$POSITION_STATE_FILE') as f:
    state = json.load(f)
print(json.dumps(state, indent=2))
" 2>/dev/null || cat "$POSITION_STATE_FILE"
    else
        cat "$POSITION_STATE_FILE"
    fi
    
    echo "─────────────────────────────────"
}

##############################################################################
# Main Script
##############################################################################

show_header
show_bot_status
show_log_preview
show_position_status

while true; do
    show_menu
    read -p "Choose option: " -n 1 -r
    echo ""
    
    case $REPLY in
        1)
            if [ -f "$LOG_FILE" ]; then
                echo ""
                print_info "Showing live logs (Ctrl+C to exit)..."
                sleep 1
                tail -f "$LOG_FILE"
            else
                print_error "Log file not found"
            fi
            ;;
        2)
            if [ -f "$LOG_FILE" ]; then
                less "$LOG_FILE"
            else
                print_error "Log file not found"
            fi
            ;;
        3)
            if [ -f "$LOG_FILE" ]; then
                echo ""
                tail -n 50 "$LOG_FILE"
            else
                print_error "Log file not found"
            fi
            ;;
        4)
            echo ""
            echo -e "${YELLOW}Searching for errors...${NC}"
            echo ""
            if [ -f "$LOG_FILE" ]; then
                grep -i "error\|failed\|exception\|traceback" "$LOG_FILE" | tail -n 20 || echo "No errors found!"
            else
                print_error "Log file not found"
            fi
            ;;
        5)
            run_tax_summary
            ;;
        6)
            view_position_state
            ;;
        7)
            show_header
            show_bot_status
            show_log_preview
            show_position_status
            ;;
        [Ss])
            stop_bot_graceful
            ;;
        [Kk])
            stop_bot_force
            ;;
        [Qq])
            echo ""
            print_info "Goodbye!"
            exit 0
            ;;
        *)
            print_error "Invalid option"
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
    show_header
    show_bot_status
    show_log_preview
    show_position_status
done

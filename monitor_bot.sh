#!/bin/bash

##############################################################################
# Skizoh Crypto Grid Trading Bot - Monitor Script
# Quick status check for your running bot
##############################################################################

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

BOT_DIR="$HOME/skizoh-crypto-grid-bot"
SRC_DIR="$BOT_DIR/src"
DATA_DIR="$BOT_DIR/data"
LOG_FILE="$DATA_DIR/grid_bot.log"

clear
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   BOT STATUS MONITOR${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if bot is running
if pgrep -f "python3.*main.py" > /dev/null; then
    echo -e "${GREEN}✓ Bot Status: RUNNING${NC}"
    
    # Get process info
    BOT_PID=$(pgrep -f "python3.*main.py")
    BOT_UPTIME=$(ps -p $BOT_PID -o etime= | xargs)
    BOT_CPU=$(ps -p $BOT_PID -o %cpu= | xargs)
    BOT_MEM=$(ps -p $BOT_PID -o %mem= | xargs)
    
    echo "  PID: $BOT_PID"
    echo "  Uptime: $BOT_UPTIME"
    echo "  CPU Usage: ${BOT_CPU}%"
    echo "  Memory Usage: ${BOT_MEM}%"
else
    echo -e "${RED}✗ Bot Status: NOT RUNNING${NC}"
fi

echo ""

# Recent log entries
if [ -f "$LOG_FILE" ]; then
    echo -e "${BLUE}Recent Activity (last 10 lines):${NC}"
    echo "---"
    tail -n 10 "$LOG_FILE"
    echo "---"
else
    echo -e "${YELLOW}No log file found at $LOG_FILE${NC}"
fi

echo ""
echo -e "${BLUE}Quick Actions:${NC}"
echo "  [1] View live logs (tail -f)"
echo "  [2] View full log file"
echo "  [3] Show last 50 lines"
echo "  [4] Check for errors"
echo "  [5] Generate tax summary"
echo "  [Q] Quit"
echo ""

read -p "Choose option: " -n 1 -r
echo ""

case $REPLY in
    1)
        echo "Showing live logs (Ctrl+C to exit)..."
        sleep 1
        tail -f "$LOG_FILE"
        ;;
    2)
        less "$LOG_FILE"
        ;;
    3)
        tail -n 50 "$LOG_FILE"
        ;;
    4)
        echo -e "${YELLOW}Searching for errors...${NC}"
        grep -i "error\|failed\|exception" "$LOG_FILE" | tail -n 20
        ;;
    5)
        cd "$SRC_DIR"
        source ../venv/bin/activate
        python3 tax_summary.py
        deactivate
        ;;
    [Qq])
        echo "Goodbye!"
        ;;
    *)
        echo "Invalid option"
        ;;
esac

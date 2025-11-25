#!/bin/bash
while true; do
    python3 grid_bot.py
    echo "Bot crashed, restarting in 10 seconds..."
    sleep 10
done

# skizoh-crypto-grid-bot
Crypto Grid Bot

# Safety Features (Most Important!):
Stop-loss at 15% - Automatically closes everything if you're down 15%
Position limits - Only 5% of balance per trade
Total exposure cap - Max 60% of your balance at risk
Volatility filter - Pauses trading during extreme market moves

# How it works:
Creates a grid of buy/sell orders around current price
When a buy order fills, it places a sell order above it (and vice versa)
Profits from price oscillations within the grid
Uses 3x leverage (configurable, keep it low!)

# To get started:
Install dependencies: pip install ccxt numpy
Get Binance Futures API keys (with futures trading enabled)
Update config.json with your API keys
Test with SMALL amounts first!
Run: python grid_bot.py

# Key config settings to adjust:
grid_spacing_percent: 0.5% between levels (tighter = more trades)
leverage: Start at 2-3x, not higher
max_position_percent: 5% per trade
symbol: ETH/USDT is less volatile than BTC

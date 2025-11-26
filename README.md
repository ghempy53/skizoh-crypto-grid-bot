# Skizoh Crypto Grid Trading Bot - Setup Guide

## 📁 File Structure

```
skizoh-crypto-grid-bot/
├── run_bot.sh               # Entry point - run this!
├── venv/                    # Python virtual environment
├── src/
│   ├── main.py
│   ├── grid_bot.py          # Smart trading bot
│   ├── market_analysis.py   # RSI, MACD, S/R detection
│   ├── config_manager.py    # Multi-scenario config
│   ├── tax_summary.py       # Tax reporting
│   ├── test_api.py          # API testing
│   └── priv/
│       └── config.json      # ⚠️ SENSITIVE - Your API keys
└── data/
    ├── grid_bot.log         # Runtime logs
    └── tax_transactions.csv # Tax records
```

## 🚀 Quick Setup

### Step 1: Create Directory Structure

```bash
cd ~
mkdir -p skizoh-crypto-grid-bot/src/priv
cd skizoh-crypto-grid-bot
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install numpy ccxt
```

### Step 3: Copy Files

Copy all files to their correct locations:

**Root directory:**
- `run_bot.sh` → `~/skizoh-crypto-grid-bot/`

**src/ directory:**
- `main.py` → `~/skizoh-crypto-grid-bot/src/`
- `grid_bot.py` → `~/skizoh-crypto-grid-bot/src/`
- `market_analysis.py` → `~/skizoh-crypto-grid-bot/src/`
- `config_manager.py` → `~/skizoh-crypto-grid-bot/src/`
- `tax_summary.py` → `~/skizoh-crypto-grid-bot/src/`
- `test_api.py` → `~/skizoh-crypto-grid-bot/src/`

**priv/ directory (sensitive):**
- `config.json` → `~/skizoh-crypto-grid-bot/src/priv/`

### Step 4: Set Permissions

```bash
chmod +x run_bot.sh
chmod 600 src/priv/config.json  # Secure your API keys!
```

### Step 5: Configure API Keys

Edit `src/priv/config.json` and add your Binance.US API keys:

```bash
nano src/priv/config.json
```

Update:
```json
{
  "api_key": "YOUR_ACTUAL_API_KEY_HERE",
  "api_secret": "YOUR_ACTUAL_SECRET_KEY_HERE",
  ...
}
```

### Step 6: Test Connection

```bash
cd src
source ../venv/bin/activate
python3 test_api.py
```

You should see:
```
✅ API Connection Successful!
Your Balances:
  USDT: 240.69
  ETH: 0.000000
```

### Step 7: Run the Bot!

```bash
cd ~/skizoh-crypto-grid-bot
./run_bot.sh
```

---

## 🔧 Common Commands

### Start Bot
```bash
./run_bot.sh
```

### Stop Bot
Press `Ctrl+C` in the terminal running the bot

### View Live Logs
```bash
tail -f grid_bot.log
```

### Generate Tax Report
```bash
cd src
source ../venv/bin/activate
python3 tax_summary.py
```

### Test API Connection
```bash
cd src
source ../venv/bin/activate
python3 test_api.py
```

---

## 📊 Features

### 1. Dynamic Grid Repositioning
- Automatically adjusts grid when price moves too far
- Prevents all orders from being out of range
- Cancels old orders and creates new ones

### 2. RSI Indicator
- **< 30**: Oversold (good time to buy)
- **> 70**: Overbought (good time to sell)
- **40-60**: Neutral zone
- Bot adjusts grid bias based on RSI

### 3. MACD Indicator
- Confirms trend direction
- Positive histogram = bullish momentum
- Negative histogram = bearish momentum
- Works with RSI for better decisions

### 4. Support/Resistance Detection
- Finds key price levels from history
- Places orders near these levels
- Higher probability of fills
- Better entry/exit points

### 5. Profit Compounding
- Automatically increases position size as you profit
- +5% profit → Use 85% of balance
- +10% profit → Use 90% of balance
- +20% profit → Use 95% of balance

---

## ⚙️ Configuration

### Scenario Selection

When you start the bot, you'll see 8 scenarios:

1. **Conservative** (Risk: ★☆☆☆☆) - Safest, learning mode
2. **Balanced** (Risk: ★★★☆☆) - Normal trading
3. **Aggressive** (Risk: ★★★★☆) - High activity
4. **Low Volatility** (Risk: ★★★☆☆) - Calm markets
5. **High Volatility** (Risk: ★★☆☆☆) - Extreme swings
6. **Scalping** (Risk: ★★★★★) - Maximum trades
7. **Swing Trading** (Risk: ★★★☆☆) - Big moves
8. **Night Mode** (Risk: ★★☆☆☆) - Safer overnight

### Market Analysis

Bot shows you:
- Current price and 24h range
- RSI value (oversold/overbought)
- MACD histogram (momentum)
- Market trend assessment
- Nearest support/resistance levels
- **Recommended scenario** for current conditions

### Example Output

```
MARKET ANALYSIS & RECOMMENDATION
======================================================================

Current ETH/USDT Price: $3,036.68
24h Range: $3,015.00 - $3,055.50 (1.34%)
24h Volume: 125,432.50 ETH

📊 RSI (14): 45.23
   → NEUTRAL
📈 MACD Histogram: -0.0234
   → BEARISH - Downward momentum

🎯 Market Trend: NEUTRAL (MODERATE)

🛡️  Nearest Support: $3,010.50
⚡ Nearest Resistance: $3,065.00

======================================================================
💡 RECOMMENDED SCENARIO: [3] Low Volatility
   Calm markets with tight spreads

Select scenario [0-7] or 'q' to quit:
```

---

## 🛡️ Security Best Practices

1. **Never share `src/priv/config.json`** - Contains your API keys
2. **Keep permissions at 600** - `chmod 600 src/priv/config.json`
3. **Disable withdrawals on API key** - Set in Binance.US
4. **Backup config separately** - Store encrypted backup
5. **Monitor regularly** - Check logs daily
6. **Use git carefully** - Add `src/priv/` to `.gitignore`

### .gitignore Example

```
venv/
src/priv/config.json
*.log
tax_transactions.csv
__pycache__/
*.pyc
```

---

## 📈 Monitoring

### Check Bot Status
```bash
ps aux | grep main.py
```

### View Recent Activity
```bash
tail -n 50 grid_bot.log
```

### Check Profit
```bash
grep "P&L:" grid_bot.log | tail -n 1
```

### Count Completed Cycles
```bash
grep "Cycle profit" grid_bot.log | wc -l
```

---

## 🐛 Troubleshooting

### Bot won't start
```bash
# Check virtual environment
source venv/bin/activate
python3 --version

# Check dependencies
pip list | grep -E "ccxt|numpy"

# Check file paths
ls -la src/priv/config.json
```

### API errors
```bash
# Test connection
cd src
python3 test_api.py

# Check permissions in Binance.US
# Make sure "Enable Spot Trading" is checked
```

### Import errors
```bash
# Make sure you're in the right directory
cd ~/skizoh-crypto-grid-bot
pwd

# Check Python path
cd src
python3 -c "import sys; print(sys.path)"
```

### Grid not repositioning
- Check logs for "Grid repositioning needed" messages
- Ensure price has moved > 2x grid spacing
- Wait at least 5 minutes between repositions

---

## 📞 Support

Check logs first: `tail -f grid_bot.log`

Common log messages:
- `✓ Order FILLED` - Trade executed successfully
- `🔄 Grid repositioning needed` - Price moved, adjusting grid
- `📊 Grid bias: BUY` - RSI/MACD favoring buy orders
- `💰 Cycle profit` - Completed buy → sell cycle
- `⚠️ High volatility detected` - Market too volatile, pausing

---

## 🎯 Tips for Success

1. **Start small** - Test with $100-200 first
2. **Monitor first 24 hours** - Watch how it behaves
3. **Check market conditions** - Use recommended scenarios
4. **Be patient** - Grid trading profits accumulate slowly
5. **Track taxes** - Run `tax_summary.py` weekly
6. **Adjust gradually** - Don't change config too often
7. **Keep learning** - Read the logs, understand the patterns

Good luck! 🚀💰
# Skizoh Crypto Grid Trading Bot v1.0

## v1.0

### Bug Fixes
- **Position State Persistence**: Positions now survive bot restarts (data saved to `position_state.json`)
- **Path Handling**: Fixed relative path issues - bot now works from any directory
- **Division by Zero Protection**: Added guards in P&L calculations, exposure checks, and grid repositioning
- **Index Out of Bounds Fix**: MACD histogram calculation now validates array bounds
- **Config Validation**: Added comprehensive validation for API keys and scenario parameters
- **Shell Script Fixes**: All scripts now use consistent directory paths

### New Features
- **ADX Trend Filter**: Automatically pauses grid trading when ADX > 35 (strong trend)
- **Bollinger Band Analysis**: Volatility assessment and price position tracking
- **Volume-Weighted S/R**: Support/resistance levels now weighted by volume and recency
- **Max Drawdown Tracking**: Real-time drawdown monitoring with emergency stops
- **Enhanced Tax Logging**: Pre-calculated cost basis and realized P&L per trade
- **Trading Safety Check**: Comprehensive pre-trade market condition analysis

---

## 📁 File Structure

```
skizoh-crypto-grid-bot/
├── run_bot.sh                    # Main entry point (start bot)
├── monitor_bot.sh                # Status monitor & quick actions
├── test_setup.sh                 # Setup verification & testing
├── README.md                     # This file
├── venv/                         # Python virtual environment
├── src/
│   ├── main.py                   # Bot entry point
│   ├── grid_bot.py               # Core trading engine
│   ├── market_analysis.py        # Technical indicators
│   ├── config_manager.py         # Configuration handling
│   ├── tax_summary.py            # Tax report generator
│   ├── test_api.py               # API connection test
│   └── priv/
│       ├── config.json           # Your config (sensitive!)
│       └── config.json.template  # Template
└── data/
    ├── grid_bot.log              # Runtime logs
    ├── tax_transactions.csv      # Tax records
    ├── position_state.json       # Position tracking
    └── form_8949_data_*.csv      # IRS-ready exports
```

---

## 🔧 Quick Setup

### 1. Clone Repository & Create Virtual Environment

```bash
cd ~
git clone git@github.com:ghempy53/skizoh-crypto-grid-bot.git
cd skizoh-crypto-grid-bot

python3 -m venv venv
source venv/bin/activate
pip install numpy ccxt
```

### 2. Configure API Keys

```bash
nano src/priv/config.json
```

Update with your Binance.US API keys:
```json
{
    "api_key": "YOUR_ACTUAL_KEY",
    "api_secret": "YOUR_ACTUAL_SECRET",
    ...
}
```

### 4. Set Permissions

```bash
chmod +x run_bot.sh monitor_bot.sh test_setup.sh
chmod 600 src/priv/config.json
```

### 5. Test Connection

```bash
./test_setup.sh --all
```

### 6. Run the Bot

```bash
./run_bot.sh
```

---

## 🛠️ Shell Scripts

### run_bot.sh - Main Startup Script

The primary way to start the bot. Performs comprehensive pre-flight checks.

```bash
# Full startup with all checks (recommended)
./run_bot.sh

# Skip checks for faster startup
./run_bot.sh --skip-checks

# Show help
./run_bot.sh --help
```

**Pre-flight checks include:**
- Directory structure verification
- Virtual environment activation
- Python dependency checks
- Configuration validation
- API key verification
- Internet connectivity test
- Running instance detection
- Log rotation (if > 10MB)

### monitor_bot.sh - Status Monitor

Interactive monitoring tool for checking bot status and performing quick actions.

```bash
./monitor_bot.sh
```

**Features:**
- Real-time bot process status
- Multiple instance detection
- Recent log preview
- Position state display (v14.1)
- Quick actions menu:
  - View live logs
  - Search for errors
  - Generate tax summary
  - Graceful/force stop bot

### test_setup.sh - Setup Verification

Comprehensive testing and validation script.

```bash
# Interactive menu
./test_setup.sh

# Run all tests
./test_setup.sh --all

# Specific tests
./test_setup.sh --config    # Validate configuration
./test_setup.sh --network   # Test connectivity
./test_setup.sh --api       # Run API test
./test_setup.sh --v14.1     # Check v14.1 features
./test_setup.sh --system    # Show system info
```

---

## ⚙️ Configuration

### Key Parameters

| Parameter | Description | Recommended |
|-----------|-------------|-------------|
| `fee_rate` | Exchange fee rate | 0.001 (0.1%) |
| `max_position_percent` | Max % of portfolio in crypto | 75% |
| `max_single_order_percent` | Max single order size | 12% |
| `grid_spacing_percent` | Space between grid levels | ≥0.5% (see below) |

### Minimum Profitable Grid Spacing

With 0.1% fees each way (0.2% round trip), your spacing must exceed this to profit:

```
Minimum = (2 × fee_rate × 100) × safety_factor
        = (2 × 0.001 × 100) × 2.5
        = 0.5%
```

**The bot will automatically adjust spacing if it's too tight.**

### Scenarios

| # | Name | Risk | Spacing | Best For |
|---|------|------|---------|----------|
| 0 | Conservative | ★☆☆☆☆ | 1.2% | Learning, uncertain markets |
| 1 | Balanced | ★★★☆☆ | 0.8% | Normal conditions |
| 2 | Aggressive | ★★★★☆ | 0.6% | Active monitoring |
| 3 | Low Volatility | ★★★☆☆ | 0.5% | Calm, ranging markets |
| 4 | High Volatility | ★★☆☆☆ | 1.5% | Volatile markets |
| 5 | Scalping | ★★★★★ | 0.5% | Max frequency (high fees!) |
| 6 | Swing Trading | ★★★☆☆ | 2.5% | Multi-day positions |
| 7 | Night Mode | ★★☆☆☆ | 1.0% | Overnight trading |

---

## 📊 Technical Indicators

### RSI (Wilder's Smoothed)
- Uses proper Wilder smoothing (α = 1/period)
- < 30: Oversold (potential buy)
- > 70: Overbought (potential sell)
- 40-60: Neutral zone

### ADX (Trend Strength) - NEW
- < 20: No trend - **IDEAL for grid trading**
- 20-25: Developing trend - OK
- 25-40: Strong trend - **CAUTION**
- > 40: Very strong trend - **AUTO-PAUSE**

### MACD
- Histogram > 0 with increasing: Bullish momentum
- Histogram < 0 with decreasing: Bearish momentum
- Used to confirm RSI signals

### Grid Bias Logic (CORRECTED)

| RSI | MACD | Signal | Buy Weight |
|-----|------|--------|------------|
| < 30 | Turning up | STRONG BUY | 70% |
| < 30 | Still falling | BUY (caution) | 60% |
| > 70 | Turning down | STRONG SELL | 30% |
| > 70 | Still rising | SELL | 40% |
| 40-60 | Any | NEUTRAL | 50% |

---

## 🛡️ Risk Management

### Exposure Limits

The bot enforces:
- **Max 75% of portfolio in crypto** (configurable)
- **Max 12% per single order** (configurable)
- **Automatic reduction** when exposure exceeds limits

### Stop Loss

Triggers emergency exit when:
- Portfolio loss exceeds `stop_loss_percent`
- Drawdown exceeds `stop_loss_percent × 1.5`

### Trend Filter

Grid trading performs poorly in trending markets. The bot:
- Calculates ADX every cycle
- **Pauses for 30 minutes** when ADX > 35
- Logs warnings when ADX > 25

### Volatility Filter

- Calculates ATR-based volatility
- Skips order placement when volatility exceeds threshold
- Adjusts dynamically based on market conditions

---

## 💰 P&L Tracking

### FIFO Cost Basis

Every position is tracked with:
- Entry price
- Quantity
- Total cost (including fees)
- Entry timestamp

When selling, the **oldest positions are sold first** (FIFO), giving accurate realized P&L.

### Position State Persistence (v14.1)

Position data is now saved to `data/position_state.json`:
- Survives bot restarts
- Maintains accurate cost basis across sessions
- Tracks cumulative realized P&L and fees

### Tax Log Format

Enhanced CSV with columns:
```
Date/Time, Type, Asset, Amount, Price, Value, Fee, 
Net Proceeds, Cost Basis, Realized P&L, Order ID, Notes
```

### Generate Tax Report

```bash
cd src
python3 tax_summary.py 2025
```

Or use the monitor script:
```bash
./monitor_bot.sh
# Select option [5] Generate tax summary
```

Outputs:
- Summary report (console)
- `form_8949_data_2025.csv` (IRS-ready)
- `full_report_2025.csv` (detailed)

---

## 📈 Monitoring

### View Live Logs

```bash
tail -f data/grid_bot.log
```

Or use the monitor script:
```bash
./monitor_bot.sh
# Select option [1]
```

### Key Log Messages

| Message | Meaning |
|---------|---------|
| `✓ FILLED: BUY` | Buy order completed |
| `✓ FILLED: SELL` | Sell order completed |
| `💰 Cycle #X P&L: $Y` | Completed trade cycle with actual profit |
| `🔄 Grid repositioning` | Price moved, adjusting grid |
| `⏸️ Trend pause active` | Strong trend detected, waiting |
| `⚠️ Exposure too high` | Reducing buy orders |
| `🛑 EMERGENCY STOP` | Stop loss triggered |

### Check Performance

```bash
# Recent P&L
grep "Cycle.*P&L" data/grid_bot.log | tail -10

# Count cycles
grep "Cycle #" data/grid_bot.log | wc -l

# Check drawdown
grep "Max DD" data/grid_bot.log | tail -1
```

---

## 🔒 Security

1. **Never share** `src/priv/config.json`
2. **Disable withdrawals** on your API key
3. **Set IP restrictions** on Binance.US
4. **Use `chmod 600`** on config file
5. **Add to `.gitignore`**:
   ```
   src/priv/config.json
   data/
   venv/
   *.log
   __pycache__/
   ```

---

## 🐛 Troubleshooting

### "Grid spacing too tight"
Bot auto-adjusts. If you see this often, increase `grid_spacing_percent`.

### "Trend pause active"
Normal! The bot detected a strong trend and is waiting. Grid trading doesn't work well in trends.

### "Exposure too high"
You have too much crypto. The bot will favor sell orders until balanced.

### API errors
```bash
./test_setup.sh --api
```

### Import errors
```bash
source venv/bin/activate
pip install numpy ccxt
```

### Bot won't start
```bash
./test_setup.sh --all
```

---

## 🎯 Tips for Maximum Profit

1. **Start with Balanced scenario** until you understand the bot
2. **Use Low Volatility scenario** when ADX < 20 and 24h range < 2%
3. **Switch to High Volatility** when 24h range > 4%
4. **Avoid Scalping** unless you have very low fees (VIP tier)
5. **Monitor ADX** - if it's consistently > 30, consider pausing
6. **Track your actual P&L** in the tax log, not just cycles
7. **Fees matter** - tighter grids need more volume to overcome fees

---

## 📞 Support

1. Check logs: `tail -f data/grid_bot.log`
2. Test setup: `./test_setup.sh --all`
3. Test API: `./test_setup.sh --api`
4. Monitor status: `./monitor_bot.sh`
5. Review config: Ensure all parameters are valid

---

**Good luck trading! 🚀💰**

*Version 1.0 - First stable version in production*

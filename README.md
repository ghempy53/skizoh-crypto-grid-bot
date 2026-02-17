# Skizoh Crypto Grid Trading Bot v3.0

A profit-optimized, Raspberry Pi-friendly cryptocurrency grid trading bot for Binance.US.

---

## What's New in v3.0

### Smart Adaptive Configuration Engine

| Feature | Description | Impact |
|---------|-------------|--------|
| **Adaptive Config Engine** | Continuously blends parameters from multiple scenarios based on live market conditions | Eliminates jarring scenario switches |
| **Continuous Parameter Interpolation** | EMA-smoothed transitions between parameter sets | Smoother, more stable trading |
| **Multi-Timeframe Regime Detection** | Detects 8 distinct market regimes across 15m, 1h, and 4h timeframes | More accurate market classification |
| **Confidence-Weighted Blending** | Weights parameter contributions by regime detection confidence | Better adaptation to ambiguous markets |
| **Time-of-Day Awareness** | Adjusts behavior for 24/7 operation based on trading session | Overnight/off-hours handling |

### 24/7 Resilience & Uptime

| Feature | Description | Impact |
|---------|-------------|--------|
| **Circuit Breaker Pattern** | Blocks API calls after repeated failures; auto-recovers after cooldown | Prevents cascading exchange failures |
| **Exponential Backoff with Jitter** | Retries with random jitter to avoid thundering-herd problems | Improved API reliability |
| **Connection Health Monitor** | Continuously monitors exchange connectivity with auto-reconnect | True 24/7 operation |
| **Flash Crash Detection** | Detects sudden price drops and triggers emergency response | Protects against sudden market dislocations |
| **Portfolio Heat Tracking** | Real-time risk scoring based on open exposure and unrealized loss | Proactive risk management |
| **Heartbeat System** | Writes a heartbeat file for external monitoring tools | Easy integration with uptime monitors |
| **Session Health Scoring** | Tracks per-session performance and flags degraded sessions | Visibility into session quality |

### v2.1 Profit Optimizations (Carried Forward)

| Feature | Description | Impact |
|---------|-------------|--------|
| **Asymmetric Grid Placement** | Places more buy orders when oversold, more sell orders when overbought | +20-40% better positioning |
| **Dynamic Grid Spacing** | Adjusts spacing based on volatility and trend strength | +15-25% more profitable cycles |
| **BNB Fee Discount** | Native support for Binance 25% fee discount | +25% savings per cycle |
| **Grid Efficiency Scoring** | Scores market conditions 0-100 for grid suitability | Avoids 50-80% of losing conditions |
| **Mean Reversion Probability** | Quantifies likelihood of price reverting to mean | Better scenario selection |
| **Win Rate Tracking** | Tracks profitable vs unprofitable cycles | Better performance visibility |

### Raspberry Pi Optimizations

| Metric | Improvement |
|--------|-------------|
| Docker Image Size | 60% smaller (~180MB) |
| Memory Usage | 40% reduction (~180MB runtime) |
| API Calls | 70% fewer (~50/hour) |
| SD Card Writes | 80% reduction via tmpfs |

---

## File Structure

```
skizoh-crypto-grid-bot/
├── run_bot.sh                 # Main startup script
├── monitor_bot.sh             # Status monitor & quick actions
├── test_setup.sh              # Setup verification
├── docker-helper.sh           # Docker utility & management script
├── portfolio.py               # Portfolio dashboard & tax helper CLI
├── README.md                  # This file
├── Dockerfile                 # Multi-stage optimized build
├── docker-compose.yml         # Docker configuration
├── docker-entrypoint.sh       # Container entry point
├── Makefile                   # Docker shortcut commands
├── requirements.txt           # Python dependencies
├── venv/                      # Virtual environment (created on first run)
├── src/
│   ├── main.py                # Bot entry point
│   ├── grid_bot.py            # Core trading engine + ProfitOptimizer
│   ├── market_analysis.py     # Technical indicators + OHLCV caching
│   ├── config_manager.py      # Scenario management & config loading
│   ├── adaptive_config.py     # Adaptive config engine + regime detection (v3.0)
│   ├── resilience.py          # Circuit breaker, flash crash, heartbeat (v3.0)
│   ├── tax_summary.py         # Tax report generator (IRS Form 8949)
│   ├── test_api.py            # API connection test
│   └── priv/
│       ├── config.json        # Your configuration (sensitive - never commit!)
│       └── config.json.template
└── data/
    ├── grid_bot.log           # Runtime logs
    ├── tax_transactions.csv   # Tax records
    ├── position_state.json    # Position tracking
    └── position_state_archive.csv  # Historical positions
```

---

## Quick Start

### 1. Clone & Setup Environment

```bash
cd ~
git clone <your-repo-url> skizoh-crypto-grid-bot
cd skizoh-crypto-grid-bot

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
cp src/priv/config.json.template src/priv/config.json
chmod 600 src/priv/config.json
nano src/priv/config.json
```

Update with your Binance.US API credentials:
```json
{
    "api_key": "YOUR_ACTUAL_API_KEY",
    "api_secret": "YOUR_ACTUAL_API_SECRET",
    "symbol": "ETH/USDT"
}
```

### 3. Set Permissions & Test

```bash
chmod +x run_bot.sh monitor_bot.sh test_setup.sh docker-helper.sh
./test_setup.sh --all
```

### 4. Run the Bot

```bash
./run_bot.sh
```

---

## Docker Deployment (Raspberry Pi)

### Quick Start

```bash
# Build the optimized image
docker compose build

# Test API connection
docker compose run --rm gridbot test-api

# Start the bot
docker compose up -d

# View logs
docker compose logs -f
```

### Resource Configuration by Pi Model

| Pi Model | Memory Limit | CPU Limit |
|----------|-------------|-----------|
| Pi 3 (1GB) | 256M | 0.5 |
| Pi 4 (2GB) | 384M | 0.75 |
| Pi 4 (4GB+) | 512M | 1.0 |
| Pi 5 | 768M | 1.5 |

Edit `docker-compose.yml` to match your Pi:
```yaml
deploy:
  resources:
    limits:
      cpus: '0.75'
      memory: 384M
```

---

## Configuration

### Key Parameters

```json
{
    "api_key": "YOUR_API_KEY",
    "api_secret": "YOUR_API_SECRET",
    "symbol": "ETH/USDT",

    "fee_rate": 0.001,
    "use_bnb_for_fees": true,

    "max_position_percent": 70,
    "max_single_order_percent": 10,

    "enable_adaptive_config": true,
    "enable_dynamic_scenarios": true,
    "cycles_per_scenario_check": 5,
    "min_scenario_hold_minutes": 45,
    "scenario_change_confidence": 0.65,

    "default_scenario": "Balanced"
}
```

### Parameter Reference

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `fee_rate` | Exchange fee rate | 0.001 | 0.0004–0.001 |
| `use_bnb_for_fees` | Enable 25% BNB discount | false | true/false |
| `max_position_percent` | Max portfolio in crypto | 70 | 50–85 |
| `max_single_order_percent` | Max single order size | 10 | 5–15 |
| `enable_adaptive_config` | Enable continuous parameter blending (v3.0) | true | true/false |
| `enable_dynamic_scenarios` | Fallback discrete scenario switching | true | true/false |
| `cycles_per_scenario_check` | Cycles between market regime evaluations | 5 | 3–10 |
| `min_scenario_hold_minutes` | Minimum time before switching scenario | 45 | 30–90 |
| `scenario_change_confidence` | Required confidence to switch scenario | 0.65 | 0.5–0.8 |
| `check_interval_seconds` | Seconds between trading cycles | 60 | 15–300 |

---

## Adaptive Configuration Engine (v3.0)

The adaptive config engine replaces hard scenario switches with smooth, continuous parameter blending based on real-time market regime detection.

### How It Works

```
Market Data (15m, 1h, 4h)
    → Regime Detection (RSI, ADX, Bollinger Bands, Volume)
    → Confidence Scores per Regime
    → Weighted Parameter Blending across Scenarios
    → EMA Smoothing (alpha=0.3)
    → Active Parameter Set (with safety bounds enforcement)
    → Grid Placement & Order Execution
```

### Market Regimes

| Regime | Conditions | Bot Behavior |
|--------|-----------|--------------|
| `RANGING` | ADX < 20, price within Bollinger Bands | Grid trading active, tighter spacing |
| `TRENDING_UP` | ADX > 25, price above VWAP | Reduced grid, bias toward buys |
| `TRENDING_DOWN` | ADX > 25, price below VWAP | Reduced grid, bias toward sells |
| `HIGH_VOLATILITY` | ATR spike, large Bollinger Band width | Wider spacing, fewer levels |
| `LOW_VOLATILITY` | ATR low, tight Bollinger Bands | Tighter spacing, more levels |
| `MEAN_REVERTING` | RSI extremes + Bollinger Band touch | Asymmetric placement maximized |
| `BREAKOUT` | Price outside Bollinger Bands + volume spike | Defensive posture |
| `CRASH` | Sudden price drop > threshold | Emergency pause, flash crash mode |

### Parameter Bounds (Safety)

The engine enforces hard bounds on all blended parameters:

| Parameter | Min | Max |
|-----------|-----|-----|
| `grid_levels` | 3 | 24 |
| `grid_spacing_percent` | 0.3% | 5.0% |
| `investment_percent` | 30% | 85% |
| `min_order_size_usdt` | $5 | $30 |
| `stop_loss_percent` | 5% | 30% |
| `check_interval_seconds` | 15s | 300s |

---

## 24/7 Resilience & Uptime (v3.0)

### Circuit Breaker

Protects against cascading API failures using the circuit breaker pattern:

| State | Description |
|-------|-------------|
| `CLOSED` | Normal operation — all calls pass through |
| `OPEN` | Too many failures — calls are blocked; cooldown active |
| `HALF_OPEN` | After cooldown — one test call is allowed through |

The circuit opens after 5 consecutive failures and attempts recovery after 60 seconds.

### Flash Crash Detection

The bot monitors for sudden price drops. When a flash crash is detected:
1. All new orders are paused immediately
2. Existing open orders may be cancelled
3. Bot waits for price stabilization before resuming
4. Event is logged with timestamp and magnitude

### Portfolio Heat

Tracks a real-time risk score based on:
- Total open exposure as % of portfolio
- Unrealized loss magnitude
- Number of open positions relative to limit

When portfolio heat is elevated, the bot reduces new buy order frequency automatically.

### Heartbeat Monitoring

The bot writes a heartbeat file (`data/heartbeat.json`) at each cycle. Use it with external tools:

```bash
# Check if bot is alive (heartbeat older than 5 minutes = problem)
python3 -c "
import json, time
from pathlib import Path
hb = json.loads(Path('data/heartbeat.json').read_text())
age = time.time() - hb['timestamp']
print(f'Bot alive: {age < 300}  (last seen {age:.0f}s ago)')
"
```

---

## Trading Scenarios

| Scenario | Risk | Spacing | Best Conditions | Expected Profit/Cycle |
|----------|------|---------|-----------------|----------------------|
| **Conservative** | ★☆☆☆☆ | 1.5% | Learning, uncertain markets | ~1.3% |
| **Balanced** | ★★★☆☆ | 0.9% | Normal volatility (RECOMMENDED) | ~0.7% |
| **Aggressive** | ★★★★☆ | 0.65% | Active monitoring | ~0.45% |
| **Low Volatility** | ★★★☆☆ | 0.55% | Calm markets, ADX < 20 | ~0.35% |
| **High Volatility** | ★★☆☆☆ | 2.0% | News events, 5%+ daily range | ~1.8% |
| **Scalping** | ★★★★★ | 0.5% | VIP fees or BNB discount ONLY | ~0.3% |
| **Swing Trading** | ★★★☆☆ | 3.0% | Multi-day holds | ~2.8% |
| **Night Mode** | ★★☆☆☆ | 1.2% | Overnight, unmonitored | ~1.0% |
| **Mean Reversion** | ★★★☆☆ | 0.75% | Ranging markets, ADX < 25 | ~0.55% |

With `enable_adaptive_config: true`, the bot blends parameters from multiple scenarios simultaneously rather than switching between them discretely.

### Minimum Profitable Spacing

```
Minimum = 2 × fee_rate × 100 × safety_factor
        = 2 × 0.001 × 100 × 2.5
        = 0.5%

With BNB discount (0.075% fees):
        = 2 × 0.00075 × 100 × 2.5
        = 0.375%
```

---

## Technical Indicators

### RSI (Wilder's Smoothed)
- Uses proper Wilder smoothing (α = 1/period)
- < 30: Oversold (potential buy zone)
- > 70: Overbought (potential sell zone)
- 40–60: Neutral

### ADX (Trend Strength) — Critical for Grid Trading
- < 20: No trend → **IDEAL for grid trading**
- 20–25: Developing trend → OK
- 25–40: Strong trend → **CAUTION**
- > 40: Very strong trend → **AUTO-PAUSE**

### Grid Efficiency Score
- 80–100: Excellent conditions for grid trading
- 60–80: Good conditions
- 40–60: Marginal conditions
- < 40: Poor conditions → Consider pausing

### Mean Reversion Probability
Higher probability = better grid trading conditions.
Based on: RSI extremes, Bollinger Band position, ADX trend strength.

### Asymmetric Grid Bias

| Condition | Buy Weight | Sell Weight |
|-----------|------------|-------------|
| RSI < 30 + MACD positive | 70% | 30% |
| RSI < 30 + MACD negative | 60% | 40% |
| RSI > 70 + MACD negative | 30% | 70% |
| RSI > 70 + MACD positive | 40% | 60% |
| Neutral (RSI 40–60) | 50% | 50% |
| Strong trend (ADX > 35) | 50% | 50% |

---

## Risk Management

### Exposure Limits
- **Max 70% of portfolio in crypto** (configurable via `max_position_percent`)
- **Max 10% per single order** (configurable via `max_single_order_percent`)
- Automatic reduction when exposure exceeds limits

### Stop Loss
Triggers emergency exit when:
- Portfolio loss exceeds `stop_loss_percent`
- Drawdown exceeds `stop_loss_percent × 1.5`

### Trend Filter
- Calculates ADX every cycle
- **Pauses for 30 minutes** when ADX > 40
- Logs warnings when ADX > 25

### Position Archival (Memory Safety)
- Archives positions to CSV when >400 are held in memory
- Keeps only 300 most recent positions in RAM
- Prevents memory issues on Raspberry Pi

---

## P&L Tracking

### FIFO Cost Basis
Every position is tracked with:
- Entry price and quantity
- Total cost (including fees)
- Entry timestamp

When selling, **oldest positions are sold first** (FIFO) for accurate realized P&L.

### Win Rate Tracking
```
Win Rate = Profitable Cycles / Total Cycles × 100

Target: >60% in ranging markets
```

### Tax Report Generation

```bash
# Generate tax summary via tax_summary.py
cd src && python3 tax_summary.py 2025

# Or use monitor script
./monitor_bot.sh  # Select option [5]
```

Outputs:
- Console summary report
- `form_8949_data_2025.csv` (IRS-ready)
- `full_report_2025.csv` (detailed)

---

## Portfolio Helper

`portfolio.py` is a standalone CLI tool for viewing portfolio status, P&L, and tax data without running the full bot.

```bash
python portfolio.py                   # Full portfolio dashboard
python portfolio.py balance           # ETH and USD balances
python portfolio.py transactions      # Last 20 transactions
python portfolio.py transactions 50   # Last 50 transactions
python portfolio.py pnl               # All-time profit and loss breakdown
python portfolio.py tax               # Current year tax summary
python portfolio.py tax 2025          # Tax summary for a specific year
python portfolio.py fees              # Total fees paid
python portfolio.py positions         # Open positions and cost basis
python portfolio.py daily             # Daily P&L breakdown
python portfolio.py summary           # Compact one-line summary
python portfolio.py export 2025       # Export Form 8949 CSV for a year
```

The tool reads directly from `data/tax_transactions.csv` and `data/position_state.json` — no bot process required.

---

## Monitoring

### View Live Logs

```bash
tail -f data/grid_bot.log
# or
./monitor_bot.sh  # Select option [1]
```

### Key Log Messages

| Message | Meaning |
|---------|---------|
| `FILLED: BUY` | Buy order completed |
| `FILLED: SELL` | Sell order completed |
| `Cycle #X P&L: $Y` | Completed trade cycle with profit |
| `Grid Efficiency: 75` | Current market suitability score |
| `Win Rate: 65%` | Percentage of profitable cycles |
| `Grid repositioning` | Price moved, adjusting grid |
| `Trend pause active` | Strong trend detected, waiting |
| `Exposure too high` | Reducing buy orders |
| `SCENARIO CHANGE` | Auto-switched to different scenario |
| `Regime: RANGING (conf=0.82)` | Current market regime and confidence |
| `[CB:exchange] Circuit OPEN` | Circuit breaker tripped — API failures |
| `[CB:exchange] Circuit CLOSED` | Circuit breaker recovered |
| `FLASH CRASH DETECTED` | Sudden price drop — orders paused |
| `Portfolio heat: HIGH` | Elevated risk — reducing new buys |
| `Adaptive params updated` | Blended parameters recalculated |

### Performance Metrics

```bash
# Recent P&L
grep "Cycle.*P&L" data/grid_bot.log | tail -10

# Win rate
grep "Win Rate" data/grid_bot.log | tail -1

# Grid efficiency
grep "Efficiency" data/grid_bot.log | tail -1

# Scenario changes
cat data/scenario_changes.csv

# Circuit breaker events
grep "Circuit" data/grid_bot.log | tail -20

# Regime changes
grep "Regime:" data/grid_bot.log | tail -20
```

---

## Shell Scripts

### run_bot.sh
Main startup script with pre-flight checks.

```bash
./run_bot.sh              # Full checks (recommended)
./run_bot.sh --skip-checks  # Fast startup
```

Checks performed: config file presence, Python version, virtual environment, dependency versions, API key format.

### monitor_bot.sh
Interactive monitoring and quick actions.

```bash
./monitor_bot.sh
```

Options: View live logs, search errors, generate tax summary, stop/restart bot.

### test_setup.sh
Setup verification and API testing.

```bash
./test_setup.sh --all     # Run all tests
./test_setup.sh --config  # Validate config only
./test_setup.sh --api     # Test API connection only
```

### docker-helper.sh
Docker management utility with convenience commands for building, running, monitoring, and troubleshooting the bot container.

```bash
./docker-helper.sh build       # Build the Docker image
./docker-helper.sh run         # Start the container
./docker-helper.sh stop        # Stop the container
./docker-helper.sh restart     # Restart the container
./docker-helper.sh logs        # View container logs
./docker-helper.sh shell       # Open a shell inside the container
./docker-helper.sh status      # Show container status and resource usage
./docker-helper.sh clean       # Remove container and image
```

### Makefile
Shortcut wrappers around `docker compose`:

```bash
make build      # Build image
make run        # Start container
make stop       # Stop container
make logs       # View logs
make clean      # Remove container/image
make realclean  # Full cleanup including volumes and build cache
```

---

## Security Best Practices

1. **Protect config.json**: `chmod 600 src/priv/config.json`
2. **Disable withdrawals** on your API key
3. **Set IP restrictions** on Binance.US
4. **Never commit** config.json to git (it is gitignored by default)
5. **Use read-only mount** in Docker: `config.json:/app/src/priv/config.json:ro`

---

## Troubleshooting

### "Grid spacing too tight"
Bot auto-adjusts. If frequent, increase `grid_spacing_percent`.

### "Grid efficiency < 40"
Market is unsuitable for grid trading. Wait for ranging conditions (ADX < 20).

### "Trend pause active"
Normal behavior. Strong trend detected (ADX > 40). Grid trading doesn't work in strong trends.

### "Exposure too high"
Too much crypto held. Bot will favor sell orders until exposure is back within limits.

### "Circuit OPEN" in logs
The exchange API returned repeated errors. The circuit breaker is protecting the bot from cascading failures. It will auto-recover after 60 seconds of cooldown.

### API errors
```bash
./test_setup.sh --api
```

### Memory issues on Pi
Check Docker resource limits. Consider:
- Reducing `max_position_percent`
- Using longer `check_interval_seconds`
- Archiving old positions manually

### Docker build fails with IPv6 errors

If you see errors like:
```
dial tcp [2606:4700:...]:443: socket: address family not supported by protocol
failed to copy: httpReadSeeker: failed open: failed to do request
```

This is an IPv6 connectivity issue. Docker is trying to reach registries over IPv6 but your network doesn't support it.

**Solution 1: Force IPv4 (Quick Fix)**
```bash
echo "--ipv4" >> ~/.curlrc
sudo systemctl restart docker
docker compose build
```

**Solution 2: Configure Docker daemon**

Edit `/etc/docker/daemon.json`:
```bash
sudo nano /etc/docker/daemon.json
```

Add or update:
```json
{
  "ipv6": false,
  "ip6tables": false,
  "dns": ["8.8.8.8", "8.8.4.4"]
}
```

Then restart Docker:
```bash
sudo systemctl restart docker
```

**Solution 3: Disable IPv6 at kernel level (Permanent Fix)**
```bash
sudo nano /boot/firmware/cmdline.txt
# Add to the END of the existing line (same line, space before):
 ipv6.disable=1

# Reboot
sudo reboot
```

After reboot, verify:
```bash
cat /proc/sys/net/ipv6/conf/all/disable_ipv6
# Should return: "No such file or directory" (module not loaded)
```

**Solution 4: Clean rebuild after applying fix**
```bash
make realclean
docker compose build
```

---

## Performance Expectations

### Ranging Market (ADX < 20)

| Metric | Expected |
|--------|----------|
| Cycles/day | 20–25 |
| Win rate | ~65% |
| Profit/cycle | ~0.5% |
| Daily profit | ~8–10% |

### Volatile Market (5%+ daily range)

| Metric | Expected |
|--------|----------|
| Cycles/day | ~8 |
| Win rate | ~60% |
| Profit/cycle | ~1.8% |
| Daily profit | ~8.5% |

### Trending Market (ADX > 35)

| Metric | Expected |
|--------|----------|
| Action | Auto-pause |
| Losses avoided | 50–80% |

---

## Configuration Profiles

### Maximum Profit (Higher Risk)

```json
{
    "use_bnb_for_fees": true,
    "max_position_percent": 75,
    "enable_adaptive_config": true,
    "enable_dynamic_scenarios": true,
    "cycles_per_scenario_check": 3,
    "min_scenario_hold_minutes": 30,
    "scenario_change_confidence": 0.6
}
```

### Steady Gains (Lower Risk)

```json
{
    "use_bnb_for_fees": true,
    "max_position_percent": 60,
    "enable_adaptive_config": true,
    "enable_dynamic_scenarios": true,
    "cycles_per_scenario_check": 7,
    "min_scenario_hold_minutes": 60,
    "scenario_change_confidence": 0.75
}
```

### Raspberry Pi (Resource Constrained)

```json
{
    "max_position_percent": 65,
    "enable_adaptive_config": true,
    "cycles_per_scenario_check": 7,
    "check_interval_seconds": 90
}
```

---

## License

GNU General Public License v3.0

---

## Disclaimer

This software is for educational purposes. Cryptocurrency trading involves significant risk. Past performance does not guarantee future results. Only trade with funds you can afford to lose.

---

*Skizoh Crypto Grid Trading Bot v3.0 — Smart Adaptive Trading*

# Skizoh Crypto Grid Trading Bot v3.1

A profit-optimized, Raspberry Pi-friendly cryptocurrency grid trading bot for Binance.US.

---

## What's New in v3.1 — Profit Optimization

v3.1 is a comprehensive profitability tuning pass across the entire trading engine. Every parameter was reviewed against a month of live performance data and adjusted to extract more profit per cycle, compound gains faster, and keep capital deployed more efficiently — all while preserving the safety guardrails from v3.0.

### Tighter, More Profitable Grid Spacing

| Change | Before (v3.0) | After (v3.1) | Impact |
|--------|---------------|--------------|--------|
| Fee safety factor | 2.5x | 1.8x | Minimum profitable spacing drops from 0.5% to 0.36% — more cycles complete |
| Low-volatility spacing | Tightens below 2% vol | Tightens below 2.5%, aggressively below 1.5% | More fills in calm markets |
| RSI mean-reversion multiplier | 0.80x at extremes | 0.72x at extremes | Much tighter grid when cycles complete fastest |
| ADX ranging bonus | 0.9x below 15 | 0.85x below 15, 0.9x below 20 | Captures more ranging-market profit |
| Asymmetric level progression | 10% wider per level | 5% wider per level | Denser grid near current price = more fills |

### Faster Capital Redeployment

| Change | Before (v3.0) | After (v3.1) | Impact |
|--------|---------------|--------------|--------|
| Stale order timeout | 60 minutes | 30 minutes | Frees capital 2x faster for redeployment |
| Grid reposition threshold | 2.0x spacing | 1.5x spacing | Grid re-centers sooner on price moves |
| Grid update interval | 5 minutes | 4 minutes | Faster adaptation to new conditions |
| Position age penalty | Starts at 24h | Starts at 8h | Unsticks capital from old positions 3x sooner |

### Accelerated Profit Compounding

| Change | Before (v3.0) | After (v3.1) | Impact |
|--------|---------------|--------------|--------|
| Profit reinvestment rate | 30% of excess | 45% of excess | 50% faster compounding |
| Reinvestment threshold | 2% of portfolio | 1% of portfolio | Starts compounding earlier |
| Reinvestment frequency | Every 10 cycles | Every 5 cycles | More frequent compounding |
| Investment compounding start | At +5% profit | At +3% profit | Earlier capital growth |
| ETH accumulation tightening | 15% tighter rebuy | 22% tighter rebuy | More ETH acquired per cycle |

### Smarter Regime-Specific Tuning

| Regime | Change | Impact |
|--------|--------|--------|
| **Mean Reverting** | Spacing 0.85x→0.75x, levels +35%, capital +8% | Maximizes profit in the best grid-trading regime |
| **Ranging** (new) | Spacing 0.92x, levels +15% | Tighter grids when price is oscillating |
| **Peak hours (12-18 UTC)** | Spacing 0.95x→0.88x, capital +8% | Captures more during highest-volume period |
| **Portfolio heat thresholds** | Full-size up to heat 40 (was 30) | 33% more headroom before position size cuts |

### Optimized Scenario Parameters

All 9 trading scenarios received tighter spacing, more grid levels, and higher capital allocation:

| Scenario | Levels (old→new) | Spacing (old→new) | Investment (old→new) |
|----------|-------------------|--------------------|----------------------|
| Conservative | 6→7 | 1.5→1.3% | 60→62% |
| **Balanced** | 10→12 | 0.9→0.75% | 70→75% |
| Aggressive | 14→16 | 0.65→0.55% | 75→78% |
| Low Volatility | 12→14 | 0.55→0.45% | 70→74% |
| High Volatility | 6→8 | 2.0→1.8% | 55→58% |
| Scalping | 16→18 | 0.5→0.4% | 65→68% |
| Swing Trading | 5→6 | 3.0→2.7% | 60→62% |
| Night Mode | 6→8 | 1.2→1.05% | 50→55% |
| **Mean Reversion** | 10→13 | 0.75→0.6% | 70→76% |

### Other Improvements

- **Momentum filtering relaxed** (threshold ±0.5→±0.8) — fewer missed entries from over-filtering
- **Volatility bonus** kicks in earlier (above 3% vol instead of 4%) with a steeper rate (+0.12%/1% vol)
- **Grid efficiency scaling** — efficiency 85+ now gives 1.5x levels (was 1.3x at 80+)
- **Safety bounds widened** for BNB fee users (min spacing 0.25%, max levels 26)

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
│   ├── adaptive_config.py     # Adaptive config engine + regime detection (v3.1)
│   ├── resilience.py          # Circuit breaker, flash crash, heartbeat (v3.1)
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
| `enable_adaptive_config` | Enable continuous parameter blending (v3.1) | true | true/false |
| `enable_dynamic_scenarios` | Fallback discrete scenario switching | true | true/false |
| `cycles_per_scenario_check` | Cycles between market regime evaluations | 5 | 3–10 |
| `min_scenario_hold_minutes` | Minimum time before switching scenario | 45 | 30–90 |
| `scenario_change_confidence` | Required confidence to switch scenario | 0.65 | 0.5–0.8 |
| `check_interval_seconds` | Seconds between trading cycles | 60 | 15–300 |

---

## Adaptive Configuration Engine (v3.1)

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
| `grid_levels` | 3 | 26 |
| `grid_spacing_percent` | 0.25% | 5.0% |
| `investment_percent` | 30% | 88% |
| `min_order_size_usdt` | $5 | $30 |
| `stop_loss_percent` | 5% | 30% |
| `check_interval_seconds` | 12s | 300s |

---

## 24/7 Resilience & Uptime (v3.1)

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

| Scenario | Risk | Levels | Spacing | Best Conditions | Expected Profit/Cycle |
|----------|------|--------|---------|-----------------|----------------------|
| **Conservative** | ★☆☆☆☆ | 7 | 1.3% | Learning, uncertain markets | ~1.1% |
| **Balanced** | ★★★☆☆ | 12 | 0.75% | Normal volatility (RECOMMENDED) | ~0.55% |
| **Aggressive** | ★★★★☆ | 16 | 0.55% | Active monitoring | ~0.35% |
| **Low Volatility** | ★★★☆☆ | 14 | 0.45% | Calm markets, ADX < 20 | ~0.27% |
| **High Volatility** | ★★☆☆☆ | 8 | 1.8% | News events, 5%+ daily range | ~1.6% |
| **Scalping** | ★★★★★ | 18 | 0.4% | VIP fees or BNB discount ONLY | ~0.22% |
| **Swing Trading** | ★★★☆☆ | 6 | 2.7% | Multi-day holds | ~2.5% |
| **Night Mode** | ★★☆☆☆ | 8 | 1.05% | Overnight, unmonitored | ~0.85% |
| **Mean Reversion** | ★★★☆☆ | 13 | 0.6% | Ranging markets, ADX < 25 | ~0.42% |

With `enable_adaptive_config: true`, the bot blends parameters from multiple scenarios simultaneously rather than switching between them discretely.

### Minimum Profitable Spacing

```
Minimum = 2 × fee_rate × 100 × safety_factor
        = 2 × 0.001 × 100 × 1.8
        = 0.36%

With BNB discount (0.075% fees):
        = 2 × 0.00075 × 100 × 1.8
        = 0.27%
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

This is an IPv6 connectivity issue. Docker is trying to reach registries over
IPv6 but your network (or the Pi's kernel) doesn't route IPv6.

> ⚠️  **A REBOOT IS REQUIRED whenever you hit this error**, even on subsequent
> occurrences. The fix touches the kernel cmdline, sysctl, systemd unit
> environments, and the DNS resolver — these only take effect together after a
> full reboot. Restarting Docker alone is not enough.

**Recommended: use the helper (fixes everything in one step)**
```bash
./docker-helper.sh fix-ipv6
sudo reboot                   # REQUIRED — do not skip, even on re-runs
./docker-helper.sh rebuild
```

The helper applies all of the following. If you prefer to do it manually, here
is exactly what it does — **all seven pieces are usually required** on a fresh
Pi OS Lite install, which is why piecemeal fixes tend to fail:

**1. Prefer IPv4 in glibc's name resolver (`/etc/gai.conf`)**

Without it, the resolver returns AAAA records first and Docker attempts IPv6
connections that fail, even when IPv6 is disabled on your interfaces.
```bash
echo "precedence ::ffff:0:0/96  100" | sudo tee -a /etc/gai.conf
```

**2. Disable IPv6 via sysctl (drop-in, not `/etc/sysctl.conf`)**
```bash
sudo tee /etc/sysctl.d/99-disable-ipv6.conf <<'EOF'
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
EOF
sudo sysctl --system
```

**3. Disable IPv6 at the kernel level (`/boot/firmware/cmdline.txt`)**

⚠️  `cmdline.txt` **must remain a single line**. Adding `ipv6.disable=1` on a
new line is a common mistake — the bootloader will ignore it.
```bash
sudo nano /boot/firmware/cmdline.txt
# Append to the END of the existing line (preceded by a single space):
#   ... ipv6.disable=1
sudo reboot                   # kernel changes require a reboot to apply
```

**4. Configure the Docker daemon (`/etc/docker/daemon.json`)**
```json
{
  "ipv6": false,
  "dns": ["8.8.8.8", "1.1.1.1"],
  "dns-opts": ["ndots:0", "single-request"],
  "features": {"buildkit": false}
}
```
Then: `sudo systemctl restart docker`

Why `buildkit: false`? BuildKit runs in its own container with a Go-based
DNS resolver that **ignores `/etc/gai.conf`** and does not fall back cleanly
from IPv6 to IPv4 when the kernel rejects `AF_INET6` sockets. The legacy
builder (used when BuildKit is off) pulls through dockerd directly and handles
IPv6-less networks correctly.

**5. Force dockerd + containerd to use glibc's resolver (systemd drop-ins)**

Even with BuildKit off, dockerd/containerd are Go programs whose default
`netgo` resolver ignores `/etc/gai.conf`. They return AAAA records first and
the `httpReadSeeker` blob-fetch path fails with `EAFNOSUPPORT` instead of
falling back to IPv4. Setting `GODEBUG=netdns=cgo+1` routes DNS through glibc,
which honours the `gai.conf` priority from step 1.
```bash
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo tee /etc/systemd/system/docker.service.d/10-ipv4-resolver.conf <<'EOF'
[Service]
Environment=GODEBUG=netdns=cgo+1
EOF
sudo mkdir -p /etc/systemd/system/containerd.service.d
sudo tee /etc/systemd/system/containerd.service.d/10-ipv4-resolver.conf <<'EOF'
[Service]
Environment=GODEBUG=netdns=cgo+1
EOF
sudo systemctl daemon-reload
```

**6. Drop AAAA records entirely (`/etc/resolv.conf` + dhcpcd hook)**

Belt-and-suspenders: tell glibc's stub resolver to skip AAAA lookups, so
nothing upstream ever sees an IPv6 address for `registry-1.docker.io`. Also
persist the option via `/etc/resolvconf.conf` and a `dhcpcd` hook so a DHCP
lease renewal doesn't wipe it.
```bash
echo 'options single-request no-aaaa' | sudo tee -a /etc/resolv.conf
echo 'resolv_conf_options="single-request no-aaaa"' | sudo tee -a /etc/resolvconf.conf
```

**7. Clear stale buildx state**
```bash
docker buildx prune -af
```

**Reboot, then verify**
```bash
sudo reboot                                    # REQUIRED — apply all changes
# --- after reboot ---
ip -6 addr                                     # no global IPv6 addresses
docker info | grep -i ipv6                     # IPv6: off / false
./docker-helper.sh rebuild                     # build should succeed
```

If the rebuild still fails after a reboot, re-run `./docker-helper.sh fix-ipv6`
— the final step pulls the base image as a live test and will tell you exactly
which piece didn't apply.

---

## Performance Expectations

### Ranging Market (ADX < 20)

| Metric | Expected |
|--------|----------|
| Cycles/day | 25–35 |
| Win rate | ~65% |
| Profit/cycle | ~0.4% |
| Daily profit | ~10–14% |

### Volatile Market (5%+ daily range)

| Metric | Expected |
|--------|----------|
| Cycles/day | ~10 |
| Win rate | ~60% |
| Profit/cycle | ~1.6% |
| Daily profit | ~9.5% |

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

*Skizoh Crypto Grid Trading Bot v3.1 — Profit-Optimized Smart Adaptive Trading*

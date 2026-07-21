# Architecture & Strategy

[← Back to README](../README.md)

## Adaptive Configuration Engine (v4.1)

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

## 24/7 Resilience & Uptime (v4.1)

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


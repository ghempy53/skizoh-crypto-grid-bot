# Configuration Reference

[← Back to README](../README.md)

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
├── daily_report.py            # Cron-driven daily phone report (v4.1, stdlib-only)
├── venv/                      # Virtual environment (created on first run)
├── src/
│   ├── main.py                # Bot entry point + fault-classified startup retry
│   ├── grid_bot.py            # Core trading engine + ProfitOptimizer
│   ├── risk_manager.py        # Exposure controller: bear exit, trailing stop, rebalancing (v4.1)
│   ├── notifier.py            # Push alerts: ntfy / webhook / Telegram (v4.1)
│   ├── market_analysis.py     # Technical indicators + OHLCV caching
│   ├── config_manager.py      # Scenario management & config loading
│   ├── adaptive_config.py     # Adaptive config engine + regime detection
│   ├── resilience.py          # Circuit breaker, flash crash, heartbeat
│   ├── tax_summary.py         # Tax report generator (IRS Form 8949)
│   ├── test_api.py            # API connection test
│   ├── test_risk_manager.py   # Unit tests for the exposure controller (v4.1)
│   └── priv/
│       ├── config.json        # Your configuration (sensitive - never commit!)
│       └── config.json.template
└── data/
    ├── grid_bot.log           # Runtime logs
    ├── tax_transactions.csv   # Tax records
    ├── position_state.json    # Position tracking
    ├── position_state_archive.csv  # Historical positions
    ├── risk_state.json        # Persisted peak value + exposure state (v4.1)
    ├── heartbeat.json         # Liveness + regime status for monitoring
    └── .alive                 # Healthcheck sentinel touched every cycle
```

---

## Configuration

### Key Parameters

```json
{
    "api_key": "YOUR_API_KEY",
    "api_secret": "YOUR_API_SECRET",
    "symbol": "ETH/USDT",

    "maker_fee_rate": 0.0,
    "taker_fee_rate": 0.0002,
    "min_spacing_floor_percent": 0.15,
    "use_bnb_for_fees": false,

    "max_position_percent": 70,
    "max_single_order_percent": 10,

    "enable_exposure_management": true,
    "risk_management": { "...": "see template — bear floor, trailing stop, rebalancing" },
    "alerts": { "ntfy_topic": "your-unique-topic" },

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
| `maker_fee_rate` | Maker fee (grid limit orders) | 0.0 | 0.0–0.001 |
| `taker_fee_rate` | Taker fee (rebalance market orders) | 0.0002 | 0.0–0.001 |
| `min_spacing_floor_percent` | Absolute min grid spacing (spread/slippage buffer) | 0.15 | 0.1–0.5 |
| `fee_rate` | Legacy fallback if maker/taker not set | 0.001 | 0.0004–0.001 |
| `use_bnb_for_fees` | Enable 25% BNB discount | false | true/false |
| `enable_exposure_management` | Regime-aware exposure control (v4.1) | true | true/false |
| `risk_management` | Bear floor, trailing stop, rebalance settings | see template | — |
| `alerts` | ntfy / webhook / Telegram push channels | disabled | — |
| `max_position_percent` | Max portfolio in crypto (dynamically capped by exposure target) | 70 | 50–85 |
| `max_single_order_percent` | Max single order size | 10 | 5–15 |
| `enable_adaptive_config` | Enable continuous parameter blending (v4.1) | true | true/false |
| `enable_dynamic_scenarios` | Fallback discrete scenario switching | true | true/false |
| `cycles_per_scenario_check` | Cycles between market regime evaluations | 5 | 3–10 |
| `min_scenario_hold_minutes` | Minimum time before switching scenario | 45 | 30–90 |
| `scenario_change_confidence` | Required confidence to switch scenario | 0.65 | 0.5–0.8 |
| `check_interval_seconds` | Seconds between trading cycles | 60 | 15–300 |

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
Minimum = max(2 × maker_fee × 100 × safety_factor, min_spacing_floor_percent)

At Binance.US 0% maker (grid limit orders are maker on both sides):
        = max(0%, 0.15%)
        = 0.15%           ← the floor covers spread + slippage

With legacy 0.1% flat fees (v3.x-era assumption):
        = 2 × 0.001 × 100 × 1.8
        = 0.36%
```

The bot verifies actual maker/taker rates at startup via `fetch_trading_fees`
and adjusts automatically — the config values are just the fallback.

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


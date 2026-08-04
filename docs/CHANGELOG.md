# Release History

[← Back to README](../README.md)

## What's New in v4.2 — Let the Grid Fill, Stop the Whipsaw

Post-mortem of 14 days live (Jul 20–Aug 3, ETH ranging $1,830–$2,000):
account -3.0%. The grid completed **4 cycles (+$1.66)** out of 2,002 orders
placed (~1,760 canceled as "stale"), while the regime rebalancer executed
61 taker trades that net-sold @ avg $1,887 and re-bought @ avg $1,904
(**-$7.3 realized**). The adaptive stack was destroying the grid's edge.

| Change | Observed problem | Fix |
|--------|------------------|-----|
| **Distance-aware stale cancels** (was: 30-min age cutoff) | 88% of orders canceled before they could fill — ~1% fill rate. A resting maker order costs 0% | Cancel only orders outside the `max_grid_distance` band; 8h age hard cap as safety |
| **Adaptive spacing cap** (`max_spacing_cap_percent`, default 1.25%) | Regime blend pushed spacing to 1.5–2.3% (Swing 2.7% weight) in a 1–2% daily range — orders sat unfillable | Spacing clamped; with 0% maker fees, tight grids cycle nearly free |
| **Reposition threshold 1.5x → 3x spacing; grid rebuild interval 4 → 30 min** | Grid re-centered on every ~1.1% move, chasing price instead of letting it cross static levels | Grid stays put; price oscillation completes cycles |
| **Flattened regime targets** (15–65% → 30–60%; band 7% → 12%; stage 15pt/20min → 10pt/60min; confidence 0.55 → 0.65; confirms 3/4 → 6/8; hold 6h) | Target swings trend-followed noisy regime flips with taker market orders — systematic sell-low/buy-high | Exposure held near-constant (constant-mix harvests ranges positively); big de-risking left to the drawdown trailing stop |
| **Trailing-stop cap decoupled from bear floor** (`trailing_stop_cap_percent`: 15) | Raising the regime floor to 25% would have weakened real-drawdown protection | Regime noise floors at 25%; a -10% drawdown still caps at 15% |

## What's New in v4.1 — Cycle Economics & Live-Data Tuning

v4.1 is a data-driven tuning release: every change traces to a specific
pattern observed in production logs and the trade ledger during the first
weeks of live operation on the previous release.

| Change | Observed problem | Fix |
|--------|------------------|-----|
| **Grid distance cap** (`max_grid_distance_percent`, default 4%) | Sells laddered up to +10% never filled within the stale window; they churned (cancel + re-place) every 30 min forever while locking ~half the ETH inventory | Levels beyond the cap aren't placed; the same capital concentrates into fewer, nearer, fillable orders. First capped ladder filled next day for the ledger's biggest wins |
| **Reinvest/rebalancer conflict removed** | Legacy `reinvest_profits_to_eth` market-bought ETH blind to the exposure target; the rebalancer sold it back — a loop paying 2x taker + spread per round | Reinvestment is disabled whenever exposure management is active; the constant-mix rebalancer alone converts USDT profit into ETH |
| **Batched order polling** | One `fetch_order` call per tracked order per cycle (~650 API calls/hour) | One `fetch_open_orders` call identifies still-open orders; only closed ones get individual fetches |
| **Quiet-climb peak persistence** | The trailing-stop peak only persisted on de-risk/regime events; a crash during a calm climb restarted the stop from a lower anchor | Peak saves whenever it grows >=0.5% (throttled for SD wear); regression-tested |
| **Rotating logs** (10MB x 3) | `grid_bot.log` grew unbounded for weeks, hit null-byte corruption from an ungraceful write, and made greps hang | `RotatingFileHandler` bounds size and retires corruption with old segments |
| **Paused-cycle status line** | Multi-hour trend pauses logged only countdowns — no portfolio visibility | Each paused cycle logs value, price, exposure target, and peak |
| **Regime hold 60 -> 240 min** (template default) | Ledger showed the 45%<->65% exposure target flapping every 1-2 days, trading ~$120 of stage-steps per flip on market indecision | 4-hour minimum hold damps target thrash; bear-entry confirmation counts are unaffected |

---

## Previous Release — Down-Market Survival & Reliability

That release was the largest to date, built from a real post-mortem: in a
sustained downtrend the old bot paused trading while fully invested (losses
ran unmanaged), and an invalid API key later caused a silent two-month
crash loop that the healthcheck never caught. It restructured both the
strategy and the reliability layer so neither failure is possible again.

### Regime-Aware Exposure Management (`src/risk_manager.py`)

| Feature | Description |
|---------|-------------|
| **Staged bear exit with ETH floor** | On a confirmed bear regime (3 consecutive detections), ETH exposure is staged down (15 points per stage) to a configurable floor (default 15%) — never fully out, so V-bottoms aren't missed |
| **Re-entry hysteresis** | Re-entering requires more confirmations (4) plus a minimum hold time, limiting whipsaw cost |
| **Trailing stop from persisted peak** | Peak portfolio value survives restarts (`data/risk_state.json`). Drawdown caps exposure in stages: -5% → 50%, -8% → 25%, -10% → floor, -20% → full exit + halt |
| **Constant-mix rebalancing** | When actual exposure drifts >7 points from target, a rebalance trade harvests the volatility and restores the USDT reserve |
| **Runs before the trend filter** | De-risking executes even when grid trading is paused — the fix for the pause-while-bag-holding bug |

### Fee-Aware Grids (Binance.US 0% maker / 0.02% taker)

Grid limit orders pay maker fees, so minimum profitable spacing is now
computed from the maker rate (0%) with an absolute floor
(`min_spacing_floor_percent`, default 0.15%) covering spread and slippage —
instead of the old flat 0.1% assumption that forced ≥0.36% spacing.
Tighter grids = more completed cycles in the same chop.

### Reliability & Alerting

| Feature | Description |
|---------|-------------|
| **Auth-error handling** | An invalid API key no longer crash-loops every 23s. The bot alerts once (urgent), re-checks every 15 min, and resumes automatically when the key is fixed |
| **Push alerts** (`src/notifier.py`) | ntfy.sh / webhook / Telegram alerts on bear regime, de-risk stages, stops, auth failures, and crashes. stdlib-only, rate-limited, no-op when unconfigured |
| **Honest healthcheck** | Docker healthcheck now verifies trading-loop liveness via the heartbeat sentinel, not just that Python can import libraries |
| **Daily report** (`daily_report.py`) | Cron-driven phone summary: portfolio value, exposure, P&L, drawdown vs peak, today's trades — plus loud warnings if the heartbeat is stale or the API key is broken. Runs independently of the bot |

New config sections: `risk_management`, `alerts`, `maker_fee_rate` /
`taker_fee_rate`, `min_spacing_floor_percent`, `enable_exposure_management`.
See `src/priv/config.json.template` — all have working defaults.

---

## Previous Release Highlights — Security Hardening

A security-focused maintenance release. No behavioral changes to the
trading engine — all prior profit-optimization work was preserved. Highlights:

- **Fatal-error handling no longer leaks tracebacks to stderr.** `main.py` and
  `grid_bot.py` now route unhandled exceptions through `logger.exception(...)`,
  which writes through the configured logging pipeline instead of printing raw
  traceback frames. This keeps exception payloads (which can include exchange
  responses) out of unmanaged streams.
- **Docker entrypoint no longer string-interpolates paths into Python.** The
  config-validation and API-key probes in `docker-entrypoint.sh` now pass the
  config path via `sys.argv` instead of embedding it in a Python one-liner,
  eliminating a theoretical shell-to-Python injection vector.
- **Version unification.** All modules, Docker artifacts, shell scripts, and
  the config template now report the same, single version label. Prior
  releases mixed v2.0 / v14.1 / v15.0 labels across layers.

## Previous Release Highlights — Profit Optimization

A comprehensive profitability tuning pass across the entire trading engine. Every parameter was reviewed against a month of live performance data and adjusted to extract more profit per cycle, compound gains faster, and keep capital deployed more efficiently — all while preserving the existing safety guardrails.

### Tighter, More Profitable Grid Spacing

| Change | Before | After | Impact |
|--------|---------------|--------------|--------|
| Fee safety factor | 2.5x | 1.8x | Minimum profitable spacing drops from 0.5% to 0.36% — more cycles complete |
| Low-volatility spacing | Tightens below 2% vol | Tightens below 2.5%, aggressively below 1.5% | More fills in calm markets |
| RSI mean-reversion multiplier | 0.80x at extremes | 0.72x at extremes | Much tighter grid when cycles complete fastest |
| ADX ranging bonus | 0.9x below 15 | 0.85x below 15, 0.9x below 20 | Captures more ranging-market profit |
| Asymmetric level progression | 10% wider per level | 5% wider per level | Denser grid near current price = more fills |

### Faster Capital Redeployment

| Change | Before | After | Impact |
|--------|---------------|--------------|--------|
| Stale order timeout | 60 minutes | 30 minutes | Frees capital 2x faster for redeployment |
| Grid reposition threshold | 2.0x spacing | 1.5x spacing | Grid re-centers sooner on price moves |
| Grid update interval | 5 minutes | 4 minutes | Faster adaptation to new conditions |
| Position age penalty | Starts at 24h | Starts at 8h | Unsticks capital from old positions 3x sooner |

### Accelerated Profit Compounding

| Change | Before | After | Impact |
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

## Previous Release Highlights — Smart Adaptive Engine

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


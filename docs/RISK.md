# Risk Management & P&L

[← Back to README](../README.md)

## Risk Management

### Exposure Limits
- **Max 70% of portfolio in crypto** (configurable via `max_position_percent`)
- **Max 10% per single order** (configurable via `max_single_order_percent`)
- Automatic reduction when exposure exceeds limits

### Exposure Controller (primary defense)
Runs every cycle, *before* the trend filter, and unifies three mechanisms
into a single target ETH exposure (see `src/risk_manager.py`):

- **Regime targets** — bull 65%, ranging 45%, bear floor 15%, staged
  transitions with hysteresis (3 confirmations in, 4 out + min hold)
- **Trailing stop from persisted peak** — drawdown caps exposure in stages:
  -5% → 50%, -8% → 25%, -10% → floor, -20% → full exit + halt. The peak
  survives restarts via `data/risk_state.json`
- **Constant-mix rebalancing** — trades back toward target when actual
  exposure drifts >7 points; guarantees a permanent USDT reserve

The effective target also caps `max_position_percent`, so grid buying can
never rebuild exposure the controller just reduced.

### Stop Loss (backstop)
The scenario-level `stop_loss_percent` (vs. initial investment) remains as
a final backstop and triggers a full emergency exit.

### Trend Filter
- Calculates ADX every cycle
- **Pauses grid trading for 30 minutes** when ADX > 40
- Logs warnings when ADX > 25
- Pausing no longer freezes risk management — the exposure controller
  keeps de-risking while the grid is paused

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


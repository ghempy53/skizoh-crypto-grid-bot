# Operations & Monitoring

[← Back to README](../README.md)

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

### Push Alerts to Your Phone (v4.1)

Set a unique topic in `config.json` and subscribe to it in the
[ntfy](https://ntfy.sh) mobile app — no account or API key needed:

```json
"alerts": { "ntfy_topic": "skizoh-gridbot-<something-random>" }
```

The bot pushes: API-key failures (urgent, re-checked every 15 min), bear
regime confirmations, de-risk stages, rebalances, stops, and crashes.
Webhook and Telegram channels are also supported (see the template).
Treat the topic name like a password.

### Daily Report (v4.1)

`daily_report.py` sends a daily phone summary — portfolio value, exposure
vs. target, P&L, drawdown from peak, today's trades — and warns loudly if
the heartbeat is stale or the API key is broken. It is stdlib-only and runs
outside Docker, so it reports even when the bot is down:

```bash
python3 daily_report.py --dry-run     # preview without sending
crontab -e                            # then add:
0 8 * * * cd ~/skizoh-crypto-grid-bot && /usr/bin/python3 daily_report.py >> data/daily_report.log 2>&1
```

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


#!/usr/bin/env python3
# =============================================================================
# SKIZOH GRID BOT - Daily Report
#
# Standalone (stdlib-only) daily summary pushed to your phone via the same
# alert channels as the bot (ntfy/webhook/telegram from config "alerts").
# Runs independently of the trading loop, so it still reports when the bot
# is down — including a loud warning if the API key is broken or the
# heartbeat is stale.
#
# Usage:
#   python3 daily_report.py            # send report
#   python3 daily_report.py --dry-run  # print report, don't send
#
# Cron (8:00 AM daily):
#   0 8 * * * cd /home/<user>/skizoh-crypto-grid-bot && /usr/bin/python3 daily_report.py >> data/daily_report.log 2>&1
# =============================================================================

import csv
import hashlib
import hmac
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
DATA_DIR = SCRIPT_DIR / 'data'
CONFIG_FILE = SCRIPT_DIR / 'src' / 'priv' / 'config.json'

sys.path.insert(0, str(SCRIPT_DIR / 'src'))
from notifier import Notifier  # stdlib-only module

API_BASE = 'https://api.binance.us'
HEARTBEAT_STALE_SECONDS = 15 * 60


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return None


def http_get(url, headers=None, timeout=15):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def fetch_ticker(symbol_compact):
    """Public 24h ticker — no auth required."""
    try:
        return http_get(f"{API_BASE}/api/v3/ticker/24hr?symbol={symbol_compact}")
    except Exception:
        return None


def fetch_balances(api_key, api_secret, assets):
    """Signed account call via stdlib HMAC. Returns (balances|None, error|None)."""
    try:
        query = urllib.parse.urlencode({
            'timestamp': int(time.time() * 1000), 'recvWindow': 60000,
        })
        sig = hmac.new(api_secret.encode(), query.encode(),
                       hashlib.sha256).hexdigest()
        data = http_get(f"{API_BASE}/api/v3/account?{query}&signature={sig}",
                        headers={'X-MBX-APIKEY': api_key})
        out = {}
        for b in data.get('balances', []):
            if b['asset'] in assets:
                out[b['asset']] = float(b['free']) + float(b['locked'])
        return out, None
    except urllib.error.HTTPError as e:
        if e.code in (400, 401, 403, 418):
            return None, ('auth', f"HTTP {e.code}: {e.read().decode()[:100]}")
        return None, ('network', f"HTTP {e.code}")
    except Exception as e:
        return None, ('network', str(e))


def todays_trades(tax_file):
    """(count, realized_pnl, fees) for trades dated today."""
    today = datetime.now().strftime('%Y-%m-%d')
    count, pnl, fees = 0, 0.0, 0.0
    try:
        with open(tax_file) as f:
            for row in csv.DictReader(f):
                if row.get('Date/Time', '').startswith(today):
                    count += 1
                    pnl += float(row.get('Realized P&L (USD)', 0) or 0)
                    fees += float(row.get('Fee (USD)', 0) or 0)
    except Exception:
        pass
    return count, pnl, fees


def build_report():
    config = load_json(CONFIG_FILE) or {}
    symbol = config.get('symbol', 'ETH/USDT')
    base, quote = symbol.split('/')
    compact = symbol.replace('/', '')

    lines = []
    warnings = []
    priority = 'default'

    # --- Bot liveness ---------------------------------------------------
    hb = load_json(DATA_DIR / 'heartbeat.json')
    if hb:
        try:
            ts = datetime.fromisoformat(hb['timestamp'])
            age = (datetime.now(timezone.utc) - ts).total_seconds()
            if age > HEARTBEAT_STALE_SECONDS:
                warnings.append(f"BOT DOWN? Heartbeat is {age/3600:.1f}h old")
                priority = 'high'
            else:
                lines.append(f"Bot: alive ({hb.get('regime', '?')}, "
                             f"{hb.get('cycles', 0)} cycles)")
        except Exception:
            warnings.append("BOT DOWN? Heartbeat unreadable")
            priority = 'high'
    else:
        warnings.append("BOT DOWN? No heartbeat file")
        priority = 'high'

    # --- Price (public) -------------------------------------------------
    ticker = fetch_ticker(compact)
    price = float(ticker['lastPrice']) if ticker else 0.0
    if ticker:
        lines.append(f"{base}: ${price:,.2f} "
                     f"({float(ticker['priceChangePercent']):+.1f}% 24h)")

    # --- Balances (signed) — doubles as a daily API-key canary ----------
    balances, err = fetch_balances(
        config.get('api_key', ''), config.get('api_secret', ''),
        {base, quote})
    if err:
        kind, detail = err
        if kind == 'auth':
            warnings.append(f"API KEY BROKEN: {detail[:120]} — "
                            f"rotate key at Binance.US > API Management")
            priority = 'urgent'
        else:
            warnings.append(f"API unreachable: {detail[:120]}")
            priority = 'high' if priority == 'default' else priority
    elif balances is not None and price > 0:
        base_qty = balances.get(base, 0.0)
        quote_qty = balances.get(quote, 0.0)
        total = base_qty * price + quote_qty
        exposure = (base_qty * price / total * 100) if total > 0 else 0
        lines.append(f"Portfolio: ${total:,.2f} "
                     f"({base_qty:.5f} {base} + ${quote_qty:,.2f})")
        lines.append(f"Exposure: {exposure:.0f}% {base}")

        risk = load_json(DATA_DIR / 'risk_state.json')
        if risk:
            peak = risk.get('peak_value', 0)
            if peak > 0:
                dd = (peak - total) / peak * 100
                lines.append(f"Peak: ${peak:,.2f} (drawdown {max(0, dd):.1f}%)"
                             + (" [BEAR MODE]" if risk.get('in_bear_mode') else ""))

    # --- P&L -------------------------------------------------------------
    pos = load_json(DATA_DIR / 'position_state.json')
    if pos:
        realized = pos.get('realized_pnl', 0.0)
        cost = pos.get('total_cost', 0.0)
        qty = pos.get('total_quantity', 0.0)
        unrealized = qty * price - cost if price > 0 else 0.0
        lines.append(f"P&L: realized ${realized:+.2f}, "
                     f"unrealized ${unrealized:+.2f}")

    n, day_pnl, day_fees = todays_trades(DATA_DIR / 'tax_transactions.csv')
    lines.append(f"Today: {n} trades, ${day_pnl:+.2f} realized, "
                 f"${day_fees:.2f} fees")

    body = ""
    if warnings:
        body += "⚠️ " + "\n⚠️ ".join(warnings) + "\n\n"
    body += "\n".join(lines)
    title = "Grid Bot daily report" + (" — ATTENTION" if warnings else "")
    return title, body, priority, config.get('alerts')


def main():
    title, body, priority, alerts_cfg = build_report()
    if '--dry-run' in sys.argv:
        print(f"[{priority}] {title}\n{body}")
        return
    n = Notifier(alerts_cfg)
    # Fresh rate-limit state per process, so the daily send always goes out
    if not n.enabled:
        print("No alert channels configured ('alerts' in config.json)")
        sys.exit(1)
    ok = n.send(title, body, key='daily-report', priority=priority)
    print(f"{datetime.now().isoformat()} report {'sent' if ok else 'FAILED'}")
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()

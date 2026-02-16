#!/usr/bin/env python3
# =============================================================================
# SKIZOH CRYPTO GRID BOT - Portfolio Helper
# =============================================================================
# Quick one-liner commands to view portfolio status, transactions, tax info,
# balances, profit/loss, and more.
#
# Usage:
#   python portfolio.py                  Show full portfolio dashboard
#   python portfolio.py balance          ETH and USD balances
#   python portfolio.py transactions     Recent transactions (default: last 20)
#   python portfolio.py transactions 50  Last 50 transactions
#   python portfolio.py pnl              All-time profit and loss breakdown
#   python portfolio.py tax              Current year tax summary
#   python portfolio.py tax 2025         Tax summary for specific year
#   python portfolio.py fees             Total fees paid
#   python portfolio.py positions        Open positions and cost basis
#   python portfolio.py daily            Daily P&L breakdown
#   python portfolio.py summary          Compact one-line summary
#   python portfolio.py export 2025      Export Form 8949 CSV for a year
# =============================================================================

import csv
import json
import sys
import os
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

# Resolve paths relative to this script
SCRIPT_DIR = Path(__file__).parent.resolve()
DATA_DIR = SCRIPT_DIR / 'data'
CONFIG_FILE = SCRIPT_DIR / 'src' / 'priv' / 'config.json'
POSITION_STATE_FILE = DATA_DIR / 'position_state.json'
TAX_TRANSACTIONS_FILE = DATA_DIR / 'tax_transactions.csv'
POSITION_ARCHIVE_FILE = DATA_DIR / 'position_state_archive.csv'

# Short-term capital gains tax rate brackets (2025 US federal, single filer)
# Used for estimation only - always consult a tax professional
FEDERAL_TAX_BRACKETS = [
    (11925, 0.10),
    (48475, 0.12),
    (103350, 0.22),
    (197300, 0.24),
    (250525, 0.32),
    (626350, 0.35),
    (float('inf'), 0.37),
]


def load_config():
    """Load bot configuration."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        print("Error: config.json is malformed.")
        return None


def load_position_state():
    """Load current position state from JSON."""
    try:
        with open(POSITION_STATE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        print("Error: position_state.json is malformed.")
        return None


def load_transactions():
    """Load all transactions from the tax CSV."""
    transactions = []
    try:
        with open(TAX_TRANSACTIONS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                transactions.append(row)
    except FileNotFoundError:
        pass
    return transactions


def safe_float(value, default=0.0):
    """Safely convert a value to float."""
    try:
        return float(value) if value else default
    except (ValueError, TypeError):
        return default


def format_usd(amount):
    """Format a number as USD."""
    if amount >= 0:
        return f"${amount:,.2f}"
    return f"-${abs(amount):,.2f}"


def format_eth(amount):
    """Format ETH amount."""
    return f"{amount:.8f} ETH"


def format_pnl(amount):
    """Format P&L with color indicator."""
    if amount > 0:
        return f"+{format_usd(amount)}"
    elif amount < 0:
        return format_usd(amount)
    return format_usd(0)


def estimate_tax_owed(taxable_gains):
    """Estimate federal tax on short-term capital gains.

    This is a rough estimate only. Grid bot trades are typically short-term
    capital gains taxed as ordinary income. This does NOT account for state
    taxes, other income, deductions, or filing status.
    """
    if taxable_gains <= 0:
        return 0.0

    tax = 0.0
    remaining = taxable_gains
    prev_bracket = 0

    for bracket_top, rate in FEDERAL_TAX_BRACKETS:
        bracket_amount = min(remaining, bracket_top - prev_bracket)
        if bracket_amount <= 0:
            break
        tax += bracket_amount * rate
        remaining -= bracket_amount
        prev_bracket = bracket_top

    return tax


# =============================================================================
# Commands
# =============================================================================

def cmd_dashboard():
    """Full portfolio dashboard."""
    state = load_position_state()
    transactions = load_transactions()
    config = load_config()

    print()
    print("=" * 70)
    print("  SKIZOH GRID BOT - PORTFOLIO DASHBOARD")
    print("=" * 70)

    if not state and not transactions:
        print("\n  No data found. Run the bot first to generate portfolio data.")
        print(f"  Expected data directory: {DATA_DIR}")
        print("=" * 70 + "\n")
        return

    # Position state
    if state:
        total_qty = safe_float(state.get('total_quantity'))
        total_cost = safe_float(state.get('total_cost'))
        realized_pnl = safe_float(state.get('realized_pnl'))
        total_fees = safe_float(state.get('total_fees_paid'))
        avg_cost = total_cost / total_qty if total_qty > 0 else 0
        num_positions = len(state.get('positions', []))
        last_updated = state.get('last_updated', 'Unknown')

        print(f"\n  {'CURRENT HOLDINGS':─<40}")
        print(f"  ETH Held:          {format_eth(total_qty)}")
        print(f"  Cost Basis:        {format_usd(total_cost)}")
        print(f"  Avg Entry Price:   {format_usd(avg_cost)}")
        print(f"  Open Positions:    {num_positions}")
        print(f"  Last Updated:      {last_updated}")

        print(f"\n  {'PROFIT & LOSS':─<40}")
        print(f"  Realized P&L:      {format_pnl(realized_pnl)}")
        print(f"  Total Fees Paid:   {format_usd(total_fees)}")
        print(f"  Net After Fees:    {format_pnl(realized_pnl)}")

    # Transaction stats
    if transactions:
        buys = [tx for tx in transactions if tx.get('Transaction Type') == 'BUY']
        sells = [tx for tx in transactions if tx.get('Transaction Type') == 'SELL']
        total_buy_value = sum(safe_float(tx.get('Total Value (USD)')) for tx in buys)
        total_sell_value = sum(safe_float(tx.get('Total Value (USD)')) for tx in sells)
        total_realized = sum(safe_float(tx.get('Realized P&L (USD)')) for tx in sells)
        total_fees_tx = sum(safe_float(tx.get('Fee (USD)')) for tx in transactions)

        # Wins vs losses
        wins = [tx for tx in sells if safe_float(tx.get('Realized P&L (USD)')) > 0]
        losses = [tx for tx in sells if safe_float(tx.get('Realized P&L (USD)')) < 0]
        total_wins = sum(safe_float(tx.get('Realized P&L (USD)')) for tx in wins)
        total_losses = sum(safe_float(tx.get('Realized P&L (USD)')) for tx in losses)
        win_rate = (len(wins) / len(sells) * 100) if sells else 0

        print(f"\n  {'TRADING ACTIVITY':─<40}")
        print(f"  Total Buys:        {len(buys)}")
        print(f"  Total Sells:       {len(sells)}")
        print(f"  Total Volume In:   {format_usd(total_buy_value)}")
        print(f"  Total Volume Out:  {format_usd(total_sell_value)}")
        print(f"  Total Fees (Txns): {format_usd(total_fees_tx)}")

        print(f"\n  {'WIN/LOSS ANALYSIS':─<40}")
        print(f"  Winning Trades:    {len(wins)} ({format_pnl(total_wins)})")
        print(f"  Losing Trades:     {len(losses)} ({format_pnl(total_losses)})")
        print(f"  Win Rate:          {win_rate:.1f}%")
        if wins:
            best = max(safe_float(tx.get('Realized P&L (USD)')) for tx in sells)
            print(f"  Best Trade:        {format_pnl(best)}")
        if losses:
            worst = min(safe_float(tx.get('Realized P&L (USD)')) for tx in sells)
            print(f"  Worst Trade:       {format_pnl(worst)}")

        # Current year tax estimate
        current_year = datetime.now().year
        year_txns = [tx for tx in sells
                     if _parse_year(tx.get('Date/Time')) == current_year]
        year_gains = sum(safe_float(tx.get('Realized P&L (USD)')) for tx in year_txns)
        est_tax = estimate_tax_owed(year_gains) if year_gains > 0 else 0

        print(f"\n  {'TAX ESTIMATE ({current_year})':─<40}")
        print(f"  Realized Gains:    {format_pnl(year_gains)}")
        print(f"  Est. Federal Tax:  {format_usd(est_tax)}")
        print(f"  (Short-term capital gains rate, single filer estimate)")

        # Time range
        if transactions:
            first_date = transactions[0].get('Date/Time', 'Unknown')
            last_date = transactions[-1].get('Date/Time', 'Unknown')
            print(f"\n  {'DATA RANGE':─<40}")
            print(f"  First Transaction: {first_date}")
            print(f"  Last Transaction:  {last_date}")
            print(f"  Total Records:     {len(transactions)}")

    if config:
        symbol = config.get('symbol', 'ETH/USDT')
        fee_rate = config.get('fee_rate', 0.001)
        bnb_fees = config.get('use_bnb_for_fees', False)
        effective_fee = fee_rate * 0.75 if bnb_fees else fee_rate

        print(f"\n  {'BOT CONFIG':─<40}")
        print(f"  Trading Pair:      {symbol}")
        print(f"  Fee Rate:          {effective_fee * 100:.3f}%{'  (BNB discount)' if bnb_fees else ''}")
        print(f"  Max Exposure:      {config.get('max_position_percent', 70)}%")

    print("\n" + "=" * 70)
    print("  TIP: Run 'python portfolio.py help' for all commands")
    print("=" * 70 + "\n")


def cmd_balance():
    """Show ETH and USD balances from position state."""
    state = load_position_state()

    print()
    print("-" * 50)
    print("  CURRENT BALANCES (from position tracker)")
    print("-" * 50)

    if not state:
        print("  No position data found. Run the bot first.")
        print("-" * 50 + "\n")
        return

    total_qty = safe_float(state.get('total_quantity'))
    total_cost = safe_float(state.get('total_cost'))
    avg_cost = total_cost / total_qty if total_qty > 0 else 0

    print(f"  ETH Held:        {format_eth(total_qty)}")
    print(f"  Cost Basis:      {format_usd(total_cost)}")
    print(f"  Avg Entry:       {format_usd(avg_cost)}")
    print(f"  Open Positions:  {len(state.get('positions', []))}")
    print(f"  Last Updated:    {state.get('last_updated', 'Unknown')}")
    print("-" * 50 + "\n")


def cmd_transactions(count=20):
    """Show recent transactions."""
    transactions = load_transactions()

    if not transactions:
        print("\n  No transactions found.\n")
        return

    recent = transactions[-count:]

    print()
    print(f"  RECENT TRANSACTIONS (last {min(count, len(transactions))} of {len(transactions)})")
    print("-" * 95)
    print(f"  {'Date/Time':<20} {'Type':<5} {'Amount':>12} {'Price':>10} {'Value':>12} {'P&L':>12} {'Fee':>8}")
    print("-" * 95)

    for tx in recent:
        dt = tx.get('Date/Time', '')[:19]
        tx_type = tx.get('Transaction Type', '?')[:4]
        amount = safe_float(tx.get('Amount'))
        price = safe_float(tx.get('Price (USD)'))
        value = safe_float(tx.get('Total Value (USD)'))
        pnl = safe_float(tx.get('Realized P&L (USD)'))
        fee = safe_float(tx.get('Fee (USD)'))

        pnl_str = f"{pnl:+.2f}" if tx_type == 'SELL' else ""

        print(f"  {dt:<20} {tx_type:<5} {amount:>12.6f} {price:>10.2f} {value:>12.2f} {pnl_str:>12} {fee:>8.4f}")

    print("-" * 95 + "\n")


def cmd_pnl():
    """Show all-time profit and loss breakdown."""
    state = load_position_state()
    transactions = load_transactions()

    print()
    print("=" * 60)
    print("  ALL-TIME PROFIT & LOSS")
    print("=" * 60)

    if state:
        realized = safe_float(state.get('realized_pnl'))
        total_fees = safe_float(state.get('total_fees_paid'))
        print(f"\n  From Position Tracker:")
        print(f"    Realized P&L:    {format_pnl(realized)}")
        print(f"    Total Fees:      {format_usd(total_fees)}")

    if transactions:
        sells = [tx for tx in transactions if tx.get('Transaction Type') == 'SELL']
        total_realized = sum(safe_float(tx.get('Realized P&L (USD)')) for tx in sells)
        total_fees_tx = sum(safe_float(tx.get('Fee (USD)')) for tx in transactions)

        wins = [tx for tx in sells if safe_float(tx.get('Realized P&L (USD)')) > 0]
        losses = [tx for tx in sells if safe_float(tx.get('Realized P&L (USD)')) < 0]
        total_wins = sum(safe_float(tx.get('Realized P&L (USD)')) for tx in wins)
        total_losses = sum(safe_float(tx.get('Realized P&L (USD)')) for tx in losses)

        print(f"\n  From Transaction Log:")
        print(f"    Total Realized:  {format_pnl(total_realized)}")
        print(f"    Gross Wins:      {format_pnl(total_wins)} ({len(wins)} trades)")
        print(f"    Gross Losses:    {format_pnl(total_losses)} ({len(losses)} trades)")
        print(f"    Total Fees:      {format_usd(total_fees_tx)}")
        print(f"    Net P&L:         {format_pnl(total_realized)}")

        # Monthly breakdown
        monthly = defaultdict(float)
        for tx in sells:
            dt = tx.get('Date/Time', '')
            if dt:
                month_key = dt[:7]  # YYYY-MM
                monthly[month_key] += safe_float(tx.get('Realized P&L (USD)'))

        if monthly:
            print(f"\n  Monthly Realized P&L:")
            for month in sorted(monthly.keys()):
                bar_len = int(min(abs(monthly[month]) / 10, 30))
                bar = "+" * bar_len if monthly[month] >= 0 else "-" * bar_len
                print(f"    {month}:  {format_pnl(monthly[month]):>14}  {bar}")

    if not state and not transactions:
        print("\n  No data available.")

    print("\n" + "=" * 60 + "\n")


def _parse_year(date_str):
    """Extract year from a date string."""
    try:
        return datetime.strptime(date_str[:10], '%Y-%m-%d').year
    except (ValueError, TypeError):
        return None


def cmd_tax(year=None):
    """Show tax summary for a given year."""
    if year is None:
        year = datetime.now().year

    transactions = load_transactions()
    if not transactions:
        print(f"\n  No transactions found.\n")
        return

    sells = [tx for tx in transactions
             if tx.get('Transaction Type') == 'SELL'
             and _parse_year(tx.get('Date/Time')) == year]
    buys = [tx for tx in transactions
            if tx.get('Transaction Type') == 'BUY'
            and _parse_year(tx.get('Date/Time')) == year]
    all_year = [tx for tx in transactions
                if _parse_year(tx.get('Date/Time')) == year]

    total_gains = sum(safe_float(tx.get('Realized P&L (USD)'))
                      for tx in sells if safe_float(tx.get('Realized P&L (USD)')) > 0)
    total_losses = sum(safe_float(tx.get('Realized P&L (USD)'))
                       for tx in sells if safe_float(tx.get('Realized P&L (USD)')) < 0)
    net_realized = total_gains + total_losses
    total_fees = sum(safe_float(tx.get('Fee (USD)')) for tx in all_year)
    total_volume = sum(safe_float(tx.get('Total Value (USD)')) for tx in all_year)
    est_tax = estimate_tax_owed(net_realized) if net_realized > 0 else 0

    print()
    print("=" * 60)
    print(f"  TAX SUMMARY - {year}")
    print("=" * 60)
    print(f"\n  Transactions:")
    print(f"    Buy Orders:      {len(buys)}")
    print(f"    Sell Orders:     {len(sells)}")
    print(f"    Total Volume:    {format_usd(total_volume)}")
    print(f"    Total Fees:      {format_usd(total_fees)}")
    print(f"\n  Capital Gains/Losses:")
    print(f"    Short-Term Gains:  {format_pnl(total_gains)}")
    print(f"    Short-Term Losses: {format_pnl(total_losses)}")
    print(f"    Net Realized:      {format_pnl(net_realized)}")
    print(f"\n  Estimated Tax Owed:")
    print(f"    Federal (est.):    {format_usd(est_tax)}")
    if net_realized > 0:
        eff_rate = (est_tax / net_realized * 100) if net_realized > 0 else 0
        print(f"    Effective Rate:    {eff_rate:.1f}%")
        print(f"\n    Note: This is a rough estimate for short-term gains")
        print(f"    taxed as ordinary income (single filer, federal only).")
        print(f"    Does NOT include state taxes or other income.")
    elif net_realized < 0:
        print(f"\n    Net capital loss of {format_usd(abs(net_realized))}")
        deductible = min(abs(net_realized), 3000)
        print(f"    Up to {format_usd(deductible)} deductible against ordinary income")
        if abs(net_realized) > 3000:
            carryover = abs(net_realized) - 3000
            print(f"    Remaining {format_usd(carryover)} carries forward to next year")
    else:
        print(f"    No taxable gains for {year}.")

    print(f"\n  Filing Notes:")
    print(f"    - Report on IRS Form 8949")
    print(f"    - Transfer totals to Schedule D")
    print(f"    - FIFO cost basis method used")
    print(f"    - Grid trades = short-term capital gains")
    print(f"    - Consult a tax professional")
    print(f"\n  Export: python portfolio.py export {year}")
    print("=" * 60 + "\n")


def cmd_fees():
    """Show total fees paid."""
    state = load_position_state()
    transactions = load_transactions()

    print()
    print("-" * 50)
    print("  FEE ANALYSIS")
    print("-" * 50)

    if state:
        print(f"  Position Tracker Fees: {format_usd(safe_float(state.get('total_fees_paid')))}")

    if transactions:
        total = sum(safe_float(tx.get('Fee (USD)')) for tx in transactions)
        buy_fees = sum(safe_float(tx.get('Fee (USD)'))
                       for tx in transactions if tx.get('Transaction Type') == 'BUY')
        sell_fees = sum(safe_float(tx.get('Fee (USD)'))
                        for tx in transactions if tx.get('Transaction Type') == 'SELL')

        # Monthly fee breakdown
        monthly = defaultdict(float)
        for tx in transactions:
            dt = tx.get('Date/Time', '')
            if dt:
                monthly[dt[:7]] += safe_float(tx.get('Fee (USD)'))

        print(f"  Transaction Log Fees:")
        print(f"    Buy Fees:    {format_usd(buy_fees)}")
        print(f"    Sell Fees:   {format_usd(sell_fees)}")
        print(f"    Total Fees:  {format_usd(total)}")

        if len(monthly) > 1:
            avg_monthly = total / len(monthly)
            print(f"    Avg Monthly: {format_usd(avg_monthly)}")

    if not state and not transactions:
        print("  No data available.")

    print("-" * 50 + "\n")


def cmd_positions():
    """Show open positions and cost basis details."""
    state = load_position_state()

    print()
    print("=" * 70)
    print("  OPEN POSITIONS (FIFO Order)")
    print("=" * 70)

    if not state:
        print("  No position data found.\n")
        return

    positions = state.get('positions', [])
    if not positions:
        print("  No open positions.")
        print("=" * 70 + "\n")
        return

    print(f"\n  {'#':<4} {'Timestamp':<20} {'Quantity':>12} {'Entry Price':>12} {'Cost Basis':>12}")
    print("  " + "-" * 64)

    total_qty = 0
    total_cost = 0
    for i, pos in enumerate(positions, 1):
        qty = safe_float(pos.get('quantity'))
        price = safe_float(pos.get('price'))
        cost = safe_float(pos.get('cost_basis'))
        ts = pos.get('timestamp', 'Unknown')[:19]

        total_qty += qty
        total_cost += cost

        print(f"  {i:<4} {ts:<20} {qty:>12.6f} {price:>12.2f} {cost:>12.2f}")

    print("  " + "-" * 64)
    avg = total_cost / total_qty if total_qty > 0 else 0
    print(f"  {'TOTAL':<4} {'':<20} {total_qty:>12.6f} {avg:>12.2f} {total_cost:>12.2f}")

    print(f"\n  Realized P&L:   {format_pnl(safe_float(state.get('realized_pnl')))}")
    print(f"  Total Fees:     {format_usd(safe_float(state.get('total_fees_paid')))}")
    print("=" * 70 + "\n")


def cmd_daily():
    """Show daily P&L breakdown."""
    transactions = load_transactions()
    if not transactions:
        print("\n  No transactions found.\n")
        return

    sells = [tx for tx in transactions if tx.get('Transaction Type') == 'SELL']
    if not sells:
        print("\n  No sell transactions to analyze.\n")
        return

    daily_pnl = defaultdict(float)
    daily_count = defaultdict(int)
    daily_volume = defaultdict(float)

    for tx in sells:
        dt = tx.get('Date/Time', '')
        if dt:
            day = dt[:10]
            daily_pnl[day] += safe_float(tx.get('Realized P&L (USD)'))
            daily_count[day] += 1
            daily_volume[day] += safe_float(tx.get('Total Value (USD)'))

    print()
    print("=" * 75)
    print("  DAILY P&L BREAKDOWN")
    print("=" * 75)
    print(f"\n  {'Date':<12} {'Trades':>7} {'Volume':>12} {'P&L':>14} {'Cumulative':>14}")
    print("  " + "-" * 63)

    cumulative = 0
    for day in sorted(daily_pnl.keys()):
        cumulative += daily_pnl[day]
        pnl_str = f"{daily_pnl[day]:+.2f}"
        cum_str = f"{cumulative:+.2f}"
        print(f"  {day:<12} {daily_count[day]:>7} {daily_volume[day]:>12.2f} {pnl_str:>14} {cum_str:>14}")

    print("  " + "-" * 63)

    total_days = len(daily_pnl)
    total_pnl = sum(daily_pnl.values())
    profitable_days = sum(1 for v in daily_pnl.values() if v > 0)
    avg_daily = total_pnl / total_days if total_days > 0 else 0

    print(f"\n  Trading Days:     {total_days}")
    print(f"  Profitable Days:  {profitable_days} ({profitable_days / total_days * 100:.0f}%)" if total_days > 0 else "")
    print(f"  Avg Daily P&L:    {format_pnl(avg_daily)}")
    print(f"  Total P&L:        {format_pnl(total_pnl)}")
    if daily_pnl:
        best_day = max(daily_pnl, key=daily_pnl.get)
        worst_day = min(daily_pnl, key=daily_pnl.get)
        print(f"  Best Day:         {best_day} ({format_pnl(daily_pnl[best_day])})")
        print(f"  Worst Day:        {worst_day} ({format_pnl(daily_pnl[worst_day])})")
    print("=" * 75 + "\n")


def cmd_summary():
    """Compact one-line summary."""
    state = load_position_state()
    transactions = load_transactions()

    eth = 0.0
    realized = 0.0
    fees = 0.0
    cost_basis = 0.0

    if state:
        eth = safe_float(state.get('total_quantity'))
        realized = safe_float(state.get('realized_pnl'))
        fees = safe_float(state.get('total_fees_paid'))
        cost_basis = safe_float(state.get('total_cost'))

    num_txns = len(transactions) if transactions else 0
    sells = [tx for tx in (transactions or []) if tx.get('Transaction Type') == 'SELL']
    wins = sum(1 for tx in sells if safe_float(tx.get('Realized P&L (USD)')) > 0)
    win_rate = (wins / len(sells) * 100) if sells else 0

    print(f"ETH: {eth:.6f} | Cost: {format_usd(cost_basis)} | "
          f"P&L: {format_pnl(realized)} | Fees: {format_usd(fees)} | "
          f"Trades: {num_txns} | Win: {win_rate:.0f}%")


def cmd_export(year=None):
    """Export Form 8949 CSV for a given year."""
    if year is None:
        year = datetime.now().year

    transactions = load_transactions()
    if not transactions:
        print("\n  No transactions to export.\n")
        return

    sells = [tx for tx in transactions
             if tx.get('Transaction Type') == 'SELL'
             and _parse_year(tx.get('Date/Time')) == year]

    if not sells:
        print(f"\n  No sell transactions for {year}.\n")
        return

    output_file = DATA_DIR / f'form_8949_data_{year}.csv'

    try:
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Description of Property',
                'Date Acquired',
                'Date Sold',
                'Proceeds (Sales Price)',
                'Cost Basis',
                'Gain or Loss',
                'Notes'
            ])

            for sale in sells:
                proceeds = safe_float(sale.get('Net Proceeds (USD)'))
                cost_basis = safe_float(sale.get('Cost Basis (USD)'))
                gain_loss = safe_float(sale.get('Realized P&L (USD)'))

                writer.writerow([
                    f"{sale.get('Amount', '0')} {sale.get('Asset', 'ETH')}",
                    'Various (FIFO)',
                    sale.get('Date/Time', '')[:10],
                    f"${proceeds:.2f}",
                    f"${cost_basis:.2f}",
                    f"${gain_loss:.2f}",
                    sale.get('Notes', '')
                ])

        print(f"\n  Exported {len(sells)} transactions to: {output_file}")
        print(f"  Import into tax software or give to your accountant.\n")
    except IOError as e:
        print(f"\n  Error writing file: {e}\n")


def cmd_help():
    """Show help."""
    print("""
SKIZOH GRID BOT - Portfolio Helper
===================================

Usage: python portfolio.py [command] [options]

Commands:
  (none)            Full portfolio dashboard
  balance           Current ETH holdings and cost basis
  transactions [N]  Last N transactions (default: 20)
  pnl               All-time profit/loss with monthly breakdown
  tax [YEAR]        Tax summary and estimated tax owed
  fees              Fee analysis breakdown
  positions         Open positions with FIFO details
  daily             Daily P&L breakdown with cumulative totals
  summary           Compact one-line portfolio summary
  export [YEAR]     Export Form 8949 CSV for tax filing
  help              Show this help message

Examples:
  python portfolio.py                   Full dashboard
  python portfolio.py summary           Quick one-liner
  python portfolio.py transactions 50   Last 50 trades
  python portfolio.py tax 2025          2025 tax summary
  python portfolio.py export 2025       Export 2025 Form 8949
""")


def main():
    args = sys.argv[1:]

    if not args:
        cmd_dashboard()
        return

    command = args[0].lower()

    if command == 'help' or command == '--help' or command == '-h':
        cmd_help()
    elif command == 'balance' or command == 'bal':
        cmd_balance()
    elif command == 'transactions' or command == 'txns' or command == 'tx':
        count = 20
        if len(args) > 1:
            try:
                count = int(args[1])
            except ValueError:
                print(f"Invalid count: {args[1]}")
                return
        cmd_transactions(count)
    elif command == 'pnl' or command == 'profit' or command == 'pl':
        cmd_pnl()
    elif command == 'tax':
        year = None
        if len(args) > 1:
            try:
                year = int(args[1])
            except ValueError:
                print(f"Invalid year: {args[1]}")
                return
        cmd_tax(year)
    elif command == 'fees' or command == 'fee':
        cmd_fees()
    elif command == 'positions' or command == 'pos':
        cmd_positions()
    elif command == 'daily':
        cmd_daily()
    elif command == 'summary' or command == 'sum' or command == 's':
        cmd_summary()
    elif command == 'export':
        year = None
        if len(args) > 1:
            try:
                year = int(args[1])
            except ValueError:
                print(f"Invalid year: {args[1]}")
                return
        cmd_export(year)
    else:
        print(f"\n  Unknown command: {command}")
        print(f"  Run 'python portfolio.py help' for usage.\n")


if __name__ == '__main__':
    main()

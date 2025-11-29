# =============================================================================
# SKIZOH CRYPTO GRID TRADING BOT - Tax Summary Generator
# =============================================================================
# Generates IRS Form 8949 compatible reports with proper P&L tracking
# =============================================================================

import csv
from datetime import datetime
from collections import defaultdict
import os


def load_transactions(filename='../data/tax_transactions.csv'):
    """Load all transactions from CSV."""
    transactions = []
    
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                transactions.append(row)
        return transactions
    except FileNotFoundError:
        print(f"Error: {filename} not found. Run the bot first.")
        return []


def calculate_summary(transactions):
    """Calculate summary statistics from transactions."""
    if not transactions:
        return None
    
    total_buys = 0
    total_sells = 0
    total_buy_value = 0
    total_sell_value = 0
    total_fees = 0
    total_realized_pnl = 0
    
    for tx in transactions:
        fee = float(tx.get('Fee (USD)', 0) or 0)
        total_fees += fee
        
        if tx['Transaction Type'] == 'BUY':
            total_buys += 1
            total_buy_value += float(tx.get('Total Value (USD)', 0) or 0)
        elif tx['Transaction Type'] == 'SELL':
            total_sells += 1
            total_sell_value += float(tx.get('Total Value (USD)', 0) or 0)
            # Use pre-calculated P&L if available
            pnl = float(tx.get('Realized P&L (USD)', 0) or 0)
            total_realized_pnl += pnl
    
    return {
        'total_buys': total_buys,
        'total_sells': total_sells,
        'total_buy_value': total_buy_value,
        'total_sell_value': total_sell_value,
        'total_fees': total_fees,
        'total_realized_pnl': total_realized_pnl,
        'net_after_fees': total_realized_pnl - total_fees
    }


def generate_summary_report(transactions, year=None):
    """Generate comprehensive tax summary."""
    if not transactions:
        print("No transactions to summarize.")
        return
    
    # Filter by year if specified
    if year:
        transactions = [
            tx for tx in transactions
            if datetime.strptime(tx['Date/Time'], '%Y-%m-%d %H:%M:%S').year == year
        ]
        if not transactions:
            print(f"No transactions found for year {year}")
            return
    
    summary = calculate_summary(transactions)
    
    print("\n" + "="*70)
    print(f"CRYPTO TRADING TAX SUMMARY {'- ' + str(year) if year else ''}")
    print("="*70)
    
    print(f"\nTransaction Summary:")
    print(f"  Total Buy Orders:  {summary['total_buys']}")
    print(f"  Total Sell Orders: {summary['total_sells']}")
    print(f"  Total Fees Paid:   ${summary['total_fees']:.2f}")
    
    print(f"\nValue Summary:")
    print(f"  Total Bought:      ${summary['total_buy_value']:.2f}")
    print(f"  Total Sold:        ${summary['total_sell_value']:.2f}")
    
    print(f"\nProfit/Loss Summary:")
    print(f"  Realized P&L:      ${summary['total_realized_pnl']:.2f}")
    print(f"  Net After Fees:    ${summary['net_after_fees']:.2f}")
    
    if summary['total_realized_pnl'] > 0:
        print(f"\n  Status: TAXABLE GAIN")
        print(f"  Note: Grid trading = typically short-term capital gains")
    else:
        print(f"\n  Status: CAPITAL LOSS")
        print(f"  Note: Can offset other capital gains")
    
    print("\n" + "="*70)
    print("\nTAX FILING NOTES:")
    print("-" * 70)
    print("1. Report on IRS Form 8949 (Sales and Dispositions)")
    print("2. Transfer totals to Schedule D")
    print("3. This bot uses FIFO accounting")
    print("4. Grid trading = typically all short-term gains")
    print("5. Keep records for 7 years")
    print("6. Consult a tax professional")
    print("="*70 + "\n")


def export_form_8949_csv(transactions, year=None):
    """Export Form 8949 compatible CSV."""
    if year is None:
        year = datetime.now().year
    
    # Filter sells only (dispositions)
    sells = [tx for tx in transactions 
             if tx['Transaction Type'] == 'SELL'
             and datetime.strptime(tx['Date/Time'], '%Y-%m-%d %H:%M:%S').year == year]
    
    if not sells:
        print(f"No sales to export for {year}.")
        return
    
    filename = f'../data/form_8949_data_{year}.csv'
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Form 8949 headers
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
            proceeds = float(sale.get('Net Proceeds (USD)', 0) or 0)
            cost_basis = float(sale.get('Cost Basis (USD)', 0) or 0)
            gain_loss = float(sale.get('Realized P&L (USD)', 0) or 0)
            
            writer.writerow([
                f"{sale['Amount']} {sale['Asset']}",
                'Various (FIFO)',
                sale['Date/Time'].split(' ')[0],
                f"${proceeds:.2f}",
                f"${cost_basis:.2f}",
                f"${gain_loss:.2f}",
                sale.get('Notes', '')
            ])
    
    print(f"\n✅ Form 8949 data exported to: {filename}")
    print("Import this into tax software or give to your accountant.\n")


def export_full_report(transactions, year=None):
    """Export detailed transaction report."""
    if year is None:
        year = datetime.now().year
    
    if year:
        transactions = [
            tx for tx in transactions
            if datetime.strptime(tx['Date/Time'], '%Y-%m-%d %H:%M:%S').year == year
        ]
    
    if not transactions:
        print(f"No transactions for {year}")
        return
    
    filename = f'../data/full_report_{year}.csv'
    
    with open(filename, 'w', newline='') as f:
        if transactions:
            writer = csv.DictWriter(f, fieldnames=transactions[0].keys())
            writer.writeheader()
            writer.writerows(transactions)
    
    print(f"✅ Full report exported to: {filename}\n")


if __name__ == "__main__":
    import sys
    
    print("="*70)
    print("SKIZOH GRID BOT v14 - TAX SUMMARY GENERATOR")
    print("="*70)
    
    # Check for year argument
    year = None
    if len(sys.argv) > 1:
        try:
            year = int(sys.argv[1])
        except ValueError:
            print("Invalid year. Usage: python tax_summary.py [year]")
            sys.exit(1)
    
    transactions = load_transactions()
    
    if transactions:
        generate_summary_report(transactions, year)
        export_form_8949_csv(transactions, year or datetime.now().year)
        export_full_report(transactions, year or datetime.now().year)
    
    print("💡 TIP: Run this weekly to track your gains/losses")
    print("💡 Usage: python tax_summary.py [year]\n")

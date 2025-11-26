#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  ÆÆÆÆÆÆÆÆ   #  #  #  #  #  #  #  #  #  #  #  #                            
#                                                          ÆÆÆÆÆÆÆÆÆÆÆÆÆ                                #
# ÆÆÆÆÆÆÆÆÆÆÆÆÆÆ    ÆÆÆÆÆ    ÆÆÆÆÆÆ  ÆÆÆÆÆ   ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ          ÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ   ÆÆÆÆÆ   ÆÆÆÆÆÆ   ÆÆÆÆÆ   ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ   ÆÆÆÆÆÆÆÆÆÆÆÆ      ÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ   ÆÆÆÆÆ   ÆÆÆÆÆ    ÆÆÆÆÆ   ÆÆÆÆÆÆÆÆÆÆÆÆÆ ÆÆÆÆÆ        ÆÆÆÆÆÆÆÆÆÆ    ÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆ     ÆÆÆÆ    ÆÆÆÆÆ  ÆÆÆÆÆÆ    ÆÆÆÆÆ          ÆÆÆÆÆÆ ÆÆÆÆÆ           ÆÆÆÆÆÆÆÆÆ  ÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆ     ÆÆÆ     ÆÆÆÆÆ ÆÆÆÆÆÆ     ÆÆÆÆÆ         ÆÆÆÆÆÆ  ÆÆÆÆÆ     ÆÆ  ÆÆ    ÆÆÆÆÆÆ ÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆ     Æ       ÆÆÆÆÆ ÆÆÆÆÆ      ÆÆÆÆÆ         ÆÆÆÆÆ   ÆÆÆÆÆ     ÆÆ  ÆÆÆ    ÆÆÆÆÆ ÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆÆÆ           ÆÆÆÆÆÆÆÆÆÆ       ÆÆÆÆÆ        ÆÆÆÆÆÆ   ÆÆÆÆÆ     ÆÆÆ ÆÆÆ     ÆÆÆÆÆÆÆÆÆÆÆ     ÆÆÆÆÆ  #
#  ÆÆÆÆÆÆÆ          ÆÆÆÆÆÆÆÆÆÆ       ÆÆÆÆÆ       ÆÆÆÆÆÆ    ÆÆÆÆÆ     ÆÆÆ ÆÆÆ  Æ  ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ  #
#    ÆÆÆÆÆÆÆ        ÆÆÆÆÆÆÆÆÆ        ÆÆÆÆÆ       ÆÆÆÆÆÆ    ÆÆÆÆÆ ÆÆÆÆ        ÆÆ  ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ  #
#      ÆÆÆÆÆÆÆ      ÆÆÆÆÆÆÆÆÆ        ÆÆÆÆÆ      ÆÆÆÆÆÆ     ÆÆÆÆÆ  ÆÆÆ       ÆÆÆ  ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ  #
#       ÆÆÆÆÆÆÆÆ    ÆÆÆÆÆÆÆÆÆÆ       ÆÆÆÆÆ      ÆÆÆÆÆ      ÆÆÆÆÆ   ÆÆÆ     ÆÆÆ   ÆÆÆÆÆÆÆÆÆÆÆ     ÆÆÆÆÆ  #
#         ÆÆÆÆÆÆÆ   ÆÆÆÆÆÆÆÆÆÆÆ      ÆÆÆÆÆ     ÆÆÆÆÆÆ       ÆÆÆÆÆ   ÆÆÆÆÆÆÆ ÆÆÆ  ÆÆÆÆÆÆÆÆÆÆÆ     ÆÆÆÆÆ  #
#    ÆÆ     ÆÆÆÆÆ   ÆÆÆÆÆ ÆÆÆÆÆÆ     ÆÆÆÆÆ    ÆÆÆÆÆÆ        ÆÆÆÆÆ        ÆÆÆÆÆÆ  ÆÆÆÆÆÆÆÆÆÆÆ     ÆÆÆÆÆ  #
#  ÆÆÆÆ     ÆÆÆÆÆ   ÆÆÆÆÆ  ÆÆÆÆÆÆ    ÆÆÆÆÆ   ÆÆÆÆÆÆ          ÆÆÆÆÆ        ÆÆÆÆÆ  ÆÆÆÆÆÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆ     ÆÆÆÆÆ   ÆÆÆÆÆ   ÆÆÆÆÆ    ÆÆÆÆÆ   ÆÆÆÆÆÆ          ÆÆÆÆÆÆÆÆÆÆÆ    ÆÆÆ  ÆÆÆÆ ÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ   ÆÆÆÆÆ   ÆÆÆÆÆÆ   ÆÆÆÆÆ  ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ   ÆÆÆÆÆÆÆÆÆÆÆÆÆ      ÆÆÆÆ ÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ   ÆÆÆÆÆ    ÆÆÆÆÆÆ  ÆÆÆÆÆ  ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ    ÆÆÆÆÆÆÆÆÆÆÆÆÆ    ÆÆÆÆÆ ÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆÆÆÆÆÆÆÆÆÆ    ÆÆÆÆÆ     ÆÆÆÆÆÆ ÆÆÆÆÆ  ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ     ÆÆÆÆÆÆÆÆÆÆÆÆÆ   ÆÆÆÆÆ ÆÆÆÆÆÆ     ÆÆÆÆÆ  #
# ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ   ÆÆÆÆÆ    ÆÆÆÆÆÆÆÆÆÆ   ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ  #
# ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ  ÆÆÆÆÆÆÆÆ ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ  #
# ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ  #
#                                                                     ÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆÆ                  #
#                                                                       ÆÆÆ  ÆÆÆÆÆÆÆ                    #    
#                                                                        ÆÆÆÆ   ÆÆÆ                     #
#                                                                         ÆÆÆÆÆÆÆÆ                      #
#                                                                          ÆÆÆÆÆÆ                       #
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #   ÆÆÆÆ   #  #  #  #  #  #  #  #

# \file: tax_summary.py
# \Date: 11-26-2025
# \Description: Tax summary generator for crypto grid trading bot
#               Generates reports for US tax filing (IRS Form 8949)

import csv
from datetime import datetime
from collections import defaultdict

def load_transactions(filename='../data/tax_transactions.csv'):
    """Load all transactions from CSV.
    
    Args:
        filename (str): Path to tax transactions CSV file
    
    Returns:
        list: List of transaction dictionaries
    """
    transactions = []
    
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                transactions.append(row)
        return transactions
    except FileNotFoundError:
        print(f"Error: {filename} not found. Run the bot first to generate transactions.")
        return []

def calculate_capital_gains(transactions):
    """Calculate capital gains using FIFO (First In First Out) method.
    
    Args:
        transactions (list): List of transaction dictionaries
    
    Returns:
        tuple: (sales list, total gain, total proceeds, total cost basis)
    """
    # Track purchases (cost basis) for each asset
    purchase_queue = defaultdict(list)  # asset -> [(amount, price, date, fee)]
    
    # Track all sales and their gains
    sales = []
    total_gain = 0
    total_proceeds = 0
    total_cost_basis = 0
    
    for tx in transactions:
        tx_type = tx['Transaction Type']
        asset = tx['Asset']
        amount = float(tx['Amount'])
        price = float(tx['Price (USD)'])
        fee = float(tx['Fee (USD)'])
        date = tx['Date/Time']
        
        if tx_type == 'BUY':
            # Add to purchase queue (cost basis includes fee)
            cost_per_unit = price + (fee / amount)
            purchase_queue[asset].append({
                'amount': amount,
                'cost_per_unit': cost_per_unit,
                'date': date,
                'total_cost': amount * cost_per_unit
            })
        
        elif tx_type == 'SELL':
            # Calculate gain using FIFO
            remaining_to_sell = amount
            sale_proceeds = (amount * price) - fee
            sale_cost_basis = 0
            
            while remaining_to_sell > 0 and purchase_queue[asset]:
                purchase = purchase_queue[asset][0]
                
                if purchase['amount'] <= remaining_to_sell:
                    # Use entire purchase
                    sale_cost_basis += purchase['total_cost']
                    remaining_to_sell -= purchase['amount']
                    purchase_queue[asset].pop(0)
                else:
                    # Use partial purchase
                    portion = remaining_to_sell / purchase['amount']
                    sale_cost_basis += purchase['total_cost'] * portion
                    purchase['amount'] -= remaining_to_sell
                    purchase['total_cost'] -= purchase['total_cost'] * portion
                    remaining_to_sell = 0
            
            # Calculate gain/loss
            gain = sale_proceeds - sale_cost_basis
            
            sales.append({
                'date': date,
                'asset': asset,
                'amount': amount,
                'proceeds': sale_proceeds,
                'cost_basis': sale_cost_basis,
                'gain_loss': gain
            })
            
            total_gain += gain
            total_proceeds += sale_proceeds
            total_cost_basis += sale_cost_basis
    
    return sales, total_gain, total_proceeds, total_cost_basis

def generate_summary_report(transactions):
    """Generate a comprehensive tax summary.
    
    Args:
        transactions (list): List of transaction dictionaries
    
    Returns:
        None
    """
    if not transactions:
        print("No transactions to summarize.")
        return
    
    print("\n" + "="*70)
    print("CRYPTO TRADING TAX SUMMARY - US TAX YEAR")
    print("="*70)
    
    # Overall statistics
    total_buys = sum(1 for tx in transactions if tx['Transaction Type'] == 'BUY')
    total_sells = sum(1 for tx in transactions if tx['Transaction Type'] == 'SELL')
    total_fees = sum(float(tx['Fee (USD)']) for tx in transactions)
    
    print(f"\nTransaction Summary:")
    print(f"  Total Buy Orders: {total_buys}")
    print(f"  Total Sell Orders: {total_sells}")
    print(f"  Total Fees Paid: ${total_fees:.2f}")
    
    # Calculate capital gains
    sales, total_gain, total_proceeds, total_cost_basis = calculate_capital_gains(transactions)
    
    print(f"\nCapital Gains/Loss Summary:")
    print(f"  Total Proceeds: ${total_proceeds:.2f}")
    print(f"  Total Cost Basis: ${total_cost_basis:.2f}")
    print(f"  Net Gain/Loss: ${total_gain:.2f}")
    
    if total_gain > 0:
        print(f"  Status: TAXABLE GAIN (you owe taxes on this)")
    else:
        print(f"  Status: CAPITAL LOSS (can offset other gains)")
    
    # Detailed sales breakdown
    if sales:
        print(f"\n" + "-"*70)
        print(f"Detailed Sales (for IRS Form 8949):")
        print("-"*70)
        
        for i, sale in enumerate(sales, 1):
            print(f"\nSale #{i} - {sale['date']}")
            print(f"  Asset: {sale['asset']}")
            print(f"  Amount Sold: {sale['amount']:.6f}")
            print(f"  Proceeds: ${sale['proceeds']:.2f}")
            print(f"  Cost Basis: ${sale['cost_basis']:.2f}")
            print(f"  Gain/Loss: ${sale['gain_loss']:.2f}")
    
    print("\n" + "="*70)
    
    # Tax filing notes
    print("\nIMPORTANT TAX FILING NOTES:")
    print("-" * 70)
    print("1. Report on IRS Form 8949 (Sales and Dispositions of Capital Assets)")
    print("2. Transfer totals to Schedule D (Capital Gains and Losses)")
    print("3. This bot uses FIFO (First In First Out) accounting method")
    print("4. Keep tax_transactions.csv for your records (7 years)")
    print("5. Consult a tax professional for personalized advice")
    print("\n6. Short-term vs Long-term:")
    print("   - Held < 1 year = Short-term (taxed as ordinary income)")
    print("   - Held > 1 year = Long-term (lower tax rate)")
    print("   Grid trading = typically all short-term gains")
    print("="*70 + "\n")

def export_form_8949_csv(transactions, year=None):
    """Export data in format ready for Form 8949.
    
    Args:
        transactions (list): List of transaction dictionaries
        year (int): Tax year (defaults to current year)
    
    Returns:
        None
    """
    if year is None:
        year = datetime.now().year
    
    sales, _, _, _ = calculate_capital_gains(transactions)
    
    if not sales:
        print("No sales to export.")
        return
    
    filename = f'../data/form_8949_data_{year}.csv'
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Headers for Form 8949
        writer.writerow([
            'Description of Property',
            'Date Acquired',
            'Date Sold',
            'Proceeds',
            'Cost Basis',
            'Gain or Loss'
        ])
        
        for sale in sales:
            writer.writerow([
                f"{sale['amount']:.6f} {sale['asset']}",
                'Various (FIFO)',
                sale['date'],
                f"${sale['proceeds']:.2f}",
                f"${sale['cost_basis']:.2f}",
                f"${sale['gain_loss']:.2f}"
            ])
    
    print(f"\n✅ Form 8949 data exported to: {filename}")
    print("You can import this into tax software or give to your accountant.\n")

def generate_year_end_report(year=None):
    """Generate complete year-end tax report.
    
    Args:
        year (int): Tax year (defaults to current year)
    
    Returns:
        None
    """
    if year is None:
        year = datetime.now().year
    
    print(f"\nGenerating tax report for year {year}...")
    
    transactions = load_transactions()
    
    if not transactions:
        return
    
    # Filter transactions by year
    year_transactions = [
        tx for tx in transactions 
        if datetime.strptime(tx['Date/Time'], '%Y-%m-%d %H:%M:%S').year == year
    ]
    
    if not year_transactions:
        print(f"No transactions found for year {year}")
        return
    
    # Generate reports
    generate_summary_report(year_transactions)
    export_form_8949_csv(year_transactions, year)

if __name__ == "__main__":
    import sys
    
    print("="*70)
    print("CRYPTO GRID BOT - TAX SUMMARY GENERATOR")
    print("="*70)
    
    # Check if year specified
    if len(sys.argv) > 1:
        try:
            year = int(sys.argv[1])
            generate_year_end_report(year)
        except ValueError:
            print("Invalid year. Usage: python tax_summary.py [year]")
    else:
        # Default to current year
        generate_year_end_report()
    
    print("\n💡 TIP: Run this script regularly to track your gains/losses")
    print("💡 Usage: python tax_summary.py [year]")
    print("   Example: python tax_summary.py 2025\n")

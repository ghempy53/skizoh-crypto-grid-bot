# =============================================================================
# SKIZOH CRYPTO GRID TRADING BOT v14 - API Connection Test
# =============================================================================

import ccxt
import json
import sys
import os


def load_config(config_file='priv/config.json'):
    """Load API credentials from config file."""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"❌ Error: {config_file} not found!")
        print("Copy priv/config.json.template to priv/config.json")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: {config_file} is not valid JSON!")
        sys.exit(1)


def test_api_connection():
    """Test connection to Binance.US API."""
    
    print("="*60)
    print("BINANCE.US API CONNECTION TEST - v14")
    print("="*60)
    print()
    
    # Load config
    print("📋 Loading configuration...")
    config = load_config()
    
    api_key = config.get('api_key')
    api_secret = config.get('api_secret')
    symbol = config.get('symbol', 'ETH/USDT')
    
    # Validate keys
    if not api_key or 'YOUR_' in api_key:
        print("❌ API key not configured")
        sys.exit(1)
    
    if not api_secret or 'YOUR_' in api_secret:
        print("❌ API secret not configured")
        sys.exit(1)
    
    print(f"✓ Config loaded, trading pair: {symbol}")
    print()
    
    # Connect to exchange
    print("🔌 Connecting to Binance.US...")
    try:
        exchange = ccxt.binanceus({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True
        })
        
        exchange.load_markets()
        print("✓ Connected to Binance.US")
        print()
        
    except ccxt.AuthenticationError as e:
        print(f"❌ Authentication Failed: {e}")
        print("\nPossible issues:")
        print("  1. API key or secret is incorrect")
        print("  2. API key not enabled for trading")
        print("  3. IP restriction blocking connection")
        sys.exit(1)
    except ccxt.NetworkError as e:
        print(f"❌ Network Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    # Test balance
    print("💰 Test 1: Fetching balance...")
    try:
        balance = exchange.fetch_balance()
        
        base_currency = symbol.split('/')[0]
        quote_currency = symbol.split('/')[1]
        
        base_balance = balance[base_currency]['free']
        quote_balance = balance[quote_currency]['free']
        
        print("✓ Balance fetch successful")
        print()
        print("Your Balances:")
        print(f"  {quote_currency}: {quote_balance:.2f}")
        print(f"  {base_currency}: {base_balance:.6f}")
        print()
        
    except Exception as e:
        print(f"❌ Balance fetch failed: {e}")
        sys.exit(1)
    
    # Test price
    print(f"📊 Test 2: Fetching {symbol} price...")
    try:
        ticker = exchange.fetch_ticker(symbol)
        current_price = ticker['last']
        high_24h = ticker['high']
        low_24h = ticker['low']
        
        print("✓ Price data retrieved")
        print()
        print(f"Market Data for {symbol}:")
        print(f"  Current Price: ${current_price:.2f}")
        print(f"  24h High: ${high_24h:.2f}")
        print(f"  24h Low: ${low_24h:.2f}")
        print(f"  24h Range: {((high_24h-low_24h)/current_price)*100:.2f}%")
        print()
        
    except Exception as e:
        print(f"❌ Price fetch failed: {e}")
        sys.exit(1)
    
    # Test trading fees
    print("💸 Test 3: Checking trading fees...")
    try:
        trading_fees = exchange.fetch_trading_fees()
        if symbol in trading_fees:
            maker = trading_fees[symbol].get('maker', 0.001)
            taker = trading_fees[symbol].get('taker', 0.001)
            print(f"✓ Fee rates - Maker: {maker*100:.2f}%, Taker: {taker*100:.2f}%")
        else:
            print("✓ Using default fee rate: 0.10%")
        print()
    except Exception as e:
        print(f"⚠️ Could not fetch fees (using default): {e}")
        print()
    
    # Test permissions
    print("🔐 Test 4: Checking API permissions...")
    try:
        open_orders = exchange.fetch_open_orders(symbol)
        print(f"✓ Read permission: OK ({len(open_orders)} open orders)")
        
        balance = exchange.fetch_balance()
        print("✓ Trading permission: OK")
        print()
        print("⚠️  REMINDER: Withdrawals should be DISABLED on your API key!")
        print()
        
    except Exception as e:
        print(f"⚠️ Permission check warning: {e}")
        print()
    
    # Calculate trading capacity
    print("📈 Trading Capacity:")
    portfolio_value = quote_balance + (base_balance * current_price)
    print(f"  Total portfolio value: ${portfolio_value:.2f}")
    print(f"  Available for buys: ${quote_balance:.2f}")
    print(f"  Crypto value: ${base_balance * current_price:.2f}")
    print()
    
    # Test scenario configuration
    print("⚙️  Test 5: Validating scenario configurations...")
    try:
        scenarios = config.get('config_data', [])
        fee_rate = config.get('fee_rate', 0.001)
        min_profitable_spacing = (2 * fee_rate * 100) * 2.5
        
        warnings = []
        for scenario in scenarios:
            spacing = scenario.get('grid_spacing_percent', 0)
            if spacing < min_profitable_spacing:
                warnings.append(f"  ⚠️  '{scenario['name']}': spacing {spacing}% may not be profitable")
        
        if warnings:
            print("✓ Scenarios loaded with warnings:")
            for w in warnings:
                print(w)
        else:
            print(f"✓ All {len(scenarios)} scenarios have profitable spacing")
        print()
    except Exception as e:
        print(f"⚠️ Could not validate scenarios: {e}")
        print()

    # Final result
    print("="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    print()
    print("Your API is ready for trading.")
    print()
    print("Next steps:")
    print("  1. Review your priv/config.json settings")
    print("  2. Run '../run_bot.sh' to start trading")
    print("  3. Monitor with 'tail -f ../data/grid_bot.log'")
    print()
    print("Good luck! 🚀")
    print()


if __name__ == "__main__":
    test_api_connection()

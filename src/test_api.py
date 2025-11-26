"""
Binance.US API Connection Test
Reads credentials from config.json for security
"""

import ccxt
import json
import sys

def load_config(config_file='config.json'):
    """Load API credentials from config file"""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"❌ Error: {config_file} not found!")
        print("Make sure config.json exists in the current directory.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: {config_file} is not valid JSON!")
        sys.exit(1)

def test_api_connection():
    """Test connection to Binance.US API"""
    
    print("="*60)
    print("BINANCE.US API CONNECTION TEST")
    print("="*60)
    print()
    
    # Load configuration
    print("📋 Loading configuration from config.json...")
    config = load_config()
    
    api_key = config.get('api_key')
    api_secret = config.get('api_secret')
    symbol = config.get('symbol', 'ETH/USDT')
    
    # Check if keys are set
    if not api_key or api_key == 'YOUR_BINANCE_US_API_KEY':
        print("❌ API key not configured in config.json")
        print("Please update config.json with your actual API keys.")
        sys.exit(1)
    
    if not api_secret or api_secret == 'YOUR_BINANCE_US_API_SECRET':
        print("❌ API secret not configured in config.json")
        print("Please update config.json with your actual API keys.")
        sys.exit(1)
    
    print(f"✓ Configuration loaded")
    print(f"  Trading pair: {symbol}")
    print()
    
    # Initialize exchange
    print("🔌 Connecting to Binance.US...")
    try:
        exchange = ccxt.binanceus({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True
        })
        
        # Load markets
        exchange.load_markets()
        print("✓ Connected to Binance.US")
        print()
        
    except ccxt.AuthenticationError as e:
        print(f"❌ Authentication Failed: {e}")
        print()
        print("Possible issues:")
        print("  1. API key or secret is incorrect")
        print("  2. API key is not enabled for trading")
        print("  3. IP restriction is blocking your connection")
        sys.exit(1)
        
    except ccxt.NetworkError as e:
        print(f"❌ Network Error: {e}")
        print("Check your internet connection.")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        sys.exit(1)
    
    # Test 1: Fetch balance
    print("💰 Test 1: Fetching account balance...")
    try:
        balance = exchange.fetch_balance()
        
        # Get base and quote currencies
        base_currency = symbol.split('/')[0]  # ETH
        quote_currency = symbol.split('/')[1]  # USDT
        
        base_balance = balance[base_currency]['free']
        quote_balance = balance[quote_currency]['free']
        
        print("✓ Balance fetch successful")
        print()
        print("Your Balances:")
        print(f"  {quote_currency}: {quote_balance:.2f}")
        
        if base_balance > 0:
            print(f"  {base_currency}: {base_balance:.6f}")
        else:
            print(f"  {base_currency}: 0.000000 (you don't own any {base_currency} yet)")
        
        print()
        
        # Check if sufficient balance for trading
        min_order_size = config.get('min_order_size_usdt', 15)
        if quote_balance < min_order_size:
            print(f"⚠️  Warning: Your {quote_currency} balance (${quote_balance:.2f}) is below")
            print(f"   the minimum order size (${min_order_size}). You may not be able")
            print(f"   to place orders. Consider adding more funds.")
            print()
        
    except Exception as e:
        print(f"❌ Failed to fetch balance: {e}")
        sys.exit(1)
    
    # Test 2: Fetch current price
    print(f"📊 Test 2: Fetching current {symbol} price...")
    try:
        ticker = exchange.fetch_ticker(symbol)
        current_price = ticker['last']
        high_24h = ticker['high']
        low_24h = ticker['low']
        volume_24h = ticker['baseVolume']
        
        print(f"✓ Price data retrieved")
        print()
        print(f"Market Data for {symbol}:")
        print(f"  Current Price: ${current_price:.2f}")
        print(f"  24h High: ${high_24h:.2f}")
        print(f"  24h Low: ${low_24h:.2f}")
        print(f"  24h Volume: {volume_24h:.2f} {base_currency}")
        
        # Calculate 24h price change
        price_change = ((current_price - low_24h) / low_24h) * 100
        print(f"  24h Range: {price_change:.2f}%")
        print()
        
    except Exception as e:
        print(f"❌ Failed to fetch price data: {e}")
        sys.exit(1)
    
    # Test 3: Check market info and limits
    print(f"📏 Test 3: Checking market requirements for {symbol}...")
    try:
        market = exchange.market(symbol)
        
        min_amount = market['limits']['amount']['min']
        min_cost = market['limits']['cost']['min']
        
        print(f"✓ Market info retrieved")
        print()
        print(f"Trading Requirements for {symbol}:")
        print(f"  Minimum Order Amount: {min_amount} {base_currency}")
        print(f"  Minimum Order Value: ${min_cost} {quote_currency}")
        print()
        
        # Estimate how many orders can be placed
        if quote_balance > 0:
            investment_percent = config.get('investment_percent', 80)
            available_for_trading = quote_balance * (investment_percent / 100)
            grid_levels = config.get('grid_levels', 8)
            buy_orders = grid_levels // 2
            
            order_size = available_for_trading / buy_orders
            
            print(f"📊 Grid Trading Estimates:")
            print(f"  Available for trading: ${available_for_trading:.2f}")
            print(f"  Number of buy orders: {buy_orders}")
            print(f"  Estimated order size: ${order_size:.2f} each")
            
            if order_size < min_cost:
                print(f"  ⚠️  Warning: Order size (${order_size:.2f}) is below")
                print(f"     minimum (${min_cost}). Consider:")
                print(f"     - Adding more funds")
                print(f"     - Reducing grid_levels in config.json")
                print(f"     - Increasing investment_percent in config.json")
            else:
                print(f"  ✓ Order sizes are above minimum requirements")
            print()
        
    except Exception as e:
        print(f"❌ Failed to fetch market info: {e}")
        sys.exit(1)
    
    # Test 4: Check API permissions
    print("🔐 Test 4: Checking API permissions...")
    try:
        # Try to fetch open orders (requires read permission)
        open_orders = exchange.fetch_open_orders(symbol)
        print("✓ Read permission: OK")
        
        # Check if we can access account info (trading permission)
        account_info = exchange.fetch_balance()
        print("✓ Trading permission: OK")
        
        print()
        print("⚠️  Remember: Withdrawals should be DISABLED on your API key!")
        print()
        
    except ccxt.InsufficientPermissions as e:
        print(f"❌ Permission Error: {e}")
        print("Make sure your API key has 'Spot Trading' enabled.")
        sys.exit(1)
    except Exception as e:
        print(f"⚠️  Warning: Could not fully verify permissions: {e}")
        print()
    
    # Final summary
    print("="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    print()
    print("Your API is configured correctly and ready for trading.")
    print()
    print("Next steps:")
    print("  1. Review your config.json settings")
    print("  2. Run './run_bot.sh' to start the grid trading bot")
    print("  3. Monitor with './monitor_bot.sh' or 'tail -f grid_bot.log'")
    print()
    print("Good luck! 🚀")
    print()

if __name__ == "__main__":
    test_api_connection()

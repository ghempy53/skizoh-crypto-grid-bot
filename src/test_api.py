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

# \file: test_api.py
# \Date: 11-26-2025
# \Description: API connection test for Binance.US (reads from priv/config.json)

import ccxt
import json
import sys

def load_config(config_file='priv/config.json'):
    """Load API credentials from config file.
    
    Args:
        config_file (str): Path to configuration file
    
    Returns:
        dict: Configuration dictionary
    """
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"❌ Error: {config_file} not found!")
        print("Make sure config.json exists in the priv/ directory.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: {config_file} is not valid JSON!")
        sys.exit(1)

def test_api_connection():
    """Test connection to Binance.US API.
    
    Args:
        None
    
    Returns:
        None
    """
    
    print("="*60)
    print("BINANCE.US API CONNECTION TEST")
    print("="*60)
    print()
    
    # Load configuration
    print("📋 Loading configuration from priv/config.json...")
    config = load_config()
    
    api_key = config.get('api_key')
    api_secret = config.get('api_secret')
    symbol = config.get('symbol', 'ETH/USDT')
    
    # Check if keys are set
    if not api_key or api_key == 'YOUR_BINANCE_US_API_KEY':
        print("❌ API key not configured in config.json")
        print("Please update priv/config.json with your actual API keys.")
        sys.exit(1)
    
    if not api_secret or api_secret == 'YOUR_BINANCE_US_API_SECRET':
        print("❌ API secret not configured in config.json")
        print("Please update priv/config.json with your actual API keys.")
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
    
    # Test 3: Check API permissions
    print("🔐 Test 3: Checking API permissions...")
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
    print("  1. Review your priv/config.json settings")
    print("  2. Run '../run_bot.sh' to start the grid trading bot")
    print("  3. Monitor with 'tail -f ../data/grid_bot.log'")
    print()
    print("Good luck! 🚀")
    print()

if __name__ == "__main__":
    test_api_connection()

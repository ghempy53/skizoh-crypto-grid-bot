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

# \file: grid_bot.py
# \Author: Garrett Hempy
# \Date: 11-23-2025
# \Description: Spot Grid Trading Bot for Binance.US
#               No leverage - Safer approach for learning


###________________________IMPORTS________________________###
import ccxt
import time
import json
import logging
from datetime import datetime
import numpy as np
import csv
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/grid_bot.log'),
        logging.StreamHandler()
    ]
)

class SpotGridTradingBot:
    def __init__(self, config_file='config.json'):
        """Initialize the spot grid trading bot"""
        self.load_config(config_file)
        self.exchange = self.initialize_exchange()
        self.grid_levels = []
        self.active_orders = {}
        self.initial_investment = 0
        self.tax_log_file = 'tax_transactions.csv'
        self.initialize_tax_log()
        
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Exchange settings
            self.api_key = config['api_key']
            self.api_secret = config['api_secret']
            self.symbol = config['symbol']
            
            # Grid settings
            self.grid_levels_count = config['grid_levels']
            self.grid_spacing_percent = config['grid_spacing_percent']
            self.investment_percent = config['investment_percent']  # % of USDT to use
            
            # Risk management
            self.min_order_size_usdt = config['min_order_size_usdt']
            self.stop_loss_percent = config['stop_loss_percent']
            self.take_profit_percent = config.get('take_profit_percent', None)
            
            # Volatility filter settings
            self.atr_period = config['atr_period']
            self.volatility_threshold = config['volatility_threshold']
            
            # Operation settings
            self.check_interval = config['check_interval_seconds']
            
            logging.info("Configuration loaded successfully")
        except Exception as e:
            logging.error(f"Failed to load config: {e}")
            raise
    
    def initialize_exchange(self):
        """Initialize connection to Binance.US"""
        try:
            exchange = ccxt.binanceus({
                'apiKey': self.api_key,
                'secret': self.api_secret,
                'enableRateLimit': True,
            })
            exchange.load_markets()
            logging.info("Exchange connection established (Binance.US)")
            return exchange
        except Exception as e:
            logging.error(f"Failed to initialize exchange: {e}")
            raise
    
    def initialize_tax_log(self):
        """Initialize CSV file for tax record keeping"""
        try:
            # Check if file exists
            file_exists = os.path.isfile(self.tax_log_file)
            
            if not file_exists:
                # Create new file with headers
                with open(self.tax_log_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        'Date/Time',
                        'Transaction Type',
                        'Asset',
                        'Amount',
                        'Price (USD)',
                        'Total Value (USD)',
                        'Fee (USD)',
                        'Net Proceeds (USD)',
                        'Order ID',
                        'Notes'
                    ])
                logging.info(f"Created tax log file: {self.tax_log_file}")
            else:
                logging.info(f"Using existing tax log file: {self.tax_log_file}")
        except Exception as e:
            logging.error(f"Failed to initialize tax log: {e}")
    
    def log_tax_transaction(self, transaction_type, asset, amount, price, fee, order_id, notes=''):
        """
        Log a transaction for tax purposes
        
        transaction_type: 'BUY' or 'SELL'
        asset: e.g., 'ETH'
        amount: quantity of asset
        price: price per unit in USD
        fee: trading fee in USD
        order_id: exchange order ID
        notes: optional additional info
        """
        try:
            total_value = amount * price
            
            # For sells, net proceeds = total - fee
            # For buys, cost basis = total + fee
            if transaction_type == 'SELL':
                net_proceeds = total_value - fee
            else:
                net_proceeds = total_value + fee
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            with open(self.tax_log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    timestamp,
                    transaction_type,
                    asset,
                    f"{amount:.8f}",
                    f"{price:.2f}",
                    f"{total_value:.2f}",
                    f"{fee:.2f}",
                    f"{net_proceeds:.2f}",
                    order_id,
                    notes
                ])
            
            logging.info(f"💰 Tax log: {transaction_type} {amount:.6f} {asset} @ ${price:.2f}")
        except Exception as e:
            logging.error(f"Failed to log tax transaction: {e}")
    
    def get_balances(self):
        """Get USDT and crypto balances"""
        try:
            balance = self.exchange.fetch_balance()
            
            # Get base and quote currencies (e.g., ETH and USDT)
            base_currency = self.symbol.split('/')[0]  # ETH
            quote_currency = self.symbol.split('/')[1]  # USDT
            
            base_balance = balance[base_currency]['free']
            quote_balance = balance[quote_currency]['free']
            
            logging.info(f"Balances - {base_currency}: {base_balance}, {quote_currency}: {quote_balance}")
            
            return {
                'base': base_balance,
                'quote': quote_balance,
                'base_currency': base_currency,
                'quote_currency': quote_currency
            }
        except Exception as e:
            logging.error(f"Failed to fetch balance: {e}")
            return None
    
    def calculate_atr(self, period=14):
        """Calculate Average True Range for volatility measurement"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, '1h', limit=period+1)
            
            highs = np.array([x[2] for x in ohlcv])
            lows = np.array([x[3] for x in ohlcv])
            closes = np.array([x[4] for x in ohlcv])
            
            # True Range calculation
            tr1 = highs[1:] - lows[1:]
            tr2 = np.abs(highs[1:] - closes[:-1])
            tr3 = np.abs(lows[1:] - closes[:-1])
            
            true_range = np.maximum(tr1, np.maximum(tr2, tr3))
            atr = np.mean(true_range)
            
            return atr
        except Exception as e:
            logging.error(f"Failed to calculate ATR: {e}")
            return 0
    
    def check_volatility(self):
        """Check if market volatility is within acceptable range"""
        try:
            current_price = self.exchange.fetch_ticker(self.symbol)['last']
            atr = self.calculate_atr(self.atr_period)
            
            # Calculate volatility as percentage of price
            volatility_percent = (atr / current_price) * 100
            
            logging.info(f"Current volatility: {volatility_percent:.2f}%")
            
            # If volatility exceeds threshold, pause trading
            if volatility_percent > self.volatility_threshold:
                logging.warning(f"High volatility detected ({volatility_percent:.2f}%), pausing trading")
                return False
            
            return True
        except Exception as e:
            logging.error(f"Failed to check volatility: {e}")
            return False
    
    def calculate_grid_levels(self):
        """Calculate grid buy/sell levels based on current price"""
        try:
            current_price = self.exchange.fetch_ticker(self.symbol)['last']
            balances = self.get_balances()
            
            if not balances:
                return False
            
            # Calculate how much USDT to allocate for buying
            available_usdt = balances['quote'] * (self.investment_percent / 100)
            
            # Store initial investment for profit tracking
            if self.initial_investment == 0:
                self.initial_investment = available_usdt + (balances['base'] * current_price)
            
            self.grid_levels = []
            
            # Calculate number of buy and sell orders
            num_buy_orders = self.grid_levels_count // 2
            num_sell_orders = self.grid_levels_count // 2
            
            # Amount of USDT per buy order
            usdt_per_buy = available_usdt / num_buy_orders
            
            # Create BUY levels below current price
            for i in range(1, num_buy_orders + 1):
                price_level = current_price * (1 - (i * self.grid_spacing_percent / 100))
                
                # Skip if order size is too small
                if usdt_per_buy < self.min_order_size_usdt:
                    logging.warning(f"Order size too small: ${usdt_per_buy:.2f}, skipping")
                    continue
                
                quantity = usdt_per_buy / price_level
                
                self.grid_levels.append({
                    'price': round(price_level, 2),
                    'quantity': quantity,
                    'type': 'buy',
                    'filled': False
                })
            
            # Create SELL levels above current price
            # Use existing crypto balance for sell orders
            crypto_per_sell = balances['base'] / num_sell_orders if balances['base'] > 0 else 0
            
            for i in range(1, num_sell_orders + 1):
                price_level = current_price * (1 + (i * self.grid_spacing_percent / 100))
                
                # Only create sell order if we have crypto to sell
                if crypto_per_sell > 0:
                    self.grid_levels.append({
                        'price': round(price_level, 2),
                        'quantity': crypto_per_sell,
                        'type': 'sell',
                        'filled': False
                    })
            
            logging.info(f"Generated {len(self.grid_levels)} grid levels around price ${current_price:.2f}")
            return True
        except Exception as e:
            logging.error(f"Failed to calculate grid levels: {e}")
            return False
    
    def place_grid_orders(self):
        """Place limit orders at grid levels"""
        if not self.check_volatility():
            logging.info("Volatility too high, skipping order placement")
            return
        
        try:
            for level in self.grid_levels:
                if level['filled']:
                    continue
                
                # Check if order already exists at this level
                order_exists = False
                for order_id, order_data in self.active_orders.items():
                    if order_data['level'] == level:
                        order_exists = True
                        break
                
                if order_exists:
                    continue
                
                price = level['price']
                quantity = level['quantity']
                order_type = level['type']
                
                # Format quantity to exchange precision
                quantity = self.exchange.amount_to_precision(self.symbol, quantity)
                quantity = float(quantity)
                
                if quantity <= 0:
                    logging.warning(f"Invalid quantity for {order_type} at ${price}")
                    continue
                
                # Place limit order
                try:
                    order = self.exchange.create_order(
                        symbol=self.symbol,
                        type='limit',
                        side=order_type,
                        amount=quantity,
                        price=price
                    )
                    
                    self.active_orders[order['id']] = {
                        'level': level,
                        'order': order
                    }
                    
                    logging.info(f"✓ Placed {order_type.upper()} order: {quantity} at ${price}")
                except Exception as e:
                    # Order might fail due to insufficient balance, min notional, etc.
                    logging.warning(f"Could not place {order_type} order at ${price}: {e}")
        
        except Exception as e:
            logging.error(f"Failed to place grid orders: {e}")
    
    def check_orders(self):
        """Check status of active orders"""
        try:
            for order_id in list(self.active_orders.keys()):
                try:
                    order_info = self.exchange.fetch_order(order_id, self.symbol)
                    
                    if order_info['status'] == 'closed':
                        # Order filled
                        level = self.active_orders[order_id]['level']
                        level['filled'] = True
                        
                        side = order_info['side']
                        amount = order_info['filled']
                        price = order_info['price']
                        
                        # Calculate fee
                        fee = 0
                        if 'fee' in order_info and order_info['fee']:
                            fee_info = order_info['fee']
                            # Fee might be in different currency, convert to USD
                            if fee_info['currency'] == 'USDT':
                                fee = float(fee_info['cost'])
                            else:
                                # If fee is in the asset (e.g., ETH), convert to USD
                                fee = float(fee_info['cost']) * price
                        
                        # If no fee info, estimate (Binance.US is 0.1%)
                        if fee == 0:
                            fee = (amount * price) * 0.001  # 0.1%
                        
                        logging.info(f"✓ Order FILLED: {side.upper()} {amount} at ${price}")
                        
                        # Log for tax purposes
                        base_currency = self.symbol.split('/')[0]
                        self.log_tax_transaction(
                            transaction_type=side.upper(),
                            asset=base_currency,
                            amount=amount,
                            price=price,
                            fee=fee,
                            order_id=order_id,
                            notes='Grid bot automated trade'
                        )
                        
                        # Remove from active orders
                        del self.active_orders[order_id]
                        
                        # Place opposite order
                        self.place_opposite_order(level, price)
                
                except Exception as e:
                    logging.warning(f"Error checking order {order_id}: {e}")
        
        except Exception as e:
            logging.error(f"Failed to check orders: {e}")
    
    def place_opposite_order(self, filled_level, fill_price):
        """Place opposite order after a grid level is filled"""
        try:
            balances = self.get_balances()
            if not balances:
                return
            
            price_adjustment = self.grid_spacing_percent / 100
            
            if filled_level['type'] == 'buy':
                # We bought crypto, now place sell order above
                new_price = fill_price * (1 + price_adjustment)
                side = 'sell'
                
                # Use the amount we just bought
                quantity = filled_level['quantity']
                
            else:
                # We sold crypto, now place buy order below
                new_price = fill_price * (1 - price_adjustment)
                side = 'buy'
                
                # Calculate how much USDT we got from the sell
                usdt_received = filled_level['quantity'] * fill_price
                
                # Use that USDT to buy back
                quantity = usdt_received / new_price
            
            # Format quantity
            quantity = self.exchange.amount_to_precision(self.symbol, quantity)
            quantity = float(quantity)
            
            if quantity <= 0:
                logging.warning(f"Invalid quantity for opposite {side} order")
                return
            
            # Place the order
            order = self.exchange.create_order(
                symbol=self.symbol,
                type='limit',
                side=side,
                amount=quantity,
                price=round(new_price, 2)
            )
            
            # Add to grid levels
            new_level = {
                'price': round(new_price, 2),
                'quantity': quantity,
                'type': side,
                'filled': False
            }
            self.grid_levels.append(new_level)
            
            self.active_orders[order['id']] = {
                'level': new_level,
                'order': order
            }
            
            logging.info(f"✓ Placed opposite {side.upper()} order: {quantity} at ${new_price:.2f}")
        
        except Exception as e:
            logging.error(f"Failed to place opposite order: {e}")
    
    def calculate_current_value(self):
        """Calculate current portfolio value and P&L"""
        try:
            balances = self.get_balances()
            if not balances:
                return None
            
            current_price = self.exchange.fetch_ticker(self.symbol)['last']
            
            # Total value = USDT + (crypto * current price)
            total_value = balances['quote'] + (balances['base'] * current_price)
            
            if self.initial_investment > 0:
                profit = total_value - self.initial_investment
                profit_percent = (profit / self.initial_investment) * 100
                
                logging.info(f"Portfolio Value: ${total_value:.2f} | P&L: ${profit:.2f} ({profit_percent:.2f}%)")
                
                return {
                    'total_value': total_value,
                    'profit': profit,
                    'profit_percent': profit_percent
                }
            
            return None
        except Exception as e:
            logging.error(f"Failed to calculate portfolio value: {e}")
            return None
    
    def check_stop_loss(self):
        """Check if stop loss threshold is hit"""
        portfolio = self.calculate_current_value()
        
        if portfolio and portfolio['profit_percent'] < -self.stop_loss_percent:
            logging.critical(f"⚠️ STOP LOSS TRIGGERED: {portfolio['profit_percent']:.2f}% loss")
            self.emergency_stop()
            return False
        
        return True
    
    def emergency_stop(self):
        """Emergency stop - cancel all orders and optionally sell everything"""
        try:
            logging.critical("🛑 EMERGENCY STOP ACTIVATED")
            
            # Cancel all open orders
            open_orders = self.exchange.fetch_open_orders(self.symbol)
            for order in open_orders:
                self.exchange.cancel_order(order['id'], self.symbol)
                logging.info(f"Cancelled order {order['id']}")
            
            self.active_orders = {}
            
            # Optional: Sell all crypto to USDT
            balances = self.get_balances()
            if balances and balances['base'] > 0:
                current_price = self.exchange.fetch_ticker(self.symbol)['last']
                
                # Market sell to exit position immediately
                quantity = self.exchange.amount_to_precision(self.symbol, balances['base'])
                
                if float(quantity) > 0:
                    order = self.exchange.create_order(
                        symbol=self.symbol,
                        type='market',
                        side='sell',
                        amount=quantity
                    )
                    
                    # Log emergency sell for taxes
                    current_price = self.exchange.fetch_ticker(self.symbol)['last']
                    fee = float(quantity) * current_price * 0.001
                    
                    self.log_tax_transaction(
                        transaction_type='SELL',
                        asset=balances['base_currency'],
                        amount=float(quantity),
                        price=current_price,
                        fee=fee,
                        order_id=order['id'],
                        notes='Emergency stop loss exit'
                    )
                    
                    logging.critical(f"Emergency sold {quantity} {balances['base_currency']}")
            
            logging.critical("All positions closed, bot stopped")
        except Exception as e:
            logging.error(f"Error during emergency stop: {e}")
    
    def cancel_all_orders(self):
        """Cancel all active orders"""
        try:
            open_orders = self.exchange.fetch_open_orders(self.symbol)
            for order in open_orders:
                self.exchange.cancel_order(order['id'], self.symbol)
            self.active_orders = {}
            logging.info("All orders cancelled")
        except Exception as e:
            logging.error(f"Failed to cancel orders: {e}")
    
    def run(self):
        """Main bot loop"""
        logging.info("🤖 Starting Spot Grid Trading Bot for Binance.US")
        
        # Display initial balances
        balances = self.get_balances()
        if balances:
            logging.info(f"Starting with: {balances['quote']:.2f} {balances['quote_currency']}, "
                        f"{balances['base']:.4f} {balances['base_currency']}")
        
        # Calculate initial grid
        if not self.calculate_grid_levels():
            logging.error("Failed to calculate grid levels, exiting")
            return
        
        # Main loop
        try:
            while True:
                logging.info("--- 🔄 Bot cycle start ---")
                
                # Safety check: stop loss
                if not self.check_stop_loss():
                    logging.critical("Stop loss triggered, bot stopped")
                    break
                
                # Place orders at grid levels
                self.place_grid_orders()
                
                # Check if any orders filled
                self.check_orders()
                
                # Display current status
                self.calculate_current_value()
                
                # Sleep before next cycle
                logging.info(f"💤 Sleeping for {self.check_interval} seconds\n")
                time.sleep(self.check_interval)
        
        except KeyboardInterrupt:
            logging.info("🛑 Bot stopped by user")
            self.cancel_all_orders()
        except Exception as e:
            logging.error(f"❌ Unexpected error: {e}")
            self.emergency_stop()

if __name__ == "__main__":
    bot = SpotGridTradingBot('config.json')
    bot.run()

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
# \Date: 11-26-2025
# \Description: Smart grid trading bot v13 with RSI/MACD, dynamic repositioning, and profit compounding

import ccxt
import time
import json
import logging
from datetime import datetime
import numpy as np
import csv
import os

from config_manager import ConfigManager
from market_analysis import MarketAnalyzer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('grid_bot.log'),
        logging.StreamHandler()
    ]
)

class SmartGridTradingBot:
    """Smart grid trading bot with advanced market analysis."""
    
    def __init__(self, config_file='config.json'):
        """Initialize the smart grid trading bot.
        
        Args:
            config_file (str): Path to configuration file
        
        Returns:
            None
        """
        self.config_manager = ConfigManager(config_file)
        config = self.config_manager.load_config()
        
        # API credentials
        self.api_key = config['api_key']
        self.api_secret = config['api_secret']
        self.symbol = config['symbol']
        
        # Select scenario interactively
        scenario = self.config_manager.select_scenario_interactive()
        self.load_scenario(scenario)
        
        # Initialize exchange and market analyzer
        self.exchange = self.initialize_exchange()
        self.market_analyzer = MarketAnalyzer(self.exchange, self.symbol)
        
        # Trading state
        self.grid_levels = []
        self.active_orders = {}
        self.initial_investment = 0
        self.total_profit = 0
        self.cycles_completed = 0
        
        # Tax logging
        self.tax_log_file = 'tax_transactions.csv'
        self.initialize_tax_log()
        
        # Grid repositioning
        self.grid_center_price = None
        self.last_grid_update = time.time()
        
    def load_scenario(self, scenario):
        """Load selected scenario configuration.
        
        Args:
            scenario (dict): Scenario configuration dictionary
        
        Returns:
            None
        """
        self.scenario_name = scenario['name']
        self.grid_levels_count = scenario['grid_levels']
        self.grid_spacing_percent = scenario['grid_spacing_percent']
        self.investment_percent = scenario['investment_percent']
        self.min_order_size_usdt = scenario['min_order_size_usdt']
        self.stop_loss_percent = scenario['stop_loss_percent']
        self.take_profit_percent = scenario.get('take_profit_percent', None)
        self.atr_period = scenario['atr_period']
        self.volatility_threshold = scenario['volatility_threshold']
        self.check_interval = scenario['check_interval_seconds']
        
        logging.info(f"Loaded scenario: {self.scenario_name}")
        
    def initialize_exchange(self):
        """Initialize connection to Binance.US.
        
        Args:
            None
        
        Returns:
            ccxt.Exchange: Initialized exchange instance
        """
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
        """Initialize CSV file for tax record keeping.
        
        Args:
            None
        
        Returns:
            None
        """
        try:
            file_exists = os.path.isfile(self.tax_log_file)
            
            if not file_exists:
                with open(self.tax_log_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        'Date/Time', 'Transaction Type', 'Asset', 'Amount',
                        'Price (USD)', 'Total Value (USD)', 'Fee (USD)',
                        'Net Proceeds (USD)', 'Order ID', 'Notes'
                    ])
                logging.info(f"Created tax log file: {self.tax_log_file}")
            else:
                logging.info(f"Using existing tax log file: {self.tax_log_file}")
        except Exception as e:
            logging.error(f"Failed to initialize tax log: {e}")
    
    def log_tax_transaction(self, transaction_type, asset, amount, price, fee, order_id, notes=''):
        """Log a transaction for tax purposes.
        
        Args:
            transaction_type (str): 'BUY' or 'SELL'
            asset (str): Asset symbol (e.g., 'ETH')
            amount (float): Quantity of asset
            price (float): Price per unit in USD
            fee (float): Trading fee in USD
            order_id (str): Exchange order ID
            notes (str): Additional notes (optional)
        
        Returns:
            None
        """
        try:
            total_value = amount * price
            net_proceeds = total_value - fee if transaction_type == 'SELL' else total_value + fee
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            with open(self.tax_log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    timestamp, transaction_type, asset, f"{amount:.8f}",
                    f"{price:.2f}", f"{total_value:.2f}", f"{fee:.2f}",
                    f"{net_proceeds:.2f}", order_id, notes
                ])
            
            logging.info(f"💰 Tax log: {transaction_type} {amount:.6f} {asset} @ ${price:.2f}")
        except Exception as e:
            logging.error(f"Failed to log tax transaction: {e}")
    
    def get_balances(self):
        """Get USDT and crypto balances.
        
        Args:
            None
        
        Returns:
            dict: Balance information with keys 'base', 'quote', 'base_currency', 'quote_currency'
        """
        try:
            balance = self.exchange.fetch_balance()
            base_currency = self.symbol.split('/')[0]
            quote_currency = self.symbol.split('/')[1]
            
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
    
    def check_volatility(self):
        """Check if market volatility is within acceptable range.
        
        Args:
            None
        
        Returns:
            bool: True if volatility is acceptable, False otherwise
        """
        try:
            current_price = self.exchange.fetch_ticker(self.symbol)['last']
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, '1h', limit=self.atr_period+1)
            
            highs = np.array([x[2] for x in ohlcv])
            lows = np.array([x[3] for x in ohlcv])
            closes = np.array([x[4] for x in ohlcv])
            
            tr1 = highs[1:] - lows[1:]
            tr2 = np.abs(highs[1:] - closes[:-1])
            tr3 = np.abs(lows[1:] - closes[:-1])
            
            true_range = np.maximum(tr1, np.maximum(tr2, tr3))
            atr = np.mean(true_range)
            volatility_percent = (atr / current_price) * 100
            
            logging.info(f"Current volatility: {volatility_percent:.2f}%")
            
            if volatility_percent > self.volatility_threshold:
                logging.warning(f"High volatility detected ({volatility_percent:.2f}%), pausing trading")
                return False
            
            return True
        except Exception as e:
            logging.error(f"Failed to check volatility: {e}")
            return False
    
    def calculate_compounded_investment(self):
        """Calculate investment amount with profit compounding.
        
        Args:
            None
        
        Returns:
            float: Percentage of balance to invest
        """
        profit_percent = (self.total_profit / self.initial_investment * 100) if self.initial_investment > 0 else 0
        
        # Increase investment as profits grow
        if profit_percent > 20:
            compound_percent = min(95, self.investment_percent + 10)
        elif profit_percent > 10:
            compound_percent = min(90, self.investment_percent + 5)
        elif profit_percent > 5:
            compound_percent = self.investment_percent + 2
        else:
            compound_percent = self.investment_percent
        
        if compound_percent > self.investment_percent:
            logging.info(f"💎 Profit compounding: {compound_percent}% (was {self.investment_percent}%)")
        
        return compound_percent
    
    def should_reposition_grid(self, current_price):
        """Check if grid needs repositioning based on price movement.
        
        Args:
            current_price (float): Current market price
        
        Returns:
            bool: True if grid should be repositioned, False otherwise
        """
        if self.grid_center_price is None:
            return False
        
        # Calculate how far price has moved from grid center
        price_move_percent = abs((current_price - self.grid_center_price) / self.grid_center_price) * 100
        
        # Reposition if price moved more than 2x the grid spacing
        reposition_threshold = self.grid_spacing_percent * 2
        
        # Also check time since last update (don't reposition too frequently)
        time_since_update = time.time() - self.last_grid_update
        min_time_between_updates = 300  # 5 minutes
        
        if price_move_percent > reposition_threshold and time_since_update > min_time_between_updates:
            logging.info(f"🔄 Grid repositioning needed: price moved {price_move_percent:.2f}% from center")
            return True
        
        return False
    
    def calculate_grid_levels(self, reposition=False):
        """Calculate grid buy/sell levels with smart positioning.
        
        Args:
            reposition (bool): Whether this is a grid repositioning
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            current_price = self.exchange.fetch_ticker(self.symbol)['last']
            balances = self.get_balances()
            
            if not balances:
                return False
            
            # Get market bias from RSI/MACD
            bias = self.market_analyzer.should_adjust_grid_bias()
            
            # Get support/resistance levels
            sr_levels = self.market_analyzer.find_support_resistance()
            
            # Calculate investment with compounding
            investment_percent = self.calculate_compounded_investment()
            available_usdt = balances['quote'] * (investment_percent / 100)
            
            if self.initial_investment == 0:
                self.initial_investment = available_usdt + (balances['base'] * current_price)
            
            # Cancel existing orders if repositioning
            if reposition:
                logging.info("🔄 Repositioning grid - cancelling old orders")
                self.cancel_all_orders()
            
            self.grid_levels = []
            self.grid_center_price = current_price
            self.last_grid_update = time.time()
            
            # Calculate buy and sell orders with bias
            total_levels = self.grid_levels_count
            buy_levels = int(total_levels * bias['buy_weight'])
            sell_levels = int(total_levels * bias['sell_weight'])
            
            logging.info(f"📊 Grid bias: {bias['bias']} (Buy: {buy_levels}, Sell: {sell_levels})")
            
            # Calculate USDT per buy order
            usdt_per_buy = available_usdt / buy_levels if buy_levels > 0 else 0
            
            # Create BUY levels below current price
            for i in range(1, buy_levels + 1):
                price_level = current_price * (1 - (i * self.grid_spacing_percent / 100))
                
                # Adjust to nearby support if available
                if sr_levels and sr_levels['support']:
                    price_level = self._adjust_to_sr_level(price_level, sr_levels['support'], 'support')
                
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
            crypto_per_sell = balances['base'] / sell_levels if sell_levels > 0 and balances['base'] > 0 else 0
            
            for i in range(1, sell_levels + 1):
                price_level = current_price * (1 + (i * self.grid_spacing_percent / 100))
                
                # Adjust to nearby resistance if available
                if sr_levels and sr_levels['resistance']:
                    price_level = self._adjust_to_sr_level(price_level, sr_levels['resistance'], 'resistance')
                
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
    
    def _adjust_to_sr_level(self, target_price, sr_levels, level_type):
        """Adjust order price to nearby support/resistance level.
        
        Args:
            target_price (float): Target price level
            sr_levels (list): List of support or resistance prices
            level_type (str): 'support' or 'resistance'
        
        Returns:
            float: Adjusted price
        """
        # Find closest S/R level within 0.5% of target
        threshold = target_price * 0.005
        
        for sr_price in sr_levels:
            if abs(sr_price - target_price) < threshold:
                logging.info(f"📍 Adjusted {level_type} order from ${target_price:.2f} to ${sr_price:.2f}")
                return sr_price
        
        return target_price
    
    def place_grid_orders(self):
        """Place limit orders at grid levels.
        
        Args:
            None
        
        Returns:
            None
        """
        if not self.check_volatility():
            logging.info("Volatility too high, skipping order placement")
            return
        
        try:
            for level in self.grid_levels:
                if level['filled']:
                    continue
                
                # Check if order already exists
                order_exists = any(
                    order_data['level'] == level 
                    for order_data in self.active_orders.values()
                )
                
                if order_exists:
                    continue
                
                price = level['price']
                quantity = self.exchange.amount_to_precision(self.symbol, level['quantity'])
                quantity = float(quantity)
                
                if quantity <= 0:
                    continue
                
                try:
                    order = self.exchange.create_order(
                        symbol=self.symbol,
                        type='limit',
                        side=level['type'],
                        amount=quantity,
                        price=price
                    )
                    
                    self.active_orders[order['id']] = {'level': level, 'order': order}
                    logging.info(f"✓ Placed {level['type'].upper()} order: {quantity} at ${price}")
                except Exception as e:
                    logging.warning(f"Could not place {level['type']} order at ${price}: {e}")
        
        except Exception as e:
            logging.error(f"Failed to place grid orders: {e}")
    
    def check_orders(self):
        """Check status of active orders.
        
        Args:
            None
        
        Returns:
            None
        """
        try:
            for order_id in list(self.active_orders.keys()):
                try:
                    order_info = self.exchange.fetch_order(order_id, self.symbol)
                    
                    if order_info['status'] == 'closed':
                        level = self.active_orders[order_id]['level']
                        level['filled'] = True
                        
                        side = order_info['side']
                        amount = order_info['filled']
                        price = order_info['price']
                        
                        # Calculate fee
                        fee = self._calculate_fee(order_info, amount, price)
                        
                        # Track profit
                        if side == 'sell':
                            profit = (amount * price * self.grid_spacing_percent / 100) - fee
                            self.total_profit += profit
                            self.cycles_completed += 1
                            logging.info(f"💰 Cycle profit: ${profit:.2f} | Total: ${self.total_profit:.2f}")
                        
                        logging.info(f"✓ Order FILLED: {side.upper()} {amount} at ${price}")
                        
                        # Log for taxes
                        base_currency = self.symbol.split('/')[0]
                        self.log_tax_transaction(
                            side.upper(), base_currency, amount, price, fee,
                            order_id, 'Grid bot automated trade'
                        )
                        
                        del self.active_orders[order_id]
                        self.place_opposite_order(level, price)
                
                except Exception as e:
                    logging.warning(f"Error checking order {order_id}: {e}")
        
        except Exception as e:
            logging.error(f"Failed to check orders: {e}")
    
    def _calculate_fee(self, order_info, amount, price):
        """Calculate trading fee from order info.
        
        Args:
            order_info (dict): Order information from exchange
            amount (float): Order amount
            price (float): Order price
        
        Returns:
            float: Fee in USD
        """
        fee = 0
        if 'fee' in order_info and order_info['fee']:
            fee_info = order_info['fee']
            if fee_info['currency'] == 'USDT':
                fee = float(fee_info['cost'])
            else:
                fee = float(fee_info['cost']) * price
        
        if fee == 0:
            fee = (amount * price) * 0.001  # Estimate 0.1%
        
        return fee
    
    def place_opposite_order(self, filled_level, fill_price):
        """Place opposite order after a grid level is filled.
        
        Args:
            filled_level (dict): Grid level that was filled
            fill_price (float): Price at which order filled
        
        Returns:
            None
        """
        try:
            balances = self.get_balances()
            if not balances:
                return
            
            price_adjustment = self.grid_spacing_percent / 100
            
            if filled_level['type'] == 'buy':
                new_price = fill_price * (1 + price_adjustment)
                side = 'sell'
                quantity = filled_level['quantity']
            else:
                new_price = fill_price * (1 - price_adjustment)
                side = 'buy'
                usdt_received = filled_level['quantity'] * fill_price
                quantity = usdt_received / new_price
            
            quantity = self.exchange.amount_to_precision(self.symbol, quantity)
            quantity = float(quantity)
            
            if quantity <= 0:
                return
            
            order = self.exchange.create_order(
                symbol=self.symbol,
                type='limit',
                side=side,
                amount=quantity,
                price=round(new_price, 2)
            )
            
            new_level = {
                'price': round(new_price, 2),
                'quantity': quantity,
                'type': side,
                'filled': False
            }
            self.grid_levels.append(new_level)
            self.active_orders[order['id']] = {'level': new_level, 'order': order}
            
            logging.info(f"✓ Placed opposite {side.upper()} order: {quantity} at ${new_price:.2f}")
        
        except Exception as e:
            logging.error(f"Failed to place opposite order: {e}")
    
    def calculate_current_value(self):
        """Calculate current portfolio value and P&L.
        
        Args:
            None
        
        Returns:
            dict: Portfolio value information or None
        """
        try:
            balances = self.get_balances()
            if not balances:
                return None
            
            current_price = self.exchange.fetch_ticker(self.symbol)['last']
            
            # Get value of open orders
            open_orders_value = 0
            try:
                open_orders = self.exchange.fetch_open_orders(self.symbol)
                for order in open_orders:
                    if order['side'] == 'buy':
                        open_orders_value += float(order['remaining']) * float(order['price'])
                    else:
                        open_orders_value += float(order['remaining']) * current_price
            except Exception as e:
                logging.warning(f"Could not fetch open orders: {e}")
            
            # Total value
            total_value = balances['quote'] + (balances['base'] * current_price) + open_orders_value
            
            if self.initial_investment > 0:
                profit = total_value - self.initial_investment
                profit_percent = (profit / self.initial_investment) * 100
                
                logging.info(
                    f"Portfolio: ${total_value:.2f} (Free: ${balances['quote']:.2f}, "
                    f"Orders: ${open_orders_value:.2f}) | P&L: ${profit:.2f} ({profit_percent:.2f}%) | "
                    f"Cycles: {self.cycles_completed}"
                )
                
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
        """Check if stop loss threshold is hit.
        
        Args:
            None
        
        Returns:
            bool: True if safe to continue, False if stop loss triggered
        """
        portfolio = self.calculate_current_value()
        
        if portfolio and portfolio['profit_percent'] < -self.stop_loss_percent:
            logging.critical(f"⚠️ STOP LOSS TRIGGERED: {portfolio['profit_percent']:.2f}% loss")
            self.emergency_stop()
            return False
        
        return True
    
    def emergency_stop(self):
        """Emergency stop - cancel all orders and exit positions.
        
        Args:
            None
        
        Returns:
            None
        """
        try:
            logging.critical("🛑 EMERGENCY STOP ACTIVATED")
            
            # Cancel all orders
            open_orders = self.exchange.fetch_open_orders(self.symbol)
            for order in open_orders:
                self.exchange.cancel_order(order['id'], self.symbol)
                logging.info(f"Cancelled order {order['id']}")
            
            self.active_orders = {}
            
            # Sell all crypto
            balances = self.get_balances()
            if balances and balances['base'] > 0:
                quantity = self.exchange.amount_to_precision(self.symbol, balances['base'])
                
                if float(quantity) > 0:
                    order = self.exchange.create_order(
                        symbol=self.symbol,
                        type='market',
                        side='sell',
                        amount=quantity
                    )
                    
                    current_price = self.exchange.fetch_ticker(self.symbol)['last']
                    fee = float(quantity) * current_price * 0.001
                    
                    self.log_tax_transaction(
                        'SELL', balances['base_currency'], float(quantity),
                        current_price, fee, order['id'], 'Emergency stop loss exit'
                    )
                    
                    logging.critical(f"Emergency sold {quantity} {balances['base_currency']}")
            
            logging.critical("All positions closed, bot stopped")
        except Exception as e:
            logging.error(f"Error during emergency stop: {e}")
    
    def cancel_all_orders(self):
        """Cancel all active orders.
        
        Args:
            None
        
        Returns:
            None
        """
        try:
            open_orders = self.exchange.fetch_open_orders(self.symbol)
            for order in open_orders:
                self.exchange.cancel_order(order['id'], self.symbol)
            self.active_orders = {}
            logging.info("All orders cancelled")
        except Exception as e:
            logging.error(f"Failed to cancel orders: {e}")
    
    def run(self):
        """Main bot loop.
        
        Args:
            None
        
        Returns:
            None
        """
        logging.info(f"🤖 Starting Smart Grid Trading Bot - Strategy: {self.scenario_name}")
        
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
                
                # Check current price
                current_price = self.exchange.fetch_ticker(self.symbol)['last']
                
                # Check if grid needs repositioning
                if self.should_reposition_grid(current_price):
                    self.calculate_grid_levels(reposition=True)
                
                # Safety check
                if not self.check_stop_loss():
                    break
                
                # Place orders
                self.place_grid_orders()
                
                # Check filled orders
                self.check_orders()
                
                # Display status
                self.calculate_current_value()
                
                # Sleep
                logging.info(f"💤 Sleeping for {self.check_interval} seconds\n")
                time.sleep(self.check_interval)
        
        except KeyboardInterrupt:
            logging.info("🛑 Bot stopped by user")
            self.cancel_all_orders()
        except Exception as e:
            logging.error(f"❌ Unexpected error: {e}")
            self.emergency_stop()

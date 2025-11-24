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
# \Description: Leveraged Crypto Grid Trading Bot with Volatility Filters
#               Designed for Raspberry Pi - Safe position management included


###________________________IMPORTS________________________###
import ccxt
import time
import json
import logging
from datetime import datetime
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('grid_bot.log'),
        logging.StreamHandler()
    ]
)

class GridTradingBot:
    def __init__(self, config_file='config.json'):
        """Initialize the grid trading bot with configuration"""
        self.load_config(config_file)
        self.exchange = self.initialize_exchange()
        self.grid_levels = []
        self.active_orders = {}
        self.positions = {}
        
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
            self.leverage = config['leverage']
            
            # Risk management
            self.max_position_percent = config['max_position_percent']  # Max % of balance per position
            self.stop_loss_percent = config['stop_loss_percent']
            self.max_total_exposure = config['max_total_exposure']  # Max total exposure as % of balance
            
            # Volatility filter settings
            self.atr_period = config['atr_period']
            self.atr_multiplier = config['atr_multiplier']
            self.volatility_threshold = config['volatility_threshold']
            
            # Operation settings
            self.check_interval = config['check_interval_seconds']
            
            logging.info("Configuration loaded successfully")
        except Exception as e:
            logging.error(f"Failed to load config: {e}")
            raise
    
    def initialize_exchange(self):
        """Initialize connection to Binance Futures"""
        try:
            exchange = ccxt.binance({
                'apiKey': self.api_key,
                'secret': self.api_secret,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'future',
                }
            })
            exchange.load_markets()
            logging.info("Exchange connection established")
            return exchange
        except Exception as e:
            logging.error(f"Failed to initialize exchange: {e}")
            raise
    
    def set_leverage(self):
        """Set leverage for the trading pair"""
        try:
            self.exchange.fapiPrivate_post_leverage({
                'symbol': self.symbol.replace('/', ''),
                'leverage': self.leverage
            })
            logging.info(f"Leverage set to {self.leverage}x for {self.symbol}")
        except Exception as e:
            logging.error(f"Failed to set leverage: {e}")
    
    def get_account_balance(self):
        """Get available balance in USDT"""
        try:
            balance = self.exchange.fetch_balance()
            available = balance['USDT']['free']
            logging.info(f"Available balance: {available} USDT")
            return available
        except Exception as e:
            logging.error(f"Failed to fetch balance: {e}")
            return 0
    
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
            
            self.grid_levels = []
            
            # Create grid levels above and below current price
            for i in range(-self.grid_levels_count // 2, self.grid_levels_count // 2 + 1):
                if i == 0:
                    continue  # Skip current price
                
                price_level = current_price * (1 + (i * self.grid_spacing_percent / 100))
                
                # Determine if this is a buy or sell level
                order_type = 'buy' if i < 0 else 'sell'
                
                self.grid_levels.append({
                    'price': round(price_level, 2),
                    'type': order_type,
                    'filled': False
                })
            
            logging.info(f"Generated {len(self.grid_levels)} grid levels around price {current_price}")
            return True
        except Exception as e:
            logging.error(f"Failed to calculate grid levels: {e}")
            return False
    
    def calculate_position_size(self, price):
        """Calculate safe position size based on risk management rules"""
        try:
            balance = self.get_account_balance()
            
            # Calculate position size as percentage of balance
            position_value = balance * (self.max_position_percent / 100)
            
            # With leverage, actual position size is larger
            leveraged_position = position_value * self.leverage
            
            # Calculate quantity (how many coins to buy/sell)
            quantity = leveraged_position / price
            
            # Round to acceptable precision for the exchange
            market = self.exchange.market(self.symbol)
            quantity = self.exchange.amount_to_precision(self.symbol, quantity)
            
            logging.info(f"Position size calculated: {quantity} at price {price}")
            return float(quantity)
        except Exception as e:
            logging.error(f"Failed to calculate position size: {e}")
            return 0
    
    def check_total_exposure(self):
        """Check if total exposure is within safe limits"""
        try:
            balance = self.get_account_balance()
            positions = self.exchange.fetch_positions([self.symbol.replace('/', '')])
            
            total_exposure = 0
            for pos in positions:
                if pos['contracts'] > 0:
                    total_exposure += abs(float(pos['notional']))
            
            exposure_percent = (total_exposure / balance) * 100
            
            logging.info(f"Total exposure: {exposure_percent:.2f}% of balance")
            
            if exposure_percent >= self.max_total_exposure:
                logging.warning(f"Max exposure reached ({exposure_percent:.2f}%), blocking new orders")
                return False
            
            return True
        except Exception as e:
            logging.error(f"Failed to check exposure: {e}")
            return False
    
    def place_grid_orders(self):
        """Place limit orders at grid levels"""
        if not self.check_volatility():
            logging.info("Volatility too high, skipping order placement")
            return
        
        if not self.check_total_exposure():
            logging.info("Max exposure reached, skipping order placement")
            return
        
        try:
            current_price = self.exchange.fetch_ticker(self.symbol)['last']
            
            for level in self.grid_levels:
                if level['filled']:
                    continue
                
                # Only place orders that haven't been filled
                price = level['price']
                order_type = level['type']
                
                # Calculate position size
                quantity = self.calculate_position_size(price)
                
                if quantity <= 0:
                    logging.warning(f"Invalid quantity for {order_type} at {price}")
                    continue
                
                # Place limit order
                side = 'buy' if order_type == 'buy' else 'sell'
                
                try:
                    order = self.exchange.create_order(
                        symbol=self.symbol,
                        type='limit',
                        side=side,
                        amount=quantity,
                        price=price
                    )
                    
                    self.active_orders[order['id']] = {
                        'level': level,
                        'order': order
                    }
                    
                    logging.info(f"Placed {side} order: {quantity} at {price}")
                except Exception as e:
                    logging.error(f"Failed to place {side} order at {price}: {e}")
        
        except Exception as e:
            logging.error(f"Failed to place grid orders: {e}")
    
    def check_orders(self):
        """Check status of active orders and manage positions"""
        try:
            for order_id in list(self.active_orders.keys()):
                order_info = self.exchange.fetch_order(order_id, self.symbol)
                
                if order_info['status'] == 'closed':
                    # Order filled, mark grid level as filled
                    level = self.active_orders[order_id]['level']
                    level['filled'] = True
                    
                    logging.info(f"Order filled: {order_info['side']} {order_info['amount']} at {order_info['price']}")
                    
                    # Remove from active orders
                    del self.active_orders[order_id]
                    
                    # Place opposite order at next grid level
                    self.place_opposite_order(level)
        
        except Exception as e:
            logging.error(f"Failed to check orders: {e}")
    
    def place_opposite_order(self, filled_level):
        """Place opposite order after a grid level is filled"""
        try:
            # If a buy was filled, place a sell above it
            # If a sell was filled, place a buy below it
            
            price_adjustment = self.grid_spacing_percent / 100
            
            if filled_level['type'] == 'buy':
                # Place sell order above
                new_price = filled_level['price'] * (1 + price_adjustment)
                side = 'sell'
            else:
                # Place buy order below
                new_price = filled_level['price'] * (1 - price_adjustment)
                side = 'buy'
            
            quantity = self.calculate_position_size(new_price)
            
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
                'type': side,
                'filled': False
            }
            self.grid_levels.append(new_level)
            
            self.active_orders[order['id']] = {
                'level': new_level,
                'order': order
            }
            
            logging.info(f"Placed opposite {side} order at {new_price}")
        
        except Exception as e:
            logging.error(f"Failed to place opposite order: {e}")
    
    def check_stop_loss(self):
        """Emergency stop loss check to prevent account wipeout"""
        try:
            balance = self.get_account_balance()
            positions = self.exchange.fetch_positions([self.symbol.replace('/', '')])
            
            for pos in positions:
                if pos['contracts'] > 0:
                    unrealized_pnl = float(pos['unrealizedPnl'])
                    pnl_percent = (unrealized_pnl / balance) * 100
                    
                    # If loss exceeds stop loss threshold, close position
                    if pnl_percent < -self.stop_loss_percent:
                        logging.critical(f"STOP LOSS TRIGGERED: {pnl_percent:.2f}% loss")
                        self.close_all_positions()
                        return False
            
            return True
        except Exception as e:
            logging.error(f"Failed to check stop loss: {e}")
            return True
    
    def close_all_positions(self):
        """Emergency close all positions"""
        try:
            # Cancel all open orders
            self.exchange.cancel_all_orders(self.symbol)
            
            # Close all positions
            positions = self.exchange.fetch_positions([self.symbol.replace('/', '')])
            
            for pos in positions:
                if pos['contracts'] > 0:
                    side = 'sell' if pos['side'] == 'long' else 'buy'
                    quantity = abs(float(pos['contracts']))
                    
                    self.exchange.create_order(
                        symbol=self.symbol,
                        type='market',
                        side=side,
                        amount=quantity,
                        params={'reduceOnly': True}
                    )
            
            logging.critical("All positions closed")
            self.active_orders = {}
        except Exception as e:
            logging.error(f"Failed to close positions: {e}")
    
    def run(self):
        """Main bot loop"""
        logging.info("Starting Grid Trading Bot")
        
        # Set leverage
        self.set_leverage()
        
        # Calculate initial grid
        if not self.calculate_grid_levels():
            logging.error("Failed to calculate grid levels, exiting")
            return
        
        # Main loop
        try:
            while True:
                logging.info("--- Bot cycle start ---")
                
                # Check stop loss first (safety)
                if not self.check_stop_loss():
                    logging.critical("Stop loss triggered, bot stopped")
                    break
                
                # Check and place orders
                self.place_grid_orders()
                
                # Check order status
                self.check_orders()
                
                # Sleep before next cycle
                logging.info(f"Sleeping for {self.check_interval} seconds")
                time.sleep(self.check_interval)
        
        except KeyboardInterrupt:
            logging.info("Bot stopped by user")
            self.close_all_positions()
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            self.close_all_positions()

if __name__ == "__main__":
    bot = GridTradingBot('config.json')
    bot.run()
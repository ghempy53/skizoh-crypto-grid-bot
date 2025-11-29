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

# =============================================================================
# SKIZOH CRYPTO GRID TRADING BOT - Core Trading Engine
# =============================================================================
# Major improvements over v13:
# - Proper cost basis tracking (FIFO) for accurate P&L
# - Fee-aware minimum grid spacing
# - Position/exposure limits to prevent over-concentration
# - ADX trend filter (pause in strong trends)
# - Partial fill handling
# - Smarter grid repositioning that preserves positions
# - More conservative profit compounding
# - Better emergency handling
# =============================================================================

import ccxt
import time
import json
import logging
from datetime import datetime
from collections import deque
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


class PositionTracker:
    """Track positions with proper cost basis using FIFO."""
    
    def __init__(self):
        self.positions = deque()  # FIFO queue of (quantity, price, timestamp)
        self.total_quantity = 0
        self.total_cost = 0
        self.realized_pnl = 0
        self.total_fees_paid = 0
    
    def add_position(self, quantity, price, fee=0):
        """Add a buy position."""
        cost_basis = (quantity * price) + fee
        self.positions.append({
            'quantity': quantity,
            'price': price,
            'cost_basis': cost_basis,
            'timestamp': datetime.now()
        })
        self.total_quantity += quantity
        self.total_cost += cost_basis
        self.total_fees_paid += fee
        
        logging.debug(f"Added position: {quantity} @ ${price:.2f}, cost basis: ${cost_basis:.2f}")
    
    def close_position(self, quantity, sell_price, fee=0):
        """Close position using FIFO and calculate realized P&L."""
        if quantity > self.total_quantity:
            logging.warning(f"Attempting to sell {quantity} but only have {self.total_quantity}")
            quantity = self.total_quantity
        
        remaining = quantity
        total_cost_basis = 0
        
        while remaining > 0 and self.positions:
            oldest = self.positions[0]
            
            if oldest['quantity'] <= remaining:
                # Use entire position
                total_cost_basis += oldest['cost_basis']
                remaining -= oldest['quantity']
                self.total_quantity -= oldest['quantity']
                self.total_cost -= oldest['cost_basis']
                self.positions.popleft()
            else:
                # Partial use
                fraction = remaining / oldest['quantity']
                used_cost = oldest['cost_basis'] * fraction
                total_cost_basis += used_cost
                
                oldest['quantity'] -= remaining
                oldest['cost_basis'] -= used_cost
                self.total_quantity -= remaining
                self.total_cost -= used_cost
                remaining = 0
        
        # Calculate P&L
        proceeds = (quantity * sell_price) - fee
        pnl = proceeds - total_cost_basis
        self.realized_pnl += pnl
        self.total_fees_paid += fee
        
        logging.debug(f"Closed position: {quantity} @ ${sell_price:.2f}, P&L: ${pnl:.2f}")
        
        return {
            'quantity': quantity,
            'sell_price': sell_price,
            'cost_basis': total_cost_basis,
            'proceeds': proceeds,
            'pnl': pnl,
            'fee': fee
        }
    
    def get_average_cost(self):
        """Get weighted average cost basis."""
        if self.total_quantity <= 0:
            return 0
        return self.total_cost / self.total_quantity
    
    def get_unrealized_pnl(self, current_price):
        """Calculate unrealized P&L at current price."""
        if self.total_quantity <= 0:
            return 0
        market_value = self.total_quantity * current_price
        return market_value - self.total_cost
    
    def get_summary(self, current_price):
        """Get full position summary."""
        return {
            'total_quantity': self.total_quantity,
            'total_cost': self.total_cost,
            'average_cost': self.get_average_cost(),
            'market_value': self.total_quantity * current_price,
            'unrealized_pnl': self.get_unrealized_pnl(current_price),
            'realized_pnl': self.realized_pnl,
            'total_pnl': self.realized_pnl + self.get_unrealized_pnl(current_price),
            'total_fees': self.total_fees_paid,
            'num_positions': len(self.positions)
        }


class SmartGridTradingBot:
    """Smart grid trading bot v14 with advanced risk management."""
    
    # Exchange fee rate (Binance.US maker/taker)
    DEFAULT_FEE_RATE = 0.001  # 0.1%
    
    def __init__(self, config_file='config.json'):
        """Initialize the smart grid trading bot."""
        self.config_manager = ConfigManager(config_file)
        config = self.config_manager.load_config()
        
        # API credentials
        self.api_key = config['api_key']
        self.api_secret = config['api_secret']
        self.symbol = config['symbol']
        
        # Fee configuration
        self.fee_rate = config.get('fee_rate', self.DEFAULT_FEE_RATE)
        
        # Select scenario interactively
        scenario = self.config_manager.select_scenario_interactive()
        self.load_scenario(scenario)
        
        # Initialize exchange and analyzers
        self.exchange = self.initialize_exchange()
        self.market_analyzer = MarketAnalyzer(self.exchange, self.symbol)
        
        # Position tracking (NEW)
        self.position_tracker = PositionTracker()
        
        # Trading state
        self.grid_levels = []
        self.active_orders = {}
        self.initial_investment = 0
        self.cycles_completed = 0
        
        # Exposure limits (NEW)
        self.max_position_percent = config.get('max_position_percent', 80)  # Max % of capital in crypto
        self.max_single_order_percent = config.get('max_single_order_percent', 10)  # Max single order size
        
        # Tax logging
        self.tax_log_file = '../data/tax_transactions.csv'
        self.initialize_tax_log()
        
        # Grid repositioning
        self.grid_center_price = None
        self.last_grid_update = time.time()
        
        # Performance tracking
        self.start_time = None
        self.peak_value = 0
        self.max_drawdown = 0
        
        # Trend pause state
        self.trend_pause_until = 0
    
    def load_scenario(self, scenario):
        """Load selected scenario configuration."""
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
        
        # Validate grid spacing vs fees
        self._validate_grid_spacing()
        
        logging.info(f"Loaded scenario: {self.scenario_name}")
    
    def _validate_grid_spacing(self):
        """Ensure grid spacing is profitable after fees."""
        # Minimum profitable spacing = 2 * fee_rate * safety_factor
        # With 0.1% fee each way, need > 0.2% spacing minimum
        # We use 2.5x safety factor
        min_spacing = (2 * self.fee_rate * 100) * 2.5
        
        if self.grid_spacing_percent < min_spacing:
            old_spacing = self.grid_spacing_percent
            self.grid_spacing_percent = min_spacing
            logging.warning(
                f"⚠️ Grid spacing {old_spacing}% is too tight for {self.fee_rate*100}% fees. "
                f"Adjusted to {min_spacing:.2f}% minimum for profitability."
            )
    
    def initialize_exchange(self):
        """Initialize connection to Binance.US."""
        try:
            exchange = ccxt.binanceus({
                'apiKey': self.api_key,
                'secret': self.api_secret,
                'enableRateLimit': True,
            })
            exchange.load_markets()
            
            # Get actual fee rate from exchange if possible
            try:
                trading_fees = exchange.fetch_trading_fees()
                if self.symbol in trading_fees:
                    self.fee_rate = max(
                        trading_fees[self.symbol].get('maker', self.fee_rate),
                        trading_fees[self.symbol].get('taker', self.fee_rate)
                    )
                    logging.info(f"Using exchange fee rate: {self.fee_rate*100:.3f}%")
            except Exception:
                logging.info(f"Using default fee rate: {self.fee_rate*100:.3f}%")
            
            logging.info("Exchange connection established (Binance.US)")
            return exchange
        except Exception as e:
            logging.error(f"Failed to initialize exchange: {e}")
            raise
    
    def initialize_tax_log(self):
        """Initialize CSV file for tax record keeping."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.tax_log_file), exist_ok=True)
            
            file_exists = os.path.isfile(self.tax_log_file)
            
            if not file_exists:
                with open(self.tax_log_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        'Date/Time', 'Transaction Type', 'Asset', 'Amount',
                        'Price (USD)', 'Total Value (USD)', 'Fee (USD)',
                        'Net Proceeds (USD)', 'Cost Basis (USD)', 'Realized P&L (USD)',
                        'Order ID', 'Notes'
                    ])
                logging.info(f"Created tax log file: {self.tax_log_file}")
            else:
                logging.info(f"Using existing tax log file: {self.tax_log_file}")
        except Exception as e:
            logging.error(f"Failed to initialize tax log: {e}")
    
    def log_tax_transaction(self, transaction_type, asset, amount, price, fee, 
                           order_id, cost_basis=0, realized_pnl=0, notes=''):
        """Log a transaction for tax purposes with enhanced tracking."""
        try:
            total_value = amount * price
            net_proceeds = total_value - fee if transaction_type == 'SELL' else total_value + fee
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            with open(self.tax_log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    timestamp, transaction_type, asset, f"{amount:.8f}",
                    f"{price:.2f}", f"{total_value:.2f}", f"{fee:.4f}",
                    f"{net_proceeds:.2f}", f"{cost_basis:.2f}", f"{realized_pnl:.2f}",
                    order_id, notes
                ])
            
            logging.info(f"💰 Tax log: {transaction_type} {amount:.6f} {asset} @ ${price:.2f}")
        except Exception as e:
            logging.error(f"Failed to log tax transaction: {e}")
    
    def get_balances(self):
        """Get USDT and crypto balances."""
        try:
            balance = self.exchange.fetch_balance()
            base_currency = self.symbol.split('/')[0]
            quote_currency = self.symbol.split('/')[1]
            
            base_free = balance[base_currency]['free']
            base_total = balance[base_currency]['total']
            quote_free = balance[quote_currency]['free']
            quote_total = balance[quote_currency]['total']
            
            logging.info(f"Balances - {base_currency}: {base_free:.6f} (total: {base_total:.6f}), "
                        f"{quote_currency}: {quote_free:.2f} (total: {quote_total:.2f})")
            
            return {
                'base': base_free,
                'base_total': base_total,
                'quote': quote_free,
                'quote_total': quote_total,
                'base_currency': base_currency,
                'quote_currency': quote_currency
            }
        except Exception as e:
            logging.error(f"Failed to fetch balance: {e}")
            return None
    
    def check_exposure_limits(self, current_price):
        """Check if we're within position limits."""
        balances = self.get_balances()
        if not balances:
            return {'within_limits': False, 'reason': 'Could not fetch balances'}
        
        crypto_value = balances['base_total'] * current_price
        total_value = crypto_value + balances['quote_total']
        
        if total_value <= 0:
            return {'within_limits': False, 'reason': 'No capital'}
        
        exposure_percent = (crypto_value / total_value) * 100
        
        return {
            'within_limits': exposure_percent < self.max_position_percent,
            'current_exposure': exposure_percent,
            'max_exposure': self.max_position_percent,
            'can_buy_more': exposure_percent < self.max_position_percent,
            'should_reduce': exposure_percent > self.max_position_percent * 1.1,
            'crypto_value': crypto_value,
            'total_value': total_value
        }
    
    def check_trend_filter(self):
        """Check if market is trending (grid trading performs poorly in trends)."""
        if time.time() < self.trend_pause_until:
            remaining = int(self.trend_pause_until - time.time())
            logging.info(f"⏸️ Trend pause active, {remaining}s remaining")
            return False
        
        safety = self.market_analyzer.is_safe_to_trade()
        
        if not safety['safe']:
            # Pause trading for 30 minutes when strong trend detected
            self.trend_pause_until = time.time() + 1800
            for reason in safety['reasons']:
                logging.warning(f"🚨 {reason}")
            logging.warning(f"⏸️ Pausing grid trading for 30 minutes: {safety['recommendation']}")
            return False
        
        if safety['warnings']:
            for warning in safety['warnings']:
                logging.info(f"⚠️ {warning}")
        
        return True
    
    def check_volatility(self):
        """Check if market volatility is within acceptable range."""
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
            
            logging.info(f"Current volatility (ATR): {volatility_percent:.2f}%")
            
            if volatility_percent > self.volatility_threshold:
                logging.warning(f"High volatility ({volatility_percent:.2f}%), using wider grid")
                return False
            
            return True
        except Exception as e:
            logging.error(f"Failed to check volatility: {e}")
            return True  # Continue trading if check fails
    
    def calculate_compounded_investment(self):
        """Calculate investment with MORE CONSERVATIVE compounding."""
        if self.initial_investment <= 0:
            return self.investment_percent
        
        current_price = self.exchange.fetch_ticker(self.symbol)['last']
        position_summary = self.position_tracker.get_summary(current_price)
        total_pnl = position_summary['total_pnl']
        profit_percent = (total_pnl / self.initial_investment) * 100
        
        # More conservative compounding tiers
        if profit_percent > 30:
            compound_percent = min(85, self.investment_percent + 8)
        elif profit_percent > 20:
            compound_percent = min(82, self.investment_percent + 6)
        elif profit_percent > 10:
            compound_percent = min(80, self.investment_percent + 4)
        elif profit_percent > 5:
            compound_percent = min(78, self.investment_percent + 2)
        elif profit_percent < -10:
            # REDUCE exposure when losing
            compound_percent = max(50, self.investment_percent - 10)
            logging.warning(f"📉 Reducing exposure due to {profit_percent:.1f}% loss")
        elif profit_percent < -5:
            compound_percent = max(60, self.investment_percent - 5)
        else:
            compound_percent = self.investment_percent
        
        if compound_percent != self.investment_percent:
            logging.info(f"💎 Investment adjusted to {compound_percent}% (P&L: {profit_percent:.1f}%)")
        
        return compound_percent
    
    def should_reposition_grid(self, current_price):
        """Check if grid needs repositioning."""
        if self.grid_center_price is None:
            return False
        
        price_move_percent = abs((current_price - self.grid_center_price) / self.grid_center_price) * 100
        reposition_threshold = self.grid_spacing_percent * 2.5  # Slightly more tolerant
        
        time_since_update = time.time() - self.last_grid_update
        min_time_between_updates = 600  # 10 minutes (increased from 5)
        
        if price_move_percent > reposition_threshold and time_since_update > min_time_between_updates:
            logging.info(f"🔄 Grid repositioning needed: price moved {price_move_percent:.2f}%")
            return True
        
        return False
    
    def calculate_grid_levels(self, reposition=False):
        """Calculate grid levels with exposure limits and fee-awareness."""
        try:
            current_price = self.exchange.fetch_ticker(self.symbol)['last']
            balances = self.get_balances()
            
            if not balances:
                return False
            
            # Check trend filter
            if not self.check_trend_filter():
                logging.info("Skipping grid calculation due to trend filter")
                return True  # Not a failure, just waiting
            
            # Get market bias
            bias = self.market_analyzer.should_adjust_grid_bias()
            
            # Get support/resistance
            sr_levels = self.market_analyzer.find_support_resistance()
            
            # Calculate investment with compounding
            investment_percent = self.calculate_compounded_investment()
            available_usdt = balances['quote'] * (investment_percent / 100)
            
            # Check exposure limits
            exposure = self.check_exposure_limits(current_price)
            if exposure.get('should_reduce'):
                logging.warning(f"⚠️ Exposure too high ({exposure['current_exposure']:.1f}%), reducing buys")
                bias['buy_weight'] *= 0.5
                bias['sell_weight'] = 1 - bias['buy_weight']
            
            if self.initial_investment == 0:
                self.initial_investment = balances['quote'] + (balances['base'] * current_price)
                self.start_time = datetime.now()
            
            # Cancel existing orders if repositioning
            if reposition:
                logging.info("🔄 Repositioning grid - cancelling unfilled orders")
                self.cancel_all_orders()
            
            self.grid_levels = []
            self.grid_center_price = current_price
            self.last_grid_update = time.time()
            
            # Calculate buy and sell levels
            total_levels = self.grid_levels_count
            buy_levels = max(1, int(total_levels * bias['buy_weight']))
            sell_levels = max(1, int(total_levels * bias['sell_weight']))
            
            logging.info(f"📊 Grid bias: {bias['bias']} (Buy: {buy_levels}, Sell: {sell_levels}, "
                        f"Confidence: {bias.get('confidence', 'N/A')})")
            
            # Calculate order sizes with limits
            max_single_usdt = self.initial_investment * (self.max_single_order_percent / 100)
            usdt_per_buy = min(available_usdt / buy_levels, max_single_usdt) if buy_levels > 0 else 0
            
            # Create BUY levels
            for i in range(1, buy_levels + 1):
                price_level = current_price * (1 - (i * self.grid_spacing_percent / 100))
                
                # Adjust to S/R
                if sr_levels and sr_levels['support']:
                    price_level = self._adjust_to_sr_level(price_level, sr_levels['support'], 'support')
                
                if usdt_per_buy < self.min_order_size_usdt:
                    continue
                
                quantity = usdt_per_buy / price_level
                
                self.grid_levels.append({
                    'price': round(price_level, 2),
                    'quantity': quantity,
                    'type': 'buy',
                    'filled': False,
                    'order_id': None
                })
            
            # Create SELL levels
            crypto_available = balances['base']
            crypto_per_sell = crypto_available / sell_levels if sell_levels > 0 and crypto_available > 0 else 0
            
            # Also cap sell size
            max_single_crypto = (max_single_usdt / current_price) if current_price > 0 else 0
            crypto_per_sell = min(crypto_per_sell, max_single_crypto)
            
            for i in range(1, sell_levels + 1):
                price_level = current_price * (1 + (i * self.grid_spacing_percent / 100))
                
                if sr_levels and sr_levels['resistance']:
                    price_level = self._adjust_to_sr_level(price_level, sr_levels['resistance'], 'resistance')
                
                if crypto_per_sell > 0:
                    self.grid_levels.append({
                        'price': round(price_level, 2),
                        'quantity': crypto_per_sell,
                        'type': 'sell',
                        'filled': False,
                        'order_id': None
                    })
            
            logging.info(f"Generated {len(self.grid_levels)} grid levels around ${current_price:.2f}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to calculate grid levels: {e}")
            return False
    
    def _adjust_to_sr_level(self, target_price, sr_levels, level_type):
        """Adjust order to nearby S/R level."""
        threshold = target_price * 0.004  # 0.4% threshold
        
        for sr_price in sr_levels[:3]:  # Only check closest 3
            if abs(sr_price - target_price) < threshold:
                logging.debug(f"📍 Adjusted {level_type}: ${target_price:.2f} → ${sr_price:.2f}")
                return sr_price
        
        return target_price
    
    def place_grid_orders(self):
        """Place limit orders at grid levels."""
        if not self.check_volatility():
            logging.info("Volatility outside range, adjusting...")
        
        try:
            for level in self.grid_levels:
                if level['filled'] or level.get('order_id'):
                    continue
                
                price = level['price']
                quantity = self.exchange.amount_to_precision(self.symbol, level['quantity'])
                quantity = float(quantity)
                
                if quantity <= 0:
                    continue
                
                # Skip if order already placed
                if any(od['level'] == level for od in self.active_orders.values()):
                    continue
                
                try:
                    order = self.exchange.create_order(
                        symbol=self.symbol,
                        type='limit',
                        side=level['type'],
                        amount=quantity,
                        price=price
                    )
                    
                    level['order_id'] = order['id']
                    self.active_orders[order['id']] = {'level': level, 'order': order}
                    logging.info(f"✓ Placed {level['type'].upper()}: {quantity:.6f} @ ${price:.2f}")
                    
                except ccxt.InsufficientFunds as e:
                    logging.warning(f"Insufficient funds for {level['type']} @ ${price}: {e}")
                    break
                except Exception as e:
                    logging.warning(f"Could not place {level['type']} @ ${price}: {e}")
        
        except Exception as e:
            logging.error(f"Failed to place grid orders: {e}")
    
    def check_orders(self):
        """Check order status with partial fill handling."""
        try:
            for order_id in list(self.active_orders.keys()):
                try:
                    order_info = self.exchange.fetch_order(order_id, self.symbol)
                    status = order_info['status']
                    
                    if status == 'closed':
                        self._handle_filled_order(order_id, order_info)
                    
                    elif status == 'canceled':
                        level = self.active_orders[order_id]['level']
                        level['order_id'] = None
                        del self.active_orders[order_id]
                        logging.info(f"Order {order_id} was cancelled externally")
                    
                    # Handle partial fills
                    elif status == 'open' and order_info['filled'] > 0:
                        self._handle_partial_fill(order_id, order_info)
                
                except Exception as e:
                    logging.warning(f"Error checking order {order_id}: {e}")
        
        except Exception as e:
            logging.error(f"Failed to check orders: {e}")
    
    def _handle_filled_order(self, order_id, order_info):
        """Handle a completely filled order."""
        level = self.active_orders[order_id]['level']
        level['filled'] = True
        
        side = order_info['side']
        amount = order_info['filled']
        price = float(order_info['average']) if order_info['average'] else float(order_info['price'])
        
        # Calculate fee
        fee = self._calculate_fee(order_info, amount, price)
        
        # Track position and P&L properly
        base_currency = self.symbol.split('/')[0]
        
        if side == 'buy':
            self.position_tracker.add_position(amount, price, fee)
            cost_basis = amount * price + fee
            self.log_tax_transaction(
                'BUY', base_currency, amount, price, fee, order_id,
                cost_basis=cost_basis, notes='Grid buy order filled'
            )
        else:
            # SELL - calculate actual P&L from cost basis
            result = self.position_tracker.close_position(amount, price, fee)
            self.cycles_completed += 1
            
            logging.info(f"💰 Cycle #{self.cycles_completed} P&L: ${result['pnl']:.2f} "
                        f"(Cost: ${result['cost_basis']:.2f}, Proceeds: ${result['proceeds']:.2f})")
            
            self.log_tax_transaction(
                'SELL', base_currency, amount, price, fee, order_id,
                cost_basis=result['cost_basis'], realized_pnl=result['pnl'],
                notes='Grid sell order filled'
            )
        
        logging.info(f"✓ FILLED: {side.upper()} {amount:.6f} @ ${price:.2f}")
        
        del self.active_orders[order_id]
        self.place_opposite_order(level, price, amount)
    
    def _handle_partial_fill(self, order_id, order_info):
        """Handle partially filled orders."""
        filled = order_info['filled']
        remaining = order_info['remaining']
        price = float(order_info['average']) if order_info['average'] else float(order_info['price'])
        side = order_info['side']
        
        # Track the filled portion
        level = self.active_orders[order_id]['level']
        
        # Only log if we haven't already processed this fill amount
        tracked_filled = self.active_orders[order_id].get('tracked_filled', 0)
        new_fill = filled - tracked_filled
        
        if new_fill > 0.000001:  # Minimum threshold
            fee = new_fill * price * self.fee_rate
            base_currency = self.symbol.split('/')[0]
            
            if side == 'buy':
                self.position_tracker.add_position(new_fill, price, fee)
            # For sells, we'll handle full position closure when order completes
            
            self.active_orders[order_id]['tracked_filled'] = filled
            logging.info(f"📊 Partial fill: {side.upper()} {new_fill:.6f} @ ${price:.2f} "
                        f"(remaining: {remaining:.6f})")
    
    def _calculate_fee(self, order_info, amount, price):
        """Calculate trading fee from order info."""
        fee = 0
        if 'fee' in order_info and order_info['fee']:
            fee_info = order_info['fee']
            if fee_info.get('cost'):
                if fee_info.get('currency') in ['USDT', 'USD', 'USDC']:
                    fee = float(fee_info['cost'])
                else:
                    fee = float(fee_info['cost']) * price
        
        if fee == 0:
            fee = (amount * price) * self.fee_rate
        
        return fee
    
    def place_opposite_order(self, filled_level, fill_price, filled_quantity):
        """Place opposite order after a grid level fills."""
        try:
            price_adjustment = self.grid_spacing_percent / 100
            
            if filled_level['type'] == 'buy':
                new_price = fill_price * (1 + price_adjustment)
                side = 'sell'
                quantity = filled_quantity  # Sell exactly what we bought
            else:
                new_price = fill_price * (1 - price_adjustment)
                side = 'buy'
                # Use proceeds to buy back
                proceeds = filled_quantity * fill_price
                quantity = proceeds / new_price
            
            quantity = self.exchange.amount_to_precision(self.symbol, quantity)
            quantity = float(quantity)
            
            if quantity <= 0:
                return
            
            new_price = round(new_price, 2)
            
            order = self.exchange.create_order(
                symbol=self.symbol,
                type='limit',
                side=side,
                amount=quantity,
                price=new_price
            )
            
            new_level = {
                'price': new_price,
                'quantity': quantity,
                'type': side,
                'filled': False,
                'order_id': order['id'],
                'linked_to': filled_level['price']  # Track linkage
            }
            
            self.grid_levels.append(new_level)
            self.active_orders[order['id']] = {'level': new_level, 'order': order}
            
            logging.info(f"✓ Placed opposite {side.upper()}: {quantity:.6f} @ ${new_price:.2f}")
        
        except Exception as e:
            logging.error(f"Failed to place opposite order: {e}")
    
    def calculate_current_value(self):
        """Calculate portfolio value with proper P&L tracking."""
        try:
            balances = self.get_balances()
            if not balances:
                return None
            
            current_price = self.exchange.fetch_ticker(self.symbol)['last']
            
            # Get position summary
            position = self.position_tracker.get_summary(current_price)
            
            # Calculate total value including open orders
            open_orders_value = 0
            try:
                open_orders = self.exchange.fetch_open_orders(self.symbol)
                for order in open_orders:
                    if order['side'] == 'buy':
                        open_orders_value += float(order['remaining']) * float(order['price'])
                    else:
                        open_orders_value += float(order['remaining']) * current_price
            except Exception:
                pass
            
            total_value = balances['quote'] + (balances['base'] * current_price)
            
            # Track peak for drawdown calculation
            if total_value > self.peak_value:
                self.peak_value = total_value
            
            if self.peak_value > 0:
                drawdown = ((self.peak_value - total_value) / self.peak_value) * 100
                if drawdown > self.max_drawdown:
                    self.max_drawdown = drawdown
            
            if self.initial_investment > 0:
                total_pnl = total_value - self.initial_investment
                pnl_percent = (total_pnl / self.initial_investment) * 100
                
                logging.info(
                    f"📊 Portfolio: ${total_value:.2f} | "
                    f"P&L: ${total_pnl:.2f} ({pnl_percent:+.2f}%) | "
                    f"Realized: ${position['realized_pnl']:.2f} | "
                    f"Cycles: {self.cycles_completed} | "
                    f"Max DD: {self.max_drawdown:.1f}%"
                )
                
                return {
                    'total_value': total_value,
                    'profit': total_pnl,
                    'profit_percent': pnl_percent,
                    'realized_pnl': position['realized_pnl'],
                    'unrealized_pnl': position['unrealized_pnl'],
                    'max_drawdown': self.max_drawdown,
                    'fees_paid': position['total_fees']
                }
            
            return None
        except Exception as e:
            logging.error(f"Failed to calculate portfolio value: {e}")
            return None
    
    def check_stop_loss(self):
        """Check stop loss with proper drawdown tracking."""
        portfolio = self.calculate_current_value()
        
        if portfolio:
            # Check percentage loss
            if portfolio['profit_percent'] < -self.stop_loss_percent:
                logging.critical(f"⚠️ STOP LOSS: {portfolio['profit_percent']:.2f}% loss")
                self.emergency_stop()
                return False
            
            # Check drawdown
            if self.max_drawdown > self.stop_loss_percent * 1.5:
                logging.critical(f"⚠️ DRAWDOWN STOP: {self.max_drawdown:.2f}% drawdown")
                self.emergency_stop()
                return False
        
        return True
    
    def emergency_stop(self):
        """Emergency stop with full reporting."""
        try:
            logging.critical("🛑 EMERGENCY STOP ACTIVATED")
            
            # Cancel all orders
            try:
                open_orders = self.exchange.fetch_open_orders(self.symbol)
                for order in open_orders:
                    self.exchange.cancel_order(order['id'], self.symbol)
                    logging.info(f"Cancelled: {order['id']}")
            except Exception as e:
                logging.error(f"Error cancelling orders: {e}")
            
            self.active_orders = {}
            
            # Sell remaining position
            balances = self.get_balances()
            if balances and balances['base'] > 0:
                try:
                    quantity = self.exchange.amount_to_precision(self.symbol, balances['base'])
                    if float(quantity) > 0:
                        order = self.exchange.create_order(
                            symbol=self.symbol,
                            type='market',
                            side='sell',
                            amount=quantity
                        )
                        
                        current_price = self.exchange.fetch_ticker(self.symbol)['last']
                        fee = float(quantity) * current_price * self.fee_rate
                        
                        result = self.position_tracker.close_position(float(quantity), current_price, fee)
                        
                        self.log_tax_transaction(
                            'SELL', balances['base_currency'], float(quantity),
                            current_price, fee, order['id'],
                            cost_basis=result['cost_basis'], realized_pnl=result['pnl'],
                            notes='Emergency stop - market sell'
                        )
                        
                        logging.critical(f"Emergency sold {quantity} @ ${current_price:.2f}")
                except Exception as e:
                    logging.error(f"Error in emergency sell: {e}")
            
            # Final summary
            self._print_final_summary()
            
        except Exception as e:
            logging.error(f"Error during emergency stop: {e}")
    
    def _print_final_summary(self):
        """Print final trading session summary."""
        try:
            current_price = self.exchange.fetch_ticker(self.symbol)['last']
            position = self.position_tracker.get_summary(current_price)
            
            runtime = datetime.now() - self.start_time if self.start_time else None
            
            logging.info("=" * 60)
            logging.info("TRADING SESSION SUMMARY")
            logging.info("=" * 60)
            logging.info(f"Strategy: {self.scenario_name}")
            if runtime:
                logging.info(f"Runtime: {runtime}")
            logging.info(f"Cycles completed: {self.cycles_completed}")
            logging.info(f"Initial investment: ${self.initial_investment:.2f}")
            logging.info(f"Realized P&L: ${position['realized_pnl']:.2f}")
            logging.info(f"Total fees paid: ${position['total_fees']:.2f}")
            logging.info(f"Max drawdown: {self.max_drawdown:.2f}%")
            logging.info("=" * 60)
        except Exception as e:
            logging.error(f"Error printing summary: {e}")
    
    def cancel_all_orders(self):
        """Cancel all active orders."""
        try:
            open_orders = self.exchange.fetch_open_orders(self.symbol)
            for order in open_orders:
                try:
                    self.exchange.cancel_order(order['id'], self.symbol)
                except Exception as e:
                    logging.warning(f"Could not cancel {order['id']}: {e}")
            
            # Clear tracked orders
            for order_id in list(self.active_orders.keys()):
                level = self.active_orders[order_id]['level']
                level['order_id'] = None
            
            self.active_orders = {}
            logging.info("All orders cancelled")
        except Exception as e:
            logging.error(f"Failed to cancel orders: {e}")
    
    def run(self):
        """Main bot loop."""
        logging.info(f"🤖 Starting Smart Grid Trading Bot v14 - {self.scenario_name}")
        logging.info(f"📊 Grid: {self.grid_levels_count} levels @ {self.grid_spacing_percent}% spacing")
        logging.info(f"💰 Fee rate: {self.fee_rate*100:.3f}%")
        
        balances = self.get_balances()
        if balances:
            logging.info(f"Starting: {balances['quote']:.2f} {balances['quote_currency']}, "
                        f"{balances['base']:.6f} {balances['base_currency']}")
        
        if not self.calculate_grid_levels():
            logging.error("Failed to calculate grid levels")
            return
        
        try:
            while True:
                logging.info("--- 🔄 Cycle start ---")
                
                current_price = self.exchange.fetch_ticker(self.symbol)['last']
                
                # Check trend filter
                if not self.check_trend_filter():
                    logging.info(f"💤 Waiting for trend to weaken... ({self.check_interval}s)")
                    time.sleep(self.check_interval)
                    continue
                
                # Check grid repositioning
                if self.should_reposition_grid(current_price):
                    self.calculate_grid_levels(reposition=True)
                
                # Safety checks
                if not self.check_stop_loss():
                    break
                
                # Place and check orders
                self.place_grid_orders()
                self.check_orders()
                
                # Status update
                self.calculate_current_value()
                
                logging.info(f"💤 Sleeping {self.check_interval}s\n")
                time.sleep(self.check_interval)
        
        except KeyboardInterrupt:
            logging.info("🛑 Stopped by user")
            self.cancel_all_orders()
            self._print_final_summary()
        except Exception as e:
            logging.error(f"❌ Unexpected error: {e}")
            self.emergency_stop()

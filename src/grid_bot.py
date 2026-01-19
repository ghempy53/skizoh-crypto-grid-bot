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
# SKIZOH CRYPTO GRID TRADING BOT - Core Trading Engine v14.1
# =============================================================================
# Major improvements over v14:
# - Fixed path handling for data files
# - State persistence for position tracking
# - Improved error handling and validation
# - Fixed potential division by zero issues
# - Removed duplicate logging configuration
# - Better handling of edge cases
# =============================================================================

import ccxt
import time
import json
import logging
from datetime import datetime
from collections import deque, Counter
from pathlib import Path
from typing import Dict, List, Optional, Any
import numpy as np
import csv
import os

from config_manager import ConfigManager
from market_analysis import MarketAnalyzer

# Get logger (configured in main.py)
logger = logging.getLogger(__name__)


class PositionTracker:
    """Track positions with proper cost basis using FIFO."""
    
    def __init__(self, state_file: Optional[str] = None):
        self.positions = deque()  # FIFO queue of (quantity, price, timestamp)
        self.total_quantity = 0.0
        self.total_cost = 0.0
        self.realized_pnl = 0.0
        self.total_fees_paid = 0.0
        self.state_file = state_file
        
        # Load existing state if available
        if state_file:
            self._load_state()
    
    def _load_state(self):
        """Load position state from file."""
        try:
            if self.state_file and os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                
                self.total_quantity = float(state.get('total_quantity', 0))
                self.total_cost = float(state.get('total_cost', 0))
                self.realized_pnl = float(state.get('realized_pnl', 0))
                self.total_fees_paid = float(state.get('total_fees_paid', 0))
                
                # Restore positions
                for pos in state.get('positions', []):
                    self.positions.append({
                        'quantity': float(pos['quantity']),
                        'price': float(pos['price']),
                        'cost_basis': float(pos['cost_basis']),
                        'timestamp': datetime.fromisoformat(pos['timestamp'])
                    })
                
                logger.info(f"Loaded position state: {self.total_quantity:.6f} units, "
                           f"realized P&L: ${self.realized_pnl:.2f}")
        except Exception as e:
            logger.warning(f"Could not load position state: {e}")
    
    def _save_state(self):
        """Save position state to file."""
        try:
            if self.state_file:
                state = {
                    'total_quantity': self.total_quantity,
                    'total_cost': self.total_cost,
                    'realized_pnl': self.realized_pnl,
                    'total_fees_paid': self.total_fees_paid,
                    'positions': [
                        {
                            'quantity': pos['quantity'],
                            'price': pos['price'],
                            'cost_basis': pos['cost_basis'],
                            'timestamp': pos['timestamp'].isoformat()
                        }
                        for pos in self.positions
                    ],
                    'last_updated': datetime.now().isoformat()
                }
                
                with open(self.state_file, 'w') as f:
                    json.dump(state, f, indent=2)
                
                # Periodically recalculate to prevent float drift
                self._recalculate_totals()
        except Exception as e:
            logger.warning(f"Could not save position state: {e}")
    
    def _recalculate_totals(self):
        """Recalculate totals from positions to prevent floating-point drift."""
        self.total_quantity = sum(p['quantity'] for p in self.positions)
        self.total_cost = sum(p['cost_basis'] for p in self.positions)
    
    def add_position(self, quantity: float, price: float, fee: float = 0):
        """Add a buy position."""
        if quantity <= 0 or price <= 0:
            logger.warning(f"Invalid position: quantity={quantity}, price={price}")
            return
        
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
        
        logger.debug(f"Added position: {quantity} @ ${price:.2f}, cost basis: ${cost_basis:.2f}")
        self._save_state()
    
    def close_position(self, quantity: float, sell_price: float, fee: float = 0) -> Dict[str, float]:
        """Close position using FIFO and calculate realized P&L."""
        if quantity <= 0:
            return {'quantity': 0, 'sell_price': sell_price, 'cost_basis': 0, 
                    'proceeds': 0, 'pnl': 0, 'fee': fee}
        
        if quantity > self.total_quantity:
            logger.warning(f"Attempting to sell {quantity} but only have {self.total_quantity}")
            quantity = self.total_quantity
        
        if quantity <= 0:
            return {'quantity': 0, 'sell_price': sell_price, 'cost_basis': 0,
                    'proceeds': 0, 'pnl': 0, 'fee': fee}
        
        remaining = quantity
        total_cost_basis = 0.0
        
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
                if oldest['quantity'] > 0:
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
        
        logger.debug(f"Closed position: {quantity} @ ${sell_price:.2f}, P&L: ${pnl:.2f}")
        self._save_state()
        
        return {
            'quantity': quantity,
            'sell_price': sell_price,
            'cost_basis': total_cost_basis,
            'proceeds': proceeds,
            'pnl': pnl,
            'fee': fee
        }
    
    def get_average_cost(self) -> float:
        """Get weighted average cost basis."""
        if self.total_quantity <= 0:
            return 0.0
        return self.total_cost / self.total_quantity
    
    def get_unrealized_pnl(self, current_price: float) -> float:
        """Calculate unrealized P&L at current price."""
        if self.total_quantity <= 0 or current_price <= 0:
            return 0.0
        market_value = self.total_quantity * current_price
        return market_value - self.total_cost
    
    def get_summary(self, current_price: float) -> Dict[str, Any]:
        """Get full position summary."""
        if current_price <= 0:
            current_price = 0.0
        
        market_value = self.total_quantity * current_price if current_price > 0 else 0
        unrealized = self.get_unrealized_pnl(current_price)
        
        return {
            'total_quantity': self.total_quantity,
            'total_cost': self.total_cost,
            'average_cost': self.get_average_cost(),
            'market_value': market_value,
            'unrealized_pnl': unrealized,
            'realized_pnl': self.realized_pnl,
            'total_pnl': self.realized_pnl + unrealized,
            'total_fees': self.total_fees_paid,
            'num_positions': len(self.positions)
        }


class SmartGridTradingBot:
    """Smart grid trading bot v14.1 with advanced risk management."""
    
    # Exchange fee rate (Binance.US maker/taker)
    DEFAULT_FEE_RATE = 0.001  # 0.1%
    # Trend pause duration in seconds (30 minutes)
    TREND_PAUSE_SECONDS = 1800
    # Grid repositioning threshold multiplier
    REPOSITION_THRESHOLD_MULTIPLIER = 2.5
    # Minimum time between grid updates in seconds
    MIN_GRID_UPDATE_INTERVAL = 600
    # Fee safety factor for minimum grid spacing calculation
    FEE_SAFETY_FACTOR = 2.5
    
    def __init__(self, config_file: str = 'config.json'):
        """Initialize the smart grid trading bot."""
        # Resolve config file path
        self.config_file_path = Path(config_file).resolve()
        self.project_root = self.config_file_path.parent.parent
        self.data_dir = self.project_root / 'data'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_manager = ConfigManager(str(self.config_file_path))
        config = self.config_manager.load_config()
        
        # Validate required config fields
        self._validate_config(config)
        
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
        
        # Position tracking with state persistence
        position_state_file = str(self.data_dir / 'position_state.json')
        self.position_tracker = PositionTracker(state_file=position_state_file)
        
        # Trading state
        self.grid_levels: List[Dict] = []
        self.active_orders: Dict[str, Dict] = {}
        self.initial_investment = 0.0
        self.cycles_completed = 0
        
        # Exposure limits
        self.max_position_percent = config.get('max_position_percent', 80)
        self.max_single_order_percent = config.get('max_single_order_percent', 10)
        
        # Tax logging with absolute path
        self.tax_log_file = str(self.data_dir / 'tax_transactions.csv')
        self.initialize_tax_log()
        
        # Dynamic scenario adjustment settings
        self.enable_dynamic_scenarios = config.get('enable_dynamic_scenarios', True)
        self.cycles_per_scenario_check = config.get('cycles_per_scenario_check', 7)
        self.cycles_since_scenario_check = 0
        self.current_scenario_index = None  # Track current scenario index
        self.last_scenario_change = time.time()
        self.min_scenario_hold_time = config.get('min_scenario_hold_minutes', 60) * 60
        self.scenario_change_threshold = config.get('scenario_change_confidence', 0.7)
        self.recent_scenario_scores = []  # Track recent recommendations for stability
        
        # Grid repositioning
        self.grid_center_price: Optional[float] = None
        self.last_grid_update = time.time()
        
        # Performance tracking
        self.start_time: Optional[datetime] = None
        self.peak_value = 0.0
        self.max_drawdown = 0.0
        
        # Trend pause state
        self.trend_pause_until = 0.0
    
    def _validate_config(self, config: Dict[str, Any]):
        """Validate required configuration fields."""
        required_fields = ['api_key', 'api_secret', 'symbol', 'config_data']
        
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required config field: {field}")
        
        if config['api_key'] == 'YOUR_BINANCE_US_API_KEY':
            raise ValueError("API key not configured - update config.json")
        
        if config['api_secret'] == 'YOUR_BINANCE_US_API_SECRET':
            raise ValueError("API secret not configured - update config.json")
    
    def load_scenario(self, scenario: Dict[str, Any]):
        """Load selected scenario configuration."""
        self.scenario_name = scenario['name']
        self.grid_levels_count = scenario['grid_levels']
        self.grid_spacing_percent = scenario['grid_spacing_percent']
        self.investment_percent = scenario['investment_percent']
        self.min_order_size_usdt = scenario['min_order_size_usdt']
        self.stop_loss_percent = scenario['stop_loss_percent']
        self.atr_period = scenario['atr_period']
        self.volatility_threshold = scenario['volatility_threshold']
        self.check_interval = scenario['check_interval_seconds']
        
        # Validate grid spacing vs fees
        self._validate_grid_spacing()
        
        logger.info(f"Loaded scenario: {self.scenario_name}")
    
    def _validate_grid_spacing(self):
        """Ensure grid spacing is profitable after fees."""
        # Minimum profitable spacing = 2 * fee_rate * safety_factor
        # With 0.1% fee each way, need > 0.2% spacing minimum
        # We use 2.5x safety factor
        min_spacing = (2 * self.fee_rate * 100) * self.FEE_SAFETY_FACTOR
        
        if self.grid_spacing_percent < min_spacing:
            old_spacing = self.grid_spacing_percent
            self.grid_spacing_percent = min_spacing
            logger.warning(
                f"⚠️ Grid spacing {old_spacing}% is too tight for {self.fee_rate*100}% fees. "
                f"Adjusted to {min_spacing:.2f}% minimum for profitability."
            )
    
    def initialize_exchange(self) -> ccxt.binanceus:
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
                    logger.info(f"Using exchange fee rate: {self.fee_rate*100:.3f}%")
            except Exception:
                logger.info(f"Using default fee rate: {self.fee_rate*100:.3f}%")
            
            logger.info("Exchange connection established (Binance.US)")
            return exchange
        except Exception as e:
            logger.error(f"Failed to initialize exchange: {e}")
            raise
    
    def initialize_tax_log(self):
        """Initialize CSV file for tax record keeping."""
        try:
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
                logger.info(f"Created tax log file: {self.tax_log_file}")
            else:
                logger.info(f"Using existing tax log file: {self.tax_log_file}")
        except Exception as e:
            logger.error(f"Failed to initialize tax log: {e}")
    
    def log_tax_transaction(self, transaction_type: str, asset: str, amount: float, 
                           price: float, fee: float, order_id: str,
                           cost_basis: float = 0, realized_pnl: float = 0, notes: str = ''):
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
            
            logger.info(f"💰 Tax log: {transaction_type} {amount:.6f} {asset} @ ${price:.2f}")
        except Exception as e:
            logger.error(f"Failed to log tax transaction: {e}")
    
    def get_balances(self) -> Optional[Dict[str, Any]]:
        """Get USDT and crypto balances."""
        try:
            balance = self.exchange.fetch_balance()
            base_currency = self.symbol.split('/')[0]
            quote_currency = self.symbol.split('/')[1]
            
            base_free = float(balance[base_currency]['free'] or 0)
            base_total = float(balance[base_currency]['total'] or 0)
            quote_free = float(balance[quote_currency]['free'] or 0)
            quote_total = float(balance[quote_currency]['total'] or 0)
            
            logger.info(f"Balances - {base_currency}: {base_free:.6f} (total: {base_total:.6f}), "
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
            logger.error(f"Failed to fetch balance: {e}")
            return None
    
    def check_exposure_limits(self, current_price: float) -> Dict[str, Any]:
        """Check if we're within position limits."""
        balances = self.get_balances()
        if not balances:
            return {'within_limits': False, 'reason': 'Could not fetch balances'}
        
        if current_price <= 0:
            return {'within_limits': False, 'reason': 'Invalid price'}
        
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
    
    def check_trend_filter(self) -> bool:
        """Check if market is trending (grid trading performs poorly in trends)."""
        if time.time() < self.trend_pause_until:
            remaining = int(self.trend_pause_until - time.time())
            logger.info(f"⏸️ Trend pause active, {remaining}s remaining")
            return False
        
        safety = self.market_analyzer.is_safe_to_trade()
        
        if not safety['safe']:
            # Pause trading for 30 minutes when strong trend detected
            self.trend_pause_until = time.time() + self.TREND_PAUSE_SECONDS
            for reason in safety['reasons']:
                logger.warning(f"🚨 {reason}")
            logger.warning(f"⏸️ Pausing grid trading for 30 minutes: {safety['recommendation']}")
            return False
        
        if safety['warnings']:
            for warning in safety['warnings']:
                logger.info(f"⚠️ {warning}")
        
        return True
    
    def check_volatility(self) -> bool:
        """Check if market volatility is within acceptable range."""
        try:
            current_price = self.exchange.fetch_ticker(self.symbol)['last']
            if not current_price or current_price <= 0:
                return True
            
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, '1h', limit=self.atr_period+1)
            
            if len(ohlcv) < self.atr_period:
                return True
            
            highs = np.array([x[2] for x in ohlcv])
            lows = np.array([x[3] for x in ohlcv])
            closes = np.array([x[4] for x in ohlcv])
            
            tr1 = highs[1:] - lows[1:]
            tr2 = np.abs(highs[1:] - closes[:-1])
            tr3 = np.abs(lows[1:] - closes[:-1])
            
            true_range = np.maximum(tr1, np.maximum(tr2, tr3))
            atr = np.mean(true_range)
            volatility_percent = (atr / current_price) * 100 if current_price > 0 else 0
            
            logger.info(f"Current volatility (ATR): {volatility_percent:.2f}%")
            
            if volatility_percent > self.volatility_threshold:
                logger.warning(f"High volatility ({volatility_percent:.2f}%), using wider grid")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Failed to check volatility: {e}")
            return True  # Continue trading if check fails
    
    def calculate_compounded_investment(self) -> float:
        """Calculate investment with MORE CONSERVATIVE compounding."""
        if self.initial_investment <= 0:
            return self.investment_percent
        
        try:
            current_price = self.exchange.fetch_ticker(self.symbol)['last']
            if not current_price or current_price <= 0:
                return self.investment_percent
            
            position_summary = self.position_tracker.get_summary(current_price)
            total_pnl = position_summary['total_pnl']
            profit_percent = (total_pnl / self.initial_investment) * 100 if self.initial_investment > 0 else 0
            
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
                logger.warning(f"📉 Reducing exposure due to {profit_percent:.1f}% loss")
            elif profit_percent < -5:
                compound_percent = max(60, self.investment_percent - 5)
            else:
                compound_percent = self.investment_percent
            
            if compound_percent != self.investment_percent:
                logger.info(f"💎 Investment adjusted to {compound_percent}% (P&L: {profit_percent:.1f}%)")
            
            return compound_percent
        except Exception as e:
            logger.error(f"Error calculating compounded investment: {e}")
            return self.investment_percent
    
    def should_reposition_grid(self, current_price: float) -> bool:
        """Check if grid needs repositioning."""
        if self.grid_center_price is None or current_price <= 0:
            return False
        
        if self.grid_center_price <= 0:
            return False
        
        price_move_percent = abs((current_price - self.grid_center_price) / self.grid_center_price) * 100
        reposition_threshold = self.grid_spacing_percent * self.REPOSITION_THRESHOLD_MULTIPLIER
        
        time_since_update = time.time() - self.last_grid_update
        min_time_between_updates = self.MIN_GRID_UPDATE_INTERVAL
        
        if price_move_percent > reposition_threshold and time_since_update > min_time_between_updates:
            logger.info(f"🔄 Grid repositioning needed: price moved {price_move_percent:.2f}%")
            return True
        
        return False
    
    def calculate_grid_levels(self, reposition: bool = False) -> bool:
        """Calculate grid levels with exposure limits and fee-awareness."""
        try:
            current_price = self.exchange.fetch_ticker(self.symbol)['last']
            if not current_price or current_price <= 0:
                logger.error("Invalid current price")
                return False
            
            balances = self.get_balances()
            if not balances:
                return False
            
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
                logger.warning(f"⚠️ Exposure too high ({exposure['current_exposure']:.1f}%), reducing buys")
                bias['buy_weight'] *= 0.5
                bias['sell_weight'] = 1 - bias['buy_weight']
            
            if self.initial_investment == 0:
                self.initial_investment = balances['quote'] + (balances['base'] * current_price)
                self.start_time = datetime.now()
            
            # Cancel existing orders if repositioning
            if reposition:
                logger.info("🔄 Repositioning grid - cancelling unfilled orders")
                self.cancel_all_orders()
            
            self.grid_levels = []
            self.grid_center_price = current_price
            self.last_grid_update = time.time()
            
            # Calculate buy and sell levels
            total_levels = self.grid_levels_count
            buy_levels = max(1, int(total_levels * bias['buy_weight']))
            sell_levels = max(1, int(total_levels * bias['sell_weight']))
            
            logger.info(f"📊 Grid bias: {bias['bias']} (Buy: {buy_levels}, Sell: {sell_levels}, "
                       f"Confidence: {bias.get('confidence', 'N/A')})")
            
            # Calculate order sizes with limits
            max_single_usdt = self.initial_investment * (self.max_single_order_percent / 100)
            usdt_per_buy = min(available_usdt / buy_levels, max_single_usdt) if buy_levels > 0 else 0
            
            # Create BUY levels
            for i in range(1, buy_levels + 1):
                price_level = current_price * (1 - (i * self.grid_spacing_percent / 100))
                
                # Skip invalid price levels early
                if price_level <= 0:
                    logger.warning(f"Skipping buy level {i}: price would be ${price_level:.2f}")
                    continue
                
                # Adjust to S/R
                if sr_levels and sr_levels.get('support'):
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
                
                if sr_levels and sr_levels.get('resistance'):
                    price_level = self._adjust_to_sr_level(price_level, sr_levels['resistance'], 'resistance')
                
                if crypto_per_sell > 0:
                    self.grid_levels.append({
                        'price': round(price_level, 2),
                        'quantity': crypto_per_sell,
                        'type': 'sell',
                        'filled': False,
                        'order_id': None
                    })
            
            logger.info(f"Generated {len(self.grid_levels)} grid levels around ${current_price:.2f}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to calculate grid levels: {e}")
            return False
    
    def _adjust_to_sr_level(self, target_price: float, sr_levels: List[float], level_type: str) -> float:
        """Adjust order to nearby S/R level."""
        if not sr_levels or target_price <= 0:
            return target_price
        
        threshold = target_price * 0.004  # 0.4% threshold
        
        for sr_price in sr_levels[:3]:  # Only check closest 3
            if sr_price > 0 and abs(sr_price - target_price) < threshold:
                logger.debug(f"📍 Adjusted {level_type}: ${target_price:.2f} → ${sr_price:.2f}")
                return sr_price
        
        return target_price
    
    def place_grid_orders(self):
        """Place limit orders at grid levels."""
        if not self.check_volatility():
            logger.info("Volatility outside range, adjusting...")
        
        try:
            # Get minimum order size from exchange
            market = self.exchange.market(self.symbol)
            min_amount = market.get('limits', {}).get('amount', {}).get('min', 0.0001)
            
            for level in self.grid_levels:
                if level['filled'] or level.get('order_id'):
                    continue
                
                price = level['price']
                if price <= 0:
                    continue
                
                quantity = self.exchange.amount_to_precision(self.symbol, level['quantity'])
                quantity = float(quantity)
                
                if quantity <= 0:
                    continue
                
                # Skip if below minimum order size (don't spam errors)
                if quantity < min_amount:
                    continue
                
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
                    logger.info(f"✓ Placed {level['type'].upper()}: {quantity:.6f} @ ${price:.2f}")
                    
                except ccxt.InsufficientFunds as e:
                    logger.warning(f"Insufficient funds for {level['type']} @ ${price}: {e}")
                    break
                except Exception as e:
                    logger.warning(f"Could not place {level['type']} @ ${price}: {e}")
        
        except Exception as e:
            logger.error(f"Failed to place grid orders: {e}")
    
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
                        logger.info(f"Order {order_id} was cancelled externally")
                    
                    # Handle partial fills
                    elif status == 'open' and order_info.get('filled', 0) > 0:
                        self._handle_partial_fill(order_id, order_info)
                
                except Exception as e:
                    logger.warning(f"Error checking order {order_id}: {e}")
        
        except Exception as e:
            logger.error(f"Failed to check orders: {e}")
    
    def _handle_filled_order(self, order_id: str, order_info: Dict[str, Any]):
        """Handle a completely filled order."""
        level = self.active_orders[order_id]['level']
        level['filled'] = True
        
        side = order_info['side']
        amount = float(order_info.get('filled', 0))
        price = float(order_info.get('average') or order_info.get('price', 0))
        
        if amount <= 0 or price <= 0:
            logger.warning(f"Invalid fill data: amount={amount}, price={price}")
            del self.active_orders[order_id]
            return
        
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
            
            logger.info(f"💰 Cycle #{self.cycles_completed} P&L: ${result['pnl']:.2f} "
                       f"(Cost: ${result['cost_basis']:.2f}, Proceeds: ${result['proceeds']:.2f})")
            
            self.log_tax_transaction(
                'SELL', base_currency, amount, price, fee, order_id,
                cost_basis=result['cost_basis'], realized_pnl=result['pnl'],
                notes='Grid sell order filled'
            )
        
        logger.info(f"✓ FILLED: {side.upper()} {amount:.6f} @ ${price:.2f}")
        
        del self.active_orders[order_id]
        self.place_opposite_order(level, price, amount)
    
    def _handle_partial_fill(self, order_id: str, order_info: Dict[str, Any]):
        """Handle partially filled orders."""
        filled = float(order_info.get('filled', 0))
        remaining = float(order_info.get('remaining', 0))
        price = float(order_info.get('average') or order_info.get('price', 0))
        side = order_info['side']
        
        if price <= 0:
            return
        
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
            else:
                # Track partial sell fills immediately to keep position in sync
                self.position_tracker.close_position(new_fill, price, fee)
            
            self.active_orders[order_id]['tracked_filled'] = filled
            logger.info(f"📊 Partial fill: {side.upper()} {new_fill:.6f} @ ${price:.2f} "
                       f"(remaining: {remaining:.6f})")
    
    def _calculate_fee(self, order_info: Dict[str, Any], amount: float, price: float) -> float:
        """Calculate trading fee from order info."""
        fee = 0.0
        if 'fee' in order_info and order_info['fee']:
            fee_info = order_info['fee']
            if fee_info.get('cost'):
                fee_currency = fee_info.get('currency', '')
                if fee_currency in ['USDT', 'USD', 'USDC']:
                    fee = float(fee_info['cost'])
                elif fee_currency == 'BNB':
                    # BNB fees need BNB price conversion
                    try:
                        bnb_ticker = self.exchange.fetch_ticker('BNB/USDT')
                        fee = float(fee_info['cost']) * bnb_ticker['last']
                    except Exception:
                        # Fallback estimate if BNB price unavailable
                        fee = float(fee_info['cost']) * 300
                else:
                    # Assume fee is in base currency
                    fee = float(fee_info['cost']) * price
        
        if fee == 0 and amount > 0 and price > 0:
            fee = (amount * price) * self.fee_rate
        
        return fee
    
    def place_opposite_order(self, filled_level: Dict, fill_price: float, filled_quantity: float):
        """Place opposite order after a grid level fills."""
        try:
            if fill_price <= 0 or filled_quantity <= 0:
                return
            
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
                quantity = proceeds / new_price if new_price > 0 else 0
            
            if quantity <= 0 or new_price <= 0:
                return
            
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
                'linked_to': filled_level['price']
            }
            
            self.grid_levels.append(new_level)
            self.active_orders[order['id']] = {'level': new_level, 'order': order}
            
            logger.info(f"✓ Placed opposite {side.upper()}: {quantity:.6f} @ ${new_price:.2f}")
        
        except Exception as e:
            logger.error(f"Failed to place opposite order: {e}")
    
    def calculate_current_value(self) -> Optional[Dict[str, Any]]:
        """Calculate portfolio value with proper P&L tracking."""
        try:
            balances = self.get_balances()
            if not balances:
                return None
            
            current_price = self.exchange.fetch_ticker(self.symbol)['last']
            if not current_price or current_price <= 0:
                return None
            
            # Get position summary
            position = self.position_tracker.get_summary(current_price)
            
            # Calculate total value including open orders
            open_orders_value = 0.0
            try:
                open_orders = self.exchange.fetch_open_orders(self.symbol)
                for order in open_orders:
                    order_price = float(order.get('price', 0))
                    order_remaining = float(order.get('remaining', 0))
                    if order['side'] == 'buy':
                        open_orders_value += order_remaining * order_price
                    else:
                        open_orders_value += order_remaining * current_price
            except Exception:
                pass
            
            total_value = balances['quote_total'] + (balances['base_total'] * current_price)
            
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
                
                logger.info(
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
            logger.error(f"Failed to calculate portfolio value: {e}")
            return None
    
    def check_stop_loss(self) -> bool:
        """Check stop loss with proper drawdown tracking."""
        portfolio = self.calculate_current_value()
        
        if portfolio:
            # Check percentage loss
            if portfolio['profit_percent'] < -self.stop_loss_percent:
                logger.critical(f"⚠️ STOP LOSS: {portfolio['profit_percent']:.2f}% loss")
                self.emergency_stop()
                return False
            
            # Check drawdown
            if self.max_drawdown > self.stop_loss_percent * 1.5:
                logger.critical(f"⚠️ DRAWDOWN STOP: {self.max_drawdown:.2f}% drawdown")
                self.emergency_stop()
                return False
        
        return True
    
    def evaluate_scenario_change(self) -> Optional[Dict[str, Any]]:
        """Evaluate if scenario change is needed based on current market conditions."""
        try:
            logger.info("🔍 Evaluating market conditions for scenario adjustment...")
            
            # Check if feature is enabled
            if not self.enable_dynamic_scenarios:
                return None
            
            # Check if enough time has passed since last change
            time_since_change = time.time() - self.last_scenario_change
            if time_since_change < self.min_scenario_hold_time:
                remaining = int(self.min_scenario_hold_time - time_since_change)
                logger.info(f"⏳ Scenario hold time not met ({remaining}s remaining)")
                return None
            
            # Get current market analysis
            ticker = self.exchange.fetch_ticker(self.symbol)
            current_price = ticker['last']
            high_24h = ticker['high']
            low_24h = ticker['low']
            
            if current_price <= 0:
                return None
            
            volatility_24h = ((high_24h - low_24h) / current_price) * 100
            
            # Get indicators
            rsi = self.market_analyzer.calculate_rsi_wilder()
            adx_data = self.market_analyzer.calculate_adx()
            bb = self.market_analyzer.calculate_bollinger_bands()
            
            # Get recommended scenario
            recommended_index = self.config_manager._recommend_scenario(
                volatility_24h, rsi, adx_data, bb
            )
            
            if recommended_index is None:
                return None
            
            # Add to recent recommendations for stability
            self.recent_scenario_scores.append(recommended_index)
            if len(self.recent_scenario_scores) > 3:
                self.recent_scenario_scores.pop(0)
            
            # Get consensus from recent recommendations
            if len(self.recent_scenario_scores) >= 2:
                # Use mode (most common recommendation)
                consensus = Counter(self.recent_scenario_scores).most_common(1)[0][0]
            else:
                consensus = recommended_index
            
            # Check if change is significant enough
            if consensus == self.current_scenario_index:
                logger.info(f"✓ Current scenario '{self.scenario_name}' still optimal")
                return None
            
            # Calculate confidence in change
            confidence = self._calculate_change_confidence(
                volatility_24h, rsi, adx_data, consensus
            )
            
            if confidence < self.scenario_change_threshold:
                logger.info(f"📊 Change confidence too low ({confidence:.2f} < {self.scenario_change_threshold})")
                return None
            
            recommended_scenario = self.config_manager.scenarios[consensus]
            
            return {
                'recommended_index': consensus,
                'recommended_scenario': recommended_scenario,
                'current_volatility': volatility_24h,
                'current_rsi': rsi,
                'current_adx': adx_data['adx'] if adx_data else None,
                'confidence': confidence,
                'reason': self._get_change_reason(volatility_24h, rsi, adx_data)
            }
            
        except Exception as e:
            logger.error(f"Error evaluating scenario change: {e}")
            return None

    def _calculate_change_confidence(self, volatility: float, rsi: Optional[float], 
                                    adx: Optional[Dict], target_index: int) -> float:
        """Calculate confidence score for scenario change."""
        confidence = 0.5  # Base confidence
        
        if self.current_scenario_index is None:
            return confidence
            
        current_scenario = self.config_manager.scenarios[self.current_scenario_index]
        target_scenario = self.config_manager.scenarios[target_index]
        
        # Check volatility match
        if 'volatility' in target_scenario['name'].lower():
            if volatility > 5 and 'high' in target_scenario['name'].lower():
                confidence += 0.2
            elif volatility < 2 and 'low' in target_scenario['name'].lower():
                confidence += 0.2
        
        # Check ADX conditions
        if adx and adx.get('adx'):
            adx_value = adx['adx']
            if adx_value > 35:  # Strong trend
                if 'conservative' in target_scenario['name'].lower():
                    confidence += 0.3
                elif 'swing' in target_scenario['name'].lower():
                    confidence += 0.2
            elif adx_value < 20:  # No trend (good for grid)
                if 'scalping' in target_scenario['name'].lower() or 'balanced' in target_scenario['name'].lower():
                    confidence += 0.2
        
        # Check RSI extremes
        if rsi:
            if rsi < 30 or rsi > 70:  # Extreme conditions
                if 'conservative' in target_scenario['name'].lower():
                    confidence += 0.1
        
        # Penalize frequent switching
        time_since_change = time.time() - self.last_scenario_change
        if time_since_change < 7200:  # Less than 2 hours
            confidence *= 0.7
        
        return min(1.0, confidence)

    def _get_change_reason(self, volatility: float, rsi: Optional[float], 
                           adx: Optional[Dict]) -> str:
        """Generate human-readable reason for scenario change."""
        reasons = []
        
        if volatility > 5:
            reasons.append(f"High volatility ({volatility:.1f}%)")
        elif volatility < 2:
            reasons.append(f"Low volatility ({volatility:.1f}%)")
        
        if adx and adx.get('adx'):
            if adx['adx'] > 35:
                reasons.append(f"Strong trend (ADX={adx['adx']:.1f})")
            elif adx['adx'] < 20:
                reasons.append(f"Ranging market (ADX={adx['adx']:.1f})")
        
        if rsi:
            if rsi < 30:
                reasons.append(f"Oversold (RSI={rsi:.1f})")
            elif rsi > 70:
                reasons.append(f"Overbought (RSI={rsi:.1f})")
        
        return ", ".join(reasons) if reasons else "Market conditions changed"

    def switch_scenario(self, new_scenario: Dict[str, Any], index: int, reason: str = ""):
        """Safely switch to a new scenario."""
        try:
            old_scenario_name = self.scenario_name
            
            logger.info("="*60)
            logger.info(f"🔄 SCENARIO CHANGE INITIATED")
            logger.info(f"  From: {old_scenario_name}")
            logger.info(f"  To: {new_scenario['name']}")
            logger.info(f"  Reason: {reason}")
            logger.info("="*60)
            
            # Cancel all active orders
            logger.info("Cancelling active orders...")
            self.cancel_all_orders()
            
            # Wait for orders to clear
            time.sleep(2)
            
            # Load new scenario parameters
            self.load_scenario(new_scenario)
            self.current_scenario_index = index
            self.last_scenario_change = time.time()
            
            # Recalculate grid with new parameters
            logger.info("Recalculating grid with new parameters...")
            if not self.calculate_grid_levels(reposition=True):
                logger.error("Failed to calculate new grid levels")
                # Revert to old scenario on failure
                if self.current_scenario_index is not None:
                    old_scenario = self.config_manager.scenarios[self.current_scenario_index]
                    self.load_scenario(old_scenario)
                return False
            
            # Clear recent recommendations to avoid flip-flopping
            self.recent_scenario_scores = [index]
            
            logger.info(f"✅ Successfully switched to '{new_scenario['name']}' scenario")
            logger.info(f"  New grid: {self.grid_levels_count} levels @ {self.grid_spacing_percent}% spacing")
            
            # Log the change for tracking
            self._log_scenario_change(old_scenario_name, new_scenario['name'], reason)
            
            return True
            
        except Exception as e:
            logger.error(f"Error switching scenario: {e}")
            return False

    def _log_scenario_change(self, from_scenario: str, to_scenario: str, reason: str):
        """Log scenario changes for analysis."""
        try:
            change_log_file = self.data_dir / 'scenario_changes.csv'
            file_exists = change_log_file.exists()
            
            with open(change_log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(['Timestamp', 'From', 'To', 'Reason', 'Cycles', 'P&L'])
                
                current_value = self.calculate_current_value()
                pnl = current_value['profit'] if current_value else 0
                
                writer.writerow([
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    from_scenario,
                    to_scenario,
                    reason,
                    self.cycles_completed,
                    f"{pnl:.2f}"
                ])
                
        except Exception as e:
            logger.warning(f"Could not log scenario change: {e}")

    def check_dynamic_adjustment(self):
        """Check if dynamic scenario adjustment is needed."""
        self.cycles_since_scenario_check += 1
        
        # Only check at specified intervals
        if self.cycles_since_scenario_check < self.cycles_per_scenario_check:
            return

        self.cycles_since_scenario_check = 0

        # Evaluate if change is needed
        evaluation = self.evaluate_scenario_change()

        if evaluation:
            logger.info(f"📈 Scenario change recommended with {evaluation['confidence']:.1%} confidence")

            # Attempt to switch
            success = self.switch_scenario(
                evaluation['recommended_scenario'],
                evaluation['recommended_index'],
                evaluation['reason']
            )

            if not success:
                logger.warning("Scenario switch failed, continuing with current settings")

    def emergency_stop(self):
        """Emergency stop with full reporting."""
        try:
            logger.critical("🛑 EMERGENCY STOP ACTIVATED")
            
            # Cancel all orders
            try:
                open_orders = self.exchange.fetch_open_orders(self.symbol)
                for order in open_orders:
                    self.exchange.cancel_order(order['id'], self.symbol)
                    logger.info(f"Cancelled: {order['id']}")
            except Exception as e:
                logger.error(f"Error cancelling orders: {e}")
            
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
                        if current_price and current_price > 0:
                            fee = float(quantity) * current_price * self.fee_rate
                            
                            result = self.position_tracker.close_position(float(quantity), current_price, fee)
                            
                            self.log_tax_transaction(
                                'SELL', balances['base_currency'], float(quantity),
                                current_price, fee, order['id'],
                                cost_basis=result['cost_basis'], realized_pnl=result['pnl'],
                                notes='Emergency stop - market sell'
                            )
                            
                            logger.critical(f"Emergency sold {quantity} @ ${current_price:.2f}")
                except Exception as e:
                    logger.error(f"Error in emergency sell: {e}")
            
            # Final summary
            self._print_final_summary()
            
        except Exception as e:
            logger.error(f"Error during emergency stop: {e}")
    
    def _print_final_summary(self):
        """Print final trading session summary."""
        try:
            current_price = self.exchange.fetch_ticker(self.symbol)['last']
            if not current_price or current_price <= 0:
                current_price = 0.0
            
            position = self.position_tracker.get_summary(current_price)
            
            runtime = datetime.now() - self.start_time if self.start_time else None
            
            logger.info("=" * 60)
            logger.info("TRADING SESSION SUMMARY")
            logger.info("=" * 60)
            logger.info(f"Strategy: {self.scenario_name}")
            if runtime:
                logger.info(f"Runtime: {runtime}")
            logger.info(f"Cycles completed: {self.cycles_completed}")
            logger.info(f"Initial investment: ${self.initial_investment:.2f}")
            logger.info(f"Realized P&L: ${position['realized_pnl']:.2f}")
            logger.info(f"Total fees paid: ${position['total_fees']:.2f}")
            logger.info(f"Max drawdown: {self.max_drawdown:.2f}%")
            logger.info("=" * 60)
        except Exception as e:
            logger.error(f"Error printing summary: {e}")
    
    def cancel_all_orders(self):
        """Cancel all active orders."""
        try:
            open_orders = self.exchange.fetch_open_orders(self.symbol)
            for order in open_orders:
                try:
                    self.exchange.cancel_order(order['id'], self.symbol)
                except Exception as e:
                    logger.warning(f"Could not cancel {order['id']}: {e}")
            
            # Clear tracked orders
            for order_id in list(self.active_orders.keys()):
                level = self.active_orders[order_id]['level']
                level['order_id'] = None
            
            self.active_orders = {}
            logger.info("All orders cancelled")
        except Exception as e:
            logger.error(f"Failed to cancel orders: {e}")

    def run(self):
        """Main bot loop with dynamic scenario adjustment."""
        logger.info(f"🤖 Starting Smart Grid Trading Bot v14.1 - {self.scenario_name}")
        logger.info(f"📊 Grid: {self.grid_levels_count} levels @ {self.grid_spacing_percent}% spacing")
        logger.info(f"💰 Fee rate: {self.fee_rate*100:.3f}%")
        
        # Show dynamic adjustment status
        if self.enable_dynamic_scenarios:
            logger.info(f"🔄 Dynamic adjustment: Every {self.cycles_per_scenario_check} cycles")
        else:
            logger.info("🔄 Dynamic adjustment: Disabled")
        
        # Store initial scenario index
        for i, scenario in enumerate(self.config_manager.scenarios):
            if scenario['name'] == self.scenario_name:
                self.current_scenario_index = i
                break
        
        balances = self.get_balances()
        if balances:
            logger.info(f"Starting: {balances['quote']:.2f} {balances['quote_currency']}, "
                       f"{balances['base']:.6f} {balances['base_currency']}")
        
        if not self.calculate_grid_levels():
            logger.error("Failed to calculate grid levels")
            return
        
        try:
            while True:
                logger.info("--- 🔄 Cycle start ---")
                
                try:
                    current_price = self.exchange.fetch_ticker(self.symbol)['last']
                    if not current_price or current_price <= 0:
                        logger.warning("Could not fetch current price, retrying...")
                        time.sleep(self.check_interval)
                        continue
                except Exception as e:
                    logger.error(f"Error fetching price: {e}")
                    time.sleep(self.check_interval)
                    continue
                
                # Check trend filter
                if not self.check_trend_filter():
                    logger.info(f"💤 Waiting for trend to weaken... ({self.check_interval}s)")
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
                
                # Check for dynamic scenario adjustment
                if self.cycles_completed > 0 and self.enable_dynamic_scenarios:
                    self.check_dynamic_adjustment()
                
                # Status update
                self.calculate_current_value()
                
                logger.info(f"💤 Sleeping {self.check_interval}s\n")
                time.sleep(self.check_interval)
        
        except KeyboardInterrupt:
            logger.info("🛑 Stopped by user")
            self.cancel_all_orders()
            self._print_final_summary()
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            self.emergency_stop()

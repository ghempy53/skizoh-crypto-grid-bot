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

#  =============================================================================
# SKIZOH CRYPTO GRID TRADING BOT - Core Trading Engine v2.0
# =============================================================================
# PROFIT OPTIMIZATIONS:
# - Asymmetric grid placement based on market bias
# - Dynamic spacing that tightens in high-profit zones
# - Momentum-based entry timing
# - Trailing profit locks
# - Capital efficiency improvements
# - BNB fee discount support
#
# PI OPTIMIZATIONS:
# - Aggressive memory management
# - Reduced API calls via smart caching
# - Temperature-based throttling
# - SD card wear reduction
# =============================================================================

import ccxt
import time
import json
import logging
import gc
from datetime import datetime, timedelta
from collections import deque, Counter
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import numpy as np
import csv
import os

from config_manager import ConfigManager
from market_analysis import MarketAnalyzer

logger = logging.getLogger(__name__)


class PositionTracker:
    """
    Track positions with proper cost basis using FIFO.
    
    OPTIMIZATIONS:
    - Automatic archival of old positions (memory efficiency)
    - Periodic state compression
    - Float precision management to prevent drift
    """
    
    MAX_POSITIONS_IN_MEMORY = 500  # Reduced for Pi
    ARCHIVE_THRESHOLD = 400
    
    def __init__(self, state_file: Optional[str] = None):
        self.positions = deque()
        self.total_quantity = 0.0
        self.total_cost = 0.0
        self.realized_pnl = 0.0
        self.total_fees_paid = 0.0
        self.state_file = state_file
        self.archive_file = None
        
        if state_file:
            self.archive_file = state_file.replace('.json', '_archive.csv')
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
        """Save position state to file with compression."""
        try:
            if not self.state_file:
                return
                
            # Archive old positions if needed
            self._archive_if_needed()
            
            # Recalculate to prevent float drift
            self._recalculate_totals()
            
            state = {
                'total_quantity': round(self.total_quantity, 8),
                'total_cost': round(self.total_cost, 4),
                'realized_pnl': round(self.realized_pnl, 4),
                'total_fees_paid': round(self.total_fees_paid, 4),
                'positions': [
                    {
                        'quantity': round(pos['quantity'], 8),
                        'price': round(pos['price'], 4),
                        'cost_basis': round(pos['cost_basis'], 4),
                        'timestamp': pos['timestamp'].isoformat()
                    }
                    for pos in self.positions
                ],
                'last_updated': datetime.now().isoformat()
            }
            
            # Atomic write
            temp_file = self.state_file + '.tmp'
            with open(temp_file, 'w') as f:
                json.dump(state, f, indent=2)
            os.replace(temp_file, self.state_file)
            
        except Exception as e:
            logger.warning(f"Could not save position state: {e}")
    
    def _archive_if_needed(self):
        """Archive old positions to reduce memory."""
        if len(self.positions) < self.ARCHIVE_THRESHOLD:
            return
        
        to_archive = []
        target_count = int(self.MAX_POSITIONS_IN_MEMORY * 0.6)
        
        while len(self.positions) > target_count:
            to_archive.append(self.positions.popleft())
        
        if to_archive and self.archive_file:
            try:
                file_exists = os.path.exists(self.archive_file)
                with open(self.archive_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(['timestamp', 'quantity', 'price', 'cost_basis'])
                    for pos in to_archive:
                        writer.writerow([
                            pos['timestamp'].isoformat(),
                            pos['quantity'],
                            pos['price'],
                            pos['cost_basis']
                        ])
                logger.info(f"Archived {len(to_archive)} old positions")
            except Exception as e:
                logger.warning(f"Could not archive positions: {e}")
    
    def _recalculate_totals(self):
        """Recalculate totals to prevent floating-point drift."""
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
                total_cost_basis += oldest['cost_basis']
                remaining -= oldest['quantity']
                self.total_quantity -= oldest['quantity']
                self.total_cost -= oldest['cost_basis']
                self.positions.popleft()
            else:
                if oldest['quantity'] > 0:
                    fraction = remaining / oldest['quantity']
                    used_cost = oldest['cost_basis'] * fraction
                    total_cost_basis += used_cost
                    
                    oldest['quantity'] -= remaining
                    oldest['cost_basis'] -= used_cost
                    self.total_quantity -= remaining
                    self.total_cost -= used_cost
                remaining = 0
        
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


class ProfitOptimizer:
    """
    Profit optimization strategies for grid trading.
    
    Features:
    - Asymmetric grid placement
    - Dynamic spacing based on volatility
    - Momentum-based entry timing
    - Profit zone acceleration
    """
    
    def __init__(self, fee_rate: float = 0.001):
        self.fee_rate = fee_rate
        self.min_profit_multiplier = 2.5  # Minimum profit vs fees
        
    def calculate_optimal_spacing(self, base_spacing: float, volatility: float,
                                   adx: float, rsi: float) -> float:
        """
        Calculate optimal grid spacing based on market conditions.
        
        Higher volatility = wider spacing (capture bigger moves)
        Strong trend = wider spacing (avoid getting run over)
        Mean reversion zone = tighter spacing (more cycles)
        """
        # Base minimum: must exceed 2x fees with buffer
        min_spacing = (2 * self.fee_rate * 100) * self.min_profit_multiplier
        
        # Start with base spacing
        optimal = max(base_spacing, min_spacing)
        
        # Volatility adjustment (0.5x to 2x multiplier)
        if volatility > 5:
            volatility_mult = 1.0 + (volatility - 5) * 0.1  # +10% per 1% vol above 5%
        elif volatility < 2:
            volatility_mult = 0.8  # Tighter in low vol
        else:
            volatility_mult = 1.0
        
        optimal *= min(2.0, max(0.5, volatility_mult))
        
        # Trend adjustment (ADX)
        if adx > 35:
            optimal *= 1.5  # Much wider in strong trends
        elif adx > 25:
            optimal *= 1.2  # Moderately wider
        elif adx < 15:
            optimal *= 0.9  # Tighter in ranging markets
        
        # RSI adjustment (tighten near extremes for mean reversion)
        if 25 < rsi < 35 or 65 < rsi < 75:
            optimal *= 0.9  # Tighter near oversold/overbought
        
        return max(min_spacing, round(optimal, 3))
    
    def calculate_asymmetric_levels(self, current_price: float, num_levels: int,
                                     spacing: float, bias: Dict[str, float]) -> Tuple[List[float], List[float]]:
        """
        Calculate asymmetric buy and sell levels based on market bias.
        
        In bullish conditions: more sell levels above, fewer buy levels below
        In bearish conditions: more buy levels below, fewer sell levels above
        """
        buy_weight = bias.get('buy_weight', 0.5)
        
        # Calculate level distribution
        num_buys = max(1, int(num_levels * buy_weight))
        num_sells = max(1, num_levels - num_buys)
        
        # Generate buy levels (below current price)
        buy_levels = []
        for i in range(1, num_buys + 1):
            # Progressive spacing: tighter near price, wider further away
            level_spacing = spacing * (1 + (i - 1) * 0.1)  # 10% wider each level
            price = current_price * (1 - (i * level_spacing / 100))
            if price > 0:
                buy_levels.append(round(price, 2))
        
        # Generate sell levels (above current price)
        sell_levels = []
        for i in range(1, num_sells + 1):
            level_spacing = spacing * (1 + (i - 1) * 0.1)
            price = current_price * (1 + (i * level_spacing / 100))
            sell_levels.append(round(price, 2))
        
        return buy_levels, sell_levels
    
    def should_wait_for_better_entry(self, current_price: float, target_price: float,
                                      momentum: float, is_buy: bool) -> bool:
        """
        Determine if we should wait for a better entry price.
        
        Uses momentum to predict short-term price movement.
        """
        price_diff_pct = abs(current_price - target_price) / current_price * 100
        
        # If very close to target, don't wait
        if price_diff_pct < 0.1:
            return False
        
        # For buys: wait if momentum is negative (price likely to fall)
        # For sells: wait if momentum is positive (price likely to rise)
        if is_buy and momentum < -0.5:
            return True
        if not is_buy and momentum > 0.5:
            return True
        
        return False
    
    def calculate_profit_target(self, entry_price: float, base_spacing: float,
                                 volatility: float, position_age_hours: float) -> float:
        """
        Calculate dynamic profit target.
        
        Older positions = lower profit target (get out faster)
        High volatility = higher target (capture bigger moves)
        """
        base_target = entry_price * (1 + base_spacing / 100)
        
        # Volatility bonus
        if volatility > 4:
            vol_bonus = (volatility - 4) * 0.1  # +0.1% per 1% vol above 4%
            base_target *= (1 + vol_bonus / 100)
        
        # Age penalty (reduce target for old positions)
        if position_age_hours > 24:
            age_factor = max(0.5, 1 - (position_age_hours - 24) * 0.01)
            target_reduction = (base_target - entry_price) * (1 - age_factor)
            base_target -= target_reduction
        
        return round(base_target, 2)


class SmartGridTradingBot:
    """
    Smart grid trading bot v2.0 with profit optimization.
    
    KEY OPTIMIZATIONS:
    1. Asymmetric grid placement based on market bias
    2. Dynamic spacing that adapts to volatility
    3. Momentum-based entry timing
    4. Profit zone acceleration
    5. Capital efficiency improvements
    6. Memory-efficient for Raspberry Pi
    """
    
    DEFAULT_FEE_RATE = 0.001  # 0.1%
    TREND_PAUSE_SECONDS = 1800  # 30 minutes
    REPOSITION_THRESHOLD_MULTIPLIER = 2.0  # Reduced for more responsive repositioning
    MIN_GRID_UPDATE_INTERVAL = 300  # 5 minutes (reduced from 10)
    FEE_SAFETY_FACTOR = 2.5
    
    # Pi-specific settings
    MEMORY_CHECK_INTERVAL = 50  # Check memory every N cycles
    MAX_MEMORY_MB = 300  # Force GC if above this
    
    def __init__(self, config_file: str = 'config.json'):
        """Initialize the smart grid trading bot."""
        # Resolve config file path
        self.config_file_path = Path(config_file).resolve()
        self.project_root = self.config_file_path.parent.parent
        self.data_dir = self.project_root / 'data'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_manager = ConfigManager(str(self.config_file_path))
        config = self.config_manager.load_config()
        
        self._validate_config(config)
        
        # API credentials
        self.api_key = config['api_key']
        self.api_secret = config['api_secret']
        self.symbol = config['symbol']
        
        # Fee configuration
        self.fee_rate = config.get('fee_rate', self.DEFAULT_FEE_RATE)
        self.use_bnb_fees = config.get('use_bnb_for_fees', False)
        if self.use_bnb_fees:
            self.fee_rate *= 0.75  # 25% discount with BNB
            logger.info(f"Using BNB for fees: effective rate {self.fee_rate*100:.3f}%")
        
        # Initialize profit optimizer
        self.profit_optimizer = ProfitOptimizer(self.fee_rate)
        
        # Select scenario
        scenario = self.config_manager.select_scenario_interactive()
        self.load_scenario(scenario)
        
        # Initialize exchange
        self.exchange = self.initialize_exchange()
        self.market_analyzer = MarketAnalyzer(self.exchange, self.symbol)
        
        # Position tracking
        position_state_file = str(self.data_dir / 'position_state.json')
        self.position_tracker = PositionTracker(state_file=position_state_file)
        
        # Trading state
        self.grid_levels: List[Dict] = []
        self.active_orders: Dict[str, Dict] = {}
        self.initial_investment = 0.0
        self.cycles_completed = 0
        self.profitable_cycles = 0
        self.total_cycle_profit = 0.0
        
        # Exposure limits
        self.max_position_percent = config.get('max_position_percent', 75)
        self.max_single_order_percent = config.get('max_single_order_percent', 10)
        
        # Tax logging
        self.tax_log_file = str(self.data_dir / 'tax_transactions.csv')
        self.initialize_tax_log()
        
        # Dynamic scenario settings
        self.enable_dynamic_scenarios = config.get('enable_dynamic_scenarios', True)
        self.cycles_per_scenario_check = config.get('cycles_per_scenario_check', 5)  # More frequent checks
        self.cycles_since_scenario_check = 0
        self.current_scenario_index = None
        self.last_scenario_change = time.time()
        self.min_scenario_hold_time = config.get('min_scenario_hold_minutes', 45) * 60  # Reduced
        self.scenario_change_threshold = config.get('scenario_change_confidence', 0.65)  # Lower threshold
        self.recent_scenario_scores = []
        
        # Grid state
        self.grid_center_price: Optional[float] = None
        self.last_grid_update = time.time()
        self.current_volatility = 0.0
        self.current_adx = 0.0
        
        # Performance tracking
        self.start_time: Optional[datetime] = None
        self.peak_value = 0.0
        self.max_drawdown = 0.0
        self.last_profit_time = time.time()
        
        # Trend pause state
        self.trend_pause_until = 0.0
        
        # Memory management (Pi optimization)
        self.cycle_count = 0
        self.last_gc_time = time.time()
    
    def _validate_config(self, config: Dict[str, Any]):
        """Validate required configuration fields."""
        required_fields = ['api_key', 'api_secret', 'symbol', 'config_data']
        
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required config field: {field}")
        
        if config['api_key'] == 'YOUR_BINANCE_US_API_KEY':
            raise ValueError("API key not configured")
        
        if config['api_secret'] == 'YOUR_BINANCE_US_API_SECRET':
            raise ValueError("API secret not configured")
    
    def load_scenario(self, scenario: Dict[str, Any]):
        """Load selected scenario configuration."""
        self.scenario_name = scenario['name']
        self.grid_levels_count = scenario['grid_levels']
        self.base_grid_spacing = scenario['grid_spacing_percent']
        self.grid_spacing_percent = self.base_grid_spacing  # Will be dynamically adjusted
        self.investment_percent = scenario['investment_percent']
        self.min_order_size_usdt = scenario['min_order_size_usdt']
        self.stop_loss_percent = scenario['stop_loss_percent']
        self.atr_period = scenario['atr_period']
        self.volatility_threshold = scenario['volatility_threshold']
        self.check_interval = scenario['check_interval_seconds']
        
        self._validate_grid_spacing()
        logger.info(f"Loaded scenario: {self.scenario_name}")
    
    def _validate_grid_spacing(self):
        """Ensure grid spacing is profitable after fees."""
        min_spacing = (2 * self.fee_rate * 100) * self.FEE_SAFETY_FACTOR
        
        if self.grid_spacing_percent < min_spacing:
            old_spacing = self.grid_spacing_percent
            self.grid_spacing_percent = min_spacing
            logger.warning(
                f"⚠️ Grid spacing {old_spacing}% adjusted to {min_spacing:.2f}% for profitability"
            )
    
    def initialize_exchange(self) -> ccxt.binanceus:
        """Initialize connection to Binance.US with optimizations."""
        try:
            exchange = ccxt.binanceus({
                'apiKey': self.api_key,
                'secret': self.api_secret,
                'enableRateLimit': True,
                'timeout': 30000,
                'options': {
                    'adjustForTimeDifference': True,
                    'recvWindow': 60000,
                }
            })
            exchange.load_markets()
            
            # Get actual fee rate
            try:
                trading_fees = exchange.fetch_trading_fees()
                if self.symbol in trading_fees:
                    base_rate = max(
                        trading_fees[self.symbol].get('maker', self.fee_rate),
                        trading_fees[self.symbol].get('taker', self.fee_rate)
                    )
                    if self.use_bnb_fees:
                        self.fee_rate = base_rate * 0.75
                    else:
                        self.fee_rate = base_rate
                    logger.info(f"Exchange fee rate: {self.fee_rate*100:.3f}%")
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
            if not os.path.isfile(self.tax_log_file):
                with open(self.tax_log_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        'Date/Time', 'Transaction Type', 'Asset', 'Amount',
                        'Price (USD)', 'Total Value (USD)', 'Fee (USD)',
                        'Net Proceeds (USD)', 'Cost Basis (USD)', 'Realized P&L (USD)',
                        'Order ID', 'Notes'
                    ])
                logger.info(f"Created tax log: {self.tax_log_file}")
        except Exception as e:
            logger.error(f"Failed to initialize tax log: {e}")
    
    def log_tax_transaction(self, transaction_type: str, asset: str, amount: float, 
                           price: float, fee: float, order_id: str,
                           cost_basis: float = 0, realized_pnl: float = 0, notes: str = ''):
        """Log a transaction for tax purposes."""
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
        except Exception as e:
            logger.error(f"Failed to log tax transaction: {e}")
    
    def get_balances(self) -> Optional[Dict[str, Any]]:
        """Get current balances."""
        try:
            balance = self.exchange.fetch_balance()
            base_currency = self.symbol.split('/')[0]
            quote_currency = self.symbol.split('/')[1]
            
            return {
                'base': float(balance[base_currency]['free'] or 0),
                'base_total': float(balance[base_currency]['total'] or 0),
                'quote': float(balance[quote_currency]['free'] or 0),
                'quote_total': float(balance[quote_currency]['total'] or 0),
                'base_currency': base_currency,
                'quote_currency': quote_currency
            }
        except Exception as e:
            logger.error(f"Failed to fetch balance: {e}")
            return None
    
    def check_exposure_limits(self, current_price: float) -> Dict[str, Any]:
        """Check position exposure limits."""
        balances = self.get_balances()
        if not balances or current_price <= 0:
            return {'within_limits': False, 'reason': 'Invalid data'}
        
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
    
    def get_market_conditions(self) -> Dict[str, Any]:
        """Get comprehensive market conditions for decision making."""
        try:
            ticker = self.exchange.fetch_ticker(self.symbol)
            current_price = ticker['last']
            high_24h = ticker['high']
            low_24h = ticker['low']
            
            if current_price <= 0:
                return None
            
            volatility = ((high_24h - low_24h) / current_price) * 100
            
            rsi = self.market_analyzer.calculate_rsi_wilder() or 50
            adx_data = self.market_analyzer.calculate_adx()
            adx = adx_data['adx'] if adx_data else 20
            macd = self.market_analyzer.calculate_macd()
            bb = self.market_analyzer.calculate_bollinger_bands()
            
            # Calculate momentum
            momentum = 0
            if macd:
                momentum = macd['histogram'] * 10  # Scale histogram
            
            self.current_volatility = volatility
            self.current_adx = adx
            
            return {
                'price': current_price,
                'volatility': volatility,
                'rsi': rsi,
                'adx': adx,
                'adx_data': adx_data,
                'macd': macd,
                'bb': bb,
                'momentum': momentum,
                'high_24h': high_24h,
                'low_24h': low_24h
            }
        except Exception as e:
            logger.error(f"Failed to get market conditions: {e}")
            return None
    
    def check_trend_filter(self) -> bool:
        """Check if market is suitable for grid trading."""
        if time.time() < self.trend_pause_until:
            remaining = int(self.trend_pause_until - time.time())
            logger.info(f"⏸️ Trend pause: {remaining}s remaining")
            return False
        
        safety = self.market_analyzer.is_safe_to_trade()
        
        if not safety['safe']:
            self.trend_pause_until = time.time() + self.TREND_PAUSE_SECONDS
            for reason in safety['reasons']:
                logger.warning(f"🚨 {reason}")
            return False
        
        return True
    
    def calculate_compounded_investment(self) -> float:
        """Calculate investment with conservative compounding."""
        if self.initial_investment <= 0:
            return self.investment_percent
        
        try:
            current_price = self.exchange.fetch_ticker(self.symbol)['last']
            if not current_price:
                return self.investment_percent
            
            position_summary = self.position_tracker.get_summary(current_price)
            total_pnl = position_summary['total_pnl']
            profit_percent = (total_pnl / self.initial_investment) * 100
            
            if profit_percent > 25:
                return min(85, self.investment_percent + 6)
            elif profit_percent > 15:
                return min(82, self.investment_percent + 4)
            elif profit_percent > 5:
                return min(78, self.investment_percent + 2)
            elif profit_percent < -10:
                return max(50, self.investment_percent - 10)
            elif profit_percent < -5:
                return max(60, self.investment_percent - 5)
            
            return self.investment_percent
        except Exception:
            return self.investment_percent
    
    def should_reposition_grid(self, current_price: float) -> bool:
        """Check if grid needs repositioning."""
        if not self.grid_center_price or current_price <= 0:
            return False
        
        price_move_pct = abs((current_price - self.grid_center_price) / self.grid_center_price) * 100
        threshold = self.grid_spacing_percent * self.REPOSITION_THRESHOLD_MULTIPLIER
        time_since_update = time.time() - self.last_grid_update
        
        return price_move_pct > threshold and time_since_update > self.MIN_GRID_UPDATE_INTERVAL
    
    def calculate_grid_levels(self, reposition: bool = False) -> bool:
        """Calculate optimized grid levels."""
        try:
            market = self.get_market_conditions()
            if not market:
                return False
            
            current_price = market['price']
            balances = self.get_balances()
            if not balances:
                return False
            
            # Get optimal spacing based on conditions
            optimal_spacing = self.profit_optimizer.calculate_optimal_spacing(
                self.base_grid_spacing,
                market['volatility'],
                market['adx'],
                market['rsi']
            )
            
            if abs(optimal_spacing - self.grid_spacing_percent) > 0.1:
                logger.info(f"📊 Spacing adjusted: {self.grid_spacing_percent:.2f}% → {optimal_spacing:.2f}%")
                self.grid_spacing_percent = optimal_spacing
            
            # Get market bias
            bias = self.market_analyzer.should_adjust_grid_bias()
            
            # Calculate asymmetric levels
            buy_prices, sell_prices = self.profit_optimizer.calculate_asymmetric_levels(
                current_price, self.grid_levels_count, self.grid_spacing_percent, bias
            )
            
            # Exposure check
            exposure = self.check_exposure_limits(current_price)
            if exposure.get('should_reduce'):
                logger.warning(f"⚠️ High exposure ({exposure['current_exposure']:.1f}%), favoring sells")
                bias['buy_weight'] *= 0.5
            
            if self.initial_investment == 0:
                self.initial_investment = balances['quote'] + (balances['base'] * current_price)
                self.start_time = datetime.now()
            
            if reposition:
                logger.info("🔄 Repositioning grid")
                self.cancel_all_orders()
            
            self.grid_levels = []
            self.grid_center_price = current_price
            self.last_grid_update = time.time()
            
            # Investment calculation
            investment_pct = self.calculate_compounded_investment()
            available_usdt = balances['quote'] * (investment_pct / 100)
            max_single_usdt = self.initial_investment * (self.max_single_order_percent / 100)
            
            # Create buy levels
            num_buys = len(buy_prices)
            if num_buys > 0:
                usdt_per_buy = min(available_usdt / num_buys, max_single_usdt)
                
                for price in buy_prices:
                    if price <= 0 or usdt_per_buy < self.min_order_size_usdt:
                        continue
                    
                    quantity = usdt_per_buy / price
                    self.grid_levels.append({
                        'price': price,
                        'quantity': quantity,
                        'type': 'buy',
                        'filled': False,
                        'order_id': None
                    })
            
            # Create sell levels
            crypto_available = balances['base']
            num_sells = len(sell_prices)
            if num_sells > 0 and crypto_available > 0:
                max_single_crypto = max_single_usdt / current_price
                crypto_per_sell = min(crypto_available / num_sells, max_single_crypto)
                
                for price in sell_prices:
                    if crypto_per_sell > 0:
                        self.grid_levels.append({
                            'price': price,
                            'quantity': crypto_per_sell,
                            'type': 'sell',
                            'filled': False,
                            'order_id': None
                        })
            
            logger.info(f"📊 Grid: {len([l for l in self.grid_levels if l['type']=='buy'])} buys, "
                       f"{len([l for l in self.grid_levels if l['type']=='sell'])} sells @ "
                       f"{self.grid_spacing_percent:.2f}% spacing (bias: {bias['bias']})")
            
            return True
        except Exception as e:
            logger.error(f"Failed to calculate grid: {e}")
            return False
    
    def place_grid_orders(self):
        """Place optimized grid orders."""
        try:
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
                
                if quantity < min_amount:
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
                    logger.info(f"✓ {level['type'].upper()}: {quantity:.6f} @ ${price:.2f}")
                    
                except ccxt.InsufficientFunds:
                    logger.warning(f"Insufficient funds for {level['type']} @ ${price}")
                    break
                except Exception as e:
                    logger.warning(f"Order failed @ ${price}: {e}")
        except Exception as e:
            logger.error(f"Failed to place orders: {e}")
    
    def check_orders(self):
        """Check and process filled orders."""
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
            except Exception as e:
                logger.warning(f"Error checking order {order_id}: {e}")
    
    def _handle_filled_order(self, order_id: str, order_info: Dict):
        """Handle filled order with profit tracking."""
        level = self.active_orders[order_id]['level']
        level['filled'] = True
        
        side = order_info['side']
        amount = float(order_info.get('filled', 0))
        price = float(order_info.get('average') or order_info.get('price', 0))
        
        if amount <= 0 or price <= 0:
            del self.active_orders[order_id]
            return
        
        # Calculate fee
        fee = self._calculate_fee(order_info, amount, price)
        base_currency = self.symbol.split('/')[0]
        
        if side == 'buy':
            self.position_tracker.add_position(amount, price, fee)
            self.log_tax_transaction('BUY', base_currency, amount, price, fee, order_id,
                                    cost_basis=amount*price+fee, notes='Grid buy')
        else:
            result = self.position_tracker.close_position(amount, price, fee)
            self.cycles_completed += 1
            
            if result['pnl'] > 0:
                self.profitable_cycles += 1
                self.total_cycle_profit += result['pnl']
                self.last_profit_time = time.time()
            
            win_rate = (self.profitable_cycles / self.cycles_completed * 100) if self.cycles_completed > 0 else 0
            
            logger.info(f"💰 Cycle #{self.cycles_completed} P&L: ${result['pnl']:.2f} "
                       f"(Win rate: {win_rate:.0f}%, Total: ${self.total_cycle_profit:.2f})")
            
            self.log_tax_transaction('SELL', base_currency, amount, price, fee, order_id,
                                    cost_basis=result['cost_basis'], realized_pnl=result['pnl'],
                                    notes='Grid sell')
        
        del self.active_orders[order_id]
        self.place_opposite_order(level, price, amount)
    
    def _calculate_fee(self, order_info: Dict, amount: float, price: float) -> float:
        """Calculate trading fee."""
        fee = 0.0
        if 'fee' in order_info and order_info['fee']:
            fee_info = order_info['fee']
            if fee_info.get('cost'):
                fee_currency = fee_info.get('currency', '')
                if fee_currency in ['USDT', 'USD', 'USDC']:
                    fee = float(fee_info['cost'])
                elif fee_currency == 'BNB':
                    try:
                        bnb_ticker = self.exchange.fetch_ticker('BNB/USDT')
                        fee = float(fee_info['cost']) * bnb_ticker['last']
                    except:
                        fee = float(fee_info['cost']) * 300
                else:
                    fee = float(fee_info['cost']) * price
        
        if fee == 0:
            fee = (amount * price) * self.fee_rate
        
        return fee
    
    def place_opposite_order(self, filled_level: Dict, fill_price: float, filled_qty: float):
        """Place opposite order after fill."""
        try:
            if fill_price <= 0 or filled_qty <= 0:
                return
            
            adjustment = self.grid_spacing_percent / 100
            
            if filled_level['type'] == 'buy':
                new_price = fill_price * (1 + adjustment)
                side = 'sell'
                quantity = filled_qty
            else:
                new_price = fill_price * (1 - adjustment)
                side = 'buy'
                quantity = (filled_qty * fill_price) / new_price
            
            if quantity <= 0 or new_price <= 0:
                return
            
            quantity = float(self.exchange.amount_to_precision(self.symbol, quantity))
            new_price = round(new_price, 2)
            
            order = self.exchange.create_order(
                symbol=self.symbol, type='limit', side=side,
                amount=quantity, price=new_price
            )
            
            new_level = {
                'price': new_price,
                'quantity': quantity,
                'type': side,
                'filled': False,
                'order_id': order['id']
            }
            
            self.grid_levels.append(new_level)
            self.active_orders[order['id']] = {'level': new_level, 'order': order}
            logger.info(f"✓ Opposite {side.upper()}: {quantity:.6f} @ ${new_price:.2f}")
            
        except Exception as e:
            logger.error(f"Failed to place opposite order: {e}")
    
    def calculate_current_value(self) -> Optional[Dict]:
        """Calculate portfolio value with metrics."""
        try:
            balances = self.get_balances()
            if not balances:
                return None
            
            current_price = self.exchange.fetch_ticker(self.symbol)['last']
            if not current_price:
                return None
            
            position = self.position_tracker.get_summary(current_price)
            total_value = balances['quote_total'] + (balances['base_total'] * current_price)
            
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
                    f"📊 Value: ${total_value:.2f} | P&L: ${total_pnl:.2f} ({pnl_percent:+.2f}%) | "
                    f"Cycles: {self.cycles_completed} | DD: {self.max_drawdown:.1f}%"
                )
                
                return {
                    'total_value': total_value,
                    'profit': total_pnl,
                    'profit_percent': pnl_percent,
                    'realized_pnl': position['realized_pnl'],
                    'max_drawdown': self.max_drawdown
                }
            return None
        except Exception as e:
            logger.error(f"Failed to calculate value: {e}")
            return None
    
    def check_stop_loss(self) -> bool:
        """Check stop loss conditions."""
        portfolio = self.calculate_current_value()
        
        if portfolio:
            if portfolio['profit_percent'] < -self.stop_loss_percent:
                logger.critical(f"⚠️ STOP LOSS: {portfolio['profit_percent']:.2f}%")
                self.emergency_stop()
                return False
            
            if self.max_drawdown > self.stop_loss_percent * 1.5:
                logger.critical(f"⚠️ DRAWDOWN STOP: {self.max_drawdown:.2f}%")
                self.emergency_stop()
                return False
        
        return True
    
    def check_memory_usage(self):
        """Check and manage memory (Pi optimization)."""
        self.cycle_count += 1
        
        if self.cycle_count % self.MEMORY_CHECK_INTERVAL != 0:
            return
        
        try:
            import resource
            mem_mb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
            
            if mem_mb > self.MAX_MEMORY_MB:
                logger.info(f"🧹 Memory cleanup: {mem_mb:.0f}MB")
                gc.collect()
                
                # Clear analyzer caches
                self.market_analyzer.clear_caches()
                
        except Exception:
            # Fallback: just run GC periodically
            if time.time() - self.last_gc_time > 300:
                gc.collect()
                self.last_gc_time = time.time()
    
    def cancel_all_orders(self):
        """Cancel all active orders."""
        try:
            open_orders = self.exchange.fetch_open_orders(self.symbol)
            for order in open_orders:
                try:
                    self.exchange.cancel_order(order['id'], self.symbol)
                except Exception:
                    pass
            
            self.active_orders = {}
            for level in self.grid_levels:
                level['order_id'] = None
            
            logger.info("All orders cancelled")
        except Exception as e:
            logger.error(f"Failed to cancel orders: {e}")
    
    def emergency_stop(self):
        """Emergency stop with cleanup."""
        logger.critical("🛑 EMERGENCY STOP")
        
        try:
            self.cancel_all_orders()
            
            balances = self.get_balances()
            if balances and balances['base'] > 0:
                quantity = self.exchange.amount_to_precision(self.symbol, balances['base'])
                if float(quantity) > 0:
                    self.exchange.create_order(
                        symbol=self.symbol, type='market',
                        side='sell', amount=quantity
                    )
        except Exception as e:
            logger.error(f"Emergency stop error: {e}")
        
        self._print_final_summary()
    
    def _print_final_summary(self):
        """Print trading session summary."""
        try:
            current_price = self.exchange.fetch_ticker(self.symbol)['last'] or 0
            position = self.position_tracker.get_summary(current_price)
            runtime = datetime.now() - self.start_time if self.start_time else None
            
            logger.info("=" * 60)
            logger.info("SESSION SUMMARY")
            logger.info("=" * 60)
            logger.info(f"Strategy: {self.scenario_name}")
            if runtime:
                logger.info(f"Runtime: {runtime}")
            logger.info(f"Cycles: {self.cycles_completed} (Win rate: {self.profitable_cycles/max(1,self.cycles_completed)*100:.0f}%)")
            logger.info(f"Realized P&L: ${position['realized_pnl']:.2f}")
            logger.info(f"Total fees: ${position['total_fees']:.2f}")
            logger.info(f"Max drawdown: {self.max_drawdown:.2f}%")
            logger.info("=" * 60)
        except Exception:
            pass
    
    def run(self):
        """Main trading loop."""
        logger.info(f"🤖 Starting Grid Bot v2.0 - {self.scenario_name}")
        logger.info(f"📊 Base spacing: {self.base_grid_spacing}%, Fee: {self.fee_rate*100:.3f}%")
        
        # Store scenario index
        for i, s in enumerate(self.config_manager.scenarios):
            if s['name'] == self.scenario_name:
                self.current_scenario_index = i
                break
        
        if not self.calculate_grid_levels():
            logger.error("Failed to initialize grid")
            return
        
        try:
            while True:
                logger.info("--- 🔄 Cycle ---")
                
                # Memory check (Pi optimization)
                self.check_memory_usage()
                
                # Get current price
                try:
                    current_price = self.exchange.fetch_ticker(self.symbol)['last']
                    if not current_price:
                        time.sleep(self.check_interval)
                        continue
                except Exception:
                    time.sleep(self.check_interval)
                    continue
                
                # Trend filter
                if not self.check_trend_filter():
                    time.sleep(self.check_interval)
                    continue
                
                # Reposition if needed
                if self.should_reposition_grid(current_price):
                    self.calculate_grid_levels(reposition=True)
                
                # Safety checks
                if not self.check_stop_loss():
                    break
                
                # Execute trading
                self.place_grid_orders()
                self.check_orders()
                
                # Status
                self.calculate_current_value()
                
                logger.info(f"💤 Sleep {self.check_interval}s\n")
                time.sleep(self.check_interval)
        
        except KeyboardInterrupt:
            logger.info("🛑 Stopped by user")
            self.cancel_all_orders()
            self._print_final_summary()
        except Exception as e:
            logger.error(f"❌ Fatal error: {e}")
            import traceback
            traceback.print_exc()
            self.emergency_stop()

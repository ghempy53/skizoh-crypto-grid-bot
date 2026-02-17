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
# SKIZOH CRYPTO GRID TRADING BOT - Core Trading Engine v3.0
# =============================================================================
# PROFIT OPTIMIZATIONS:
# - Asymmetric grid placement based on market bias
# - Dynamic spacing that tightens in high-profit zones
# - Momentum-based entry timing
# - Trailing profit locks
# - Capital efficiency improvements
# - BNB fee discount support
#
# SMART v3.0 FEATURES:
# - Adaptive configuration engine (continuous parameter blending)
# - Multi-timeframe market regime detection
# - Circuit breaker pattern for API resilience
# - Flash crash detection and emergency response
# - Portfolio heat tracking for position sizing
# - Volume-aware grid placement
# - VWAP-based buy/sell bias
# - Heartbeat system for external monitoring
# - Auto-recovery from exchange disconnections
# - 24/7 uptime resilience
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
from adaptive_config import AdaptiveConfigEngine, MarketRegimeDetector, MarketRegime
from resilience import (
    CircuitBreaker, retry_with_backoff, ConnectionMonitor,
    FlashCrashDetector, PortfolioHeatTracker, Heartbeat,
    SessionHealth
)

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
    - ETH accumulation bias (buy-back more ETH than sold)
    """

    def __init__(self, fee_rate: float = 0.001):
        self.fee_rate = fee_rate
        self.min_profit_multiplier = 2.5  # Minimum profit vs fees
        # ETH accumulation: tighter buy-back spacing means more ETH purchased per cycle
        self.accumulation_rebuy_tightening = 0.15  # Buy back 15% closer than sell spacing
        
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
        
        # RSI adjustment: tighter spacing at mean reversion zones
        # where grid cycles complete faster
        if rsi < 25 or rsi > 75:
            optimal *= 0.8  # Strong mean reversion zone - much tighter
        elif rsi < 30 or rsi > 70:
            optimal *= 0.85  # Oversold/overbought - tighter
        elif 30 <= rsi < 40 or 60 < rsi <= 70:
            optimal *= 0.92  # Mildly extended - slightly tighter

        return max(min_spacing, round(optimal, 3))
    
    def calculate_asymmetric_levels(self, current_price: float, num_levels: int,
                                     spacing: float, bias: Dict[str, float]) -> Tuple[List[float], List[float]]:
        """
        Calculate asymmetric buy and sell levels based on market bias.

        In bullish conditions: more sell levels above, fewer buy levels below
        In bearish conditions: more buy levels below, fewer sell levels above

        Uses cumulative progressive spacing so each successive level is 10%
        wider than the previous gap, giving tighter density near price.
        """
        buy_weight = bias.get('buy_weight', 0.5)

        # Calculate level distribution
        num_buys = max(1, int(num_levels * buy_weight))
        num_sells = max(1, num_levels - num_buys)

        # Generate buy levels (below current price) with cumulative spacing
        buy_levels = []
        cumulative_offset = 0.0
        for i in range(1, num_buys + 1):
            # Each gap is 10% wider than the previous
            gap = spacing * (1 + (i - 1) * 0.1)
            cumulative_offset += gap
            price = current_price * (1 - cumulative_offset / 100)
            if price > 0:
                buy_levels.append(round(price, 2))

        # Generate sell levels (above current price) with cumulative spacing
        sell_levels = []
        cumulative_offset = 0.0
        for i in range(1, num_sells + 1):
            gap = spacing * (1 + (i - 1) * 0.1)
            cumulative_offset += gap
            price = current_price * (1 + cumulative_offset / 100)
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
    Smart grid trading bot v3.0 with adaptive intelligence.

    KEY FEATURES:
    1. Asymmetric grid placement based on market bias
    2. Dynamic spacing that adapts to volatility
    3. Momentum-based entry timing
    4. Profit zone acceleration
    5. Capital efficiency improvements
    6. Memory-efficient for Raspberry Pi
    7. Adaptive config engine (v3.0) - continuous parameter blending
    8. Market regime detection (v3.0) - multi-timeframe analysis
    9. Circuit breaker resilience (v3.0) - 24/7 uptime
    10. Flash crash protection (v3.0) - emergency response
    11. Portfolio heat management (v3.0) - dynamic position sizing
    12. Volume-aware grid placement (v3.0) - VWAP/volume profile
    """

    DEFAULT_FEE_RATE = 0.001  # 0.1%
    TREND_PAUSE_SECONDS = 1800  # 30 minutes
    REPOSITION_THRESHOLD_MULTIPLIER = 2.0  # Reduced for more responsive repositioning
    MIN_GRID_UPDATE_INTERVAL = 300  # 5 minutes (reduced from 10)
    FEE_SAFETY_FACTOR = 2.5
    STALE_ORDER_SECONDS = 3600  # Cancel unfilled orders older than 1 hour

    # Pi-specific settings
    MEMORY_CHECK_INTERVAL = 50  # Check memory every N cycles
    MAX_MEMORY_MB = 300  # Force GC if above this

    # v3.0 resilience settings
    MAX_CONSECUTIVE_API_FAILURES = 10
    RECONNECT_DELAY_BASE = 5.0  # seconds
    DEGRADED_MODE_INTERVAL_MULTIPLIER = 3.0  # Slow down checks in degraded mode

    def __init__(self, config_file: str = 'config.json', scenario: Optional[Dict[str, Any]] = None):
        """Initialize the smart grid trading bot."""
        # Resolve config file path
        # Config lives at <project>/src/priv/config.json, so project root is 3 levels up
        self.config_file_path = Path(config_file).resolve()
        self.project_root = self.config_file_path.parent.parent.parent
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

        # Use provided scenario or prompt for selection
        if scenario is None:
            scenario = self.config_manager.select_scenario_interactive()
        self.load_scenario(scenario)

        # Initialize exchange
        self.exchange = self.initialize_exchange()
        self.market_analyzer = MarketAnalyzer(self.exchange, self.symbol)

        # =====================================================================
        # v3.0: Smart Adaptive Systems
        # =====================================================================

        # Adaptive configuration engine (replaces discrete scenario switching)
        self.enable_adaptive_config = config.get('enable_adaptive_config', True)
        self.regime_detector = MarketRegimeDetector(self.market_analyzer)
        self.adaptive_engine = AdaptiveConfigEngine(
            self.config_manager.scenarios, self.regime_detector
        )

        # Circuit breakers for API resilience
        self._cb_trading = CircuitBreaker(
            'trading', failure_threshold=5, recovery_timeout=120
        )
        self._cb_market_data = CircuitBreaker(
            'market_data', failure_threshold=8, recovery_timeout=60
        )

        # Connection monitoring
        self.connection_monitor = ConnectionMonitor()

        # Flash crash detector
        self.flash_crash_detector = FlashCrashDetector()

        # Portfolio heat tracker
        self.portfolio_heat = PortfolioHeatTracker()

        # Heartbeat for external monitoring
        heartbeat_file = str(self.data_dir / 'heartbeat.json')
        self.heartbeat = Heartbeat(heartbeat_file, interval=60)

        # Session health
        self.session_health = SessionHealth()

        # =====================================================================
        # End v3.0 systems
        # =====================================================================

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

        # Dynamic scenario settings (v2.0 fallback when adaptive config is disabled)
        self.enable_dynamic_scenarios = config.get('enable_dynamic_scenarios', True)
        self.cycles_per_scenario_check = config.get('cycles_per_scenario_check', 5)
        self.cycles_since_scenario_check = 0
        self.current_scenario_index = None
        self.last_scenario_change = time.time()
        self.min_scenario_hold_time = config.get('min_scenario_hold_minutes', 45) * 60
        self.scenario_change_threshold = config.get('scenario_change_confidence', 0.65)
        self.recent_scenario_scores = []

        # Grid state
        self.grid_center_price: Optional[float] = None
        self.last_grid_update = time.time()
        self.current_volatility = 0.0
        self.current_adx = 0.0
        self._last_market_conditions: Optional[Dict[str, Any]] = None
        self._last_market_conditions_time = 0.0
        self._market_conditions_ttl = 30  # reuse for 30s

        # Performance tracking
        self.start_time: Optional[datetime] = None
        self.peak_value = 0.0
        self.max_drawdown = 0.0
        self.last_profit_time = time.time()

        # Trend pause state
        self.trend_pause_until = 0.0

        # ETH accumulation tracking
        self.initial_eth_balance: Optional[float] = None
        self.eth_high_watermark = 0.0

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

    def _reconnect_exchange(self) -> bool:
        """
        Attempt to reconnect to the exchange after connection loss.

        v3.0: Uses exponential backoff and updates connection monitor.
        """
        logger.warning("Attempting exchange reconnection...")
        self.connection_monitor.record_reconnect()

        def _try_connect():
            self.exchange = ccxt.binanceus({
                'apiKey': self.api_key,
                'secret': self.api_secret,
                'enableRateLimit': True,
                'timeout': 30000,
                'options': {
                    'adjustForTimeDifference': True,
                    'recvWindow': 60000,
                }
            })
            self.exchange.load_markets()
            # Verify connection with a lightweight call
            self.exchange.fetch_ticker(self.symbol)
            return True

        result = retry_with_backoff(
            _try_connect, max_retries=4,
            base_delay=self.RECONNECT_DELAY_BASE,
            circuit_breaker=self._cb_market_data,
            fallback=False
        )

        if result:
            self.market_analyzer = MarketAnalyzer(self.exchange, self.symbol)
            self.regime_detector = MarketRegimeDetector(self.market_analyzer)
            self.adaptive_engine.regime_detector = self.regime_detector
            logger.info("Exchange reconnection successful")
        else:
            logger.error("Exchange reconnection failed after all retries")

        return bool(result)

    def _resilient_api_call(self, func, circuit_breaker=None, fallback=None):
        """
        Execute an API call with circuit breaker protection and monitoring.

        v3.0: Wraps all exchange API calls for resilience.
        """
        cb = circuit_breaker or self._cb_market_data
        start = time.time()

        try:
            if not cb.can_execute():
                return fallback

            result = func()
            duration = time.time() - start
            self.connection_monitor.record_api_call(duration, success=True)
            cb.record_success()
            return result
        except Exception as e:
            duration = time.time() - start
            self.connection_monitor.record_api_call(duration, success=False)
            cb.record_failure()
            logger.warning(f"API call failed: {e}")
            return fallback
    
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
            # SELL: proceeds = value received minus fee
            # BUY: cost = value paid plus fee (negative proceeds)
            net_proceeds = total_value - fee if transaction_type == 'SELL' else -(total_value + fee)
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
    
    def get_market_conditions(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Get comprehensive market conditions for decision making.

        Results are cached for ``_market_conditions_ttl`` seconds so that
        multiple callers in the same cycle (main loop, scenario checker) share
        the same data without redundant API calls.

        v3.0: Now includes volume analysis, VWAP, and regime detection.
        """
        now = time.time()
        if (not force_refresh
                and self._last_market_conditions is not None
                and now - self._last_market_conditions_time < self._market_conditions_ttl):
            return self._last_market_conditions

        try:
            ticker = self._resilient_api_call(
                lambda: self.exchange.fetch_ticker(self.symbol)
            )
            if not ticker:
                return self._last_market_conditions  # Return stale data if available

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

            result = {
                'price': current_price,
                'volatility': volatility,
                'rsi': rsi,
                'adx': adx,
                'adx_data': adx_data,
                'macd': macd,
                'bb': bb,
                'momentum': momentum,
                'high_24h': high_24h,
                'low_24h': low_24h,
            }

            # v3.0: Add volume analysis (non-critical, won't block on failure)
            try:
                vwap = self.market_analyzer.calculate_vwap()
                vol_momentum = self.market_analyzer.calculate_volume_momentum()
                vol_profile = self.market_analyzer.calculate_volume_profile()
                result['vwap'] = vwap
                result['volume_momentum'] = vol_momentum
                result['volume_profile'] = vol_profile
            except Exception:
                pass

            # v3.0: Flash crash detection
            crash_status = self.flash_crash_detector.update(current_price)
            result['flash_crash'] = crash_status

            self._last_market_conditions = result
            self._last_market_conditions_time = now
            return result
        except Exception as e:
            logger.error(f"Failed to get market conditions: {e}")
            return self._last_market_conditions  # Return stale data on failure
    
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
        """
        Calculate optimized grid levels.

        v3.0: Uses adaptive config engine for parameters, volume profile
        for grid placement, and portfolio heat for position sizing.
        """
        try:
            market = self.get_market_conditions()
            if not market:
                return False

            current_price = market['price']
            balances = self.get_balances()
            if not balances:
                return False

            # v3.0: Use adaptive config engine for parameters if enabled
            if self.enable_adaptive_config:
                adaptive_params = self.adaptive_engine.compute_blended_params(market)
                adapted_spacing = adaptive_params.get('grid_spacing_percent', self.base_grid_spacing)
                adapted_levels = adaptive_params.get_int('grid_levels', self.grid_levels_count)
                adapted_investment = adaptive_params.get('investment_percent', self.investment_percent)
                adapted_interval = adaptive_params.get('check_interval_seconds', self.check_interval)

                # Apply smoothly adapted parameters
                self.check_interval = max(15, adapted_interval)
            else:
                adapted_spacing = self.base_grid_spacing
                adapted_levels = self.grid_levels_count
                adapted_investment = self.investment_percent

            # Get optimal spacing based on conditions (layered on top of adaptive base)
            optimal_spacing = self.profit_optimizer.calculate_optimal_spacing(
                adapted_spacing,
                market['volatility'],
                market['adx'],
                market['rsi']
            )

            if abs(optimal_spacing - self.grid_spacing_percent) > 0.1:
                logger.info(f"[Grid] Spacing adjusted: {self.grid_spacing_percent:.2f}% -> {optimal_spacing:.2f}%")
                self.grid_spacing_percent = optimal_spacing

            # Dynamic level count based on grid efficiency
            efficiency = self.market_analyzer.calculate_grid_efficiency_score()
            if efficiency:
                eff_score = efficiency['score']
                base_levels = adapted_levels
                if eff_score >= 80:
                    adjusted_levels = min(int(base_levels * 1.3), 24)
                elif eff_score >= 60:
                    adjusted_levels = base_levels
                elif eff_score >= 40:
                    adjusted_levels = max(int(base_levels * 0.7), 3)
                else:
                    adjusted_levels = max(int(base_levels * 0.5), 2)

                if adjusted_levels != adapted_levels:
                    logger.info(f"[Grid] Levels adjusted: {adapted_levels} -> {adjusted_levels} "
                               f"(efficiency: {eff_score})")

                effective_levels = adjusted_levels
            else:
                effective_levels = adapted_levels

            # v3.0: Portfolio heat-based position sizing
            heat_multiplier = self.portfolio_heat.get_position_size_multiplier()
            if heat_multiplier < 1.0:
                effective_levels = max(2, int(effective_levels * heat_multiplier))
                logger.info(f"[Heat] Reduced levels to {effective_levels} (heat multiplier: {heat_multiplier:.2f})")

            # Get market bias
            bias = self.market_analyzer.should_adjust_grid_bias()

            # v3.0: VWAP-based bias adjustment
            vwap_data = market.get('vwap')
            if vwap_data:
                if vwap_data.get('price_above_vwap'):
                    # Price above VWAP: slight sell bias (revert to VWAP)
                    distance = abs(vwap_data.get('distance_percent', 0))
                    if distance > 0.5:
                        sell_boost = min(0.1, distance * 0.02)
                        bias['sell_weight'] = min(0.75, bias['sell_weight'] + sell_boost)
                        bias['buy_weight'] = 1.0 - bias['sell_weight']
                else:
                    # Price below VWAP: slight buy bias
                    distance = abs(vwap_data.get('distance_percent', 0))
                    if distance > 0.5:
                        buy_boost = min(0.1, distance * 0.02)
                        bias['buy_weight'] = min(0.75, bias['buy_weight'] + buy_boost)
                        bias['sell_weight'] = 1.0 - bias['buy_weight']

            # Exposure check BEFORE calculating levels so bias adjustment takes effect
            exposure = self.check_exposure_limits(current_price)
            if exposure.get('should_reduce'):
                logger.warning(f"[Exposure] High exposure ({exposure['current_exposure']:.1f}%), favoring sells")
                bias['buy_weight'] = max(0.15, bias['buy_weight'] * 0.5)
                bias['sell_weight'] = 1.0 - bias['buy_weight']

            # Calculate asymmetric levels with exposure-adjusted bias
            buy_prices, sell_prices = self.profit_optimizer.calculate_asymmetric_levels(
                current_price, effective_levels, self.grid_spacing_percent, bias
            )

            # v3.0: Snap buy levels to high-volume nodes (support zones) if available
            vol_profile = market.get('volume_profile')
            if vol_profile and vol_profile.get('hvn_prices'):
                buy_prices = self._snap_to_volume_nodes(
                    buy_prices, vol_profile['hvn_prices'],
                    current_price, is_buy=True
                )

            if self.initial_investment == 0:
                self.initial_investment = balances['quote'] + (balances['base'] * current_price)
                self.start_time = datetime.now()

            if reposition:
                logger.info("[Grid] Repositioning grid")
                self.cancel_all_orders()

            self.grid_levels = []
            self.grid_center_price = current_price
            self.last_grid_update = time.time()

            # Investment calculation with adaptive percentage
            investment_pct = self.calculate_compounded_investment()
            if self.enable_adaptive_config:
                investment_pct = min(investment_pct, adapted_investment)
            available_usdt = balances['quote'] * (investment_pct / 100)
            max_single_usdt = self.initial_investment * (self.max_single_order_percent / 100)

            # v3.0: Apply heat-based sizing to order amounts
            available_usdt *= heat_multiplier

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

            # Create sell levels (only above average cost basis to protect ETH)
            crypto_available = balances['base']
            num_sells = len(sell_prices)
            avg_cost = self.position_tracker.get_average_cost()
            if num_sells > 0 and crypto_available > 0:
                max_single_crypto = max_single_usdt / current_price
                crypto_per_sell = min(crypto_available / num_sells, max_single_crypto)

                # v3.0: Apply heat multiplier to sell sizing too
                crypto_per_sell *= heat_multiplier

                for price in sell_prices:
                    if avg_cost > 0 and price < avg_cost * (1 + self.fee_rate * 2):
                        logger.debug(f"Skipping sell @ ${price:.2f} — below cost basis ${avg_cost:.2f}")
                        continue
                    if crypto_per_sell > 0:
                        self.grid_levels.append({
                            'price': price,
                            'quantity': crypto_per_sell,
                            'type': 'sell',
                            'filled': False,
                            'order_id': None
                        })

            # Get regime info for logging
            regime_info = ""
            if self.enable_adaptive_config:
                regime = self.adaptive_engine.get_active_regime()
                if regime:
                    regime_info = f" | Regime: {regime.primary_regime}"

            logger.info(f"[Grid] {len([l for l in self.grid_levels if l['type']=='buy'])} buys, "
                       f"{len([l for l in self.grid_levels if l['type']=='sell'])} sells @ "
                       f"{self.grid_spacing_percent:.2f}% spacing (bias: {bias['bias']}{regime_info})")

            return True
        except Exception as e:
            logger.error(f"Failed to calculate grid: {e}")
            return False

    def _snap_to_volume_nodes(self, prices: List[float], hvn_prices: List[float],
                               current_price: float, is_buy: bool,
                               snap_threshold_pct: float = 0.3) -> List[float]:
        """
        Snap grid prices to nearby high-volume nodes.

        HVN prices act as support/resistance where grid orders are more
        likely to fill and bounce back, completing cycles faster.

        Only snaps if the HVN is within snap_threshold_pct of the original level.
        """
        if not hvn_prices:
            return prices

        snapped = []
        for price in prices:
            best_hvn = None
            best_distance = float('inf')

            for hvn in hvn_prices:
                if is_buy and hvn >= current_price:
                    continue  # Only snap buys to HVNs below price
                if not is_buy and hvn <= current_price:
                    continue  # Only snap sells to HVNs above price

                distance_pct = abs(price - hvn) / price * 100
                if distance_pct < snap_threshold_pct and distance_pct < best_distance:
                    best_distance = distance_pct
                    best_hvn = hvn

            snapped.append(best_hvn if best_hvn else price)

        return snapped
    
    def place_grid_orders(self):
        """
        Place optimized grid orders with momentum-based entry timing.

        v3.0: Uses circuit breaker for API resilience. Skips order placement
        if flash crash is detected or portfolio heat is too high.
        """
        try:
            # v3.0: Skip if flash crash detected
            if self.flash_crash_detector.is_alert_active():
                logger.warning("[Flash] Skipping order placement — flash crash alert active")
                return

            # v3.0: Skip if trading circuit breaker is open
            if not self._cb_trading.can_execute():
                logger.warning("[CB] Trading circuit breaker is open — skipping orders")
                return

            market_info = self.exchange.market(self.symbol)
            min_amount = market_info.get('limits', {}).get('amount', {}).get('min', 0.0001)

            # Get momentum for entry timing (cached, low overhead)
            momentum = 0.0
            try:
                macd = self.market_analyzer.calculate_macd()
                if macd:
                    momentum = macd.get('momentum', 0.0)
            except Exception:
                pass

            current_price = self.grid_center_price or 0
            orders_placed = 0

            for level in self.grid_levels:
                if level['filled'] or level.get('order_id'):
                    continue

                price = level['price']
                if price <= 0:
                    continue

                # Skip orders where momentum suggests a better entry is coming
                is_buy = level['type'] == 'buy'
                if current_price > 0 and self.profit_optimizer.should_wait_for_better_entry(
                        current_price, price, momentum, is_buy):
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
                    self.active_orders[order['id']] = {
                        'level': level, 'order': order, 'placed_at': time.time()
                    }
                    self._cb_trading.record_success()
                    orders_placed += 1
                    logger.info(f"[Order] {level['type'].upper()}: {quantity:.6f} @ ${price:.2f}")

                except ccxt.InsufficientFunds:
                    logger.warning(f"Insufficient funds for {level['type']} @ ${price}")
                    break
                except Exception as e:
                    self._cb_trading.record_failure()
                    logger.warning(f"Order failed @ ${price}: {e}")

            if orders_placed > 0:
                logger.info(f"[Orders] Placed {orders_placed} new orders")

        except Exception as e:
            logger.error(f"Failed to place orders: {e}")
    
    def check_orders(self):
        """Check and process filled orders, including partial fills."""
        for order_id in list(self.active_orders.keys()):
            try:
                order_info = self.exchange.fetch_order(order_id, self.symbol)
                status = order_info['status']

                if status == 'closed':
                    self._handle_filled_order(order_id, order_info)
                elif status == 'canceled':
                    # Handle cancellation with partial fill: process whatever was filled
                    filled_amount = float(order_info.get('filled', 0))
                    if filled_amount > 0:
                        logger.info(f"Processing partial fill ({filled_amount:.6f}) from canceled order")
                        self._handle_filled_order(order_id, order_info)
                    else:
                        level = self.active_orders[order_id]['level']
                        level['order_id'] = None
                        del self.active_orders[order_id]
            except Exception as e:
                logger.warning(f"Error checking order {order_id}: {e}")

        # Prune filled levels that have no active order to prevent unbounded growth
        self.grid_levels = [
            level for level in self.grid_levels
            if not level['filled'] or level.get('order_id')
        ]
    
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
        """Place opposite order after fill with dynamic profit targets."""
        try:
            if fill_price <= 0 or filled_qty <= 0:
                return

            if filled_level['type'] == 'buy':
                # Sell at a dynamic profit target based on volatility
                new_price = self.profit_optimizer.calculate_profit_target(
                    fill_price, self.grid_spacing_percent,
                    self.current_volatility, 0  # New position, age = 0
                )
                side = 'sell'
                quantity = filled_qty
            else:
                # ETH accumulation: use tighter buy-back spacing so we re-enter
                # closer to the sell price, acquiring more ETH per cycle.
                # The tighter spacing still exceeds the fee threshold.
                tightening = self.profit_optimizer.accumulation_rebuy_tightening
                min_spacing_pct = (2 * self.fee_rate * 100) * self.FEE_SAFETY_FACTOR
                rebuy_spacing = max(
                    min_spacing_pct,
                    self.grid_spacing_percent * (1 - tightening)
                )
                adjustment = rebuy_spacing / 100
                new_price = fill_price * (1 - adjustment)
                side = 'buy'
                # Account for the fee paid on the sell to avoid over-allocating USDT
                net_proceeds = filled_qty * fill_price * (1 - self.fee_rate)
                quantity = net_proceeds / new_price

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
            self.active_orders[order['id']] = {
                'level': new_level, 'order': order, 'placed_at': time.time()
            }
            logger.info(f"✓ Opposite {side.upper()}: {quantity:.6f} @ ${new_price:.2f}")

        except Exception as e:
            logger.error(f"Failed to place opposite order: {e}")
    
    def calculate_current_value(self, current_price: float = 0) -> Optional[Dict]:
        """Calculate portfolio value with metrics."""
        try:
            balances = self.get_balances()
            if not balances:
                return None

            if current_price <= 0:
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
            
            # Track ETH accumulation
            eth_balance = balances['base_total']
            if self.initial_eth_balance is None:
                self.initial_eth_balance = eth_balance
                self.eth_high_watermark = eth_balance
            if eth_balance > self.eth_high_watermark:
                self.eth_high_watermark = eth_balance
            eth_change = eth_balance - self.initial_eth_balance

            if self.initial_investment > 0:
                total_pnl = total_value - self.initial_investment
                pnl_percent = (total_pnl / self.initial_investment) * 100

                logger.info(
                    f"📊 Value: ${total_value:.2f} | P&L: ${total_pnl:.2f} ({pnl_percent:+.2f}%) | "
                    f"Cycles: {self.cycles_completed} | DD: {self.max_drawdown:.1f}%"
                )
                logger.info(
                    f"🪙 ETH: {eth_balance:.6f} ({eth_change:+.6f} since start) | "
                    f"HWM: {self.eth_high_watermark:.6f}"
                )

                return {
                    'total_value': total_value,
                    'profit': total_pnl,
                    'profit_percent': pnl_percent,
                    'realized_pnl': position['realized_pnl'],
                    'max_drawdown': self.max_drawdown,
                    'eth_balance': eth_balance,
                    'eth_change': eth_change
                }
            return None
        except Exception as e:
            logger.error(f"Failed to calculate value: {e}")
            return None
    
    def check_stop_loss(self, portfolio: Optional[Dict] = None) -> bool:
        """Check stop loss conditions."""
        if portfolio is None:
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
    
    def _check_scenario_switch(self):
        """Evaluate if a scenario switch would improve profitability."""
        self.cycles_since_scenario_check += 1

        if self.cycles_since_scenario_check < self.cycles_per_scenario_check:
            return

        self.cycles_since_scenario_check = 0

        # Respect minimum hold time
        if time.time() - self.last_scenario_change < self.min_scenario_hold_time:
            return

        try:
            market = self.get_market_conditions()
            if not market:
                return

            volatility = market['volatility']
            adx = market['adx']
            rsi = market['rsi']

            best_idx = None
            best_score = 0.0

            for i, scenario in enumerate(self.config_manager.scenarios):
                score = self._score_scenario_fit(scenario, volatility, adx, rsi)
                if score > best_score:
                    best_score = score
                    best_idx = i

            # Track scores for stability (require consistent recommendation)
            self.recent_scenario_scores.append(best_idx)
            if len(self.recent_scenario_scores) > 3:
                self.recent_scenario_scores = self.recent_scenario_scores[-3:]

            # Only switch if the same scenario is recommended consistently
            # and confidence exceeds threshold
            if (best_idx is not None
                    and best_idx != self.current_scenario_index
                    and best_score >= self.scenario_change_threshold
                    and len(self.recent_scenario_scores) >= 2
                    and all(s == best_idx for s in self.recent_scenario_scores[-2:])):

                new_scenario = self.config_manager.scenarios[best_idx]
                old_name = self.scenario_name
                self.load_scenario(new_scenario)
                self.current_scenario_index = best_idx
                self.last_scenario_change = time.time()
                self.recent_scenario_scores.clear()

                logger.info(f"🔄 SCENARIO CHANGE: {old_name} → {new_scenario['name']} "
                           f"(confidence: {best_score:.0%})")

                # Reposition grid with new scenario parameters
                self.calculate_grid_levels(reposition=True)

        except Exception as e:
            logger.warning(f"Scenario check failed: {e}")

    def _score_scenario_fit(self, scenario: Dict[str, Any], volatility: float,
                            adx: float, rsi: float) -> float:
        """Score how well a scenario fits current market conditions (0-1)."""
        score = 0.5
        name = scenario['name'].lower()
        spacing = scenario['grid_spacing_percent']

        # Low volatility market
        if volatility < 1.5:
            if 'low volatility' in name or spacing <= 0.6:
                score += 0.3
            elif spacing > 1.5:
                score -= 0.2

        # High volatility market
        elif volatility > 5:
            if 'high volatility' in name or spacing >= 1.5:
                score += 0.3
            elif 'scalping' in name or spacing < 0.6:
                score -= 0.3

        # Ranging market (ideal for grid)
        if adx < 20:
            if 'mean reversion' in name or 'balanced' in name:
                score += 0.2
        elif adx > 35:
            if 'conservative' in name or spacing >= 1.5:
                score += 0.2
            elif 'aggressive' in name or 'scalping' in name:
                score -= 0.3

        # RSI extremes favor mean reversion
        if (rsi < 30 or rsi > 70) and adx < 25:
            if 'mean reversion' in name:
                score += 0.2

        return max(0.0, min(1.0, score))

    def reinvest_profits_to_eth(self, current_price: float):
        """Reinvest excess USDT profits into ETH to grow ETH holdings.

        Strategy: once realized profits exceed a threshold, use a portion
        to buy ETH at market price. This converts grid-trading USDT profit
        directly into the target asset.
        """
        if current_price <= 0 or self.initial_investment <= 0:
            return

        realized = self.position_tracker.realized_pnl
        # Only reinvest when realized profit > 2% of initial investment
        profit_threshold = self.initial_investment * 0.02
        if realized < profit_threshold:
            return

        # Reinvest 30% of realized profits beyond the threshold
        reinvest_amount = (realized - profit_threshold) * 0.30
        if reinvest_amount < self.min_order_size_usdt:
            return

        # Check we have enough free USDT
        balances = self.get_balances()
        if not balances or balances['quote'] < reinvest_amount:
            return

        try:
            quantity = reinvest_amount / current_price
            quantity = float(self.exchange.amount_to_precision(self.symbol, quantity))
            market_info = self.exchange.market(self.symbol)
            min_amount = market_info.get('limits', {}).get('amount', {}).get('min', 0.0001)

            if quantity < min_amount:
                return

            order = self.exchange.create_order(
                symbol=self.symbol, type='market',
                side='buy', amount=quantity
            )

            fill_price = float(order.get('average') or order.get('price') or current_price)
            fee = self._calculate_fee(order, quantity, fill_price)
            self.position_tracker.add_position(quantity, fill_price, fee)

            base_currency = self.symbol.split('/')[0]
            self.log_tax_transaction(
                'BUY', base_currency, quantity, fill_price, fee,
                order.get('id', 'reinvest'),
                cost_basis=quantity * fill_price + fee,
                notes='Profit reinvestment into ETH'
            )

            # Reset realized P&L tracking so we don't reinvest the same profit twice
            self.position_tracker.realized_pnl -= reinvest_amount

            logger.info(
                f"💎 REINVESTED ${reinvest_amount:.2f} profit → "
                f"{quantity:.6f} {base_currency} @ ${fill_price:.2f}"
            )
        except ccxt.InsufficientFunds:
            logger.debug("Insufficient funds for profit reinvestment")
        except Exception as e:
            logger.warning(f"Profit reinvestment failed: {e}")

    def cancel_stale_orders(self):
        """Cancel orders that have been open too long without filling.

        Stale orders tie up capital that could be redeployed at current prices.
        """
        now = time.time()
        stale_ids = []
        for order_id, info in self.active_orders.items():
            placed_at = info.get('placed_at', now)
            if now - placed_at > self.STALE_ORDER_SECONDS:
                stale_ids.append(order_id)

        for order_id in stale_ids:
            try:
                self.exchange.cancel_order(order_id, self.symbol)
                level = self.active_orders[order_id]['level']
                level['order_id'] = None
                level['filled'] = False
                del self.active_orders[order_id]
                logger.info(f"♻️ Canceled stale order {order_id}")
            except Exception as e:
                logger.warning(f"Could not cancel stale order {order_id}: {e}")

        if stale_ids:
            logger.info(f"♻️ Canceled {len(stale_ids)} stale orders — capital unlocked for redeployment")

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
                qty_float = float(quantity)
                if qty_float > 0:
                    order = self.exchange.create_order(
                        symbol=self.symbol, type='market',
                        side='sell', amount=quantity
                    )
                    # Track the emergency sell in position tracker and tax log
                    sell_price = float(order.get('average') or order.get('price', 0))
                    if sell_price > 0:
                        fee = self._calculate_fee(order, qty_float, sell_price)
                        result = self.position_tracker.close_position(qty_float, sell_price, fee)
                        base_currency = self.symbol.split('/')[0]
                        self.log_tax_transaction(
                            'SELL', base_currency, qty_float, sell_price, fee,
                            order.get('id', 'emergency'),
                            cost_basis=result['cost_basis'],
                            realized_pnl=result['pnl'],
                            notes='Emergency stop sell'
                        )
        except Exception as e:
            logger.error(f"Emergency stop error: {e}")

        self._print_final_summary()
    
    def _print_final_summary(self):
        """Print trading session summary with v3.0 diagnostics."""
        try:
            current_price = self.exchange.fetch_ticker(self.symbol)['last'] or 0
            position = self.position_tracker.get_summary(current_price)
            runtime = datetime.now() - self.start_time if self.start_time else None

            logger.info("=" * 60)
            logger.info("SESSION SUMMARY (v3.0)")
            logger.info("=" * 60)
            logger.info(f"Strategy: {self.scenario_name}")
            if runtime:
                logger.info(f"Runtime: {runtime}")
            logger.info(f"Cycles: {self.cycles_completed} "
                       f"(Win rate: {self.profitable_cycles/max(1,self.cycles_completed)*100:.0f}%)")
            logger.info(f"Realized P&L: ${position['realized_pnl']:.2f}")
            logger.info(f"Total fees: ${position['total_fees']:.2f}")
            logger.info(f"Max drawdown: {self.max_drawdown:.2f}%")

            if self.initial_eth_balance is not None:
                balances = self.get_balances()
                if balances:
                    eth_now = balances['base_total']
                    eth_change = eth_now - self.initial_eth_balance
                    logger.info(f"ETH: {eth_now:.6f} ({eth_change:+.6f} since start)")

            # v3.0: Smart system diagnostics
            logger.info("-" * 60)
            logger.info("SMART SYSTEMS DIAGNOSTICS")
            logger.info("-" * 60)

            # Session health
            health = self.session_health.get_status()
            logger.info(f"Session health: {health['overall_score']}/100 "
                       f"(degraded: {health['degraded_mode']})")
            logger.info(f"Uptime: {health['uptime_seconds']/3600:.1f}h")

            # Connection stats
            conn = self.connection_monitor.get_stats()
            logger.info(f"Connection: {conn['health_score']}/100, "
                       f"Error rate: {conn['error_rate']}, "
                       f"Reconnects: {conn['reconnects']}")

            # Circuit breaker stats
            cb_trading = self._cb_trading.get_stats()
            cb_market = self._cb_market_data.get_stats()
            logger.info(f"Circuit breakers: "
                       f"Trading({cb_trading['state']}, {cb_trading['total_failures']} failures) "
                       f"Market({cb_market['state']}, {cb_market['total_failures']} failures)")

            # Portfolio heat
            heat = self.portfolio_heat.get_status()
            logger.info(f"Portfolio heat: {heat['heat']:.0f}/100 "
                       f"(multiplier: {heat['size_multiplier']:.2f}x)")

            # Regime detection
            if self.enable_adaptive_config:
                regime = self.adaptive_engine.get_active_regime()
                if regime:
                    stability = self.regime_detector.get_regime_stability()
                    logger.info(f"Final regime: {regime.primary_regime} "
                               f"(confidence: {regime.confidence:.0%}, "
                               f"stability: {stability:.0%})")
                weights = self.adaptive_engine.get_scenario_weights()
                if weights:
                    top = sorted(weights.items(), key=lambda x: x[1], reverse=True)[:3]
                    logger.info(f"Top scenarios: {', '.join(f'{n}: {w:.0%}' for n, w in top)}")

            logger.info("=" * 60)
        except Exception:
            pass
    
    def _update_portfolio_heat(self, current_price: float):
        """Update portfolio heat tracking with current market data."""
        try:
            position = self.position_tracker.get_summary(current_price)
            self.portfolio_heat.calculate_heat(
                open_positions=position['num_positions'],
                unrealized_pnl=position['unrealized_pnl'],
                total_investment=self.initial_investment,
                volatility=self.current_volatility,
                drawdown_pct=self.max_drawdown,
            )
        except Exception:
            pass

    def _write_heartbeat(self, current_price: float = 0):
        """Write heartbeat for external monitoring."""
        try:
            regime = self.adaptive_engine.get_active_regime() if self.enable_adaptive_config else None
            self.heartbeat.beat({
                'uptime_seconds': self.session_health.get_uptime_seconds(),
                'cycles': self.cycles_completed,
                'health_score': self.session_health.get_overall_score(),
                'regime': regime.primary_regime if regime else 'N/A',
                'portfolio_heat': self.portfolio_heat._current_heat,
                'price': current_price,
                'scenario': self.scenario_name,
            })
        except Exception:
            pass

    def _log_smart_status(self, current_price: float):
        """Log comprehensive smart bot status (v3.0)."""
        try:
            health = self.session_health.get_status()
            heat = self.portfolio_heat.get_status()
            conn = self.connection_monitor.get_stats()

            status_parts = [
                f"[Health] Score: {health['overall_score']}",
                f"Heat: {heat['heat']:.0f}/{heat['max_heat']}",
                f"Conn: {conn['health_score']}",
            ]

            if self.enable_adaptive_config:
                regime = self.adaptive_engine.get_active_regime()
                if regime:
                    stability = self.regime_detector.get_regime_stability()
                    status_parts.append(
                        f"Regime: {regime.primary_regime}({regime.confidence:.0%})"
                    )
                    status_parts.append(f"Stability: {stability:.0%}")

            if self.session_health.is_degraded():
                status_parts.append("MODE: DEGRADED")

            logger.info(" | ".join(status_parts))
        except Exception:
            pass

    def run(self):
        """
        Main trading loop with v3.0 smart systems.

        Features:
        - Adaptive configuration with continuous parameter blending
        - Flash crash detection and emergency response
        - Auto-reconnect on connection loss
        - Degraded mode operation (slower but keeps running)
        - Portfolio heat-based position sizing
        - Heartbeat for external monitoring
        - Circuit breaker API protection
        """
        logger.info(f"[Bot] Starting Grid Bot v3.0 - {self.scenario_name}")
        logger.info(f"[Bot] Base spacing: {self.base_grid_spacing}%, Fee: {self.fee_rate*100:.3f}%")
        logger.info(f"[Bot] Adaptive config: {'ENABLED' if self.enable_adaptive_config else 'DISABLED'}")

        # Store scenario index
        for i, s in enumerate(self.config_manager.scenarios):
            if s['name'] == self.scenario_name:
                self.current_scenario_index = i
                break

        if not self.calculate_grid_levels():
            logger.error("Failed to initialize grid")
            return

        smart_status_interval = 600  # Log smart status every 10 minutes
        last_smart_status = time.time()

        try:
            while True:
                cycle_start = time.time()
                error_in_cycle = False

                logger.info("--- Cycle ---")

                # Memory check (Pi optimization)
                self.check_memory_usage()

                # ============================================================
                # PHASE 1: Get market data (with resilience)
                # ============================================================
                current_price = 0
                try:
                    # v3.0: Check connection health, reconnect if needed
                    if not self.connection_monitor.is_connected():
                        logger.warning("[Conn] Connection appears lost, attempting reconnect...")
                        if not self._reconnect_exchange():
                            self.session_health.update(0, False, error_occurred=True)
                            sleep_time = self.check_interval * self.DEGRADED_MODE_INTERVAL_MULTIPLIER
                            logger.warning(f"[Conn] Reconnect failed, sleeping {sleep_time:.0f}s")
                            time.sleep(sleep_time)
                            continue

                    market = self.get_market_conditions()
                    if market:
                        current_price = market['price']
                    else:
                        error_in_cycle = True
                        time.sleep(self.check_interval)
                        continue
                except Exception as e:
                    logger.error(f"[Market] Data fetch failed: {e}")
                    error_in_cycle = True
                    self.session_health.update(
                        self.connection_monitor.get_health_score(), False, error_occurred=True
                    )
                    time.sleep(self.check_interval)
                    continue

                # ============================================================
                # PHASE 2: Flash crash check (v3.0)
                # ============================================================
                flash_crash = market.get('flash_crash', {})
                if flash_crash.get('crash_detected'):
                    severity = flash_crash.get('severity', 0)
                    logger.critical(
                        f"[Flash] CRASH DETECTED (severity: {severity:.1f}x) — "
                        f"cancelling orders and pausing"
                    )
                    self.cancel_all_orders()
                    # Don't emergency stop unless very severe — just pause
                    if severity >= 2.0:
                        logger.critical("[Flash] Severe crash — triggering emergency stop")
                        self.emergency_stop()
                        break
                    else:
                        # Wait for crash cooldown
                        time.sleep(min(300, self.check_interval * 5))
                        continue

                # ============================================================
                # PHASE 3: Trend filter
                # ============================================================
                if not self.check_trend_filter():
                    self.session_health.update(
                        self.connection_monitor.get_health_score(), True
                    )
                    time.sleep(self.check_interval)
                    continue

                # ============================================================
                # PHASE 4: Update adaptive parameters (v3.0)
                # ============================================================
                if self.enable_adaptive_config:
                    try:
                        self.adaptive_engine.compute_blended_params(market)
                    except Exception as e:
                        logger.debug(f"[Adaptive] Parameter update failed: {e}")

                # ============================================================
                # PHASE 5: Update portfolio heat (v3.0)
                # ============================================================
                self._update_portfolio_heat(current_price)

                # v3.0: If portfolio heat says reduce, be more aggressive about cancelling
                if self.portfolio_heat.should_reduce_exposure():
                    logger.warning(
                        f"[Heat] Portfolio heat critical ({self.portfolio_heat._current_heat:.0f}) — "
                        f"reducing exposure"
                    )

                # ============================================================
                # PHASE 6: Grid management
                # ============================================================
                # Reposition if needed
                if self.should_reposition_grid(current_price):
                    self.calculate_grid_levels(reposition=True)

                # Execute trading
                self.cancel_stale_orders()
                self.place_grid_orders()
                self.check_orders()

                # ============================================================
                # PHASE 7: Status, stop-loss, reinvestment
                # ============================================================
                portfolio = self.calculate_current_value(current_price)
                if not self.check_stop_loss(portfolio):
                    break

                # Reinvest USDT profits into ETH periodically
                if self.cycle_count % 10 == 0:
                    self.reinvest_profits_to_eth(current_price)

                # ============================================================
                # PHASE 8: Dynamic scenario switching (v2.0 fallback)
                # ============================================================
                if self.enable_dynamic_scenarios and not self.enable_adaptive_config:
                    self._check_scenario_switch()

                # ============================================================
                # PHASE 9: Health updates and heartbeat (v3.0)
                # ============================================================
                self.session_health.update(
                    self.connection_monitor.get_health_score(),
                    trading_ok=True,
                    error_occurred=error_in_cycle,
                )
                self._write_heartbeat(current_price)

                # Periodic smart status logging
                if time.time() - last_smart_status > smart_status_interval:
                    self._log_smart_status(current_price)
                    last_smart_status = time.time()

                # v3.0: Check if session health warrants emergency stop
                if self.session_health.should_emergency_stop():
                    logger.critical("[Health] Too many consecutive errors — emergency stop")
                    self.emergency_stop()
                    break

                # ============================================================
                # PHASE 10: Sleep (with degraded mode adjustment)
                # ============================================================
                sleep_time = self.check_interval
                if self.session_health.is_degraded():
                    sleep_time *= self.DEGRADED_MODE_INTERVAL_MULTIPLIER
                    logger.info(f"[Degraded] Extended sleep: {sleep_time:.0f}s")
                else:
                    logger.info(f"[Sleep] {sleep_time:.0f}s")

                time.sleep(sleep_time)

        except KeyboardInterrupt:
            logger.info("[Bot] Stopped by user")
            self.cancel_all_orders()
            self._print_final_summary()
        except Exception as e:
            logger.error(f"[Bot] Fatal error: {e}")
            import traceback
            traceback.print_exc()
            self.emergency_stop()

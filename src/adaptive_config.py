# =============================================================================
# SKIZOH CRYPTO GRID TRADING BOT - Adaptive Configuration Engine v3.0
# =============================================================================
# SMART FEATURES:
# - Continuous parameter interpolation (no jarring scenario switches)
# - Multi-timeframe market regime detection
# - Confidence-weighted parameter blending from multiple scenarios
# - Smooth exponential transition between parameter sets
# - Time-of-day awareness for 24/7 operation
# - Parameter bounds enforcement for safety
# =============================================================================

import logging
import time
import math
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple

logger = logging.getLogger(__name__)


class MarketRegime:
    """Detected market regime with confidence scores."""

    RANGING = 'RANGING'
    TRENDING_UP = 'TRENDING_UP'
    TRENDING_DOWN = 'TRENDING_DOWN'
    HIGH_VOLATILITY = 'HIGH_VOLATILITY'
    LOW_VOLATILITY = 'LOW_VOLATILITY'
    MEAN_REVERTING = 'MEAN_REVERTING'
    BREAKOUT = 'BREAKOUT'
    CRASH = 'CRASH'

    def __init__(self):
        self.primary_regime: str = self.RANGING
        self.confidence: float = 0.5
        self.regime_scores: Dict[str, float] = {}
        self.duration_seconds: float = 0
        self.timestamp: float = time.time()

    def __repr__(self):
        return f"MarketRegime({self.primary_regime}, confidence={self.confidence:.2f})"


class AdaptiveParameterSet:
    """A continuously-adjustable set of trading parameters."""

    # Safety bounds for all parameters
    BOUNDS = {
        'grid_levels': (3, 24),
        'grid_spacing_percent': (0.3, 5.0),
        'investment_percent': (30, 85),
        'min_order_size_usdt': (5, 30),
        'stop_loss_percent': (5, 30),
        'check_interval_seconds': (15, 300),
        'atr_period': (6, 30),
        'volatility_threshold': (1.5, 15.0),
    }

    def __init__(self, params: Optional[Dict[str, float]] = None):
        self.params: Dict[str, float] = params or {}
        self._smoothed: Dict[str, float] = {}
        self._smooth_alpha = 0.3  # EMA smoothing factor (lower = smoother transitions)

    def get(self, key: str, default: float = 0.0) -> float:
        """Get a parameter value (smoothed if available, else raw)."""
        return self._smoothed.get(key, self.params.get(key, default))

    def get_int(self, key: str, default: int = 0) -> int:
        """Get a parameter as integer."""
        return int(round(self.get(key, float(default))))

    def update_smooth(self, new_params: Dict[str, float]):
        """Apply EMA smoothing to transition between parameter sets."""
        alpha = self._smooth_alpha
        for key, new_val in new_params.items():
            bounds = self.BOUNDS.get(key)
            if bounds:
                new_val = max(bounds[0], min(bounds[1], new_val))

            if key in self._smoothed:
                self._smoothed[key] = alpha * new_val + (1 - alpha) * self._smoothed[key]
            else:
                self._smoothed[key] = new_val

            self.params[key] = new_val

    def set_immediate(self, key: str, value: float):
        """Set a parameter immediately without smoothing."""
        bounds = self.BOUNDS.get(key)
        if bounds:
            value = max(bounds[0], min(bounds[1], value))
        self.params[key] = value
        self._smoothed[key] = value

    def snapshot(self) -> Dict[str, float]:
        """Get a snapshot of all current (smoothed) parameters."""
        result = {}
        for key in self.params:
            result[key] = self.get(key)
        return result


class MarketRegimeDetector:
    """
    Multi-timeframe market regime detection.

    Analyzes multiple timeframes and indicators to determine the current
    market regime with a confidence score. Designed for 24/7 operation
    with efficient caching.
    """

    # Regime detection thresholds
    TREND_ADX_THRESHOLD = 25
    STRONG_TREND_ADX = 35
    LOW_VOL_BB_WIDTH = 2.0
    HIGH_VOL_BB_WIDTH = 6.0
    CRASH_THRESHOLD_PERCENT = -8.0  # 8% drop in 24h
    BREAKOUT_BB_SQUEEZE_WIDTH = 1.2
    BREAKOUT_VOL_MULTIPLIER = 1.8

    def __init__(self, market_analyzer):
        self.analyzer = market_analyzer
        self._last_regime: Optional[MarketRegime] = None
        self._last_detection_time = 0.0
        self._detection_cooldown = 30  # seconds between full recalculations
        self._regime_history: List[Tuple[float, str, float]] = []
        self._max_history = 100

    def detect(self, market_data: Optional[Dict] = None) -> MarketRegime:
        """
        Detect current market regime using multi-indicator analysis.

        Uses ADX, RSI, Bollinger Bands, MACD, and volume to classify
        the market into one of the known regimes.
        """
        now = time.time()
        if (self._last_regime is not None
                and now - self._last_detection_time < self._detection_cooldown):
            return self._last_regime

        regime = MarketRegime()
        scores = {
            MarketRegime.RANGING: 0.0,
            MarketRegime.TRENDING_UP: 0.0,
            MarketRegime.TRENDING_DOWN: 0.0,
            MarketRegime.HIGH_VOLATILITY: 0.0,
            MarketRegime.LOW_VOLATILITY: 0.0,
            MarketRegime.MEAN_REVERTING: 0.0,
            MarketRegime.BREAKOUT: 0.0,
            MarketRegime.CRASH: 0.0,
        }

        # Gather indicators
        adx_data = None
        rsi = None
        bb = None
        macd = None
        volatility = 0.0

        if market_data:
            adx_data = market_data.get('adx_data')
            rsi = market_data.get('rsi')
            bb = market_data.get('bb')
            macd = market_data.get('macd')
            volatility = market_data.get('volatility', 0)
        else:
            rsi = self.analyzer.calculate_rsi_wilder()
            adx_data = self.analyzer.calculate_adx()
            bb = self.analyzer.calculate_bollinger_bands()
            macd = self.analyzer.calculate_macd()

        adx = adx_data['adx'] if adx_data else 20
        trend_dir = adx_data.get('trend_direction', 'NEUTRAL') if adx_data else 'NEUTRAL'

        # --- Score each regime ---

        # RANGING: low ADX, price near BB middle
        if adx < 20:
            scores[MarketRegime.RANGING] += 0.4
        elif adx < 25:
            scores[MarketRegime.RANGING] += 0.2
        if bb and 0.3 < bb.get('price_position', 0.5) < 0.7:
            scores[MarketRegime.RANGING] += 0.15

        # TRENDING UP/DOWN: high ADX with directional confirmation
        if adx > self.TREND_ADX_THRESHOLD:
            trend_strength = min(1.0, (adx - self.TREND_ADX_THRESHOLD) / 25)
            if trend_dir == 'UP':
                scores[MarketRegime.TRENDING_UP] += 0.3 + 0.2 * trend_strength
                if rsi and rsi > 55:
                    scores[MarketRegime.TRENDING_UP] += 0.15
                if macd and macd.get('histogram', 0) > 0:
                    scores[MarketRegime.TRENDING_UP] += 0.1
            else:
                scores[MarketRegime.TRENDING_DOWN] += 0.3 + 0.2 * trend_strength
                if rsi and rsi < 45:
                    scores[MarketRegime.TRENDING_DOWN] += 0.15
                if macd and macd.get('histogram', 0) < 0:
                    scores[MarketRegime.TRENDING_DOWN] += 0.1

        # HIGH VOLATILITY: wide BB, high 24h range
        bb_width = bb.get('width_percent', 3.0) if bb else 3.0
        if bb_width > self.HIGH_VOL_BB_WIDTH:
            scores[MarketRegime.HIGH_VOLATILITY] += 0.35
        elif bb_width > 4.0:
            scores[MarketRegime.HIGH_VOLATILITY] += 0.2
        if volatility > 5:
            scores[MarketRegime.HIGH_VOLATILITY] += 0.2

        # LOW VOLATILITY: tight BB, low 24h range
        if bb_width < self.LOW_VOL_BB_WIDTH:
            scores[MarketRegime.LOW_VOLATILITY] += 0.35
        elif bb_width < 2.5:
            scores[MarketRegime.LOW_VOLATILITY] += 0.15
        if volatility < 1.5:
            scores[MarketRegime.LOW_VOLATILITY] += 0.2

        # MEAN REVERTING: RSI at extremes + low ADX
        if rsi is not None:
            if (rsi < 30 or rsi > 70) and adx < 25:
                scores[MarketRegime.MEAN_REVERTING] += 0.4
            elif (rsi < 35 or rsi > 65) and adx < 20:
                scores[MarketRegime.MEAN_REVERTING] += 0.25

        # BREAKOUT: BB squeeze (very low width) followed by expansion
        if bb_width < self.BREAKOUT_BB_SQUEEZE_WIDTH and adx > 20:
            scores[MarketRegime.BREAKOUT] += 0.3
        # MACD histogram acceleration indicates breakout momentum
        if macd and abs(macd.get('momentum', 0)) > 2:
            scores[MarketRegime.BREAKOUT] += 0.15

        # CRASH: extreme negative price action
        if volatility < self.CRASH_THRESHOLD_PERCENT * -1:  # volatility is positive
            pass  # volatility alone doesn't indicate crash direction
        if rsi is not None and rsi < 20 and adx > 30:
            scores[MarketRegime.CRASH] += 0.4
        if bb and bb.get('price_position', 0.5) < 0.05:
            scores[MarketRegime.CRASH] += 0.2

        # Determine primary regime
        regime.regime_scores = scores
        best_regime = max(scores, key=scores.get)
        regime.primary_regime = best_regime
        regime.confidence = min(1.0, max(0.1, scores[best_regime]))

        # Track duration
        if self._last_regime and self._last_regime.primary_regime == best_regime:
            regime.duration_seconds = (self._last_regime.duration_seconds
                                       + (now - self._last_detection_time))
        else:
            regime.duration_seconds = 0

        # Record history
        self._regime_history.append((now, best_regime, regime.confidence))
        if len(self._regime_history) > self._max_history:
            self._regime_history = self._regime_history[-self._max_history:]

        self._last_regime = regime
        self._last_detection_time = now

        return regime

    def get_regime_stability(self, lookback_count: int = 10) -> float:
        """
        How stable is the current regime? (0 = chaotic, 1 = very stable).

        Measures what fraction of recent detections agree with current regime.
        """
        if not self._regime_history or not self._last_regime:
            return 0.5

        recent = self._regime_history[-lookback_count:]
        current = self._last_regime.primary_regime
        agree_count = sum(1 for _, r, _ in recent if r == current)
        return agree_count / len(recent)

    def get_regime_duration_minutes(self) -> float:
        """How long has the current regime been active?"""
        if self._last_regime:
            return self._last_regime.duration_seconds / 60
        return 0


class AdaptiveConfigEngine:
    """
    Continuously adapts trading parameters based on market conditions.

    Instead of switching between discrete scenarios, this engine blends
    parameters from multiple scenarios weighted by how well each fits
    the current market regime. Transitions are smoothed via EMA to
    prevent jarring parameter changes.

    Features:
    - Multi-scenario weighted blending
    - Time-of-day adjustments for 24/7 operation
    - Regime-aware parameter tuning
    - Safety bounds enforcement
    - Smooth parameter transitions
    """

    # Parameters that should be blended across scenarios
    BLENDABLE_PARAMS = [
        'grid_levels', 'grid_spacing_percent', 'investment_percent',
        'min_order_size_usdt', 'stop_loss_percent', 'check_interval_seconds',
        'atr_period', 'volatility_threshold'
    ]

    # Time-of-day multipliers (UTC hours -> parameter adjustments)
    # Crypto markets have patterns: lower volume during Asian night hours (UTC 0-8)
    TIME_ADJUSTMENTS = {
        # (start_hour, end_hour): {param: multiplier}
        (0, 6): {   # Late night / early morning UTC (low volume)
            'grid_spacing_percent': 1.15,    # Wider spacing
            'investment_percent': 0.85,       # Less capital deployed
            'check_interval_seconds': 1.5,    # Slower checks
        },
        (6, 12): {   # Morning UTC (rising volume)
            'grid_spacing_percent': 1.0,
            'investment_percent': 1.0,
            'check_interval_seconds': 1.0,
        },
        (12, 18): {  # Afternoon UTC (US markets open, peak volume)
            'grid_spacing_percent': 0.95,     # Tighter spacing for more cycles
            'investment_percent': 1.05,        # Slightly more capital
            'check_interval_seconds': 0.85,    # Faster checks
        },
        (18, 24): {  # Evening UTC (mixed volume)
            'grid_spacing_percent': 1.05,
            'investment_percent': 0.95,
            'check_interval_seconds': 1.1,
        },
    }

    def __init__(self, scenarios: List[Dict[str, Any]], regime_detector: MarketRegimeDetector):
        self.scenarios = scenarios
        self.regime_detector = regime_detector
        self.active_params = AdaptiveParameterSet()
        self._scenario_weights: Dict[int, float] = {}
        self._last_blend_time = 0.0
        self._blend_interval = 60  # Re-blend every 60 seconds
        self._override_params: Dict[str, float] = {}  # Manual overrides
        self._transition_speed = 0.3  # EMA alpha for transitions
        self._last_log_time = 0.0
        self._log_interval = 300  # Log parameter state every 5 minutes

        # Initialize with first scenario's params
        if scenarios:
            for param in self.BLENDABLE_PARAMS:
                if param in scenarios[0]:
                    self.active_params.set_immediate(param, float(scenarios[0][param]))

    def compute_blended_params(self, market_data: Optional[Dict] = None) -> AdaptiveParameterSet:
        """
        Compute blended parameters based on current market regime.

        1. Detect market regime
        2. Score each scenario's fit for the regime
        3. Weight-blend all scenario parameters
        4. Apply time-of-day adjustments
        5. Apply safety bounds
        6. Smooth transition from current values
        """
        now = time.time()
        if now - self._last_blend_time < self._blend_interval:
            return self.active_params

        self._last_blend_time = now

        # 1. Detect regime
        regime = self.regime_detector.detect(market_data)

        # 2. Score each scenario
        weights = self._score_scenarios_for_regime(regime, market_data)
        self._scenario_weights = weights

        # 3. Blend parameters
        blended = self._blend_scenario_params(weights)

        # 4. Apply regime-specific overrides
        blended = self._apply_regime_adjustments(blended, regime)

        # 5. Apply time-of-day adjustments
        blended = self._apply_time_adjustments(blended)

        # 6. Apply manual overrides
        for key, val in self._override_params.items():
            blended[key] = val

        # 7. Smooth transition
        self.active_params.update_smooth(blended)

        # Periodic logging
        if now - self._last_log_time > self._log_interval:
            self._last_log_time = now
            stability = self.regime_detector.get_regime_stability()
            top_scenarios = sorted(weights.items(), key=lambda x: x[1], reverse=True)[:3]
            scenario_info = ", ".join(
                f"{self.scenarios[i]['name']}:{w:.0%}" for i, w in top_scenarios if w > 0.05
            )
            logger.info(
                f"[Adaptive] Regime: {regime.primary_regime} ({regime.confidence:.0%}) | "
                f"Stability: {stability:.0%} | Blend: [{scenario_info}]"
            )

        return self.active_params

    def _score_scenarios_for_regime(self, regime: MarketRegime,
                                     market_data: Optional[Dict]) -> Dict[int, float]:
        """Score how well each scenario fits the detected market regime."""
        weights: Dict[int, float] = {}

        volatility = market_data.get('volatility', 3.0) if market_data else 3.0
        adx = market_data.get('adx', 20) if market_data else 20
        rsi = market_data.get('rsi', 50) if market_data else 50

        for i, scenario in enumerate(self.scenarios):
            score = 0.0
            name = scenario['name'].lower()
            spacing = scenario.get('grid_spacing_percent', 1.0)

            # Regime-specific scoring
            if regime.primary_regime == MarketRegime.RANGING:
                if 'balanced' in name or 'mean reversion' in name:
                    score += 0.3
                if spacing < 1.2:
                    score += 0.2
                if adx < 20:
                    score += 0.1

            elif regime.primary_regime == MarketRegime.TRENDING_UP:
                if 'conservative' in name or 'swing' in name:
                    score += 0.3
                if spacing > 1.0:
                    score += 0.15

            elif regime.primary_regime == MarketRegime.TRENDING_DOWN:
                if 'conservative' in name:
                    score += 0.35
                if spacing > 1.2:
                    score += 0.15

            elif regime.primary_regime == MarketRegime.HIGH_VOLATILITY:
                if 'high volatility' in name or 'swing' in name:
                    score += 0.35
                if spacing > 1.5:
                    score += 0.15

            elif regime.primary_regime == MarketRegime.LOW_VOLATILITY:
                if 'low volatility' in name or 'scalping' in name:
                    score += 0.35
                if spacing < 0.7:
                    score += 0.15

            elif regime.primary_regime == MarketRegime.MEAN_REVERTING:
                if 'mean reversion' in name:
                    score += 0.4
                if 'balanced' in name:
                    score += 0.2
                if spacing < 1.0:
                    score += 0.1

            elif regime.primary_regime == MarketRegime.BREAKOUT:
                if 'aggressive' in name or 'high volatility' in name:
                    score += 0.25
                if spacing > 1.0:
                    score += 0.15

            elif regime.primary_regime == MarketRegime.CRASH:
                if 'conservative' in name or 'night' in name:
                    score += 0.4
                if spacing > 1.5:
                    score += 0.1
                # In crash, heavily favor conservative settings
                score += 0.1

            # Volatility fit bonus
            vol_threshold = scenario.get('volatility_threshold', 5)
            if abs(volatility - vol_threshold * 0.5) < 2:
                score += 0.1

            # RSI-based bonus
            if rsi < 30 or rsi > 70:
                if 'mean reversion' in name:
                    score += 0.15

            weights[i] = max(0.01, score)  # Minimum weight to prevent division by zero

        # Normalize weights to sum to 1
        total = sum(weights.values())
        if total > 0:
            for k in weights:
                weights[k] /= total

        return weights

    def _blend_scenario_params(self, weights: Dict[int, float]) -> Dict[str, float]:
        """Blend parameters from all scenarios using computed weights."""
        blended: Dict[str, float] = {}

        for param in self.BLENDABLE_PARAMS:
            weighted_sum = 0.0
            for i, weight in weights.items():
                if i < len(self.scenarios) and param in self.scenarios[i]:
                    weighted_sum += weight * float(self.scenarios[i][param])
            blended[param] = weighted_sum

        return blended

    def _apply_regime_adjustments(self, params: Dict[str, float],
                                   regime: MarketRegime) -> Dict[str, float]:
        """Apply regime-specific parameter adjustments on top of blended values."""
        adjusted = dict(params)

        if regime.primary_regime == MarketRegime.CRASH:
            # Emergency: widen spacing, reduce investment, increase check frequency
            adjusted['grid_spacing_percent'] = max(adjusted.get('grid_spacing_percent', 1.5), 2.0)
            adjusted['investment_percent'] = min(adjusted.get('investment_percent', 50), 40)
            adjusted['check_interval_seconds'] = min(adjusted.get('check_interval_seconds', 30), 30)
            adjusted['stop_loss_percent'] = min(adjusted.get('stop_loss_percent', 10), 8)

        elif regime.primary_regime == MarketRegime.BREAKOUT:
            # Wider spacing to avoid being run over
            adjusted['grid_spacing_percent'] *= 1.3
            adjusted['check_interval_seconds'] *= 0.7  # Check more frequently

        elif regime.primary_regime == MarketRegime.MEAN_REVERTING:
            # Tighter spacing for more cycle completions
            adjusted['grid_spacing_percent'] *= 0.85
            adjusted['grid_levels'] = min(adjusted.get('grid_levels', 10) * 1.2, 20)

        elif regime.primary_regime in (MarketRegime.TRENDING_UP, MarketRegime.TRENDING_DOWN):
            # Trending: reduce grid density, favor wider spacing
            stability = self.regime_detector.get_regime_stability()
            if stability > 0.7:
                # Strong stable trend: significantly adjust
                adjusted['grid_spacing_percent'] *= 1.4
                adjusted['grid_levels'] = max(adjusted.get('grid_levels', 8) * 0.7, 3)
            else:
                adjusted['grid_spacing_percent'] *= 1.15

        return adjusted

    def _apply_time_adjustments(self, params: Dict[str, float]) -> Dict[str, float]:
        """Apply time-of-day based parameter adjustments for 24/7 operation."""
        current_hour = datetime.now(timezone.utc).hour

        for (start, end), multipliers in self.TIME_ADJUSTMENTS.items():
            if start <= current_hour < end:
                for param, mult in multipliers.items():
                    if param in params:
                        params[param] *= mult
                break

        return params

    def set_override(self, param: str, value: float):
        """Set a manual override for a parameter."""
        self._override_params[param] = value

    def clear_override(self, param: str):
        """Clear a manual override."""
        self._override_params.pop(param, None)

    def set_transition_speed(self, alpha: float):
        """Set how fast parameters transition (0.05=very slow, 0.5=fast)."""
        self._transition_speed = max(0.05, min(0.5, alpha))
        self.active_params._smooth_alpha = self._transition_speed

    def get_active_regime(self) -> Optional[MarketRegime]:
        """Get the currently detected market regime."""
        return self.regime_detector._last_regime

    def get_scenario_weights(self) -> Dict[str, float]:
        """Get current scenario weights (for logging/display)."""
        return {
            self.scenarios[i]['name']: w
            for i, w in self._scenario_weights.items()
            if i < len(self.scenarios)
        }

    def get_status(self) -> Dict[str, Any]:
        """Get full adaptive config status."""
        regime = self.regime_detector._last_regime
        return {
            'regime': regime.primary_regime if regime else 'UNKNOWN',
            'regime_confidence': regime.confidence if regime else 0,
            'regime_duration_min': self.regime_detector.get_regime_duration_minutes(),
            'regime_stability': self.regime_detector.get_regime_stability(),
            'scenario_weights': self.get_scenario_weights(),
            'active_params': self.active_params.snapshot(),
            'overrides': dict(self._override_params),
        }

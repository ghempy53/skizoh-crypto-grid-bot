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
# SKIZOH CRYPTO GRID TRADING BOT - Market Analysis Module v14.1
# =============================================================================
# Enhanced with:
# - Wilder's RSI (proper smoothing)
# - Corrected RSI/MACD bias logic
# - ADX trend strength filter
# - Volume-weighted support/resistance
# - Bollinger Bands for volatility
# - Fixed potential index out of bounds errors
# - Better null checking and error handling
# =============================================================================

import numpy as np
import logging
from collections import defaultdict
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class MarketAnalyzer:
    """Advanced market analysis for smart trading decisions."""
    
    def __init__(self, exchange, symbol: str):
        """Initialize market analyzer.
        
        Args:
            exchange: CCXT exchange instance
            symbol (str): Trading pair symbol (e.g., 'ETH/USDT')
        """
        self.exchange = exchange
        self.symbol = symbol
        self._cache: Dict[str, Any] = {}
        self._cache_ttl = 60  # Cache results for 60 seconds
        self._last_fetch = 0
    
    def calculate_rsi_wilder(self, period: int = 14, timeframe: str = '1h') -> Optional[float]:
        """Calculate RSI using Wilder's Smoothed Moving Average (correct method).
        
        Wilder's smoothing uses: α = 1/period (not 2/(period+1) like standard EMA)
        This is the industry-standard RSI calculation.
        
        Args:
            period (int): RSI period (default 14)
            timeframe (str): Timeframe for candles (default '1h')
        
        Returns:
            float: RSI value (0-100), or None if calculation fails
        """
        try:
            # Need more data for proper Wilder smoothing initialization
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, timeframe, limit=period * 3)
            
            if not ohlcv or len(ohlcv) < period + 1:
                logger.warning("Insufficient data for RSI calculation")
                return None
            
            closes = np.array([x[4] for x in ohlcv])
            
            # Calculate price changes
            deltas = np.diff(closes)
            
            if len(deltas) < period:
                return None
            
            # Separate gains and losses
            gains = np.where(deltas > 0, deltas, 0)
            losses = np.where(deltas < 0, -deltas, 0)
            
            # Initialize with SMA for first value
            avg_gain = np.mean(gains[:period])
            avg_loss = np.mean(losses[:period])
            
            # Apply Wilder's smoothing for subsequent values
            for i in range(period, len(gains)):
                avg_gain = (avg_gain * (period - 1) + gains[i]) / period
                avg_loss = (avg_loss * (period - 1) + losses[i]) / period
            
            # Avoid division by zero
            if avg_loss == 0:
                return 100.0
            if avg_gain == 0:
                return 0.0
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
            return float(rsi)
            
        except Exception as e:
            logger.error(f"Failed to calculate RSI: {e}")
            return None
    
    # Alias for backward compatibility
    def calculate_rsi(self, period: int = 14, timeframe: str = '1h') -> Optional[float]:
        """Alias for calculate_rsi_wilder for backward compatibility."""
        return self.calculate_rsi_wilder(period, timeframe)
    
    def calculate_adx(self, period: int = 14, timeframe: str = '1h') -> Optional[Dict[str, Any]]:
        """Calculate Average Directional Index (ADX) for trend strength.
        
        ADX measures trend strength regardless of direction:
        - ADX < 20: Weak/No trend (GOOD for grid trading)
        - ADX 20-25: Developing trend
        - ADX 25-50: Strong trend (CAUTION for grid trading)
        - ADX > 50: Very strong trend (AVOID grid trading)
        
        Args:
            period (int): ADX period (default 14)
            timeframe (str): Timeframe for candles
        
        Returns:
            dict: {'adx': float, 'plus_di': float, 'minus_di': float} or None
        """
        try:
            # Need 2x period + buffer for proper calculation
            limit = period * 3 + 10
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, timeframe, limit=limit)
            
            if not ohlcv or len(ohlcv) < period * 2:
                return None
            
            highs = np.array([x[2] for x in ohlcv])
            lows = np.array([x[3] for x in ohlcv])
            closes = np.array([x[4] for x in ohlcv])
            
            # Calculate True Range
            tr1 = highs[1:] - lows[1:]
            tr2 = np.abs(highs[1:] - closes[:-1])
            tr3 = np.abs(lows[1:] - closes[:-1])
            true_range = np.maximum(tr1, np.maximum(tr2, tr3))
            
            # Calculate Directional Movement
            up_move = highs[1:] - highs[:-1]
            down_move = lows[:-1] - lows[1:]
            
            plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
            minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
            
            # Wilder's smoothing for TR, +DM, -DM
            def wilder_smooth(data: np.ndarray, period: int) -> np.ndarray:
                if len(data) < period:
                    return np.zeros(len(data))
                smoothed = np.zeros(len(data))
                smoothed[period-1] = np.sum(data[:period])
                for i in range(period, len(data)):
                    smoothed[i] = smoothed[i-1] - (smoothed[i-1] / period) + data[i]
                return smoothed
            
            atr = wilder_smooth(true_range, period)
            smooth_plus_dm = wilder_smooth(plus_dm, period)
            smooth_minus_dm = wilder_smooth(minus_dm, period)
            
            # Calculate +DI and -DI
            plus_di = 100 * smooth_plus_dm / np.where(atr > 0, atr, 1)
            minus_di = 100 * smooth_minus_dm / np.where(atr > 0, atr, 1)
            
            # Calculate DX
            di_sum = plus_di + minus_di
            di_diff = np.abs(plus_di - minus_di)
            dx = 100 * di_diff / np.where(di_sum > 0, di_sum, 1)
            
            # Calculate ADX (smoothed DX)
            if len(dx) <= period:
                return None
            
            adx = wilder_smooth(dx[period:], period)
            
            if len(adx) == 0:
                return None
            
            return {
                'adx': float(adx[-1]),
                'plus_di': float(plus_di[-1]),
                'minus_di': float(minus_di[-1]),
                'trend_direction': 'UP' if plus_di[-1] > minus_di[-1] else 'DOWN'
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate ADX: {e}")
            return None
    
    def calculate_macd(self, fast: int = 12, slow: int = 26, signal: int = 9, 
                       timeframe: str = '1h') -> Optional[Dict[str, Any]]:
        """Calculate MACD (Moving Average Convergence Divergence).
        
        Args:
            fast (int): Fast EMA period (default 12)
            slow (int): Slow EMA period (default 26)
            signal (int): Signal line period (default 9)
            timeframe (str): Timeframe for candles (default '1h')
        
        Returns:
            dict: {'macd': float, 'signal': float, 'histogram': float} or None
        """
        try:
            limit = slow + signal + 50  # Extra buffer for EMA stabilization
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, timeframe, limit=limit)
            
            if not ohlcv or len(ohlcv) < slow + signal:
                return None
            
            closes = np.array([x[4] for x in ohlcv])
            
            ema_fast = self._calculate_ema(closes, fast)
            ema_slow = self._calculate_ema(closes, slow)
            
            macd_line = ema_fast - ema_slow
            
            # Ensure we have enough data for signal line
            if len(macd_line) <= slow - 1 + signal:
                return None
            
            signal_line = self._calculate_ema(macd_line[slow-1:], signal)
            
            if len(signal_line) < 2:
                return None
            
            # Align arrays
            macd_val = macd_line[-1]
            signal_val = signal_line[-1]
            histogram = macd_val - signal_val
            
            # Calculate histogram increasing (with bounds checking)
            histogram_increasing = False
            if len(signal_line) >= 2 and len(macd_line) >= 2:
                current_hist = macd_line[-1] - signal_line[-1]
                prev_hist = macd_line[-2] - signal_line[-2]
                histogram_increasing = current_hist > prev_hist
            
            return {
                'macd': float(macd_val),
                'signal': float(signal_val),
                'histogram': float(histogram),
                'histogram_increasing': histogram_increasing
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate MACD: {e}")
            return None
    
    def _calculate_ema(self, data: np.ndarray, period: int) -> np.ndarray:
        """Calculate Exponential Moving Average."""
        if len(data) < period:
            return np.zeros(len(data))
        
        ema = np.zeros(len(data))
        multiplier = 2 / (period + 1)
        
        # First EMA is SMA
        ema[period - 1] = np.mean(data[:period])
        
        for i in range(period, len(data)):
            ema[i] = (data[i] - ema[i-1]) * multiplier + ema[i-1]
        
        return ema
    
    def calculate_bollinger_bands(self, period: int = 20, std_dev: float = 2, 
                                  timeframe: str = '1h') -> Optional[Dict[str, Any]]:
        """Calculate Bollinger Bands for volatility assessment.
        
        Args:
            period (int): SMA period
            std_dev (float): Number of standard deviations
            timeframe (str): Timeframe
        
        Returns:
            dict: {'upper': float, 'middle': float, 'lower': float, 'width': float}
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, timeframe, limit=period + 10)
            
            if not ohlcv or len(ohlcv) < period:
                return None
            
            closes = np.array([x[4] for x in ohlcv])
            
            sma = np.mean(closes[-period:])
            std = np.std(closes[-period:])
            
            upper = sma + (std_dev * std)
            lower = sma - (std_dev * std)
            
            # Band width as percentage of price (measure of volatility)
            width_percent = ((upper - lower) / sma) * 100 if sma > 0 else 0
            
            # Current price position within bands (0 = lower, 1 = upper)
            current_price = closes[-1]
            band_range = upper - lower
            position = (current_price - lower) / band_range if band_range > 0 else 0.5
            
            return {
                'upper': float(upper),
                'middle': float(sma),
                'lower': float(lower),
                'width_percent': float(width_percent),
                'price_position': float(position),
                'current_price': float(current_price)
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate Bollinger Bands: {e}")
            return None
    
    def find_support_resistance(self, lookback_hours: int = 168, 
                                num_levels: int = 5) -> Optional[Dict[str, Any]]:
        """Find support and resistance levels with volume weighting.
        
        Enhanced method:
        - Weight by volume at each price level
        - Consider recency (recent levels matter more)
        - Track number of touches
        
        Args:
            lookback_hours (int): Hours of history (default 168 = 1 week)
            num_levels (int): Number of levels to find
        
        Returns:
            dict: {'support': [...], 'resistance': [...]} with metadata
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, '1h', limit=lookback_hours)
            
            if not ohlcv or len(ohlcv) < 10:
                return None
            
            highs = np.array([x[2] for x in ohlcv])
            lows = np.array([x[3] for x in ohlcv])
            closes = np.array([x[4] for x in ohlcv])
            volumes = np.array([x[5] for x in ohlcv])
            
            current_price = closes[-1]
            if current_price <= 0:
                return None
            
            # Adaptive step size based on price
            price_step = max(1, current_price * 0.002)  # 0.2% clusters
            
            # Create weighted price clusters
            price_clusters: Dict[float, Dict[str, float]] = defaultdict(
                lambda: {'count': 0, 'volume': 0.0, 'recency_score': 0.0}
            )
            
            num_bars = len(highs)
            for i, (high, low, close, volume) in enumerate(zip(highs, lows, closes, volumes)):
                # Recency weight: more recent = higher weight
                recency = (i + 1) / num_bars
                
                for price in [high, low, close]:
                    if price <= 0:
                        continue
                    cluster_key = round(price / price_step) * price_step
                    price_clusters[cluster_key]['count'] += 1
                    price_clusters[cluster_key]['volume'] += volume * recency
                    price_clusters[cluster_key]['recency_score'] += recency
            
            # Calculate composite score for each level
            scored_levels: List[tuple] = []
            for price, data in price_clusters.items():
                # Composite score: touches × volume_weight × recency
                score = data['count'] * np.log1p(data['volume']) * data['recency_score']
                scored_levels.append((price, score, data['count']))
            
            # Sort by score
            scored_levels.sort(key=lambda x: x[1], reverse=True)
            
            # Separate into support and resistance
            support_levels: List[Dict[str, Any]] = []
            resistance_levels: List[Dict[str, Any]] = []
            
            for price, score, touches in scored_levels:
                level_data = {'price': price, 'score': score, 'touches': touches}
                
                if price < current_price * 0.998 and len(support_levels) < num_levels:
                    support_levels.append(level_data)
                elif price > current_price * 1.002 and len(resistance_levels) < num_levels:
                    resistance_levels.append(level_data)
                
                if len(support_levels) >= num_levels and len(resistance_levels) >= num_levels:
                    break
            
            # Sort: support descending, resistance ascending
            support_levels.sort(key=lambda x: x['price'], reverse=True)
            resistance_levels.sort(key=lambda x: x['price'])
            
            return {
                'support': [s['price'] for s in support_levels],
                'resistance': [r['price'] for r in resistance_levels],
                'support_details': support_levels,
                'resistance_details': resistance_levels
            }
            
        except Exception as e:
            logger.error(f"Failed to find support/resistance: {e}")
            return None
    
    def get_market_trend(self) -> Optional[Dict[str, Any]]:
        """Analyze overall market trend using multiple indicators.
        
        Returns:
            dict with trend analysis including ADX-based trend strength
        """
        try:
            rsi = self.calculate_rsi_wilder()
            macd = self.calculate_macd()
            adx = self.calculate_adx()
            
            if rsi is None or macd is None:
                return None
            
            # Base trend from RSI
            trend = 'NEUTRAL'
            strength = 'WEAK'
            
            if rsi < 30:
                trend = 'OVERSOLD'
                strength = 'STRONG' if rsi < 20 else 'MODERATE'
            elif rsi > 70:
                trend = 'OVERBOUGHT'
                strength = 'STRONG' if rsi > 80 else 'MODERATE'
            elif rsi < 45:
                trend = 'BEARISH'
                strength = 'MODERATE'
            elif rsi > 55:
                trend = 'BULLISH'
                strength = 'MODERATE'
            
            # MACD confirmation (FIXED LOGIC)
            if macd['histogram'] > 0:
                if trend in ['BULLISH', 'OVERSOLD']:
                    strength = 'STRONG'  # Momentum confirms
                elif trend == 'BEARISH':
                    strength = 'WEAK'  # Conflicting signals
            else:  # histogram < 0
                if trend in ['BEARISH', 'OVERBOUGHT']:
                    strength = 'STRONG'  # Momentum confirms
                elif trend == 'BULLISH':
                    strength = 'WEAK'  # Conflicting signals
            
            # ADX trend strength assessment
            adx_value = adx['adx'] if adx else 0
            is_trending = adx_value > 25 if adx else False
            is_strong_trend = adx_value > 40 if adx else False
            
            # Grid trading suitability
            grid_suitable = not is_trending  # Grid trading works best in ranging markets
            
            return {
                'trend': trend,
                'strength': strength,
                'rsi': rsi,
                'macd': macd,
                'adx': adx,
                'is_trending': is_trending,
                'is_strong_trend': is_strong_trend,
                'grid_suitable': grid_suitable,
                'adx_value': adx_value
            }
            
        except Exception as e:
            logger.error(f"Failed to get market trend: {e}")
            return None
    
    def should_adjust_grid_bias(self) -> Dict[str, Any]:
        """Determine grid bias with CORRECTED logic.
        
        FIXED: RSI oversold + MACD turning up = BUY signal
               RSI overbought + MACD turning down = SELL signal
        
        Returns:
            dict: {'bias': str, 'buy_weight': float, 'sell_weight': float, 'confidence': str}
        """
        try:
            trend = self.get_market_trend()
            
            if trend is None:
                return {'bias': 'NEUTRAL', 'buy_weight': 0.5, 'sell_weight': 0.5, 'confidence': 'LOW'}
            
            rsi = trend['rsi']
            macd_hist = trend['macd']['histogram']
            macd_increasing = trend['macd'].get('histogram_increasing', False)
            adx_value = trend.get('adx_value', 0)
            
            # Strong trend warning - reduce bias in trending markets
            if adx_value > 35:
                logger.warning(f"Strong trend detected (ADX={adx_value:.1f}), reducing grid bias")
                return {'bias': 'NEUTRAL', 'buy_weight': 0.5, 'sell_weight': 0.5, 
                        'confidence': 'LOW', 'warning': 'STRONG_TREND'}
            
            # CORRECTED LOGIC:
            # Oversold (RSI < 30) + momentum turning up (MACD hist increasing) = STRONG BUY
            # Overbought (RSI > 70) + momentum turning down = STRONG SELL
            
            if rsi < 30:
                if macd_hist > 0 or macd_increasing:
                    # Oversold with bullish momentum = STRONG BUY
                    return {'bias': 'STRONG_BUY', 'buy_weight': 0.70, 'sell_weight': 0.30, 'confidence': 'HIGH'}
                else:
                    # Oversold but still falling = moderate buy (catching falling knife risk)
                    return {'bias': 'BUY', 'buy_weight': 0.60, 'sell_weight': 0.40, 'confidence': 'MEDIUM'}
            
            elif rsi > 70:
                if macd_hist < 0 or not macd_increasing:
                    # Overbought with bearish momentum = STRONG SELL
                    return {'bias': 'STRONG_SELL', 'buy_weight': 0.30, 'sell_weight': 0.70, 'confidence': 'HIGH'}
                else:
                    # Overbought but still rising = moderate sell
                    return {'bias': 'SELL', 'buy_weight': 0.40, 'sell_weight': 0.60, 'confidence': 'MEDIUM'}
            
            elif rsi < 40:
                return {'bias': 'BUY', 'buy_weight': 0.58, 'sell_weight': 0.42, 'confidence': 'MEDIUM'}
            
            elif rsi > 60:
                return {'bias': 'SELL', 'buy_weight': 0.42, 'sell_weight': 0.58, 'confidence': 'MEDIUM'}
            
            else:
                return {'bias': 'NEUTRAL', 'buy_weight': 0.5, 'sell_weight': 0.5, 'confidence': 'MEDIUM'}
                
        except Exception as e:
            logger.error(f"Failed to determine grid bias: {e}")
            return {'bias': 'NEUTRAL', 'buy_weight': 0.5, 'sell_weight': 0.5, 'confidence': 'LOW'}
    
    def is_safe_to_trade(self) -> Dict[str, Any]:
        """Check if market conditions are suitable for grid trading.
        
        Returns:
            dict: {'safe': bool, 'reasons': list, 'recommendation': str}
        """
        try:
            trend = self.get_market_trend()
            bb = self.calculate_bollinger_bands()
            
            reasons: List[str] = []
            warnings: List[str] = []
            
            # Check ADX for trend strength
            if trend and trend.get('adx'):
                adx = trend['adx']['adx']
                if adx > 40:
                    reasons.append(f"Very strong trend (ADX={adx:.1f}) - grid trading not recommended")
                elif adx > 30:
                    warnings.append(f"Moderate trend (ADX={adx:.1f}) - use wider grid spacing")
            
            # Check Bollinger Band width for volatility
            if bb:
                if bb['width_percent'] > 8:
                    warnings.append(f"High volatility (BB width={bb['width_percent']:.1f}%) - use caution")
                if bb['price_position'] < 0.1:
                    warnings.append("Price near lower Bollinger Band - potential bounce zone")
                elif bb['price_position'] > 0.9:
                    warnings.append("Price near upper Bollinger Band - potential reversal zone")
            
            # Check RSI extremes
            if trend and trend['rsi']:
                if trend['rsi'] < 20:
                    warnings.append(f"Extremely oversold (RSI={trend['rsi']:.1f})")
                elif trend['rsi'] > 80:
                    warnings.append(f"Extremely overbought (RSI={trend['rsi']:.1f})")
            
            is_safe = len(reasons) == 0
            
            if not is_safe:
                recommendation = "PAUSE trading until trend weakens"
            elif warnings:
                recommendation = "PROCEED with caution - consider adjusting parameters"
            else:
                recommendation = "SAFE to trade - market conditions favorable for grid strategy"
            
            return {
                'safe': is_safe,
                'reasons': reasons,
                'warnings': warnings,
                'recommendation': recommendation,
                'trend_data': trend,
                'volatility_data': bb
            }
            
        except Exception as e:
            logger.error(f"Failed to check trading safety: {e}")
            return {'safe': False, 'reasons': ['Analysis failed'], 
                    'warnings': [], 'recommendation': 'WAIT'}

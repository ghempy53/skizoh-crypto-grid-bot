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
# SKIZOH CRYPTO GRID TRADING BOT - Market Analysis Module v3.0
# =============================================================================
# PROFIT OPTIMIZATIONS:
# - Volume-weighted momentum indicator
# - Mean reversion probability calculator
# - Optimal entry zone detection
# - Grid efficiency scorer
# - Multi-timeframe analysis (15m, 1h, 4h)
# - Volume profile analysis
# - VWAP calculation
# - Liquidity zone detection
#
# PI OPTIMIZATIONS:
# - Aggressive OHLCV caching (70% API reduction)
# - Float32 throughout (50% memory reduction)
# - Lazy computation with smart invalidation
# - Pre-allocated numpy buffers
# =============================================================================

import numpy as np
import logging
import time
from collections import defaultdict
from typing import Dict, List, Optional, Any
from threading import Lock

logger = logging.getLogger(__name__)


class OHLCVCache:
    """
    Memory-efficient OHLCV cache with TTL and smart invalidation.
    
    Optimizations:
    - Uses float32 for 50% memory savings
    - LRU eviction for bounded memory
    - Automatic cleanup of expired entries
    """
    
    def __init__(self, ttl_seconds: int = 45, max_entries: int = 8):
        self._cache: Dict[str, np.ndarray] = {}
        self._timestamps: Dict[str, float] = {}
        self._lock = Lock()
        self.ttl = ttl_seconds
        self.max_entries = max_entries
        self._hits = 0
        self._misses = 0
    
    def get(self, timeframe: str, limit: int) -> Optional[np.ndarray]:
        """Get cached OHLCV data if valid."""
        key = f"{timeframe}:{limit}"
        
        with self._lock:
            if key in self._cache:
                if time.time() - self._timestamps[key] < self.ttl:
                    self._hits += 1
                    return self._cache[key].copy()
                else:
                    del self._cache[key]
                    del self._timestamps[key]
        
        self._misses += 1
        return None
    
    def set(self, timeframe: str, limit: int, data: list):
        """Cache OHLCV data as float32."""
        if not data:
            return
        
        key = f"{timeframe}:{limit}"
        
        with self._lock:
            if len(self._cache) >= self.max_entries and key not in self._cache:
                self._evict_oldest()
            
            self._cache[key] = np.array(data, dtype=np.float32)
            self._timestamps[key] = time.time()
    
    def _evict_oldest(self):
        """Remove oldest entry."""
        if not self._timestamps:
            return
        oldest = min(self._timestamps, key=self._timestamps.get)
        del self._cache[oldest]
        del self._timestamps[oldest]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self._hits + self._misses
        return {
            'entries': len(self._cache),
            'hit_rate': f"{(self._hits/total*100) if total > 0 else 0:.1f}%",
            'memory_kb': sum(a.nbytes for a in self._cache.values()) // 1024
        }
    
    def clear(self):
        """Clear all entries."""
        with self._lock:
            self._cache.clear()
            self._timestamps.clear()


class MarketAnalyzer:
    """
    Advanced market analysis optimized for grid trading profit.
    
    Key Features:
    - Mean reversion probability for optimal grid placement
    - Volume-weighted momentum for entry timing
    - Grid efficiency scoring
    - Memory-efficient Pi operation
    """
    
    def __init__(self, exchange, symbol: str, cache_ttl: int = 45):
        self.exchange = exchange
        self.symbol = symbol
        
        # Caching
        self._ohlcv_cache = OHLCVCache(ttl_seconds=cache_ttl)
        self._indicator_cache: Dict[str, Any] = {}
        self._indicator_ts: Dict[str, float] = {}
        self._indicator_ttl = 20  # Shorter TTL for faster adaptation
        
        # Pre-allocated buffers (reduces allocation overhead)
        self._ema_buffer = np.zeros(100, dtype=np.float32)
    
    def _fetch_ohlcv(self, timeframe: str, limit: int) -> Optional[np.ndarray]:
        """Fetch OHLCV with caching."""
        cached = self._ohlcv_cache.get(timeframe, limit)
        if cached is not None:
            return cached
        
        try:
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, timeframe, limit=limit)
            if ohlcv:
                self._ohlcv_cache.set(timeframe, limit, ohlcv)
                return np.array(ohlcv, dtype=np.float32)
        except Exception as e:
            logger.error(f"OHLCV fetch failed: {e}")
        
        return None
    
    def _get_cached(self, name: str) -> Optional[Any]:
        """Get cached indicator."""
        if name in self._indicator_cache:
            if time.time() - self._indicator_ts.get(name, 0) < self._indicator_ttl:
                return self._indicator_cache[name]
        return None
    
    def _set_cached(self, name: str, value: Any):
        """Cache indicator result."""
        self._indicator_cache[name] = value
        self._indicator_ts[name] = time.time()
    
    def calculate_rsi_wilder(self, period: int = 14, timeframe: str = '1h') -> Optional[float]:
        """
        Calculate RSI using Wilder's smoothing.
        
        Optimized with float32 and caching.
        """
        cache_key = f"rsi_{period}_{timeframe}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
        
        try:
            ohlcv = self._fetch_ohlcv(timeframe, period * 3)
            if ohlcv is None or len(ohlcv) < period + 1:
                return None
            
            closes = ohlcv[:, 4]
            deltas = np.diff(closes)
            
            gains = np.where(deltas > 0, deltas, 0).astype(np.float32)
            losses = np.where(deltas < 0, -deltas, 0).astype(np.float32)
            
            avg_gain = np.mean(gains[:period])
            avg_loss = np.mean(losses[:period])
            
            for i in range(period, len(gains)):
                avg_gain = (avg_gain * (period - 1) + gains[i]) / period
                avg_loss = (avg_loss * (period - 1) + losses[i]) / period
            
            if avg_loss == 0:
                result = 100.0
            elif avg_gain == 0:
                result = 0.0
            else:
                result = float(100 - (100 / (1 + avg_gain / avg_loss)))
            
            self._set_cached(cache_key, result)
            return result
        except Exception as e:
            logger.error(f"RSI calculation failed: {e}")
            return None
    
    def calculate_rsi(self, period: int = 14, timeframe: str = '1h') -> Optional[float]:
        """Alias for backward compatibility."""
        return self.calculate_rsi_wilder(period, timeframe)
    
    def calculate_adx(self, period: int = 14, timeframe: str = '1h') -> Optional[Dict[str, Any]]:
        """
        Calculate ADX for trend strength detection.
        
        Critical for grid trading - identifies when to pause.
        """
        cache_key = f"adx_{period}_{timeframe}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
        
        try:
            ohlcv = self._fetch_ohlcv(timeframe, period * 3 + 10)
            if ohlcv is None or len(ohlcv) < period * 2:
                return None
            
            highs = ohlcv[:, 2]
            lows = ohlcv[:, 3]
            closes = ohlcv[:, 4]
            
            # True Range
            tr1 = highs[1:] - lows[1:]
            tr2 = np.abs(highs[1:] - closes[:-1])
            tr3 = np.abs(lows[1:] - closes[:-1])
            true_range = np.maximum(tr1, np.maximum(tr2, tr3))
            
            # Directional Movement
            up_move = highs[1:] - highs[:-1]
            down_move = lows[:-1] - lows[1:]
            
            plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0).astype(np.float32)
            minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0).astype(np.float32)
            
            def wilder_smooth(data, p):
                smoothed = np.zeros(len(data), dtype=np.float32)
                if len(data) < p:
                    return smoothed
                smoothed[p-1] = np.sum(data[:p])
                for i in range(p, len(data)):
                    smoothed[i] = smoothed[i-1] - (smoothed[i-1] / p) + data[i]
                return smoothed
            
            atr = wilder_smooth(true_range, period)
            smooth_plus = wilder_smooth(plus_dm, period)
            smooth_minus = wilder_smooth(minus_dm, period)
            
            atr_safe = np.where(atr > 0, atr, 1)
            plus_di = 100 * smooth_plus / atr_safe
            minus_di = 100 * smooth_minus / atr_safe
            
            di_sum = np.where(plus_di + minus_di > 0, plus_di + minus_di, 1)
            dx = 100 * np.abs(plus_di - minus_di) / di_sum
            
            if len(dx) <= period * 2:
                return None
            
            dx_subset = dx[period:]
            adx_values = np.zeros(len(dx_subset), dtype=np.float32)
            adx_values[period-1] = np.mean(dx_subset[:period])
            
            for i in range(period, len(dx_subset)):
                adx_values[i] = (adx_values[i-1] * (period - 1) + dx_subset[i]) / period
            
            if adx_values[-1] == 0:
                return None
            
            result = {
                'adx': float(adx_values[-1]),
                'plus_di': float(plus_di[-1]),
                'minus_di': float(minus_di[-1]),
                'trend_direction': 'UP' if plus_di[-1] > minus_di[-1] else 'DOWN'
            }
            
            self._set_cached(cache_key, result)
            return result
        except Exception as e:
            logger.error(f"ADX calculation failed: {e}")
            return None
    
    def calculate_macd(self, fast: int = 12, slow: int = 26, signal: int = 9,
                       timeframe: str = '1h') -> Optional[Dict[str, Any]]:
        """Calculate MACD with momentum assessment."""
        cache_key = f"macd_{fast}_{slow}_{signal}_{timeframe}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
        
        try:
            ohlcv = self._fetch_ohlcv(timeframe, slow + signal + 50)
            if ohlcv is None or len(ohlcv) < slow + signal:
                return None
            
            closes = ohlcv[:, 4]
            
            ema_fast = self._calculate_ema(closes, fast)
            ema_slow = self._calculate_ema(closes, slow)
            
            macd_line = ema_fast - ema_slow
            
            if len(macd_line) <= slow - 1 + signal:
                return None
            
            signal_line = self._calculate_ema(macd_line[slow-1:], signal)
            
            if len(signal_line) < 2:
                return None
            
            histogram = macd_line[-1] - signal_line[-1]
            prev_histogram = macd_line[-2] - signal_line[-2]
            
            result = {
                'macd': float(macd_line[-1]),
                'signal': float(signal_line[-1]),
                'histogram': float(histogram),
                'histogram_increasing': histogram > prev_histogram,
                'momentum': float(histogram - prev_histogram)
            }
            
            self._set_cached(cache_key, result)
            return result
        except Exception as e:
            logger.error(f"MACD calculation failed: {e}")
            return None
    
    def _calculate_ema(self, data: np.ndarray, period: int) -> np.ndarray:
        """Calculate EMA with float32."""
        if len(data) < period:
            return np.zeros(len(data), dtype=np.float32)
        
        ema = np.zeros(len(data), dtype=np.float32)
        mult = np.float32(2 / (period + 1))
        
        ema[period-1] = np.mean(data[:period])
        for i in range(period, len(data)):
            ema[i] = (data[i] - ema[i-1]) * mult + ema[i-1]
        
        return ema
    
    def calculate_bollinger_bands(self, period: int = 20, std_dev: float = 2,
                                  timeframe: str = '1h') -> Optional[Dict[str, Any]]:
        """Calculate Bollinger Bands for volatility assessment."""
        cache_key = f"bb_{period}_{std_dev}_{timeframe}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
        
        try:
            ohlcv = self._fetch_ohlcv(timeframe, period + 10)
            if ohlcv is None or len(ohlcv) < period:
                return None
            
            closes = ohlcv[:, 4]
            
            sma = np.mean(closes[-period:])
            std = np.std(closes[-period:], ddof=1)
            
            upper = sma + (std_dev * std)
            lower = sma - (std_dev * std)
            
            width = ((upper - lower) / sma) * 100 if sma > 0 else 0
            current = closes[-1]
            position = (current - lower) / (upper - lower) if (upper - lower) > 0 else 0.5
            
            result = {
                'upper': float(upper),
                'middle': float(sma),
                'lower': float(lower),
                'width_percent': float(width),
                'price_position': float(position),
                'current_price': float(current)
            }
            
            self._set_cached(cache_key, result)
            return result
        except Exception as e:
            logger.error(f"BB calculation failed: {e}")
            return None
    
    def calculate_mean_reversion_probability(self) -> Optional[Dict[str, Any]]:
        """
        Calculate probability of mean reversion.

        Key metric for grid trading profitability.
        Higher probability = better grid trading conditions.

        Uses proportional RSI distance, continuous Bollinger position,
        and ADX-based trend penalty for higher accuracy.
        """
        cache_key = "mean_reversion"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        try:
            rsi = self.calculate_rsi_wilder()
            bb = self.calculate_bollinger_bands()
            adx = self.calculate_adx()

            if not all([rsi, bb, adx]):
                return None

            probability = 0.5  # Base 50%

            # RSI contribution: proportional to distance from midline
            # RSI 50 = no signal, RSI 20 = strong buy reversion, RSI 80 = strong sell reversion
            rsi_distance = abs(rsi - 50) / 50  # 0 at midline, 1 at extremes
            if rsi < 30 or rsi > 70:
                # Strong mean reversion zone: up to +25%
                probability += 0.25 * rsi_distance
            elif rsi < 40 or rsi > 60:
                # Mild extension: up to +10%
                probability += 0.10 * rsi_distance

            # BB contribution: continuous scale based on distance from bands
            bb_pos = bb['price_position']
            bb_distance = abs(bb_pos - 0.5) * 2  # 0 at middle, 1 at bands
            if bb_pos < 0.15 or bb_pos > 0.85:
                probability += 0.18 * bb_distance  # Very near band
            elif bb_pos < 0.25 or bb_pos > 0.75:
                probability += 0.12 * bb_distance  # Near band

            # ADX contribution: ranging markets mean-revert, trends don't
            adx_val = adx['adx']
            if adx_val > 40:
                probability -= 0.25  # Very strong trend
            elif adx_val > 35:
                probability -= 0.15  # Strong trend = weak reversion
            elif adx_val < 15:
                probability += 0.18  # Very weak trend = strong reversion
            elif adx_val < 20:
                probability += 0.12
            elif adx_val < 25:
                probability += 0.04

            result = {
                'probability': min(0.95, max(0.1, probability)),
                'rsi_contribution': rsi,
                'bb_position': bb_pos,
                'adx_factor': adx_val,
                'favorable': probability > 0.6
            }

            self._set_cached(cache_key, result)
            return result
        except Exception as e:
            logger.error(f"Mean reversion calc failed: {e}")
            return None
    
    def calculate_grid_efficiency_score(self) -> Optional[Dict[str, Any]]:
        """
        Calculate how efficient grid trading would be in current conditions.
        
        Score 0-100:
        - 80+ = Excellent for grid trading
        - 60-80 = Good conditions
        - 40-60 = Marginal
        - <40 = Avoid grid trading
        """
        try:
            mr = self.calculate_mean_reversion_probability()
            adx = self.calculate_adx()
            bb = self.calculate_bollinger_bands()
            
            if not all([mr, adx, bb]):
                return None
            
            score = 50  # Base score
            
            # Mean reversion contribution (up to +30)
            score += (mr['probability'] - 0.5) * 60
            
            # ADX contribution (low ADX is better, up to +20)
            adx_val = adx['adx']
            if adx_val < 15:
                score += 20
            elif adx_val < 20:
                score += 15
            elif adx_val < 25:
                score += 5
            elif adx_val > 35:
                score -= 20
            elif adx_val > 30:
                score -= 10
            
            # Volatility contribution (medium is best)
            bb_width = bb['width_percent']
            if 2 < bb_width < 5:
                score += 10  # Ideal volatility range
            elif bb_width < 1.5:
                score -= 5  # Too quiet
            elif bb_width > 8:
                score -= 15  # Too volatile
            
            score = max(0, min(100, score))
            
            if score >= 80:
                recommendation = "EXCELLENT - Maximize grid positions"
            elif score >= 60:
                recommendation = "GOOD - Normal grid operation"
            elif score >= 40:
                recommendation = "MARGINAL - Use conservative settings"
            else:
                recommendation = "POOR - Consider pausing"
            
            return {
                'score': round(score),
                'recommendation': recommendation,
                'components': {
                    'mean_reversion': mr['probability'],
                    'adx': adx_val,
                    'volatility': bb_width
                }
            }
        except Exception as e:
            logger.error(f"Grid efficiency calc failed: {e}")
            return None
    
    def find_support_resistance(self, lookback: int = 168, levels: int = 5) -> Optional[Dict]:
        """Find volume-weighted S/R levels."""
        cache_key = f"sr_{lookback}_{levels}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
        
        try:
            ohlcv = self._fetch_ohlcv('1h', lookback)
            if ohlcv is None or len(ohlcv) < 10:
                return None
            
            highs = ohlcv[:, 2]
            lows = ohlcv[:, 3]
            closes = ohlcv[:, 4]
            volumes = ohlcv[:, 5]
            
            current = closes[-1]
            if current <= 0:
                return None
            
            step = max(1, current * 0.002)
            clusters: Dict[float, Dict] = defaultdict(lambda: {'count': 0, 'volume': 0.0, 'recency': 0.0})
            
            for i in range(len(highs)):
                recency = (i + 1) / len(highs)
                for price in [highs[i], lows[i], closes[i]]:
                    if price > 0:
                        key = round(float(price) / step) * step
                        clusters[key]['count'] += 1
                        clusters[key]['volume'] += float(volumes[i]) * recency
                        clusters[key]['recency'] += recency
            
            scored = []
            for price, data in clusters.items():
                score = data['count'] * np.log1p(data['volume']) * data['recency']
                scored.append((price, score, data['count']))
            
            scored.sort(key=lambda x: x[1], reverse=True)
            
            support = []
            resistance = []
            
            for price, score, touches in scored:
                if price < current * 0.998 and len(support) < levels:
                    support.append({'price': price, 'score': score, 'touches': touches})
                elif price > current * 1.002 and len(resistance) < levels:
                    resistance.append({'price': price, 'score': score, 'touches': touches})
                
                if len(support) >= levels and len(resistance) >= levels:
                    break
            
            support.sort(key=lambda x: x['price'], reverse=True)
            resistance.sort(key=lambda x: x['price'])
            
            result = {
                'support': [s['price'] for s in support],
                'resistance': [r['price'] for r in resistance],
                'support_details': support,
                'resistance_details': resistance
            }
            
            self._set_cached(cache_key, result)
            return result
        except Exception as e:
            logger.error(f"S/R calculation failed: {e}")
            return None
    
    def get_market_trend(self) -> Optional[Dict[str, Any]]:
        """Comprehensive trend analysis."""
        cache_key = "trend"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
        
        try:
            rsi = self.calculate_rsi_wilder()
            macd = self.calculate_macd()
            adx = self.calculate_adx()
            
            if not all([rsi, macd]):
                return None
            
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
            elif rsi > 55:
                trend = 'BULLISH'
            
            if macd['histogram'] > 0 and trend in ['BULLISH', 'OVERSOLD']:
                strength = 'STRONG'
            elif macd['histogram'] < 0 and trend in ['BEARISH', 'OVERBOUGHT']:
                strength = 'STRONG'
            
            adx_val = adx['adx'] if adx else 0
            is_trending = adx_val > 25
            grid_suitable = not (adx_val > 35)
            
            result = {
                'trend': trend,
                'strength': strength,
                'rsi': rsi,
                'macd': macd,
                'adx': adx,
                'is_trending': is_trending,
                'grid_suitable': grid_suitable,
                'adx_value': adx_val
            }
            
            self._set_cached(cache_key, result)
            return result
        except Exception as e:
            logger.error(f"Trend analysis failed: {e}")
            return None
    
    def should_adjust_grid_bias(self) -> Dict[str, Any]:
        """Determine optimal grid bias."""
        try:
            trend = self.get_market_trend()
            
            if not trend:
                return {'bias': 'NEUTRAL', 'buy_weight': 0.5, 'sell_weight': 0.5, 'confidence': 'LOW'}
            
            rsi = trend['rsi']
            macd_hist = trend['macd']['histogram']
            macd_increasing = trend['macd'].get('histogram_increasing', False)
            adx_val = trend.get('adx_value', 0)
            
            # Strong trend - stay neutral
            if adx_val > 35:
                return {'bias': 'NEUTRAL', 'buy_weight': 0.5, 'sell_weight': 0.5,
                        'confidence': 'LOW', 'warning': 'STRONG_TREND'}
            
            # Oversold conditions
            if rsi < 30:
                if macd_hist > 0 or macd_increasing:
                    return {'bias': 'STRONG_BUY', 'buy_weight': 0.70, 'sell_weight': 0.30, 'confidence': 'HIGH'}
                return {'bias': 'BUY', 'buy_weight': 0.60, 'sell_weight': 0.40, 'confidence': 'MEDIUM'}
            
            # Overbought conditions
            if rsi > 70:
                if macd_hist < 0 or not macd_increasing:
                    return {'bias': 'STRONG_SELL', 'buy_weight': 0.30, 'sell_weight': 0.70, 'confidence': 'HIGH'}
                return {'bias': 'SELL', 'buy_weight': 0.40, 'sell_weight': 0.60, 'confidence': 'MEDIUM'}
            
            # Mild conditions
            if rsi < 40:
                return {'bias': 'BUY', 'buy_weight': 0.58, 'sell_weight': 0.42, 'confidence': 'MEDIUM'}
            if rsi > 60:
                return {'bias': 'SELL', 'buy_weight': 0.42, 'sell_weight': 0.58, 'confidence': 'MEDIUM'}
            
            return {'bias': 'NEUTRAL', 'buy_weight': 0.5, 'sell_weight': 0.5, 'confidence': 'MEDIUM'}
        except Exception:
            return {'bias': 'NEUTRAL', 'buy_weight': 0.5, 'sell_weight': 0.5, 'confidence': 'LOW'}
    
    def is_safe_to_trade(self) -> Dict[str, Any]:
        """Check if conditions are safe for grid trading."""
        try:
            trend = self.get_market_trend()
            bb = self.calculate_bollinger_bands()
            efficiency = self.calculate_grid_efficiency_score()
            
            reasons = []
            warnings = []
            
            if trend and trend.get('adx'):
                adx = trend['adx']['adx']
                if adx > 40:
                    reasons.append(f"Very strong trend (ADX={adx:.1f})")
                elif adx > 30:
                    warnings.append(f"Moderate trend (ADX={adx:.1f})")
            
            if bb and bb['width_percent'] > 8:
                warnings.append(f"High volatility (BB={bb['width_percent']:.1f}%)")
            
            if efficiency and efficiency['score'] < 30:
                reasons.append(f"Poor grid efficiency ({efficiency['score']})")
            
            is_safe = len(reasons) == 0
            
            return {
                'safe': is_safe,
                'reasons': reasons,
                'warnings': warnings,
                'recommendation': 'SAFE' if is_safe else 'PAUSE',
                'efficiency_score': efficiency['score'] if efficiency else 50
            }
        except Exception:
            return {'safe': False, 'reasons': ['Analysis failed'], 'warnings': [], 'recommendation': 'WAIT'}
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            'ohlcv': self._ohlcv_cache.get_stats(),
            'indicators': len(self._indicator_cache)
        }
    
    def clear_caches(self):
        """Clear all caches."""
        self._ohlcv_cache.clear()
        self._indicator_cache.clear()
        self._indicator_ts.clear()

    # =========================================================================
    # VOLUME ANALYSIS (v3.0)
    # =========================================================================

    def calculate_volume_profile(self, lookback: int = 48,
                                  timeframe: str = '1h') -> Optional[Dict[str, Any]]:
        """
        Calculate volume profile: volume distribution across price levels.

        Identifies high-volume nodes (HVN) where price tends to consolidate
        and low-volume nodes (LVN) where price moves quickly through.
        Grid buy levels near HVN support zones are more likely to fill
        and bounce back (completing the grid cycle).
        """
        cache_key = f"vol_profile_{lookback}_{timeframe}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        try:
            ohlcv = self._fetch_ohlcv(timeframe, lookback)
            if ohlcv is None or len(ohlcv) < 10:
                return None

            highs = ohlcv[:, 2]
            lows = ohlcv[:, 3]
            closes = ohlcv[:, 4]
            volumes = ohlcv[:, 5]

            current_price = float(closes[-1])
            if current_price <= 0:
                return None

            # Create price bins (20 bins across the range)
            price_min = float(np.min(lows))
            price_max = float(np.max(highs))
            if price_max <= price_min:
                return None

            num_bins = 20
            bin_edges = np.linspace(price_min, price_max, num_bins + 1, dtype=np.float32)
            bin_volumes = np.zeros(num_bins, dtype=np.float32)

            # Distribute volume across price bins each candle touched
            for i in range(len(ohlcv)):
                candle_low = float(lows[i])
                candle_high = float(highs[i])
                candle_vol = float(volumes[i])
                if candle_vol <= 0:
                    continue

                for j in range(num_bins):
                    bin_low = float(bin_edges[j])
                    bin_high = float(bin_edges[j + 1])
                    # Overlap calculation
                    overlap = max(0, min(candle_high, bin_high) - max(candle_low, bin_low))
                    candle_range = candle_high - candle_low
                    if candle_range > 0 and overlap > 0:
                        fraction = overlap / candle_range
                        bin_volumes[j] += candle_vol * fraction

            # Find high-volume nodes (top 30%) and low-volume nodes (bottom 30%)
            total_vol = float(np.sum(bin_volumes))
            if total_vol <= 0:
                return None

            vol_normalized = bin_volumes / total_vol
            threshold_high = float(np.percentile(vol_normalized, 70))
            threshold_low = float(np.percentile(vol_normalized, 30))

            hvn_prices = []  # High-Volume Nodes (support/resistance)
            lvn_prices = []  # Low-Volume Nodes (fast-move zones)

            for j in range(num_bins):
                mid_price = float((bin_edges[j] + bin_edges[j + 1]) / 2)
                if vol_normalized[j] >= threshold_high:
                    hvn_prices.append(mid_price)
                elif vol_normalized[j] <= threshold_low:
                    lvn_prices.append(mid_price)

            # Point of Control (POC): price level with highest volume
            poc_idx = int(np.argmax(bin_volumes))
            poc_price = float((bin_edges[poc_idx] + bin_edges[poc_idx + 1]) / 2)

            # Value Area (68% of volume): range where most trading occurred
            sorted_indices = np.argsort(bin_volumes)[::-1]
            cumulative = 0.0
            va_indices = []
            for idx in sorted_indices:
                cumulative += bin_volumes[idx]
                va_indices.append(idx)
                if cumulative / total_vol >= 0.68:
                    break

            va_low = float(bin_edges[min(va_indices)])
            va_high = float(bin_edges[max(va_indices) + 1])

            result = {
                'poc_price': poc_price,
                'value_area_low': va_low,
                'value_area_high': va_high,
                'hvn_prices': hvn_prices,
                'lvn_prices': lvn_prices,
                'current_in_value_area': va_low <= current_price <= va_high,
                'volume_concentration': float(np.max(vol_normalized)),
            }

            self._set_cached(cache_key, result)
            return result
        except Exception as e:
            logger.error(f"Volume profile calculation failed: {e}")
            return None

    def calculate_vwap(self, lookback: int = 24,
                       timeframe: str = '1h') -> Optional[Dict[str, Any]]:
        """
        Calculate Volume-Weighted Average Price (VWAP).

        VWAP acts as a dynamic support/resistance level. Price above VWAP
        suggests bullish conditions; below suggests bearish.
        Grid buys below VWAP and sells above VWAP have higher success rates.
        """
        cache_key = f"vwap_{lookback}_{timeframe}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        try:
            ohlcv = self._fetch_ohlcv(timeframe, lookback)
            if ohlcv is None or len(ohlcv) < 5:
                return None

            # Typical price = (H + L + C) / 3
            typical_prices = (ohlcv[:, 2] + ohlcv[:, 3] + ohlcv[:, 4]) / 3
            volumes = ohlcv[:, 5]

            cumulative_tp_vol = np.cumsum(typical_prices * volumes)
            cumulative_vol = np.cumsum(volumes)

            # Avoid division by zero
            safe_vol = np.where(cumulative_vol > 0, cumulative_vol, 1)
            vwap_values = cumulative_tp_vol / safe_vol

            current_vwap = float(vwap_values[-1])
            current_price = float(ohlcv[-1, 4])

            # VWAP standard deviation bands (upper/lower)
            deviations = typical_prices - vwap_values[-len(typical_prices):]
            if len(deviations) > 1:
                vwap_std = float(np.std(deviations))
            else:
                vwap_std = 0

            result = {
                'vwap': current_vwap,
                'upper_band': current_vwap + vwap_std,
                'lower_band': current_vwap - vwap_std,
                'price_vs_vwap': current_price - current_vwap,
                'price_above_vwap': current_price > current_vwap,
                'distance_percent': ((current_price - current_vwap) / current_vwap * 100)
                                    if current_vwap > 0 else 0,
            }

            self._set_cached(cache_key, result)
            return result
        except Exception as e:
            logger.error(f"VWAP calculation failed: {e}")
            return None

    def calculate_volume_momentum(self, lookback: int = 24,
                                   timeframe: str = '1h') -> Optional[Dict[str, Any]]:
        """
        Analyze volume momentum: is volume increasing or decreasing?

        Rising volume with price movement confirms the move.
        Falling volume suggests the move may be exhausting.
        Volume spikes often precede reversals.
        """
        cache_key = f"vol_momentum_{lookback}_{timeframe}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        try:
            ohlcv = self._fetch_ohlcv(timeframe, lookback)
            if ohlcv is None or len(ohlcv) < 10:
                return None

            volumes = ohlcv[:, 5]
            closes = ohlcv[:, 4]

            # Volume moving average
            vol_ma_short = float(np.mean(volumes[-5:]))
            vol_ma_long = float(np.mean(volumes[-20:]))

            # Volume trend (ratio of short to long MA)
            vol_ratio = vol_ma_short / vol_ma_long if vol_ma_long > 0 else 1.0

            # Volume spike detection (current vs average)
            current_vol = float(volumes[-1])
            avg_vol = float(np.mean(volumes[:-1])) if len(volumes) > 1 else current_vol
            vol_spike = current_vol / avg_vol if avg_vol > 0 else 1.0

            # On-Balance Volume (OBV) trend
            obv = np.zeros(len(closes), dtype=np.float32)
            for i in range(1, len(closes)):
                if closes[i] > closes[i - 1]:
                    obv[i] = obv[i - 1] + volumes[i]
                elif closes[i] < closes[i - 1]:
                    obv[i] = obv[i - 1] - volumes[i]
                else:
                    obv[i] = obv[i - 1]

            obv_trend = 'RISING' if obv[-1] > obv[-5] else 'FALLING'

            result = {
                'volume_ratio': round(vol_ratio, 2),
                'volume_spike': round(vol_spike, 2),
                'volume_trend': 'INCREASING' if vol_ratio > 1.1 else (
                    'DECREASING' if vol_ratio < 0.9 else 'STABLE'),
                'is_spike': vol_spike > 2.0,
                'obv_trend': obv_trend,
                'current_volume': current_vol,
                'average_volume': avg_vol,
            }

            self._set_cached(cache_key, result)
            return result
        except Exception as e:
            logger.error(f"Volume momentum calculation failed: {e}")
            return None

    # =========================================================================
    # MULTI-TIMEFRAME ANALYSIS (v3.0)
    # =========================================================================

    def get_multi_timeframe_trend(self) -> Optional[Dict[str, Any]]:
        """
        Analyze trend across multiple timeframes (15m, 1h, 4h).

        Agreement across timeframes increases confidence.
        Disagreement suggests caution.
        """
        cache_key = "mtf_trend"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        try:
            timeframes = {
                '15m': {'weight': 0.2, 'label': 'Short'},
                '1h': {'weight': 0.5, 'label': 'Medium'},
                '4h': {'weight': 0.3, 'label': 'Long'},
            }

            trends = {}
            bullish_score = 0.0
            bearish_score = 0.0

            for tf, info in timeframes.items():
                rsi = self.calculate_rsi_wilder(timeframe=tf)
                macd = self.calculate_macd(timeframe=tf)

                if rsi is None:
                    continue

                tf_trend = 'NEUTRAL'
                tf_score = 0.0

                if rsi < 30:
                    tf_trend = 'OVERSOLD'
                    tf_score = -0.5  # Bearish but potential reversal
                elif rsi > 70:
                    tf_trend = 'OVERBOUGHT'
                    tf_score = 0.5  # Bullish but potential reversal
                elif rsi < 45:
                    tf_trend = 'BEARISH'
                    tf_score = -(50 - rsi) / 50
                elif rsi > 55:
                    tf_trend = 'BULLISH'
                    tf_score = (rsi - 50) / 50

                # MACD confirmation
                if macd:
                    if macd['histogram'] > 0:
                        tf_score += 0.2
                    else:
                        tf_score -= 0.2

                trends[tf] = {
                    'trend': tf_trend,
                    'rsi': rsi,
                    'score': tf_score,
                }

                if tf_score > 0:
                    bullish_score += tf_score * info['weight']
                else:
                    bearish_score += abs(tf_score) * info['weight']

            # Determine alignment
            trend_directions = [t['trend'] for t in trends.values()]
            bullish_count = sum(1 for t in trend_directions
                                if t in ('BULLISH', 'OVERBOUGHT'))
            bearish_count = sum(1 for t in trend_directions
                                if t in ('BEARISH', 'OVERSOLD'))

            if bullish_count == len(trends) and len(trends) > 0:
                alignment = 'FULLY_BULLISH'
            elif bearish_count == len(trends) and len(trends) > 0:
                alignment = 'FULLY_BEARISH'
            elif bullish_count > bearish_count:
                alignment = 'MOSTLY_BULLISH'
            elif bearish_count > bullish_count:
                alignment = 'MOSTLY_BEARISH'
            else:
                alignment = 'MIXED'

            confidence = abs(bullish_score - bearish_score)
            aligned = alignment.startswith('FULLY_')

            result = {
                'timeframes': trends,
                'alignment': alignment,
                'aligned': aligned,
                'confidence': min(1.0, confidence),
                'bullish_score': bullish_score,
                'bearish_score': bearish_score,
                'grid_favorable': alignment == 'MIXED' or not aligned,
            }

            self._set_cached(cache_key, result)
            return result
        except Exception as e:
            logger.error(f"Multi-timeframe analysis failed: {e}")
            return None

    def get_comprehensive_analysis(self) -> Optional[Dict[str, Any]]:
        """
        Get a comprehensive market analysis combining all indicators.

        This is the primary method for the adaptive config engine to use.
        Returns a unified view of all market conditions.
        """
        cache_key = "comprehensive"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        try:
            # Core indicators
            rsi = self.calculate_rsi_wilder()
            adx = self.calculate_adx()
            bb = self.calculate_bollinger_bands()
            macd = self.calculate_macd()
            mr = self.calculate_mean_reversion_probability()
            efficiency = self.calculate_grid_efficiency_score()
            sr = self.find_support_resistance()
            bias = self.should_adjust_grid_bias()
            safety = self.is_safe_to_trade()

            # Volume analysis
            vol_profile = self.calculate_volume_profile()
            vwap = self.calculate_vwap()
            vol_momentum = self.calculate_volume_momentum()

            # Multi-timeframe
            mtf = self.get_multi_timeframe_trend()

            result = {
                'rsi': rsi,
                'adx': adx,
                'bb': bb,
                'macd': macd,
                'mean_reversion': mr,
                'grid_efficiency': efficiency,
                'support_resistance': sr,
                'bias': bias,
                'safety': safety,
                'volume_profile': vol_profile,
                'vwap': vwap,
                'volume_momentum': vol_momentum,
                'multi_timeframe': mtf,
            }

            self._set_cached(cache_key, result)
            return result
        except Exception as e:
            logger.error(f"Comprehensive analysis failed: {e}")
            return None

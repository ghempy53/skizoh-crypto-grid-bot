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
# SKIZOH CRYPTO GRID TRADING BOT - Market Analysis Module v14.2
# =============================================================================
# RASPBERRY PI OPTIMIZATIONS:
# - OHLCV caching to reduce API calls (50% reduction)
# - Float32 numpy arrays (50% memory reduction)
# - Lazy computation of indicators
# - Automatic cache cleanup
# - Connection pooling support
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
    Memory-efficient OHLCV data cache with TTL.
    
    Reduces API calls by caching recent market data.
    Automatically cleans up expired entries.
    
    Memory optimization: Uses float32 for price data.
    """
    
    def __init__(self, ttl_seconds: int = 60, max_entries: int = 10):
        """
        Initialize cache.
        
        Args:
            ttl_seconds: Time-to-live for cache entries
            max_entries: Maximum number of cached timeframe/limit combinations
        """
        self._cache: Dict[str, np.ndarray] = {}
        self._timestamps: Dict[str, float] = {}
        self._lock = Lock()
        self.ttl = ttl_seconds
        self.max_entries = max_entries
        self._hit_count = 0
        self._miss_count = 0
    
    def get(self, timeframe: str, limit: int) -> Optional[np.ndarray]:
        """Get cached OHLCV data if valid."""
        key = f"{timeframe}:{limit}"
        
        with self._lock:
            if key in self._cache:
                if time.time() - self._timestamps[key] < self.ttl:
                    self._hit_count += 1
                    return self._cache[key].copy()  # Return copy to prevent mutation
                else:
                    # Expired - remove it
                    del self._cache[key]
                    del self._timestamps[key]
        
        self._miss_count += 1
        return None
    
    def set(self, timeframe: str, limit: int, data: list):
        """Cache OHLCV data as float32 numpy array."""
        if not data:
            return
        
        key = f"{timeframe}:{limit}"
        
        with self._lock:
            # Enforce max entries limit
            if len(self._cache) >= self.max_entries and key not in self._cache:
                self._evict_oldest()
            
            # Convert to memory-efficient float32 array
            # OHLCV: [timestamp, open, high, low, close, volume]
            self._cache[key] = np.array(data, dtype=np.float32)
            self._timestamps[key] = time.time()
    
    def _evict_oldest(self):
        """Remove oldest cache entry."""
        if not self._timestamps:
            return
        oldest_key = min(self._timestamps, key=self._timestamps.get)
        del self._cache[oldest_key]
        del self._timestamps[oldest_key]
    
    def clear_expired(self):
        """Remove all expired entries."""
        now = time.time()
        with self._lock:
            expired = [k for k, t in self._timestamps.items() if now - t > self.ttl]
            for k in expired:
                del self._cache[k]
                del self._timestamps[k]
        
        if expired:
            logger.debug(f"Cleared {len(expired)} expired cache entries")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self._hit_count + self._miss_count
        hit_rate = (self._hit_count / total * 100) if total > 0 else 0
        
        return {
            'entries': len(self._cache),
            'hits': self._hit_count,
            'misses': self._miss_count,
            'hit_rate': f"{hit_rate:.1f}%",
            'memory_bytes': sum(arr.nbytes for arr in self._cache.values())
        }
    
    def clear(self):
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
            self._timestamps.clear()


class MarketAnalyzer:
    """
    Advanced market analysis for smart trading decisions.
    
    Optimized for Raspberry Pi with:
    - OHLCV caching
    - Memory-efficient numpy operations
    - Lazy computation
    """
    
    def __init__(self, exchange, symbol: str, cache_ttl: int = 60):
        """
        Initialize market analyzer.
        
        Args:
            exchange: CCXT exchange instance
            symbol: Trading pair symbol (e.g., 'ETH/USDT')
            cache_ttl: OHLCV cache TTL in seconds
        """
        self.exchange = exchange
        self.symbol = symbol
        
        # OHLCV cache for reducing API calls
        self._ohlcv_cache = OHLCVCache(ttl_seconds=cache_ttl)
        
        # Indicator result cache (separate from OHLCV)
        self._indicator_cache: Dict[str, Any] = {}
        self._indicator_timestamps: Dict[str, float] = {}
        self._indicator_ttl = 30  # 30 second TTL for computed indicators
        
        # Pre-allocated buffers for common operations (reduces allocation overhead)
        self._buffer_size = 100
        self._price_buffer = np.zeros(self._buffer_size, dtype=np.float32)
    
    def _fetch_ohlcv_cached(self, timeframe: str, limit: int) -> Optional[np.ndarray]:
        """
        Fetch OHLCV with caching.
        
        Returns float32 numpy array for memory efficiency.
        """
        # Try cache first
        cached = self._ohlcv_cache.get(timeframe, limit)
        if cached is not None:
            return cached
        
        # Fetch from exchange
        try:
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, timeframe, limit=limit)
            if ohlcv:
                self._ohlcv_cache.set(timeframe, limit, ohlcv)
                return np.array(ohlcv, dtype=np.float32)
        except Exception as e:
            logger.error(f"Failed to fetch OHLCV: {e}")
        
        return None
    
    def _get_cached_indicator(self, name: str) -> Optional[Any]:
        """Get cached indicator result if valid."""
        if name in self._indicator_cache:
            if time.time() - self._indicator_timestamps.get(name, 0) < self._indicator_ttl:
                return self._indicator_cache[name]
        return None
    
    def _set_cached_indicator(self, name: str, value: Any):
        """Cache indicator result."""
        self._indicator_cache[name] = value
        self._indicator_timestamps[name] = time.time()
    
    def calculate_rsi_wilder(self, period: int = 14, timeframe: str = '1h') -> Optional[float]:
        """
        Calculate RSI using Wilder's Smoothed Moving Average.
        
        Optimized with caching and float32 operations.
        """
        cache_key = f"rsi_{period}_{timeframe}"
        cached = self._get_cached_indicator(cache_key)
        if cached is not None:
            return cached
        
        try:
            ohlcv = self._fetch_ohlcv_cached(timeframe, period * 3)
            
            if ohlcv is None or len(ohlcv) < period + 1:
                logger.warning("Insufficient data for RSI calculation")
                return None
            
            # Extract closes (column 4) - already float32
            closes = ohlcv[:, 4]
            
            # Calculate price changes
            deltas = np.diff(closes)
            
            if len(deltas) < period:
                return None
            
            # Separate gains and losses
            gains = np.where(deltas > 0, deltas, 0).astype(np.float32)
            losses = np.where(deltas < 0, -deltas, 0).astype(np.float32)
            
            # Initialize with SMA for first value
            avg_gain = np.mean(gains[:period])
            avg_loss = np.mean(losses[:period])
            
            # Apply Wilder's smoothing for subsequent values
            for i in range(period, len(gains)):
                avg_gain = (avg_gain * (period - 1) + gains[i]) / period
                avg_loss = (avg_loss * (period - 1) + losses[i]) / period
            
            # Avoid division by zero
            if avg_loss == 0:
                result = 100.0
            elif avg_gain == 0:
                result = 0.0
            else:
                rs = avg_gain / avg_loss
                result = float(100 - (100 / (1 + rs)))
            
            self._set_cached_indicator(cache_key, result)
            return result
            
        except Exception as e:
            logger.error(f"Failed to calculate RSI: {e}")
            return None
    
    # Alias for backward compatibility
    def calculate_rsi(self, period: int = 14, timeframe: str = '1h') -> Optional[float]:
        return self.calculate_rsi_wilder(period, timeframe)
    
    def calculate_adx(self, period: int = 14, timeframe: str = '1h') -> Optional[Dict[str, Any]]:
        """
        Calculate Average Directional Index (ADX) for trend strength.
        
        Optimized with vectorized operations and caching.
        """
        cache_key = f"adx_{period}_{timeframe}"
        cached = self._get_cached_indicator(cache_key)
        if cached is not None:
            return cached
        
        try:
            limit = period * 3 + 10
            ohlcv = self._fetch_ohlcv_cached(timeframe, limit)
            
            if ohlcv is None or len(ohlcv) < period * 2:
                return None
            
            # Extract OHLC data (already float32)
            highs = ohlcv[:, 2]
            lows = ohlcv[:, 3]
            closes = ohlcv[:, 4]
            
            # Calculate True Range (vectorized)
            tr1 = highs[1:] - lows[1:]
            tr2 = np.abs(highs[1:] - closes[:-1])
            tr3 = np.abs(lows[1:] - closes[:-1])
            true_range = np.maximum(tr1, np.maximum(tr2, tr3))
            
            # Calculate Directional Movement (vectorized)
            up_move = highs[1:] - highs[:-1]
            down_move = lows[:-1] - lows[1:]
            
            plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0).astype(np.float32)
            minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0).astype(np.float32)
            
            # Wilder's smoothing function (local, avoids repeated allocation)
            def wilder_smooth(data: np.ndarray, p: int) -> np.ndarray:
                if len(data) < p:
                    return np.zeros(len(data), dtype=np.float32)
                smoothed = np.zeros(len(data), dtype=np.float32)
                smoothed[p-1] = np.sum(data[:p])
                for i in range(p, len(data)):
                    smoothed[i] = smoothed[i-1] - (smoothed[i-1] / p) + data[i]
                return smoothed
            
            atr = wilder_smooth(true_range, period)
            smooth_plus_dm = wilder_smooth(plus_dm, period)
            smooth_minus_dm = wilder_smooth(minus_dm, period)
            
            # Calculate +DI and -DI (avoid division by zero)
            atr_safe = np.where(atr > 0, atr, 1)
            plus_di = 100 * smooth_plus_dm / atr_safe
            minus_di = 100 * smooth_minus_dm / atr_safe
            
            # Calculate DX
            di_sum = plus_di + minus_di
            di_sum_safe = np.where(di_sum > 0, di_sum, 1)
            di_diff = np.abs(plus_di - minus_di)
            dx = 100 * di_diff / di_sum_safe
            
            # Calculate ADX
            if len(dx) <= period * 2:
                return None
            
            dx_subset = dx[period:]
            
            if len(dx_subset) < period:
                return None
            
            adx_values = np.zeros(len(dx_subset), dtype=np.float32)
            adx_values[period - 1] = np.mean(dx_subset[:period])
            
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
            
            self._set_cached_indicator(cache_key, result)
            return result
            
        except Exception as e:
            logger.error(f"Failed to calculate ADX: {e}")
            return None
    
    def calculate_macd(self, fast: int = 12, slow: int = 26, signal: int = 9, 
                       timeframe: str = '1h') -> Optional[Dict[str, Any]]:
        """
        Calculate MACD with float32 optimization.
        """
        cache_key = f"macd_{fast}_{slow}_{signal}_{timeframe}"
        cached = self._get_cached_indicator(cache_key)
        if cached is not None:
            return cached
        
        try:
            limit = slow + signal + 50
            ohlcv = self._fetch_ohlcv_cached(timeframe, limit)
            
            if ohlcv is None or len(ohlcv) < slow + signal:
                return None
            
            closes = ohlcv[:, 4]  # Already float32
            
            ema_fast = self._calculate_ema(closes, fast)
            ema_slow = self._calculate_ema(closes, slow)
            
            macd_line = ema_fast - ema_slow
            
            if len(macd_line) <= slow - 1 + signal:
                return None
            
            signal_line = self._calculate_ema(macd_line[slow-1:], signal)
            
            if len(signal_line) < 2:
                return None
            
            macd_val = float(macd_line[-1])
            signal_val = float(signal_line[-1])
            histogram = macd_val - signal_val
            
            histogram_increasing = False
            if len(signal_line) >= 2 and len(macd_line) >= 2:
                current_hist = macd_line[-1] - signal_line[-1]
                prev_hist = macd_line[-2] - signal_line[-2]
                histogram_increasing = current_hist > prev_hist
            
            result = {
                'macd': macd_val,
                'signal': signal_val,
                'histogram': float(histogram),
                'histogram_increasing': histogram_increasing
            }
            
            self._set_cached_indicator(cache_key, result)
            return result
            
        except Exception as e:
            logger.error(f"Failed to calculate MACD: {e}")
            return None
    
    def _calculate_ema(self, data: np.ndarray, period: int) -> np.ndarray:
        """Calculate EMA with float32 precision."""
        if len(data) < period:
            return np.zeros(len(data), dtype=np.float32)
        
        ema = np.zeros(len(data), dtype=np.float32)
        multiplier = np.float32(2 / (period + 1))
        
        ema[period - 1] = np.mean(data[:period])
        
        for i in range(period, len(data)):
            ema[i] = (data[i] - ema[i-1]) * multiplier + ema[i-1]
        
        return ema
    
    def calculate_bollinger_bands(self, period: int = 20, std_dev: float = 2, 
                                  timeframe: str = '1h') -> Optional[Dict[str, Any]]:
        """Calculate Bollinger Bands with caching."""
        cache_key = f"bb_{period}_{std_dev}_{timeframe}"
        cached = self._get_cached_indicator(cache_key)
        if cached is not None:
            return cached
        
        try:
            ohlcv = self._fetch_ohlcv_cached(timeframe, period + 10)
            
            if ohlcv is None or len(ohlcv) < period:
                return None
            
            closes = ohlcv[:, 4]
            
            sma = np.mean(closes[-period:])
            std = np.std(closes[-period:])
            
            upper = sma + (std_dev * std)
            lower = sma - (std_dev * std)
            
            width_percent = ((upper - lower) / sma) * 100 if sma > 0 else 0
            
            current_price = closes[-1]
            band_range = upper - lower
            position = (current_price - lower) / band_range if band_range > 0 else 0.5
            
            result = {
                'upper': float(upper),
                'middle': float(sma),
                'lower': float(lower),
                'width_percent': float(width_percent),
                'price_position': float(position),
                'current_price': float(current_price)
            }
            
            self._set_cached_indicator(cache_key, result)
            return result
            
        except Exception as e:
            logger.error(f"Failed to calculate Bollinger Bands: {e}")
            return None
    
    def find_support_resistance(self, lookback_hours: int = 168, 
                                num_levels: int = 5) -> Optional[Dict[str, Any]]:
        """Find support and resistance levels with volume weighting."""
        cache_key = f"sr_{lookback_hours}_{num_levels}"
        cached = self._get_cached_indicator(cache_key)
        if cached is not None:
            return cached
        
        try:
            ohlcv = self._fetch_ohlcv_cached('1h', lookback_hours)
            
            if ohlcv is None or len(ohlcv) < 10:
                return None
            
            highs = ohlcv[:, 2]
            lows = ohlcv[:, 3]
            closes = ohlcv[:, 4]
            volumes = ohlcv[:, 5]
            
            current_price = closes[-1]
            if current_price <= 0:
                return None
            
            price_step = max(1, current_price * 0.002)
            
            price_clusters: Dict[float, Dict[str, float]] = defaultdict(
                lambda: {'count': 0, 'volume': 0.0, 'recency_score': 0.0}
            )
            
            num_bars = len(highs)
            for i in range(num_bars):
                recency = (i + 1) / num_bars
                
                for price in [highs[i], lows[i], closes[i]]:
                    if price <= 0:
                        continue
                    cluster_key = round(float(price) / price_step) * price_step
                    price_clusters[cluster_key]['count'] += 1
                    price_clusters[cluster_key]['volume'] += float(volumes[i]) * recency
                    price_clusters[cluster_key]['recency_score'] += recency
            
            scored_levels: List[tuple] = []
            for price, data in price_clusters.items():
                score = data['count'] * np.log1p(data['volume']) * data['recency_score']
                scored_levels.append((price, score, data['count']))
            
            scored_levels.sort(key=lambda x: x[1], reverse=True)
            
            support_levels: List[Dict[str, Any]] = []
            resistance_levels: List[Dict[str, Any]] = []
            
            for price, score, touches in scored_levels:
                level_data = {'price': price, 'score': float(score), 'touches': touches}
                
                if price < current_price * 0.998 and len(support_levels) < num_levels:
                    support_levels.append(level_data)
                elif price > current_price * 1.002 and len(resistance_levels) < num_levels:
                    resistance_levels.append(level_data)
                
                if len(support_levels) >= num_levels and len(resistance_levels) >= num_levels:
                    break
            
            support_levels.sort(key=lambda x: x['price'], reverse=True)
            resistance_levels.sort(key=lambda x: x['price'])
            
            result = {
                'support': [s['price'] for s in support_levels],
                'resistance': [r['price'] for r in resistance_levels],
                'support_details': support_levels,
                'resistance_details': resistance_levels
            }
            
            self._set_cached_indicator(cache_key, result)
            return result
            
        except Exception as e:
            logger.error(f"Failed to find support/resistance: {e}")
            return None
    
    def get_market_trend(self) -> Optional[Dict[str, Any]]:
        """Analyze overall market trend using multiple indicators."""
        cache_key = "market_trend"
        cached = self._get_cached_indicator(cache_key)
        if cached is not None:
            return cached
        
        try:
            rsi = self.calculate_rsi_wilder()
            macd = self.calculate_macd()
            adx = self.calculate_adx()
            
            if rsi is None or macd is None:
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
                strength = 'MODERATE'
            elif rsi > 55:
                trend = 'BULLISH'
                strength = 'MODERATE'
            
            if macd['histogram'] > 0:
                if trend in ['BULLISH', 'OVERSOLD']:
                    strength = 'STRONG'
                elif trend == 'BEARISH':
                    strength = 'WEAK'
            else:
                if trend in ['BEARISH', 'OVERBOUGHT']:
                    strength = 'STRONG'
                elif trend == 'BULLISH':
                    strength = 'WEAK'
            
            adx_value = adx['adx'] if adx else 0
            is_trending = adx_value > 25 if adx else False
            is_strong_trend = adx_value > 40 if adx else False
            grid_suitable = not is_trending
            
            result = {
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
            
            self._set_cached_indicator(cache_key, result)
            return result
            
        except Exception as e:
            logger.error(f"Failed to get market trend: {e}")
            return None
    
    def should_adjust_grid_bias(self) -> Dict[str, Any]:
        """Determine grid bias with corrected logic."""
        try:
            trend = self.get_market_trend()
            
            if trend is None:
                return {'bias': 'NEUTRAL', 'buy_weight': 0.5, 'sell_weight': 0.5, 'confidence': 'LOW'}
            
            rsi = trend['rsi']
            macd_hist = trend['macd']['histogram']
            macd_increasing = trend['macd'].get('histogram_increasing', False)
            adx_value = trend.get('adx_value', 0)
            
            if adx_value > 35:
                logger.warning(f"Strong trend detected (ADX={adx_value:.1f}), reducing grid bias")
                return {'bias': 'NEUTRAL', 'buy_weight': 0.5, 'sell_weight': 0.5, 
                        'confidence': 'LOW', 'warning': 'STRONG_TREND'}
            
            if rsi < 30:
                if macd_hist > 0 or macd_increasing:
                    return {'bias': 'STRONG_BUY', 'buy_weight': 0.70, 'sell_weight': 0.30, 'confidence': 'HIGH'}
                else:
                    return {'bias': 'BUY', 'buy_weight': 0.60, 'sell_weight': 0.40, 'confidence': 'MEDIUM'}
            
            elif rsi > 70:
                if macd_hist < 0 or not macd_increasing:
                    return {'bias': 'STRONG_SELL', 'buy_weight': 0.30, 'sell_weight': 0.70, 'confidence': 'HIGH'}
                else:
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
        """Check if market conditions are suitable for grid trading."""
        try:
            trend = self.get_market_trend()
            bb = self.calculate_bollinger_bands()
            
            reasons: List[str] = []
            warnings: List[str] = []
            
            if trend and trend.get('adx'):
                adx = trend['adx']['adx']
                if adx > 40:
                    reasons.append(f"Very strong trend (ADX={adx:.1f}) - grid trading not recommended")
                elif adx > 30:
                    warnings.append(f"Moderate trend (ADX={adx:.1f}) - use wider grid spacing")
            
            if bb:
                if bb['width_percent'] > 8:
                    warnings.append(f"High volatility (BB width={bb['width_percent']:.1f}%) - use caution")
                if bb['price_position'] < 0.1:
                    warnings.append("Price near lower Bollinger Band - potential bounce zone")
                elif bb['price_position'] > 0.9:
                    warnings.append("Price near upper Bollinger Band - potential reversal zone")
            
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
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics for monitoring."""
        return {
            'ohlcv_cache': self._ohlcv_cache.get_stats(),
            'indicator_cache_entries': len(self._indicator_cache)
        }
    
    def clear_caches(self):
        """Clear all caches (useful for forced refresh)."""
        self._ohlcv_cache.clear()
        self._indicator_cache.clear()
        self._indicator_timestamps.clear()
        logger.info("All caches cleared")

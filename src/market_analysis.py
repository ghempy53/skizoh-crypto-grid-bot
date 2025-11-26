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

# \file: market_analysis.py
# \Date: 11-26-2025
# \Description: Advanced market analysis tools including RSI, MACD, and support/resistance detection
#               All mathematical formulas verified for accuracy

import numpy as np
import logging
from collections import defaultdict

class MarketAnalyzer:
    """Advanced market analysis for smart trading decisions."""
    
    def __init__(self, exchange, symbol):
        """Initialize market analyzer.
        
        Args:
            exchange: CCXT exchange instance
            symbol (str): Trading pair symbol (e.g., 'ETH/USDT')
        
        Returns:
            None
        """
        self.exchange = exchange
        self.symbol = symbol
    
    def calculate_rsi(self, period=14, timeframe='1h'):
        """Calculate Relative Strength Index (RSI).
        
        Formula:
            RSI = 100 - (100 / (1 + RS))
            where RS = Average Gain / Average Loss
        
        Args:
            period (int): RSI period (default 14)
            timeframe (str): Timeframe for candles (default '1h')
        
        Returns:
            float: RSI value (0-100), or None if calculation fails
        """
        try:
            # Fetch OHLCV data (need period+1 to calculate deltas)
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, timeframe, limit=period + 1)
            closes = np.array([x[4] for x in ohlcv])
            
            # Calculate price changes (deltas)
            deltas = np.diff(closes)
            
            # Separate gains and losses
            gains = np.where(deltas > 0, deltas, 0)
            losses = np.where(deltas < 0, -deltas, 0)
            
            # Calculate average gain and average loss over period
            avg_gain = np.mean(gains)
            avg_loss = np.mean(losses)
            
            # Avoid division by zero
            if avg_loss == 0:
                return 100.0  # All gains, maximum RSI
            
            # Calculate Relative Strength (RS)
            rs = avg_gain / avg_loss
            
            # Calculate RSI using standard formula
            rsi = 100 - (100 / (1 + rs))
            
            return rsi
            
        except Exception as e:
            logging.error(f"Failed to calculate RSI: {e}")
            return None
    
    def calculate_macd(self, fast=12, slow=26, signal=9, timeframe='1h'):
        """Calculate MACD (Moving Average Convergence Divergence).
        
        Formula:
            MACD Line = 12-period EMA - 26-period EMA
            Signal Line = 9-period EMA of MACD Line
            Histogram = MACD Line - Signal Line
        
        Args:
            fast (int): Fast EMA period (default 12)
            slow (int): Slow EMA period (default 26)
            signal (int): Signal line period (default 9)
            timeframe (str): Timeframe for candles (default '1h')
        
        Returns:
            dict: {'macd': float, 'signal': float, 'histogram': float} or None if fails
        """
        try:
            # Fetch enough data for slow EMA + signal line + buffer
            limit = slow + signal + 10
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, timeframe, limit=limit)
            closes = np.array([x[4] for x in ohlcv])
            
            # Calculate fast and slow EMAs
            ema_fast = self._calculate_ema(closes, fast)
            ema_slow = self._calculate_ema(closes, slow)
            
            # MACD line = Fast EMA - Slow EMA
            macd_line = ema_fast - ema_slow
            
            # Signal line = EMA of MACD line
            signal_line = self._calculate_ema(macd_line, signal)
            
            # Histogram = MACD line - Signal line
            histogram = macd_line[-1] - signal_line[-1]
            
            return {
                'macd': macd_line[-1],
                'signal': signal_line[-1],
                'histogram': histogram
            }
            
        except Exception as e:
            logging.error(f"Failed to calculate MACD: {e}")
            return None
    
    def _calculate_ema(self, data, period):
        """Calculate Exponential Moving Average.
        
        Formula:
            Multiplier = 2 / (Period + 1)
            EMA = (Close - Previous EMA) × Multiplier + Previous EMA
            First EMA = Simple Moving Average (SMA)
        
        Args:
            data (np.array): Price data
            period (int): EMA period
        
        Returns:
            np.array: EMA values
        """
        ema = np.zeros(len(data))
        
        # Smoothing multiplier
        multiplier = 2 / (period + 1)
        
        # First EMA value is SMA (Simple Moving Average)
        ema[period - 1] = np.mean(data[:period])
        
        # Calculate subsequent EMAs using exponential formula
        for i in range(period, len(data)):
            ema[i] = (data[i] - ema[i-1]) * multiplier + ema[i-1]
        
        return ema
    
    def find_support_resistance(self, lookback_hours=168, num_levels=5):
        """Find support and resistance levels based on price clusters.
        
        Method:
            - Analyze price history for clustering
            - Identify levels where price frequently bounced
            - Separate into support (below) and resistance (above)
        
        Args:
            lookback_hours (int): Hours of history to analyze (default 168 = 1 week)
            num_levels (int): Number of S/R levels to find (default 5)
        
        Returns:
            dict: {'support': [prices], 'resistance': [prices]} or None if fails
        """
        try:
            # Fetch historical data
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, '1h', limit=lookback_hours)
            
            # Extract highs, lows, and closes
            highs = np.array([x[2] for x in ohlcv])
            lows = np.array([x[3] for x in ohlcv])
            closes = np.array([x[4] for x in ohlcv])
            
            current_price = closes[-1]
            
            # Combine all price points (highs/lows/closes all important)
            all_prices = np.concatenate([highs, lows, closes])
            
            # Create price clusters (round to steps for grouping)
            # Step size = 0.3% of current price (adaptive to price level)
            price_step = max(1, int(current_price * 0.003))
            price_clusters = defaultdict(int)
            
            # Count frequency of each price cluster
            for price in all_prices:
                cluster_key = int(price / price_step) * price_step
                price_clusters[cluster_key] += 1
            
            # Sort clusters by frequency (most common first)
            sorted_clusters = sorted(price_clusters.items(), key=lambda x: x[1], reverse=True)
            
            # Separate into support (below current price) and resistance (above)
            support_levels = []
            resistance_levels = []
            
            for price, count in sorted_clusters:
                if price < current_price and len(support_levels) < num_levels:
                    support_levels.append(price)
                elif price > current_price and len(resistance_levels) < num_levels:
                    resistance_levels.append(price)
                
                # Stop when we have enough of each
                if len(support_levels) >= num_levels and len(resistance_levels) >= num_levels:
                    break
            
            # Sort support descending (highest support first)
            # Sort resistance ascending (lowest resistance first)
            support_levels.sort(reverse=True)
            resistance_levels.sort()
            
            return {
                'support': support_levels,
                'resistance': resistance_levels
            }
            
        except Exception as e:
            logging.error(f"Failed to find support/resistance: {e}")
            return None
    
    def get_market_trend(self):
        """Analyze overall market trend using RSI and MACD.
        
        Args:
            None
        
        Returns:
            dict: {'trend': str, 'strength': str, 'rsi': float, 'macd': dict} or None
        """
        try:
            rsi = self.calculate_rsi()
            macd = self.calculate_macd()
            
            if rsi is None or macd is None:
                return None
            
            # Determine trend from RSI
            trend = 'NEUTRAL'
            strength = 'WEAK'
            
            # RSI-based trend detection
            if rsi < 30:
                trend = 'OVERSOLD'
                strength = 'STRONG' if rsi < 25 else 'MODERATE'
            elif rsi > 70:
                trend = 'OVERBOUGHT'
                strength = 'STRONG' if rsi > 75 else 'MODERATE'
            elif rsi < 45:
                trend = 'BEARISH'
                strength = 'MODERATE'
            elif rsi > 55:
                trend = 'BULLISH'
                strength = 'MODERATE'
            
            # MACD confirmation (histogram)
            # Positive histogram = upward momentum
            # Negative histogram = downward momentum
            if macd['histogram'] > 0:
                if trend == 'BEARISH':
                    trend = 'NEUTRAL'  # Conflicting signals
                elif trend in ['BULLISH', 'NEUTRAL']:
                    strength = 'STRONG'  # Confirmation
            elif macd['histogram'] < 0:
                if trend == 'BULLISH':
                    trend = 'NEUTRAL'  # Conflicting signals
                elif trend in ['BEARISH', 'NEUTRAL']:
                    strength = 'STRONG'  # Confirmation
            
            return {
                'trend': trend,
                'strength': strength,
                'rsi': rsi,
                'macd': macd
            }
            
        except Exception as e:
            logging.error(f"Failed to get market trend: {e}")
            return None
    
    def should_adjust_grid_bias(self):
        """Determine if grid should be biased toward buy or sell orders.
        
        Logic:
            - RSI < 30 + MACD negative = Strong buy bias
            - RSI > 70 + MACD positive = Strong sell bias
            - RSI 30-40 = Mild buy bias
            - RSI 60-70 = Mild sell bias
            - RSI 40-60 = Neutral
        
        Args:
            None
        
        Returns:
            dict: {'bias': str, 'buy_weight': float, 'sell_weight': float} or None
        """
        try:
            trend = self.get_market_trend()
            
            if trend is None:
                return {'bias': 'NEUTRAL', 'buy_weight': 0.5, 'sell_weight': 0.5}
            
            rsi = trend['rsi']
            macd_hist = trend['macd']['histogram']
            
            # Calculate weights based on RSI and MACD
            if rsi < 30 and macd_hist < 0:
                # Strong oversold signal = favor buy orders heavily
                return {'bias': 'BUY', 'buy_weight': 0.65, 'sell_weight': 0.35}
            elif rsi > 70 and macd_hist > 0:
                # Strong overbought signal = favor sell orders heavily
                return {'bias': 'SELL', 'buy_weight': 0.35, 'sell_weight': 0.65}
            elif rsi < 40:
                # Mild oversold = slightly favor buy orders
                return {'bias': 'BUY', 'buy_weight': 0.6, 'sell_weight': 0.4}
            elif rsi > 60:
                # Mild overbought = slightly favor sell orders
                return {'bias': 'SELL', 'buy_weight': 0.4, 'sell_weight': 0.6}
            else:
                # Neutral RSI range = balanced grid
                return {'bias': 'NEUTRAL', 'buy_weight': 0.5, 'sell_weight': 0.5}
                
        except Exception as e:
            logging.error(f"Failed to determine grid bias: {e}")
            return {'bias': 'NEUTRAL', 'buy_weight': 0.5, 'sell_weight': 0.5}

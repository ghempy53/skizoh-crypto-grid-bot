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

# \file: config_manager.py
# \Date: 11-26-2025
# \Description: Configuration management with multi-scenario support and market analysis

# =============================================================================
# SKIZOH CRYPTO GRID TRADING BOT - Configuration Manager
# =============================================================================
# Enhanced with ADX-based scenario recommendations
# =============================================================================

import json
import logging
import ccxt
import numpy as np
from market_analysis import MarketAnalyzer

class ConfigManager:
    """Manage multi-scenario configurations with enhanced market analysis."""
    
    def __init__(self, config_file='config.json'):
        """Initialize configuration manager."""
        self.config_file = config_file
        self.config = None
        self.scenarios = []
        self.selected_scenario = None
        
    def load_config(self):
        """Load configuration from JSON file."""
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
            
            self.scenarios = self.config['config_data']
            logging.info(f"Loaded {len(self.scenarios)} trading scenarios")
            
            return self.config
            
        except FileNotFoundError:
            logging.error(f"Config file not found: {self.config_file}")
            raise
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in config file: {self.config_file}")
            raise
        except Exception as e:
            logging.error(f"Failed to load config: {e}")
            raise
    
    def select_scenario_interactive(self):
        """Interactive scenario selection with enhanced market analysis."""
        print("\n" + "="*70)
        print("SKIZOH GRID TRADING BOT v14 - SCENARIO SELECTION")
        print("="*70 + "\n")
        
        # Display scenarios
        print("Available Trading Scenarios:\n")
        for i, scenario in enumerate(self.scenarios):
            risk_stars = "★" * scenario['risk_level'] + "☆" * (5 - scenario['risk_level'])
            min_profit = self._calculate_min_cycle_profit(scenario)
            
            print(f"[{i}] {scenario['name']}")
            print(f"    {scenario['description']}")
            print(f"    Risk: {risk_stars} ({scenario['risk_level']}/5)")
            print(f"    Grid: {scenario['grid_levels']} levels @ {scenario['grid_spacing_percent']}% spacing")
            print(f"    Est. profit/cycle: ~{min_profit:.2f}% (after fees)")
            print()
        
        # Market analysis
        print("="*70)
        print("MARKET ANALYSIS & RECOMMENDATION")
        print("="*70 + "\n")
        
        try:
            recommendation = self.analyze_and_recommend()
            print(recommendation)
        except Exception as e:
            print(f"⚠️  Could not analyze market: {e}")
            print("Proceeding with manual selection...\n")
        
        # User selection
        while True:
            try:
                selection = input(f"\nSelect scenario [0-{len(self.scenarios)-1}] or 'q' to quit: ")
                
                if selection.lower() == 'q':
                    print("Exiting...")
                    exit(0)
                
                selected_index = int(selection)
                
                if 0 <= selected_index < len(self.scenarios):
                    self.selected_scenario = self.scenarios[selected_index]
                    print(f"\n✓ Selected: {self.selected_scenario['name']}")
                    print(f"  {self.selected_scenario['description']}")
                    return self.selected_scenario
                else:
                    print(f"❌ Enter 0-{len(self.scenarios)-1}")
            except ValueError:
                print("❌ Invalid input")
    
    def _calculate_min_cycle_profit(self, scenario):
        """Calculate minimum profit per cycle after fees."""
        fee_rate = self.config.get('fee_rate', 0.001)
        spacing = scenario['grid_spacing_percent']
        # Profit = spacing - (2 * fee_rate * 100)
        return spacing - (2 * fee_rate * 100)
    
    def analyze_and_recommend(self):
        """Analyze market and recommend scenario with ADX consideration."""
        exchange = ccxt.binanceus({
            'apiKey': self.config['api_key'],
            'secret': self.config['api_secret'],
            'enableRateLimit': True,
        })
        exchange.load_markets()
        
        symbol = self.config['symbol']
        analyzer = MarketAnalyzer(exchange, symbol)
        
        # Fetch market data
        ticker = exchange.fetch_ticker(symbol)
        current_price = ticker['last']
        high_24h = ticker['high']
        low_24h = ticker['low']
        volume_24h = ticker['baseVolume']
        
        volatility_24h = ((high_24h - low_24h) / current_price) * 100
        
        # Get indicators
        rsi = analyzer.calculate_rsi_wilder()
        macd = analyzer.calculate_macd()
        adx = analyzer.calculate_adx()
        trend = analyzer.get_market_trend()
        sr_levels = analyzer.find_support_resistance()
        bb = analyzer.calculate_bollinger_bands()
        
        # Build output
        output = []
        output.append(f"Current {symbol} Price: ${current_price:.2f}")
        output.append(f"24h Range: ${low_24h:.2f} - ${high_24h:.2f} ({volatility_24h:.2f}%)")
        output.append(f"24h Volume: {volume_24h:,.2f} {symbol.split('/')[0]}\n")
        
        # RSI
        if rsi is not None:
            output.append(f"📊 RSI (14, Wilder): {rsi:.2f}")
            if rsi < 30:
                output.append("   → OVERSOLD - Potential buying opportunity")
            elif rsi > 70:
                output.append("   → OVERBOUGHT - Potential selling opportunity")
            elif rsi < 45:
                output.append("   → SLIGHTLY BEARISH")
            elif rsi > 55:
                output.append("   → SLIGHTLY BULLISH")
            else:
                output.append("   → NEUTRAL")
        
        # MACD
        if macd is not None:
            output.append(f"📈 MACD Histogram: {macd['histogram']:.4f}")
            if macd['histogram'] > 0:
                output.append("   → BULLISH momentum")
            else:
                output.append("   → BEARISH momentum")
        
        # ADX - Critical for grid trading
        if adx is not None:
            output.append(f"\n🎯 ADX (Trend Strength): {adx['adx']:.2f}")
            if adx['adx'] < 20:
                output.append("   → WEAK/NO TREND - ✅ Ideal for grid trading!")
            elif adx['adx'] < 25:
                output.append("   → DEVELOPING trend - Grid trading OK")
            elif adx['adx'] < 40:
                output.append("   → STRONG trend - ⚠️ Caution advised")
            else:
                output.append("   → VERY STRONG trend - ❌ Avoid grid trading!")
            output.append(f"   → Direction: {adx['trend_direction']}")
        
        # Bollinger Bands
        if bb is not None:
            output.append(f"\n📏 Bollinger Band Width: {bb['width_percent']:.2f}%")
            output.append(f"   → Price position: {bb['price_position']*100:.0f}% (0=lower, 100=upper)")
        
        # S/R Levels
        if sr_levels and sr_levels['support']:
            output.append(f"\n🛡️  Nearest Support: ${sr_levels['support'][0]:.2f}")
        if sr_levels and sr_levels['resistance']:
            output.append(f"⚡ Nearest Resistance: ${sr_levels['resistance'][0]:.2f}")
        
        # Overall assessment
        output.append("\n" + "="*70)
        
        if trend and not trend.get('grid_suitable', True):
            output.append("⚠️  WARNING: Strong trend detected!")
            output.append("   Grid trading may underperform. Consider waiting.")
            output.append("="*70)
        
        # Recommendation
        recommended_index = self._recommend_scenario(volatility_24h, rsi, adx, bb)
        
        if recommended_index is not None:
            recommended = self.scenarios[recommended_index]
            output.append(f"💡 RECOMMENDED: [{recommended_index}] {recommended['name']}")
            output.append(f"   {recommended['description']}")
        
        return "\n".join(output)
    
    def _recommend_scenario(self, volatility, rsi, adx, bb):
        """Recommend scenario based on ADX and volatility."""
        adx_value = adx['adx'] if adx else 20
        
        # Strong trend - recommend conservative
        if adx_value > 35:
            return 0  # Conservative
        
        # Very low volatility
        if volatility < 1.5:
            return 3  # Low Volatility scenario
        
        # Check RSI extremes
        if rsi:
            if rsi < 25:  # Very oversold
                if adx_value < 25:
                    return 2  # Aggressive (buying opportunity in range)
                return 0  # Conservative (could be falling knife)
            elif rsi > 75:  # Very overbought
                return 0  # Conservative
        
        # Normal volatility, weak trend
        if volatility < 3.0 and adx_value < 25:
            return 1  # Balanced
        
        # Moderate volatility
        if volatility < 5.0:
            if adx_value < 20:
                return 1  # Balanced
            return 4  # High Volatility
        
        # High volatility
        if volatility >= 5.0:
            return 4  # High Volatility
        
        return 1  # Default to balanced
    
    def get_scenario_by_name(self, name):
        """Get scenario by name."""
        for scenario in self.scenarios:
            if scenario['name'].lower() == name.lower():
                return scenario
        return None

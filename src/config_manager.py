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

import json
import logging
import ccxt
import numpy as np
from market_analysis import MarketAnalyzer

class ConfigManager:
    """Manage multi-scenario configurations and interactive selection."""
    
    def __init__(self, config_file='config.json'):
        """Initialize configuration manager.
        
        Args:
            config_file (str): Path to configuration JSON file
        
        Returns:
            None
        """
        self.config_file = config_file
        self.config = None
        self.scenarios = []
        self.selected_scenario = None
        
    def load_config(self):
        """Load configuration from JSON file.
        
        Args:
            None
        
        Returns:
            dict: Full configuration dictionary
        """
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
        """Interactive scenario selection with market analysis.
        
        Args:
            None
        
        Returns:
            dict: Selected scenario configuration
        """
        print("\n" + "="*70)
        print("SCENARIO SELECTION - Choose Your Trading Strategy")
        print("="*70 + "\n")
        
        # Display available scenarios
        print("Available Trading Scenarios:\n")
        for i, scenario in enumerate(self.scenarios):
            risk_stars = "★" * scenario['risk_level'] + "☆" * (5 - scenario['risk_level'])
            print(f"[{i}] {scenario['name']}")
            print(f"    {scenario['description']}")
            print(f"    Risk: {risk_stars} ({scenario['risk_level']}/5)")
            print(f"    Grid: {scenario['grid_levels']} levels @ {scenario['grid_spacing_percent']}% spacing")
            print()
        
        # Get market analysis and recommendation
        print("="*70)
        print("MARKET ANALYSIS & RECOMMENDATION")
        print("="*70 + "\n")
        
        try:
            recommendation = self.analyze_and_recommend()
            print(recommendation)
        except Exception as e:
            print(f"⚠️  Could not analyze market: {e}")
            print("Proceeding with manual selection...\n")
        
        # Get user selection
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
                    print(f"  Description: {self.selected_scenario['description']}")
                    return self.selected_scenario
                else:
                    print(f"❌ Please enter a number between 0 and {len(self.scenarios)-1}")
            except ValueError:
                print("❌ Invalid input. Please enter a number.")
    
    def analyze_and_recommend(self):
        """Analyze current market and recommend best scenario.
        
        Args:
            None
        
        Returns:
            str: Recommendation text with market analysis
        """
        # Initialize exchange for market analysis
        exchange = ccxt.binanceus({
            'apiKey': self.config['api_key'],
            'secret': self.config['api_secret'],
            'enableRateLimit': True,
        })
        exchange.load_markets()
        
        symbol = self.config['symbol']
        analyzer = MarketAnalyzer(exchange, symbol)
        
        # Get current market data
        ticker = exchange.fetch_ticker(symbol)
        current_price = ticker['last']
        high_24h = ticker['high']
        low_24h = ticker['low']
        volume_24h = ticker['baseVolume']
        
        # Calculate 24h volatility
        price_range = high_24h - low_24h
        volatility_24h = (price_range / current_price) * 100
        
        # Get advanced indicators
        rsi = analyzer.calculate_rsi()
        macd = analyzer.calculate_macd()
        trend = analyzer.get_market_trend()
        sr_levels = analyzer.find_support_resistance()
        
        # Build recommendation
        output = []
        output.append(f"Current {symbol} Price: ${current_price:.2f}")
        output.append(f"24h Range: ${low_24h:.2f} - ${high_24h:.2f} ({volatility_24h:.2f}%)")
        output.append(f"24h Volume: {volume_24h:.2f} {symbol.split('/')[0]}\n")
        
        # Technical indicators
        if rsi is not None:
            output.append(f"📊 RSI (14): {rsi:.2f}")
            if rsi < 30:
                output.append("   → OVERSOLD - Good buying opportunity")
            elif rsi > 70:
                output.append("   → OVERBOUGHT - Consider selling")
            else:
                output.append(f"   → NEUTRAL")
        
        if macd is not None:
            output.append(f"📈 MACD Histogram: {macd['histogram']:.4f}")
            if macd['histogram'] > 0:
                output.append("   → BULLISH - Upward momentum")
            else:
                output.append("   → BEARISH - Downward momentum")
        
        if trend is not None:
            output.append(f"\n🎯 Market Trend: {trend['trend']} ({trend['strength']})")
        
        if sr_levels and sr_levels['support']:
            output.append(f"\n🛡️  Nearest Support: ${sr_levels['support'][0]:.2f}")
        if sr_levels and sr_levels['resistance']:
            output.append(f"⚡ Nearest Resistance: ${sr_levels['resistance'][0]:.2f}")
        
        # Recommend scenario based on analysis
        output.append("\n" + "="*70)
        recommended_index = self._recommend_scenario(volatility_24h, rsi, trend)
        
        if recommended_index is not None:
            recommended = self.scenarios[recommended_index]
            output.append(f"💡 RECOMMENDED SCENARIO: [{recommended_index}] {recommended['name']}")
            output.append(f"   {recommended['description']}")
        
        return "\n".join(output)
    
    def _recommend_scenario(self, volatility, rsi, trend):
        """Recommend best scenario based on market conditions.
        
        Args:
            volatility (float): 24h volatility percentage
            rsi (float): Current RSI value
            trend (dict): Trend analysis dictionary
        
        Returns:
            int: Recommended scenario index
        """
        # Very low volatility
        if volatility < 1.5:
            return 3  # Low Volatility
        
        # Low volatility
        elif volatility < 2.5:
            if rsi and rsi < 40:
                return 2  # Aggressive (buy opportunity)
            return 1  # Balanced
        
        # Medium volatility
        elif volatility < 4.0:
            if trend and trend['trend'] in ['BULLISH', 'OVERSOLD']:
                return 2  # Aggressive
            return 1  # Balanced
        
        # High volatility
        elif volatility < 6.0:
            return 4  # High Volatility
        
        # Extreme volatility
        else:
            return 0  # Conservative
    
    def get_scenario_by_name(self, name):
        """Get scenario configuration by name.
        
        Args:
            name (str): Scenario name
        
        Returns:
            dict: Scenario configuration or None if not found
        """
        for scenario in self.scenarios:
            if scenario['name'].lower() == name.lower():
                return scenario
        return None

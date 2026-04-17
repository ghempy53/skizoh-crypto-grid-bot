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
# SKIZOH CRYPTO GRID TRADING BOT - Configuration Manager v3.2
# =============================================================================
# Enhanced with profit-focused scenario recommendations
# =============================================================================

import json
import logging
import ccxt
import numpy as np
from typing import Dict, List, Optional, Any
from market_analysis import MarketAnalyzer

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manage multi-scenario configurations with enhanced market analysis."""
    
    REQUIRED_CONFIG_FIELDS = ['api_key', 'api_secret', 'symbol', 'config_data']
    
    REQUIRED_SCENARIO_FIELDS = [
        'name', 'grid_levels', 'grid_spacing_percent', 'investment_percent',
        'min_order_size_usdt', 'stop_loss_percent', 'atr_period',
        'volatility_threshold', 'check_interval_seconds'
    ]
    
    def __init__(self, config_file: str = 'config.json'):
        self.config_file = config_file
        self.config: Optional[Dict[str, Any]] = None
        self.scenarios: List[Dict[str, Any]] = []
        self.selected_scenario: Optional[Dict[str, Any]] = None
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
            
            self._validate_config()
            self.scenarios = self.config['config_data']
            logger.info(f"Loaded {len(self.scenarios)} trading scenarios")
            
            return self.config
            
        except FileNotFoundError:
            logger.error(f"Config file not found: {self.config_file}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise
    
    def _validate_config(self):
        """Validate configuration structure."""
        if not self.config:
            raise ValueError("Config is empty")
        
        for field in self.REQUIRED_CONFIG_FIELDS:
            if field not in self.config:
                raise ValueError(f"Missing field: {field}")
        
        if 'YOUR_' in self.config['api_key'] or not self.config['api_key']:
            raise ValueError("API key not configured")
        
        if 'YOUR_' in self.config['api_secret'] or not self.config['api_secret']:
            raise ValueError("API secret not configured")
        
        scenarios = self.config['config_data']
        if not scenarios or not isinstance(scenarios, list):
            raise ValueError("config_data must be a non-empty list")
        
        for i, scenario in enumerate(scenarios):
            self._validate_scenario(scenario, i)
    
    def _validate_scenario(self, scenario: Dict[str, Any], index: int):
        """Validate scenario configuration."""
        for field in self.REQUIRED_SCENARIO_FIELDS:
            if field not in scenario:
                raise ValueError(f"Scenario {index} missing: {field}")
        
        if scenario['grid_levels'] < 2:
            raise ValueError(f"Scenario {index}: grid_levels must be >= 2")
        
        if scenario['grid_spacing_percent'] <= 0:
            raise ValueError(f"Scenario {index}: grid_spacing_percent must be > 0")
    
    def select_scenario_interactive(self) -> Dict[str, Any]:
        """Interactive scenario selection."""
        print("\n" + "="*70)
        print("SKIZOH GRID TRADING BOT v3.2 - SCENARIO SELECTION")
        print("="*70 + "\n")
        
        print("Available Scenarios:\n")
        for i, scenario in enumerate(self.scenarios):
            risk_level = scenario.get('risk_level', 3)
            risk_stars = "★" * risk_level + "☆" * (5 - risk_level)
            min_profit = self._calculate_min_profit(scenario)
            
            print(f"[{i}] {scenario['name']}")
            print(f"    {scenario.get('description', '')}")
            print(f"    Risk: {risk_stars} | Profit/cycle: ~{min_profit:.2f}%")
            print()
        
        print("="*70)
        print("MARKET ANALYSIS")
        print("="*70 + "\n")
        
        try:
            recommendation = self.analyze_and_recommend()
            print(recommendation)
        except Exception as e:
            print(f"⚠️ Analysis unavailable: {e}\n")
        
        while True:
            try:
                selection = input(f"\nSelect [0-{len(self.scenarios)-1}] or 'q' to quit: ")
                
                if selection.lower() == 'q':
                    exit(0)
                
                idx = int(selection)
                if 0 <= idx < len(self.scenarios):
                    self.selected_scenario = self.scenarios[idx]
                    print(f"\n✓ Selected: {self.selected_scenario['name']}")
                    return self.selected_scenario
                else:
                    print(f"❌ Enter 0-{len(self.scenarios)-1}")
            except ValueError:
                print("❌ Invalid input")
    
    def _calculate_min_profit(self, scenario: Dict[str, Any]) -> float:
        """Calculate minimum profit per cycle after fees."""
        fee_rate = self.config.get('fee_rate', 0.001) if self.config else 0.001
        if self.config and self.config.get('use_bnb_for_fees', False):
            fee_rate *= 0.75
        spacing = scenario['grid_spacing_percent']
        return spacing - (2 * fee_rate * 100)
    
    def analyze_and_recommend(self) -> str:
        """Analyze market and recommend scenario."""
        if not self.config:
            return "Config not loaded"
        
        exchange = ccxt.binanceus({
            'apiKey': self.config['api_key'],
            'secret': self.config['api_secret'],
            'enableRateLimit': True,
        })
        exchange.load_markets()
        
        symbol = self.config['symbol']
        analyzer = MarketAnalyzer(exchange, symbol)
        
        ticker = exchange.fetch_ticker(symbol)
        current_price = ticker['last']
        high_24h = ticker['high']
        low_24h = ticker['low']
        
        if current_price <= 0:
            return "Could not fetch price"
        
        volatility = ((high_24h - low_24h) / current_price) * 100
        
        rsi = analyzer.calculate_rsi_wilder()
        adx = analyzer.calculate_adx()
        bb = analyzer.calculate_bollinger_bands()
        efficiency = analyzer.calculate_grid_efficiency_score()
        mr = analyzer.calculate_mean_reversion_probability()
        
        output: List[str] = []
        output.append(f"Current {symbol}: ${current_price:.2f}")
        output.append(f"24h Range: ${low_24h:.2f} - ${high_24h:.2f} ({volatility:.2f}%)\n")
        
        if rsi is not None:
            output.append(f"📊 RSI: {rsi:.1f}")
            if rsi < 30:
                output.append("   → OVERSOLD - Accumulation zone")
            elif rsi > 70:
                output.append("   → OVERBOUGHT - Distribution zone")
        
        if adx is not None:
            output.append(f"🎯 ADX: {adx['adx']:.1f} ({adx['trend_direction']})")
            if adx['adx'] < 20:
                output.append("   → NO TREND - ✅ Ideal for grid trading")
            elif adx['adx'] < 25:
                output.append("   → DEVELOPING - Grid trading OK")
            elif adx['adx'] < 40:
                output.append("   → STRONG TREND - ⚠️ Caution")
            else:
                output.append("   → VERY STRONG - ❌ Avoid grid trading")
        
        if bb is not None:
            output.append(f"📏 BB Width: {bb['width_percent']:.2f}%")
        
        if efficiency:
            output.append(f"\n🏆 Grid Efficiency Score: {efficiency['score']}/100")
            output.append(f"   → {efficiency['recommendation']}")
        
        if mr:
            output.append(f"📈 Mean Reversion Prob: {mr['probability']*100:.0f}%")
        
        output.append("\n" + "="*70)
        
        recommended = self._recommend_scenario(volatility, rsi, adx, bb)
        if recommended is not None and 0 <= recommended < len(self.scenarios):
            rec = self.scenarios[recommended]
            output.append(f"💡 RECOMMENDED: [{recommended}] {rec['name']}")
            output.append(f"   {rec.get('description', '')}")
        
        return "\n".join(output)
    
    def _recommend_scenario(self, volatility: float, rsi: Optional[float], 
                           adx: Optional[Dict], bb: Optional[Dict]) -> Optional[int]:
        """Recommend scenario based on conditions."""
        adx_value = adx['adx'] if adx else 20
        
        # Strong trend - conservative
        if adx_value > 35:
            return 0
        
        # Very low volatility
        if volatility < 1.5:
            for i, s in enumerate(self.scenarios):
                if 'low volatility' in s['name'].lower():
                    return i
            return 3 if len(self.scenarios) > 3 else 0
        
        # Mean reversion conditions
        if rsi and (rsi < 35 or rsi > 65) and adx_value < 25:
            for i, s in enumerate(self.scenarios):
                if 'mean reversion' in s['name'].lower():
                    return i
        
        # RSI extremes
        if rsi is not None:
            if rsi < 25 and adx_value < 25:
                return 2 if len(self.scenarios) > 2 else 0
            elif rsi > 75:
                return 0
        
        # Normal volatility, weak trend
        if volatility < 3.0 and adx_value < 25:
            return 1 if len(self.scenarios) > 1 else 0
        
        # High volatility
        if volatility >= 5.0:
            return 4 if len(self.scenarios) > 4 else 0
        
        # Default to balanced
        return 1 if len(self.scenarios) > 1 else 0
    
    def get_scenario_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get scenario by name."""
        for scenario in self.scenarios:
            if scenario['name'].lower() == name.lower():
                return scenario
        return None

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
# SKIZOH CRYPTO GRID TRADING BOT - Docker Entry Point
# =============================================================================
# Modified for Docker deployment with environment variable configuration
# =============================================================================

import logging
import sys
import os
from pathlib import Path

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent

# Add src directory to path
sys.path.insert(0, str(SCRIPT_DIR))

from grid_bot import SmartGridTradingBot
from config_manager import ConfigManager

# Ensure data directory exists using absolute path
DATA_DIR = PROJECT_ROOT / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging with absolute path
LOG_FILE = DATA_DIR / 'grid_bot.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(str(LOG_FILE)),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def print_banner():
    """Display welcome banner."""
    print("\n" + "="*70)
    print("       SKIZOH CRYPTO GRID TRADING BOT v14.1")
    print("       Smart Automated Trading with Advanced Risk Management")
    print("       Docker Container Mode")
    print("="*70)
    print("\n🚀 Features:")
    print("  • Proper cost basis tracking (FIFO) for accurate P&L")
    print("  • Fee-aware minimum grid spacing")
    print("  • ADX trend filter (pause in strong trends)")
    print("  • Position exposure limits")
    print("  • State persistence across restarts")
    print("\n" + "="*70 + "\n")


def get_scenario_from_env(config_manager: ConfigManager) -> dict:
    """Get scenario from environment variable or use default."""
    scenarios = config_manager.scenarios
    
    # Check for SCENARIO environment variable
    scenario_env = os.environ.get('GRIDBOT_SCENARIO', '').strip()
    
    if scenario_env:
        # Try to match by name (case-insensitive)
        for scenario in scenarios:
            if scenario['name'].lower() == scenario_env.lower():
                logger.info(f"Using scenario from environment: {scenario['name']}")
                return scenario
        
        # Try to match by index
        try:
            index = int(scenario_env)
            if 0 <= index < len(scenarios):
                logger.info(f"Using scenario index {index}: {scenarios[index]['name']}")
                return scenarios[index]
        except ValueError:
            pass
        
        logger.warning(f"Scenario '{scenario_env}' not found, using default")
    
    # Check for DEFAULT_SCENARIO in config
    config = config_manager.config
    default_name = config.get('default_scenario', 'Balanced')
    
    for scenario in scenarios:
        if scenario['name'].lower() == default_name.lower():
            logger.info(f"Using default scenario: {scenario['name']}")
            return scenario
    
    # Fallback to first scenario
    logger.info(f"Using first available scenario: {scenarios[0]['name']}")
    return scenarios[0]


def is_interactive():
    """Check if running in interactive mode."""
    # Check if stdin is a TTY
    if not sys.stdin.isatty():
        return False
    
    # Check for explicit non-interactive flag
    if os.environ.get('GRIDBOT_NONINTERACTIVE', '').lower() in ('1', 'true', 'yes'):
        return False
    
    return True


class DockerGridBot(SmartGridTradingBot):
    """Extended bot class for Docker deployment."""
    
    def __init__(self, config_file: str = 'config.json'):
        """Initialize with Docker-specific handling."""
        # Resolve config file path
        self.config_file_path = Path(config_file).resolve()
        self.project_root = self.config_file_path.parent.parent
        self.data_dir = self.project_root / 'data'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_manager = ConfigManager(str(self.config_file_path))
        config = self.config_manager.load_config()
        
        # Validate required config fields
        self._validate_config(config)
        
        # API credentials
        self.api_key = config['api_key']
        self.api_secret = config['api_secret']
        self.symbol = config['symbol']
        
        # Fee configuration
        self.fee_rate = config.get('fee_rate', self.DEFAULT_FEE_RATE)
        
        # Select scenario based on mode
        if is_interactive():
            scenario = self.config_manager.select_scenario_interactive()
        else:
            scenario = get_scenario_from_env(self.config_manager)
            self._print_scenario_info(scenario)
        
        self.load_scenario(scenario)
        
        # Continue with normal initialization
        self._complete_init(config)
    
    def _print_scenario_info(self, scenario: dict):
        """Print selected scenario information."""
        print("\n" + "="*50)
        print(f"📊 Selected Scenario: {scenario['name']}")
        print("="*50)
        print(f"   {scenario.get('description', 'No description')}")
        print(f"   Grid Levels: {scenario['grid_levels']}")
        print(f"   Grid Spacing: {scenario['grid_spacing_percent']}%")
        print(f"   Investment: {scenario['investment_percent']}%")
        print(f"   Stop Loss: {scenario['stop_loss_percent']}%")
        print("="*50 + "\n")
    
    def _complete_init(self, config: dict):
        """Complete initialization after scenario selection."""
        from market_analysis import MarketAnalyzer
        from grid_bot import PositionTracker
        
        # Initialize exchange and analyzers
        self.exchange = self.initialize_exchange()
        self.market_analyzer = MarketAnalyzer(self.exchange, self.symbol)
        
        # Position tracking with state persistence
        position_state_file = str(self.data_dir / 'position_state.json')
        self.position_tracker = PositionTracker(state_file=position_state_file)
        
        # Trading state
        self.grid_levels = []
        self.active_orders = {}
        self.initial_investment = 0.0
        self.cycles_completed = 0
        
        # Exposure limits
        self.max_position_percent = config.get('max_position_percent', 80)
        self.max_single_order_percent = config.get('max_single_order_percent', 10)
        
        # Tax logging with absolute path
        self.tax_log_file = str(self.data_dir / 'tax_transactions.csv')
        self.initialize_tax_log()
        
        # Grid repositioning
        self.grid_center_price = None
        self.last_grid_update = 0
        
        # Performance tracking
        self.start_time = None
        self.peak_value = 0.0
        self.max_drawdown = 0.0
        
        # Trend pause state
        self.trend_pause_until = 0.0


def main():
    """Main entry point."""
    try:
        print_banner()
        
        # Check for config using path relative to script location
        config_path = SCRIPT_DIR / 'priv' / 'config.json'
        if not config_path.exists():
            print(f"❌ Config file not found: {config_path}")
            print("   Mount your config.json to: /app/src/priv/config.json")
            sys.exit(1)
        
        # Show mode
        if is_interactive():
            print("🖥️  Running in INTERACTIVE mode")
            print("   You will be prompted to select a scenario.\n")
        else:
            scenario_env = os.environ.get('GRIDBOT_SCENARIO', '')
            print("🐳 Running in DOCKER (non-interactive) mode")
            if scenario_env:
                print(f"   Scenario from environment: {scenario_env}")
            else:
                print("   Using default scenario (set GRIDBOT_SCENARIO to change)\n")
        
        # Initialize and run bot
        bot = DockerGridBot(str(config_path))
        bot.run()
        
    except KeyboardInterrupt:
        logging.info("Bot stopped by user (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

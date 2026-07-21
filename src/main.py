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
# SKIZOH CRYPTO GRID TRADING BOT v4.1 - Entry Point
# =============================================================================

import logging
import sys
import os
import time
from pathlib import Path

import ccxt

# Setup paths
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(SCRIPT_DIR))

from grid_bot import SmartGridTradingBot
from config_manager import ConfigManager
import notifier

# Configure logging (v4.1: size-capped rotation)
# The unbounded FileHandler grew for weeks on the Pi's SD card until greps
# hung and an ungraceful write left null bytes mid-file. 10MB x 3 backups
# keeps ~1 month of history, bounds SD wear, and retires corruption with
# old segments instead of accumulating it forever.
from logging.handlers import RotatingFileHandler

LOG_FILE = DATA_DIR / 'grid_bot.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(str(LOG_FILE), maxBytes=10 * 1024 * 1024,
                            backupCount=3),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def print_banner():
    """Display welcome banner."""
    print("\n" + "="*70)
    print("       SKIZOH CRYPTO GRID TRADING BOT v4.1")
    print("       Profit-Optimized Smart Adaptive Trading")
    print("="*70)
    print("\nv4.1 Smart Features:")
    print("  [Adaptive]   Continuous parameter blending across scenarios")
    print("  [Regime]     Multi-timeframe market regime detection")
    print("  [Resilience] Circuit breakers + auto-reconnect")
    print("  [Volume]     VWAP + volume profile grid placement")
    print("  [Safety]     Flash crash detection + portfolio heat")
    print("  [Monitor]    Heartbeat system for external monitoring")
    print("  [24/7]       Graceful degradation + auto-recovery")
    print("\nCore Features:")
    print("  [Grid]       Asymmetric grid placement with market bias")
    print("  [Spacing]    Dynamic spacing adapted to volatility")
    print("  [ETH]        ETH accumulation with profit reinvestment")
    print("  [Pi]         Memory-optimized for Raspberry Pi")
    print("\n" + "="*70 + "\n")


def is_interactive():
    """Check if running interactively."""
    if not sys.stdin.isatty():
        return False
    if os.environ.get('GRIDBOT_NONINTERACTIVE', '').lower() in ('1', 'true', 'yes'):
        return False
    return True


def get_scenario_from_env(config_manager):
    """Get scenario from environment or config default."""
    scenarios = config_manager.scenarios
    scenario_env = os.environ.get('GRIDBOT_SCENARIO', '').strip()
    
    if scenario_env:
        # Try name match
        for scenario in scenarios:
            if scenario['name'].lower() == scenario_env.lower():
                return scenario
        # Try index
        try:
            idx = int(scenario_env)
            if 0 <= idx < len(scenarios):
                return scenarios[idx]
        except ValueError:
            pass
    
    # Use default from config
    default = config_manager.config.get('default_scenario', 'Balanced')
    for scenario in scenarios:
        if scenario['name'].lower() == default.lower():
            return scenario
    
    return scenarios[0]


# Startup retry policy (v4.1).
#
# The legacy (v3.x) behavior — exit on any fatal error and let Docker's
# `restart: unless-stopped` relaunch instantly — caused a 2-month
# undetected crash loop on an invalid API key (restart every ~23s,
# hammering the Binance.US API, healthcheck green the whole time).
#
# Auth errors are NOT retryable on a short fuse: no amount of retrying
# fixes a bad key. But they ARE fixable externally (user rotates the key),
# so instead of exiting we alert once and re-check on a long interval —
# the bot then recovers automatically when the key is fixed.
AUTH_RETRY_SECONDS = 15 * 60      # re-check credentials every 15 min
TRANSIENT_RETRY_BASE = 60         # first retry after 1 min
TRANSIENT_RETRY_MAX = 30 * 60     # cap backoff at 30 min


def main():
    """Main entry point with fault-classified retry."""
    print_banner()

    config_path = SCRIPT_DIR / 'priv' / 'config.json'
    if not config_path.exists():
        print(f"❌ Config not found: {config_path}")
        sys.exit(1)

    config_manager = ConfigManager(str(config_path))
    config = config_manager.load_config()

    # Configure alerts as early as possible so startup failures are reported
    notifier.configure(config.get('alerts'))

    if is_interactive():
        print("🖥️  Interactive mode\n")
        scenario = config_manager.select_scenario_interactive()
    else:
        scenario = get_scenario_from_env(config_manager)
        print(f"🐳 Non-interactive mode")
        print(f"   Scenario: {scenario['name']}\n")

    transient_delay = TRANSIENT_RETRY_BASE

    while True:
        try:
            bot = SmartGridTradingBot(str(config_path), scenario=scenario)
            transient_delay = TRANSIENT_RETRY_BASE  # startup succeeded; reset
            bot.run()
            # run() returned: intentional halt (stop loss / emergency stop).
            # Do NOT restart trading automatically after an intentional halt.
            logger.critical("Bot halted intentionally — exiting. "
                            "Restart manually after reviewing.")
            sys.exit(0)

        except KeyboardInterrupt:
            logging.info("Stopped by user")
            sys.exit(0)

        except (ccxt.AuthenticationError, ccxt.PermissionDenied) as e:
            logger.critical(
                f"AUTH ERROR (not retryable by waiting): {e}\n"
                f"Fix the API key in src/priv/config.json "
                f"(Binance.US → API Management), or check its IP whitelist. "
                f"Re-checking in {AUTH_RETRY_SECONDS // 60} min."
            )
            notifier.notify(
                "Grid Bot: API key rejected",
                f"Binance.US rejected the API key ({e}). Trading is DOWN. "
                f"Fix the key or its IP whitelist; the bot re-checks every "
                f"{AUTH_RETRY_SECONDS // 60} minutes and will resume "
                f"automatically.",
                key='auth', priority='urgent',
            )
            time.sleep(AUTH_RETRY_SECONDS)

        except Exception as e:
            logger.exception(f"Fatal error: {e}")
            notifier.notify("Grid Bot: crashed",
                            f"Fatal error: {e}. Retrying in "
                            f"{transient_delay // 60 or 1} min.",
                            key='fatal', priority='high')
            time.sleep(transient_delay)
            transient_delay = min(transient_delay * 2, TRANSIENT_RETRY_MAX)


if __name__ == "__main__":
    main()

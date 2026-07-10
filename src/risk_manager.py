# =============================================================================
# Risk Manager (v3.3) - regime-aware exposure control
#
# Unifies three down-market defenses into a single "target ETH exposure":
#
#   1. Regime exposure targets - bear regime => staged exit down to a
#      configurable ETH floor (never fully out, so V-bottoms aren't missed).
#      Hysteresis + minimum hold times limit whipsaw.
#   2. Trailing equity stop - drawdown from the persisted peak portfolio
#      value caps exposure in stages instead of an all-or-nothing dump.
#   3. Constant-mix rebalancing - when actual exposure drifts outside a
#      band around the target, emit a rebalance trade. This harvests
#      volatility in both directions and guarantees a USDT reserve.
#
# The controller is pure logic (no exchange calls) so it is unit-testable;
# the bot executes the trades it recommends.
# =============================================================================

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

BULLISH_REGIMES = ('TRENDING_UP', 'BREAKOUT')
BEARISH_REGIMES = ('TRENDING_DOWN', 'CRASH')


class ExposureController:
    """Computes the target percentage of the portfolio held in the base
    asset (ETH) and recommends rebalance trades toward it.

    All percentages are 0-100.
    """

    DEFAULTS = {
        # Regime targets: % of portfolio to hold as ETH per regime
        'regime_targets': {
            'TRENDING_UP': 65,
            'BREAKOUT': 65,
            'RANGING': 45,
            'MEAN_REVERTING': 45,
            'LOW_VOLATILITY': 45,
            'HIGH_VOLATILITY': 30,
            'TRENDING_DOWN': 15,
            'CRASH': 15,
        },
        'bear_exposure_floor_percent': 15,   # never sell below this in bear regime
        'bear_confirm_checks': 3,            # consecutive bearish detections to confirm
        'bull_reentry_confirm_checks': 4,    # consecutive non-bearish detections to re-enter
        'min_regime_hold_minutes': 60,       # min time between regime-driven target changes
        'regime_confidence_threshold': 0.55, # ignore low-confidence regime flips
        'stage_step_percent': 15,            # max exposure change per stage (percentage points)
        'stage_interval_minutes': 20,        # min time between stages
        # Trailing stop: drawdown-from-peak => exposure cap (% points)
        'trailing_stop_percent': 10,         # at this drawdown, cap at floor
        'derisk_stages': [[5, 50], [8, 25]], # [drawdown %, exposure cap %]
        'catastrophic_stop_percent': 20,     # emergency: halt + full exit
        'peak_reset_profit_percent': 3,      # new peak > old*(1+x%) resets stages
        # Rebalancing
        'rebalance_band_percent': 7,         # act only when drift exceeds this
        'min_rebalance_notional_usdt': 10,
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None,
                 state_file: Optional[str] = None):
        cfg = dict(self.DEFAULTS)
        merged_targets = dict(self.DEFAULTS['regime_targets'])
        if config:
            user_targets = config.get('regime_targets') or {}
            merged_targets.update(user_targets)
            cfg.update({k: v for k, v in config.items() if k != 'regime_targets'})
        cfg['regime_targets'] = merged_targets
        self.cfg = cfg

        self.state_file = Path(state_file) if state_file else None

        # Regime state
        self._bear_streak = 0
        self._recovery_streak = 0
        self._in_bear_mode = False
        self._last_target_change = 0.0
        self._last_stage_time = 0.0

        # Exposure target starts neutral; refined on first update
        self.target_exposure: float = cfg['regime_targets'].get('RANGING', 45)

        # Trailing stop state (persisted)
        self.peak_value: float = 0.0
        self._derisk_cap: float = 100.0
        self.halt_requested: bool = False

        self._load_state()

    # ------------------------------------------------------------------
    # Persistence (peak value must survive restarts, or every restart
    # silently resets the trailing stop - the v3.2 bug)
    # ------------------------------------------------------------------

    def _load_state(self):
        if not self.state_file or not self.state_file.exists():
            return
        try:
            with open(self.state_file) as f:
                s = json.load(f)
            self.peak_value = float(s.get('peak_value', 0.0))
            self._in_bear_mode = bool(s.get('in_bear_mode', False))
            self.target_exposure = float(s.get('target_exposure', self.target_exposure))
            self._derisk_cap = float(s.get('derisk_cap', 100.0))
            logger.info(
                f"[Risk] Restored state: peak=${self.peak_value:.2f}, "
                f"bear_mode={self._in_bear_mode}, target={self.target_exposure:.0f}%"
            )
        except Exception as e:
            logger.warning(f"[Risk] Could not load risk state: {e}")

    def _save_state(self):
        if not self.state_file:
            return
        try:
            tmp = self.state_file.with_suffix('.tmp')
            with open(tmp, 'w') as f:
                json.dump({
                    'peak_value': round(self.peak_value, 2),
                    'in_bear_mode': self._in_bear_mode,
                    'target_exposure': round(self.target_exposure, 1),
                    'derisk_cap': round(self._derisk_cap, 1),
                    'updated': time.time(),
                }, f)
            tmp.replace(self.state_file)
        except Exception as e:
            logger.debug(f"[Risk] Could not save risk state: {e}")

    # ------------------------------------------------------------------
    # Regime tracking
    # ------------------------------------------------------------------

    def update_regime(self, regime_name: Optional[str],
                      confidence: float = 1.0) -> Dict[str, Any]:
        """Feed one regime observation. Returns a dict describing any
        target change (empty 'events' when nothing changed).
        """
        events: List[str] = []
        if not regime_name:
            return {'events': events, 'target': self.target_exposure}

        if confidence < self.cfg['regime_confidence_threshold']:
            return {'events': events, 'target': self.target_exposure}

        bearish = regime_name in BEARISH_REGIMES
        if bearish:
            self._bear_streak += 1
            self._recovery_streak = 0
        else:
            self._recovery_streak += 1
            self._bear_streak = 0

        now = time.time()
        min_hold = self.cfg['min_regime_hold_minutes'] * 60

        # Enter bear mode: confirmed consecutive bearish readings
        if (not self._in_bear_mode
                and self._bear_streak >= self.cfg['bear_confirm_checks']):
            self._in_bear_mode = True
            self._last_target_change = now
            events.append('BEAR_CONFIRMED')
            logger.warning(f"[Risk] Bear regime confirmed ({regime_name}) — "
                           f"staging exposure down to "
                           f"{self.cfg['bear_exposure_floor_percent']}% floor")

        # Exit bear mode: hysteresis (more confirmations + min hold)
        elif (self._in_bear_mode
              and self._recovery_streak >= self.cfg['bull_reentry_confirm_checks']
              and now - self._last_target_change >= min_hold):
            self._in_bear_mode = False
            self._last_target_change = now
            events.append('BEAR_EXITED')
            logger.info(f"[Risk] Bear regime cleared ({regime_name}) — "
                        f"re-entry enabled")

        # Compute regime target
        targets = self.cfg['regime_targets']
        if self._in_bear_mode:
            regime_target = float(self.cfg['bear_exposure_floor_percent'])
        else:
            regime_target = float(targets.get(regime_name,
                                              targets.get('RANGING', 45)))

        # Stage toward the regime target rather than jumping, one step per
        # stage interval. This is the "staged exit" (and staged re-entry).
        step = self.cfg['stage_step_percent']
        stage_gap = now - self._last_stage_time
        if abs(regime_target - self.target_exposure) > 0.5:
            if stage_gap >= self.cfg['stage_interval_minutes'] * 60:
                if regime_target < self.target_exposure:
                    self.target_exposure = max(regime_target,
                                               self.target_exposure - step)
                else:
                    self.target_exposure = min(regime_target,
                                               self.target_exposure + step)
                self._last_stage_time = now
                events.append('TARGET_STAGED')
                logger.info(f"[Risk] Exposure target staged to "
                            f"{self.target_exposure:.0f}% "
                            f"(regime {regime_name} → {regime_target:.0f}%)")

        self._save_state()
        return {'events': events, 'target': self.target_exposure}

    # ------------------------------------------------------------------
    # Trailing stop
    # ------------------------------------------------------------------

    def update_portfolio_value(self, total_value: float) -> Dict[str, Any]:
        """Feed the current total portfolio value (USDT terms). Updates the
        persisted peak and the drawdown-based exposure cap.
        """
        events: List[str] = []
        if total_value <= 0:
            return {'events': events, 'cap': self._derisk_cap,
                    'drawdown': 0.0, 'halt': self.halt_requested}

        if total_value > self.peak_value:
            reset_mult = 1 + self.cfg['peak_reset_profit_percent'] / 100
            if self._derisk_cap < 100.0 and total_value >= self.peak_value * reset_mult:
                # Recovered meaningfully above old peak: relax de-risk cap
                self._derisk_cap = 100.0
                events.append('DERISK_RESET')
                logger.info("[Risk] New equity high — de-risk stages reset")
            self.peak_value = total_value

        drawdown = 0.0
        if self.peak_value > 0:
            drawdown = (self.peak_value - total_value) / self.peak_value * 100

        # Catastrophic stop
        if drawdown >= self.cfg['catastrophic_stop_percent']:
            if not self.halt_requested:
                events.append('CATASTROPHIC_STOP')
                logger.critical(f"[Risk] Catastrophic drawdown "
                                f"{drawdown:.1f}% — full exit requested")
            self.halt_requested = True
            self._derisk_cap = 0.0
            self._save_state()
            return {'events': events, 'cap': 0.0,
                    'drawdown': drawdown, 'halt': True}

        # Staged de-risk caps (config: [[drawdown %, cap %], ...])
        floor = float(self.cfg['bear_exposure_floor_percent'])
        new_cap = 100.0
        for dd_threshold, cap in sorted(self.cfg['derisk_stages']):
            if drawdown >= dd_threshold:
                new_cap = float(cap)
        if drawdown >= self.cfg['trailing_stop_percent']:
            new_cap = min(new_cap, floor)

        # Caps only tighten; they relax via DERISK_RESET on new highs
        if new_cap < self._derisk_cap:
            self._derisk_cap = new_cap
            events.append('DERISK_STAGE')
            logger.warning(f"[Risk] Drawdown {drawdown:.1f}% — "
                           f"exposure capped at {new_cap:.0f}%")
            self._save_state()

        return {'events': events, 'cap': self._derisk_cap,
                'drawdown': drawdown, 'halt': self.halt_requested}

    # ------------------------------------------------------------------
    # Effective target and rebalancing
    # ------------------------------------------------------------------

    def get_effective_target(self) -> float:
        """Regime target constrained by the drawdown cap."""
        return max(0.0, min(self.target_exposure, self._derisk_cap))

    def recommend_rebalance(self, crypto_value: float, quote_value: float,
                            current_price: float) -> Optional[Dict[str, Any]]:
        """If actual exposure drifted outside the band around the effective
        target, return {'side', 'quantity', 'notional', ...}; else None.
        """
        total = crypto_value + quote_value
        if total <= 0 or current_price <= 0:
            return None

        target = self.get_effective_target()
        actual = crypto_value / total * 100
        drift = actual - target

        if abs(drift) < self.cfg['rebalance_band_percent']:
            return None

        notional = abs(drift) / 100 * total
        if notional < self.cfg['min_rebalance_notional_usdt']:
            return None

        side = 'sell' if drift > 0 else 'buy'
        quantity = notional / current_price
        return {
            'side': side,
            'quantity': quantity,
            'notional': notional,
            'actual_exposure': actual,
            'target_exposure': target,
        }

    def get_status(self) -> Dict[str, Any]:
        return {
            'target_exposure': self.target_exposure,
            'effective_target': self.get_effective_target(),
            'derisk_cap': self._derisk_cap,
            'in_bear_mode': self._in_bear_mode,
            'peak_value': self.peak_value,
            'halt_requested': self.halt_requested,
        }

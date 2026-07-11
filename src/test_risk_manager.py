# =============================================================================
# Unit tests for risk_manager.ExposureController (v4.0)
# Run: python3 -m unittest src.test_risk_manager  (or pytest)
# =============================================================================

import json
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))

from risk_manager import ExposureController


def fast_config(**overrides):
    """Config with timing gates disabled so tests run instantly."""
    cfg = {
        'stage_interval_minutes': 0,
        'min_regime_hold_minutes': 0,
        'bear_confirm_checks': 3,
        'bull_reentry_confirm_checks': 4,
    }
    cfg.update(overrides)
    return cfg


class TestBearStagedExit(unittest.TestCase):
    def test_bear_requires_consecutive_confirmations(self):
        c = ExposureController(fast_config())
        c.update_regime('TRENDING_DOWN')
        c.update_regime('TRENDING_DOWN')
        self.assertFalse(c.get_status()['in_bear_mode'])
        r = c.update_regime('TRENDING_DOWN')
        self.assertTrue(c.get_status()['in_bear_mode'])
        self.assertIn('BEAR_CONFIRMED', r['events'])

    def test_single_bullish_reading_resets_streak(self):
        c = ExposureController(fast_config())
        c.update_regime('TRENDING_DOWN')
        c.update_regime('TRENDING_DOWN')
        c.update_regime('RANGING')  # resets streak
        c.update_regime('TRENDING_DOWN')
        c.update_regime('TRENDING_DOWN')
        self.assertFalse(c.get_status()['in_bear_mode'])

    def test_staged_descent_to_floor(self):
        c = ExposureController(fast_config(
            bear_exposure_floor_percent=15, stage_step_percent=15))
        c.target_exposure = 45.0
        for _ in range(6):
            c.update_regime('TRENDING_DOWN')
        # 45 -> 30 -> 15, one step per (zero-length) interval
        self.assertEqual(c.target_exposure, 15.0)
        # Never below floor
        c.update_regime('TRENDING_DOWN')
        self.assertEqual(c.target_exposure, 15.0)

    def test_low_confidence_ignored(self):
        c = ExposureController(fast_config(regime_confidence_threshold=0.55))
        for _ in range(10):
            c.update_regime('TRENDING_DOWN', confidence=0.3)
        self.assertFalse(c.get_status()['in_bear_mode'])

    def test_reentry_hysteresis(self):
        c = ExposureController(fast_config())
        for _ in range(3):
            c.update_regime('TRENDING_DOWN')
        self.assertTrue(c.get_status()['in_bear_mode'])
        # Needs 4 consecutive non-bearish readings (vs 3 to enter)
        for _ in range(3):
            c.update_regime('TRENDING_UP')
        self.assertTrue(c.get_status()['in_bear_mode'])
        r = c.update_regime('TRENDING_UP')
        self.assertFalse(c.get_status()['in_bear_mode'])
        self.assertIn('BEAR_EXITED', r['events'])


class TestTrailingStop(unittest.TestCase):
    def test_caps_tighten_with_drawdown(self):
        c = ExposureController(fast_config(
            derisk_stages=[[5, 50], [8, 25]], trailing_stop_percent=10,
            bear_exposure_floor_percent=15, catastrophic_stop_percent=20))
        c.update_portfolio_value(260.0)   # set peak
        r = c.update_portfolio_value(250.0)  # -3.8%: no cap
        self.assertEqual(r['cap'], 100.0)
        r = c.update_portfolio_value(245.0)  # -5.8%: cap 50
        self.assertEqual(r['cap'], 50.0)
        r = c.update_portfolio_value(238.0)  # -8.5%: cap 25
        self.assertEqual(r['cap'], 25.0)
        r = c.update_portfolio_value(233.0)  # -10.4%: floor
        self.assertEqual(r['cap'], 15.0)
        self.assertFalse(r['halt'])

    def test_users_actual_loss_would_have_been_caught(self):
        """$260 peak -> $220 (-15.4%) should trigger heavy de-risking,
        unlike the legacy (pre-v4.0) logic which required -22.5%."""
        c = ExposureController(fast_config())
        c.update_portfolio_value(260.0)
        r = c.update_portfolio_value(220.0)
        self.assertLessEqual(r['cap'], 15.0)

    def test_catastrophic_halt(self):
        c = ExposureController(fast_config(catastrophic_stop_percent=20))
        c.update_portfolio_value(260.0)
        r = c.update_portfolio_value(205.0)  # -21%
        self.assertTrue(r['halt'])
        self.assertEqual(r['cap'], 0.0)

    def test_caps_do_not_relax_on_partial_recovery(self):
        c = ExposureController(fast_config())
        c.update_portfolio_value(260.0)
        c.update_portfolio_value(240.0)  # -7.7%: cap 50
        r = c.update_portfolio_value(255.0)  # partial recovery
        self.assertEqual(r['cap'], 50.0)

    def test_cap_resets_on_meaningful_new_high(self):
        c = ExposureController(fast_config(peak_reset_profit_percent=3))
        c.update_portfolio_value(260.0)
        c.update_portfolio_value(240.0)  # cap 50
        r = c.update_portfolio_value(268.0)  # > 260 * 1.03
        self.assertIn('DERISK_RESET', r['events'])
        self.assertEqual(r['cap'], 100.0)


class TestRebalancing(unittest.TestCase):
    def _controller(self, target=45.0):
        c = ExposureController(fast_config(
            rebalance_band_percent=7, min_rebalance_notional_usdt=10))
        c.target_exposure = target
        return c

    def test_no_action_within_band(self):
        c = self._controller(45.0)
        # 50% actual vs 45% target: within 7-point band
        self.assertIsNone(c.recommend_rebalance(125.0, 125.0, 2500.0))

    def test_sell_when_overexposed(self):
        c = self._controller(45.0)
        # 70% actual vs 45% target
        rec = c.recommend_rebalance(175.0, 75.0, 2500.0)
        self.assertEqual(rec['side'], 'sell')
        self.assertAlmostEqual(rec['notional'], 62.5, places=1)

    def test_buy_when_underexposed(self):
        c = self._controller(45.0)
        rec = c.recommend_rebalance(25.0, 225.0, 2500.0)  # 10% actual
        self.assertEqual(rec['side'], 'buy')

    def test_dust_trades_skipped(self):
        c = self._controller(45.0)
        # 8-point drift on a $100 portfolio = $8 notional < $10 min
        self.assertIsNone(c.recommend_rebalance(53.0, 47.0, 2500.0))

    def test_derisk_cap_constrains_target(self):
        c = self._controller(65.0)
        c.update_portfolio_value(260.0)
        c.update_portfolio_value(238.0)  # -8.5%: cap 25
        self.assertEqual(c.get_effective_target(), 25.0)
        rec = c.recommend_rebalance(169.0, 91.0, 2500.0)  # 65% actual
        self.assertEqual(rec['side'], 'sell')


class TestPersistence(unittest.TestCase):
    def test_peak_survives_restart(self):
        with tempfile.TemporaryDirectory() as d:
            state = str(Path(d) / 'risk_state.json')
            c1 = ExposureController(fast_config(), state_file=state)
            c1.update_portfolio_value(260.0)
            c1.update_portfolio_value(240.0)  # persists via cap change

            c2 = ExposureController(fast_config(), state_file=state)
            self.assertEqual(c2.peak_value, 260.0)
            # Drawdown continuity: new instance still knows the cap
            r = c2.update_portfolio_value(238.0)
            self.assertLessEqual(r['cap'], 50.0)

    def test_quiet_climb_persists_peak(self):
        """Peaks reached without any de-risk/regime events must still be
        persisted (throttled to 0.5% growth), or a crash during a calm
        climb restarts the trailing stop from a lower anchor."""
        with tempfile.TemporaryDirectory() as d:
            state = str(Path(d) / 'risk_state.json')
            c1 = ExposureController(fast_config(), state_file=state)
            c1.update_portfolio_value(229.79)  # no events fire here
            c1.update_portfolio_value(235.00)  # +2.3%, still no events
            self.assertTrue(Path(state).exists())
            c2 = ExposureController(fast_config(), state_file=state)
            self.assertGreaterEqual(c2.peak_value, 235.00 * 0.995)

    def test_corrupt_state_is_tolerated(self):
        with tempfile.TemporaryDirectory() as d:
            state = Path(d) / 'risk_state.json'
            state.write_text('{not json')
            c = ExposureController(fast_config(), state_file=str(state))
            self.assertEqual(c.peak_value, 0.0)  # falls back cleanly


if __name__ == '__main__':
    unittest.main(verbosity=2)

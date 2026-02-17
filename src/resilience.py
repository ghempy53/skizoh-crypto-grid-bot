# =============================================================================
# SKIZOH CRYPTO GRID TRADING BOT - Resilience Module v3.0
# =============================================================================
# 24/7 UPTIME FEATURES:
# - Circuit breaker pattern for API calls (prevents cascading failures)
# - Exponential backoff with jitter for retries
# - Connection health monitoring with auto-reconnect
# - Graceful degradation when exchange is unreachable
# - Flash crash detection and emergency response
# - Heartbeat system for external monitoring
# - Portfolio heat tracking for risk management
# - Session health scoring
# =============================================================================

import logging
import time
import random
import json
import os
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Optional, Any, Callable
from pathlib import Path

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    CLOSED = 'CLOSED'       # Normal operation
    OPEN = 'OPEN'           # Failure detected, blocking calls
    HALF_OPEN = 'HALF_OPEN'  # Testing if service recovered


class CircuitBreaker:
    """
    Circuit breaker pattern for API calls.

    Prevents cascading failures by temporarily blocking calls to a failing
    service. After a cooldown, allows a single test call through.

    States:
    - CLOSED: Normal operation, calls pass through
    - OPEN: Too many failures, calls are blocked (returns None/raises)
    - HALF_OPEN: After cooldown, one test call is allowed through
    """

    def __init__(self, name: str, failure_threshold: int = 5,
                 recovery_timeout: float = 60, half_open_max: int = 1):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max = half_open_max

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = 0.0
        self.last_state_change = time.time()
        self.half_open_calls = 0
        self._total_failures = 0
        self._total_successes = 0
        self._total_blocked = 0

    def can_execute(self) -> bool:
        """Check if a call is allowed through the circuit breaker."""
        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self._transition(CircuitState.HALF_OPEN)
                return True
            self._total_blocked += 1
            return False

        if self.state == CircuitState.HALF_OPEN:
            if self.half_open_calls < self.half_open_max:
                self.half_open_calls += 1
                return True
            return False

        return False

    def record_success(self):
        """Record a successful call."""
        self._total_successes += 1
        self.success_count += 1

        if self.state == CircuitState.HALF_OPEN:
            self._transition(CircuitState.CLOSED)
            self.failure_count = 0
            self.half_open_calls = 0
            logger.info(f"[CB:{self.name}] Circuit CLOSED - service recovered")

    def record_failure(self):
        """Record a failed call."""
        self._total_failures += 1
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == CircuitState.HALF_OPEN:
            self._transition(CircuitState.OPEN)
            logger.warning(f"[CB:{self.name}] Circuit OPEN - recovery failed")

        elif self.state == CircuitState.CLOSED:
            if self.failure_count >= self.failure_threshold:
                self._transition(CircuitState.OPEN)
                logger.warning(
                    f"[CB:{self.name}] Circuit OPEN after {self.failure_count} failures "
                    f"(cooldown: {self.recovery_timeout}s)"
                )

    def _transition(self, new_state: CircuitState):
        """Transition to a new state."""
        old_state = self.state
        self.state = new_state
        self.last_state_change = time.time()
        if new_state == CircuitState.HALF_OPEN:
            self.half_open_calls = 0

    def get_stats(self) -> Dict[str, Any]:
        """Get circuit breaker statistics."""
        return {
            'name': self.name,
            'state': self.state.value,
            'failures': self.failure_count,
            'total_failures': self._total_failures,
            'total_successes': self._total_successes,
            'total_blocked': self._total_blocked,
            'time_in_state': time.time() - self.last_state_change,
        }


def retry_with_backoff(func: Callable, max_retries: int = 4,
                       base_delay: float = 2.0, max_delay: float = 30.0,
                       circuit_breaker: Optional[CircuitBreaker] = None,
                       fallback: Any = None) -> Any:
    """
    Execute a function with exponential backoff and optional circuit breaker.

    Args:
        func: The function to execute
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay between retries
        circuit_breaker: Optional circuit breaker to check
        fallback: Value to return if all retries fail

    Returns:
        Function result or fallback value
    """
    if circuit_breaker and not circuit_breaker.can_execute():
        logger.debug(f"[CB:{circuit_breaker.name}] Call blocked by circuit breaker")
        return fallback

    last_exception = None
    for attempt in range(max_retries + 1):
        try:
            result = func()
            if circuit_breaker:
                circuit_breaker.record_success()
            return result
        except Exception as e:
            last_exception = e
            if circuit_breaker:
                circuit_breaker.record_failure()

            if attempt < max_retries:
                # Exponential backoff with jitter
                delay = min(max_delay, base_delay * (2 ** attempt))
                jitter = delay * 0.2 * random.random()
                sleep_time = delay + jitter

                logger.warning(
                    f"Attempt {attempt + 1}/{max_retries + 1} failed: {e}. "
                    f"Retrying in {sleep_time:.1f}s..."
                )
                time.sleep(sleep_time)
            else:
                logger.error(f"All {max_retries + 1} attempts failed: {e}")

    return fallback


class ConnectionMonitor:
    """
    Monitor exchange connection health and trigger reconnection.

    Tracks API response times, error rates, and connectivity status.
    Provides health scoring for the overall connection.
    """

    def __init__(self):
        self._response_times: list = []
        self._max_samples = 50
        self._error_count = 0
        self._success_count = 0
        self._last_successful_call = time.time()
        self._connection_lost_threshold = 300  # 5 min without success = lost
        self._reconnect_count = 0
        self._last_health_check = 0.0
        self._health_check_interval = 60

    def record_api_call(self, duration_seconds: float, success: bool):
        """Record an API call result."""
        if success:
            self._success_count += 1
            self._last_successful_call = time.time()
            self._response_times.append(duration_seconds)
            if len(self._response_times) > self._max_samples:
                self._response_times = self._response_times[-self._max_samples:]
        else:
            self._error_count += 1

    def is_connected(self) -> bool:
        """Check if exchange connection appears healthy."""
        time_since_success = time.time() - self._last_successful_call
        return time_since_success < self._connection_lost_threshold

    def should_reconnect(self) -> bool:
        """Check if we should attempt to reconnect."""
        if self.is_connected():
            return False
        return True

    def record_reconnect(self):
        """Record a reconnection attempt."""
        self._reconnect_count += 1

    def get_health_score(self) -> float:
        """
        Get connection health score (0-100).

        Components:
        - Recency of last successful call
        - Error rate
        - Average response time
        """
        score = 100.0

        # Recency penalty
        time_since_success = time.time() - self._last_successful_call
        if time_since_success > 120:
            score -= min(50, time_since_success / 6)  # -50 at 5 min

        # Error rate penalty
        total = self._success_count + self._error_count
        if total > 10:
            error_rate = self._error_count / total
            score -= error_rate * 30  # Up to -30 for 100% error rate

        # Response time penalty
        if self._response_times:
            avg_time = sum(self._response_times) / len(self._response_times)
            if avg_time > 5:
                score -= min(20, (avg_time - 5) * 4)  # -20 at 10s avg

        return max(0, min(100, score))

    def get_stats(self) -> Dict[str, Any]:
        """Get connection statistics."""
        total = self._success_count + self._error_count
        avg_response = (sum(self._response_times) / len(self._response_times)
                        if self._response_times else 0)
        return {
            'health_score': round(self.get_health_score()),
            'connected': self.is_connected(),
            'total_calls': total,
            'error_rate': f"{(self._error_count / total * 100) if total > 0 else 0:.1f}%",
            'avg_response_ms': round(avg_response * 1000),
            'reconnects': self._reconnect_count,
            'seconds_since_success': round(time.time() - self._last_successful_call),
        }


class FlashCrashDetector:
    """
    Detect flash crashes and extreme price movements for emergency response.

    Monitors price changes across multiple time windows and triggers
    alerts when movement exceeds thresholds.
    """

    def __init__(self):
        self._price_history: list = []  # (timestamp, price) tuples
        self._max_history = 300  # ~5 min at 1s intervals
        self._alert_active = False
        self._alert_start_time = 0.0
        self._alert_cooldown = 300  # 5 min cooldown after alert

        # Thresholds (percent drop over time window)
        self.thresholds = {
            60: -3.0,    # 3% drop in 1 minute
            300: -5.0,   # 5% drop in 5 minutes
            900: -8.0,   # 8% drop in 15 minutes
        }

    def update(self, price: float) -> Dict[str, Any]:
        """
        Update with new price and check for flash crash conditions.

        Returns:
            Dict with 'crash_detected', 'severity', 'max_drop_pct', 'window'
        """
        now = time.time()
        self._price_history.append((now, price))

        # Prune old entries
        cutoff = now - max(self.thresholds.keys()) - 60
        self._price_history = [(t, p) for t, p in self._price_history if t > cutoff]

        if len(self._price_history) < 3:
            return {'crash_detected': False, 'severity': 0, 'max_drop_pct': 0}

        # Check cooldown
        if self._alert_active and now - self._alert_start_time < self._alert_cooldown:
            return {'crash_detected': True, 'severity': 0.5, 'max_drop_pct': 0,
                    'message': 'Flash crash cooldown active'}

        max_drop = 0.0
        trigger_window = 0
        severity = 0.0

        for window_seconds, threshold_pct in self.thresholds.items():
            # Find max price in the window
            window_start = now - window_seconds
            window_prices = [p for t, p in self._price_history if t >= window_start]

            if not window_prices:
                continue

            max_price = max(window_prices)
            if max_price <= 0:
                continue

            drop_pct = ((price - max_price) / max_price) * 100

            if drop_pct < threshold_pct:
                drop_severity = abs(drop_pct / threshold_pct)
                if drop_severity > severity:
                    severity = drop_severity
                    max_drop = drop_pct
                    trigger_window = window_seconds

        crash_detected = severity >= 1.0

        if crash_detected and not self._alert_active:
            self._alert_active = True
            self._alert_start_time = now
            logger.critical(
                f"FLASH CRASH DETECTED: {max_drop:.1f}% drop in {trigger_window}s "
                f"(severity: {severity:.1f}x threshold)"
            )

        if not crash_detected:
            self._alert_active = False

        return {
            'crash_detected': crash_detected,
            'severity': severity,
            'max_drop_pct': max_drop,
            'window_seconds': trigger_window,
        }

    def is_alert_active(self) -> bool:
        """Check if a flash crash alert is currently active."""
        if not self._alert_active:
            return False
        if time.time() - self._alert_start_time > self._alert_cooldown:
            self._alert_active = False
            return False
        return True


class PortfolioHeatTracker:
    """
    Track portfolio risk exposure ("heat") for dynamic position sizing.

    Heat increases with:
    - More open positions
    - Larger unrealized losses
    - Higher volatility
    - Correlated positions

    Heat decreases with:
    - Realized profits
    - Position closures
    - Lower volatility
    """

    def __init__(self, max_heat: float = 100.0):
        self.max_heat = max_heat
        self._current_heat = 0.0
        self._components: Dict[str, float] = {}

    def calculate_heat(self, open_positions: int, unrealized_pnl: float,
                       total_investment: float, volatility: float,
                       drawdown_pct: float) -> float:
        """
        Calculate current portfolio heat (0-100).

        Returns:
            Heat value where 0 = cold (safe to add risk),
            100 = max heat (reduce positions)
        """
        heat = 0.0

        # Position count heat (0-25)
        position_heat = min(25, open_positions * 2.5)
        self._components['positions'] = position_heat
        heat += position_heat

        # Unrealized loss heat (0-30)
        if total_investment > 0 and unrealized_pnl < 0:
            loss_pct = abs(unrealized_pnl / total_investment) * 100
            loss_heat = min(30, loss_pct * 3)
            self._components['unrealized_loss'] = loss_heat
            heat += loss_heat
        else:
            self._components['unrealized_loss'] = 0

        # Volatility heat (0-25)
        vol_heat = min(25, max(0, (volatility - 2) * 5))
        self._components['volatility'] = vol_heat
        heat += vol_heat

        # Drawdown heat (0-20)
        dd_heat = min(20, drawdown_pct * 2)
        self._components['drawdown'] = dd_heat
        heat += dd_heat

        self._current_heat = min(self.max_heat, heat)
        return self._current_heat

    def get_position_size_multiplier(self) -> float:
        """
        Get a multiplier for position sizing based on current heat.

        Heat 0-30: 1.0x (full size)
        Heat 30-60: 0.7x (reduced)
        Heat 60-80: 0.4x (significantly reduced)
        Heat 80+: 0.2x (minimal)
        """
        heat = self._current_heat
        if heat <= 30:
            return 1.0
        elif heat <= 60:
            return 0.7 - (heat - 30) * 0.01  # 0.7 to 0.4
        elif heat <= 80:
            return 0.4 - (heat - 60) * 0.01  # 0.4 to 0.2
        else:
            return 0.2

    def should_reduce_exposure(self) -> bool:
        """Check if we should actively reduce positions."""
        return self._current_heat > 70

    def get_status(self) -> Dict[str, Any]:
        """Get heat status."""
        return {
            'heat': round(self._current_heat, 1),
            'max_heat': self.max_heat,
            'size_multiplier': round(self.get_position_size_multiplier(), 2),
            'should_reduce': self.should_reduce_exposure(),
            'components': {k: round(v, 1) for k, v in self._components.items()},
        }


class Heartbeat:
    """
    Heartbeat system for external monitoring.

    Writes a heartbeat file that external monitors (cron, systemd)
    can check to verify the bot is running and healthy.
    """

    def __init__(self, heartbeat_file: str, interval: float = 60):
        self.heartbeat_file = heartbeat_file
        self.interval = interval
        self._last_beat = 0.0

    def beat(self, status: Dict[str, Any]):
        """Write a heartbeat with current status."""
        now = time.time()
        if now - self._last_beat < self.interval:
            return

        self._last_beat = now
        heartbeat_data = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'uptime_seconds': status.get('uptime_seconds', 0),
            'cycles': status.get('cycles', 0),
            'health_score': status.get('health_score', 0),
            'regime': status.get('regime', 'UNKNOWN'),
            'portfolio_heat': status.get('portfolio_heat', 0),
            'pid': os.getpid(),
        }

        try:
            temp = self.heartbeat_file + '.tmp'
            with open(temp, 'w') as f:
                json.dump(heartbeat_data, f)
            os.replace(temp, self.heartbeat_file)
        except Exception as e:
            logger.debug(f"Heartbeat write failed: {e}")


class SessionHealth:
    """
    Track overall session health for decision making.

    Combines connection health, trading performance, and system
    metrics into a single health score.
    """

    def __init__(self):
        self._start_time = time.time()
        self._connection_health = 100.0
        self._trading_health = 100.0
        self._system_health = 100.0
        self._consecutive_errors = 0
        self._max_consecutive_errors = 10
        self._degraded_mode = False

    def update(self, connection_score: float, trading_ok: bool,
               error_occurred: bool = False):
        """Update session health with latest data."""
        self._connection_health = connection_score

        if trading_ok:
            self._trading_health = min(100, self._trading_health + 2)
            self._consecutive_errors = 0
        else:
            self._trading_health = max(0, self._trading_health - 5)

        if error_occurred:
            self._consecutive_errors += 1
            if self._consecutive_errors >= self._max_consecutive_errors:
                if not self._degraded_mode:
                    self._degraded_mode = True
                    logger.warning(
                        f"[Health] Entering DEGRADED mode after "
                        f"{self._consecutive_errors} consecutive errors"
                    )
        else:
            if self._consecutive_errors > 0:
                self._consecutive_errors = max(0, self._consecutive_errors - 1)
            if self._consecutive_errors == 0 and self._degraded_mode:
                self._degraded_mode = False
                logger.info("[Health] Recovered from DEGRADED mode")

    def get_overall_score(self) -> float:
        """Get overall health score (0-100)."""
        return (self._connection_health * 0.4
                + self._trading_health * 0.4
                + self._system_health * 0.2)

    def is_degraded(self) -> bool:
        """Check if session is in degraded mode."""
        return self._degraded_mode

    def should_emergency_stop(self) -> bool:
        """Check if conditions warrant emergency stop."""
        return self._consecutive_errors >= self._max_consecutive_errors * 2

    def get_uptime_seconds(self) -> float:
        """Get session uptime."""
        return time.time() - self._start_time

    def get_status(self) -> Dict[str, Any]:
        """Get full health status."""
        return {
            'overall_score': round(self.get_overall_score()),
            'connection_health': round(self._connection_health),
            'trading_health': round(self._trading_health),
            'system_health': round(self._system_health),
            'consecutive_errors': self._consecutive_errors,
            'degraded_mode': self._degraded_mode,
            'uptime_seconds': round(self.get_uptime_seconds()),
        }

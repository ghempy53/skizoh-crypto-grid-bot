# =============================================================================
# Notifier - lightweight push alerts (ntfy.sh / generic webhook / Telegram)
#
# stdlib-only (urllib), fail-silent, rate-limited per event key so a crash
# loop or flapping regime can't spam the user.
# =============================================================================

import json
import logging
import threading
import time
import urllib.request
import urllib.parse
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class Notifier:
    """Sends alerts to any of: an ntfy.sh topic, a generic JSON webhook,
    or a Telegram bot. All channels are optional; with none configured the
    notifier is a no-op.

    Config (under the top-level "alerts" key in config.json):
        {
            "ntfy_topic": "my-gridbot-alerts",
            "webhook_url": "https://...",
            "telegram_bot_token": "...",
            "telegram_chat_id": "...",
            "min_interval_seconds": 300
        }
    """

    HTTP_TIMEOUT = 10  # seconds

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        config = config or {}
        self.ntfy_topic = (config.get('ntfy_topic') or '').strip()
        self.webhook_url = (config.get('webhook_url') or '').strip()
        self.telegram_token = (config.get('telegram_bot_token') or '').strip()
        self.telegram_chat_id = str(config.get('telegram_chat_id') or '').strip()
        self.min_interval = float(config.get('min_interval_seconds', 300))
        self._last_sent: Dict[str, float] = {}
        self._lock = threading.Lock()

    @property
    def enabled(self) -> bool:
        return bool(self.ntfy_topic or self.webhook_url
                    or (self.telegram_token and self.telegram_chat_id))

    def send(self, title: str, message: str, key: Optional[str] = None,
             priority: str = 'default') -> bool:
        """Send an alert. ``key`` groups related alerts for rate limiting
        (defaults to the title). Returns True if at least one channel
        accepted the message. Never raises.
        """
        if not self.enabled:
            return False

        rate_key = key or title
        now = time.monotonic()
        with self._lock:
            last = self._last_sent.get(rate_key, 0.0)
            if now - last < self.min_interval:
                return False
            self._last_sent[rate_key] = now

        sent = False
        if self.ntfy_topic:
            sent |= self._send_ntfy(title, message, priority)
        if self.webhook_url:
            sent |= self._send_webhook(title, message, priority)
        if self.telegram_token and self.telegram_chat_id:
            sent |= self._send_telegram(title, message)
        return sent

    # ------------------------------------------------------------------
    # Channels
    # ------------------------------------------------------------------

    def _send_ntfy(self, title: str, message: str, priority: str) -> bool:
        try:
            url = f"https://ntfy.sh/{urllib.parse.quote(self.ntfy_topic)}"
            req = urllib.request.Request(
                url, data=message.encode('utf-8'), method='POST',
                headers={
                    'Title': title.encode('ascii', 'ignore').decode(),
                    'Priority': priority,
                    'Tags': 'robot',
                })
            with urllib.request.urlopen(req, timeout=self.HTTP_TIMEOUT) as resp:
                return 200 <= resp.status < 300
        except Exception as e:
            logger.debug(f"ntfy alert failed: {e}")
            return False

    def _send_webhook(self, title: str, message: str, priority: str) -> bool:
        try:
            payload = json.dumps({
                'title': title, 'message': message,
                'priority': priority, 'source': 'skizoh-grid-bot',
                'timestamp': time.time(),
            }).encode('utf-8')
            req = urllib.request.Request(
                self.webhook_url, data=payload, method='POST',
                headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=self.HTTP_TIMEOUT) as resp:
                return 200 <= resp.status < 300
        except Exception as e:
            logger.debug(f"webhook alert failed: {e}")
            return False

    def _send_telegram(self, title: str, message: str) -> bool:
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = urllib.parse.urlencode({
                'chat_id': self.telegram_chat_id,
                'text': f"*{title}*\n{message}",
                'parse_mode': 'Markdown',
            }).encode('utf-8')
            req = urllib.request.Request(url, data=payload, method='POST')
            with urllib.request.urlopen(req, timeout=self.HTTP_TIMEOUT) as resp:
                return 200 <= resp.status < 300
        except Exception as e:
            logger.debug(f"telegram alert failed: {e}")
            return False


# Module-level singleton so deeply nested code can alert without plumbing.
_notifier = Notifier()


def configure(config: Optional[Dict[str, Any]]) -> Notifier:
    """Configure the global notifier from the "alerts" config section."""
    global _notifier
    _notifier = Notifier(config)
    if _notifier.enabled:
        logger.info("[Alerts] Notifier enabled")
    else:
        logger.info("[Alerts] No alert channels configured (see 'alerts' in config)")
    return _notifier


def notify(title: str, message: str, key: Optional[str] = None,
           priority: str = 'default') -> bool:
    return _notifier.send(title, message, key=key, priority=priority)

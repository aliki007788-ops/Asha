# ==========================================
# event_bus.py
# Version: 0.1.0
# Last Change: Initial Event Bus (in-memory + Redis-ready interface) (2026-09-14)
# Impact Set (v0.1.0): orchestrator.py
# Caller Audit: N/A (bootstrap)
# Adapter Audit: N/A
# ==========================================

"""
ASHA Event Bus

ارتباط غیرهمزمان بین ایجنت‌ها.
در نسخه فعلی از حافظه داخلی استفاده می‌کند.
در نسخه‌های بعدی به Redis Streams یا RabbitMQ مهاجرت می‌کند.
"""

from __future__ import annotations

import asyncio
import logging
from collections import defaultdict
from typing import Any, Callable, Awaitable, Optional

logger = logging.getLogger("asha.core.event_bus")

EventHandler = Callable[[dict[str, Any]], Awaitable[None]]


class EventBus:
    """باسبار رویداد غیرهمزمان آشا."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[EventHandler]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def publish(self, topic: str, event: dict[str, Any]) -> None:
        """
        انتشار رویداد روی یک موضوع.

        Args:
            topic: نام موضوع (مثلاً system.task)
            event: دیکشنری رویداد
        """
        handlers = list(self._subscribers.get(topic, []))
        if not handlers:
            logger.debug("No subscribers for topic: %s", topic)
            return

        logger.debug("Publishing to %s → %d handlers", topic, len(handlers))
        tasks = [self._safe_call(handler, event) for handler in handlers]
        await asyncio.gather(*tasks)

    async def subscribe(self, topic: str, handler: EventHandler) -> None:
        """عضویت یک handler در موضوع."""
        async with self._lock:
            self._subscribers[topic].append(handler)
            logger.info("Subscribed handler to topic: %s", topic)

    async def unsubscribe(self, topic: str, handler: EventHandler) -> None:
        """لغو عضویت یک handler."""
        async with self._lock:
            if handler in self._subscribers[topic]:
                self._subscribers[topic].remove(handler)
                logger.info("Unsubscribed handler from topic: %s", topic)

    async def unsubscribe_all(self) -> None:
        """لغو تمام عضویت‌ها."""
        async with self._lock:
            self._subscribers.clear()
            logger.info("All subscriptions cleared")

    def list_topics(self) -> list[str]:
        return list(self._subscribers.keys())

    async def _safe_call(self, handler: EventHandler, event: dict[str, Any]) -> None:
        """فراخوانی امن handler با مدیریت خطا."""
        try:
            await handler(event)
        except Exception:
            logger.exception("Error in event handler for event: %s", event)

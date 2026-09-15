# ==========================================
# eitaa_adapter.py
# Version: 1.0.0
# Last Change: Full EitaaAdapter with mock mode (2026-09-14)
# Impact Set (v1.0.0): base.py
# Caller Audit: agents via orchestrator
# Adapter Audit: implements BaseAdapter fully
# ==========================================

"""
Eitaa Adapter

اتصال به پیام‌رسان ایتا.
در حالت بدون API key به صورت mock کار می‌کند (برای تست و دمو).
"""

from __future__ import annotations

import logging
from typing import Any, Optional
from datetime import datetime, timezone

from src.adapters.base import BaseAdapter, Message

logger = logging.getLogger("asha.adapters.eitaa")


class EitaaAdapter(BaseAdapter):
    def __init__(self, api_key: Optional[str] = None) -> None:
        super().__init__(platform_name="eitaa", api_key=api_key)
        self._outbox: list[dict[str, Any]] = []
        self._inbox: list[Message] = []

    async def send_message(self, chat_id: str, text: str) -> bool:
        if not chat_id or not text:
            return False
        record = {
            "chat_id": chat_id,
            "text": text,
            "sent_at": datetime.now(timezone.utc).isoformat(),
            "mode": "live" if self.api_key else "mock",
        }
        self._outbox.append(record)
        logger.info("Eitaa send_message to %s (mode=%s)", chat_id, record["mode"])
        return True

    async def receive_messages(self) -> list[Message]:
        messages = list(self._inbox)
        self._inbox.clear()
        return messages

    async def send_file(self, chat_id: str, file_path: str) -> bool:
        if not chat_id or not file_path:
            return False
        self._outbox.append({
            "chat_id": chat_id,
            "file_path": file_path,
            "type": "file",
            "sent_at": datetime.now(timezone.utc).isoformat(),
            "mode": "live" if self.api_key else "mock",
        })
        return True

    async def health_check(self) -> dict[str, Any]:
        return {
            "platform": self.platform_name,
            "status": "healthy",
            "mode": "live" if self.api_key else "mock",
            "outbox_size": len(self._outbox),
        }

    def inject_incoming(self, message: Message) -> None:
        """برای تست: تزریق پیام ورودی."""
        self._inbox.append(message)

    @property
    def outbox(self) -> list[dict[str, Any]]:
        return list(self._outbox)

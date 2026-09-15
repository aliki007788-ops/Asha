# ==========================================
# instagram_bridge.py
# Version: 1.0.0
# Last Change: Instagram Bridge (mock + interface) (2026-09-14)
# Impact Set (v1.0.0): base.py
# Caller Audit: N/A
# Adapter Audit: implements BaseAdapter fully
# ==========================================

"""
Instagram Bridge

لایه واسط برای اینستاگرام (از طریق Graph API / RSSHub و مشابه).
بدون توکن واقعی در حالت mock کار می‌کند.
"""

from __future__ import annotations

from typing import Any, Optional
from datetime import datetime, timezone

from src.adapters.base import BaseAdapter, Message


class InstagramBridge(BaseAdapter):
    def __init__(self, api_key: Optional[str] = None) -> None:
        super().__init__(platform_name="instagram", api_key=api_key)
        self._outbox: list[dict[str, Any]] = []
        self._inbox: list[Message] = []

    async def send_message(self, chat_id: str, text: str) -> bool:
        if not chat_id or not text:
            return False
        self._outbox.append({
            "chat_id": chat_id,
            "text": text,
            "sent_at": datetime.now(timezone.utc).isoformat(),
            "mode": "live" if self.api_key else "mock",
        })
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
            "bridge": True,
        }

    def inject_incoming(self, message: Message) -> None:
        self._inbox.append(message)

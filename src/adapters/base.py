# ==========================================
# base.py
# Version: 0.1.0
# Last Change: Initial BaseAdapter abstract class (2026-09-14)
# Impact Set (v0.1.0): all future adapters
# Caller Audit: N/A (bootstrap)
# Adapter Audit: N/A
# ==========================================

"""
ASHA Base Adapter

اینترفیس مشترک برای تمام Adapterهای پلتفرم‌ها.
هر پلتفرم جدید فقط نیاز به پیاده‌سازی این کلاس دارد.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Message:
    """پیام استاندارد آشا."""
    chat_id: str
    text: str
    sender_id: Optional[str] = None
    message_id: Optional[str] = None
    timestamp: Optional[str] = None
    raw: Optional[dict[str, Any]] = None


class BaseAdapter(ABC):
    """کلاس پایه Adapterهای پلتفرم."""

    def __init__(self, platform_name: str, api_key: Optional[str] = None) -> None:
        self.platform_name = platform_name
        self.api_key = api_key

    @abstractmethod
    async def send_message(self, chat_id: str, text: str) -> bool:
        """ارسال پیام متنی."""
        ...

    @abstractmethod
    async def receive_messages(self) -> list[Message]:
        """دریافت پیام‌های جدید."""
        ...

    @abstractmethod
    async def send_file(self, chat_id: str, file_path: str) -> bool:
        """ارسال فایل."""
        ...

    async def health_check(self) -> dict[str, Any]:
        """بررسی سلامت اتصال به پلتفرم."""
        return {
            "platform": self.platform_name,
            "status": "unknown",
        }

    def __repr__(self) -> str:
        return f"<Adapter {self.platform_name}>"

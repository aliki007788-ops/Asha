# ==========================================
# base.py
# Version: 0.1.0
# Last Change: Initial BasePlugin abstract class (2026-09-14)
# Impact Set (v0.1.0): loader.py
# Caller Audit: N/A (bootstrap)
# Adapter Audit: N/A
# ==========================================

"""
ASHA Base Plugin

کلاس پایه برای Pluginهای ثالث که به آشا اضافه می‌شوند.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BasePlugin(ABC):
    """کلاس پایه Plugin."""

    def __init__(
        self,
        plugin_id: str,
        name: str,
        version: str = "0.1.0",
    ) -> None:
        self.plugin_id = plugin_id
        self.name = name
        self.version = version

    @abstractmethod
    async def initialize(self, context: dict[str, Any]) -> None:
        """راه‌اندازی اولیه Plugin با context سیستم."""
        ...

    @abstractmethod
    async def execute(self, payload: dict[str, Any]) -> Any:
        """اجرای منطق Plugin."""
        ...

    async def shutdown(self) -> None:
        """خاموشی امن Plugin."""
        pass

    def __repr__(self) -> str:
        return f"<Plugin {self.plugin_id} v{self.version}>"

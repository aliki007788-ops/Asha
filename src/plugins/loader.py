# ==========================================
# loader.py
# Version: 0.1.0
# Last Change: Initial Plugin Loader (2026-09-14)
# Impact Set (v0.1.0): base.py
# Caller Audit: N/A (bootstrap)
# Adapter Audit: N/A
# ==========================================

"""
ASHA Plugin Loader

بارگذاری و مدیریت Pluginهای ثالث.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from src.plugins.base import BasePlugin

logger = logging.getLogger("asha.plugins.loader")


class PluginLoader:
    """بارگذار Pluginهای آشا."""

    def __init__(self) -> None:
        self._plugins: dict[str, BasePlugin] = {}

    def register(self, plugin: BasePlugin) -> None:
        """ثبت یک Plugin."""
        if plugin.plugin_id in self._plugins:
            raise ValueError(f"Plugin '{plugin.plugin_id}' already registered")
        self._plugins[plugin.plugin_id] = plugin
        logger.info("Registered plugin: %s v%s", plugin.plugin_id, plugin.version)

    async def initialize_all(self, context: dict[str, Any]) -> None:
        """راه‌اندازی تمام Pluginهای ثبت‌شده."""
        for plugin_id, plugin in self._plugins.items():
            try:
                await plugin.initialize(context)
                logger.info("Initialized plugin: %s", plugin_id)
            except Exception:
                logger.exception("Failed to initialize plugin: %s", plugin_id)

    def get(self, plugin_id: str) -> Optional[BasePlugin]:
        return self._plugins.get(plugin_id)

    def list_plugins(self) -> list[str]:
        return list(self._plugins.keys())

    async def shutdown_all(self) -> None:
        """خاموشی تمام Pluginها."""
        for plugin_id, plugin in self._plugins.items():
            try:
                await plugin.shutdown()
                logger.info("Shutdown plugin: %s", plugin_id)
            except Exception:
                logger.exception("Failed to shutdown plugin: %s", plugin_id)

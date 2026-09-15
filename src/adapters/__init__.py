# ==========================================
# __init__.py
# Version: 1.0.0
# Last Change: Export all adapters (2026-09-14)
# Impact Set (v1.0.0): all adapter modules
# Caller Audit: N/A
# Adapter Audit: N/A
# ==========================================

from src.adapters.base import BaseAdapter, Message
from src.adapters.eitaa_adapter import EitaaAdapter
from src.adapters.bale_adapter import BaleAdapter
from src.adapters.rubika_adapter import RubikaAdapter
from src.adapters.divar_adapter import DivarAdapter
from src.adapters.torob_adapter import TorobAdapter
from src.adapters.emalls_adapter import EmallsAdapter
from src.adapters.telegram_bridge import TelegramBridge
from src.adapters.instagram_bridge import InstagramBridge

__all__ = [
    "BaseAdapter",
    "Message",
    "EitaaAdapter",
    "BaleAdapter",
    "RubikaAdapter",
    "DivarAdapter",
    "TorobAdapter",
    "EmallsAdapter",
    "TelegramBridge",
    "InstagramBridge",
]


# ==========================================
# config.py
# Version: 0.1.0
# Last Change: Initial ASHA Config with industry support (2026-09-14)
# Impact Set (v0.1.0): orchestrator.py, state.py
# Caller Audit: N/A (bootstrap)
# Adapter Audit: N/A
# ==========================================

"""
ASHA Configuration

تنظیمات مخصوص هر صنف و هر کسب‌وکار.
از متغیرهای محیطی و فایل‌های تنظیمات پشتیبانی می‌کند.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class IndustryConfig:
    """تنظیمات مخصوص یک صنف."""
    industry_id: str
    name: str
    default_language: str = "fa"
    currency: str = "IRR"
    timezone: str = "Asia/Tehran"
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class AshaConfig:
    """تنظیمات کلی سیستم آشا."""

    # محیط اجرا
    env: str = "development"
    debug: bool = False
    log_level: str = "INFO"

    # دیتابیس
    database_url: str = "postgresql://asha:asha@localhost:5432/asha"

    # Redis (Event Bus)
    redis_url: str = "redis://localhost:6379/0"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # صنف فعلی
    industry: Optional[IndustryConfig] = None

    # کلیدهای پلتفرم‌ها (از .env خوانده می‌شود)
    eitaa_api_key: Optional[str] = None
    bale_api_key: Optional[str] = None
    rubika_api_key: Optional[str] = None
    divar_api_key: Optional[str] = None
    torob_api_key: Optional[str] = None
    emalls_api_key: Optional[str] = None

    @classmethod
    def from_env(cls) -> "AshaConfig":
        """ساخت تنظیمات از متغیرهای محیطی."""
        return cls(
            env=os.getenv("ASHA_ENV", "development"),
            debug=os.getenv("ASHA_DEBUG", "false").lower() == "true",
            log_level=os.getenv("ASHA_LOG_LEVEL", "INFO"),
            database_url=os.getenv(
                "DATABASE_URL",
                "postgresql://asha:asha@localhost:5432/asha",
            ),
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            api_host=os.getenv("API_HOST", "0.0.0.0"),
            api_port=int(os.getenv("API_PORT", "8000")),
            eitaa_api_key=os.getenv("EITAA_API_KEY"),
            bale_api_key=os.getenv("BALE_API_KEY"),
            rubika_api_key=os.getenv("RUBIKA_API_KEY"),
            divar_api_key=os.getenv("DIVAR_API_KEY"),
            torob_api_key=os.getenv("TOROB_API_KEY"),
            emalls_api_key=os.getenv("EMALLS_API_KEY"),
        )

    def set_industry(self, industry: IndustryConfig) -> None:
        """تنظیم صنف فعلی."""
        self.industry = industry

    def get(self, key: str, default: Any = None) -> Any:
        """دسترسی عمومی به تنظیمات."""
        return getattr(self, key, default)

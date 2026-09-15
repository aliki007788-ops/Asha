# ==========================================
# upsell.py
# Version: 1.0.0
# Last Change: Full UpsellAgent implementation (2026-09-14)
# Impact Set (v1.0.0): base.py
# Caller Audit: orchestrator via registry
# Adapter Audit: N/A
# ==========================================

"""
Upsell Agent

ایجنت افزایش فروش — پیشنهاد محصولات مکمل و ارتقا.
"""

from __future__ import annotations

from typing import Any

from src.agents.base import BaseAgent


class UpsellAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            agent_id="upsell",
            name="Upsell",
            version="1.0.0",
            description="پیشنهاد محصول مکمل و افزایش سبد خرید",
        )

    async def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        purchased = payload.get("purchased_product", "")
        customer_name = payload.get("customer_name", "مشتری")
        catalog = payload.get("catalog", [])

        suggestions = self._suggest(purchased, catalog)
        message = self._craft_message(customer_name, purchased, suggestions)

        return {
            "agent_id": self.agent_id,
            "status": "success",
            "purchased_product": purchased,
            "suggestions": suggestions,
            "message": message,
        }

    def _suggest(self, purchased: str, catalog: list) -> list[dict[str, Any]]:
        if catalog:
            return [
                {"name": c.get("name"), "price": c.get("price"), "reason": c.get("reason", "مکمل مناسب")}
                for c in catalog[:3]
            ]
        # پیشنهادهای پیش‌فرض بر اساس نام محصول
        defaults = {
            "گوشی": [{"name": "کاور محافظ", "price": 150000, "reason": "محافظت از دستگاه"}],
            "لپ‌تاپ": [{"name": "کیف لپ‌تاپ", "price": 450000, "reason": "حمل آسان و ایمن"}],
        }
        for key, items in defaults.items():
            if key in purchased:
                return items
        return [{"name": "گارانتی تمدید شده", "price": 200000, "reason": "آرامش خاطر بیشتر"}]

    def _craft_message(self, customer_name: str, purchased: str, suggestions: list) -> str:
        if not suggestions:
            return f"{customer_name} عزیز، از خریدتون ممنونیم!"
        names = "، ".join(s["name"] for s in suggestions)
        return (
            f"{customer_name} عزیز، از خرید {purchased} ممنونیم! "
            f"پیشنهاد ما برای تکمیل تجربه شما: {names}. "
            "اگر مایلید اضافه کنم بفرمایید."
        )

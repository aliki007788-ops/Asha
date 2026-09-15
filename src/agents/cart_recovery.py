# ==========================================
# cart_recovery.py
# Version: 1.0.0
# Last Change: Full CartRecoveryAgent implementation (2026-09-14)
# Impact Set (v1.0.0): base.py
# Caller Audit: orchestrator via registry
# Adapter Audit: N/A
# ==========================================

from __future__ import annotations

from typing import Any

from src.agents.base import BaseAgent


class CartRecoveryAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            agent_id="cart_recovery",
            name="Cart Recovery",
            version="1.0.0",
            description="بازیابی سبد خرید رها شده",
        )

    async def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        customer_name = payload.get("customer_name", "مشتری")
        cart_items = payload.get("cart_items", [])
        hours_abandoned = int(payload.get("hours_abandoned", 24))
        discount_code = payload.get("discount_code")

        urgency = "بالا" if hours_abandoned >= 48 else "متوسط" if hours_abandoned >= 12 else "کم"
        message = self._build_message(customer_name, cart_items, hours_abandoned, discount_code)

        return {
            "agent_id": self.agent_id,
            "status": "success",
            "customer_name": customer_name,
            "cart_items": cart_items,
            "hours_abandoned": hours_abandoned,
            "urgency": urgency,
            "message": message,
            "discount_code": discount_code,
        }

    def _build_message(
        self,
        name: str,
        items: list,
        hours: int,
        code: str | None,
    ) -> str:
        item_names = "، ".join(
            (i.get("name") if isinstance(i, dict) else str(i)) for i in items
        ) or "محصولات انتخابی"
        msg = (
            f"{name} عزیز، سبد خریدتون هنوز منتظر شماست! "
            f"اقلام: {item_names}."
        )
        if hours >= 24:
            msg += " موجودی برخی اقلام محدود است."
        if code:
            msg += f" با کد {code} تخفیف ویژه بگیرید."
        msg += " برای تکمیل خرید آماده‌ایم."
        return msg

# ==========================================
# proposal.py
# Version: 1.0.0
# Last Change: Full ProposalAgent implementation (2026-09-14)
# Impact Set (v1.0.0): base.py
# Caller Audit: orchestrator via registry
# Adapter Audit: N/A
# ==========================================

"""
Proposal Agent

ایجنت پیشنهاد قیمت و پروپوزال — ساخت پیشنهاد رسمی برای مشتری.
"""

from __future__ import annotations

from typing import Any
from datetime import datetime, timezone, timedelta

from src.agents.base import BaseAgent


class ProposalAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            agent_id="proposal",
            name="Proposal",
            version="1.0.0",
            description="ساخت پیشنهاد قیمت و پروپوزال رسمی",
        )

    async def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        customer_name = payload.get("customer_name", "مشتری")
        items = payload.get("items", [])
        discount_percent = float(payload.get("discount_percent", 0))
        valid_days = int(payload.get("valid_days", 7))
        notes = payload.get("notes", "")

        line_items = []
        subtotal = 0.0
        for item in items:
            qty = float(item.get("qty", 1))
            unit_price = float(item.get("unit_price", 0))
            line_total = qty * unit_price
            subtotal += line_total
            line_items.append({
                "name": item.get("name", "آیتم"),
                "qty": qty,
                "unit_price": unit_price,
                "line_total": line_total,
            })

        discount_amount = subtotal * (discount_percent / 100.0)
        total = subtotal - discount_amount
        valid_until = (datetime.now(timezone.utc) + timedelta(days=valid_days)).date().isoformat()

        proposal_text = self._render_proposal(
            customer_name, line_items, subtotal, discount_percent, discount_amount, total, valid_until, notes
        )

        return {
            "agent_id": self.agent_id,
            "status": "success",
            "customer_name": customer_name,
            "line_items": line_items,
            "subtotal": subtotal,
            "discount_percent": discount_percent,
            "discount_amount": discount_amount,
            "total": total,
            "valid_until": valid_until,
            "proposal_text": proposal_text,
        }

    def _render_proposal(
        self,
        customer_name: str,
        line_items: list,
        subtotal: float,
        discount_percent: float,
        discount_amount: float,
        total: float,
        valid_until: str,
        notes: str,
    ) -> str:
        lines = [f"پیشنهاد قیمت برای {customer_name}", "", "اقلام:"]
        for li in line_items:
            lines.append(f"  - {li['name']}: {li['qty']} × {li['unit_price']:,.0f} = {li['line_total']:,.0f}")
        lines.append("")
        lines.append(f"جمع جزء: {subtotal:,.0f} ریال")
        if discount_percent > 0:
            lines.append(f"تخفیف ({discount_percent}%): −{discount_amount:,.0f} ریال")
        lines.append(f"مبلغ نهایی: {total:,.0f} ریال")
        lines.append(f"اعتبار پیشنهاد تا: {valid_until}")
        if notes:
            lines.append(f"\nتوضیحات: {notes}")
        return "\n".join(lines)

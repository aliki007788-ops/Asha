# ==========================================
# invoice.py
# Version: 1.0.0
# Last Change: Full InvoiceAgent implementation (2026-09-14)
# Impact Set (v1.0.0): base.py
# Caller Audit: orchestrator via registry
# Adapter Audit: N/A
# ==========================================

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import uuid

from src.agents.base import BaseAgent


class InvoiceAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            agent_id="invoice",
            name="Invoice",
            version="1.0.0",
            description="صدور فاکتور و صورتحساب",
        )

    async def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        customer_name = payload.get("customer_name", "مشتری")
        items = payload.get("items", [])
        tax_percent = float(payload.get("tax_percent", 9))

        line_items = []
        subtotal = 0.0
        for item in items:
            qty = float(item.get("qty", 1))
            unit = float(item.get("unit_price", 0))
            total = qty * unit
            subtotal += total
            line_items.append({
                "name": item.get("name", "آیتم"),
                "qty": qty,
                "unit_price": unit,
                "total": total,
            })

        tax = subtotal * (tax_percent / 100.0)
        grand_total = subtotal + tax
        invoice_id = f"INV-{uuid.uuid4().hex[:8].upper()}"
        issued_at = datetime.now(timezone.utc).isoformat()

        text = self._render(invoice_id, customer_name, line_items, subtotal, tax_percent, tax, grand_total, issued_at)

        return {
            "agent_id": self.agent_id,
            "status": "success",
            "invoice_id": invoice_id,
            "customer_name": customer_name,
            "line_items": line_items,
            "subtotal": subtotal,
            "tax_percent": tax_percent,
            "tax": tax,
            "grand_total": grand_total,
            "issued_at": issued_at,
            "invoice_text": text,
        }

    def _render(
        self,
        invoice_id: str,
        customer: str,
        lines: list,
        subtotal: float,
        tax_pct: float,
        tax: float,
        grand: float,
        issued_at: str,
    ) -> str:
        parts = [
            f"فاکتور شماره: {invoice_id}",
            f"تاریخ: {issued_at}",
            f"مشتری: {customer}",
            "",
            "اقلام:",
        ]
        for li in lines:
            parts.append(f"  {li['name']} | {li['qty']} × {li['unit_price']:,.0f} = {li['total']:,.0f}")
        parts.extend([
            "",
            f"جمع: {subtotal:,.0f}",
            f"مالیات ({tax_pct}%): {tax:,.0f}",
            f"مبلغ قابل پرداخت: {grand:,.0f} ریال",
        ])
        return "\n".join(parts)

# ==========================================
# pricing.py
# Version: 1.0.0
# Last Change: Full Pricing helper (2026-09-14)
# Impact Set (v1.0.0): support layer
# Caller Audit: proposal, invoice agents
# Adapter Audit: N/A
# ==========================================

from __future__ import annotations


class PricingEngine:
    @staticmethod
    def apply_discount(amount: float, percent: float) -> float:
        if percent < 0 or percent > 100:
            raise ValueError("discount percent must be between 0 and 100")
        return amount * (1 - percent / 100.0)

    @staticmethod
    def apply_tax(amount: float, tax_percent: float = 9.0) -> float:
        return amount * (1 + tax_percent / 100.0)

    @staticmethod
    def format_irr(amount: float) -> str:
        return f"{amount:,.0f} ریال"

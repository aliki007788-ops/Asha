# ==========================================
# compliance.py
# Version: 1.0.0
# Last Change: Compliance checks (2026-09-14)
# Impact Set (v1.0.0): support layer
# Caller Audit: N/A
# Adapter Audit: N/A
# ==========================================

from __future__ import annotations

from typing import Any


class ComplianceChecker:
    BLOCKED_KEYWORDS = ["کلاهبرداری", "قمار غیرقانونی"]

    def check_message(self, text: str) -> dict[str, Any]:
        text_l = text.lower()
        violations = [k for k in self.BLOCKED_KEYWORDS if k in text_l]
        return {
            "ok": len(violations) == 0,
            "violations": violations,
        }

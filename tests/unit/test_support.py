# ==========================================
# test_support.py
# Version: 1.0.0
# ==========================================

import pytest
from src.support_agents.memory import MemoryStore
from src.support_agents.pricing import PricingEngine
from src.support_agents.auth import AuthService
from src.support_agents.compliance import ComplianceChecker
from src.support_agents.analytics import Analytics
from src.support_agents.error_recovery import retry_async


def test_memory():
    m = MemoryStore()
    m.set("k", "v")
    assert m.get("k") == "v"
    assert m.delete("k")
    assert m.get("k") is None


def test_pricing():
    assert PricingEngine.apply_discount(1000, 10) == 900
    assert PricingEngine.apply_tax(1000, 9) == 1090
    assert "ریال" in PricingEngine.format_irr(1000)


def test_auth():
    auth = AuthService()
    token = auth.create_token("user1")
    assert auth.validate_token(token) == "user1"
    assert auth.revoke_token(token)
    assert auth.validate_token(token) is None


def test_compliance():
    c = ComplianceChecker()
    assert c.check_message("سلام عادی")["ok"] is True
    assert c.check_message("این کلاهبرداری است")["ok"] is False


def test_analytics():
    a = Analytics()
    a.track("sale", {"amount": 100})
    assert a.count("sale") == 1
    assert a.summary()["total_events"] == 1


@pytest.mark.asyncio
async def test_retry():
    attempts = {"n": 0}

    async def flaky():
        attempts["n"] += 1
        if attempts["n"] < 2:
            raise RuntimeError("fail")
        return "ok"

    result = await retry_async(flaky, max_attempts=3, delay_sec=0.01)
    assert result == "ok"
    assert attempts["n"] == 2

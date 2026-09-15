# ==========================================
# test_bootstrap.py
# Version: 1.0.0
# ==========================================

from src.bootstrap import create_system, create_registry


def test_create_registry_has_15_agents():
    reg = create_registry()
    assert len(reg) == 15
    expected = {
        "sales_closer", "outbound", "sequencer", "proposal", "upsell",
        "support", "seo_content", "video_script", "content_calendar",
        "cart_recovery", "invoice", "recruitment", "market_research",
        "personal_assistant", "agency",
    }
    assert set(reg.list_agents()) == expected


def test_create_system():
    sys = create_system()
    assert "orchestrator" in sys
    assert "registry" in sys
    assert "adapters" in sys
    assert len(sys["adapters"]) == 8
    assert len(sys["registry"]) == 15

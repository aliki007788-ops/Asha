# ==========================================
# test_registry.py
# Version: 1.0.0
# ==========================================

import pytest
from src.core.registry import AgentRegistry
from src.agents.sales_closer import SalesCloserAgent
from src.agents.support import SupportAgent


def test_register_and_get():
    reg = AgentRegistry()
    agent = SalesCloserAgent()
    reg.register(agent)
    assert reg.has("sales_closer")
    assert reg.get("sales_closer") is agent
    assert len(reg) == 1
    assert "sales_closer" in reg


def test_duplicate_register_raises():
    reg = AgentRegistry()
    reg.register(SalesCloserAgent())
    with pytest.raises(ValueError):
        reg.register(SalesCloserAgent())


def test_list_and_unregister():
    reg = AgentRegistry()
    reg.register(SalesCloserAgent())
    reg.register(SupportAgent())
    assert sorted(reg.list_agents()) == ["sales_closer", "support"]
    reg.unregister("support")
    assert not reg.has("support")
    reg.clear()
    assert len(reg) == 0

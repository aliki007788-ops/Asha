# ==========================================
# bootstrap.py
# Version: 1.0.0
# Last Change: Full system bootstrap — register all agents (2026-09-14)
# Impact Set (v1.0.0): core, agents, adapters
# Caller Audit: api.main
# Adapter Audit: N/A
# ==========================================

"""
راه‌اندازی کامل سیستم آشا — ثبت همه ایجنت‌ها و ساخت Orchestrator.
"""

from __future__ import annotations

import logging
from typing import Optional

from src.core.config import AshaConfig
from src.core.registry import AgentRegistry
from src.core.state import SystemState
from src.core.event_bus import EventBus
from src.core.orchestrator import Orchestrator
from src.agents import (
    SalesCloserAgent,
    OutboundAgent,
    SequencerAgent,
    ProposalAgent,
    UpsellAgent,
    SupportAgent,
    SeoContentAgent,
    VideoScriptAgent,
    ContentCalendarAgent,
    CartRecoveryAgent,
    InvoiceAgent,
    RecruitmentAgent,
    MarketResearchAgent,
    PersonalAssistantAgent,
    AgencyAgent,
)
from src.adapters import (
    EitaaAdapter,
    BaleAdapter,
    RubikaAdapter,
    DivarAdapter,
    TorobAdapter,
    EmallsAdapter,
    TelegramBridge,
    InstagramBridge,
)

logger = logging.getLogger("asha.bootstrap")


def create_registry() -> AgentRegistry:
    registry = AgentRegistry()
    agents = [
        SalesCloserAgent(),
        OutboundAgent(),
        SequencerAgent(),
        ProposalAgent(),
        UpsellAgent(),
        SupportAgent(),
        SeoContentAgent(),
        VideoScriptAgent(),
        ContentCalendarAgent(),
        CartRecoveryAgent(),
        InvoiceAgent(),
        RecruitmentAgent(),
        MarketResearchAgent(),
        PersonalAssistantAgent(),
        AgencyAgent(),
    ]
    for agent in agents:
        registry.register(agent)
    logger.info("Registered %d agents", len(registry))
    return registry


def create_adapters(config: AshaConfig) -> dict:
    return {
        "eitaa": EitaaAdapter(api_key=config.eitaa_api_key),
        "bale": BaleAdapter(api_key=config.bale_api_key),
        "rubika": RubikaAdapter(api_key=config.rubika_api_key),
        "divar": DivarAdapter(api_key=config.divar_api_key),
        "torob": TorobAdapter(api_key=config.torob_api_key),
        "emalls": EmallsAdapter(api_key=config.emalls_api_key),
        "telegram": TelegramBridge(api_key=None),
        "instagram": InstagramBridge(api_key=None),
    }


def create_system(config: Optional[AshaConfig] = None) -> dict:
    """ساخت کامل سیستم آشا."""
    config = config or AshaConfig.from_env()
    registry = create_registry()
    state = SystemState()
    event_bus = EventBus()
    orchestrator = Orchestrator(
        registry=registry,
        event_bus=event_bus,
        state=state,
        config=config,
    )
    adapters = create_adapters(config)
    return {
        "config": config,
        "registry": registry,
        "state": state,
        "event_bus": event_bus,
        "orchestrator": orchestrator,
        "adapters": adapters,
    }

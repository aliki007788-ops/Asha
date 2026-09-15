# ==========================================
# test_agents.py
# Version: 1.0.0
# ==========================================

import pytest
from src.agents.sales_closer import SalesCloserAgent
from src.agents.outbound import OutboundAgent
from src.agents.proposal import ProposalAgent
from src.agents.support import SupportAgent
from src.agents.invoice import InvoiceAgent
from src.agents.upsell import UpsellAgent
from src.agents.sequencer import SequencerAgent
from src.agents.cart_recovery import CartRecoveryAgent
from src.agents.seo_content import SeoContentAgent
from src.agents.video_script import VideoScriptAgent
from src.agents.content_calendar import ContentCalendarAgent
from src.agents.recruitment import RecruitmentAgent
from src.agents.market_research import MarketResearchAgent
from src.agents.personal_assistant import PersonalAssistantAgent
from src.agents.agency import AgencyAgent


@pytest.mark.asyncio
async def test_sales_closer():
    agent = SalesCloserAgent()
    result = await agent.execute({
        "conversation": [{"text": "می‌خرم قیمت چقدره؟"}],
        "customer_name": "علی",
        "product": "گوشی",
        "price": 10000000,
    })
    assert result["status"] == "success"
    assert result["intent_score"] > 0.3
    assert "closing_message" in result


@pytest.mark.asyncio
async def test_outbound():
    agent = OutboundAgent()
    result = await agent.execute({"lead_name": "سارا", "product": "دوره", "template": "intro"})
    assert result["status"] == "success"
    assert "سارا" in result["message"]


@pytest.mark.asyncio
async def test_proposal():
    agent = ProposalAgent()
    result = await agent.execute({
        "customer_name": "شرکت نمونه",
        "items": [{"name": "سرویس", "qty": 2, "unit_price": 500000}],
        "discount_percent": 10,
    })
    assert result["status"] == "success"
    assert result["subtotal"] == 1000000
    assert result["total"] == 900000


@pytest.mark.asyncio
async def test_support_faq():
    agent = SupportAgent()
    result = await agent.execute({"question": "شرایط مرجوعی چیست؟", "customer_name": "رضا"})
    assert result["status"] == "success"
    assert result["confidence"] >= 0.5
    assert "مرجوعی" in result["category"] or result["category"] == "مرجوعی"


@pytest.mark.asyncio
async def test_invoice():
    agent = InvoiceAgent()
    result = await agent.execute({
        "customer_name": "خریدار",
        "items": [{"name": "کالا", "qty": 1, "unit_price": 1000}],
        "tax_percent": 9,
    })
    assert result["status"] == "success"
    assert result["grand_total"] == 1090
    assert result["invoice_id"].startswith("INV-")


@pytest.mark.asyncio
async def test_all_agents_execute():
    agents = [
        SalesCloserAgent(), OutboundAgent(), SequencerAgent(), ProposalAgent(),
        UpsellAgent(), SupportAgent(), SeoContentAgent(), VideoScriptAgent(),
        ContentCalendarAgent(), CartRecoveryAgent(), InvoiceAgent(),
        RecruitmentAgent(), MarketResearchAgent(), PersonalAssistantAgent(),
        AgencyAgent(),
    ]
    for agent in agents:
        result = await agent.execute({})
        assert result["status"] == "success", f"{agent.agent_id} failed"
        assert result["agent_id"] == agent.agent_id

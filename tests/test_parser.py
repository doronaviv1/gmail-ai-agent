from datetime import datetime
from zoneinfo import ZoneInfo

from scheduling_agent.llm_parser import LLMMeetingParser
from scheduling_agent.models import EmailMessage


def test_fallback_parser_extracts_tomorrow_and_time():
    parser = LLMMeetingParser(api_key=None, model="unused", timezone=ZoneInfo("UTC"))
    email = EmailMessage(
        id="1",

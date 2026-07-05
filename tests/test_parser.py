from datetime import datetime
from zoneinfo import ZoneInfo

from scheduling_agent.llm_parser import LLMMeetingParser
from scheduling_agent.models import EmailMessage


def test_fallback_parser_extracts_tomorrow_and_time():
    parser = LLMMeetingParser(api_key=None, model="unused", timezone=ZoneInfo("UTC"))
    email = EmailMessage(
        id="1",
        thread_id="t1",
        sender="alex@example.com",
        subject="Quick meeting",
        body="Hi, are you free tomorrow at 2pm for a 45 minute call?",
    )

    result = parser.parse(email, now=datetime(2026, 7, 4, 12, tzinfo=ZoneInfo("UTC")))

    assert result.is_meeting_request is True
    assert result.requested_day == "2026-07-05"
    assert result.start_time == "14:00"
    assert result.duration_minutes == 45
    assert result.attendees == ["alex@example.com"]


def test_fallback_parser_skips_non_meeting_email():
    parser = LLMMeetingParser(api_key=None, model="unused", timezone=ZoneInfo("UTC"))
    email = EmailMessage(id="1", thread_id="t1", sender="a@example.com", subject="FYI", body="Here is the report.")


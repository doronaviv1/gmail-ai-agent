from datetime import time
from zoneinfo import ZoneInfo

from scheduling_agent.agent import SchedulingAgent
from scheduling_agent.config import Config
from scheduling_agent.models import EmailMessage, MeetingRequest, SchedulingAction, TimeSlot
from scheduling_agent.scheduler import Scheduler


class FakeGmail:
    def __init__(self):
        self.marked = []
        self.replies = []
        self.email = EmailMessage("m1", "t1", "alex@example.com", "Meeting", "Can we meet tomorrow?")

    def ensure_processed_label(self):
        return "label-1"

    def search_messages(self, query, max_results=10):
        return ["m1"]

    def get_message(self, message_id):
        return self.email

    def mark_processed(self, message_id, label_id):
        self.marked.append((message_id, label_id))

    def send_reply(self, original, body):
        self.replies.append((original, body))


class FakeParser:
    def parse(self, email):
        return MeetingRequest(True, "Meeting", requested_day="2026-07-06", attendees=[email.sender])


class FakeCalendar:
    def __init__(self):
        self.created = []

    def is_available(self, slot: TimeSlot):
        return True

    def create_event(self, title, slot, attendees, description):
        self.created.append((title, slot, attendees, description))
        return {"id": "event-1"}


def make_config(dry_run: bool):
    return Config(
        openai_api_key=None,
        openai_model="unused",
        google_credentials_file="credentials.json",
        google_token_file="token.json",
        google_calendar_id="primary",
        gmail_query="is:unread",
        processed_label="AI_SCHEDULER_PROCESSED",
        workday_start=time(9),
        workday_end=time(17),
        default_meeting_duration_minutes=30,
        timezone=ZoneInfo("UTC"),
        poll_interval_seconds=60,
        dry_run=dry_run,
        send_confirmation_email=True,
    )


def test_agent_dry_run_does_not_mutate_external_services():
    gmail = FakeGmail()
    calendar = FakeCalendar()
    scheduler = Scheduler(calendar, ZoneInfo("UTC"), time(9), time(17), 30)
    agent = SchedulingAgent(make_config(dry_run=True), gmail, FakeParser(), scheduler)

    decisions = agent.run_once()

    assert decisions[0].action == SchedulingAction.BOOK
    assert calendar.created == []

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

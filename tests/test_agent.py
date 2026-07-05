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

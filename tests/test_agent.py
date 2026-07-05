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

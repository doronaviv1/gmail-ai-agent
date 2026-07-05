from datetime import datetime, time
from zoneinfo import ZoneInfo

from scheduling_agent.models import MeetingRequest, SchedulingAction, TimeSlot
from scheduling_agent.scheduler import Scheduler


class FakeCalendar:
    def __init__(self, busy: list[TimeSlot] | None = None):

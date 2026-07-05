from datetime import datetime, time
from zoneinfo import ZoneInfo

from scheduling_agent.models import MeetingRequest, SchedulingAction, TimeSlot
from scheduling_agent.scheduler import Scheduler


class FakeCalendar:
    def __init__(self, busy: list[TimeSlot] | None = None):
        self.busy = busy or []

    def is_available(self, slot: TimeSlot) -> bool:
        return not any(slot.start < busy.end and busy.start < slot.end for busy in self.busy)


def test_scheduler_books_explicit_available_slot():

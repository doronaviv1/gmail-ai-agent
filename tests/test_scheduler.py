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
    scheduler = Scheduler(FakeCalendar(), ZoneInfo("UTC"), time(9), time(17), 30)
    request = MeetingRequest(True, "Demo", requested_day="2026-07-06", start_time="10:00", duration_minutes=30)

    decision = scheduler.decide(request)

    assert decision.action == SchedulingAction.BOOK
    assert decision.slot is not None
    assert decision.slot.start.hour == 10


def test_scheduler_reports_conflict_for_busy_explicit_slot():
    busy = [TimeSlot(datetime(2026, 7, 6, 10, tzinfo=ZoneInfo("UTC")), datetime(2026, 7, 6, 11, tzinfo=ZoneInfo("UTC")))]

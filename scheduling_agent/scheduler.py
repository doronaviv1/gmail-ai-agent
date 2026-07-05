from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from .calendar_client import CalendarClient
from .models import MeetingRequest, SchedulingAction, SchedulingDecision, TimeSlot


@dataclass
class Scheduler:
    calendar: CalendarClient
    timezone: ZoneInfo
    workday_start: time
    workday_end: time
    default_duration_minutes: int

    def decide(self, request: MeetingRequest) -> SchedulingDecision:
        if not request.is_meeting_request:
            return SchedulingDecision(SchedulingAction.SKIP, request, message="Email is not a meeting request.")

        if not request.requested_day:
            return SchedulingDecision(SchedulingAction.SKIP, request, message="No requested day was found.")

        duration = request.duration_minutes or self.default_duration_minutes
        requested_date = date.fromisoformat(request.requested_day)

        if request.start_time:
            slot = self._slot_from_requested_time(requested_date, request.start_time, request.end_time, duration)
            if self.calendar.is_available(slot):
                return SchedulingDecision(SchedulingAction.BOOK, request, slot=slot, message="Requested slot is available.")
            return SchedulingDecision(SchedulingAction.CONFLICT, request, slot=slot, message="Requested slot is unavailable.")

        slot = self._find_available_slot(requested_date, duration)

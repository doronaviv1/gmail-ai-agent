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

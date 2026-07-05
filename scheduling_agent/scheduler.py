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

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class SchedulingAction(str, Enum):
    BOOK = "book"
    CONFLICT = "conflict"
    SKIP = "skip"


@dataclass(frozen=True)
class EmailMessage:
    id: str
    thread_id: str
    sender: str
    subject: str
    body: str


@dataclass(frozen=True)
class MeetingRequest:
    is_meeting_request: bool
    title: str
    requested_day: str | None = None
    start_time: str | None = None
    end_time: str | None = None
    duration_minutes: int | None = None
    timezone: str | None = None
    attendees: list[str] = field(default_factory=list)
    confidence: float = 0.0
    reason: str = ""


@dataclass(frozen=True)
class TimeSlot:
    start: datetime
    end: datetime


@dataclass(frozen=True)
class SchedulingDecision:
    action: SchedulingAction
    request: MeetingRequest

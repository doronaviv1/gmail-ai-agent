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

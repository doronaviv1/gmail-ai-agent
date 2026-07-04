from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .models import TimeSlot


@dataclass
class CalendarClient:
    service: Any
    calendar_id: str

    def busy_slots(self, start: datetime, end: datetime) -> list[TimeSlot]:
        response = (
            self.service.freebusy()
            .query(
                body={
                    "timeMin": start.isoformat(),

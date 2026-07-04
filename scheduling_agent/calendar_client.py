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
                    "timeMax": end.isoformat(),
                    "items": [{"id": self.calendar_id}],
                }
            )
            .execute()
        )
        busy = response.get("calendars", {}).get(self.calendar_id, {}).get("busy", [])
        return [
            TimeSlot(
                start=datetime.fromisoformat(item["start"].replace("Z", "+00:00")),
                end=datetime.fromisoformat(item["end"].replace("Z", "+00:00")),
            )
            for item in busy
        ]

    def is_available(self, slot: TimeSlot) -> bool:
        return len(self.busy_slots(slot.start, slot.end)) == 0

    def create_event(
        self,
        title: str,
        slot: TimeSlot,
        attendees: list[str],
        description: str,
    ) -> dict[str, Any]:

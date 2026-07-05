from __future__ import annotations

import json
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from dateutil import parser as date_parser
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

from .models import EmailMessage, MeetingRequest


class ParsedMeeting(BaseModel):
    is_meeting_request: bool = Field(description="True only when the email asks to schedule a meeting or call.")
    title: str = Field(default="Meeting")
    requested_day: str | None = Field(default=None, description="ISO date YYYY-MM-DD when available.")
    start_time: str | None = Field(default=None, description="HH:MM 24-hour local time when explicitly requested.")
    end_time: str | None = Field(default=None, description="HH:MM 24-hour local time when explicitly requested.")
    duration_minutes: int | None = Field(default=None)
    timezone: str | None = Field(default=None)
    attendees: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    reason: str = Field(default="")


class LLMMeetingParser:
    def __init__(self, api_key: str | None, model: str, timezone: ZoneInfo) -> None:
        self.model = model
        self.timezone = timezone
        self.client = OpenAI(api_key=api_key) if api_key else None

    def parse(self, email: EmailMessage, now: datetime | None = None) -> MeetingRequest:
        now = now or datetime.now(self.timezone)
        if self.client is None:
            return self._fallback_parse(email, now)

        prompt = (
            "Extract scheduling intent from this email. Return only JSON matching these keys: "
            "is_meeting_request, title, requested_day, start_time, end_time, duration_minutes, "
            "timezone, attendees, confidence, reason. Use null when unknown. "
            f"Today is {now.date().isoformat()} in timezone {self.timezone.key}.\n\n"
            f"Subject: {email.subject}\nFrom: {email.sender}\nBody:\n{email.body}"
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[

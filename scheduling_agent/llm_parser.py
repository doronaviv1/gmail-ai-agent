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
                {"role": "system", "content": "You are a precise scheduling-intent extraction engine."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content or "{}"
        try:
            parsed = ParsedMeeting.model_validate(json.loads(content))
        except (json.JSONDecodeError, ValidationError):
            return self._fallback_parse(email, now)
        return MeetingRequest(**parsed.model_dump())

    def _fallback_parse(self, email: EmailMessage, now: datetime) -> MeetingRequest:
        text = f"{email.subject}\n{email.body}".lower()
        meeting_words = ("meeting", "meet", "call", "sync", "schedule", "appointment", "chat")
        if not any(word in text for word in meeting_words):
            return MeetingRequest(False, "Meeting", confidence=0.1, reason="No meeting intent keywords found.")

        requested_day = self._extract_day(text, now)
        start_time, end_time = self._extract_times(text)
        duration = self._extract_duration(text)
        title = email.subject.strip() or "Meeting"
        attendees = [email.sender] if email.sender else []
        confidence = 0.7 if requested_day else 0.45
        return MeetingRequest(
            is_meeting_request=True,
            title=title,
            requested_day=requested_day,
            start_time=start_time,
            end_time=end_time,
            duration_minutes=duration,
            timezone=self.timezone.key,
            attendees=attendees,
            confidence=confidence,
            reason="Fallback parser detected scheduling language.",
        )

    def _extract_day(self, text: str, now: datetime) -> str | None:
        if "tomorrow" in text:
            return (now + timedelta(days=1)).date().isoformat()
        if "today" in text:
            return now.date().isoformat()
        weekday_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for index, name in enumerate(weekday_names):
            if name in text:
                days_ahead = (index - now.weekday()) % 7
                days_ahead = 7 if days_ahead == 0 else days_ahead
                return (now + timedelta(days=days_ahead)).date().isoformat()
        match = re.search(r"\b\d{4}-\d{2}-\d{2}\b", text)
        if match:
            return match.group(0)
        try:
            parsed = date_parser.parse(text, fuzzy=True, default=now)
            return parsed.date().isoformat()
        except (ValueError, OverflowError):
            return None

    def _extract_times(self, text: str) -> tuple[str | None, str | None]:
        match = re.search(r"\b([01]?\d|2[0-3])(?::([0-5]\d))?\s*(am|pm)?\b", text)
        if not match:
            return None, None
        hour = int(match.group(1))

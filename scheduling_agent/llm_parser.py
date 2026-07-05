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

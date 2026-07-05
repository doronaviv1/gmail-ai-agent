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

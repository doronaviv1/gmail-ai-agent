from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import time
from zoneinfo import ZoneInfo

from dotenv import load_dotenv


def _parse_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _parse_time(value: str, name: str) -> time:
    try:
        hour, minute = value.split(":", 1)
        return time(hour=int(hour), minute=int(minute))
    except ValueError as exc:
        raise ValueError(f"{name} must use HH:MM format") from exc


@dataclass(frozen=True)
class Config:
    openai_api_key: str | None
    openai_model: str
    google_credentials_file: str
    google_token_file: str
    google_calendar_id: str
    gmail_query: str
    processed_label: str
    workday_start: time
    workday_end: time
    default_meeting_duration_minutes: int
    timezone: ZoneInfo
    poll_interval_seconds: int
    dry_run: bool
    send_confirmation_email: bool

    @classmethod
    def from_env(cls) -> "Config":
        load_dotenv()
        timezone_name = os.getenv("TIMEZONE", "UTC")
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY") or None,
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),

from __future__ import annotations

import argparse
import json
import logging
from dataclasses import asdict

from .agent import SchedulingAgent
from .auth import GoogleAuthenticator
from .calendar_client import CalendarClient
from .config import Config
from .gmail_client import GmailClient
from .llm_parser import LLMMeetingParser
from .scheduler import Scheduler


def build_agent(config: Config) -> SchedulingAgent:
    auth = GoogleAuthenticator(config.google_credentials_file, config.google_token_file)
    gmail = GmailClient(auth.gmail_service(), config.processed_label)
    calendar = CalendarClient(auth.calendar_service(), config.google_calendar_id)
    parser = LLMMeetingParser(config.openai_api_key, config.openai_model, config.timezone)
    scheduler = Scheduler(
        calendar=calendar,
        timezone=config.timezone,
        workday_start=config.workday_start,
        workday_end=config.workday_end,
        default_duration_minutes=config.default_meeting_duration_minutes,
    )
    return SchedulingAgent(config=config, gmail=gmail, parser=parser, scheduler=scheduler)


def main() -> None:
    parser = argparse.ArgumentParser(description="Gmail AI scheduling agent")
    parser.add_argument("command", choices=["run-once", "watch", "config"])
    parser.add_argument("--max-results", type=int, default=10)
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level.upper()), format="%(asctime)s %(levelname)s %(message)s")
    config = Config.from_env()

    if args.command == "config":
        data = asdict(config)

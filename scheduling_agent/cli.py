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

from __future__ import annotations

import logging
import time
from dataclasses import dataclass

from .config import Config
from .gmail_client import GmailClient
from .llm_parser import LLMMeetingParser
from .models import EmailMessage, SchedulingAction, SchedulingDecision
from .scheduler import Scheduler

logger = logging.getLogger(__name__)


@dataclass
class SchedulingAgent:
    config: Config
    gmail: GmailClient
    parser: LLMMeetingParser
    scheduler: Scheduler

    def run_once(self, max_results: int = 10) -> list[SchedulingDecision]:
        label_id = self.gmail.ensure_processed_label()
        decisions: list[SchedulingDecision] = []
        for message_id in self.gmail.search_messages(self.config.gmail_query, max_results=max_results):
            try:
                email = self.gmail.get_message(message_id)

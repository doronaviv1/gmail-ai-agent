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
                decision = self._handle_email(email)
                decisions.append(decision)
                if not self.config.dry_run:
                    self.gmail.mark_processed(message_id, label_id)
            except Exception:
                logger.exception("Failed to process Gmail message %s", message_id)
        return decisions

    def watch(self) -> None:
        while True:
            self.run_once()
            time.sleep(self.config.poll_interval_seconds)

    def _handle_email(self, email: EmailMessage) -> SchedulingDecision:
        request = self.parser.parse(email)
        decision = self.scheduler.decide(request)
        logger.info("Decision for %s: %s - %s", email.id, decision.action.value, decision.message)

        if decision.action == SchedulingAction.BOOK and decision.slot:
            if self.config.dry_run:
                logger.info("Dry run: would create calendar event for %s", decision.slot)
            else:
                self.scheduler.calendar.create_event(
                    title=request.title,
                    slot=decision.slot,

from __future__ import annotations

from dataclasses import dataclass

from .models import EmailMessage, SchedulingDecision
from .llm_parser import LLMMeetingParser
from .scheduler import Scheduler


@dataclass
class SchedulingSkill:
    """Reusable AI skill that maps an email into a scheduling decision."""

    parser: LLMMeetingParser
    scheduler: Scheduler

    def run(self, email: EmailMessage) -> SchedulingDecision:
        request = self.parser.parse(email)
        return self.scheduler.decide(request)

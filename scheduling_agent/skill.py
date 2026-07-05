from __future__ import annotations

from dataclasses import dataclass

from .models import EmailMessage, SchedulingDecision
from .llm_parser import LLMMeetingParser
from .scheduler import Scheduler

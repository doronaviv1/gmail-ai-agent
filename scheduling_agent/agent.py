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

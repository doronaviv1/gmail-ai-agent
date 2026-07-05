from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class SchedulingAction(str, Enum):
    BOOK = "book"
    CONFLICT = "conflict"
    SKIP = "skip"


@dataclass(frozen=True)
class EmailMessage:

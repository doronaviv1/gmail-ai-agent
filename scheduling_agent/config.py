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



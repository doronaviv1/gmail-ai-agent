from __future__ import annotations

import base64
import email.utils
from dataclasses import dataclass
from email.message import EmailMessage as OutboundEmail
from typing import Any

from .models import EmailMessage


def _decode_body(data: str | None) -> str:
    if not data:
        return ""
    padded = data + "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(padded.encode("utf-8")).decode("utf-8", errors="replace")



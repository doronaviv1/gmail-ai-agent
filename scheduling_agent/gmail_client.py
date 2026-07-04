from __future__ import annotations

import base64
import email.utils
from dataclasses import dataclass
from email.message import EmailMessage as OutboundEmail
from typing import Any

from .models import EmailMessage


def _decode_body(data: str | None) -> str:

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


def _headers_by_name(headers: list[dict[str, str]]) -> dict[str, str]:
    return {header["name"].lower(): header.get("value", "") for header in headers}


def _extract_text(payload: dict[str, Any]) -> str:
    mime_type = payload.get("mimeType")
    body = payload.get("body", {})
    if mime_type == "text/plain":
        return _decode_body(body.get("data"))

    parts = payload.get("parts", [])
    for part in parts:
        if part.get("mimeType") == "text/plain":
            return _extract_text(part)

    for part in parts:
        nested = _extract_text(part)
        if nested:
            return nested
    return _decode_body(body.get("data"))


@dataclass
class GmailClient:
    service: Any
    processed_label_name: str

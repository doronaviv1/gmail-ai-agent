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

    def ensure_processed_label(self) -> str:
        labels = self.service.users().labels().list(userId="me").execute().get("labels", [])
        for label in labels:
            if label.get("name") == self.processed_label_name:
                return label["id"]

        created = (
            self.service.users()
            .labels()
            .create(
                userId="me",
                body={
                    "name": self.processed_label_name,
                    "labelListVisibility": "labelShow",
                    "messageListVisibility": "show",
                },
            )
            .execute()
        )
        return created["id"]

    def search_messages(self, query: str, max_results: int = 10) -> list[str]:
        response = (
            self.service.users()
            .messages()
            .list(userId="me", q=f"{query} -label:{self.processed_label_name}", maxResults=max_results)
            .execute()
        )
        return [message["id"] for message in response.get("messages", [])]

    def get_message(self, message_id: str) -> EmailMessage:
        raw = (
            self.service.users()
            .messages()
            .get(userId="me", id=message_id, format="full")
            .execute()

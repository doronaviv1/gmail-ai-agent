from __future__ import annotations

from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar",
]


class GoogleAuthenticator:
    def __init__(self, credentials_file: str, token_file: str) -> None:
        self.credentials_file = Path(credentials_file)
        self.token_file = Path(token_file)

    def credentials(self) -> Credentials:
        creds = None
        if self.token_file.exists():
            creds = Credentials.from_authorized_user_file(str(self.token_file), SCOPES)

        if creds and creds.valid:
            return creds

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not self.credentials_file.exists():
                raise FileNotFoundError(
                    f"Missing {self.credentials_file}. Download an OAuth Desktop client JSON from Google Cloud."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(self.credentials_file), SCOPES)
            creds = flow.run_local_server(port=0)

        self.token_file.write_text(creds.to_json(), encoding="utf-8")
        return creds


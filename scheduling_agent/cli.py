from __future__ import annotations

import argparse
import json
import logging
from dataclasses import asdict

from .agent import SchedulingAgent
from .auth import GoogleAuthenticator
from .calendar_client import CalendarClient
from .config import Config

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from dateutil import parser as date_parser
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

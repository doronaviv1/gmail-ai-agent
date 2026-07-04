# Gmail AI Scheduling Agent

A Python agent that monitors Gmail for meeting requests, uses an LLM to turn email text into structured scheduling intent, checks Google Calendar availability, and either books the meeting or replies with a conflict message.

![Agent dashboard screenshot](screenshots/demo1.png)
![Scheduling flow screenshot](screenshots/demo2.png)

## What It Does

The agent is designed for a single Google Workspace user. It polls Gmail for unread messages, identifies likely meeting requests, parses requested dates, times, durations, attendee details, and intent, then checks the user's primary Google Calendar. If a requested slot is available, it creates a calendar event and optionally replies to the sender. If the requested slot is busy, it replies with a concise conflict message. When an email asks for a day but not a specific time, the agent searches working hours for the first available slot.

## Architecture

The codebase is split into small modules:

- `scheduling_agent.auth`: OAuth authentication for Gmail and Calendar.
- `scheduling_agent.gmail_client`: Gmail search, message parsing, and replies.
- `scheduling_agent.calendar_client`: Free/busy lookup and event creation.
- `scheduling_agent.llm_parser`: LLM-backed parsing with a deterministic fallback.
- `scheduling_agent.scheduler`: Availability decisions and slot selection.
- `scheduling_agent.skill`: Reusable AI skill wrapper for parse-and-schedule decisions.
- `scheduling_agent.agent`: Main orchestration loop.
- `scheduling_agent.cli`: Command-line entry point.

The agent intentionally keeps Google credentials and user tokens outside Git. Use `.env` for local configuration and keep `credentials.json` and `token.json` on your workstation only.

## Repository Layout

```text
.
├── PRD.md
├── Plan.md
├── TODO.md
├── README.md
├── requirements.txt

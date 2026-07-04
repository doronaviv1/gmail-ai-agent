# Gmail AI Scheduling Agent

A Python agent that monitors Gmail for meeting requests, uses an LLM to turn email text into structured scheduling intent, checks Google Calendar availability, and either books the meeting or replies with a conflict message.

![Agent dashboard screenshot](screenshots/demo1.png)
![Scheduling flow screenshot](screenshots/demo2.png)

## What It Does

The agent is designed for a single Google Workspace user. It polls Gmail for unread messages, identifies likely meeting requests, parses requested dates, times, durations, attendee details, and intent, then checks the user's primary Google Calendar. If a requested slot is available, it creates a calendar event and optionally replies to the sender. If the requested slot is busy, it replies with a concise conflict message. When an email asks for a day but not a specific time, the agent searches working hours for the first available slot.

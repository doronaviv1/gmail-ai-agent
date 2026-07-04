# Product Requirements Document

## Product

Gmail AI Scheduling Agent

## Goal

Automate first-pass meeting scheduling from Gmail by parsing natural language requests, checking Google Calendar availability, and taking the correct scheduling action without manual triage.

## Users

- Primary user: an individual Google Workspace user who receives meeting requests by email.
- Secondary user: administrators or developers configuring the agent.

## Core Requirements

1. Monitor Gmail for incoming candidate meeting requests.
2. Parse free-text email content into structured scheduling intent.
3. Detect explicit requested time windows.
4. If no time is supplied, find an available time during configured working hours.
5. Check Google Calendar availability before booking.
6. Create a calendar event when a slot is available.
7. Reply to the sender when a requested slot is unavailable.
8. Avoid duplicate processing of the same email.
9. Keep credentials and tokens out of Git.

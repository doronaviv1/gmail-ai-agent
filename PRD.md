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

## Non-Goals

- Multi-user admin console.
- Full bidirectional negotiation across many participants.
- Native push notification setup. Polling is sufficient for the first version.
- PDF exports.

## Functional Acceptance Criteria

- The agent can run a single pass from the CLI.
- The agent can run continuously with a configurable polling interval.
- The parser returns a typed scheduling request object.
- The scheduler can choose a free slot when only a day is requested.
- The calendar client can call free/busy and event creation APIs.
- The Gmail client can fetch message content and send thread replies.
- Dry-run mode avoids external mutations.

## Security Acceptance Criteria

- `.gitignore` excludes `.env`, `credentials.json`, `token.json`, Python caches, local databases, logs, and virtual environments.
- `.env.example` contains placeholders only.
- Tests do not require real credentials.
- No repository file contains OAuth tokens or client secrets.


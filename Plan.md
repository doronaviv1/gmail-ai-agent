# System Architecture and Development Plan

## Architecture

```text
Gmail polling
  -> message extraction
  -> meeting intent parsing
  -> calendar availability lookup
  -> event creation or reply
  -> message labeling
```

## Components

- `Config`: Loads environment variables with safe defaults.
- `GoogleAuthenticator`: Handles OAuth token creation and refresh.
- `GmailClient`: Searches unread messages, extracts sender/body/subject, sends replies, and labels processed threads.
- `CalendarClient`: Queries free/busy and inserts events.
- `LLMMeetingParser`: Uses OpenAI structured output when configured, with a deterministic fallback parser.
- `Scheduler`: Resolves requested times, searches working hours, and returns a scheduling decision.
- `SchedulingAgent`: Orchestrates one pass or a long-running loop.

## Data Flow

1. CLI loads configuration.
2. OAuth services are created for Gmail and Calendar.
3. Gmail is searched for candidate unread messages.
4. Each message is converted into plain text.
5. Parser extracts meeting intent.
6. Scheduler checks Calendar.
7. Agent creates an event or sends a conflict response.
8. Gmail message is labeled as processed.

## Development Plan

1. Scaffold secure repository structure.
2. Implement typed domain models.
3. Implement config loading.
4. Implement Google OAuth helper.
5. Implement Gmail adapter.
6. Implement Calendar adapter.
7. Implement LLM parser and deterministic fallback.
8. Implement scheduler.
9. Implement orchestration and CLI.
10. Add tests with fakes.
11. Add documentation and screenshots.

## Deployment Plan

Run as a local process, cron job, systemd service, container, or server task. For production, prefer a service account only if the Workspace domain supports domain-wide delegation; otherwise use OAuth Desktop credentials for a single user.

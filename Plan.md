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

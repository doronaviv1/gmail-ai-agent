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

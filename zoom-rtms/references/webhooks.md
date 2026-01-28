# RTMS - Webhooks

RTMS-related webhook events.

## Overview

RTMS uses webhooks to notify your server when streams are available.

## Events

### meeting.rtms_started

Sent when RTMS stream is ready for a meeting.

```json
{
  "event": "meeting.rtms_started",
  "payload": {
    "account_id": "account_id",
    "object": {
      "meeting_id": "meeting_id",
      "meeting_uuid": "meeting_uuid",
      "host_id": "host_user_id",
      "rtms_stream_id": "stream_id",
      "server_urls": "wss://rtms.zoom.us/...",
      "signature": "auth_signature"
    }
  }
}
```

### meeting.rtms_stopped

Sent when RTMS stream ends.

```json
{
  "event": "meeting.rtms_stopped",
  "payload": {
    "account_id": "account_id",
    "object": {
      "meeting_id": "meeting_id",
      "rtms_stream_id": "stream_id"
    }
  }
}
```

## Payload Fields

| Field | Description |
|-------|-------------|
| `rtms_stream_id` | Unique stream identifier |
| `server_urls` | WebSocket endpoint URL |
| `signature` | Authentication signature for connection |

## Subscribing to RTMS Events

1. Go to app settings in Marketplace
2. Add event subscription
3. Select RTMS events
4. Configure endpoint URL

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/

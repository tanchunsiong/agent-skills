# Zoom RTMS - Complete Documentation Index

RTMS provides real-time access to live audio, video, transcript, chat, and screen share from Zoom meetings, webinars, and Video SDK sessions.

## Quick Start Path

**If you're new to RTMS, follow this order:**

1. **Understand the architecture** -> [concepts/connection-architecture.md](concepts/connection-architecture.md)
   - Two-phase WebSocket: Signaling + Media
   - Why RTMS doesn't use bots

2. **Choose your approach** -> SDK or Manual
   - SDK (recommended): [examples/sdk-quickstart.md](examples/sdk-quickstart.md)
   - Manual WebSocket: [examples/manual-websocket.md](examples/manual-websocket.md)

3. **Understand the lifecycle** -> [concepts/lifecycle-flow.md](concepts/lifecycle-flow.md)
   - Webhook -> Signaling -> Media -> Streaming

4. **Configure media types** -> [references/media-types.md](references/media-types.md)
   - Audio, video, transcript, chat, screen share

5. **Troubleshoot issues** -> [troubleshooting/common-issues.md](troubleshooting/common-issues.md)
   - Connection problems, duplicate webhooks, missing data

---

## Documentation Structure

```
zoom-rtms/
├── SKILL.md                           # Main skill overview
├── INDEX.md                           # This file - navigation guide
│
├── concepts/                          # Core architectural patterns
│   ├── connection-architecture.md     # Two-phase WebSocket design
│   └── lifecycle-flow.md              # Webhook to streaming flow
│
├── examples/                          # Complete working code
│   ├── sdk-quickstart.md              # Using @zoom/rtms SDK
│   ├── manual-websocket.md            # Raw protocol implementation
│   ├── rtms-bot.md                    # Complete RTMS bot implementation
│   └── ai-integration.md              # Transcription and analysis
│
├── references/                        # Reference documentation
│   ├── media-types.md                 # Audio, video, transcript, chat, share
│   ├── data-types.md                  # All enums and constants
│   ├── connection.md                  # WebSocket protocol details
│   └── webhooks.md                    # Event subscription
│
└── troubleshooting/                   # Problem solving guides
    └── common-issues.md               # FAQ and solutions
```

---

## By Use Case

### I want to get meeting transcripts
1. [SDK Quickstart](examples/sdk-quickstart.md) - Fastest approach
2. [Media Types](references/media-types.md#transcript) - Transcript configuration
3. [AI Integration](examples/ai-integration.md) - Whisper, Deepgram, AssemblyAI

### I want to record meetings
1. [Media Types](references/media-types.md) - Audio + Video configuration
2. [SDK Quickstart](examples/sdk-quickstart.md) - Receiving media
3. [AI Integration](examples/ai-integration.md#audio-recording) - Gap-filled recording

### I want to build an AI meeting assistant
1. [AI Integration](examples/ai-integration.md) - Complete patterns
2. [SDK Quickstart](examples/sdk-quickstart.md) - Media ingestion
3. [Lifecycle Flow](concepts/lifecycle-flow.md) - Event handling

### I want to build a complete RTMS bot
1. [RTMS Bot](examples/rtms-bot.md) - **Complete implementation guide**
2. [Lifecycle Flow](concepts/lifecycle-flow.md) - Webhook to streaming flow
3. [Connection Architecture](concepts/connection-architecture.md) - Two-phase design

### I need full protocol control
1. [Manual WebSocket](examples/manual-websocket.md) - **START HERE**
2. [Connection Architecture](concepts/connection-architecture.md) - Two-phase design
3. [Data Types](references/data-types.md) - All message types and enums
4. [Connection](references/connection.md) - Protocol details

### I'm getting connection errors
1. [Common Issues](troubleshooting/common-issues.md) - Diagnostic checklist
2. [Connection Architecture](concepts/connection-architecture.md) - Verify flow
3. [Webhooks](references/webhooks.md) - Validation and timing

### I want to understand the architecture
1. [Connection Architecture](concepts/connection-architecture.md) - Two-phase WebSocket
2. [Lifecycle Flow](concepts/lifecycle-flow.md) - Complete flow diagram
3. [Data Types](references/data-types.md) - Protocol constants

---

## By Product

### I'm building for Zoom Meetings
- Standard RTMS setup. Webhook event: `meeting.rtms_started`. Uses General App with OAuth.
- Start with [SDK Quickstart](examples/sdk-quickstart.md) or [Manual WebSocket](examples/manual-websocket.md).

### I'm building for Zoom Webinars
- Same as meetings, but webhook event is `webinar.rtms_started`. Payload still uses `meeting_uuid` (NOT `webinar_uuid`).
- Add webinar scopes and event subscriptions. See [Webhooks](references/webhooks.md).
- Only **panelist** streams are confirmed available. Attendee streams may not be individual.

### I'm building for Zoom Video SDK
- Webhook event: `session.rtms_started`. Payload uses `session_id` (NOT `meeting_uuid`).
- Requires a **Video SDK App** with SDK Key/Secret (not OAuth Client ID/Secret).
- Once connected, the protocol is **identical** to meetings.
- See [Webhooks](references/webhooks.md) for payload details.

---

## Key Documents

### 1. Connection Architecture (CRITICAL)
**[concepts/connection-architecture.md](concepts/connection-architecture.md)**

RTMS uses **two separate WebSocket connections**:
- **Signaling WebSocket**: Authentication, control, heartbeats
- **Media WebSocket**: Actual audio/video/transcript data

### 2. SDK vs Manual (DECISION POINT)
**[examples/sdk-quickstart.md](examples/sdk-quickstart.md)** vs **[examples/manual-websocket.md](examples/manual-websocket.md)**

| SDK | Manual |
|-----|--------|
| Handles WebSocket complexity | Full protocol control |
| Automatic reconnection | DIY reconnection |
| Less code | More code |
| Best for most use cases | Best for custom requirements |

### 3. Critical Gotchas (MOST COMMON ISSUES)
**[troubleshooting/common-issues.md](troubleshooting/common-issues.md)**

1. **Respond 200 immediately** - Delayed webhook responses cause duplicates
2. **Only 1 connection per stream** - New connections kick out existing
3. **Heartbeat required** - Must respond to keep-alive or connection dies
4. **Track active sessions** - Prevent duplicate join attempts

---

## Key Learnings

### Critical Discoveries:

1. **Two-Phase WebSocket Design**
   - Signaling: Control plane (handshake, heartbeat, start/stop)
   - Media: Data plane (audio, video, transcript, chat, share)
   - See: [Connection Architecture](concepts/connection-architecture.md)

2. **Webhook Response Timing**
   - MUST respond 200 BEFORE any processing
   - Delayed response -> Zoom retries -> duplicate connections
   - See: [Common Issues](troubleshooting/common-issues.md#webhook-response-timing)

3. **Heartbeat is Mandatory**
   - Signaling: Receive msg_type 12, respond with msg_type 13
   - Media: Same pattern
   - Failure to respond = connection closed
   - See: [Connection](references/connection.md#heartbeat)

4. **Signature Generation**
   - Format: `HMAC-SHA256(clientSecret, "clientId,meetingUuid,streamId")`
   - For Video SDK, use `session_id` in place of `meetingUuid`
   - Webinars still use `meeting_uuid` (not `webinar_uuid`)
   - Required for both signaling and media handshakes
   - See: [Manual WebSocket](examples/manual-websocket.md#signature-generation)

5. **Media Types are Bitmasks**
   - Audio=1, Video=2, Share=4, Transcript=8, Chat=16, All=32
   - Combine with OR: Audio+Transcript = 1|8 = 9
   - See: [Media Types](references/media-types.md)

6. **Screen Share is SEPARATE from Video**
   - Different msg_type (16 vs 15)
   - Different media flag (4 vs 2)
   - Must subscribe separately
   - See: [Media Types](references/media-types.md#screen-share)

---

## Quick Reference

### "Connection fails"
-> [Common Issues](troubleshooting/common-issues.md)

### "Duplicate connections"
-> [Webhook timing](troubleshooting/common-issues.md#webhook-response-timing)

### "No audio/video data"
-> [Media Types](references/media-types.md) - Check configuration

### "How do I implement manually?"
-> [Manual WebSocket](examples/manual-websocket.md)

### "What message types exist?"
-> [Data Types](references/data-types.md)

### "How do I integrate AI?"
-> [AI Integration](examples/ai-integration.md)

---

## Document Version

Based on **Zoom RTMS SDK v1.x** and official documentation as of 2026.

---

**Happy coding!**

Remember: Start with [SDK Quickstart](examples/sdk-quickstart.md) for the fastest path, or [Manual WebSocket](examples/manual-websocket.md) if you need full control.

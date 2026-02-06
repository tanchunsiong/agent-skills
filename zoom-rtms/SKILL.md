---
name: zoom-rtms
description: |
  Zoom Realtime Media Streams (RTMS) for accessing live audio, video, transcript, chat, and 
  screen share from Zoom meetings. WebSocket-based protocol using open web standards. Use when 
  building AI/ML applications, live transcription, recording, streaming, or real-time meeting analysis.
---

# Zoom Realtime Media Streams (RTMS)

Expert guidance for accessing live audio, video, transcript, chat, and screen share data from Zoom meetings in real-time. RTMS uses WebSocket-based protocol with open standards - no meeting bots required.

**Official Documentation**: https://developers.zoom.us/docs/rtms/
**SDK Reference (JS)**: https://zoom.github.io/rtms/js/
**SDK Reference (Python)**: https://zoom.github.io/rtms/py/
**Sample Repository**: https://github.com/zoom/rtms-samples

## Quick Links

**New to RTMS? Follow this path:**

1. **[Connection Architecture](concepts/connection-architecture.md)** - Two-phase WebSocket design
2. **[SDK Quickstart](examples/sdk-quickstart.md)** - Fastest way to receive media (recommended)
3. **[Manual WebSocket](examples/manual-websocket.md)** - Full protocol control without SDK
4. **[Media Types](references/media-types.md)** - Audio, video, transcript, chat, screen share

**Reference:**
- **[Lifecycle Flow](concepts/lifecycle-flow.md)** - Complete webhook-to-streaming flow
- **[Data Types](references/data-types.md)** - All enums and constants
- **[Webhooks](references/webhooks.md)** - Event subscription details
- **[INDEX.md](INDEX.md)** - Complete documentation navigation

**Having issues?**
- Connection fails -> [Common Issues](troubleshooting/common-issues.md)
- Duplicate connections -> [Webhook Gotchas](troubleshooting/common-issues.md#webhook-response-timing)
- No audio/video -> [Media Configuration](references/media-types.md)

## RTMS Overview

RTMS is a data pipeline that gives your app access to live media from Zoom meetings **without participant bots**. Instead of having automated clients join meetings, use RTMS to collect media data directly from Zoom's infrastructure.

### What RTMS Provides

| Media Type | Format | Use Cases |
|------------|--------|-----------|
| **Audio** | PCM (L16), G.711, G.722, Opus | Transcription, voice analysis, recording |
| **Video** | H.264, JPG, PNG | Recording, AI vision, thumbnails |
| **Screen Share** | H.264, JPG, PNG | Content capture, slide extraction |
| **Transcript** | JSON text | Meeting notes, search, compliance |
| **Chat** | JSON text | Archive, sentiment analysis |

### Two Approaches

| Approach | Best For | Complexity |
|----------|----------|------------|
| **SDK** (`@zoom/rtms`) | Most use cases | Low - handles WebSocket complexity |
| **Manual WebSocket** | Custom protocols, other languages | High - full protocol implementation |

## Prerequisites

- **Node.js 20.3.0+** (24 LTS recommended) for JavaScript SDK
- **Python 3.10+** for Python SDK
- Zoom General App with RTMS feature enabled
- Webhook endpoint for RTMS events
- Server to receive WebSocket streams

> **Need RTMS access?** Post in [Zoom Developer Forum](https://devforum.zoom.us/) requesting RTMS access with your use case.

## Quick Start (SDK - Recommended)

```javascript
import rtms from "@zoom/rtms";

// Handle webhook events
rtms.onWebhookEvent(({ event, payload }) => {
  if (event !== "meeting.rtms_started") return;

  const client = new rtms.Client();

  client.onAudioData((data, timestamp, metadata) => {
    console.log(`Audio from ${metadata.userName}: ${data.length} bytes`);
  });

  client.onTranscriptData((data, timestamp, metadata) => {
    const text = data.toString('utf8');
    console.log(`${metadata.userName}: ${text}`);
  });

  client.onJoinConfirm((reason) => {
    console.log(`Joined meeting: ${reason}`);
  });

  // SDK handles all WebSocket connections automatically
  client.join(payload);
});
```

## Quick Start (Manual WebSocket)

For full control or non-SDK languages, implement the two-phase WebSocket protocol:

```javascript
const WebSocket = require('ws');
const crypto = require('crypto');

// 1. Generate signature
function generateSignature(clientId, meetingUuid, streamId, clientSecret) {
  const message = `${clientId},${meetingUuid},${streamId}`;
  return crypto.createHmac('sha256', clientSecret).update(message).digest('hex');
}

// 2. Handle webhook
app.post('/webhook', (req, res) => {
  res.status(200).send();  // CRITICAL: Respond immediately!
  
  const { event, payload } = req.body;
  if (event === 'meeting.rtms_started') {
    connectToRTMS(payload);
  }
});

// 3. Connect to signaling WebSocket
function connectToRTMS(payload) {
  const { server_urls, rtms_stream_id, meeting_uuid } = payload;
  const signature = generateSignature(CLIENT_ID, meeting_uuid, rtms_stream_id, CLIENT_SECRET);
  
  const signalingWs = new WebSocket(server_urls);
  
  signalingWs.on('open', () => {
    signalingWs.send(JSON.stringify({
      msg_type: 1,  // Handshake request
      protocol_version: 1,
      meeting_uuid,
      rtms_stream_id,
      signature,
      media_type: 9  // AUDIO(1) | TRANSCRIPT(8)
    }));
  });
  
  // ... handle responses, connect to media WebSocket
}
```

**See**: [Manual WebSocket Guide](examples/manual-websocket.md) for complete implementation.

## Media Type Bitmask

Combine types with bitwise OR:

| Type | Value | Description |
|------|-------|-------------|
| Audio | 1 | PCM audio samples |
| Video | 2 | H.264/JPG video frames |
| Screen Share | 4 | **Separate from video!** |
| Transcript | 8 | Real-time speech-to-text |
| Chat | 16 | In-meeting chat messages |
| All | 32 | All media types |

**Example**: Audio + Transcript = `1 | 8` = `9`

## Critical Gotchas

| Issue | Solution |
|-------|----------|
| **Only 1 connection allowed** | New connections kick out existing ones. Track active sessions! |
| **Respond 200 immediately** | If webhook delays, Zoom retries creating duplicate connections |
| **Heartbeat mandatory** | Respond to msg_type 12 with msg_type 13, or connection dies |
| **Reconnection is YOUR job** | RTMS doesn't auto-reconnect. Media: 30s, Signaling: 60s timeout |
| **Transcript language delay** | Auto-detect takes 30s. Set language explicitly to skip delay |

## Environment Variables

### SDK Environment Variables

```bash
# Required - Authentication
ZM_RTMS_CLIENT=your_client_id          # Zoom OAuth Client ID
ZM_RTMS_SECRET=your_client_secret      # Zoom OAuth Client Secret

# Optional - Webhook server
ZM_RTMS_PORT=8080                      # Default: 8080
ZM_RTMS_PATH=/webhook                  # Default: /

# Optional - Logging
ZM_RTMS_LOG_LEVEL=info                 # error, warn, info, debug, trace
ZM_RTMS_LOG_FORMAT=progressive         # progressive or json
ZM_RTMS_LOG_ENABLED=true
```

### Manual Implementation Variables

```bash
ZOOM_CLIENT_ID=your_client_id
ZOOM_CLIENT_SECRET=your_client_secret
ZOOM_SECRET_TOKEN=your_webhook_token   # For webhook validation
```

## Zoom App Setup

1. Go to [marketplace.zoom.us](https://marketplace.zoom.us) -> Develop -> Build App
2. Choose **General App** -> **User-Managed**
3. Features -> Access -> **Enable Event Subscription**
4. Add Events -> Search "rtms" -> Select:
   - `meeting.rtms_started`
   - `meeting.rtms_stopped`
5. Scopes -> Add Scopes -> Search "rtms" -> Add:
   - `meeting:read:meeting_audio`
   - `meeting:read:meeting_video`
   - `meeting:read:meeting_transcript`
   - `meeting:read:meeting_chat`

## Sample Repositories

### Official Samples

| Repository | Description |
|------------|-------------|
| [rtms-samples](https://github.com/zoom/rtms-samples) | RTMSManager, boilerplates, AI samples |
| [rtms-quickstart-js](https://github.com/zoom/rtms-quickstart-js) | JavaScript SDK quickstart |
| [rtms-quickstart-py](https://github.com/zoom/rtms-quickstart-py) | Python SDK quickstart |
| [rtms-sdk-cpp](https://github.com/zoom/rtms-sdk-cpp) | C++ SDK |
| [rtms](https://github.com/zoom/rtms) | Main SDK repository |

### AI Integration Samples

| Sample | Description |
|--------|-------------|
| [rtms-meeting-assistant-starter-kit](https://github.com/zoom/rtms-meeting-assistant-starter-kit) | AI meeting assistant with summaries |
| [arlo-meeting-assistant](https://github.com/zoom/arlo-meeting-assistant) | Production meeting assistant with DB |
| [videosdk-rtms-transcribe-audio](https://github.com/zoom/videosdk-rtms-transcribe-audio) | Whisper transcription |

## Complete Documentation

### Concepts
- **[Connection Architecture](concepts/connection-architecture.md)** - Two-phase WebSocket design
- **[Lifecycle Flow](concepts/lifecycle-flow.md)** - Webhook to streaming flow

### Examples
- **[SDK Quickstart](examples/sdk-quickstart.md)** - Using @zoom/rtms SDK
- **[Manual WebSocket](examples/manual-websocket.md)** - Raw protocol implementation
- **[AI Integration](examples/ai-integration.md)** - Transcription and analysis patterns

### References
- **[Media Types](references/media-types.md)** - Audio, video, transcript, chat, screen share
- **[Data Types](references/data-types.md)** - All enums and constants
- **[Connection](references/connection.md)** - WebSocket protocol details
- **[Webhooks](references/webhooks.md)** - Event subscription

### Troubleshooting
- **[Common Issues](troubleshooting/common-issues.md)** - FAQ and solutions

## Resources

- **Official docs**: https://developers.zoom.us/docs/rtms/
- **Data types**: https://developers.zoom.us/docs/rtms/data-types/
- **Media params**: https://developers.zoom.us/docs/rtms/media-parameter-definition/
- **Developer forum**: https://devforum.zoom.us/

---

**Need help?** Start with [INDEX.md](INDEX.md) for complete navigation.

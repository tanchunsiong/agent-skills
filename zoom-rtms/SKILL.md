---
name: zoom-rtms
description: |
  Zoom Realtime Media Streams (RTMS) for accessing live audio, video, transcript, chat, and 
  screen share from Zoom meetings. WebSocket-based protocol using open web standards. Use when 
  building AI/ML applications, live transcription, recording, streaming, or real-time meeting analysis.
---

# Zoom Realtime Media Streams (RTMS)

Access live audio, video, transcript, chat, and screen share data from Zoom meetings in real-time.

## Prerequisites

- **Node.js 20.3.0+** (24 LTS recommended) if using `@zoom/rtms` SDK
- Zoom General App with RTMS feature enabled
- Webhook endpoint for RTMS events
- Server to receive WebSocket streams

> **Need help with OAuth?** See the **[zoom-oauth](/zoom-oauth/SKILL.md)** skill for authentication flows.

## Quick Start (Recommended: RTMSManager)

```javascript
import { RTMSManager } from './library/javascript/rtmsManager/RTMSManager.js';
import express from 'express';
import crypto from 'crypto';

const app = express();
app.use(express.json());

// 1. Initialize
await RTMSManager.init({
  credentials: {
    meeting: {
      clientId: process.env.ZOOM_CLIENT_ID,
      clientSecret: process.env.ZOOM_CLIENT_SECRET,
      secretToken: process.env.ZOOM_SECRET_TOKEN,  // For webhook validation
    }
  },
  mediaTypes: RTMSManager.MEDIA.AUDIO | RTMSManager.MEDIA.TRANSCRIPT,  // Bitmask
  logging: 'info'
});

// 2. Handle media events
RTMSManager.on('audio', ({ buffer, userName, timestamp }) => {
  console.log(`Audio from ${userName}: ${buffer.length} bytes`);
});

RTMSManager.on('transcript', ({ text, userName }) => {
  console.log(`${userName}: ${text}`);
});

RTMSManager.on('chat', ({ text, userName }) => {
  console.log(`[Chat] ${userName}: ${text}`);
});

RTMSManager.on('sharescreen', ({ buffer, userName }) => {
  console.log(`Screen share from ${userName}`);
});

RTMSManager.on('error', (error) => {
  console.error(error.toString());
});

// 3. Webhook endpoint - RESPOND 200 IMMEDIATELY!
app.post('/webhook', (req, res) => {
  res.status(200).send();  // CRITICAL: Send 200 FIRST before any processing!
  
  const { event, payload } = req.body;
  
  // Handle URL validation challenge
  if (event === 'endpoint.url_validation') {
    const hash = crypto
      .createHmac('sha256', process.env.ZOOM_SECRET_TOKEN)
      .update(payload.plainToken)
      .digest('hex');
    return res.json({ plainToken: payload.plainToken, encryptedToken: hash });
  }
  
  // Feed RTMS events to manager (async)
  RTMSManager.handleEvent(event, payload);
});

await RTMSManager.start();
app.listen(3000);
```

## Media Types (Bitmask)

| Type | Value | Event | Description |
|------|-------|-------|-------------|
| Audio | 1 | `audio` | PCM audio samples |
| Video | 2 | `video` | H.264 video frames |
| Screen Share | 4 | `sharescreen` | Separate from video! |
| Transcript | 8 | `transcript` | Real-time speech-to-text |
| Chat | 16 | `chat` | In-meeting chat messages |
| All | 32 | all events | All media types |

**Example**: Audio + Transcript = `1 | 8` = `9`

## Critical Gotchas

| Issue | Solution |
|-------|----------|
| **Only 1 connection allowed** | New connections kick out existing ones. Only connect once per stream! |
| **Respond 200 immediately** | If webhook response is delayed, Zoom retries → causes duplicate connections → kicks out original |
| **Heartbeat mandatory** | Respond to msg_type 12 with msg_type 13, or connection dies |
| **Reconnection is YOUR job** | RTMS doesn't auto-reconnect. Media: 30s timeout, Signaling: 60s timeout |
| **Transcript language delay** | Auto-detect takes 30s. Set language explicitly to skip delay |

## Credentials

Get from [marketplace.zoom.us](https://marketplace.zoom.us):

| Credential | Location | Env Var |
|------------|----------|---------|
| Client ID | App Credentials | `ZOOM_CLIENT_ID` |
| Client Secret | App Credentials | `ZOOM_CLIENT_SECRET` |
| Secret Token | Feature → Webhook | `ZOOM_SECRET_TOKEN` |

**If using `@zoom/rtms` SDK**: The SDK requires these exact env var names (hardcoded):
```bash
ZM_RTMS_CLIENT=your_client_id
ZM_RTMS_SECRET=your_client_secret
```

## Zoom App Setup

1. Go to [marketplace.zoom.us](https://marketplace.zoom.us) → Develop → Build App
2. Choose **General App** → **User-Managed**
3. Features → Access → Enable Event Subscription
4. Add Events → Search "rtms" → Select RTMS endpoints
5. Scopes → Add Scopes → Search "rtms" → Add for both "Meetings" and "Rtms"
6. Required scopes: `meeting:read:meeting_audio`, `meeting:read:meeting_video`, etc.

## Audio Configuration

| Property | Options |
|----------|---------|
| Sample Rate | 8kHz (0), 16kHz (1), 32kHz (2), 48kHz (3) |
| Codec | L16/PCM (1), G.711 (2), G.722 (3), Opus (4) |
| Channels | Mono (1), Stereo (2) - **Stereo only with Opus!** |
| Data Option | Mixed (1), Multi-stream per participant (2) |

## Video Configuration

| Property | Options |
|----------|---------|
| Codec | H.264 (7), JPG (5), PNG (6) |
| Resolution | SD (1), HD 720p (2), FHD 1080p (3), QHD 2K (4) |
| FPS | 1-30 (use 1-5 for screen share, 25-30 for video) |
| Data Option | Single active (3), Speaker view (4), Gallery view (5) |

**Rule**: Use JPG/PNG when fps <= 5, H.264 when fps > 5

## Signaling Protocol

| msg_type | Name | Direction |
|----------|------|-----------|
| 1 | Handshake Request | Client → Server |
| 2 | Handshake Response | Server → Client |
| 3 | Media Handshake Request | Client → Server |
| 4 | Media Handshake Response | Server → Client |
| 7 | Ready to Receive | Client → Server |
| 12 | Keep Alive Request | Server → Client |
| 13 | Keep Alive Response | Client → Server |

| msg_type | Media Type |
|----------|------------|
| 14 | Audio |
| 15 | Video |
| 16 | Screen Share |
| 17 | Transcript |
| 18 | Chat |

## Signature Generation

```javascript
const message = `${clientId},${meetingUuid},${streamId}`;
const signature = crypto.createHmac('sha256', clientSecret).update(message).digest('hex');
```

## Scaling (Production)

- **Master-Worker Architecture**: Masters receive webhooks, Workers handle connections
- **Redis**: Store meeting→worker mapping, worker capacity, heartbeats
- **Message Queue**: Decouple webhook receipt from processing (RabbitMQ/SQS)
- **Golden Rule**: Separate I/O from processing. Workers do I/O only, heavy processing on separate nodes
- **Worker Sizing**: 50-100 meetings per 8-core node (I/O only)
- **Geo-Routing**: Server URLs contain airport codes (sjc, sin, iad). Route to nearest worker.

## Concurrency Limits

| Tier | Limit |
|------|-------|
| Trial | 5 concurrent RTMS connections |
| Production | Up to 2000 (more on request) |

## Detailed References

- **[references/quickstart.md](references/quickstart.md)** - Getting started guide
- **[references/webhooks.md](references/webhooks.md)** - Webhook events
- **[references/media-types.md](references/media-types.md)** - Audio, video, transcript, chat, screen share formats
- **[references/connection.md](references/connection.md)** - WebSocket protocol & message types

## Sample Repositories

### Official (by Zoom)

| Type | Repository | Description |
|------|------------|-------------|
| **Samples (BEST)** | [rtms-samples](https://github.com/zoom/rtms-samples) | RTMSManager, boilerplates, AI samples, streaming |
| SDK | [rtms](https://github.com/zoom/rtms) | Node/Python/Go SDK |
| C++ SDK | [rtms-sdk-cpp](https://github.com/zoom/rtms-sdk-cpp) | Native C++ implementation |

### Key Samples in rtms-samples

| Category | Sample | Description |
|----------|--------|-------------|
| AI | `ai_industry_specific_notetaker_js` | NER, action items, topics, summaries |
| AI | `ai_rag_customer_support_js` | RAG-based customer service |
| Transcription | `send_audio_to_deepgram_*` | Deepgram integration |
| Transcription | `send_audio_to_assemblyai_*` | AssemblyAI integration |
| Streaming | `stream_to_aws_ivs_*` | AWS IVS with gap filler/jitter buffer |
| Streaming | `stream_to_youtube_*` | YouTube Live |
| Storage | `save_audio_and_video_to_*` | AWS S3, Azure Blob, local |

### Boilerplate Templates

JavaScript, Python, Go, Java, C++, .NET - all available at `rtms-samples/boilerplate/`

## Gold Reference Documentation

| Document | Content |
|----------|---------|
| [PRODUCTION.md](https://github.com/zoom/rtms-samples/blob/main/PRODUCTION.md) | Horizontal scaling architecture (50KB!) |
| [RTMS_CONNECTION_FLOW.md](https://github.com/zoom/rtms-samples/blob/main/RTMS_CONNECTION_FLOW.md) | Protocol details with JS/Python/Go examples |
| [MEDIA_PARAMETERS.md](https://github.com/zoom/rtms-samples/blob/main/MEDIA_PARAMETERS.md) | Complete constant definitions |
| [TROUBLESHOOTING.md](https://github.com/zoom/rtms-samples/blob/main/TROUBLESHOOTING.md) | Common issues & fixes |
| [ARCHITECTURE.md](https://github.com/zoom/rtms-samples/blob/main/ARCHITECTURE.md) | Connection flow diagrams |

## Resources

- **Official docs**: https://developers.zoom.us/docs/rtms/
- **Data types**: https://developers.zoom.us/docs/rtms/data-types/
- **Media params**: https://developers.zoom.us/docs/rtms/media-parameter-definition/
- **Events**: https://developers.zoom.us/docs/rtms/event-reference/
- **Developer forum**: https://devforum.zoom.us/

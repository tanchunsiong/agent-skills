---
name: zoom-rtms
description: |
  Zoom Realtime Media Streams (RTMS) for accessing live audio, video, and transcripts 
  from Zoom meetings. WebSocket-based protocol using open web standards. Use when building 
  AI/ML applications, live transcription, or real-time meeting analysis.
---

# Zoom Realtime Media Streams (RTMS)

Access live audio, video, and transcript data from Zoom meetings in real-time.

## Prerequisites

- Zoom app with RTMS feature enabled
- Webhook endpoint for `meeting.rtms_started` event
- Server to receive WebSocket streams

## How It Works

```
1. Meeting starts with RTMS enabled
         ↓
2. Zoom sends `meeting.rtms_started` webhook
         ↓
3. Your server connects via WebSocket
         ↓
4. Receive real-time audio/video/transcript streams
```

## Quick Start

```javascript
// Handle RTMS webhook
app.post('/webhook', (req, res) => {
  const { event, payload } = req.body;
  
  if (event === 'meeting.rtms_started') {
    const { server_urls, rtms_stream_id, signature } = payload;
    
    // Connect to RTMS WebSocket
    const ws = new WebSocket(server_urls);
    
    ws.on('message', (data) => {
      // Process audio/video/transcript data
      console.log('Received media data');
    });
  }
  
  res.status(200).send();
});
```

## Media Types

| Type | Format | Description |
|------|--------|-------------|
| Audio | PCM 16-bit | Raw audio samples |
| Video | H.264 | Encoded video frames |
| Transcript | JSON | Real-time speech-to-text |

## Key Concepts

| Concept | Description |
|---------|-------------|
| RTMS Stream | WebSocket connection for media |
| Stream ID | Unique identifier for the stream |
| Signature | Authentication token |
| Server URLs | WebSocket endpoint(s) |

## Detailed References

- **[references/quickstart.md](references/quickstart.md)** - Getting started guide
- **[references/webhooks.md](references/webhooks.md)** - Webhook events
- **[references/media-types.md](references/media-types.md)** - Audio, video, transcript formats
- **[references/connection.md](references/connection.md)** - WebSocket protocol

## Sample Repositories

### Official (by Zoom)

| Type | Repository | Stars |
|------|------------|-------|
| SDK (Node/Python/Go) | [rtms](https://github.com/zoom/rtms) | 29 |
| Sample Apps | [rtms-samples](https://github.com/zoom/rtms-samples) | 22 |
| C++ SDK | [rtms-sdk-cpp](https://github.com/zoom/rtms-sdk-cpp) | 2 |
| Dev Preview | [rtms-developer-preview-js](https://github.com/zoom/rtms-developer-preview-js) | 3 |
| Quickstart JS | [rtms-quickstart-js](https://github.com/zoom/rtms-quickstart-js) | 1 |
| LangChain | [zoom_rtms_langchain_sample](https://github.com/zoom/zoom_rtms_langchain_sample) | 1 |
| Meeting Assistant | [rtms-meeting-assistant-starter-kit](https://github.com/zoom/rtms-meeting-assistant-starter-kit) | 1 |

### Community

| Type | Repository | Description |
|------|------------|-------------|
| Starter Kit | [tanchunsiong/zoom-rtms-meeting-assistance-starter-kit](https://github.com/tanchunsiong/zoom-rtms-meeting-assistance-starter-kit) | Meeting assistance starter |

**Full list**: See [zoom-general/references/community-repos.md](../zoom-general/references/community-repos.md)

## Resources

- **Official docs**: https://developers.zoom.us/docs/rtms/
- **Developer forum**: https://devforum.zoom.us/

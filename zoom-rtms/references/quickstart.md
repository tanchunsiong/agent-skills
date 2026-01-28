# RTMS - Quickstart

Get started with Zoom Realtime Media Streams.

## Overview

RTMS provides WebSocket-based access to live audio, video, and transcript data from Zoom meetings.

## Prerequisites

1. Zoom app with RTMS feature enabled
2. Webhook endpoint configured
3. Server to handle WebSocket connections

## Setup Steps

### 1. Enable RTMS on Your App

1. Go to [Marketplace](https://marketplace.zoom.us/)
2. Edit your app
3. Enable RTMS feature
4. Configure webhook for `meeting.rtms_started`

### 2. Handle RTMS Webhook

```javascript
app.post('/webhook', (req, res) => {
  const { event, payload } = req.body;
  
  if (event === 'meeting.rtms_started') {
    const {
      server_urls,
      rtms_stream_id,
      signature
    } = payload;
    
    // Connect to RTMS WebSocket
    connectToRTMS(server_urls, rtms_stream_id, signature);
  }
  
  res.status(200).send();
});
```

### 3. Connect to WebSocket

```javascript
const WebSocket = require('ws');

function connectToRTMS(serverUrl, streamId, signature) {
  const ws = new WebSocket(serverUrl, {
    headers: {
      'X-Zoom-RTMS-Stream-Id': streamId,
      'X-Zoom-RTMS-Signature': signature
    }
  });
  
  ws.on('open', () => {
    console.log('Connected to RTMS');
  });
  
  ws.on('message', (data) => {
    // Process media data
    handleMediaData(data);
  });
  
  ws.on('close', () => {
    console.log('RTMS connection closed');
  });
}
```

### 4. Process Media Data

```javascript
function handleMediaData(data) {
  // Parse message type and process accordingly
  // Audio: PCM 16-bit samples
  // Video: H.264 encoded frames
  // Transcript: JSON with text
}
```

## Next Steps

- [Media Types](media-types.md) - Audio, video, transcript formats
- [Connection](connection.md) - WebSocket protocol details

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/

# RTMS - Connection

WebSocket connection protocol details.

## Overview

RTMS uses WebSocket for real-time media streaming from Zoom meetings.

## Connection Flow

```
1. Receive meeting.rtms_started webhook
          ↓
2. Extract server_urls, stream_id, signature
          ↓
3. Open WebSocket connection with auth headers
          ↓
4. Receive media data frames
          ↓
5. Connection closes when meeting ends
```

## Authentication

Include these headers when connecting:

```javascript
const ws = new WebSocket(serverUrl, {
  headers: {
    'X-Zoom-RTMS-Stream-Id': streamId,
    'X-Zoom-RTMS-Signature': signature
  }
});
```

## Message Format

Messages are binary frames with a header indicating type:

| Type | Description |
|------|-------------|
| `0x01` | Audio data |
| `0x02` | Video data |
| `0x03` | Transcript data |
| `0x04` | Control message |

## Handling Connection

```javascript
const WebSocket = require('ws');

function connectRTMS(serverUrl, streamId, signature) {
  const ws = new WebSocket(serverUrl, {
    headers: {
      'X-Zoom-RTMS-Stream-Id': streamId,
      'X-Zoom-RTMS-Signature': signature
    }
  });
  
  ws.on('open', () => {
    console.log('RTMS connected');
  });
  
  ws.on('message', (data) => {
    const type = data[0];
    const payload = data.slice(1);
    
    switch (type) {
      case 0x01:
        handleAudio(payload);
        break;
      case 0x02:
        handleVideo(payload);
        break;
      case 0x03:
        handleTranscript(JSON.parse(payload.toString()));
        break;
    }
  });
  
  ws.on('error', (error) => {
    console.error('RTMS error:', error);
  });
  
  ws.on('close', (code, reason) => {
    console.log('RTMS closed:', code, reason);
  });
  
  return ws;
}
```

## Reconnection

If connection drops:
1. Check if meeting is still active
2. Request new connection credentials via API
3. Reconnect with new credentials

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/

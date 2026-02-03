# RTMS - Connection

WebSocket connection protocol details.

## Connection Flow

```
1. Receive meeting.rtms_started webhook
           ↓
2. Extract server_urls, stream_id, meeting_uuid
           ↓
3. Generate signature (HMAC-SHA256)
           ↓
4. Connect to signaling WebSocket
           ↓
5. Send handshake request (msg_type 1)
           ↓
6. Receive handshake response (msg_type 2) with media server URL
           ↓
7. Connect to media WebSocket(s)
           ↓
8. Send media handshake (msg_type 3)
           ↓
9. Receive media handshake response (msg_type 4)
           ↓
10. Send ready to receive (msg_type 7)
           ↓
11. Receive media data (msg_type 14-18)
           ↓
12. Respond to heartbeats (msg_type 12 → 13)
```

## Signature Generation

```javascript
const crypto = require('crypto');

function generateSignature(clientId, meetingUuid, streamId, clientSecret) {
  const message = `${clientId},${meetingUuid},${streamId}`;
  return crypto.createHmac('sha256', clientSecret).update(message).digest('hex');
}
```

## Signaling Message Types

| msg_type | Name | Direction | Description |
|----------|------|-----------|-------------|
| 1 | Handshake Request | Client → Server | Initiate connection |
| 2 | Handshake Response | Server → Client | Returns media server URL |
| 3 | Media Handshake Request | Client → Server | Request specific media types |
| 4 | Media Handshake Response | Server → Client | Confirms media subscription |
| 7 | Ready to Receive | Client → Server | Signal ready for data |
| 12 | Keep Alive Request | Server → Client | Heartbeat ping |
| 13 | Keep Alive Response | Client → Server | Heartbeat pong |

## Media Message Types

| msg_type | Media Type |
|----------|------------|
| 14 | Audio |
| 15 | Video |
| 16 | Screen Share |
| 17 | Transcript |
| 18 | Chat |

## Critical Gotchas

### 1. Only ONE Connection Per Stream!

```javascript
// WRONG - Connecting twice kicks out first connection
connectToRTMS(serverUrl, streamId);  // Connection 1
connectToRTMS(serverUrl, streamId);  // Connection 2 - kicks out Connection 1!

// CORRECT - Only connect once
if (!activeConnections.has(streamId)) {
  connectToRTMS(serverUrl, streamId);
  activeConnections.set(streamId, ws);
}
```

### 2. Heartbeat is MANDATORY

When you receive msg_type 12, you MUST respond with msg_type 13:

```javascript
ws.on('message', (data) => {
  const msg = JSON.parse(data);
  
  if (msg.msg_type === 12) {  // Keep Alive Request
    ws.send(JSON.stringify({ 
      msg_type: 13,  // Keep Alive Response
      timestamp: msg.timestamp 
    }));
  }
});
```

### 3. Reconnection is YOUR Responsibility

RTMS does NOT auto-reconnect. Implement your own retry logic:

| Server Type | Timeout |
|-------------|---------|
| Media Server | 30 seconds to reconnect |
| Signaling Server | 60 seconds to reconnect |

```javascript
ws.on('close', () => {
  // Implement exponential backoff
  setTimeout(() => reconnect(), retryDelay);
  retryDelay = Math.min(retryDelay * 2, 30000);
});
```

## Split vs Unified Mode

| Mode | Description | Best For |
|------|-------------|----------|
| **Split** | One connection per media type | Most use cases. Media server supports multiple connections with different media types |
| **Unified** | One connection for all media | Real-time audio+video streaming/muxing where sync matters |

## Low-Level Connection Example

```javascript
const WebSocket = require('ws');
const crypto = require('crypto');

async function connectRTMS(webhookPayload) {
  const { server_urls, rtms_stream_id, meeting_uuid } = webhookPayload;
  
  // Generate signature
  const signature = crypto
    .createHmac('sha256', process.env.ZOOM_CLIENT_SECRET)
    .update(`${process.env.ZOOM_CLIENT_ID},${meeting_uuid},${rtms_stream_id}`)
    .digest('hex');
  
  // Connect to signaling server
  const signalingWs = new WebSocket(server_urls, {
    headers: {
      'X-Zoom-RTMS-Stream-Id': rtms_stream_id,
      'X-Zoom-RTMS-Signature': signature
    }
  });
  
  signalingWs.on('open', () => {
    // Send handshake request
    signalingWs.send(JSON.stringify({
      msg_type: 1,
      protocol_version: 1,
      client_id: process.env.ZOOM_CLIENT_ID,
      meeting_uuid: meeting_uuid,
      stream_id: rtms_stream_id,
      signature: signature,
      media_type: 9  // AUDIO(1) | TRANSCRIPT(8)
    }));
  });
  
  signalingWs.on('message', (data) => {
    const msg = JSON.parse(data);
    
    switch (msg.msg_type) {
      case 2:  // Handshake response
        // Connect to media server from msg.media_server_url
        connectMediaServer(msg.media_server_url);
        break;
      case 12:  // Keep alive request
        signalingWs.send(JSON.stringify({ msg_type: 13, timestamp: msg.timestamp }));
        break;
    }
  });
  
  signalingWs.on('error', (error) => {
    console.error('Signaling error:', error);
  });
  
  signalingWs.on('close', (code, reason) => {
    console.log('Signaling closed:', code, reason);
    // Implement reconnection logic
  });
}
```

## Resources

- **RTMS_CONNECTION_FLOW.md**: https://github.com/zoom/rtms-samples/blob/main/RTMS_CONNECTION_FLOW.md
- **ARCHITECTURE.md**: https://github.com/zoom/rtms-samples/blob/main/ARCHITECTURE.md
- **TROUBLESHOOTING.md**: https://github.com/zoom/rtms-samples/blob/main/TROUBLESHOOTING.md

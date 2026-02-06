# RTMS Lifecycle Flow

Complete flow from meeting start to media streaming.

## High-Level Flow

```
┌──────────────────┐
│  Meeting Starts  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Zoom sends      │
│  webhook event   │
│  meeting.rtms_   │
│  started         │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Your server     │
│  receives        │
│  webhook         │
│                  │
│  RESPOND 200     │
│  IMMEDIATELY!    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Connect to      │
│  Signaling WS    │
│                  │
│  Send handshake  │
│  (msg_type: 1)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Receive         │
│  handshake resp  │
│  (msg_type: 2)   │
│                  │
│  Extract media   │
│  server URL      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Connect to      │
│  Media WS        │
│                  │
│  Send handshake  │
│  (msg_type: 3)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Receive media   │
│  handshake resp  │
│  (msg_type: 4)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Send Client     │
│  Ready to        │
│  Signaling       │
│  (msg_type: 7)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Receive media   │
│  data:           │
│  - Audio (14)    │
│  - Video (15)    │
│  - Share (16)    │
│  - Transcript(17)│
│  - Chat (18)     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Respond to      │
│  heartbeats      │
│  (12 -> 13)      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  meeting.rtms_   │
│  stopped         │
│                  │
│  Close sockets   │
│  Cleanup         │
└──────────────────┘
```

## Detailed Steps

### Step 1: Receive Webhook

When RTMS starts, Zoom sends a webhook:

```json
{
  "event": "meeting.rtms_started",
  "payload": {
    "account_id": "abc123",
    "object": {
      "meeting_id": "123456789",
      "meeting_uuid": "AbC123...",
      "host_id": "user123",
      "rtms_stream_id": "stream123==",
      "server_urls": "wss://rtms-sjc1.zoom.us/...",
      "signature": "pre_computed_signature"
    }
  }
}
```

**CRITICAL**: Respond with HTTP 200 **IMMEDIATELY** before any processing!

```javascript
app.post('/webhook', (req, res) => {
  res.status(200).send();  // FIRST!
  
  // Then process async
  handleRTMSStarted(req.body.payload);
});
```

**Why?** If you delay, Zoom retries the webhook. The retry creates a second connection, which kicks out your first connection.

### Step 2: Connect to Signaling WebSocket

```javascript
const signalingWs = new WebSocket(payload.server_urls);

signalingWs.on('open', () => {
  const signature = generateSignature(
    CLIENT_ID, 
    payload.meeting_uuid, 
    payload.rtms_stream_id, 
    CLIENT_SECRET
  );

  signalingWs.send(JSON.stringify({
    msg_type: 1,                    // Handshake request
    protocol_version: 1,
    meeting_uuid: payload.meeting_uuid,
    rtms_stream_id: payload.rtms_stream_id,
    signature: signature,
    media_type: 9                   // Audio(1) + Transcript(8)
  }));
});
```

### Step 3: Handle Signaling Response

```javascript
signalingWs.on('message', (data) => {
  const msg = JSON.parse(data);
  
  switch (msg.msg_type) {
    case 2:  // Handshake response
      if (msg.status_code === 0) {
        // Extract media server URL
        const mediaUrl = msg.media_server.server_urls.all;
        connectToMediaServer(mediaUrl);
      } else {
        console.error('Handshake failed:', msg.status_code);
      }
      break;
      
    case 12:  // Keep alive request
      signalingWs.send(JSON.stringify({
        msg_type: 13,
        timestamp: msg.timestamp
      }));
      break;
  }
});
```

### Step 4: Connect to Media WebSocket

```javascript
function connectToMediaServer(mediaUrl) {
  const mediaWs = new WebSocket(mediaUrl);
  
  mediaWs.on('open', () => {
    mediaWs.send(JSON.stringify({
      msg_type: 3,                  // Media handshake request
      protocol_version: 1,
      meeting_uuid: meetingUuid,
      rtms_stream_id: streamId,
      signature: signature,
      media_type: 9,                // Audio + Transcript
      payload_encryption: false,
      media_params: {
        audio: {
          content_type: 2,          // RAW_AUDIO
          sample_rate: 1,           // 16kHz
          channel: 1,               // Mono
          codec: 1,                 // L16 (PCM)
          data_opt: 1,              // Mixed stream
          send_rate: 20             // 20ms chunks
        },
        transcript: {
          content_type: 5,          // TEXT
          language: 9               // English
        }
      }
    }));
  });
}
```

### Step 5: Start Streaming

After media handshake succeeds, tell signaling you're ready:

```javascript
mediaWs.on('message', (data) => {
  const msg = JSON.parse(data);
  
  if (msg.msg_type === 4 && msg.status_code === 0) {
    // Media handshake success - tell signaling we're ready
    signalingWs.send(JSON.stringify({
      msg_type: 7,                  // Client ready
      rtms_stream_id: streamId
    }));
  }
});
```

### Step 6: Receive Media Data

```javascript
mediaWs.on('message', (data) => {
  const msg = JSON.parse(data);
  
  switch (msg.msg_type) {
    case 14:  // Audio
      const audioBuffer = Buffer.from(msg.content, 'base64');
      processAudio(audioBuffer, msg.user_name, msg.timestamp);
      break;
      
    case 15:  // Video
      const videoBuffer = Buffer.from(msg.content, 'base64');
      processVideo(videoBuffer, msg.user_name, msg.timestamp);
      break;
      
    case 16:  // Screen share
      const shareBuffer = Buffer.from(msg.content, 'base64');
      processScreenShare(shareBuffer, msg.user_name, msg.timestamp);
      break;
      
    case 17:  // Transcript
      console.log(`${msg.user_name}: ${msg.content}`);
      break;
      
    case 18:  // Chat
      console.log(`[Chat] ${msg.user_name}: ${msg.content}`);
      break;
      
    case 12:  // Keep alive
      mediaWs.send(JSON.stringify({
        msg_type: 13,
        timestamp: msg.timestamp
      }));
      break;
  }
});
```

### Step 7: Handle Session End

```javascript
// Via webhook
app.post('/webhook', (req, res) => {
  res.status(200).send();
  
  const { event, payload } = req.body;
  
  if (event === 'meeting.rtms_stopped') {
    const streamId = payload.rtms_stream_id;
    
    // Close connections
    signalingConnections.get(streamId)?.close();
    mediaConnections.get(streamId)?.close();
    
    // Cleanup
    signalingConnections.delete(streamId);
    mediaConnections.delete(streamId);
  }
});

// Also handle WebSocket close events
signalingWs.on('close', (code, reason) => {
  console.log('Signaling closed:', code, reason);
  // Implement reconnection if needed
});
```

## Session Tracking

**CRITICAL**: Track active sessions to prevent duplicate connections!

```javascript
const activeSessions = new Map();

function handleRTMSStarted(payload) {
  const streamId = payload.rtms_stream_id;
  
  // Check for existing connection
  if (activeSessions.has(streamId)) {
    console.log('Already connected to this stream, ignoring');
    return;
  }
  
  // Mark as active
  activeSessions.set(streamId, {
    startTime: Date.now(),
    meetingUuid: payload.meeting_uuid
  });
  
  // Connect
  connectToRTMS(payload);
}

function handleRTMSStopped(payload) {
  const streamId = payload.rtms_stream_id;
  activeSessions.delete(streamId);
  // ... cleanup
}
```

## Error Handling

```javascript
// SDK state management (from Arlo sample)
try {
  client.join(payload);
} catch (error) {
  if (error.message?.includes('Invalid status')) {
    console.warn('SDK in invalid state, waiting to retry...');
    
    setTimeout(() => {
      handleRTMSStarted(payload);
    }, 2000);
  }
}
```

## Next Steps

- **[SDK Quickstart](../examples/sdk-quickstart.md)** - SDK handles all this automatically
- **[Manual WebSocket](../examples/manual-websocket.md)** - Full implementation code
- **[Common Issues](../troubleshooting/common-issues.md)** - Debugging connection problems

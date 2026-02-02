# Connect to RTMS WebSocket

Establish a WebSocket connection to receive real-time media streams from Zoom meetings.

## Overview

The first step in RTMS integration is connecting to the WebSocket server. When a meeting with RTMS enabled starts, Zoom sends a webhook with connection details including the WebSocket URL, stream ID, and signature.

## Skills Needed

- **zoom-rtms** - Primary
- **zoom-webhooks** - Receive RTMS start event

## Architecture

```
┌─────────────┐     Webhook: meeting.rtms_started      ┌─────────────┐
│    Zoom     │ ─────────────────────────────────────▶ │ Your Server │
│   Meeting   │                                        │             │
└─────────────┘                                        └──────┬──────┘
       │                                                      │
       │              WebSocket Connection                    │
       └──────────────────────────────────────────────────────┘
```

## Prerequisites

- Zoom app with RTMS feature enabled
- Webhook endpoint configured for `meeting.rtms_started`
- WebSocket client library (ws for Node.js, websockets for Python)

## Implementation

### JavaScript/Node.js

```javascript
const WebSocket = require('ws');
const express = require('express');

const app = express();
app.use(express.json());

// Store active connections
const activeConnections = new Map();

// Webhook handler
app.post('/webhook', (req, res) => {
  const { event, payload } = req.body;
  
  if (event === 'meeting.rtms_started') {
    const { 
      server_urls,      // Array of WebSocket URLs
      rtms_stream_id,   // Unique stream identifier
      signature,        // Authentication signature
      meeting_uuid      // Meeting identifier
    } = payload;
    
    // Connect to RTMS
    connectToRTMS({
      url: server_urls[0],
      streamId: rtms_stream_id,
      signature: signature,
      meetingUuid: meeting_uuid
    });
  }
  
  res.status(200).send();
});

const crypto = require('crypto');

function generateSignature(clientId, meetingUuid, streamId, clientSecret) {
  return crypto.createHmac('sha256', clientSecret)
    .update(`${clientId},${meetingUuid},${streamId}`)
    .digest('hex');
}

function connectToRTMS(config) {
  // Phase 1: Connect to signaling server
  connectToSignaling(config.meetingUuid, config.streamId, config.url);
}

function connectToSignaling(meetingUuid, streamId, serverUrl) {
  const signalingWs = new WebSocket(serverUrl);
  
  signalingWs.on('open', () => {
    console.log(`Connected to signaling for meeting: ${meetingUuid}`);
    
    // Generate HMAC-SHA256 signature
    const signature = generateSignature(
      process.env.ZOOM_CLIENT_ID,
      meetingUuid,
      streamId,
      process.env.ZOOM_CLIENT_SECRET
    );
    
    // Send signaling handshake (msg_type 1)
    const handshake = {
      msg_type: 1,
      protocol_version: 1,
      meeting_uuid: meetingUuid,
      rtms_stream_id: streamId,
      sequence: Math.floor(Math.random() * 1000000),
      signature: signature
    };
    
    signalingWs.send(JSON.stringify(handshake));
  });
  
  signalingWs.on('message', (data) => {
    const msg = JSON.parse(data);
    handleSignalingMessage(msg, signalingWs, meetingUuid, streamId);
  });
  
  signalingWs.on('error', (err) => {
    console.error('Signaling WebSocket error:', err);
  });
  
  signalingWs.on('close', (code, reason) => {
    console.log(`Signaling connection closed: ${code} - ${reason}`);
    activeConnections.delete(meetingUuid);
  });
  
  // Store signaling connection
  activeConnections.set(meetingUuid, { signaling: signalingWs });
}

function handleSignalingMessage(msg, signalingWs, meetingUuid, streamId) {
  // msg_type 2: Signaling response with media server info
  if (msg.msg_type === 2) {
    if (msg.status_code === 0) {
      console.log('Signaling handshake successful');
      // Connect to media server
      const mediaUrl = msg.media_server.server_urls.all[0];
      connectToMedia(mediaUrl, signalingWs, meetingUuid, streamId);
    } else {
      console.error(`Signaling failed with status: ${msg.status_code}`);
    }
  }
  
  // msg_type 12: Heartbeat request
  if (msg.msg_type === 12) {
    signalingWs.send(JSON.stringify({
      msg_type: 13,
      timestamp: msg.timestamp
    }));
  }
}

function connectToMedia(mediaUrl, signalingWs, meetingUuid, streamId) {
  const mediaWs = new WebSocket(mediaUrl);
  
  mediaWs.on('open', () => {
    console.log(`Connected to media server for meeting: ${meetingUuid}`);
    
    // Generate signature for media connection
    const signature = generateSignature(
      process.env.ZOOM_CLIENT_ID,
      meetingUuid,
      streamId,
      process.env.ZOOM_CLIENT_SECRET
    );
    
    // Send media handshake (msg_type 3)
    const handshake = {
      msg_type: 3,
      protocol_version: 1,
      meeting_uuid: meetingUuid,
      rtms_stream_id: streamId,
      signature: signature,
      media_type: 32, // All media types
      payload_encryption: false,
      media_params: {
        audio: {
          content_type: 1,  // RAW_AUDIO
          sample_rate: 1,   // SR_16K
          channel: 1,       // MONO
          codec: 1,         // L16
          data_opt: 1,      // AUDIO_MIXED_STREAM
          send_rate: 100    // 100ms chunks
        },
        video: {
          codec: 7,         // H264
          resolution: 2,    // 720p
          fps: 25
        }
      }
    };
    
    mediaWs.send(JSON.stringify(handshake));
  });
  
  mediaWs.on('message', (data) => {
    const msg = JSON.parse(data);
    handleMediaMessage(msg, mediaWs, signalingWs, streamId);
  });
  
  mediaWs.on('error', (err) => {
    console.error('Media WebSocket error:', err);
  });
  
  mediaWs.on('close', (code, reason) => {
    console.log(`Media connection closed: ${code} - ${reason}`);
  });
  
  // Store media connection
  const conn = activeConnections.get(meetingUuid);
  if (conn) {
    conn.media = mediaWs;
  }
}

function handleMediaMessage(msg, mediaWs, signalingWs, streamId) {
  // msg_type 4: Media handshake response
  if (msg.msg_type === 4) {
    if (msg.status_code === 0) {
      console.log('Media handshake successful');
      // Send ready message (msg_type 7)
      signalingWs.send(JSON.stringify({
        msg_type: 7,
        rtms_stream_id: streamId
      }));
    } else {
      console.error(`Media handshake failed with status: ${msg.status_code}`);
    }
  }
  
  // msg_type 12: Heartbeat request
  if (msg.msg_type === 12) {
    mediaWs.send(JSON.stringify({
      msg_type: 13,
      timestamp: msg.timestamp
    }));
  }
  
  // msg_type 14: Audio data
  if (msg.msg_type === 14) {
    const audioBuffer = Buffer.from(msg.content, 'base64');
    processAudio(audioBuffer);
  }
  
  // msg_type 15: Video data
  if (msg.msg_type === 15) {
    const videoBuffer = Buffer.from(msg.content, 'base64');
    processVideo(videoBuffer);
  }
  
  // msg_type 17: Transcript data
  if (msg.msg_type === 17) {
    processTranscript(msg);
  }
}

function processAudio(buffer) {
  // Handle audio data
  console.log(`Received audio chunk: ${buffer.length} bytes`);
}

function processVideo(buffer) {
  // Handle video data
  console.log(`Received video chunk: ${buffer.length} bytes`);
}

function processTranscript(msg) {
  // Handle transcript data
  console.log(`Received transcript: ${msg.text}`);
}

function handleMessage(message, meetingUuid) {
  // Legacy handler - kept for compatibility
  // New code uses handleSignalingMessage and handleMediaMessage
}

app.listen(3000, () => {
  console.log('RTMS server listening on port 3000');
});
```

### Python

```python
import asyncio
import websockets
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
active_connections = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event = data.get('event')
    
    if event == 'meeting.rtms_started':
        payload = data['payload']
        config = {
            'url': payload['server_urls'][0],
            'stream_id': payload['rtms_stream_id'],
            'signature': payload['signature'],
            'meeting_uuid': payload['meeting_uuid']
        }
        
        # Start WebSocket connection in background
        asyncio.run(connect_to_rtms(config))
    
    return jsonify({'status': 'ok'}), 200

import hmac
import hashlib
import random
import os

def generate_signature(client_id, meeting_uuid, stream_id, client_secret):
    message = f"{client_id},{meeting_uuid},{stream_id}"
    return hmac.new(
        client_secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

async def connect_to_rtms(config):
    # Phase 1: Connect to signaling server
    await connect_to_signaling(
        config['meeting_uuid'],
        config['stream_id'],
        config['url']
    )

async def connect_to_signaling(meeting_uuid, stream_id, server_url):
    try:
        async with websockets.connect(server_url) as signaling_ws:
            print(f"Connected to signaling for meeting: {meeting_uuid}")
            
            # Generate HMAC-SHA256 signature
            signature = generate_signature(
                os.environ['ZOOM_CLIENT_ID'],
                meeting_uuid,
                stream_id,
                os.environ['ZOOM_CLIENT_SECRET']
            )
            
            # Send signaling handshake (msg_type 1)
            handshake = {
                "msg_type": 1,
                "protocol_version": 1,
                "meeting_uuid": meeting_uuid,
                "rtms_stream_id": stream_id,
                "sequence": random.randint(1, 1000000),
                "signature": signature
            }
            
            await signaling_ws.send(json.dumps(handshake))
            
            # Store connection
            active_connections[meeting_uuid] = {'signaling': signaling_ws}
            
            # Listen for signaling messages
            async for message in signaling_ws:
                data = json.loads(message)
                await handle_signaling_message(data, signaling_ws, meeting_uuid, stream_id)
                
    except Exception as e:
        print(f"Signaling connection error: {e}")

async def handle_signaling_message(msg, signaling_ws, meeting_uuid, stream_id):
    # msg_type 2: Signaling response with media server info
    if msg.get('msg_type') == 2:
        if msg.get('status_code') == 0:
            print('Signaling handshake successful')
            # Connect to media server
            media_url = msg['media_server']['server_urls']['all'][0]
            await connect_to_media(media_url, signaling_ws, meeting_uuid, stream_id)
        else:
            print(f"Signaling failed with status: {msg.get('status_code')}")
    
    # msg_type 12: Heartbeat request
    if msg.get('msg_type') == 12:
        await signaling_ws.send(json.dumps({
            "msg_type": 13,
            "timestamp": msg.get('timestamp')
        }))

async def connect_to_media(media_url, signaling_ws, meeting_uuid, stream_id):
    try:
        async with websockets.connect(media_url) as media_ws:
            print(f"Connected to media server for meeting: {meeting_uuid}")
            
            # Generate signature for media connection
            signature = generate_signature(
                os.environ['ZOOM_CLIENT_ID'],
                meeting_uuid,
                stream_id,
                os.environ['ZOOM_CLIENT_SECRET']
            )
            
            # Send media handshake (msg_type 3)
            handshake = {
                "msg_type": 3,
                "protocol_version": 1,
                "meeting_uuid": meeting_uuid,
                "rtms_stream_id": stream_id,
                "signature": signature,
                "media_type": 32,  # All media types
                "payload_encryption": False,
                "media_params": {
                    "audio": {
                        "content_type": 1,  # RAW_AUDIO
                        "sample_rate": 1,   # SR_16K
                        "channel": 1,       # MONO
                        "codec": 1,         # L16
                        "data_opt": 1,      # AUDIO_MIXED_STREAM
                        "send_rate": 100    # 100ms chunks
                    },
                    "video": {
                        "codec": 7,         # H264
                        "resolution": 2,    # 720p
                        "fps": 25
                    }
                }
            }
            
            await media_ws.send(json.dumps(handshake))
            
            # Store media connection
            conn = active_connections.get(meeting_uuid)
            if conn:
                conn['media'] = media_ws
            
            # Listen for media messages
            async for message in media_ws:
                data = json.loads(message)
                await handle_media_message(data, media_ws, signaling_ws, stream_id)
                
    except Exception as e:
        print(f"Media connection error: {e}")

async def handle_media_message(msg, media_ws, signaling_ws, stream_id):
    # msg_type 4: Media handshake response
    if msg.get('msg_type') == 4:
        if msg.get('status_code') == 0:
            print('Media handshake successful')
            # Send ready message (msg_type 7)
            await signaling_ws.send(json.dumps({
                "msg_type": 7,
                "rtms_stream_id": stream_id
            }))
        else:
            print(f"Media handshake failed with status: {msg.get('status_code')}")
    
    # msg_type 12: Heartbeat request
    if msg.get('msg_type') == 12:
        await media_ws.send(json.dumps({
            "msg_type": 13,
            "timestamp": msg.get('timestamp')
        }))
    
    # msg_type 14: Audio data
    if msg.get('msg_type') == 14:
        audio_buffer = bytes.fromhex(msg.get('content', ''))
        await process_audio(audio_buffer)
    
    # msg_type 15: Video data
    if msg.get('msg_type') == 15:
        video_buffer = bytes.fromhex(msg.get('content', ''))
        await process_video(video_buffer)
    
    # msg_type 17: Transcript data
    if msg.get('msg_type') == 17:
        await process_transcript(msg)

async def process_audio(buffer):
    # Handle audio data
    print(f"Received audio chunk: {len(buffer)} bytes")

async def process_video(buffer):
    # Handle video data
    print(f"Received video chunk: {len(buffer)} bytes")

async def process_transcript(msg):
    # Handle transcript data
    print(f"Received transcript: {msg.get('text')}")

async def handle_message(message, meeting_uuid):
    # Legacy handler - kept for compatibility
    # New code uses handle_signaling_message and handle_media_message
    pass

if __name__ == '__main__':
    app.run(port=3000)
```

## Connection Parameters

| Parameter | Description |
|-----------|-------------|
| `server_urls` | Array of WebSocket URLs (use first available) |
| `rtms_stream_id` | Unique identifier for this media stream |
| `signature` | Authentication token (time-limited) |
| `meeting_uuid` | UUID of the meeting |

## Message Types

| Type | Phase | Description |
|------|-------|-------------|
| 1 | Signaling | Client handshake request |
| 2 | Signaling | Server handshake response with media server info |
| 3 | Media | Client media handshake request |
| 4 | Media | Server media handshake response |
| 7 | Signaling | Client ready message |
| 12 | Both | Server heartbeat request |
| 13 | Both | Client heartbeat response |
| 14 | Media | Audio data |
| 15 | Media | Video data |
| 17 | Media | Transcript data |

## Best Practices

1. **Use the first available URL** - `server_urls` array provides redundancy
2. **Handle reconnection** - Implement exponential backoff for dropped connections
3. **Store connections by meeting UUID** - Allows managing multiple concurrent meetings
4. **Send heartbeats** - Keep connection alive during quiet periods

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/
- **Quick Start**: https://developers.zoom.us/docs/rtms/quick-start/
- **GitHub SDK**: https://github.com/zoom/rtms

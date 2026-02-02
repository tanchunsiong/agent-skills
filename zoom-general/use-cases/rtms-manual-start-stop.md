# Manual Start/Stop RTMS via API

Programmatically start and stop RTMS streams using the Zoom REST API instead of relying solely on webhook-triggered flows.

## Overview

This use case demonstrates how to manually control RTMS streaming using the Zoom REST API. Instead of waiting for a webhook-triggered flow, you listen for `meeting.started` events and then call the Zoom API to start RTMS. You can also schedule automatic stops or trigger them programmatically. This approach uses native WebSocket connections (not the RTMSManager library) to show the raw two-phase RTMS protocol.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

```javascript
import express from 'express';
import WebSocket from 'ws';
import crypto from 'crypto';
import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
app.use(express.json());

// Step 1: Webhook receiver - listen for meeting events
app.post(process.env.WEBHOOK_PATH || '/webhook', async (req, res) => {
  const { event, payload } = req.body;

  // Step 2: On meeting.started, call API to start RTMS
  if (event === 'meeting.started') {
    const meetingId = payload.object.id;
    try {
      const accessToken = process.env.access_token;
      await startRTMS(meetingId, accessToken);
      // Schedule automatic stop after configured duration
      scheduleRTMSStop(meetingId, accessToken);
    } catch (error) {
      console.error('Error starting RTMS:', error);
    }
  }

  // Step 3: On meeting.rtms_started, connect to signaling WebSocket
  if (event === 'meeting.rtms_started') {
    const { meeting_uuid, rtms_stream_id, server_urls } = payload;
    connectToSignalingWebSocket(meeting_uuid, rtms_stream_id, server_urls);
  }

  res.sendStatus(200);
});

// Start RTMS using Zoom REST API
async function startRTMS(meetingId, accessToken) {
  const response = await axios.patch(
    `https://api.zoom.us/v2/live_meetings/${meetingId}/rtms_app/status`,
    {
      action: 'start',
      settings: { client_id: process.env.ZOOM_CLIENT_ID }
    },
    {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      }
    }
  );
  console.log('RTMS start response:', response.data);
  return response.data;
}

// Stop RTMS using Zoom REST API
async function stopRTMS(meetingId, accessToken) {
  const response = await axios.patch(
    `https://api.zoom.us/v2/live_meetings/${meetingId}/rtms_app/status`,
    {
      action: 'stop',
      settings: { client_id: process.env.ZOOM_CLIENT_ID }
    },
    {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      }
    }
  );
  console.log('RTMS stop response:', response.data);
}

// Generate HMAC-SHA256 signature for WebSocket handshake
function generateSignature(meetingUuid, streamId) {
  const message = `${process.env.ZOOM_CLIENT_ID},${meetingUuid},${streamId}`;
  return crypto.createHmac('sha256', process.env.ZOOM_CLIENT_SECRET)
    .update(message).digest('hex');
}

// Phase 1: Connect to signaling WebSocket
function connectToSignalingWebSocket(meetingUuid, streamId, serverUrls) {
  const signalingWs = new WebSocket(serverUrls);

  signalingWs.on('open', () => {
    signalingWs.send(JSON.stringify({
      msg_type: 1, // HANDSHAKE_REQUEST
      meeting_uuid: meetingUuid,
      rtms_stream_id: streamId,
      signature: generateSignature(meetingUuid, streamId)
    }));
  });

  signalingWs.on('message', (data) => {
    const msg = JSON.parse(data);
    if (msg.msg_type === 2 && msg.status_code === 0) {
      const mediaUrl = msg.media_server.server_urls.transcript;
      connectToMediaWebSocket(mediaUrl, meetingUuid, streamId, signalingWs);
    }
    if (msg.msg_type === 12) {
      signalingWs.send(JSON.stringify({ msg_type: 13, timestamp: msg.timestamp }));
    }
  });
}

// Phase 2: Connect to media WebSocket
function connectToMediaWebSocket(mediaUrl, meetingUuid, streamId, signalingSocket) {
  const mediaWs = new WebSocket(mediaUrl);

  mediaWs.on('open', () => {
    mediaWs.send(JSON.stringify({
      msg_type: 3, // MEDIA_HANDSHAKE_REQUEST
      protocol_version: 1,
      meeting_uuid: meetingUuid,
      rtms_stream_id: streamId,
      signature: generateSignature(meetingUuid, streamId),
      media_type: 8 // Transcript only
    }));
  });

  mediaWs.on('message', (data) => {
    const msg = JSON.parse(data);
    if (msg.msg_type === 4 && msg.status_code === 0) {
      signalingSocket.send(JSON.stringify({
        msg_type: 7, // CLIENT_READY
        rtms_stream_id: streamId
      }));
    }
    if (msg.msg_type === 12) {
      mediaWs.send(JSON.stringify({ msg_type: 13, timestamp: msg.timestamp }));
    }
    if (msg.msg_type === 5) {
      console.log('Transcript:', msg);
    }
  });
}

function scheduleRTMSStop(meetingId, accessToken) {
  setTimeout(async () => {
    await stopRTMS(meetingId, accessToken);
  }, 10000); // Stop after 10 seconds (demo)
}

app.listen(3000, () => console.log('Server running on port 3000'));
```

### Python

```python
import requests
import hmac
import hashlib
import json
import os

def start_rtms(meeting_id: str, access_token: str):
    """Start RTMS using Zoom REST API."""
    response = requests.patch(
        f"https://api.zoom.us/v2/live_meetings/{meeting_id}/rtms_app/status",
        json={
            "action": "start",
            "settings": {"client_id": os.environ["ZOOM_CLIENT_ID"]}
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
    )
    response.raise_for_status()
    return response.json()

def stop_rtms(meeting_id: str, access_token: str):
    """Stop RTMS using Zoom REST API."""
    response = requests.patch(
        f"https://api.zoom.us/v2/live_meetings/{meeting_id}/rtms_app/status",
        json={
            "action": "stop",
            "settings": {"client_id": os.environ["ZOOM_CLIENT_ID"]}
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
    )
    response.raise_for_status()
    return response.json()

def generate_signature(meeting_uuid: str, stream_id: str) -> str:
    message = f"{os.environ['ZOOM_CLIENT_ID']},{meeting_uuid},{stream_id}"
    return hmac.new(
        os.environ['ZOOM_CLIENT_SECRET'].encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
```

## Resources

- **Sample repo**: https://github.com/zoom/rtms-samples/tree/main/rtms_api/manual_start_stop_using_js
- **RTMS docs**: https://developers.zoom.us/docs/rtms/
- **Zoom REST API**: https://developers.zoom.us/docs/api/
- **OAuth Guide**: https://developers.zoom.us/docs/integrations/oauth/

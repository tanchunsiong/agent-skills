# Receive Chat Stream via RTMS

Receive and process in-meeting chat messages in real time using Zoom's RTMS.

## Overview

This guide shows how to receive chat messages from a Zoom meeting via the Real-Time Media Stream (RTMS). Chat is delivered as `msg_type: 18` (MEDIA_DATA_CHAT) on the media WebSocket, using `media_type: 16` (MEDIA_DATA_TYPE_CHAT) during the handshake. Each chat message includes the sender's user ID, name, and the message text.

## Prerequisites

- Zoom RTMS app with chat media type enabled
- Zoom Client ID and Client Secret
- Node.js 14+ (for JavaScript) or Python 3.7+ (for Python)

## Skills Needed

- zoom-rtms

## JavaScript Example

### Installation

```bash
npm install express ws dotenv
```

### Code

```javascript
import express from 'express';
import crypto from 'crypto';
import WebSocket from 'ws';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
app.use(express.json());

const CLIENT_ID = process.env.ZOOM_CLIENT_ID;
const CLIENT_SECRET = process.env.ZOOM_CLIENT_SECRET;
const ZOOM_SECRET_TOKEN = process.env.ZOOM_SECRET_TOKEN;

const activeConnections = new Map();

function generateSignature(clientId, meetingUuid, streamId, clientSecret) {
  const message = `${clientId},${meetingUuid},${streamId}`;
  return crypto.createHmac('sha256', clientSecret).update(message).digest('hex');
}

app.post('/webhook', (req, res) => {
  res.sendStatus(200);
  const { event, payload } = req.body;

  if (event === 'endpoint.url_validation' && payload?.plainToken) {
    const hash = crypto.createHmac('sha256', ZOOM_SECRET_TOKEN)
      .update(payload.plainToken).digest('hex');
    return res.json({ plainToken: payload.plainToken, encryptedToken: hash });
  }

  if (event === 'meeting.rtms_started') {
    const { meeting_uuid, rtms_stream_id, server_urls } = payload;
    connectSignaling(meeting_uuid, rtms_stream_id, server_urls);
  }
});

function connectSignaling(meetingUuid, streamId, serverUrl) {
  const ws = new WebSocket(serverUrl);

  ws.on('open', () => {
    ws.send(JSON.stringify({
      msg_type: 1,
      protocol_version: 1,
      meeting_uuid: meetingUuid,
      rtms_stream_id: streamId,
      sequence: Math.floor(Math.random() * 1e9),
      signature: generateSignature(CLIENT_ID, meetingUuid, streamId, CLIENT_SECRET)
    }));
  });

  ws.on('message', (data) => {
    const msg = JSON.parse(data);
    if (msg.msg_type === 2 && msg.status_code === 0) {
      connectMedia(msg.media_server.server_urls.all, meetingUuid, streamId, ws);
    }
    if (msg.msg_type === 12) {
      ws.send(JSON.stringify({ msg_type: 13, timestamp: msg.timestamp }));
    }
  });
}

function connectMedia(mediaUrl, meetingUuid, streamId, signalingWs) {
  const mediaWs = new WebSocket(mediaUrl);

  mediaWs.on('open', () => {
    mediaWs.send(JSON.stringify({
      msg_type: 3,
      protocol_version: 1,
      meeting_uuid: meetingUuid,
      rtms_stream_id: streamId,
      signature: generateSignature(CLIENT_ID, meetingUuid, streamId, CLIENT_SECRET),
      media_type: 16, // MEDIA_DATA_TYPE_CHAT
      payload_encryption: false,
      media_params: {
        chat: { content_type: 5 } // MEDIA_CONTENT_TYPE_TEXT
      }
    }));
  });

  mediaWs.on('message', (data) => {
    const msg = JSON.parse(data.toString());

    if (msg.msg_type === 4 && msg.status_code === 0) {
      signalingWs.send(JSON.stringify({ msg_type: 7, rtms_stream_id: streamId }));
      console.log('Chat streaming started');
    }
    if (msg.msg_type === 12) {
      mediaWs.send(JSON.stringify({ msg_type: 13, timestamp: msg.timestamp }));
    }
    // msg_type 18 = MEDIA_DATA_CHAT
    if (msg.msg_type === 18) {
      console.log(`[${msg.content?.user_name}]: ${msg.content?.data}`);
    }
  });
}

app.listen(3000, () => console.log('Listening on port 3000'));
```

## Python Example

```python
import os, json, hmac, hashlib, random, threading
from flask import Flask, request
import websocket

app = Flask(__name__)
CLIENT_ID = os.environ['ZOOM_CLIENT_ID']
CLIENT_SECRET = os.environ['ZOOM_CLIENT_SECRET']

def generate_signature(meeting_uuid, stream_id):
    message = f"{CLIENT_ID},{meeting_uuid},{stream_id}"
    return hmac.new(CLIENT_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()

def connect_media(media_url, meeting_uuid, stream_id, signaling_ws):
    def on_open(ws):
        ws.send(json.dumps({
            "msg_type": 3, "protocol_version": 1,
            "meeting_uuid": meeting_uuid, "rtms_stream_id": stream_id,
            "signature": generate_signature(meeting_uuid, stream_id),
            "media_type": 16,  # MEDIA_DATA_TYPE_CHAT
            "payload_encryption": False,
            "media_params": {"chat": {"content_type": 5}}
        }))

    def on_message(ws, message):
        msg = json.loads(message)
        if msg['msg_type'] == 4 and msg.get('status_code') == 0:
            signaling_ws.send(json.dumps({"msg_type": 7, "rtms_stream_id": stream_id}))
        if msg['msg_type'] == 12:
            ws.send(json.dumps({"msg_type": 13, "timestamp": msg['timestamp']}))
        if msg['msg_type'] == 18:
            content = msg.get('content', {})
            print(f"[{content.get('user_name')}]: {content.get('data')}")

    media_ws = websocket.WebSocketApp(media_url, on_open=on_open, on_message=on_message)
    threading.Thread(target=media_ws.run_forever).start()

def connect_signaling(meeting_uuid, stream_id, server_url):
    def on_open(ws):
        ws.send(json.dumps({
            "msg_type": 1, "protocol_version": 1,
            "meeting_uuid": meeting_uuid, "rtms_stream_id": stream_id,
            "sequence": random.randint(1, 1000000),
            "signature": generate_signature(meeting_uuid, stream_id)
        }))

    def on_message(ws, message):
        msg = json.loads(message)
        if msg['msg_type'] == 2 and msg.get('status_code') == 0:
            media_url = msg['media_server']['server_urls']['all']
            connect_media(media_url, meeting_uuid, stream_id, ws)
        if msg['msg_type'] == 12:
            ws.send(json.dumps({"msg_type": 13, "timestamp": msg['timestamp']}))

    ws = websocket.WebSocketApp(server_url, on_open=on_open, on_message=on_message)
    threading.Thread(target=ws.run_forever).start()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data.get('event') == 'meeting.rtms_started':
        p = data['payload']
        connect_signaling(p['meeting_uuid'], p['rtms_stream_id'], p['server_urls'])
    return 'OK', 200

if __name__ == '__main__':
    app.run(port=3000)
```

## Resources

- [RTMS Chat Processor](https://github.com/zoom/rtms-samples/tree/main/library/javascript/rtmsManager/processors/chatProcessor.js)
- [RTMS Connection Flow](https://github.com/zoom/rtms-samples/blob/main/RTMS_CONNECTION_FLOW.md)
- [Zoom RTMS Documentation](https://developers.zoom.us/docs/rtms/)

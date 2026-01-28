# Stream to AWS Kinesis

Stream Zoom RTMS audio and video data to AWS Kinesis Video Streams for real-time processing.

## Overview

This guide shows how to forward Zoom RTMS media to AWS Kinesis Video Streams (KVS). RTMS delivers base64-encoded PCM audio and H.264 video via WebSocket. The sample uses a KVS PutMedia producer to push raw audio and video buffers into a Kinesis Video Stream, enabling downstream consumers like Amazon Rekognition, analytics pipelines, or custom processing.

## Prerequisites

- AWS account with Kinesis Video Streams configured
- AWS credentials (Access Key ID, Secret Access Key)
- Zoom RTMS app configured for audio + video
- Node.js 14+ (for JavaScript) or Python 3.7+ (for Python)

## Skills Needed

- zoom-rtms

## JavaScript Example

### Installation

```bash
npm install express ws dotenv aws-sdk amazon-kinesis-video-streams-webrtc
```

### Environment Variables

```bash
ZOOM_CLIENT_ID=your_client_id
ZOOM_CLIENT_SECRET=your_client_secret
ZOOM_SECRET_TOKEN=your_secret_token
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1
KVS_STREAM_NAME=your_kinesis_stream
```

### Code

```javascript
const express = require('express');
const crypto = require('crypto');
const WebSocket = require('ws');
const dotenv = require('dotenv');

// KVS producer module (PutMedia or GStreamer-based)
const { startStream, sendAudioBuffer, sendVideoBuffer } = require('./kvs_putmedia_producer.js');

dotenv.config();

const app = express();
app.use(express.json());

const CLIENT_ID = process.env.ZOOM_CLIENT_ID;
const CLIENT_SECRET = process.env.ZOOM_CLIENT_SECRET;
const activeConnections = new Map();

function generateSignature(clientId, meetingUuid, streamId, clientSecret) {
  const message = `${clientId},${meetingUuid},${streamId}`;
  return crypto.createHmac('sha256', clientSecret).update(message).digest('hex');
}

app.post('/webhook', (req, res) => {
  res.sendStatus(200);
  const { event, payload } = req.body;

  if (event === 'meeting.rtms_started') {
    const { meeting_uuid, rtms_stream_id, server_urls } = payload;
    connectSignaling(meeting_uuid, rtms_stream_id, server_urls);
  }
  if (event === 'meeting.rtms_stopped') {
    const { rtms_stream_id } = payload;
    activeConnections.delete(rtms_stream_id);
  }
});

function connectSignaling(meetingUuid, streamId, serverUrl) {
  const ws = new WebSocket(serverUrl);
  ws.on('open', () => {
    ws.send(JSON.stringify({
      msg_type: 1, protocol_version: 1,
      meeting_uuid: meetingUuid, rtms_stream_id: streamId,
      sequence: Math.floor(Math.random() * 1e9),
      signature: generateSignature(CLIENT_ID, meetingUuid, streamId, CLIENT_SECRET)
    }));
  });
  ws.on('message', (data) => {
    const msg = JSON.parse(data);
    if (msg.msg_type === 2 && msg.status_code === 0) {
      connectMedia(msg.media_server.server_urls.all, meetingUuid, streamId, ws);
    }
    if (msg.msg_type === 12) ws.send(JSON.stringify({ msg_type: 13, timestamp: msg.timestamp }));
  });
}

function connectMedia(mediaUrl, meetingUuid, streamId, signalingWs) {
  const mediaWs = new WebSocket(mediaUrl, { rejectUnauthorized: false });

  mediaWs.on('open', () => {
    mediaWs.send(JSON.stringify({
      msg_type: 3, protocol_version: 1,
      meeting_uuid: meetingUuid, rtms_stream_id: streamId,
      signature: generateSignature(CLIENT_ID, meetingUuid, streamId, CLIENT_SECRET),
      media_type: 32, payload_encryption: false,
      media_params: {
        audio: { content_type: 1, sample_rate: 1, channel: 1, codec: 1, data_opt: 1, send_rate: 100 },
        video: { codec: 7, resolution: 2, fps: 25 }
      }
    }));
  });

  mediaWs.on('message', (data) => {
    try {
      const msg = JSON.parse(data.toString());
      if (msg.msg_type === 4 && msg.status_code === 0) {
        signalingWs.send(JSON.stringify({ msg_type: 7, rtms_stream_id: streamId }));
      }
      if (msg.msg_type === 12) mediaWs.send(JSON.stringify({ msg_type: 13, timestamp: msg.timestamp }));
      if (msg.msg_type === 14 && msg.content?.data) {
        sendAudioBuffer(Buffer.from(msg.content.data, 'base64'));
      }
      if (msg.msg_type === 15 && msg.content?.data) {
        sendVideoBuffer(Buffer.from(msg.content.data, 'base64'));
      }
    } catch (err) {
      console.error('Error processing media message:', err);
    }
  });
}

app.listen(3000, () => {
  console.log('Server running on port 3000');
  startStream(); // Initialize KVS PutMedia producer
});
```

## Python Example

```python
import os, json, hmac, hashlib, random, threading, base64
import boto3
from flask import Flask, request

app = Flask(__name__)
CLIENT_ID = os.environ['ZOOM_CLIENT_ID']
CLIENT_SECRET = os.environ['ZOOM_CLIENT_SECRET']

kvs_client = boto3.client('kinesisvideo', region_name=os.environ.get('AWS_REGION', 'us-east-1'))

def generate_signature(meeting_uuid, stream_id):
    message = f"{CLIENT_ID},{meeting_uuid},{stream_id}"
    return hmac.new(CLIENT_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data.get('event') == 'meeting.rtms_started':
        p = data['payload']
        threading.Thread(target=start_rtms_flow,
                         args=(p['meeting_uuid'], p['rtms_stream_id'], p['server_urls'])).start()
    return 'OK', 200

def start_rtms_flow(meeting_uuid, stream_id, server_url):
    import websocket
    # Follow two-phase WebSocket pattern: signaling then media
    # On msg_type 14 (audio): send to KVS via PutMedia API
    # On msg_type 15 (video): send to KVS via PutMedia API
    pass

if __name__ == '__main__':
    app.run(port=3000)
```

## Resources

- [RTMS Kinesis Streaming Sample](https://github.com/zoom/rtms-samples/tree/main/streaming/stream_to_aws_kinesis_passthru_js)
- [RTMS Connection Flow](https://github.com/zoom/rtms-samples/blob/main/RTMS_CONNECTION_FLOW.md)
- [AWS Kinesis Video Streams](https://docs.aws.amazon.com/kinesisvideostreams/)
- [Zoom RTMS Documentation](https://developers.zoom.us/docs/rtms/)

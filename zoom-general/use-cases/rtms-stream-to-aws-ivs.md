# Stream to AWS Interactive Video Service

Stream Zoom meeting audio and video to AWS IVS for low-latency live streaming.

## Overview

This guide shows how to forward Zoom RTMS audio and video to AWS Interactive Video Service (IVS) using FFmpeg. RTMS delivers raw PCM audio (L16, 16kHz, mono) and H.264 video via WebSocket. FFmpeg re-encodes and pushes the stream to your IVS RTMP ingest endpoint. A gap-filler mechanism injects black video keyframes during mute periods to maintain a continuous stream.

## Prerequisites

- AWS account with an IVS channel created
- IVS RTMP ingest URL (e.g., `rtmps://...ivs.amazonaws.com:443/app/{stream_key}`)
- FFmpeg installed on your server
- Zoom RTMS app configured for audio + video
- Node.js 14+ (for JavaScript) or Python 3.7+ (for Python)

## Skills Needed

- zoom-rtms

## JavaScript Example

### Installation

```bash
npm install express ws dotenv
```

### Environment Variables

```bash
ZOOM_CLIENT_ID=your_client_id
ZOOM_CLIENT_SECRET=your_client_secret
ZOOM_SECRET_TOKEN=your_secret_token
IVS_RTMP_URL=rtmps://abc123.global-contribute.live-video.net:443/app/your_stream_key
```

### Code

```javascript
import express from 'express';
import crypto from 'crypto';
import WebSocket from 'ws';
import { spawn } from 'child_process';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
app.use(express.json());

const CLIENT_ID = process.env.ZOOM_CLIENT_ID;
const CLIENT_SECRET = process.env.ZOOM_CLIENT_SECRET;

function generateSignature(meetingUuid, streamId) {
  const message = `${CLIENT_ID},${meetingUuid},${streamId}`;
  return crypto.createHmac('sha256', CLIENT_SECRET).update(message).digest('hex');
}

function startIVSStream() {
  const ffmpeg = spawn('ffmpeg', [
    '-framerate', '25', '-f', 'h264', '-i', 'pipe:3',
    '-f', 's16le', '-ar', '16000', '-ac', '1', '-i', 'pipe:4',
    '-filter_complex',
    '[1:a]aresample=44100[aout];' +
    '[0:v]scale=1280:720:force_original_aspect_ratio=decrease,' +
    'pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1[vout]',
    '-map', '[vout]', '-map', '[aout]',
    '-c:v', 'libx264', '-preset', 'veryfast', '-tune', 'zerolatency',
    '-g', '50', '-keyint_min', '50', '-b:v', '3000k',
    '-maxrate', '3000k', '-bufsize', '6000k',
    '-c:a', 'aac', '-b:a', '128k', '-ar', '44100',
    '-f', 'flv', process.env.IVS_RTMP_URL
  ], { stdio: ['ignore', 'inherit', 'inherit', 'pipe', 'pipe'] });

  return { ffmpeg, videoStream: ffmpeg.stdio[3], audioStream: ffmpeg.stdio[4] };
}

app.post('/webhook', (req, res) => {
  res.sendStatus(200);
  const { event, payload } = req.body;
  if (event === 'meeting.rtms_started') {
    const { meeting_uuid, rtms_stream_id, server_urls } = payload;
    connectSignaling(meeting_uuid, rtms_stream_id, server_urls);
  }
});

function connectSignaling(meetingUuid, streamId, serverUrl) {
  const ws = new WebSocket(serverUrl);
  ws.on('open', () => {
    ws.send(JSON.stringify({
      msg_type: 1, protocol_version: 1,
      meeting_uuid: meetingUuid, rtms_stream_id: streamId,
      sequence: Math.floor(Math.random() * 1e9),
      signature: generateSignature(meetingUuid, streamId)
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
  const { videoStream, audioStream, ffmpeg } = startIVSStream();
  const mediaWs = new WebSocket(mediaUrl);

  mediaWs.on('open', () => {
    mediaWs.send(JSON.stringify({
      msg_type: 3, protocol_version: 1,
      meeting_uuid: meetingUuid, rtms_stream_id: streamId,
      signature: generateSignature(meetingUuid, streamId),
      media_type: 32, payload_encryption: false,
      media_params: {
        audio: { content_type: 1, sample_rate: 1, channel: 1, codec: 1, data_opt: 1, send_rate: 100 },
        video: { codec: 7, resolution: 2, fps: 25 }
      }
    }));
  });

  mediaWs.on('message', (data) => {
    const msg = JSON.parse(data.toString());
    if (msg.msg_type === 4 && msg.status_code === 0) {
      signalingWs.send(JSON.stringify({ msg_type: 7, rtms_stream_id: streamId }));
    }
    if (msg.msg_type === 12) mediaWs.send(JSON.stringify({ msg_type: 13, timestamp: msg.timestamp }));
    if (msg.msg_type === 14 && msg.content?.data) audioStream.write(Buffer.from(msg.content.data, 'base64'));
    if (msg.msg_type === 15 && msg.content?.data) videoStream.write(Buffer.from(msg.content.data, 'base64'));
  });
}

app.listen(3000, () => console.log('Server running on port 3000'));
```

## Python Example

```python
import os, json, hmac, hashlib, subprocess, threading, random
from flask import Flask, request

app = Flask(__name__)
CLIENT_ID = os.environ['ZOOM_CLIENT_ID']
CLIENT_SECRET = os.environ['ZOOM_CLIENT_SECRET']

def generate_signature(meeting_uuid, stream_id):
    message = f"{CLIENT_ID},{meeting_uuid},{stream_id}"
    return hmac.new(CLIENT_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()

def start_ivs_stream():
    cmd = [
        'ffmpeg',
        '-framerate', '25', '-f', 'h264', '-i', 'pipe:0',
        '-f', 's16le', '-ar', '16000', '-ac', '1', '-i', 'pipe:3',
        '-c:v', 'libx264', '-preset', 'veryfast', '-tune', 'zerolatency',
        '-b:v', '3000k', '-c:a', 'aac', '-b:a', '128k', '-ar', '44100',
        '-f', 'flv', os.environ['IVS_RTMP_URL']
    ]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data.get('event') == 'meeting.rtms_started':
        p = data['payload']
        threading.Thread(target=start_rtms_flow,
                         args=(p['meeting_uuid'], p['rtms_stream_id'], p['server_urls'])).start()
    return 'OK', 200

def start_rtms_flow(meeting_uuid, stream_id, server_url):
    import websocket, base64
    ffmpeg = start_ivs_stream()
    # Follow two-phase WebSocket pattern: signaling (msg_type:1→2) then media (msg_type:3→4→7)
    # On msg_type 14: ffmpeg.stdin.write(base64.b64decode(content['data']))
    # On msg_type 15: ffmpeg.stdin.write(base64.b64decode(content['data']))
    pass

if __name__ == '__main__':
    app.run(port=3000)
```

## Resources

- [RTMS AWS IVS Streaming Sample](https://github.com/zoom/rtms-samples/tree/main/streaming/stream_to_aws_ivs_gap_filler_js)
- [RTMS Connection Flow](https://github.com/zoom/rtms-samples/blob/main/RTMS_CONNECTION_FLOW.md)
- [AWS IVS Documentation](https://docs.aws.amazon.com/ivs/)
- [Zoom RTMS Documentation](https://developers.zoom.us/docs/rtms/)

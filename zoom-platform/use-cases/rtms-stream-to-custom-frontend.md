# Stream to Custom Frontend

Stream Zoom RTMS audio and video to a custom web frontend via HLS.

## Overview

This guide shows how to capture audio and video from Zoom RTMS and serve them as an HLS stream that any web browser can play. FFmpeg receives raw PCM audio and H.264 video from the RTMS media WebSocket, transcodes them, and outputs HLS segments to a local directory. An Express server serves the HLS `.m3u8` playlist and `.ts` segments, and a simple HTML page with hls.js provides the player.

## Prerequisites

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

### Code

```javascript
import express from 'express';
import crypto from 'crypto';
import WebSocket from 'ws';
import { spawn } from 'child_process';
import fs from 'fs';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
app.use(express.json());
app.use(express.static('public'));
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  next();
});

const CLIENT_ID = process.env.ZOOM_CLIENT_ID;
const CLIENT_SECRET = process.env.ZOOM_CLIENT_SECRET;

function generateSignature(meetingUuid, streamId) {
  const message = `${CLIENT_ID},${meetingUuid},${streamId}`;
  return crypto.createHmac('sha256', CLIENT_SECRET).update(message).digest('hex');
}

// FFmpeg transcodes RTMS streams into HLS segments
function startLocalTranscoding() {
  fs.mkdirSync('public/hls', { recursive: true });
  const ffmpeg = spawn('ffmpeg', [
    '-framerate', '25', '-f', 'h264', '-i', 'pipe:3',
    '-f', 's16le', '-ar', '16000', '-ac', '1', '-i', 'pipe:4',
    '-c:v', 'libx264', '-preset', 'veryfast', '-tune', 'zerolatency',
    '-g', '50', '-b:v', '2500k',
    '-c:a', 'aac', '-b:a', '128k', '-ar', '44100',
    '-f', 'hls', '-hls_time', '2', '-hls_list_size', '5',
    '-hls_flags', 'delete_segments',
    'public/hls/stream.m3u8'
  ], { stdio: ['ignore', 'inherit', 'inherit', 'pipe', 'pipe'] });

  return { ffmpeg, videoStream: ffmpeg.stdio[3], audioStream: ffmpeg.stdio[4] };
}

// Serve a simple HLS player page
app.get('/player', (req, res) => {
  res.send(`<!DOCTYPE html>
<html><head><title>Live Stream</title></head>
<body>
  <h2>Live Stream</h2>
  <video id="v" width="720" height="480" controls autoplay></video>
  <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
  <script>
    if (Hls.isSupported()) {
      var hls = new Hls();
      hls.loadSource('/hls/stream.m3u8');
      hls.attachMedia(document.getElementById('v'));
    }
  </script>
</body></html>`);
});

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
  const { videoStream, audioStream, ffmpeg } = startLocalTranscoding();
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

app.listen(3000, () => {
  console.log('Server on port 3000');
  console.log('Player at http://localhost:3000/player');
});
```

## Python Example

```python
import os, json, hmac, hashlib, subprocess, threading
from flask import Flask, request, send_from_directory

app = Flask(__name__, static_folder='public')
CLIENT_ID = os.environ['ZOOM_CLIENT_ID']
CLIENT_SECRET = os.environ['ZOOM_CLIENT_SECRET']

def generate_signature(meeting_uuid, stream_id):
    message = f"{CLIENT_ID},{meeting_uuid},{stream_id}"
    return hmac.new(CLIENT_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()

def start_hls_transcoder():
    os.makedirs('public/hls', exist_ok=True)
    cmd = [
        'ffmpeg', '-framerate', '25', '-f', 'h264', '-i', 'pipe:0',
        '-f', 's16le', '-ar', '16000', '-ac', '1', '-i', 'pipe:3',
        '-c:v', 'libx264', '-preset', 'veryfast',
        '-c:a', 'aac', '-b:a', '128k',
        '-f', 'hls', '-hls_time', '2', '-hls_list_size', '5',
        'public/hls/stream.m3u8'
    ]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)

@app.route('/player')
def player():
    return '''<video id="v" controls autoplay width="720"></video>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>var h=new Hls();h.loadSource("/hls/stream.m3u8");h.attachMedia(document.getElementById("v"));</script>'''

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data.get('event') == 'meeting.rtms_started':
        p = data['payload']
        threading.Thread(target=start_rtms_flow,
                         args=(p['meeting_uuid'], p['rtms_stream_id'], p['server_urls'])).start()
    return 'OK', 200

def start_rtms_flow(meeting_uuid, stream_id, server_url):
    # Follow two-phase WebSocket pattern, pipe audio/video to FFmpeg HLS output
    pass

if __name__ == '__main__':
    app.run(port=3000)
```

## Resources

- [RTMS Custom Frontend Sample](https://github.com/zoom/rtms-samples/tree/main/streaming/stream_audio_and_video_to_custom_frontend_passthru_js)
- [RTMS Connection Flow](https://github.com/zoom/rtms-samples/blob/main/RTMS_CONNECTION_FLOW.md)
- [hls.js](https://github.com/video-dev/hls.js/)
- [Zoom RTMS Documentation](https://developers.zoom.us/docs/rtms/)

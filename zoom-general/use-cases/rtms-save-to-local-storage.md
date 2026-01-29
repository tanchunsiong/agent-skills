# Save to Local Storage

Save Zoom RTMS audio and video streams to local files.

## Overview

This guide shows how to capture audio and video from Zoom RTMS and save them as local files. The RTMSManager library handles the two-phase WebSocket connection, emitting `audio` and `video` events with raw buffers. Audio is saved as raw PCM and later converted to WAV. Video is saved as raw H.264 and converted to MP4 using FFmpeg. A VideoGapFiller fills gaps during mute periods with black keyframes to produce a continuous recording.

## Prerequisites

- FFmpeg installed (for post-processing conversion)
- Zoom RTMS app configured for audio + video
- Node.js 14+ (for JavaScript) or Python 3.7+ (for Python)

## Skills Needed

- zoom-rtms

## JavaScript Example (RTMSManager)

### Installation

```bash
npm install express ws dotenv
```

### Code

```javascript
import { RTMSManager } from './library/javascript/rtmsManager/RTMSManager.js';
import WebhookManager from './library/javascript/webhookManager/WebhookManager.js';
import HelperManager, { VideoGapFiller } from './library/javascript/commonHelpers/HelperManager.js';
import dotenv from 'dotenv';
import path from 'path';
import express from 'express';
import http from 'http';

dotenv.config();

const { MEDIA_PARAMS } = RTMSManager;

const rtmsConfig = {
  logging: 'info',
  mediaTypesFlag: 3, // Audio + Video
  credentials: {
    meeting: {
      clientId: process.env.ZOOM_CLIENT_ID,
      clientSecret: process.env.ZOOM_CLIENT_SECRET,
      zoomSecretToken: process.env.ZOOM_SECRET_TOKEN,
    }
  },
  mediaParams: {
    audio: {
      contentType: MEDIA_PARAMS.MEDIA_CONTENT_TYPE_RTP,
      sampleRate: MEDIA_PARAMS.AUDIO_SAMPLE_RATE_SR_16K,
      channel: MEDIA_PARAMS.AUDIO_CHANNEL_MONO,
      codec: MEDIA_PARAMS.MEDIA_PAYLOAD_TYPE_L16,
      dataOpt: MEDIA_PARAMS.MEDIA_DATA_OPTION_AUDIO_MIXED_STREAM,
      sendRate: 20,
    },
    video: {
      codec: MEDIA_PARAMS.MEDIA_PAYLOAD_TYPE_H264,
      dataOpt: MEDIA_PARAMS.MEDIA_DATA_OPTION_VIDEO_SINGLE_ACTIVE_STREAM,
      resolution: MEDIA_PARAMS.MEDIA_RESOLUTION_HD,
      fps: 25,
    },
  }
};

const app = express();
const server = http.createServer(app);
await RTMSManager.init(rtmsConfig);

const webhookManager = new WebhookManager({
  config: { webhookPath: '/', zoomSecretToken: rtmsConfig.credentials.meeting.zoomSecretToken },
  app
});
webhookManager.on('event', (event, payload) => RTMSManager.handleEvent(event, payload));
webhookManager.setup();

const meetingState = new Map();

// Save raw audio buffers to disk
RTMSManager.on('audio', ({ buffer, timestamp, meetingId, streamId }) => {
  HelperManager.audio.saveRawAudio(buffer, meetingId, 'mixed', timestamp, streamId, true);
});

// Save video with gap filling for continuous output
RTMSManager.on('video', ({ buffer, timestamp, meetingId, streamId }) => {
  if (!meetingState.has(meetingId)) {
    const videoFiller = new VideoGapFiller({ fps: 25, gapThreshold: 320 });
    videoFiller.on('data', ({ buffer: vBuf, timestamp: ts }) => {
      HelperManager.video.saveRawVideo(vBuf, 'mixed', ts, meetingId, streamId, true);
    });
    videoFiller.start();
    meetingState.set(meetingId, { videoFiller, streamId });
  }
  meetingState.get(meetingId).videoFiller.push(buffer, timestamp);
});

// On stop: convert raw files to WAV/MP4 and mux together
RTMSManager.on('meeting.rtms_stopped', async (payload) => {
  const { meeting_uuid, rtms_stream_id } = payload;
  const state = meetingState.get(meeting_uuid);
  if (state) {
    state.videoFiller.stop();
    meetingState.delete(meeting_uuid);
  }
  setTimeout(async () => {
    await HelperManager.audiovideo.convertMeetingMedia(meeting_uuid, rtms_stream_id);
    await HelperManager.audiovideo.muxMixedAudioVideo(meeting_uuid, rtms_stream_id);
  }, 2000);
});

await RTMSManager.start();
server.listen(3000, () => console.log('Listening on port 3000'));
```

## Python Example

```python
import os, json, hmac, hashlib, random, threading, base64
from flask import Flask, request

app = Flask(__name__)
CLIENT_ID = os.environ['ZOOM_CLIENT_ID']
CLIENT_SECRET = os.environ['ZOOM_CLIENT_SECRET']

def generate_signature(meeting_uuid, stream_id):
    message = f"{CLIENT_ID},{meeting_uuid},{stream_id}"
    return hmac.new(CLIENT_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()

def save_buffer(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'ab') as f:
        f.write(data)

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
    # Two-phase WebSocket: signaling (msg_type:1→2) then media (msg_type:3→4→7)
    # On msg_type 14: save_buffer(f'recordings/{meeting_uuid}/audio.pcm', decoded_audio)
    # On msg_type 15: save_buffer(f'recordings/{meeting_uuid}/video.h264', decoded_video)
    # Post-process with FFmpeg: ffmpeg -f s16le -ar 16000 -ac 1 -i audio.pcm audio.wav
    pass

if __name__ == '__main__':
    app.run(port=3000)
```

## Resources

- [RTMS Local Storage Sample](https://github.com/zoom/rtms-samples/tree/main/storage/save_audio_and_video_to_local_storage_js)
- [RTMS Connection Flow](https://github.com/zoom/rtms-samples/blob/main/RTMS_CONNECTION_FLOW.md)
- [Zoom RTMS Documentation](https://developers.zoom.us/docs/rtms/)

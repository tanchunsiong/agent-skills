# Start/Stop RTMS Control from Zoom App

Build a Zoom App UI to start, stop, pause, and resume RTMS streaming from within the meeting using the Zoom Apps SDK.

## Overview

This use case demonstrates programmatic control of RTMS streaming directly from within a Zoom meeting using the Zoom Apps SDK. The frontend provides buttons to call `zoomSdk.startRTMS()`, `zoomSdk.stopRTMS()`, `zoomSdk.pauseRTMS()`, and `zoomSdk.resumeRTMS()`. It subscribes to `onRTMSStatusChange` events for real-time status updates. The backend supports both webhook and WebSocket modes, streaming all media types (audio, video, transcripts, screenshare, chat) to connected frontend clients.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

#### Backend: RTMSManager with All Media Types

```javascript
import { RTMSManager } from './library/javascript/rtmsManager/RTMSManager.js';
import WebhookManager from './library/javascript/webhookManager/WebhookManager.js';
import { FrontendWssManager } from './library/javascript/rtmsManager/FrontendWssManager.js';
import express from 'express';
import http from 'http';

const { MEDIA_PARAMS } = RTMSManager;

const rtmsConfig = {
  logging: 'info',
  credentials: {
    meeting: {
      clientId: process.env.ZOOM_CLIENT_ID,
      clientSecret: process.env.ZOOM_CLIENT_SECRET,
      zoomSecretToken: process.env.ZOOM_SECRET_TOKEN,
    },
  },
  mediaParams: {
    audio: {
      contentType: MEDIA_PARAMS.MEDIA_CONTENT_TYPE_RTP,
      sampleRate: MEDIA_PARAMS.AUDIO_SAMPLE_RATE_SR_16K,
      channel: MEDIA_PARAMS.AUDIO_CHANNEL_MONO,
      codec: MEDIA_PARAMS.MEDIA_PAYLOAD_TYPE_L16,
      dataOpt: MEDIA_PARAMS.MEDIA_DATA_OPTION_AUDIO_MIXED_STREAM,
      sendRate: 100,
    },
    video: {
      codec: MEDIA_PARAMS.VIDEO_CODEC_H264,
      resolution: MEDIA_PARAMS.VIDEO_RESOLUTION_720P,
      dataOpt: MEDIA_PARAMS.MEDIA_DATA_OPTION_VIDEO_SINGLE_ACTIVE_STREAM,
      fps: 25,
    },
    transcript: {
      contentType: MEDIA_PARAMS.MEDIA_CONTENT_TYPE_TEXT,
      language: MEDIA_PARAMS.LANGUAGE_ID_ENGLISH,
    },
  }
};

const app = express();
const server = http.createServer(app);

await RTMSManager.init(rtmsConfig);

const frontendWss = new FrontendWssManager({
  server,
  config: { frontendWssEnabled: true, frontendWssPath: '/ws' }
});
frontendWss.setup();

// Handle all media types and broadcast to frontend
RTMSManager.on('audio', ({ buffer, userName, meetingId, timestamp }) => {
  frontendWss.broadcastToMeeting(meetingId, {
    type: 'audio', user: userName || 'mixed', size: buffer.length, timestamp
  });
});

RTMSManager.on('video', ({ buffer, userName, meetingId }) => {
  frontendWss.broadcastToMeeting(meetingId, {
    type: 'video', user: userName, size: buffer.length
  });
});

RTMSManager.on('transcript', ({ text, userName, userId, meetingId, timestamp }) => {
  frontendWss.broadcastToUser(meetingId, String(userId), {
    type: 'transcript', user: userName, content: text, timestamp
  });
});

RTMSManager.on('screenshare', ({ buffer, userName, meetingId }) => {
  frontendWss.broadcastToMeeting(meetingId, {
    type: 'screenshare', user: userName, size: buffer.length
  });
});

RTMSManager.on('chat', ({ text, userName, meetingId }) => {
  frontendWss.broadcastToMeeting(meetingId, {
    type: 'chat', user: userName, content: text
  });
});

// Track RTMS lifecycle and participant events
RTMSManager.on('meeting.rtms_started', (payload) => {
  frontendWss.broadcastToMeeting(payload.meeting_uuid, {
    type: 'rtms_started', meetingUuid: payload.meeting_uuid
  });
});

RTMSManager.on('meeting.rtms_stopped', (payload) => {
  frontendWss.broadcastToMeeting(payload.meeting_uuid, {
    type: 'rtms_stopped', meetingUuid: payload.meeting_uuid
  });
});

// Event handler for participant and active speaker changes
RTMSManager.on('event', ({ eventType, data, meetingId }) => {
  if (eventType === 2) { // Active speaker changed
    frontendWss.broadcastToMeeting(meetingId, {
      type: 'active_speaker', user: data.user_name, userId: data.user_id
    });
  } else if (eventType === 3) { // Participant joined
    frontendWss.broadcastToMeeting(meetingId, {
      type: 'participant_join', user: data.user_name, userId: data.user_id
    });
  } else if (eventType === 4) { // Participant left
    frontendWss.broadcastToMeeting(meetingId, {
      type: 'participant_leave', user: data.user_name, userId: data.user_id
    });
  }
});

const webhookManager = new WebhookManager({
  config: {
    webhookPath: process.env.WEBHOOK_PATH || '/webhook',
    zoomSecretToken: rtmsConfig.credentials.meeting.zoomSecretToken,
  },
  app: app
});
webhookManager.on('event', (event, payload) => {
  RTMSManager.handleEvent(event, payload);
});
webhookManager.setup();

await RTMSManager.start();
server.listen(process.env.PORT || 3000);
```

#### Frontend: Zoom Apps SDK RTMS Controls

```javascript
// Frontend (runs inside Zoom meeting)
const zoomSdk = window.zoomSdk;

await zoomSdk.config({
  capabilities: [
    'startRTMS', 'stopRTMS', 'pauseRTMS', 'resumeRTMS',
    'getRTMSStatus', 'onRTMSStatusChange',
  ],
});

// Start/Stop/Pause/Resume buttons
document.getElementById('startRtms').addEventListener('click', async () => {
  const response = await zoomSdk.startRTMS();
  console.log('RTMS Start:', response);
});

document.getElementById('stopRtms').addEventListener('click', async () => {
  const response = await zoomSdk.stopRTMS();
  console.log('RTMS Stop:', response);
});

document.getElementById('pauseRtms').addEventListener('click', async () => {
  const response = await zoomSdk.pauseRTMS();
  console.log('RTMS Pause:', response);
});

document.getElementById('resumeRtms').addEventListener('click', async () => {
  const response = await zoomSdk.resumeRTMS();
  console.log('RTMS Resume:', response);
});

// Monitor RTMS status changes in real-time
zoomSdk.on('onRTMSStatusChange', (event) => {
  console.log('RTMS Status Changed:', event);
  document.getElementById('statusBox').textContent =
    `RTMS Status: ${JSON.stringify(event)}`;
});
```

### Python

```python
# Python equivalent for backend RTMS control
# The Zoom Apps SDK frontend controls are JavaScript-only,
# but backend event handling can be done in Python

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event = data.get('event')

    if event == 'meeting.rtms_started':
        payload = data['payload']
        connect_to_rtms(
            payload['meeting_uuid'],
            payload['rtms_stream_id'],
            payload['server_urls']
        )
    elif event == 'meeting.rtms_stopped':
        print(f"RTMS stopped: {data['payload']['meeting_uuid']}")

    return 'OK', 200
```

## Resources

- **Sample repo**: https://github.com/zoom/rtms-samples/tree/main/zoom_apps/start_stop_rtms_control_js
- **RTMS docs**: https://developers.zoom.us/docs/rtms/
- **Zoom Apps SDK**: https://developers.zoom.us/docs/zoom-apps/
- **Zoom Apps SDK JS Reference**: https://appssdk.zoom.us/classes/ZoomSdk.html

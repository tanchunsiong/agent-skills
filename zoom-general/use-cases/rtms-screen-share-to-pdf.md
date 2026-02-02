# Screen Share to PDF

Capture screen share frames from RTMS and compile unique slides into a PDF document.

## Overview

This guide shows how to capture screen share data from Zoom RTMS as JPEG frames, detect unique slides using pixel-level comparison, and compile them into a PDF when the meeting ends. RTMS delivers screen share as `msg_type: 16` (MEDIA_DATA_SHARE_SCREEN). The media handshake uses `media_type: 4` (MEDIA_DATA_TYPE_DESKSHARE) with JPEG codec at 5 FPS. The `pixelmatch` library compares consecutive frames, and only visually distinct frames are saved and later assembled into a PDF with `pdfkit`.

## Prerequisites

- Zoom RTMS app configured for screen share
- Node.js 14+ (for JavaScript) or Python 3.7+ (for Python)

## Skills Needed

- zoom-rtms

## JavaScript Example (RTMSManager)

### Installation

```bash
npm install express ws dotenv sharp pixelmatch pdfkit
```

### Code

```javascript
import { RTMSManager } from './library/javascript/rtmsManager/RTMSManager.js';
import WebhookManager from './library/javascript/webhookManager/WebhookManager.js';
import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs';
import sharp from 'sharp';
import pixelmatch from 'pixelmatch';
import PDFDocument from 'pdfkit';
import express from 'express';
import http from 'http';

dotenv.config();

const { MEDIA_PARAMS } = RTMSManager;

const rtmsConfig = {
  mediaTypesFlag: 4, // Screen share only
  credentials: {
    meeting: {
      clientId: process.env.ZOOM_CLIENT_ID,
      clientSecret: process.env.ZOOM_CLIENT_SECRET,
      zoomSecretToken: process.env.ZOOM_SECRET_TOKEN,
    }
  },
  mediaParams: {
    deskshare: {
      codec: MEDIA_PARAMS.MEDIA_PAYLOAD_TYPE_JPG, // JPEG frames
      resolution: MEDIA_PARAMS.MEDIA_RESOLUTION_FHD,
      fps: 5,
    }
  }
};

const app = express();
const server = http.createServer(app);
await RTMSManager.init(rtmsConfig);

const webhookManager = new WebhookManager({
  config: { webhookPath: '/webhook', zoomSecretToken: rtmsConfig.credentials.meeting.zoomSecretToken },
  app
});
webhookManager.on('event', (event, payload) => RTMSManager.handleEvent(event, payload));
webhookManager.setup();

const sessions = new Map();

RTMSManager.on('sharescreen', async ({ buffer, userId, timestamp, meetingId }) => {
  // Only process valid JPEG frames
  if (!buffer.slice(0, 2).equals(Buffer.from([0xff, 0xd8]))) return;
  if (buffer.length < 1000) return;

  if (!sessions.has(meetingId)) {
    sessions.set(meetingId, { counter: 0, lastBuffer: null, frames: [] });
  }
  const session = sessions.get(meetingId);
  const outDir = path.resolve('recordings', meetingId, 'processed', 'jpg');
  fs.mkdirSync(outDir, { recursive: true });

  let isDifferent = session.lastBuffer === null;
  if (!isDifferent) {
    const current = await sharp(buffer).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
    const { width, height } = current.info;
    const diff = pixelmatch(current.data, session.lastBuffer, null, width, height, { threshold: 0.1 });
    isDifferent = (diff / (width * height)) > 0.01;
  }

  if (isDifferent) {
    session.counter++;
    const filePath = path.join(outDir, `unique_${session.counter}.jpg`);
    fs.writeFileSync(filePath, buffer);
    const rgba = await sharp(buffer).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
    session.lastBuffer = rgba.data;
    session.frames.push({ filePath, timestamp });
  }
});

RTMSManager.on('meeting.rtms_stopped', async ({ meeting_uuid }) => {
  const session = sessions.get(meeting_uuid);
  if (!session || session.frames.length === 0) return;

  const outDir = path.resolve('recordings', meeting_uuid, 'processed');
  const doc = new PDFDocument();
  doc.pipe(fs.createWriteStream(path.join(outDir, 'slides.pdf')));
  for (const frame of session.frames) {
    doc.image(frame.filePath, 0, 0, { width: 600 });
    doc.addPage();
  }
  doc.end();
  console.log(`PDF saved with ${session.frames.length} slides`);
  sessions.delete(meeting_uuid);
});

await RTMSManager.start();
server.listen(3000, () => console.log('Listening on port 3000'));
```

## Python Example

```python
import os, json, hmac, hashlib, threading, io
from flask import Flask, request
from PIL import Image
from fpdf import FPDF

app = Flask(__name__)
CLIENT_ID = os.environ['ZOOM_CLIENT_ID']
CLIENT_SECRET = os.environ['ZOOM_CLIENT_SECRET']
sessions = {}

def generate_signature(meeting_uuid, stream_id):
    message = f"{CLIENT_ID},{meeting_uuid},{stream_id}"
    return hmac.new(CLIENT_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()

def save_frame(meeting_id, frame_data, timestamp):
    """Save unique JPEG frames for later PDF assembly."""
    out_dir = os.path.join('recordings', meeting_id, 'jpg')
    os.makedirs(out_dir, exist_ok=True)
    if meeting_id not in sessions:
        sessions[meeting_id] = {'counter': 0, 'frames': []}
    s = sessions[meeting_id]
    s['counter'] += 1
    path = os.path.join(out_dir, f"unique_{s['counter']}.jpg")
    with open(path, 'wb') as f:
        f.write(frame_data)
    s['frames'].append(path)

def generate_pdf(meeting_id):
    s = sessions.get(meeting_id)
    if not s or not s['frames']:
        return
    pdf = FPDF()
    for frame_path in s['frames']:
        pdf.add_page()
        pdf.image(frame_path, 0, 0, 200)
    pdf.output(os.path.join('recordings', meeting_id, 'slides.pdf'))
    del sessions[meeting_id]

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data.get('event') == 'meeting.rtms_started':
        p = data['payload']
        threading.Thread(target=start_rtms_flow,
                         args=(p['meeting_uuid'], p['rtms_stream_id'], p['server_urls'])).start()
    if data.get('event') == 'meeting.rtms_stopped':
        generate_pdf(data['payload']['meeting_uuid'])
    return 'OK', 200

def start_rtms_flow(meeting_uuid, stream_id, server_url):
    # Two-phase WebSocket with media_type: 4 (screen share)
    # media_params: { deskshare: { codec: 5 (JPG), resolution: 3, fps: 5 } }
    # On msg_type 16: save_frame(meeting_uuid, decoded_jpeg, timestamp)
    pass

if __name__ == '__main__':
    app.run(port=3000)
```

## Resources

- [RTMS Screen Share PDF Sample](https://github.com/zoom/rtms-samples/tree/main/screen_share/save_screen_share_pdf_js)
- [RTMS Connection Flow](https://github.com/zoom/rtms-samples/blob/main/RTMS_CONNECTION_FLOW.md)
- [Zoom RTMS Documentation](https://developers.zoom.us/docs/rtms/)

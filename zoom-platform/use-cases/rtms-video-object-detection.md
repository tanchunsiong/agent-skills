# Video Object Detection with TensorFlow.js

Detect objects in Zoom RTMS video frames using TensorFlow.js and COCO-SSD.

## Overview

This guide shows how to process video frames from Zoom RTMS through a TensorFlow.js object detection model. RTMS delivers H.264 video as `msg_type: 15` (MEDIA_DATA_VIDEO). Each H.264 chunk is decoded into individual image frames using FFmpeg, then fed into the TensorFlow.js COCO-SSD model for real-time object detection. Results include bounding boxes, class labels, and confidence scores for each detected object.

## Prerequisites

- Zoom RTMS app configured for video
- FFmpeg installed (for H.264 frame decoding)
- Node.js 14+ with TensorFlow.js support
- Python 3.7+ (for Python example)

## Skills Needed

- zoom-rtms

## JavaScript Example (RTMSManager + TensorFlow.js)

### Installation

```bash
npm install express ws dotenv @tensorflow/tfjs-node @tensorflow-models/coco-ssd
```

### Code

```javascript
import { RTMSManager } from './library/javascript/rtmsManager/RTMSManager.js';
import WebhookManager from './library/javascript/webhookManager/WebhookManager.js';
import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs';
import express from 'express';
import http from 'http';
import { spawn } from 'child_process';

dotenv.config();

const { MEDIA_PARAMS } = RTMSManager;

const rtmsConfig = {
  mediaTypesFlag: 2, // Video only
  credentials: {
    meeting: {
      clientId: process.env.ZOOM_CLIENT_ID,
      clientSecret: process.env.ZOOM_CLIENT_SECRET,
      zoomSecretToken: process.env.ZOOM_SECRET_TOKEN,
    }
  },
  mediaParams: {
    video: {
      codec: MEDIA_PARAMS.MEDIA_PAYLOAD_TYPE_H264,
      resolution: MEDIA_PARAMS.MEDIA_RESOLUTION_HD,
      fps: 25,
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

// H264 frame decoder using FFmpeg subprocess
class H264FrameDecoder {
  constructor(outputDir, onFrame) {
    this.outputDir = outputDir;
    this.onFrame = onFrame;
    this.frameCount = 0;
    this.ffmpeg = spawn('ffmpeg', [
      '-f', 'h264', '-i', 'pipe:0',
      '-vf', 'fps=1', // Extract 1 frame per second
      '-f', 'image2pipe', '-vcodec', 'mjpeg', 'pipe:1'
    ], { stdio: ['pipe', 'pipe', 'ignore'] });

    this.ffmpeg.stdout.on('data', (data) => {
      this.frameCount++;
      const framePath = path.join(this.outputDir, `frame_${this.frameCount}.jpg`);
      fs.writeFileSync(framePath, data);
      this.onFrame(framePath, { timestamp: Date.now() });
    });
  }

  writeChunk(buffer) {
    if (this.ffmpeg.stdin.writable) this.ffmpeg.stdin.write(buffer);
  }

  close() {
    this.ffmpeg.stdin.end();
  }
}

// TensorFlow.js object detection
async function detectObjects(imagePath, userName, timestamp, meetingId) {
  const tf = await import('@tensorflow/tfjs-node');
  const cocoSsd = await import('@tensorflow-models/coco-ssd');
  const model = await cocoSsd.load();

  const imageBuffer = fs.readFileSync(imagePath);
  const tensor = tf.node.decodeImage(imageBuffer, 3);
  const predictions = await model.detect(tensor);
  tensor.dispose();

  for (const pred of predictions) {
    console.log(`[${meetingId}] ${userName}: ${pred.class} (${(pred.score * 100).toFixed(1)}%)`);
  }
  return predictions;
}

const decoderMap = new Map();

RTMSManager.on('video', ({ buffer, userId, userName, timestamp, meetingId }) => {
  const outputDir = path.join('recordings', meetingId);
  fs.mkdirSync(outputDir, { recursive: true });

  if (!decoderMap.has(userName)) {
    const decoder = new H264FrameDecoder(outputDir, (imagePath, meta) => {
      detectObjects(imagePath, userName, meta.timestamp, meetingId);
    });
    decoderMap.set(userName, decoder);
  }
  decoderMap.get(userName).writeChunk(buffer);
});

RTMSManager.on('meeting.rtms_stopped', () => {
  for (const decoder of decoderMap.values()) decoder.close();
  decoderMap.clear();
});

await RTMSManager.start();
server.listen(3000, () => console.log('Listening on port 3000'));
```

## Python Example

```python
import os, json, hmac, hashlib, threading, base64, subprocess
import numpy as np
import tensorflow as tf
from flask import Flask, request

app = Flask(__name__)
CLIENT_ID = os.environ['ZOOM_CLIENT_ID']
CLIENT_SECRET = os.environ['ZOOM_CLIENT_SECRET']

# Load a pre-trained object detection model
model = tf.saved_model.load('ssd_mobilenet_v2_320x320/saved_model')

def generate_signature(meeting_uuid, stream_id):
    message = f"{CLIENT_ID},{meeting_uuid},{stream_id}"
    return hmac.new(CLIENT_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()

def detect_objects(image_bytes):
    """Run object detection on a JPEG image."""
    img = tf.image.decode_jpeg(image_bytes, channels=3)
    input_tensor = tf.expand_dims(img, 0)
    detections = model(input_tensor)
    scores = detections['detection_scores'][0].numpy()
    classes = detections['detection_classes'][0].numpy()
    for i, score in enumerate(scores):
        if score > 0.5:
            print(f"Detected class {int(classes[i])} with score {score:.2f}")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data.get('event') == 'meeting.rtms_started':
        p = data['payload']
        threading.Thread(target=start_rtms_flow,
                         args=(p['meeting_uuid'], p['rtms_stream_id'], p['server_urls'])).start()
    return 'OK', 200

def start_rtms_flow(meeting_uuid, stream_id, server_url):
    # Two-phase WebSocket with media_type: 2 (video only)
    # Decode H.264 frames with FFmpeg, then run detect_objects() on each frame
    pass

if __name__ == '__main__':
    app.run(port=3000)
```

## Resources

- [RTMS TensorFlow Object Detection Sample](https://github.com/zoom/rtms-samples/tree/main/video/detect_object_using_tensorflow_js)
- [TensorFlow.js COCO-SSD](https://github.com/tensorflow/tfjs-models/tree/master/coco-ssd)
- [RTMS Connection Flow](https://github.com/zoom/rtms-samples/blob/main/RTMS_CONNECTION_FLOW.md)
- [Zoom RTMS Documentation](https://developers.zoom.us/docs/rtms/)

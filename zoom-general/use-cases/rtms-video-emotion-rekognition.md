# Video Emotion Detection with Amazon Rekognition

Detect participant emotions in real-time from video frames using AWS Rekognition facial analysis.

## Overview

This use case captures video frames from Zoom meeting participants via RTMS and analyzes them using Amazon Rekognition's facial analysis API. It detects emotions such as happiness, sadness, anger, surprise, and more for each face detected in the frame. To optimize API usage and costs, only every Nth frame is processed (configurable).

Unlike text-based emotion detection, this approach uses actual video data — analyzing facial expressions rather than transcript sentiment.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

```javascript
import { RTMSManager } from './library/javascript/rtmsManager/RTMSManager.js';
import WebhookManager from './library/javascript/webhookManager/WebhookManager.js';
import { RekognitionClient, DetectFacesCommand } from '@aws-sdk/client-rekognition';
import express from 'express';
import http from 'http';

const { MEDIA_PARAMS } = RTMSManager;

let frameCounter = 0;
const PROCESS_EVERY_N_FRAMES = parseInt(process.env.PROCESS_EVERY_N_FRAMES) || 50;

// Initialize AWS Rekognition client
const rekognition = new RekognitionClient({
  region: process.env.AWS_REGION || 'us-east-1',
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  },
});

async function detectEmotions(imageBuffer) {
  const command = new DetectFacesCommand({
    Image: { Bytes: imageBuffer },
    Attributes: ['ALL'],
  });
  const response = await rekognition.send(command);
  return response.FaceDetails.map(face => ({
    emotions: face.Emotions.sort((a, b) => b.Confidence - a.Confidence),
    ageRange: face.AgeRange,
    smile: face.Smile,
    confidence: face.Confidence,
  }));
}

// Configure RTMSManager for video (JPEG codec for Rekognition compatibility)
const rtmsConfig = {
  logging: { enabled: true, console: true },
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
      codec: MEDIA_PARAMS.MEDIA_PAYLOAD_TYPE_JPG,
      resolution: MEDIA_PARAMS.MEDIA_RESOLUTION_HD,
      fps: 25,
    }
  }
};

const app = express();
const server = http.createServer(app);

await RTMSManager.init(rtmsConfig);

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

// Process video frames for emotion detection
RTMSManager.on('video', async (payload) => {
  const { buffer, userId, userName, timestamp } = payload;
  frameCounter++;

  if (frameCounter % PROCESS_EVERY_N_FRAMES === 0) {
    try {
      const emotions = await detectEmotions(buffer);
      if (emotions.length > 0) {
        console.log(`Frame ${frameCounter} - User: ${userName || userId}`);
        console.log(JSON.stringify(emotions, null, 2));
      }
    } catch (err) {
      console.error(`Error on frame ${frameCounter}:`, err.message);
    }
  }
});

RTMSManager.on('meeting.rtms_started', (payload) => {
  console.log('RTMS Started:', payload.meeting_uuid);
  frameCounter = 0;
});

RTMSManager.on('meeting.rtms_stopped', (payload) => {
  console.log('RTMS Stopped:', payload.meeting_uuid);
});

await RTMSManager.start();

server.listen(process.env.PORT || 3000, () => {
  console.log(`Server listening on port ${process.env.PORT || 3000}`);
});
```

### Python

```python
import boto3
import json
from typing import List, Dict

rekognition = boto3.client(
    'rekognition',
    region_name='us-east-1'
)

def detect_emotions(image_bytes: bytes) -> List[Dict]:
    """Detect emotions in video frame using Amazon Rekognition."""
    response = rekognition.detect_faces(
        Image={'Bytes': image_bytes},
        Attributes=['ALL']
    )
    results = []
    for face in response['FaceDetails']:
        sorted_emotions = sorted(
            face['Emotions'],
            key=lambda e: e['Confidence'],
            reverse=True
        )
        results.append({
            'emotions': sorted_emotions,
            'age_range': face['AgeRange'],
            'smile': face['Smile'],
            'confidence': face['Confidence'],
        })
    return results

# Usage with RTMS video frames
def on_video_frame(frame_data: bytes, user_name: str, frame_num: int):
    """Process every Nth frame for emotion detection."""
    if frame_num % 50 == 0:
        try:
            emotions = detect_emotions(frame_data)
            for face in emotions:
                top_emotion = face['emotions'][0]
                print(f"[{user_name}] {top_emotion['Type']}: "
                      f"{top_emotion['Confidence']:.1f}%")
        except Exception as e:
            print(f"Error detecting emotions: {e}")
```

## Resources

- **Sample repo**: https://github.com/zoom/rtms-samples/tree/main/video/detect_emotion_using_amazon_rekognition_js
- **RTMS docs**: https://developers.zoom.us/docs/rtms/
- **Amazon Rekognition**: https://docs.aws.amazon.com/rekognition/
- **AWS SDK for JavaScript v3**: https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/

# Stream to Azure Blob Storage

Upload Zoom RTMS audio and video recordings to Azure Blob Storage.

## Overview

This guide shows how to capture audio and video from Zoom RTMS, save them locally, convert to WAV/MP4 with FFmpeg, and then upload the final files to Azure Blob Storage. The RTMSManager handles the two-phase WebSocket connection and media events. After the stream stops, converted media files are uploaded to an Azure Blob container using the `@azure/storage-blob` SDK.

## Prerequisites

- Azure Storage account with a connection string
- FFmpeg installed (for post-processing)
- Zoom RTMS app configured for audio + video
- Node.js 14+ (for JavaScript) or Python 3.7+ (for Python)

## Skills Needed

- zoom-rtms

## JavaScript Example (RTMSManager + Azure SDK)

### Installation

```bash
npm install express ws dotenv @azure/storage-blob
```

### Environment Variables

```bash
ZOOM_CLIENT_ID=your_client_id
ZOOM_CLIENT_SECRET=your_client_secret
ZOOM_SECRET_TOKEN=your_secret_token
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...
```

### Code

```javascript
import { RTMSManager } from './library/javascript/rtmsManager/RTMSManager.js';
import WebhookManager from './library/javascript/webhookManager/WebhookManager.js';
import HelperManager, { VideoGapFiller } from './library/javascript/commonHelpers/HelperManager.js';
import { BlobServiceClient } from '@azure/storage-blob';
import dotenv from 'dotenv';
import fs from 'fs';
import path from 'path';
import express from 'express';
import http from 'http';

dotenv.config();

const { MEDIA_PARAMS } = RTMSManager;

const rtmsConfig = {
  mediaTypesFlag: 3,
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

RTMSManager.on('audio', ({ buffer, timestamp, meetingId, streamId }) => {
  HelperManager.audio.saveRawAudio(buffer, meetingId, 'mixed', timestamp, streamId, true);
});

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

// Upload converted files to Azure after stream stops
async function saveToAzure(meetingUuid, streamId) {
  const blobServiceClient = BlobServiceClient.fromConnectionString(
    process.env.AZURE_STORAGE_CONNECTION_STRING
  );
  const containerClient = blobServiceClient.getContainerClient('rtms');
  await containerClient.createIfNotExists();

  const folderPath = path.join('recordings', meetingUuid, streamId);
  const files = fs.readdirSync(folderPath).filter(f =>
    ['.wav', '.mp4'].includes(path.extname(f))
  );

  for (const file of files) {
    const blobName = `${meetingUuid}/${streamId}/${file}`;
    const blockBlobClient = containerClient.getBlockBlobClient(blobName);
    const stream = fs.createReadStream(path.join(folderPath, file));
    await blockBlobClient.uploadStream(stream);
    console.log(`Uploaded: ${blobName}`);
  }
}

RTMSManager.on('meeting.rtms_stopped', async (payload) => {
  const { meeting_uuid, rtms_stream_id } = payload;
  const state = meetingState.get(meeting_uuid);
  if (state) { state.videoFiller.stop(); meetingState.delete(meeting_uuid); }

  setTimeout(async () => {
    await HelperManager.audiovideo.convertMeetingMedia(meeting_uuid, rtms_stream_id);
    await HelperManager.audiovideo.muxMixedAudioVideo(meeting_uuid, rtms_stream_id);
    await saveToAzure(meeting_uuid, rtms_stream_id);
  }, 2000);
});

await RTMSManager.start();
server.listen(3000, () => console.log('Listening on port 3000'));
```

## Python Example

```python
import os, json, hmac, hashlib, threading
from azure.storage.blob import BlobServiceClient
from flask import Flask, request

app = Flask(__name__)
CLIENT_ID = os.environ['ZOOM_CLIENT_ID']
CLIENT_SECRET = os.environ['ZOOM_CLIENT_SECRET']

def generate_signature(meeting_uuid, stream_id):
    message = f"{CLIENT_ID},{meeting_uuid},{stream_id}"
    return hmac.new(CLIENT_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()

def upload_to_azure(meeting_uuid, stream_id):
    blob_service = BlobServiceClient.from_connection_string(
        os.environ['AZURE_STORAGE_CONNECTION_STRING']
    )
    container = blob_service.get_container_client('rtms')
    folder = os.path.join('recordings', meeting_uuid, stream_id)
    for f in os.listdir(folder):
        if f.endswith(('.wav', '.mp4')):
            blob = container.get_blob_client(f"{meeting_uuid}/{stream_id}/{f}")
            with open(os.path.join(folder, f), 'rb') as data:
                blob.upload_blob(data, overwrite=True)
            print(f"Uploaded: {f}")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data.get('event') == 'meeting.rtms_started':
        p = data['payload']
        threading.Thread(target=start_rtms_flow,
                         args=(p['meeting_uuid'], p['rtms_stream_id'], p['server_urls'])).start()
    return 'OK', 200

def start_rtms_flow(meeting_uuid, stream_id, server_url):
    # Two-phase WebSocket: save locally, then upload_to_azure on stop
    pass

if __name__ == '__main__':
    app.run(port=3000)
```

## Resources

- [RTMS Azure Blob Storage Sample](https://github.com/zoom/rtms-samples/tree/main/storage/save_audio_and_video_to_azure_blob_storage_js)
- [Azure Storage Blob SDK](https://learn.microsoft.com/en-us/javascript/api/@azure/storage-blob/)
- [RTMS Connection Flow](https://github.com/zoom/rtms-samples/blob/main/RTMS_CONNECTION_FLOW.md)
- [Zoom RTMS Documentation](https://developers.zoom.us/docs/rtms/)

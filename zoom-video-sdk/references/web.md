# Video SDK - Web

Build custom video experiences in the browser with Zoom Video SDK.

## Overview

The Zoom Video SDK for Web enables fully customized video applications using Zoom's infrastructure. You control the UI, branding, and user experience.

## Prerequisites

- Video SDK credentials from [Marketplace](https://marketplace.zoom.us/) (sign-in required)
- SDK Key and Secret
- Modern browser (Chrome, Firefox, Safari, Edge)

## Installation

```bash
npm install @zoom/videosdk
```

Or via CDN:
```html
<script src="https://source.zoom.us/videosdk/zoom-video-1.11.0.min.js"></script>
```

## Quick Start

```javascript
import ZoomVideo from '@zoom/videosdk';

const client = ZoomVideo.createClient();
await client.init('en-US', 'CDN');
await client.join(topic, signature, userName, password);

const stream = client.getMediaStream();
await stream.startVideo();
await stream.startAudio();
```

## Key Features

### WebRTC Mode

Enable WebRTC mode for direct peer-to-peer streaming with HD video support:

```javascript
await client.init('en-US', 'CDN', {
  webrtc: true  // Enable WebRTC mode
});
```

**Benefits:**
- Up to 1080p HD video
- Improved performance for direct streaming

### Virtual Backgrounds

**Check support before using:**

```javascript
const stream = client.getMediaStream();

// Always check support first
if (stream.isSupportVirtualBackground()) {
  // Blur background
  await stream.updateVirtualBackgroundImage('blur');
  
  // Custom image background
  await stream.updateVirtualBackgroundImage('https://example.com/bg.jpg');
  
  // Remove virtual background
  await stream.updateVirtualBackgroundImage(undefined);
} else {
  console.log('Virtual backgrounds not supported on this device');
}
```

### HD Video Resolution

#### Check HD Capability (IMPORTANT)

**Always check if HD is supported before enabling:**

```javascript
const stream = client.getMediaStream();

// Check if 720p is supported
const hdSupported = stream.isSupportHDVideo();
console.log('HD (720p) supported:', hdSupported);

// Get maximum video quality (returns VideoQuality enum)
const maxQuality = stream.getVideoMaxQuality();
// 0=90P, 1=180P, 2=360P, 3=720P, 4=1080P

// Check SharedArrayBuffer (required for HD)
const sabAvailable = typeof SharedArrayBuffer === 'function';
if (!sabAvailable) {
  console.warn('HD requires SharedArrayBuffer - enable COOP/COEP headers');
}
```

#### Enable HD Video

```javascript
// Start video with HD quality (720p)
await stream.startVideo({ hd: true });

// Start video with Full HD (1080p)
await stream.startVideo({ hd: true, fullHd: true });

// Subscribe to specific quality
await stream.attachVideo(userId, VideoQuality.Video_720P);
```

#### Check Multiple Video Support

```javascript
// Check if gallery view is possible
const multipleVideosSupported = stream.isSupportMultipleVideos();

// Get max renderable videos
const maxRenderable = stream.getMaxRenderableVideos();
console.log('Can render up to', maxRenderable, 'videos');
```

#### Complete HD Detection Flow

```javascript
async function checkHDCapability(client) {
  // 1. Check SharedArrayBuffer
  const sabAvailable = typeof SharedArrayBuffer === 'function';
  
  // 2. Check system requirements
  const compatibility = ZoomVideo.checkSystemRequirements();
  
  // 3. Check feature requirements
  const features = ZoomVideo.checkFeatureRequirements();
  
  // 4. After joining, check stream capabilities
  const stream = client.getMediaStream();
  
  return {
    sharedArrayBuffer: sabAvailable,
    videoCompatible: compatibility.video,
    hdSupported: stream.isSupportHDVideo(),
    maxQuality: stream.getVideoMaxQuality(),
    maxRenderable: stream.getMaxRenderableVideos(),
    multipleVideos: stream.isSupportMultipleVideos(),
    virtualBackground: stream.isSupportVirtualBackground()
  };
}
```

**Resolution tiers:**
- 1:1 calls: Up to 1080p
- Small groups: Up to 720p
- Larger sessions: Adaptive

**Concurrent HD limits:**
- Max 2 concurrent 720p subscriptions
- Max 1 concurrent 1080p render

### Rendering Modes

Multiple rendering options available:
- WebRTC mode (direct streaming)
- WebAssembly mode (default)
- Canvas rendering
- Video element rendering

## Video Processor (Custom Effects)

The `VideoProcessor` class allows you to intercept and modify video frames before transmission. Use this for custom overlays, effects, face detection, and more.

### How It Works

1. Create a video processor worker
2. Extend `VideoProcessor` class
3. Implement `processFrame()` to modify each frame
4. Output to `OffscreenCanvas`

### Basic Example

```javascript
// video-processor-worker.js
class MyVideoProcessor extends VideoProcessor {
  constructor(port, options) {
    super(port, options);
  }

  processFrame(input, output) {
    const ctx = output.getContext('2d');
    
    // Draw original frame
    ctx.drawImage(input, 0, 0);
    
    // Add overlay (e.g., text, graphics)
    ctx.fillStyle = 'white';
    ctx.font = '24px Arial';
    ctx.fillText('Live', 20, 40);
    
    return true;
  }
}
```

### Face Detection with face-api.js

Combine VideoProcessor with face-api.js for face detection overlays:

```javascript
// video-processor-worker.js
import * as faceapi from 'face-api.js';

class FaceDetectionProcessor extends VideoProcessor {
  async processFrame(input, output) {
    const ctx = output.getContext('2d');
    
    // Draw original frame
    ctx.drawImage(input, 0, 0);
    
    // Detect faces
    const detections = await faceapi.detectAllFaces(input);
    
    // Draw bounding boxes
    detections.forEach(detection => {
      const box = detection.box;
      ctx.strokeStyle = '#00ff00';
      ctx.lineWidth = 2;
      ctx.strokeRect(box.x, box.y, box.width, box.height);
    });
    
    return true;
  }
}
```

### Use Cases

| Use Case | Description |
|----------|-------------|
| Face detection | Bounding boxes, landmarks |
| AR effects | Glasses, hats, masks |
| Beauty filters | Skin smoothing, color correction |
| Overlays | Text, logos, watermarks |
| Real-time translation | OCR + translation overlay |

### Resources

- **VideoProcessor API**: https://marketplacefront.zoom.us/sdk/custom/web/classes/VideoProcessor.html
- **Zoom Blog - AI Text Translation**: https://developers.zoom.us/blog/ai-text-translator-with-videosdk-share-processor/

## Video Rendering (Canvas Mode)

### Render Order (CRITICAL)

**Must call `renderVideo()` AFTER `startVideo()` completes:**

```javascript
const stream = client.getMediaStream();

// CORRECT: Wait for startVideo to complete
await stream.startVideo();
await stream.renderVideo(canvas, client.getCurrentUserInfo().oderId, 640, 360, 0, 0, 3);

// WRONG: Calling renderVideo before startVideo completes
stream.startVideo();  // Don't await
stream.renderVideo(canvas, userId);  // Will fail!
```

### Stop Order (CRITICAL)

**Stop rendering BEFORE stopping video:**

```javascript
// CORRECT order
await stream.stopRenderVideo(canvas, userId);
await stream.stopVideo();

// WRONG order - may cause errors
await stream.stopVideo();
await stream.stopRenderVideo(canvas, userId);  // Too late!
```

### Canvas Must Exist in DOM

```javascript
// CORRECT: Canvas exists before rendering
const canvas = document.getElementById('my-canvas');  // Already in DOM
await stream.renderVideo(canvas, userId, 640, 360, 0, 0, 3);

// WRONG: Creating canvas but not adding to DOM
const canvas = document.createElement('canvas');
await stream.renderVideo(canvas, userId);  // Won't display!
```

### Use Single Rendering Control (IMPORTANT)

**For performance, use ONE shared rendering control for all video streams, NOT one control per video.**

```javascript
// CORRECT: Single video container for all participants
const videoContainer = document.getElementById('video-container');
const stream = client.getMediaStream();

// Render all participants to the same container
await stream.renderVideo(videoContainer, userId, width, height, x, y, quality);
```

```javascript
// WRONG: Creating separate controls per participant
// This degrades performance significantly!
participants.forEach(p => {
  const container = document.createElement('div');  // DON'T do this
  stream.renderVideo(container, p.id, ...);
});
```

**Why:**
- Multiple rendering controls consume excessive resources
- Performance degrades significantly with more participants
- Single control handles internal layout management efficiently

## Peer Video on Mid-Session Join (IMPORTANT)

**Existing participants' videos won't auto-render when you join mid-session.**

You must manually iterate all users and render their video:

```javascript
client.on('connection-change', async (payload) => {
  if (payload.state === 'Connected') {
    // Add delay to ensure session is fully established
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const stream = client.getMediaStream();
    const users = client.getAllUser();
    
    for (const user of users) {
      if (user.bVideoOn && user.oderId !== client.getCurrentUserInfo().oderId) {
        await stream.renderVideo(canvas, user.oderId, 640, 360, 0, 0, 3);
      }
    }
  }
});
```

**Key points:**
- Check `user.bVideoOn` to see if video is enabled
- Skip self (`client.getCurrentUserInfo().oderId`)
- Add ~1 second delay after join before rendering

## SharedArrayBuffer

For optimal performance, configure these headers on your server:

```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

**Note:** As of v1.11.2, SharedArrayBuffer is elective (not strictly required).

## Event Handling

```javascript
client.on('user-added', (payload) => {
  console.log('User joined:', payload);
});

client.on('user-removed', (payload) => {
  console.log('User left:', payload);
});

client.on('video-active-change', (payload) => {
  // Handle video state changes
});
```

## Common Tasks

### Start/Stop Video
```javascript
await stream.startVideo();
await stream.stopVideo();
```

### Start/Stop Audio
```javascript
await stream.startAudio();
await stream.muteAudio();
await stream.unmuteAudio();
```

### Screen Sharing

#### Receive Screen Share

Listen to `active-share-change` event and render when active:

```javascript
client.on('active-share-change', async (payload) => {
  const stream = client.getMediaStream();
  
  if (payload.state === 'Active') {
    // Add small delay to ensure DOM element exists
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // Check if should use video element or canvas
    if (stream.isStartShareScreenWithVideoElement()) {
      const video = document.getElementById('share-video');
      await stream.startShareView(video as unknown as HTMLCanvasElement, payload.userId);
    } else {
      const canvas = document.getElementById('share-canvas');
      await stream.startShareView(canvas, payload.userId);
    }
  } else if (payload.state === 'Inactive') {
    await stream.stopShareView();
  }
});
```

#### Send Screen Share

Check rendering mode before starting:

```javascript
const stream = client.getMediaStream();

// Check which element type to use
if (stream.isStartShareScreenWithVideoElement()) {
  // Use video element
  const video = document.getElementById('share-video');
  await stream.startShareScreen(video as unknown as HTMLCanvasElement);
} else {
  // Use canvas element
  const canvas = document.getElementById('share-canvas');
  await stream.startShareScreen(canvas);
}
```

#### Stop Screen Share

```javascript
await stream.stopShareScreen();
```

#### Type Casting Workaround

SDK types expect `HTMLCanvasElement` even for video elements. Cast when needed:

```typescript
// When using HTMLVideoElement where SDK expects HTMLCanvasElement
const video = document.getElementById('share-video') as HTMLVideoElement;
await stream.startShareView(video as unknown as HTMLCanvasElement, userId);
```

## Host vs Participant

```javascript
// Leave session (others stay)
await client.leave();

// End session for ALL participants (host only)
await client.leave(true);
```

## Recording (Host Only)

Only the host (role=1) can start/stop recording:

```javascript
const recordingClient = client.getRecordingClient();

// Start cloud recording
await recordingClient.startCloudRecording();

// Stop recording
await recordingClient.stopCloudRecording();

// Listen for recording status changes
client.on('recording-change', (payload) => {
  console.log('Recording status:', payload.status);
});
```

## Live Transcription

```javascript
const transcriptionClient = client.getLiveTranscriptionClient();

// Start live transcription
await transcriptionClient.startLiveTranscription();

// Stop live transcription
await transcriptionClient.stopLiveTranscription();

// Listen for captions
client.on('caption-message', (payload) => {
  console.log(`${payload.displayName}: ${payload.text}`);
});
```

## Device Selection

```javascript
// Get available devices
const devices = await ZoomVideo.getDevices();
console.log('Cameras:', devices.cameras);
console.log('Microphones:', devices.microphones);
console.log('Speakers:', devices.speakers);

// Get currently active devices
const stream = client.getMediaStream();
const activeCamera = stream.getActiveCamera();
const activeMic = stream.getActiveMicrophone();
const activeSpeaker = stream.getActiveSpeaker();

// Switch devices
await stream.switchCamera(deviceId);
await stream.switchMicrophone(deviceId);
await stream.switchSpeaker(deviceId);
```

## Network Quality

Monitor network quality in real-time:

```javascript
client.on('network-quality-change', (payload) => {
  // payload.type = 'uplink' or 'downlink'
  // payload.level = 0-5 (5 is best)
  
  if (payload.level < 2) {
    console.warn(`Poor ${payload.type} network quality: ${payload.level}`);
  }
});
```

## File Sharing

```javascript
const chatClient = client.getChatClient();

// Send file to everyone (receiverId = 0)
await chatClient.sendFile(file, 0);

// Send file to specific user
await chatClient.sendFile(file, userId);
```

## Breakout Rooms (Subsessions)

Video SDK uses "Subsessions" instead of native breakout rooms:

```javascript
const subsessionClient = client.getSubsessionClient();

// Create subsessions
const roomNames = ['Room 1', 'Room 2', 'Room 3'];
await subsessionClient.createSubsessions(roomNames);

// Open subsessions
const rooms = subsessionClient.getSubsessionList();
await subsessionClient.openSubsessions(rooms);

// Broadcast message to all rooms
await subsessionClient.broadcast('Please return to main session in 5 minutes');

// Close all subsessions
await subsessionClient.closeAllSubsessions();
```

## Reactions via Command Channel

Use the command channel for custom messages like reactions:

```javascript
const commandClient = client.getCommandClient();

// Send reaction
const reaction = { type: 'reaction', emoji: '👍' };
await commandClient.send(JSON.stringify(reaction));

// Receive reactions
client.on('command-channel-message', (payload) => {
  try {
    const data = JSON.parse(payload.text);
    if (data.type === 'reaction') {
      console.log(`${payload.senderName} reacted with ${data.emoji}`);
    }
  } catch (e) {
    console.log('Non-JSON message:', payload.text);
  }
});
```

## CORS Errors (Telemetry)

**CORS errors to `log-external-gateway.zoom.us` are harmless.**

These are caused by COOP/COEP headers blocking telemetry requests. They don't affect SDK functionality.

```
// These console errors can be safely ignored:
// Access to fetch at 'https://log-external-gateway.zoom.us/...' has been blocked by CORS policy
```

## Resources

- **Official docs**: https://developers.zoom.us/docs/video-sdk/web/
- **API Reference**: https://marketplacefront.zoom.us/sdk/custom/web/modules.html
- **Sample app**: https://github.com/zoom/videosdk-web-sample

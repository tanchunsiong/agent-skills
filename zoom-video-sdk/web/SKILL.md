---
name: zoom-video-sdk/web
description: "Zoom Video SDK for Web - JavaScript/TypeScript integration for browser-based video sessions, real-time communication, screen sharing, recording, and live transcription"
---

# Zoom Video SDK - Web Development

Expert guidance for developing with the Zoom Video SDK on Web. This SDK enables custom video applications in the browser with real-time video/audio, screen sharing, cloud recording, live streaming, chat, and live transcription.

**Official Documentation**: https://developers.zoom.us/docs/zoom-video-sdk/web/
**API Reference**: https://marketplacefront.zoom.us/sdk/custom/web/modules.html
**Sample Repository**: https://github.com/zoom/videosdk-web-sample

## Quick Links

**New to Video SDK? Follow this path:**

1. **[SDK Architecture Pattern](concepts/sdk-architecture-pattern.md)** - Universal 3-step pattern for ANY feature
2. **[Session Join Pattern](examples/session-join-pattern.md)** - Complete working code to join a session
3. **[Video Rendering](examples/video-rendering.md)** - Display video with attachVideo()
4. **[Event Handling](examples/event-handling.md)** - Required events for video/audio

**Reference:**
- **[Singleton Hierarchy](concepts/singleton-hierarchy.md)** - 4-level SDK navigation map
- **[API Reference](references/web-reference.md)** - Methods, events, error codes
- **[INDEX.md](INDEX.md)** - Complete documentation navigation

**Having issues?**
- Video not showing → [Video Rendering](examples/video-rendering.md) (use attachVideo, not renderVideo)
- getMediaStream() returns undefined → Call AFTER join() completes
- Quick diagnostics → [Common Issues](troubleshooting/common-issues.md)

## SDK Overview

The Zoom Video SDK for Web is a JavaScript library that provides:
- **Session Management**: Join/leave video SDK sessions
- **Video/Audio**: Start/stop camera and microphone
- **Screen Sharing**: Share screens or browser tabs
- **Cloud Recording**: Record sessions to Zoom cloud
- **Live Streaming**: Stream to RTMP endpoints
- **Chat**: In-session messaging
- **Command Channel**: Custom command messaging
- **Live Transcription**: Real-time speech-to-text
- **Subsessions**: Breakout room support
- **Whiteboard**: Collaborative whiteboard features
- **Virtual Background**: Blur or custom image backgrounds

## Prerequisites

### System Requirements

- **Modern Browser**: Chrome 80+, Firefox 75+, Safari 14+, Edge 80+
- **Video SDK Credentials**: SDK Key and Secret from [Marketplace](https://marketplace.zoom.us/)
- **JWT Token**: Server-side generated signature

### Browser Feature Requirements

```javascript
// Check browser compatibility before init
const compatibility = ZoomVideo.checkSystemRequirements();
console.log('Audio:', compatibility.audio);
console.log('Video:', compatibility.video);
console.log('Screen:', compatibility.screen);

// Check feature support
const features = ZoomVideo.checkFeatureRequirements();
console.log('Supported:', features.supportFeatures);
console.log('Unsupported:', features.unSupportFeatures);
```

## Installation

### NPM (Recommended)

```bash
npm install @zoom/videosdk
```

```javascript
import ZoomVideo from '@zoom/videosdk';
```

### CDN (Fallback Strategy Recommended)

> **Note**: Some networks/ad blockers can block `source.zoom.us`. If you see flaky loads, first try allowlisting the domain in your environment. If needed, consider a fallback (mirror/self-host) only if it's permitted for your use case and you can keep versions in sync.

```bash
# Download SDK locally
curl "https://source.zoom.us/videosdk/zoom-video-2.3.12.min.js" -o public/js/zoom-video-sdk.min.js
```

```html
<!-- Use local copy instead of CDN -->
<script src="js/zoom-video-sdk.min.js"></script>
```

```javascript
// CDN exports as WebVideoSDK, NOT ZoomVideo
const ZoomVideo = WebVideoSDK.default;
```

## Quick Start

```javascript
import ZoomVideo from '@zoom/videosdk';

// 1. Create client (singleton - returns same instance)
const client = ZoomVideo.createClient();

// 2. Initialize SDK
await client.init('en-US', 'Global', { patchJsMedia: true });

// 3. Join session
await client.join(topic, signature, userName, password);

// 4. CRITICAL: Get stream AFTER join
const stream = client.getMediaStream();

// 5. Start media
await stream.startVideo();
await stream.startAudio();

// 6. Attach video to DOM
const videoElement = await stream.attachVideo(userId, VideoQuality.Video_360P);
document.getElementById('video-container').appendChild(videoElement);
```

## SDK Lifecycle (CRITICAL ORDER)

The SDK has a strict lifecycle. Violating it causes **silent failures**.

```
1. Create client:     client = ZoomVideo.createClient()
2. Initialize:        await client.init('en-US', 'Global', options)
3. Join session:      await client.join(topic, signature, userName, password)
4. Get stream:        stream = client.getMediaStream()  ← ONLY AFTER JOIN
5. Start media:       await stream.startVideo() / await stream.startAudio()
```

**Common Mistake:**

```javascript
// WRONG: Getting stream before joining
const stream = client.getMediaStream();  // Returns undefined!
await client.join(...);

// CORRECT: Get stream after joining
await client.join(...);
const stream = client.getMediaStream();  // Works!
```

## Critical Gotchas and Best Practices

### getMediaStream() ONLY Works After join()

The #1 issue that causes video/audio to fail:

```javascript
// WRONG
const stream = client.getMediaStream();  // undefined!
await client.join(...);

// CORRECT
await client.join(...);
const stream = client.getMediaStream();  // Works
```

### Use attachVideo() NOT renderVideo()

`renderVideo()` is **deprecated**. Use `attachVideo()` which returns a VideoPlayer element:

```javascript
import { VideoQuality } from '@zoom/videosdk';

// CORRECT: attachVideo returns element to append
const videoElement = await stream.attachVideo(userId, VideoQuality.Video_360P);
document.getElementById('video-container').appendChild(videoElement);

// WRONG: renderVideo is deprecated
await stream.renderVideo(canvas, userId, ...);  // Don't use!
```

### Video Rendering is Event-Driven (CRITICAL)

You MUST listen for events to properly render participant videos:

```javascript
// When another participant's video state changes
client.on('peer-video-state-change', async (payload) => {
  const { action, userId } = payload;
  
  if (action === 'Start') {
    // Participant turned on video - attach it
    const element = await stream.attachVideo(userId, VideoQuality.Video_360P);
    container.appendChild(element);
  } else if (action === 'Stop') {
    // Participant turned off video - detach it
    await stream.detachVideo(userId);
  }
});

// When participants join/leave
client.on('user-added', (payload) => {
  // New participant joined - check if their video is on
  const users = client.getAllUser();
  // Render videos for users with bVideoOn === true
});

client.on('user-removed', (payload) => {
  // Participant left - clean up their video element
  stream.detachVideo(payload[0].userId);
});
```

### Peer Video on Mid-Session Join

**Existing participants' videos won't auto-render when you join mid-session.**

```javascript
// After joining, render existing participants' videos
const renderExistingVideos = async () => {
  await new Promise(resolve => setTimeout(resolve, 500));
  
  const users = client.getAllUser();
  const currentUserId = client.getCurrentUserInfo().userId;
  
  for (const user of users) {
    if (user.bVideoOn && user.userId !== currentUserId) {
      const element = await stream.attachVideo(user.userId, VideoQuality.Video_360P);
      document.getElementById(`video-${user.userId}`).appendChild(element);
    }
  }
};
```

### CDN Race Condition with ES Modules

When using `<script type="module">` with CDN, the SDK may not be loaded yet:

```javascript
function waitForSDK(timeout = 10000) {
  return new Promise((resolve, reject) => {
    if (typeof WebVideoSDK !== 'undefined') {
      resolve();
      return;
    }
    const start = Date.now();
    const check = setInterval(() => {
      if (typeof WebVideoSDK !== 'undefined') {
        clearInterval(check);
        resolve();
      } else if (Date.now() - start > timeout) {
        clearInterval(check);
        reject(new Error('SDK failed to load'));
      }
    }, 100);
  });
}

await waitForSDK();
const ZoomVideo = WebVideoSDK.default;
```

### SharedArrayBuffer for HD Video

For optimal performance and HD video, configure these headers on your server:

```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

**Note:** As of v1.11.2, SharedArrayBuffer is elective (not strictly required).

### Check HD Capability Before Enabling

```javascript
const stream = client.getMediaStream();

// Check if 720p is supported
const hdSupported = stream.isSupportHDVideo();

// Get maximum video quality
const maxQuality = stream.getVideoMaxQuality();
// 0=90P, 1=180P, 2=360P, 3=720P, 4=1080P

// Start video with HD
if (hdSupported) {
  await stream.startVideo({ hd: true });
}
```

### Screen Share Rendering Mode Check

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

## Key Features

### Video Quality Enum

```javascript
import { VideoQuality } from '@zoom/videosdk';

VideoQuality.Video_90P   // 0
VideoQuality.Video_180P  // 1
VideoQuality.Video_360P  // 2 (recommended for most cases)
VideoQuality.Video_720P  // 3
VideoQuality.Video_1080P // 4
```

### Virtual Backgrounds

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
}
```

### Video Processor (Custom Effects)

The `VideoProcessor` class allows you to intercept and modify video frames:

```javascript
// video-processor-worker.js
class MyVideoProcessor extends VideoProcessor {
  processFrame(input, output) {
    const ctx = output.getContext('2d');
    ctx.drawImage(input, 0, 0);
    
    // Add overlay
    ctx.fillStyle = 'white';
    ctx.font = '24px Arial';
    ctx.fillText('Live', 20, 40);
    
    return true;
  }
}
```

### WebRTC Mode

Enable WebRTC mode for direct peer-to-peer streaming with HD video support:

```javascript
await client.init('en-US', 'Global', {
  patchJsMedia: true,
  webrtc: true  // Enable WebRTC mode
});
```

## Feature Clients

Access specialized clients from the VideoClient:

| Client | Access Method | Purpose |
|--------|---------------|---------|
| **Stream** | `client.getMediaStream()` | Video, audio, screen share, devices |
| **Chat** | `client.getChatClient()` | Send/receive messages |
| **Command** | `client.getCommandClient()` | Custom commands (reactions, etc.) |
| **Recording** | `client.getRecordingClient()` | Cloud recording control |
| **Transcription** | `client.getLiveTranscriptionClient()` | Live captions |
| **LiveStream** | `client.getLiveStreamClient()` | RTMP streaming |
| **Subsession** | `client.getSubsessionClient()` | Breakout rooms |
| **Whiteboard** | `client.getWhiteboardClient()` | Collaborative whiteboard |

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
await stream.stopAudio();
```

### Switch Devices

```javascript
// Get available devices
const cameras = stream.getCameraList();
const mics = stream.getMicList();
const speakers = stream.getSpeakerList();

// Switch devices
await stream.switchCamera(cameraId);
await stream.switchMicrophone(micId);
await stream.switchSpeaker(speakerId);
```

### Screen Sharing

```javascript
// Start sharing
await stream.startShareScreen(canvas);

// Stop sharing
await stream.stopShareScreen();

// Receive share
client.on('active-share-change', async (payload) => {
  if (payload.state === 'Active') {
    await stream.startShareView(canvas, payload.userId);
  } else {
    await stream.stopShareView();
  }
});
```

### Chat

```javascript
const chatClient = client.getChatClient();

// Send to everyone
await chatClient.send('Hello, everyone!');

// Send to specific user
await chatClient.sendToUser(userId, 'Private message');

// Receive messages
client.on('chat-on-message', (payload) => {
  console.log(`${payload.sender.name}: ${payload.message}`);
});
```

### Recording (Host Only)

```javascript
const recordingClient = client.getRecordingClient();

await recordingClient.startCloudRecording();
await recordingClient.stopCloudRecording();

client.on('recording-change', (payload) => {
  console.log('Recording status:', payload.state);
});
```

### Leave/End Session

```javascript
// Leave session (others stay)
await client.leave();

// End session for ALL participants (host only)
await client.leave(true);
```

## Error Handling

### Common Join Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Invalid signature` | JWT expired or malformed | Generate new signature |
| `Session does not exist` | Host hasn't started yet | Show "waiting" message, retry |
| `Permission denied` | User denied camera/mic | Request permission again |

### Example Error Handler

```javascript
try {
  await client.join(topic, signature, userName, password);
} catch (error) {
  if (error.reason?.includes('signature')) {
    // Regenerate signature and retry
  } else if (error.reason?.includes('Session')) {
    // Show "Waiting for host..." and poll
  } else if (error.reason?.includes('Permission')) {
    // Guide user to enable permissions
  }
  console.error('Join failed:', error);
}
```

## Browser Compatibility

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| Video | 80+ | 75+ | 14+ | 80+ |
| Audio | 80+ | 75+ | 14+ | 80+ |
| Screen Share | 80+ | 75+ | 15+ | 80+ |
| Virtual BG | 80+ | 90+ | - | 80+ |

**Safari Notes:**
- Virtual background not supported
- Screen sharing requires macOS 15+

## CORS Errors (Telemetry)

**CORS errors to `log-external-gateway.zoom.us` are harmless.**

These are caused by COOP/COEP headers blocking telemetry requests. They don't affect SDK functionality.

## Complete Documentation Library

### Core Concepts
- **[SDK Architecture Pattern](concepts/sdk-architecture-pattern.md)** - Universal 3-step pattern for ANY feature
- **[Singleton Hierarchy](concepts/singleton-hierarchy.md)** - 4-level navigation guide

### Complete Examples
- **[Session Join Pattern](examples/session-join-pattern.md)** - JWT auth + session join with full code
- **[Video Rendering](examples/video-rendering.md)** - attachVideo() patterns
- **[Screen Share](examples/screen-share.md)** - Send and receive screen shares
- **[Event Handling](examples/event-handling.md)** - Required events
- **[Chat](examples/chat.md)** - In-session messaging
- **[Recording](examples/recording.md)** - Cloud recording control
- **[Transcription](examples/transcription.md)** - Live captions

### Framework Integrations
- **[React Hooks](examples/react-hooks.md)** - Official @zoom/videosdk-react library
- **[Framework Integrations](examples/framework-integrations.md)** - Next.js, Vue/Nuxt patterns

### Troubleshooting
- **[Common Issues](troubleshooting/common-issues.md)** - Quick diagnostics & error codes

### References
- **[API Reference](references/web-reference.md)** - Complete method signatures
- **[Events Reference](references/events-reference.md)** - All event types
- **[INDEX.md](INDEX.md)** - Complete navigation guide

## Official Sample Repositories

| Type | Repository |
|------|------------|
| Web Sample | [videosdk-web-sample](https://github.com/zoom/videosdk-web-sample) |
| React SDK | [videosdk-react](https://github.com/zoom/videosdk-react) |
| Next.js | [videosdk-nextjs-quickstart](https://github.com/zoom/videosdk-nextjs-quickstart) |
| Vue/Nuxt | [videosdk-vue-nuxt-quickstart](https://github.com/zoom/videosdk-vue-nuxt-quickstart) |
| Auth Endpoint | [videosdk-auth-endpoint-sample](https://github.com/zoom/videosdk-auth-endpoint-sample) |
| UI Toolkit | [videosdk-zoom-ui-toolkit-react-sample](https://github.com/zoom/videosdk-zoom-ui-toolkit-react-sample) |

## Resources

- **Official Docs**: https://developers.zoom.us/docs/zoom-video-sdk/web/
- **API Reference**: https://marketplacefront.zoom.us/sdk/custom/web/modules.html
- **Dev Forum**: https://devforum.zoom.us/
- **GitHub Samples**: https://github.com/zoom/videosdk-web-sample

---

**Need help?** Start with [INDEX.md](INDEX.md) for complete navigation.

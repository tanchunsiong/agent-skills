---
name: zoom-video-sdk
description: |
  Zoom Video SDK for building custom video experiences (not Zoom meetings). Supports Web, 
  iOS, Android, macOS, Windows, and Linux. Use when you want full control over the video 
  UI and experience, or need raw audio/video data access.
---

# Zoom Video SDK

Build custom video experiences powered by Zoom's infrastructure.

## Meeting SDK vs Video SDK

| Feature | Meeting SDK | Video SDK |
|---------|-------------|-----------|
| UI | Default Zoom UI or Custom UI | **Fully custom UI** (you build it) |
| Experience | Zoom meetings | Video sessions |
| Branding | Limited customization | **Full branding control** |
| Features | Full Zoom features | Core video features |

## UI Options

Video SDK gives you **full control over the UI**:

| Option | Description |
|--------|-------------|
| **UI Toolkit** | Pre-built components (low-code) - Web, iOS, Android |
| **Custom UI** | Build your own UI using the SDK APIs |
| **Headless** | No UI - server-side processing (Linux, Windows, macOS) |

All platforms support custom UI. You render video to your own canvas/view elements.

## Prerequisites

- Zoom Video SDK credentials from Marketplace
- SDK Key and Secret
- Platform-specific development environment

## Choose Your Platform

| Platform | Use Case |
|----------|----------|
| **Web** | Browser-based custom video apps |
| **Electron** | Cross-platform desktop apps (Windows, macOS, Linux) |
| **iOS** | Custom video on iPhone/iPad |
| **Android** | Custom video on Android |
| **macOS** | Native desktop video apps for Mac |
| **Windows** | Native desktop video apps for Windows |
| **Linux** | Server-side video processing (headless) |

## Quick Start (Web)

### NPM Usage (Bundler like Vite/Webpack)

```javascript
import ZoomVideo from '@zoom/videosdk';

const client = ZoomVideo.createClient();
await client.init('en-US', 'Global', { patchJsMedia: true });
await client.join(topic, signature, userName, password);

// IMPORTANT: getMediaStream() ONLY works AFTER join()
const stream = client.getMediaStream();
await stream.startVideo();
await stream.startAudio();
```

### CDN Usage (No Bundler)

> **WARNING: Ad blockers block `source.zoom.us`**. Self-host the SDK to avoid issues.

```bash
# Download SDK locally
curl "https://source.zoom.us/videosdk/zoom-video-1.12.0.min.js" -o js/zoom-video-sdk.min.js
```

```html
<script src="js/zoom-video-sdk.min.js"></script>
```

```javascript
// CDN exports as WebVideoSDK, NOT ZoomVideo
// Must use .default property
const ZoomVideo = WebVideoSDK.default;
const client = ZoomVideo.createClient();

await client.init('en-US', 'Global', { patchJsMedia: true });
await client.join(topic, signature, userName, password);

// IMPORTANT: getMediaStream() ONLY works AFTER join()
const stream = client.getMediaStream();
await stream.startVideo();
await stream.startAudio();
```

### ES Module with CDN (Race Condition Fix)

When using `<script type="module">` with CDN, SDK may not be loaded yet:

```javascript
// Wait for SDK to load before using
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

// Usage
await waitForSDK();
const ZoomVideo = WebVideoSDK.default;
const client = ZoomVideo.createClient();
```

## SDK Lifecycle (CRITICAL ORDER)

The SDK has a strict lifecycle. Violating it causes silent failures.

```
1. Create client:     client = ZoomVideo.createClient()
2. Initialize:        await client.init('en-US', 'Global', options)
3. Join session:      await client.join(topic, signature, userName, password)
4. Get stream:        stream = client.getMediaStream()  ← ONLY AFTER JOIN
5. Start media:       await stream.startVideo() / await stream.startAudio()
```

**Common Mistake (Silent Failure):**

```javascript
// ❌ WRONG: Getting stream before joining
const client = ZoomVideo.createClient();
await client.init('en-US', 'Global');
const stream = client.getMediaStream();  // Returns undefined!
await client.join(...);

// ✅ CORRECT: Get stream after joining
const client = ZoomVideo.createClient();
await client.init('en-US', 'Global');
await client.join(...);
const stream = client.getMediaStream();  // Works!
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| Session | Video session (not a meeting) |
| Topic | Session identifier (any string you choose) |
| Signature | JWT for authorization |
| MediaStream | Audio/video stream control |

## Session Creation Model

**Important**: Video SDK sessions are created **just-in-time**, not in advance.

| Aspect | Video SDK | Meeting SDK |
|--------|-----------|-------------|
| Pre-creation | NOT required | Create meeting via API first |
| Session start | First participant joins with topic | Join existing meeting ID |
| Topic | Any string (you define it) | Meeting ID from API |
| Scheduling | N/A - sessions are ad-hoc | Meetings can be scheduled |

### How Sessions Work

1. **No pre-creation needed**: Sessions don't exist until someone joins
2. **Topic = Session ID**: Any participants joining with the same `topic` string join the same session
3. **First join creates it**: The session is created when the first participant joins
4. **No meeting ID**: There's no numeric meeting ID like in Zoom Meetings

```javascript
// Session is created on-the-fly when first user joins
// Any string can be the topic - it becomes the session identifier
await client.join('my-custom-session-123', signature, 'User Name');

// Other participants join the SAME session by using the SAME topic
await client.join('my-custom-session-123', signature, 'Another User');
```

### Practical Session Scenarios

**Scenario 1: Host joins first (creates session)**
```javascript
await client.join('math-101', hostSignature, 'Tutor');
// Session "math-101" is created, tutor is alone
```

**Scenario 2: Participant joins before host**
```javascript
await client.join('math-101', participantSignature, 'Student');
// Error: Session doesn't exist yet
// Solution: Show "Waiting for host..." and retry
```

**Scenario 3: Rejoin after disconnect**
```javascript
// Generate NEW signature (old one expired)
const newSignature = await fetchSignature(...);
await client.join('math-101', newSignature, 'User');
// Rejoins if session still active
```

### Signature Endpoint Setup

The signature endpoint must be accessible from your frontend without CORS issues.

**Option 1: Same-Origin Proxy (Recommended)**

```nginx
# Nginx config
location /api/ {
    proxy_pass http://localhost:3005/api/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
}
```

```javascript
// Frontend uses relative URL (same origin)
const response = await fetch('/api/signature', { ... });
```

**Option 2: CORS Configuration**

```javascript
// Express.js backend
const cors = require('cors');
app.use(cors({
  origin: ['https://your-domain.com'],
  credentials: true
}));
```

**WARNING:** Mixed content (HTTPS page → HTTP API) will be blocked by browsers.

### Exception: Create Session API (PSTN Dial-In)

The only exception is the **Create Session API**, which is used specifically for associating a session with a **dial-in phone number** (PSTN). This does NOT mean you must create sessions in advance for regular video sessions.

```javascript
// Only needed for PSTN dial-in support
// POST /v2/videosdk/sessions
const response = await fetch('https://api.zoom.us/v2/videosdk/sessions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    session_name: 'my-session',
    // This associates a dial-in number with the session
  })
});
```

**When to use Create Session API**:
- You need PSTN dial-in capability for your video session
- You want phone participants to join via a phone number

**When NOT needed**:
- Standard video-only sessions (just use `client.join()`)
- WebRTC-only participants

## Detailed References

### UI & Components
- **[references/ui-toolkit.md](references/ui-toolkit.md)** - Pre-built UI components (Web, iOS, Android)

### Platform Guides
- **[references/authorization.md](references/authorization.md)** - Video SDK JWT generation
- **[references/web.md](references/web.md)** - Web Video SDK
- **[references/electron.md](references/electron.md)** - Electron Video SDK (cross-platform desktop)
- **[references/ios.md](references/ios.md)** - iOS Video SDK
- **[references/android.md](references/android.md)** - Android Video SDK
- **[references/macos.md](references/macos.md)** - macOS Video SDK (native)
- **[references/windows.md](references/windows.md)** - Windows Video SDK (native)
- **[references/linux.md](references/linux.md)** - Linux Video SDK (headless)

## Sample Repositories

### Official (by Zoom)

| Platform | Repository | Stars |
|----------|------------|-------|
| Web | [videosdk-web-sample](https://github.com/zoom/videosdk-web-sample) | 137 |
| Web NPM | [videosdk-web](https://github.com/zoom/videosdk-web) | 56 |
| Auth | [videosdk-auth-endpoint-sample](https://github.com/zoom/videosdk-auth-endpoint-sample) | 23 |
| UI Toolkit Web | [videosdk-ui-toolkit-web](https://github.com/zoom/videosdk-ui-toolkit-web) | 17 |
| UI Toolkit React | [videosdk-ui-toolkit-react-sample](https://github.com/zoom/videosdk-ui-toolkit-react-sample) | 17 |
| Next.js | [videosdk-nextjs-quickstart](https://github.com/zoom/videosdk-nextjs-quickstart) | 16 |
| Telehealth | [VideoSDK-Web-Telehealth](https://github.com/zoom/VideoSDK-Web-Telehealth) | 11 |
| React Native | [videosdk-reactnative-quickstart](https://github.com/zoom/videosdk-reactnative-quickstart) | 10 |
| Linux Raw Recording | [videosdk-linux-raw-recording-sample](https://github.com/zoom/videosdk-linux-raw-recording-sample) | 9 |
| S3 Recordings | [videosdk-s3-cloud-recordings](https://github.com/zoom/videosdk-s3-cloud-recordings) | 8 |
| iOS | [videosdk-ios](https://github.com/zoom/videosdk-ios) | 7 |
| Flutter | [videosdk-flutter-quickstart](https://github.com/zoom/videosdk-flutter-quickstart) | 2 |
| Electron | [videosdk-electron-sample](https://github.com/zoom/videosdk-electron-sample) | 1 |

### Community / Extended

| Platform | Repository | Description |
|----------|------------|-------------|
| Windows .NET | [tanchunsiong/videosdk-windows-dotnet-desktop-framework-quickstart](https://github.com/tanchunsiong/videosdk-windows-dotnet-desktop-framework-quickstart) | C++/CLI wrapper for .NET |
| Linux Qt | [tanchunsiong/videosdk-linux-qt-quickstart](https://github.com/tanchunsiong/videosdk-linux-qt-quickstart) | Qt GUI integration |
| Linux GTK | [tanchunsiong/videosdk-linux-gtk-quickstart](https://github.com/tanchunsiong/videosdk-linux-gtk-quickstart) | GTK GUI integration |
| Windows Raw Data | [tanchunsiong/Zoom_VideoSDK_Windows_RawDataDemos](https://github.com/tanchunsiong/Zoom_VideoSDK_Windows_RawDataDemos) | Raw audio/video demos |

**Full list**: See [zoom-general/references/community-repos.md](../zoom-general/references/community-repos.md)

## Resources

- **Official docs**: https://developers.zoom.us/docs/video-sdk/
- **Developer forum**: https://devforum.zoom.us/

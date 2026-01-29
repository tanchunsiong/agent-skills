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
| **iOS** | Custom video on iPhone/iPad |
| **Android** | Custom video on Android |
| **macOS** | Desktop video apps for Mac |
| **Windows** | Desktop video apps for Windows |
| **Linux** | Server-side video processing |

## Quick Start (Web)

```javascript
import ZoomVideo from '@zoom/videosdk';

const client = ZoomVideo.createClient();

await client.init('en-US', 'CDN');

await client.join(topic, signature, userName, password);

const stream = client.getMediaStream();
await stream.startVideo();
await stream.startAudio();
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
- **[references/ios.md](references/ios.md)** - iOS Video SDK
- **[references/android.md](references/android.md)** - Android Video SDK
- **[references/macos.md](references/macos.md)** - macOS Video SDK
- **[references/windows.md](references/windows.md)** - Windows Video SDK
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

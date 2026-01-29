---
name: zoom-meeting-sdk
description: |
  Zoom Meeting SDK for embedding Zoom meetings into your application. Supports Web, iOS, 
  Android, macOS, Windows, and Linux platforms. Use when you want to integrate the full 
  Zoom meeting experience into your app or build meeting bots.
---

# Zoom Meeting SDK

Embed the full Zoom meeting experience into your application.

## Prerequisites

- Zoom app with Meeting SDK credentials
- SDK Key and Secret from Marketplace
- Platform-specific development environment

## Choose Your Platform

| Platform | Use Case |
|----------|----------|
| **Web** | Browser-based apps (Component or Client View) |
| **iOS** | iPhone/iPad apps |
| **Android** | Android apps |
| **macOS** | Mac desktop apps |
| **Windows** | Windows desktop apps |
| **C#/.NET** | Windows apps with .NET (WPF, WinForms) |
| **Linux** | Meeting bots, server-side processing |
| **Electron** | Cross-platform desktop apps |
| **React Native** | Cross-platform mobile apps |
| **Unreal Engine** | Game/VR integrations |

## Quick Start (Web)

```html
<script src="https://source.zoom.us/2.18.0/lib/vendor/react.min.js"></script>
<script src="https://source.zoom.us/2.18.0/lib/vendor/react-dom.min.js"></script>
<script src="https://source.zoom.us/2.18.0/lib/vendor/redux.min.js"></script>
<script src="https://source.zoom.us/2.18.0/lib/vendor/redux-thunk.min.js"></script>
<script src="https://source.zoom.us/2.18.0/lib/vendor/lodash.min.js"></script>
<script src="https://source.zoom.us/zoom-meeting-2.18.0.min.js"></script>

<script>
const client = ZoomMtgEmbedded.createClient();

client.init({
  zoomAppRoot: document.getElementById('meetingSDKElement'),
  language: 'en-US',
});

client.join({
  sdkKey: 'YOUR_SDK_KEY',
  signature: 'YOUR_SIGNATURE',
  meetingNumber: 'MEETING_NUMBER',
  userName: 'User Name',
});
</script>
```

## UI Options

Meeting SDK provides **Zoom's UI with customization options**:

| Platform | UI Options |
|----------|------------|
| **Web** | Component View (customizable) or Client View (full-page Zoom) |
| **iOS/Android** | Default Zoom UI with Custom UI layer option |
| **Windows/macOS** | Default Zoom UI with Custom UI layer option |
| **Linux** | **Headless** - no UI, for bots/server-side (you can add your own GUI) |

**Note**: Unlike Video SDK where you build the UI from scratch, Meeting SDK uses Zoom's UI as the base with customization on top.

## Key Concepts

| Concept | Description |
|---------|-------------|
| SDK Key/Secret | Credentials from Marketplace |
| Signature | JWT signed with SDK Secret |
| Component View | Extractable, customizable UI (Web) |
| Client View | Full-page Zoom UI (Web) |
| Custom UI Layer | Add your UI on top of Zoom's UI (Mobile/Desktop) |
| Headless | No UI - server-side processing (Linux) |
| Raw Data | Direct audio/video access (Desktop) |

## Detailed References

### Platform Guides
- **[references/web.md](references/web.md)** - Web SDK (Component + Client View)
- **[references/ios.md](references/ios.md)** - iOS SDK
- **[references/android.md](references/android.md)** - Android SDK
- **[references/macos.md](references/macos.md)** - macOS SDK
- **[references/windows.md](references/windows.md)** - Windows SDK
- **[references/csharp.md](references/csharp.md)** - C#/.NET wrapper for Windows
- **[references/linux.md](references/linux.md)** - Linux SDK (headless/bots)
- **[references/electron.md](references/electron.md)** - Electron cross-platform desktop
- **[references/react-native.md](references/react-native.md)** - React Native mobile
- **[references/unreal-engine.md](references/unreal-engine.md)** - Unreal Engine integration

### Features
- **[references/authorization.md](references/authorization.md)** - SDK JWT generation
- **[references/bot-authentication.md](references/bot-authentication.md)** - ZAK vs OBF vs JWT tokens for bots
- **[references/breakout-rooms.md](references/breakout-rooms.md)** - Programmatic breakout room management
- **[references/ai-companion.md](references/ai-companion.md)** - AI Companion controls in meetings
- **[references/troubleshooting.md](references/troubleshooting.md)** - Common issues and solutions

## Sample Repositories

### Official (by Zoom)

| Platform | Repository | Stars |
|----------|------------|-------|
| Web | [meetingsdk-web-sample](https://github.com/zoom/meetingsdk-web-sample) | 643 |
| Web NPM | [meetingsdk-web](https://github.com/zoom/meetingsdk-web) | 324 |
| React | [meetingsdk-react-sample](https://github.com/zoom/meetingsdk-react-sample) | 177 |
| Auth | [meetingsdk-auth-endpoint-sample](https://github.com/zoom/meetingsdk-auth-endpoint-sample) | 124 |
| iOS | [zoom-sdk-ios](https://github.com/zoom/zoom-sdk-ios) | 179 |
| Android | [zoom-sdk-android](https://github.com/zoom/zoom-sdk-android) | 159 |
| Windows | [zoom-sdk-windows](https://github.com/zoom/zoom-sdk-windows) | 108 |
| Electron | [zoom-sdk-electron](https://github.com/zoom/zoom-sdk-electron) | 97 |
| macOS | [zoom-sdk-macos](https://github.com/zoom/zoom-sdk-macos) | 70 |
| Angular | [meetingsdk-angular-sample](https://github.com/zoom/meetingsdk-angular-sample) | 60 |
| C# Wrapper | [zoom-c-sharp-wrapper](https://github.com/zoom/zoom-c-sharp-wrapper) | 44 |
| Vue.js | [meetingsdk-vuejs-sample](https://github.com/zoom/meetingsdk-vuejs-sample) | 42 |
| Headless Linux | [meetingsdk-headless-linux-sample](https://github.com/zoom/meetingsdk-headless-linux-sample) | 3 |

### Community

| Platform | Repository | Description |
|----------|------------|-------------|
| React Native | [nagarro-dv/react-native-zoom-us-bridge](https://github.com/nagarro-dv/react-native-zoom-us-bridge) | iOS + Android bridge |
| Flutter | [ark-brighthustle/flutter_zoom_sdk](https://github.com/ark-brighthustle/flutter_zoom_sdk) | Flutter plugin with Null Safety |
| Python | [noah-duncan/py-zoom-meeting-sdk](https://github.com/noah-duncan/py-zoom-meeting-sdk) | Python bindings |
| .NET/MAUI | [AdamDiament/dotnet-zoom-meeting-SDK](https://github.com/AdamDiament/dotnet-zoom-meeting-SDK) | .NET/MAUI/Xamarin binding |
| Windows Raw Data | [tanchunsiong/Zoom_MeetingSDK_Windows_RawDataDemos](https://github.com/tanchunsiong/Zoom_MeetingSDK_Windows_RawDataDemos) | Raw audio/video access |

**Full list**: See [zoom-general/references/community-repos.md](../zoom-general/references/community-repos.md)

## Resources

- **Official docs**: https://developers.zoom.us/docs/meeting-sdk/
- **Developer forum**: https://devforum.zoom.us/

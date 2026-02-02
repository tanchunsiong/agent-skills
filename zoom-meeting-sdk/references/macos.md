# Meeting SDK - macOS

Desktop meeting applications on Mac with raw data access.

## Overview

macOS SDK for embedding Zoom meetings with UI customization and raw audio/video data access.

## Prerequisites

- Meeting SDK downloaded from [Marketplace](https://marketplace.zoom.us/) (sign-in required)
- Xcode 13+
- macOS 10.13+
- Valid SDK credentials

## Installation

1. Download SDK from Marketplace (requires sign-in)
2. Add `ZoomSDK.framework` to your project
3. Configure entitlements for camera/microphone

## Quick Start

```swift
import ZoomSDK

// Initialize
let initParams = ZoomSDKInitParams()
initParams.zoomDomain = "zoom.us"
ZoomSDK.shared().initSDK(with: initParams)

// Auth and join
let authService = ZoomSDK.shared().getAuthService()
authService?.sdkAuth(SDK_KEY, appSecret: SDK_SECRET)
```

## Raw Recording / Raw Data Access

Access raw audio and video frames:

```swift
// Get raw data controller
let rawDataCtrl = meetingService.getRawDataController()

// Subscribe to raw data
rawDataCtrl?.subscribeAudioRawData(audioDelegate)
rawDataCtrl?.subscribeVideoRawData(videoDelegate, forUser: userId)
```

## Common Tasks

### NSView Integration

```swift
// Get the meeting video view
let videoView = meetingService?.getMeetingVideoController()?.getVideoView()

// Add to your NSView hierarchy
yourContainerView.addSubview(videoView!)
videoView?.frame = yourContainerView.bounds
videoView?.autoresizingMask = [.width, .height]
```

### UI Customization

**Default UI (Zoom's built-in interface)**:
```swift
// Control default UI elements
let uiController = meetingService?.getMeetingUIController()
uiController?.showChatDialog()
uiController?.hideChatDialog()
uiController?.enterFullScreen()
uiController?.switchToVideoWall()
```

**Custom UI**:
- Set `needCustomizedUI = true` in `ZoomSDKInitParams`
- You must implement ALL UI elements yourself

### Audio/Video Controls

```swift
// Get audio controller
let audioCtrl = meetingService?.getInMeetingAudioController()

// Mute/unmute
audioCtrl?.muteAudio()
audioCtrl?.unmuteAudio()

// Get video controller
let videoCtrl = meetingService?.getInMeetingVideoController()

// Start/stop video
videoCtrl?.stopVideo()
videoCtrl?.startVideo()
```

### Raw Audio Processing

```swift
class AudioDelegate: NSObject, ZoomSDKAudioRawDataDelegate {
    func onMixedAudioRawDataReceived(_ data: ZoomSDKAudioRawData) {
        // Access PCM audio data
        let buffer = data.getBuffer()
        let length = data.getBufferLen()
        let sampleRate = data.getSampleRate()
        // Format: 16-bit PCM, mono
    }
}

// Subscribe
let rawDataCtrl = ZoomSDK.shared().getRawDataController()
rawDataCtrl?.subscribeAudioRawData(audioDelegate)
```

### Raw Video Processing

```swift
class VideoDelegate: NSObject, ZoomSDKRendererDelegate {
    func onRawDataFrameReceived(_ data: ZoomSDKYUVRawDataI420) {
        // Access YUV frame data
        let width = data.getStreamWidth()
        let height = data.getStreamHeight()
        let buffer = data.getBuffer()
    }
}

// Subscribe to specific user's video
rawDataCtrl?.subscribeVideoRawData(videoDelegate, forUser: userId)
```

## App Store Limitations

**CRITICAL**: Zoom Meeting SDK for macOS **CANNOT** be submitted to the Mac App Store because it includes unsigned helper apps that require entitlements not allowed by Apple:

```
Error: The App sandbox not enabled. The following executables must include 
the "com.apple.security.app-sandbox" entitlement:
- SDK_Transcode.app/Contents/MacOS/SDK_Transcode
- airhost.app/Contents/MacOS/airhost  
- aomhost.app/Contents/MacOS/aomhost
```

**Solution**: Distribute outside the App Store via direct download.

| Aspect | App Store | Direct Distribution |
|--------|------------|-------------------|
| **Sandboxing** | Required (SDK incompatible) | Not required |
| **Notarization** | Not required | Required for Gatekeeper |
| **Code Signing** | Apple Developer ID | Apple Developer ID |

## Notarization (Required for Direct Distribution)

```bash
# Code sign all .app bundles in SDK
codesign --force --verify --timestamp --verbose \
    --options=runtime \
    --sign "Developer ID Application: Your Name (Team ID)" \
    ZoomSDK/*.app

# Notarize
xcrun notarytool submit YourApp.zip \
    --apple-id "your@email.com" \
    --password "app-specific-password" \
    --team-id "Team ID" \
    --wait
```

## Accessibility Permissions

Required permissions in `Info.plist`:

```xml
<key>NSCameraUsageDescription</key>
<string>Need camera access for video meetings</string>

<key>NSMicrophoneUsageDescription</key>
<string>Need microphone access for audio meetings</string>

<key>NSScreenCaptureDescription</key>
<string>Need screen access for screen sharing</string>
```

**User must grant permissions** in System Settings > Privacy & Security:
- Camera
- Microphone
- Screen Recording

## Resources

- **macOS docs**: https://developers.zoom.us/docs/meeting-sdk/macos/
- **API Reference**: https://marketplacefront.zoom.us/sdk/meeting/macos/

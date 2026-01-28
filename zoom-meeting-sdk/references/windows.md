# Meeting SDK - Windows

Desktop meeting applications on Windows with raw data access.

## Overview

Windows SDK for embedding Zoom meetings with full UI customization and raw audio/video data access.

## Prerequisites

- Meeting SDK downloaded from [Marketplace](https://marketplace.zoom.us/) (sign-in required)
- Visual Studio 2017+
- Windows 10+
- Valid SDK credentials

## Installation

1. Download SDK from Marketplace (requires sign-in)
2. Add SDK headers and libraries to your project
3. Configure linker settings

## Quick Start

```cpp
#include "zoom_sdk.h"

// Initialize
ZOOM_SDK_NAMESPACE::InitParam initParam;
initParam.strWebDomain = L"zoom.us";
ZOOM_SDK_NAMESPACE::SDKError err = ZOOM_SDK_NAMESPACE::InitSDK(initParam);

// Auth
ZOOM_SDK_NAMESPACE::AuthParam authParam;
authParam.appKey = SDK_KEY;
authParam.appSecret = SDK_SECRET;
```

## Raw Recording / Raw Data Access

Access raw audio and video frames:

### Subscribe to Raw Data

```cpp
// Get raw data controller
auto rawDataCtrl = meetingService->GetMeetingRawDataController();

// Subscribe to audio
rawDataCtrl->SubscribeAudioRawData(audioDelegate);

// Subscribe to video
rawDataCtrl->SubscribeVideoRawData(videoDelegate, participantId);
```

## Common Tasks

### UI Customization - Default UI vs Custom UI

**Default UI (Zoom's built-in interface)**:
```cpp
// Use IMeetingUIController to control default UI elements
IMeetingUIController* pUIController = pMeetingService->GetMeetingUIController();
pUIController->EnterFullScreen(true, false);  // Enter fullscreen
pUIController->ShowChatDlg(param);            // Show chat dialog
pUIController->HideChatDlg();                 // Hide chat dialog
pUIController->SwitchToVideoWall();           // Switch to gallery view
pUIController->BackToMeeting();               // Return to active speaker
```

**Custom UI**:
- Requires `needCustomizedUI = true` in `InitParam`
- You must implement ALL UI elements yourself
- More complex but fully customizable

### Audio/Video Controls

```cpp
// Get audio controller
auto audioCtrl = pMeetingService->GetMeetingAudioController();

// Mute/unmute self
audioCtrl->MuteAudio(GetMyUserID(), true);   // Mute
audioCtrl->UnMuteAudio(GetMyUserID());       // Unmute

// Get video controller
auto videoCtrl = pMeetingService->GetMeetingVideoController();

// Start/stop video
videoCtrl->MuteVideo();    // Stop video
videoCtrl->UnmuteVideo();  // Start video
```

### Raw Audio Processing

```cpp
class AudioRawDataDelegate : public IZoomSDKAudioRawDataDelegate {
public:
    void onMixedAudioRawDataReceived(AudioRawData* data) override {
        // Access mixed audio from all participants
        const char* buffer = data->GetBuffer();
        uint32_t length = data->GetBufferLen();
        uint32_t sampleRate = data->GetSampleRate();  // 16kHz or 32kHz
        // Format: 16-bit PCM, mono
    }

    void onOneWayAudioRawDataReceived(AudioRawData* data, uint32_t node_id) override {
        // Access individual participant audio
    }
};

// Subscribe to audio
auto* pRawDataHelper = GetAudioRawdataHelper();
pRawDataHelper->subscribe(new AudioRawDataDelegate());
```

### Raw Video Processing

```cpp
class VideoRawDataDelegate : public IZoomSDKRendererDelegate {
public:
    void onRawDataFrameReceived(YUVRawDataI420* data) override {
        // Access video frame in I420/YUV format
        uint32_t width = data->GetStreamWidth();
        uint32_t height = data->GetStreamHeight();
        const char* buffer = data->GetBuffer();
        uint32_t bufferLen = data->GetBufferLen();
    }
};

// Subscribe to video
auto* pVideoHelper = GetRawdataRendererHelper();
pVideoHelper->setRawDataResolution(ZoomSDKResolution_720P);
pVideoHelper->subscribe(userId, RAW_DATA_TYPE_VIDEO, new VideoRawDataDelegate());
```

## Common Issues & Gotchas

### DLL Not Found Error

**Problem**: `sdk.dll not found on fresh runtime folder`

**Solution**: Copy ALL files from SDK's `x64\bin` to your output directory:
```
From: zoom-sdk\SDK\x64\bin\*
To:   your-project\x64\Release\ (or Debug)
```

### "DLL from Unknown Publisher" Warning

**Registry workaround** (not guaranteed):
```
[HKEY_LOCAL_MACHINE\SOFTWARE\Zoom\SDK]
"Disable3rdModuleVerify"=dword:00000001
```

**Better solution**: Code sign your application properly.

### Common Error Codes

| Error Code | Meaning | Common Cause |
|------------|---------|--------------|
| **8** | SDK not authorized | Missing or invalid JWT/ZAK token |
| **100000400** | Meeting join failed | Incorrect meeting number, password, or permissions |
| **SDKERR_UNINITIALIZE** | SDK not initialized | `InitSDK()` not called or failed |
| **AUTHRET_JWTTOKENWRONG** | JWT invalid | Expired or malformed JWT token |

## Resources

- **Windows docs**: https://developers.zoom.us/docs/meeting-sdk/windows/
- **API Reference**: https://marketplacefront.zoom.us/sdk/meeting/windows/

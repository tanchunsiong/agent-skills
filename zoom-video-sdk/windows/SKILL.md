---
name: zoom-video-sdk/windows
description: "Zoom Video SDK for Windows - C++ integration for video sessions, raw audio/video capture, screen sharing, recording, and real-time communication"
---

# Zoom Video SDK - Windows Development

Expert guidance for developing with the Zoom Video SDK on Windows. This SDK enables custom video applications, raw media capture/injection, cloud recording, live streaming, and real-time transcription on Windows platforms.

**Official Documentation**: https://developers.zoom.us/docs/video-sdk/windows/
**API Reference**: https://marketplacefront.zoom.us/sdk/custom/windows/
**Sample Repository**: https://github.com/zoom/videosdk-windows-rawdata-sample

## Quick Links

- **[Getting Started Guide](getting-started.md)** - Setup, prerequisites, and first session
- **[Implementation Guide](implementation.md)** - Core patterns, raw data, and helpers
- **[C# Integration](csharp-integration.md)** - C++/CLI wrapper for .NET applications
- **[API Reference](../references/windows-reference.md)** - Complete API documentation
- **[Samples](samples.md)** - Official sample applications reference

## SDK Overview

The Zoom Video SDK for Windows is a C++ library that provides:
- **Session Management**: Join/leave video SDK sessions
- **Raw Data Access**: Capture raw audio/video frames (YUV420, PCM)
- **Raw Data Injection**: Send custom audio/video into sessions
- **Screen Sharing**: Share screens or inject custom share sources
- **Cloud Recording**: Record sessions to Zoom cloud
- **Live Streaming**: Stream to RTMP endpoints (YouTube, etc.)
- **Chat & Commands**: In-session messaging and command channels
- **Live Transcription**: Real-time speech-to-text
- **Subsessions**: Breakout room support
- **Whiteboard**: Collaborative whiteboard features
- **Annotations**: Screen share annotations
- **C# Integration**: C++/CLI wrapper for .NET applications

## Prerequisites

### System Requirements

- **OS**: Windows 10 (1903 or later) or Windows 11
- **Architecture**: x64 (recommended), x86, or ARM64
- **Visual Studio**: 2019 or 2022 (Community, Professional, or Enterprise)
- **Windows SDK**: 10.0.19041.0 or later
- **.NET Framework**: 4.8 or later (for C# applications)

### Visual Studio Workloads

Install these workloads via Visual Studio Installer:

1. **Desktop development with C++**
   - MSVC v142 or v143 compiler
   - Windows 10/11 SDK
   - C++ CMake tools (optional)

2. **.NET desktop development** (for C# applications)
   - .NET Framework 4.8 targeting pack
   - C++/CLI support

## Quick Start

### C++ Application

```cpp
#include <windows.h>
#include "zoom_video_sdk_api.h"
#include "zoom_video_sdk_interface.h"
#include "zoom_video_sdk_delegate_interface.h"

USING_ZOOM_VIDEO_SDK_NAMESPACE

// 1. Create SDK object
IZoomVideoSDK* video_sdk_obj = CreateZoomVideoSDKObj();

// 2. Initialize
ZoomVideoSDKInitParams init_params;
init_params.domain = L"https://zoom.us";
init_params.enableLog = true;
init_params.logFilePrefix = L"zoom_win_video";
init_params.videoRawDataMemoryMode = ZoomVideoSDKRawDataMemoryModeHeap;
init_params.shareRawDataMemoryMode = ZoomVideoSDKRawDataMemoryModeHeap;
init_params.audioRawDataMemoryMode = ZoomVideoSDKRawDataMemoryModeHeap;

ZoomVideoSDKErrors err = video_sdk_obj->initialize(init_params);

// 3. Add event listener
video_sdk_obj->addListener(myDelegate);

// 4. Join session (IMPORTANT: set audioOption.connect = false)
ZoomVideoSDKSessionContext session_context;
session_context.sessionName = L"my-session";
session_context.userName = L"Windows User";
session_context.token = L"your-jwt-token";
session_context.videoOption.localVideoOn = false;
session_context.audioOption.connect = false;  // Connect audio after join
session_context.audioOption.mute = true;

IZoomVideoSDKSession* session = video_sdk_obj->joinSession(session_context);

// 5. CRITICAL: Add Windows message pump for callbacks to work
bool running = true;
while (running) {
    // Process Windows messages (required for SDK callbacks)
    MSG msg;
    while (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    
    // Your application logic here
    Sleep(10);
}
```

### C# Application

```csharp
using ZoomVideoSDK;

var sdkManager = new ZoomSDKManager();
sdkManager.Initialize();
sdkManager.JoinSession("my-session", "jwt-token", "User Name", "");
```

## Documentation Structure

### Getting Started
- [getting-started.md](getting-started.md) - Installation, setup, configuration

### Implementation Guides
- [implementation.md](implementation.md) - Core patterns and best practices
- [raw-data.md](raw-data.md) - Raw audio/video capture and injection
- [helpers.md](helpers.md) - Audio, video, chat, recording helpers

### Integration
- [csharp-integration.md](csharp-integration.md) - C++/CLI wrapper for .NET

### Reference
- [samples.md](samples.md) - Official sample applications
- [troubleshooting.md](troubleshooting.md) - Common issues and solutions
- [../references/windows-reference.md](../references/windows-reference.md) - Complete API reference

## Key Features

| Feature | Description |
|---------|-------------|
| **Session Management** | Join, leave, and manage video sessions |
| **Raw Video (YUV I420)** | Capture and inject raw video frames |
| **Raw Audio (PCM)** | Capture and inject raw audio data |
| **Screen Sharing** | Share screens or custom content |
| **Cloud Recording** | Record sessions to Zoom cloud |
| **Live Streaming** | Stream to RTMP endpoints |
| **Chat** | Send/receive chat messages |
| **Command Channel** | Custom command messaging |
| **Live Transcription** | Real-time speech-to-text |
| **C# Support** | Full .NET Framework integration |

## Sample Applications

Located in local codebase:
- `C:\tempsdk\Zoom_VideoSDK_Windows_RawDataDemos\` - C++ raw data demos
- `C:\tempsdk\videosdk-windows-dotnet-desktop-framework-quickstart\` - C# integration demos
- `C:\tempsdk\sdksamples\zoom-video-sdk-windows-2.4.12\` - Official SDK 2.4.12 samples

## Critical Gotchas and Best Practices

### ⚠️ CRITICAL: Windows Message Pump Required

**The #1 issue that causes session joins to hang with no callbacks:**

All Windows applications using the Zoom SDK **MUST** process Windows messages. The SDK uses Windows messages to deliver callbacks like `onSessionJoin()`, `onError()`, etc.

**Problem**: Without a message pump, `joinSession()` appears to succeed but callbacks never fire.

**Solution**: Add this to your main loop:

```cpp
while (running) {
    // REQUIRED: Process Windows messages
    MSG msg;
    while (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    
    // Your application logic
    Sleep(10);
}
```

**Applies to**:
- Console applications (no automatic message pump)
- Custom main loops
- Applications that don't use standard WinMain/WndProc

**GUI applications** using WinMain with standard message loop already have this.

### Audio Connection Strategy

**Best Practice**: Set `audioOption.connect = false` when joining, then connect audio in the `onSessionJoin()` callback.

```cpp
// During join
session_context.audioOption.connect = false;  // Don't connect yet
session_context.audioOption.mute = true;

// In onSessionJoin() callback
void onSessionJoin() override {
    IZoomVideoSDKAudioHelper* audioHelper = video_sdk_obj->getAudioHelper();
    if (audioHelper) {
        audioHelper->startAudio();  // Connect now
    }
}
```

**Why**: This pattern is used in all official Zoom samples. It separates session join from audio initialization for better reliability and error handling.

### All Delegate Callbacks Must Be Implemented

The `IZoomVideoSDKDelegate` interface has 70+ pure virtual methods. **ALL must be implemented**, even if empty:

```cpp
// Required even if you don't use them
void onProxyDetectComplete() override {}
void onUserWhiteboardShareStatusChanged(IZoomVideoSDKUser*, IZoomVideoSDKWhiteboardHelper*) override {}
// ... etc
```

**Tip**: Check the SDK version's `zoom_video_sdk_delegate_interface.h` for the complete list. The interface changes between SDK versions.

### Memory Mode for Raw Data

Always use heap mode for raw data memory:

```cpp
init_params.videoRawDataMemoryMode = ZoomVideoSDKRawDataMemoryModeHeap;
init_params.shareRawDataMemoryMode = ZoomVideoSDKRawDataMemoryModeHeap;
init_params.audioRawDataMemoryMode = ZoomVideoSDKRawDataMemoryModeHeap;
```

Stack mode can cause issues with large video frames.

### Thread Safety

SDK callbacks execute on SDK threads, not your main thread:
- Don't perform heavy operations in callbacks
- Don't call `cleanup()` from within callbacks
- Use thread-safe queues for passing data to UI thread
- Use mutexes when accessing shared state

### Consult Official Samples First

When SDK behavior is unexpected, **always check the official samples** before troubleshooting:

**Local samples**:
- `C:\tempsdk\Zoom_VideoSDK_Windows_RawDataDemos\VSDK_SkeletonDemo\` (simplest)
- `C:\tempsdk\sdksamples\zoom-video-sdk-windows-2.4.12\Sample-Libs\x64\demo\`

Official samples show correct patterns for:
- Message pump implementation ✓
- Audio connection strategy ✓
- Error handling ✓
- Memory management ✓

## Resources

- **Official Docs**: https://developers.zoom.us/docs/video-sdk/windows/
- **API Reference**: https://marketplacefront.zoom.us/sdk/custom/windows/
- **Dev Forum**: https://devforum.zoom.us/
- **GitHub Samples**: https://github.com/zoom/videosdk-windows-rawdata-sample
- **Working Sample**: `C:\tempsdk\zoom-video-sdk-windows-sample\` (complete implementation)

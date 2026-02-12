---
name: zoom-video-sdk/linux
description: "Zoom Video SDK for Linux - C++ headless bots, raw audio/video capture/injection, Qt/GTK integration, Docker support"
triggers:
- linux video sdk
- zoom linux
- headless bot
- raw data linux
- qt zoom
- gtk zoom
- virtual audio linux
---

# Zoom Video SDK - Linux Development

Expert guidance for developing with the Zoom Video SDK on Linux. Build headless bots, raw media capture/injection applications, and custom UI integrations with Qt/GTK.

**Official Documentation**: https://developers.zoom.us/docs/video-sdk/linux/
**API Reference**: https://marketplacefront.zoom.us/sdk/custom/linux/
**Sample Repository**: https://github.com/zoom/videosdk-linux-raw-recording-sample

## Quick Links

**New to Video SDK? Follow this path:**

1. **[SDK Architecture Pattern](concepts/sdk-architecture-pattern.md)** - Universal 3-step pattern for ANY feature
2. **[Session Join Pattern](examples/session-join-pattern.md)** - Complete working code to join a session
3. **[Raw Data vs Canvas](concepts/raw-data-vs-canvas.md)** - **CRITICAL**: Linux has NO Canvas API - raw data ONLY
4. **[Raw Video Capture](examples/raw-video-capture.md)** - Capture and process YUV420 frames

**Reference:**
- **[Singleton Hierarchy](concepts/singleton-hierarchy.md)** - 5-level SDK navigation map
- **[API Reference](references/linux-reference.md)** - Complete API documentation
- **[Qt/GTK Integration](examples/qt-gtk-integration.md)** - UI framework patterns
- **[Troubleshooting](troubleshooting/common-issues.md)** - Quick diagnostics

**Having issues?**
- PulseAudio setup → [PulseAudio Guide](troubleshooting/pulseaudio-setup.md)
- Qt dependencies → [Qt Dependencies](troubleshooting/qt-dependencies.md)
- Build errors → [Build Errors Guide](troubleshooting/build-errors.md)

## Key Differences from Windows/macOS

| Feature | Linux | Windows/Mac |
|---------|-------|-------------|
| **Canvas API** | ❌ Not available | ✅ Available |
| **Raw Data Pipe** | ✅ **ONLY option** | ✅ Available |
| **UI Integration** | Qt, GTK, SDL2, OpenGL | Win32/WinForms/WPF, Cocoa |
| **Headless Support** | ✅ Excellent (Docker) | Limited |
| **Audio** | PulseAudio required | Native |
| **Virtual Devices** | ✅ Required for headless | Optional |

## SDK Overview

The Zoom Video SDK for Linux is a C++ library optimized for:
- **Headless Bots**: Docker/WSL support, no display required
- **Raw Data Access**: Capture YUV420 video, PCM audio
- **Raw Data Injection**: Virtual camera/mic for custom media
- **Screen Sharing**: Capture or inject share data
- **Cloud Recording**: Record sessions to Zoom cloud
- **Live Streaming**: Stream to RTMP endpoints
- **Live Transcription**: Real-time speech-to-text
- **Qt/GTK Integration**: Full UI framework support

## Prerequisites

### System Requirements

- **OS**: Ubuntu 20.04+, Debian 11+, or compatible
- **Architecture**: x64 (recommended), ARM64
- **Compiler**: GCC 9+, Clang 10+
- **CMake**: 3.14 or later
- **Qt5**: Bundled with SDK (do NOT install system Qt5)

### Dependencies

```bash
sudo apt update
sudo apt install -y build-essential gcc cmake libglib2.0-dev liblzma-dev \
    libxcb-image0 libxcb-keysyms1 libxcb-xfixes0 libxcb-xkb1 libxcb-shape0 \
    libxcb-shm0 libxcb-randr0 libxcb-xtest0 libgbm1 libxtst6 libgl1 libnss3 \
    libasound2 libpulse0

# For headless Linux
sudo apt install -y pulseaudio

# PulseAudio configuration (CRITICAL for audio)
mkdir -p ~/.config
echo "[General]" > ~/.config/zoomus.conf
echo "system.audio.type=default" >> ~/.config/zoomus.conf

# Log directory
mkdir -p ~/.zoom/logs
```

## Quick Start

```cpp
#include "zoom_video_sdk_api.h"
#include "zoom_video_sdk_interface.h"
#include "zoom_video_sdk_delegate_interface.h"

USING_ZOOM_VIDEO_SDK_NAMESPACE

// 1. Create SDK
IZoomVideoSDK* sdk = CreateZoomVideoSDKObj();

// 2. Initialize
ZoomVideoSDKInitParams init_params;
init_params.domain = "https://zoom.us";
init_params.enableLog = true;
init_params.logFilePrefix = "bot";
init_params.videoRawDataMemoryMode = ZoomVideoSDKRawDataMemoryModeHeap;
init_params.shareRawDataMemoryMode = ZoomVideoSDKRawDataMemoryModeHeap;
init_params.audioRawDataMemoryMode = ZoomVideoSDKRawDataMemoryModeHeap;

sdk->initialize(init_params);

// 3. Add delegate
sdk->addListener(myDelegate);

// 4. Join session
ZoomVideoSDKSessionContext ctx;
ctx.sessionName = "my-session";
ctx.userName = "Linux Bot";
ctx.token = "jwt-token";
ctx.audioOption.connect = true;
ctx.audioOption.mute = false;
ctx.videoOption.localVideoOn = false;

// For headless: Virtual audio speaker
ctx.virtualAudioSpeaker = new VirtualSpeaker();

IZoomVideoSDKSession* session = sdk->joinSession(ctx);
```

See **[Session Join Pattern](examples/session-join-pattern.md)** for complete code.

## Key Features

| Feature | Linux Support | Guide |
|---------|---------------|-------|
| **Session Management** | ✅ Full | [Session Join](examples/session-join-pattern.md) |
| **Raw Video (YUV420)** | ✅ ONLY rendering option | [Raw Video](examples/raw-video-capture.md) |
| **Raw Audio (PCM)** | ✅ Full | [Raw Audio](examples/raw-audio-capture.md) |
| **Virtual Camera/Mic** | ✅ Full | [Virtual Devices](examples/virtual-audio-video.md) |
| **Cloud Recording** | ✅ Full | [Recording](examples/cloud-recording.md) |
| **Live Streaming** | ✅ Full | [Live Stream](examples/live-streaming.md) |
| **Live Transcription** | ✅ Full | [Transcription](examples/transcription.md) |
| **Command Channel** | ✅ Full | [Commands](examples/command-channel.md) |
| **Chat** | ✅ Full | [Chat](examples/chat.md) |
| **Qt Integration** | ✅ Recommended | [Qt/GTK](examples/qt-gtk-integration.md) |
| **GTK Integration** | ✅ Supported | [Qt/GTK](examples/qt-gtk-integration.md) |
| **Docker/Headless** | ✅ Excellent | [Virtual Devices](examples/virtual-audio-video.md) |

## Critical Gotchas

### ⚠️ CRITICAL #1: No Canvas API on Linux

**Problem**: Linux SDK does NOT have Canvas API like Windows/Mac.

**Solution**: You MUST use Raw Data Pipe and implement your own rendering.

See: **[Raw Data vs Canvas](concepts/raw-data-vs-canvas.md)**

### ⚠️ CRITICAL #2: PulseAudio Required for Audio

**Problem**: SDK requires PulseAudio for raw audio functions.

**Solution**:
```bash
sudo apt install -y pulseaudio
mkdir -p ~/.config
echo "[General]" > ~/.config/zoomus.conf
echo "system.audio.type=default" >> ~/.config/zoomus.conf
```

See: **[PulseAudio Setup](troubleshooting/pulseaudio-setup.md)**

### ⚠️ CRITICAL #3: Qt5 Dependencies

**Problem**: SDK requires Qt5 libraries (bundled, NOT system Qt5).

**Solution**:
```bash
# Copy from SDK package
cp -r samples/qt_libs/Qt/lib/* lib/zoom_video_sdk/

# Create symlinks
cd lib/zoom_video_sdk
for lib in libQt5*.so.5; do ln -sf $lib ${lib%.5}; done
```

See: **[Qt Dependencies](troubleshooting/qt-dependencies.md)**

### ⚠️ CRITICAL #4: Heap Memory Mode

Always use heap mode for raw data:

```cpp
init_params.videoRawDataMemoryMode = ZoomVideoSDKRawDataMemoryModeHeap;
init_params.shareRawDataMemoryMode = ZoomVideoSDKRawDataMemoryModeHeap;
init_params.audioRawDataMemoryMode = ZoomVideoSDKRawDataMemoryModeHeap;
```

### ⚠️ CRITICAL #5: Virtual Audio for Headless

**Problem**: Docker/headless environments have no audio devices.

**Solution**: Use virtual audio speaker and mic.

```cpp
session_context.virtualAudioSpeaker = new VirtualSpeaker();
session_context.virtualAudioMic = new VirtualMic();
```

See: **[Virtual Audio/Video](examples/virtual-audio-video.md)**

## Sample Repositories

### Official Samples

| Repository | Description |
|-----------|-------------|
| **[raw-recording-sample](https://github.com/zoom/videosdk-linux-raw-recording-sample)** | Raw audio/video capture |
| **[qt-quickstart](https://github.com/tanchunsiong/videosdk-linux-qt-quickstart)** | Qt6 UI integration |
| **[gtk-quickstart](https://github.com/tanchunsiong/videosdk-linux-gtk-quickstart)** | GTK3 UI integration |

### Sample Architecture

```
Headless Bot (Docker):
┌──────────────────────────────────┐
│  Virtual Audio Speaker/Mic       │
├──────────────────────────────────┤
│  Raw Data Processing             │
│  - YUV420 → File/Stream   

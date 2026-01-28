# Meeting SDK - Linux

Headless meeting bots and server-side processing on Linux.

## Overview

Linux SDK for building meeting bots, automated participants, and server-side meeting processing with raw audio/video data access.

## Prerequisites

- Meeting SDK downloaded from [Marketplace](https://marketplace.zoom.us/) (sign-in required)
- Ubuntu 18.04+ or compatible Linux distribution
- GCC/G++ compiler
- Valid SDK credentials

## Installation

1. Download SDK from Marketplace (requires sign-in)
2. Extract to your project directory
3. Link against SDK libraries

## Quick Start

```cpp
#include "zoom_sdk.h"

// Initialize
ZOOM_SDK_NAMESPACE::InitParam initParam;
initParam.strWebDomain = "zoom.us";
ZOOM_SDK_NAMESPACE::SDKError err = ZOOM_SDK_NAMESPACE::InitSDK(initParam);

// Join meeting
ZOOM_SDK_NAMESPACE::JoinParam joinParam;
joinParam.userType = ZOOM_SDK_NAMESPACE::SDK_UT_NORMALUSER;
ZOOM_SDK_NAMESPACE::JoinParam4NormalUser& normalParam = joinParam.param.normaluserJoin;
normalParam.meetingNumber = meetingNumber;
normalParam.userName = L"Bot";
normalParam.psw = password;
```

## Raw Recording / Raw Data Access

Access raw audio and video frames for custom processing.

### Audio Delegate Interface

```cpp
class IZoomSDKAudioRawDataDelegate {
public:
    // Mixed audio from all participants
    virtual void onMixedAudioRawDataReceived(AudioRawData* data) = 0;
    
    // Individual participant audio
    virtual void onOneWayAudioRawDataReceived(AudioRawData* data, uint32_t user_id) = 0;
    
    // Shared audio (e.g., screen share with audio)
    virtual void onShareAudioRawDataReceived(AudioRawData* data, uint32_t user_id) = 0;
    
    // Individual interpreter audio
    virtual void onOneWayInterpreterAudioRawDataReceived(AudioRawData* data, const zchar_t* pLanguageName) = 0;
};
```

### Send Audio (Virtual Microphone)

```cpp
class IZoomSDKVirtualAudioMicEvent {
public:
    virtual void onMicInitialize(IZoomSDKAudioRawDataSender* pSender) = 0;
    virtual void onMicStartSend() = 0;
    virtual void onMicStopSend() = 0;
    virtual void onMicUninitialized() = 0;
};

// Audio sender interface
class IZoomSDKAudioRawDataSender {
public:
    // Send 16-bit PCM audio
    // Mono sample rates: 8000/11025/16000/32000/44100/48000/50000/50400/96000/192000
    // Stereo sample rates: 8000/16000/32000/44100/48000/50000/50400/96000/192000
    virtual SDKError send(char* data, unsigned int data_length, int sample_rate, 
                          ZoomSDKAudioChannel channel = ZoomSDKAudioChannel_Mono) = 0;
};
```

### Raw Audio Data

```cpp
class AudioRawDataDelegate : public IZoomSDKAudioRawDataDelegate {
public:
    void onMixedAudioRawDataReceived(AudioRawData* data) override {
        // Process mixed audio from all participants
        // data->GetBuffer() - PCM audio data
        // data->GetSampleRate() - Sample rate
        // data->GetChannelNum() - Number of channels
    }
    
    void onOneWayAudioRawDataReceived(AudioRawData* data, uint32_t node_id) override {
        // Process audio from specific participant
    }
};
```

### Video Source Interface (Send Video)

```cpp
struct VideoSourceCapability {
    unsigned int width;
    unsigned int height;
    unsigned int frame;  // FPS
};

class IZoomSDKVideoSource {
public:
    virtual void onInitialize(IZoomSDKVideoSender* sender, 
                              IList<VideoSourceCapability>* support_cap_list, 
                              VideoSourceCapability& suggest_cap) = 0;
    virtual void onPropertyChange(IList<VideoSourceCapability>* support_cap_list, 
                                  VideoSourceCapability suggest_cap) = 0;
    virtual void onStartSend() = 0;
    virtual void onStopSend() = 0;
    virtual void onUninitialized() = 0;
};

// Video sender interface
class IZoomSDKVideoSender {
public:
    virtual SDKError sendVideoFrame(char* frameBuffer, int width, int height, 
                                     int frameLength, int rotation, 
                                     FrameDataFormat format = FrameDataFormat_I420_FULL) = 0;
};
```

### Raw Video Data (Receive Video)

```cpp
class VideoRawDataDelegate : public IZoomSDKVideoRawDataDelegate {
public:
    void onRawDataFrameReceived(YUVRawDataI420* data) override {
        // Process raw video frames
        // data->GetBuffer() - YUV420 frame data
        // data->GetStreamWidth() - Frame width
        // data->GetStreamHeight() - Frame height
    }
};
```

## Common Use Cases

- Meeting bots for AI/transcription
- Automated meeting recording
- Real-time audio/video processing
- Compliance and archival solutions

## Common Tasks

### Headless Operation Setup

Linux SDK runs without a display (headless). Key considerations:

```cpp
// Initialize SDK (same as other platforms)
InitParam initParam;
initParam.strWebDomain = "zoom.us";
initParam.strSupportUrl = "zoom.us";
initParam.emLanguageID = LANGUAGE_English;
initParam.enableLogByDefault = true;
initParam.enableGenerateDump = true;

auto err = InitSDK(initParam);

// Create services
CreateMeetingService(&m_meetingService);
CreateSettingService(&m_settingService);
CreateAuthService(&m_authService);
```

**Even headless mode requires X11**: Use `xvfb-run` for containers:
```bash
xvfb-run -a ./your_bot_application
```

### Raw Audio Processing Pipeline

```cpp
class AudioRawDataDelegate : public IZoomSDKAudioRawDataDelegate {
public:
    void onMixedAudioRawDataReceived(AudioRawData *data) override {
        // Write to file
        std::ofstream file("out/meeting.pcm", std::ios::binary | std::ios::app);
        file.write(data->GetBuffer(), data->GetBufferLen());
        
        // Or send to transcription service via WebSocket
        transcriptionSocket.send(data->GetBuffer(), data->GetBufferLen());
    }
    
    void onOneWayAudioRawDataReceived(AudioRawData* data, uint32_t node_id) override {
        // Per-participant audio for speaker identification
    }
};

// Audio format: 16-bit PCM, 16kHz or 32kHz, mono
```

### Raw Video Processing Pipeline

```cpp
class VideoRawDataDelegate : public IZoomSDKRendererDelegate {
public:
    void onRawDataFrameReceived(YUVRawDataI420 *data) override {
        // Convert I420 to BGR using OpenCV
        cv::Mat I420(data->GetStreamHeight() * 3/2, 
                   data->GetStreamWidth(), 
                   CV_8UC1, 
                   data->GetBuffer());
        cv::Mat colorFrame;
        cv::cvtColor(I420, colorFrame, cv::COLOR_YUV2BGR_I420);
        
        // Process: face detection, OCR, etc.
        // Save as video
        videoWriter.write(colorFrame);
    }
};
```

### Bot Identity Configuration

```cpp
// Join as bot with custom display name
JoinParam joinParam;
joinParam.userType = SDK_UT_WITHOUT_LOGIN;
JoinParam4WithoutLogin& param = joinParam.param.withoutloginuserJoin;
param.meetingNumber = meetingNumber;
param.userName = "My Bot";  // Display name shown to participants
param.psw = password;
param.isVideoOff = false;   // Bot can have video
param.isAudioOff = false;   // Bot can have audio

// Use ZAK token for authenticated bot access
if (zakToken) {
    param.userZAK = zakToken;
}

// Use OBF token for external meetings (required after Feb 2026)
if (obfToken) {
    param.onBehalfToken = obfToken;
}

err = m_meetingService->Join(joinParam);
```

## Container Deployment (Docker)

**Dockerfile**:
```dockerfile
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libpulse0 \
    libasound2-dev \
    libx11-6 \
    libxext6 \
    libxi6 \
    libxrender1 \
    libxcb1 \
    xvfb \
    pulseaudio

# Add to audio group for sound access
RUN usermod -aG audio root

# Copy SDK binaries
COPY lib/zoomsdk /usr/lib/zoomsdk
ENV LD_LIBRARY_PATH=/usr/lib/zoomsdk:$LD_LIBRARY_PATH

# Run with Xvfb
CMD ["xvfb-run", "-a", "./your_bot"]
```

**Key gotchas**:
1. **Must run as root or add user to `audio` group** for PulseAudio access
2. **Xvfb required** even for headless operation
3. **PulseAudio daemon** must be running for audio

## System Requirements

**Minimum**:
- Ubuntu 18.04+, CentOS 8+, Oracle Linux 8+
- x86_64 architecture
- 2GB RAM minimum (4GB recommended)
- OpenGL 2.0+ for video

**Dependencies (Ubuntu/Debian)**:
```bash
sudo apt-get install -y \
    libgl1-mesa-glx \
    libpulse0 \
    libasound2-dev \
    libx11-6 \
    libxext6 \
    libxi6
```

## Resources

- **Linux docs**: https://developers.zoom.us/docs/meeting-sdk/linux/
- **Headless Sample**: https://github.com/zoom/meetingsdk-headless-linux-sample

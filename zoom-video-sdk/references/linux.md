# Video SDK - Linux

Server-side video processing and meeting bots with Video SDK on Linux.

## Overview

Linux SDK for headless video applications, bots, and server-side processing with raw audio/video data access.

## Prerequisites

- Video SDK downloaded from [Marketplace](https://marketplace.zoom.us/) (sign-in required)
- Ubuntu 18.04+ or compatible Linux distribution
- GCC/G++ compiler
- Valid SDK credentials

## Installation

1. Download SDK from Marketplace (requires sign-in)
2. Extract to your project directory
3. Link against SDK libraries

## Quick Start

```cpp
#include "ZoomVideoSDK.h"

// Initialize
ZoomVideoSDKInitParams initParams;
initParams.domain = "zoom.us";
ZoomVideoSDK::getInstance().initialize(initParams);

// Join session
ZoomVideoSDKSessionContext sessionContext;
sessionContext.sessionName = "MySession";
sessionContext.userName = "Bot";
sessionContext.token = signature;
ZoomVideoSDK::getInstance().joinSession(sessionContext);
```

## Raw Recording / Raw Data Access

Access raw audio and video frames for custom processing:

### Raw Audio Data

```cpp
class MyRawDataDelegate : public IZoomVideoSDKRawDataPipeDelegate {
public:
    void onRawDataReceived(YUVRawDataI420* data) override {
        // Process raw video frames
        // data->GetBuffer() - YUV420 frame data
        // data->GetStreamWidth(), data->GetStreamHeight()
    }
    
    void onRawAudioDataReceived(AudioRawData* data) override {
        // Process raw audio samples
        // data->GetBuffer() - PCM audio data
        // data->GetSampleRate(), data->GetChannelNum()
    }
};
```

### Subscribe to Raw Data

```cpp
auto user = session->getMyself();
auto rawDataPipe = user->GetVideoPipe();
rawDataPipe->subscribe(ZoomVideoSDKRawDataType_Video, myDelegate);
```

## Common Use Cases

- Meeting bots for AI/transcription
- Custom recording pipelines
- Real-time audio/video processing
- Media archival solutions

## Common Tasks

### Headless Operation

```cpp
#include "ZoomVideoSDK.h"

// Initialize SDK for headless operation
int main() {
    ZoomVideoSDKInitParams initParams;
    initParams.domain = "zoom.us";
    initParams.enableLog = true;
    initParams.logFilePrefix = "zoom_video_sdk";
    
    auto sdk = &ZoomVideoSDK::getInstance();
    auto err = sdk->initialize(initParams);
    if (err != ZoomVideoSDKErrors_Success) {
        std::cerr << "Init failed: " << err << std::endl;
        return 1;
    }
    
    // Set delegate for events
    sdk->addListener(new MySessionDelegate());
    
    // Join session
    ZoomVideoSDKSessionContext ctx;
    ctx.sessionName = "MySession";
    ctx.userName = "Bot";
    ctx.token = generateJWT();
    
    sdk->joinSession(ctx);
    
    // Run event loop
    while (running) {
        sdk->processEvents();  // Or use your own event loop
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
    
    sdk->cleanup();
    return 0;
}
```

### Raw Audio Processing Pipeline

```cpp
class AudioRawDataDelegate : public IZoomVideoSDKRawDataPipeDelegate {
private:
    std::ofstream audioFile;
    WebSocketClient* transcriptionClient;
    
public:
    AudioRawDataDelegate() {
        audioFile.open("session_audio.pcm", std::ios::binary);
        transcriptionClient = new WebSocketClient("wss://transcription-service");
    }
    
    void onRawAudioDataReceived(AudioRawData* data) override {
        // Format: 16-bit PCM, 16kHz or 32kHz, mono
        const char* buffer = data->GetBuffer();
        uint32_t length = data->GetBufferLen();
        uint32_t sampleRate = data->GetSampleRate();
        uint32_t channels = data->GetChannelNum();
        
        // Save to file
        audioFile.write(buffer, length);
        
        // Stream to transcription service
        transcriptionClient->send(buffer, length);
        
        // Or process locally
        processAudioChunk(buffer, length, sampleRate);
    }
    
    void processAudioChunk(const char* buffer, uint32_t length, uint32_t sampleRate) {
        // Voice activity detection
        // Noise reduction
        // Feature extraction for ML
    }
};

// Subscribe to mixed audio (all participants)
void subscribeToMixedAudio(IZoomVideoSDKSession* session) {
    auto audioHelper = session->getAudioHelper();
    audioHelper->subscribe(new AudioRawDataDelegate());
}
```

### Raw Video Processing Pipeline

```cpp
#include <opencv2/opencv.hpp>

class VideoRawDataDelegate : public IZoomVideoSDKRawDataPipeDelegate {
private:
    cv::VideoWriter videoWriter;
    
public:
    VideoRawDataDelegate() {
        videoWriter.open("session_video.mp4", 
            cv::VideoWriter::fourcc('m', 'p', '4', 'v'),
            30, cv::Size(1280, 720));
    }
    
    void onRawDataReceived(YUVRawDataI420* data) override {
        // Format: I420 (YUV 4:2:0)
        uint32_t width = data->GetStreamWidth();
        uint32_t height = data->GetStreamHeight();
        const char* buffer = data->GetBuffer();
        
        // Convert I420 to BGR
        cv::Mat I420(height * 3/2, width, CV_8UC1, (void*)buffer);
        cv::Mat bgr;
        cv::cvtColor(I420, bgr, cv::COLOR_YUV2BGR_I420);
        
        // Process frame
        processFrame(bgr);
        
        // Save to video
        videoWriter.write(bgr);
    }
    
    void processFrame(cv::Mat& frame) {
        // Face detection
        // OCR on shared content
        // Object detection
        // Custom AI/ML processing
    }
};

// Subscribe to user's video
void subscribeToVideo(IZoomVideoSDKUser* user) {
    auto videoPipe = user->GetVideoPipe();
    videoPipe->setRawDataResolution(ZoomVideoSDKResolution_720P);
    videoPipe->subscribe(new VideoRawDataDelegate());
}
```

### Resource Management

```cpp
class SessionManager {
private:
    std::vector<IZoomVideoSDKRawDataPipeDelegate*> delegates;
    std::atomic<bool> running{true};
    
public:
    void addDelegate(IZoomVideoSDKRawDataPipeDelegate* delegate) {
        delegates.push_back(delegate);
    }
    
    void cleanup() {
        running = false;
        
        // Unsubscribe all delegates
        for (auto delegate : delegates) {
            delete delegate;
        }
        delegates.clear();
        
        // Leave session
        ZoomVideoSDK::getInstance().leaveSession(false);
        
        // Cleanup SDK
        ZoomVideoSDK::getInstance().cleanup();
    }
    
    // Handle graceful shutdown
    void setupSignalHandlers() {
        signal(SIGINT, [](int sig) {
            // Trigger cleanup
            instance->cleanup();
        });
        signal(SIGTERM, [](int sig) {
            instance->cleanup();
        });
    }
};

// Memory monitoring
void monitorResources() {
    struct rusage usage;
    getrusage(RUSAGE_SELF, &usage);
    
    size_t memoryMB = usage.ru_maxrss / 1024;
    if (memoryMB > 2048) {  // 2GB threshold
        std::cerr << "Warning: High memory usage: " << memoryMB << " MB" << std::endl;
    }
}
```

### Container Deployment (Docker)

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
    xvfb \
    libopencv-dev

# Copy SDK
COPY lib/zoomsdk /usr/lib/zoomsdk
ENV LD_LIBRARY_PATH=/usr/lib/zoomsdk:$LD_LIBRARY_PATH

# Copy application
COPY build/video_bot /app/video_bot

# Run with virtual display
CMD ["xvfb-run", "-a", "/app/video_bot"]
```

## System Requirements

- Ubuntu 18.04+ / CentOS 8+ / Oracle Linux 8+
- x86_64 architecture
- 4GB RAM recommended
- OpenGL 2.0+ for video processing

## Resources

- **Linux docs**: https://developers.zoom.us/docs/video-sdk/linux/
- **Sample app**: https://github.com/zoom/videosdk-linux-raw-recording-sample

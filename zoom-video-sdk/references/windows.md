# Video SDK - Windows

Desktop video applications and raw data processing on Windows.

## Overview

Windows SDK for building custom video applications with full UI control and raw audio/video data access.

## Prerequisites

- Video SDK downloaded from [Marketplace](https://marketplace.zoom.us/) (sign-in required)
- Visual Studio 2017+
- Windows 10+
- Valid SDK credentials

## Installation

1. Download SDK from Marketplace (requires sign-in)
2. Add SDK headers and libraries to your project
3. Configure linker settings

## Quick Start

```cpp
#include "ZoomVideoSDK.h"

// Initialize
ZoomVideoSDKInitParams initParams;
initParams.domain = L"zoom.us";
ZoomVideoSDK::getInstance().initialize(initParams);

// Join session
ZoomVideoSDKSessionContext sessionContext;
sessionContext.sessionName = L"MySession";
sessionContext.userName = L"User";
sessionContext.token = signature;
ZoomVideoSDK::getInstance().joinSession(sessionContext);
```

## Raw Recording / Raw Data Access

Access raw audio and video frames for custom processing:

### Raw Data Delegate

```cpp
class MyRawDataDelegate : public IZoomVideoSDKRawDataPipeDelegate {
public:
    void onRawDataReceived(YUVRawDataI420* data) override {
        // Process raw video frames
    }
    
    void onRawAudioDataReceived(AudioRawData* data) override {
        // Process raw audio samples
    }
};
```

## Common Tasks

### Window/UI Integration

```cpp
// Create video canvas window
HWND CreateVideoWindow(HWND parent) {
    HWND hwnd = CreateWindowEx(
        0, L"VideoCanvas", L"",
        WS_CHILD | WS_VISIBLE,
        0, 0, 640, 360,
        parent, NULL, hInstance, NULL
    );
    return hwnd;
}

// Render video to window
void RenderVideo(IZoomVideoSDKUser* user, HWND targetWindow) {
    auto videoCanvas = user->GetVideoCanvas();
    videoCanvas->SetCanvas(targetWindow);
    videoCanvas->Subscribe(ZoomVideoSDKResolution_720P);
}

// Handle window resize
void OnResize(HWND hwnd, int width, int height) {
    // Update video canvas size
    auto user = currentSession->GetMyself();
    auto videoCanvas = user->GetVideoCanvas();
    videoCanvas->SetSize(width, height);
}
```

### Raw Audio Processing

```cpp
class AudioRawDataDelegate : public IZoomVideoSDKRawDataPipeDelegate {
public:
    void onRawAudioDataReceived(AudioRawData* data) override {
        // Format: 16-bit PCM, 16kHz or 32kHz
        const char* buffer = data->GetBuffer();
        uint32_t length = data->GetBufferLen();
        uint32_t sampleRate = data->GetSampleRate();
        uint32_t channels = data->GetChannelNum();
        
        // Process or forward to transcription service
        processAudio(buffer, length, sampleRate, channels);
    }
};

// Subscribe to audio
void SubscribeAudio(IZoomVideoSDKUser* user) {
    auto audioPipe = user->GetAudioPipe();
    audioPipe->subscribe(new AudioRawDataDelegate());
}
```

### Raw Video Processing

```cpp
class VideoRawDataDelegate : public IZoomVideoSDKRawDataPipeDelegate {
public:
    void onRawDataReceived(YUVRawDataI420* data) override {
        // Format: I420 (YUV 4:2:0)
        uint32_t width = data->GetStreamWidth();
        uint32_t height = data->GetStreamHeight();
        const char* buffer = data->GetBuffer();
        
        // Convert to RGB for display or processing
        convertI420toRGB(buffer, width, height, rgbBuffer);
    }
};

// Subscribe to video at specific resolution
void SubscribeVideo(IZoomVideoSDKUser* user) {
    auto videoPipe = user->GetVideoPipe();
    videoPipe->setRawDataResolution(ZoomVideoSDKResolution_720P);
    videoPipe->subscribe(new VideoRawDataDelegate());
}
```

### Device Management

```cpp
// Enumerate devices
void ListDevices() {
    // Cameras
    auto videoHelper = ZoomVideoSDK::getInstance().getVideoHelper();
    auto cameras = videoHelper->getCameraList();
    for (int i = 0; i < cameras->GetCount(); i++) {
        auto camera = cameras->GetItem(i);
        wprintf(L"Camera: %s\n", camera->GetDeviceName());
    }
    
    // Microphones
    auto audioHelper = ZoomVideoSDK::getInstance().getAudioHelper();
    auto mics = audioHelper->getMicList();
    for (int i = 0; i < mics->GetCount(); i++) {
        auto mic = mics->GetItem(i);
        wprintf(L"Mic: %s\n", mic->GetDeviceName());
    }
    
    // Speakers
    auto speakers = audioHelper->getSpeakerList();
}

// Switch devices
void SwitchCamera(const wchar_t* deviceId) {
    auto videoHelper = ZoomVideoSDK::getInstance().getVideoHelper();
    videoHelper->selectCamera(deviceId);
}

void SwitchMicrophone(const wchar_t* deviceId) {
    auto audioHelper = ZoomVideoSDK::getInstance().getAudioHelper();
    audioHelper->selectMic(deviceId);
}
```

## Event Handling (Delegate Pattern)

Windows SDK uses the `IZoomVideoSDKDelegate` interface for event callbacks.

### Session Events

```cpp
class MyEventHandler : public IZoomVideoSDKDelegate {
public:
    // Session lifecycle
    void onSessionJoin() override {
        std::wcout << L"Joined session" << std::endl;
    }
    
    void onSessionLeave() override {
        std::wcout << L"Left session" << std::endl;
    }
    
    void onSessionNeedPassword(IZoomVideoSDKPasswordHandler* handler) override {
        handler->inputSessionPassword(L"password");
    }
    
    void onSessionPasswordWrong(IZoomVideoSDKPasswordHandler* handler) override {
        // Prompt user for correct password
    }
    
    // User events
    void onUserJoin(IZoomVideoSDKUserHelper* helper, 
                    IVideoSDKVector<IZoomVideoSDKUser*>* userList) override {
        for (int i = 0; i < userList->GetCount(); i++) {
            auto user = userList->GetItem(i);
            wprintf(L"User joined: %s\n", user->getUserName());
            
            // Subscribe to their video
            auto canvas = user->GetVideoCanvas();
            if (canvas) {
                canvas->Subscribe(ZoomVideoSDKResolution_720P);
            }
        }
    }
    
    void onUserLeave(IZoomVideoSDKUserHelper* helper,
                     IVideoSDKVector<IZoomVideoSDKUser*>* userList) override {
        for (int i = 0; i < userList->GetCount(); i++) {
            wprintf(L"User left: %s\n", userList->GetItem(i)->getUserName());
        }
    }
    
    // Audio events
    void onUserAudioStatusChanged(IZoomVideoSDKAudioHelper* helper,
                                   IVideoSDKVector<IZoomVideoSDKUser*>* userList) override {
        for (int i = 0; i < userList->GetCount(); i++) {
            auto user = userList->GetItem(i);
            auto audioStatus = user->getAudioStatus();
            if (audioStatus) {
                bool muted = audioStatus->isMuted();
                wprintf(L"User %s audio: %s\n", 
                        user->getUserName(), 
                        muted ? L"muted" : L"unmuted");
            }
        }
    }
    
    // Video events
    void onUserVideoStatusChanged(IZoomVideoSDKVideoHelper* helper,
                                   IVideoSDKVector<IZoomVideoSDKUser*>* userList) override {
        for (int i = 0; i < userList->GetCount(); i++) {
            auto user = userList->GetItem(i);
            bool videoOn = user->getVideoStatus()->isOn();
            wprintf(L"User %s video: %s\n",
                    user->getUserName(),
                    videoOn ? L"on" : L"off");
        }
    }
    
    // Chat events
    void onChatNewMessageNotify(IZoomVideoSDKChatHelper* helper,
                                 IZoomVideoSDKChatMessage* message) override {
        wprintf(L"Chat from %s: %s\n", 
                message->getSenderUser()->getUserName(),
                message->getContent());
    }
};

// Register event handler
void SetupEventHandler() {
    auto sdk = &ZoomVideoSDK::getInstance();
    sdk->addListener(new MyEventHandler());
}
```

### Connection Events

```cpp
class ConnectionHandler : public IZoomVideoSDKDelegate {
public:
    void onError(ZoomVideoSDKErrors errorCode) override {
        switch (errorCode) {
            case ZoomVideoSDKErrors_Session_Join_Failed:
                std::wcout << L"Failed to join session" << std::endl;
                break;
            case ZoomVideoSDKErrors_Session_Disconnecting:
                std::wcout << L"Session disconnected" << std::endl;
                break;
            case ZoomVideoSDKErrors_Session_Reconnecting:
                std::wcout << L"Reconnecting..." << std::endl;
                break;
            default:
                wprintf(L"Error: %d\n", errorCode);
        }
    }
    
    void onSessionStateChanged(ZoomVideoSDKSessionStatus status) override {
        switch (status) {
            case ZoomVideoSDKSessionStatus_Idle:
                std::wcout << L"Session idle" << std::endl;
                break;
            case ZoomVideoSDKSessionStatus_InSession:
                std::wcout << L"In session" << std::endl;
                break;
        }
    }
};
```

## Screen Sharing

### Share Monitor or Window

```cpp
// Get shareable sources
void ListShareSources() {
    auto shareHelper = ZoomVideoSDK::getInstance().getShareHelper();
    
    // List monitors
    auto monitorList = shareHelper->getMonitorList();
    for (int i = 0; i < monitorList->GetCount(); i++) {
        auto monitor = monitorList->GetItem(i);
        wprintf(L"Monitor %d: %s\n", i, monitor->getMonitorName());
    }
    
    // List windows (applications)
    auto windowList = shareHelper->getShareableWindowList();
    for (int i = 0; i < windowList->GetCount(); i++) {
        auto window = windowList->GetItem(i);
        wprintf(L"Window: %s (HWND: %p)\n", 
                window->getWindowTitle(),
                window->getWindowHandle());
    }
}

// Share entire monitor
void ShareMonitor(int monitorIndex) {
    auto shareHelper = ZoomVideoSDK::getInstance().getShareHelper();
    auto monitorList = shareHelper->getMonitorList();
    
    if (monitorIndex < monitorList->GetCount()) {
        auto monitor = monitorList->GetItem(monitorIndex);
        shareHelper->startShareScreen(monitor);
    }
}

// Share specific window
void ShareWindow(HWND windowHandle) {
    auto shareHelper = ZoomVideoSDK::getInstance().getShareHelper();
    auto windowList = shareHelper->getShareableWindowList();
    
    for (int i = 0; i < windowList->GetCount(); i++) {
        auto window = windowList->GetItem(i);
        if (window->getWindowHandle() == windowHandle) {
            shareHelper->startShareWindow(window);
            break;
        }
    }
}

// Stop sharing
void StopShare() {
    ZoomVideoSDK::getInstance().getShareHelper()->stopShare();
}
```

### Screen Share Event Handler

```cpp
class ShareEventHandler : public IZoomVideoSDKDelegate {
public:
    void onUserShareStatusChanged(IZoomVideoSDKShareHelper* helper,
                                   IZoomVideoSDKUser* user,
                                   ZoomVideoSDKShareStatus status) override {
        switch (status) {
            case ZoomVideoSDKShareStatus_Start:
                wprintf(L"User %s started sharing\n", user->getUserName());
                // Subscribe to share canvas
                if (auto shareCanvas = user->GetShareCanvas()) {
                    shareCanvas->SetCanvas(shareWindowHandle);
                    shareCanvas->Subscribe(ZoomVideoSDKResolution_1080P);
                }
                break;
                
            case ZoomVideoSDKShareStatus_Stop:
                wprintf(L"User %s stopped sharing\n", user->getUserName());
                break;
                
            case ZoomVideoSDKShareStatus_Pause:
                std::wcout << L"Screen share paused" << std::endl;
                break;
        }
    }
    
private:
    HWND shareWindowHandle;
};

// View screen share from another user
void ViewScreenShare(IZoomVideoSDKUser* sharingUser, HWND targetWindow) {
    auto shareCanvas = sharingUser->GetShareCanvas();
    if (shareCanvas) {
        shareCanvas->SetCanvas(targetWindow);
        shareCanvas->Subscribe(ZoomVideoSDKResolution_720P);
    }
}
```

## Virtual Camera (Custom Video Source)

Inject custom video frames (e.g., from file, NDI, or generated graphics).

### Implement Video Source Interface

```cpp
class MyVirtualCamera : public IZoomVideoSDKVideoSource {
public:
    MyVirtualCamera() : running(false), width(1280), height(720) {}
    
    // SDK calls this when it's ready to receive frames
    void onInitialize(IZoomVideoSDKVideoSender* sender,
                      IVideoSDKVector<VideoSourceCapability>* capList,
                      VideoSourceCapability& suggestCap) override {
        videoSender = sender;
        
        // Set our capability
        suggestCap.width = width;
        suggestCap.height = height;
        suggestCap.frame = 30;  // 30 FPS
    }
    
    void onPropertyChange(IVideoSDKVector<VideoSourceCapability>* capList,
                          VideoSourceCapability suggestCap) override {
        width = suggestCap.width;
        height = suggestCap.height;
    }
    
    void onStartSend() override {
        running = true;
        // Start your frame generation thread
        frameThread = std::thread(&MyVirtualCamera::generateFrames, this);
    }
    
    void onStopSend() override {
        running = false;
        if (frameThread.joinable()) {
            frameThread.join();
        }
    }
    
    void onUninitialized() override {
        videoSender = nullptr;
    }
    
private:
    void generateFrames() {
        while (running) {
            // Create I420 frame buffer
            int ySize = width * height;
            int uvSize = ySize / 4;
            std::vector<char> frameBuffer(ySize + uvSize * 2);
            
            // Fill with your video data (I420 format)
            // Y plane: frameBuffer[0..ySize]
            // U plane: frameBuffer[ySize..ySize+uvSize]
            // V plane: frameBuffer[ySize+uvSize..]
            generateTestPattern(frameBuffer.data(), width, height);
            
            // Send frame to SDK
            if (videoSender) {
                videoSender->sendVideoFrame(
                    frameBuffer.data(),
                    width,
                    height,
                    ySize + uvSize * 2,
                    0  // rotation
                );
            }
            
            // 30 FPS = ~33ms per frame
            std::this_thread::sleep_for(std::chrono::milliseconds(33));
        }
    }
    
    void generateTestPattern(char* buffer, int w, int h) {
        // Example: generate a simple color bar pattern
        int ySize = w * h;
        int uvSize = ySize / 4;
        
        // Y plane (luminance)
        for (int y = 0; y < h; y++) {
            for (int x = 0; x < w; x++) {
                buffer[y * w + x] = (x * 256 / w);  // gradient
            }
        }
        
        // U and V planes (chrominance)
        memset(buffer + ySize, 128, uvSize * 2);
    }
    
    IZoomVideoSDKVideoSender* videoSender = nullptr;
    std::thread frameThread;
    std::atomic<bool> running;
    int width, height;
};

// Use virtual camera
void EnableVirtualCamera() {
    auto videoHelper = ZoomVideoSDK::getInstance().getVideoHelper();
    
    static MyVirtualCamera virtualCamera;
    videoHelper->setExternalVideoSource(&virtualCamera);
    
    // Start video will now use virtual camera
    videoHelper->startVideo();
}

// Switch back to physical camera
void DisableVirtualCamera() {
    auto videoHelper = ZoomVideoSDK::getInstance().getVideoHelper();
    videoHelper->setExternalVideoSource(nullptr);
}
```

## Virtual Microphone (Custom Audio Source)

Inject custom audio (e.g., from file, text-to-speech, or audio processing).

### Implement Audio Source Interface

```cpp
class MyVirtualMic : public IZoomVideoSDKVirtualAudioMic {
public:
    MyVirtualMic() : running(false), sampleRate(16000), channels(1) {}
    
    void onMicInitialize(IZoomVideoSDKAudioSender* sender) override {
        audioSender = sender;
    }
    
    void onMicStartSend() override {
        running = true;
        // Start audio generation thread
        audioThread = std::thread(&MyVirtualMic::generateAudio, this);
    }
    
    void onMicStopSend() override {
        running = false;
        if (audioThread.joinable()) {
            audioThread.join();
        }
    }
    
    void onMicUninitialized() override {
        audioSender = nullptr;
    }
    
private:
    void generateAudio() {
        // 20ms of audio at 16kHz = 320 samples
        const int samplesPerFrame = sampleRate / 50;
        std::vector<int16_t> audioBuffer(samplesPerFrame * channels);
        
        while (running) {
            // Fill with your audio data
            // Could be from file, TTS, or generated tone
            generateTone(audioBuffer.data(), samplesPerFrame);
            
            // Send audio to SDK
            if (audioSender) {
                audioSender->send(
                    reinterpret_cast<char*>(audioBuffer.data()),
                    samplesPerFrame * sizeof(int16_t) * channels,
                    sampleRate
                );
            }
            
            // 20ms frames
            std::this_thread::sleep_for(std::chrono::milliseconds(20));
        }
    }
    
    void generateTone(int16_t* buffer, int samples) {
        static double phase = 0;
        const double frequency = 440.0;  // 440 Hz tone
        const double amplitude = 16000;
        
        for (int i = 0; i < samples; i++) {
            buffer[i] = static_cast<int16_t>(
                amplitude * sin(2.0 * M_PI * frequency * phase / sampleRate)
            );
            phase += 1.0;
            if (phase >= sampleRate) phase -= sampleRate;
        }
    }
    
    IZoomVideoSDKAudioSender* audioSender = nullptr;
    std::thread audioThread;
    std::atomic<bool> running;
    int sampleRate;
    int channels;
};

// Use virtual microphone
void EnableVirtualMic() {
    auto audioHelper = ZoomVideoSDK::getInstance().getAudioHelper();
    
    static MyVirtualMic virtualMic;
    audioHelper->setExternalAudioSource(&virtualMic);
    
    // Start audio will now use virtual mic
    audioHelper->startAudio();
}
```

### Audio Playback from File

```cpp
class FileAudioSource : public IZoomVideoSDKVirtualAudioMic {
public:
    FileAudioSource(const std::wstring& wavFilePath) {
        loadWavFile(wavFilePath);
    }
    
    void onMicStartSend() override {
        running = true;
        playbackPosition = 0;
        audioThread = std::thread(&FileAudioSource::streamAudio, this);
    }
    
private:
    void loadWavFile(const std::wstring& path) {
        // Parse WAV header and load PCM data
        // Store in audioData vector
        // Set sampleRate from WAV header
    }
    
    void streamAudio() {
        const int samplesPerFrame = sampleRate / 50;  // 20ms
        
        while (running && playbackPosition < audioData.size()) {
            int samplesToSend = std::min(
                samplesPerFrame,
                static_cast<int>(audioData.size() - playbackPosition)
            );
            
            audioSender->send(
                reinterpret_cast<char*>(&audioData[playbackPosition]),
                samplesToSend * sizeof(int16_t),
                sampleRate
            );
            
            playbackPosition += samplesToSend;
            std::this_thread::sleep_for(std::chrono::milliseconds(20));
        }
    }
    
    std::vector<int16_t> audioData;
    size_t playbackPosition = 0;
    int sampleRate = 16000;
};
```

## Virtual Speaker (Audio Output Capture)

Capture audio that would normally go to speakers.

```cpp
class MyVirtualSpeaker : public IZoomVideoSDKVirtualAudioSpeaker {
public:
    void onVirtualSpeakerMixedAudioReceived(AudioRawData* data) override {
        // Receive mixed audio from all participants
        const char* buffer = data->GetBuffer();
        uint32_t length = data->GetBufferLen();
        uint32_t sampleRate = data->GetSampleRate();
        
        // Process, save, or forward to transcription
        processAudio(buffer, length, sampleRate);
    }
    
    void onVirtualSpeakerOneWayAudioReceived(AudioRawData* data,
                                              IZoomVideoSDKUser* user) override {
        // Receive audio from specific user
        wprintf(L"Audio from: %s\n", user->getUserName());
    }
    
private:
    void processAudio(const char* buffer, uint32_t length, uint32_t sampleRate) {
        // Example: write to file or send to STT service
    }
};

// Enable virtual speaker
void EnableVirtualSpeaker() {
    auto audioHelper = ZoomVideoSDK::getInstance().getAudioHelper();
    
    static MyVirtualSpeaker virtualSpeaker;
    audioHelper->setExternalAudioReceiver(&virtualSpeaker);
}
```

## Complete Event Handler Example

```cpp
class FullEventHandler : public IZoomVideoSDKDelegate {
public:
    // Session lifecycle
    void onSessionJoin() override { /* ... */ }
    void onSessionLeave() override { /* ... */ }
    void onError(ZoomVideoSDKErrors errorCode) override { /* ... */ }
    
    // Users
    void onUserJoin(IZoomVideoSDKUserHelper*, IVideoSDKVector<IZoomVideoSDKUser*>*) override { /* ... */ }
    void onUserLeave(IZoomVideoSDKUserHelper*, IVideoSDKVector<IZoomVideoSDKUser*>*) override { /* ... */ }
    void onUserNameChanged(IZoomVideoSDKUser*) override { /* ... */ }
    void onUserActiveAudioChanged(IZoomVideoSDKAudioHelper*, IVideoSDKVector<IZoomVideoSDKUser*>*) override { /* ... */ }
    
    // Audio/Video
    void onUserAudioStatusChanged(IZoomVideoSDKAudioHelper*, IVideoSDKVector<IZoomVideoSDKUser*>*) override { /* ... */ }
    void onUserVideoStatusChanged(IZoomVideoSDKVideoHelper*, IVideoSDKVector<IZoomVideoSDKUser*>*) override { /* ... */ }
    
    // Screen share
    void onUserShareStatusChanged(IZoomVideoSDKShareHelper*, IZoomVideoSDKUser*, ZoomVideoSDKShareStatus) override { /* ... */ }
    
    // Chat
    void onChatNewMessageNotify(IZoomVideoSDKChatHelper*, IZoomVideoSDKChatMessage*) override { /* ... */ }
    
    // Command channel
    void onCommandReceived(IZoomVideoSDKUser*, const wchar_t*) override { /* ... */ }
    
    // Live transcription
    void onLiveTranscriptionStatus(ZoomVideoSDKLiveTranscriptionStatus) override { /* ... */ }
    void onLiveTranscriptionMsgReceived(const wchar_t*, IZoomVideoSDKUser*, ZoomVideoSDKLiveTranscriptionOperationType) override { /* ... */ }
    
    // Recording
    void onCloudRecordingStatus(ZoomVideoSDKRecordingStatus) override { /* ... */ }
};
```

## Resources

- **Windows docs**: https://developers.zoom.us/docs/video-sdk/windows/
- **API Reference**: https://marketplacefront.zoom.us/sdk/custom/windows/
- **Sample apps**: [zoom/videosdk-ui-toolkit-windows-sample](https://github.com/zoom/videosdk-ui-toolkit-windows-sample)
- **Community samples**: [tanchunsiong/ZoomVideoSDK](https://github.com/nicholasyiu/nicholasyiu.github.io)

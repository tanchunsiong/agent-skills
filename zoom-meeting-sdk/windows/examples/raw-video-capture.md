# Raw Video Capture Example

## Overview

This guide shows how to capture raw video data from Zoom meetings using the Windows Meeting SDK. Raw video data is provided in **YUV420 (I420) format**, which is the industry standard for video processing.

---

## Complete Workflow

### Step 1: Join Meeting Successfully

Before capturing video, you must:
1. ✅ Initialize SDK
2. ✅ Authenticate with JWT token
3. ✅ Join meeting successfully (`MEETING_STATUS_INMEETING`)

See [Authentication Pattern](authentication-pattern.md) for this setup.

---

### Step 2: Start Raw Recording

**CRITICAL**: You MUST call `StartRawRecording()` before you can capture video data.

```cpp
void OnInMeeting() {
    std::cout << "[VIDEO] In meeting! Starting video capture..." << std::endl;
    
    // Get recording controller
    IMeetingRecordingController* recordingCtrl = 
        meetingService->GetMeetingRecordingController();
    
    if (!recordingCtrl) {
        std::cerr << "[VIDEO] ERROR: Failed to get recording controller" << std::endl;
        return;
    }
    
    // Check if we can start recording
    SDKError canStart = recordingCtrl->CanStartRecording(false, 0);
    if (canStart != SDKERR_SUCCESS) {
        std::cerr << "[VIDEO] Cannot start recording: " << canStart << std::endl;
        return;
    }
    
    // Start raw recording (this enables raw data capture)
    SDKError err = recordingCtrl->StartRawRecording();
    if (err != SDKERR_SUCCESS) {
        std::cerr << "[VIDEO] StartRawRecording failed: " << err << std::endl;
        return;
    }
    
    std::cout << "[VIDEO] Raw recording started!" << std::endl;
    
    // Wait a moment for recording to initialize
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    
    // Continue to Step 3...
}
```

**Important notes**:
- `StartRawRecording()` does NOT create a recording file on disk
- It only enables raw data capture via SDK callbacks
- You need host/co-host permissions OR special SDK app privileges
- If you get `SDKERR_WRONG_USAGE`, you may lack permissions

---

### Step 3: Get Participant IDs

You need to know which user's video you want to capture:

```cpp
// Get participants controller
IMeetingParticipantsController* participantsCtrl = 
    meetingService->GetMeetingParticipantsController();

if (!participantsCtrl) {
    std::cerr << "[VIDEO] Failed to get participants controller" << std::endl;
    return;
}

// Get list of all participants
IList<unsigned int>* participantList = participantsCtrl->GetParticipantsList();

if (!participantList || participantList->GetCount() == 0) {
    std::cerr << "[VIDEO] No participants in meeting" << std::endl;
    return;
}

// Get first participant's user ID
uint32_t userId = participantList->GetItem(0);
std::cout << "[VIDEO] Found participant: " << userId << std::endl;

// You can also get the user's name:
IUserInfo* userInfo = participantsCtrl->GetUserByUserID(userId);
if (userInfo) {
    const wchar_t* userName = userInfo->GetUserName();
    std::wcout << L"[VIDEO] User name: " << userName << std::endl;
}
```

**How to capture specific users**:
- **All participants**: Loop through `participantList` and subscribe to each
- **Active speaker**: Use `IMeetingVideoController()->GetActiveVideoUserID()`
- **Yourself**: Use `IMeetingParticipantsController()->GetMySelfUser()->GetUserID()`
- **Specific name**: Loop and match `GetUserName()`

---

### Step 4: Implement Renderer Delegate

This class receives the video frames:

**ZoomSDKRendererDelegate.h**:
```cpp
#pragma once
#include <windows.h>
#include <cstdint>
#include <rawdata/rawdata_renderer_interface.h>
#include <zoom_sdk_raw_data_def.h>
#include <fstream>
#include <iostream>

using namespace ZOOM_SDK_NAMESPACE;

class ZoomSDKRendererDelegate : public IZoomSDKRendererDelegate {
public:
    ZoomSDKRendererDelegate();
    ~ZoomSDKRendererDelegate();
    
    // Called when a new video frame arrives
    void onRawDataFrameReceived(YUVRawDataI420* data) override;
    
    // Called when raw data status changes
    void onRawDataStatusChanged(RawDataStatus status) override;
    
    // Called before renderer is destroyed
    void onRendererBeDestroyed() override;

private:
    void SaveToRawYUVFile(YUVRawDataI420* data);
    int frameCount;
};
```

**ZoomSDKRendererDelegate.cpp**:
```cpp
#include "ZoomSDKRendererDelegate.h"

ZoomSDKRendererDelegate::ZoomSDKRendererDelegate() : frameCount(0) {
    std::cout << "[VIDEO] Renderer delegate created" << std::endl;
}

ZoomSDKRendererDelegate::~ZoomSDKRendererDelegate() {
    std::cout << "[VIDEO] Renderer destroyed. Total frames: " << frameCount << std::endl;
}

void ZoomSDKRendererDelegate::onRawDataFrameReceived(YUVRawDataI420* data) {
    if (!data) return;
    
    // Get frame dimensions
    int width = data->GetStreamWidth();
    int height = data->GetStreamHeight();
    
    // Get rotation (0, 90, 180, 270 degrees)
    int rotation = data->GetRotation();
    
    // Log every 30 frames (every ~1 second at 30fps)
    if (frameCount % 30 == 0) {
        std::cout << "[VIDEO] Frame " << frameCount 
                  << " - " << width << "x" << height 
                  << " (rotation: " << rotation << "°)" << std::endl;
    }
    
    // Process the frame (save to file, encode, analyze, etc.)
    SaveToRawYUVFile(data);
    
    frameCount++;
}

void ZoomSDKRendererDelegate::onRawDataStatusChanged(RawDataStatus status) {
    switch (status) {
        case RawData_On:
            std::cout << "[VIDEO] Raw data ON" << std::endl;
            break;
        case RawData_Off:
            std::cout << "[VIDEO] Raw data OFF" << std::endl;
            break;
        default:
            std::cout << "[VIDEO] Status: " << status << std::endl;
            break;
    }
}

void ZoomSDKRendererDelegate::onRendererBeDestroyed() {
    std::cout << "[VIDEO] Renderer being destroyed" << std::endl;
}

void ZoomSDKRendererDelegate::SaveToRawYUVFile(YUVRawDataI420* data) {
    // Open output file in append binary mode
    std::ofstream outputFile("output.yuv", std::ios::out | std::ios::binary | std::ios::app);
    if (!outputFile.is_open()) {
        std::cerr << "[VIDEO] Error opening output.yuv" << std::endl;
        return;
    }
    
    // YUV420 format: Y plane + U plane + V plane
    size_t ySize = data->GetStreamWidth() * data->GetStreamHeight();
    size_t uvSize = ySize / 4;  // U and V are quarter size each
    
    // Write planes in order: Y, U, V
    outputFile.write(data->GetYBuffer(), ySize);
    outputFile.write(data->GetUBuffer(), uvSize);
    outputFile.write(data->GetVBuffer(), uvSize);
    
    outputFile.close();
}
```

---

### Step 5: Create Renderer and Subscribe

```cpp
// Create renderer helper and delegate
IZoomSDKVideoSource* videoHelper = nullptr;
ZoomSDKRendererDelegate* videoDelegate = new ZoomSDKRendererDelegate();

SDKError err = createRenderer(&videoHelper, videoDelegate);
if (err != SDKERR_SUCCESS || !videoHelper) {
    std::cerr << "[VIDEO] Failed to create renderer: " << err << std::endl;
    delete videoDelegate;
    return;
}

// Set desired resolution (affects CPU/bandwidth usage)
videoHelper->setRawDataResolution(ZoomSDKResolution_720P);
// Other options: ZoomSDKResolution_90P, 180P, 360P, 720P, 1080P

// Subscribe to user's video stream
err = videoHelper->subscribe(userId, RAW_DATA_TYPE_VIDEO);
if (err != SDKERR_SUCCESS) {
    std::cerr << "[VIDEO] Subscribe failed: " << err << std::endl;
    return;
}

std::cout << "[VIDEO] Successfully subscribed! Frames will arrive in onRawDataFrameReceived()" << std::endl;
```

**Important notes**:
- Use `createRenderer()` (global function), not `CreateRenderer()` or `new`
- Set resolution BEFORE subscribing
- Higher resolutions = more CPU/bandwidth but better quality
- Frames arrive asynchronously in `onRawDataFrameReceived()`

---

## YUV420 (I420) Format Explained

### What is YUV420?

YUV420 separates image into:
- **Y (luma)**: Brightness information (full resolution)
- **U (Cb, blue-difference)**: Color information (quarter resolution)
- **V (Cr, red-difference)**: Color information (quarter resolution)

### Memory Layout

For a 1920x1080 frame:

```
Total bytes: 1920 * 1080 * 1.5 = 3,110,400 bytes

Y plane: [0 to 2,073,599]       (1920 * 1080 = 2,073,600 bytes)
U plane: [2,073,600 to 2,592,639]  (960 * 540 = 518,400 bytes)
V plane: [2,592,640 to 3,110,399]  (960 * 540 = 518,400 bytes)
```

**Formula**:
```cpp
size_t ySize = width * height;
size_t uSize = (width / 2) * (height / 2) = width * height / 4;
size_t vSize = (width / 2) * (height / 2) = width * height / 4;
size_t totalSize = ySize + uSize + vSize = width * height * 1.5;
```

### Accessing Frame Data

```cpp
void ProcessFrame(YUVRawDataI420* data) {
    int width = data->GetStreamWidth();    // e.g., 1920
    int height = data->GetStreamHeight();  // e.g., 1080
    
    // Get pointers to each plane
    const char* yBuffer = data->GetYBuffer();  // Brightness
    const char* uBuffer = data->GetUBuffer();  // Blue-difference
    const char* vBuffer = data->GetVBuffer();  // Red-difference
    
    // Calculate sizes
    size_t ySize = width * height;
    size_t uvSize = (width / 2) * (height / 2);
    
    // Example: Access pixel at (x, y)
    int x = 100, y = 50;
    
    // Y value (full resolution)
    unsigned char yValue = yBuffer[y * width + x];
    
    // U and V values (subsampled 2x2)
    unsigned char uValue = uBuffer[(y/2) * (width/2) + (x/2)];
    unsigned char vValue = vBuffer[(y/2) * (width/2) + (x/2)];
    
    std::cout << "Pixel (" << x << "," << y << "): "
              << "Y=" << (int)yValue << " "
              << "U=" << (int)uValue << " "
              << "V=" << (int)vValue << std::endl;
}
```

### Converting YUV420 to RGB

```cpp
void YUVtoRGB(unsigned char y, unsigned char u, unsigned char v, 
              unsigned char& r, unsigned char& g, unsigned char& b) {
    int c = y - 16;
    int d = u - 128;
    int e = v - 128;
    
    int red   = (298 * c + 409 * e + 128) >> 8;
    int green = (298 * c - 100 * d - 208 * e + 128) >> 8;
    int blue  = (298 * c + 516 * d + 128) >> 8;
    
    // Clamp to [0, 255]
    r = (red < 0) ? 0 : (red > 255) ? 255 : red;
    g = (green < 0) ? 0 : (green > 255) ? 255 : green;
    b = (blue < 0) ? 0 : (blue > 255) ? 255 : blue;
}
```

---

## Complete Example: Save to File

### Save Raw YUV File

```cpp
void SaveToRawYUVFile(YUVRawDataI420* data) {
    std::ofstream file("output.yuv", std::ios::binary | std::ios::app);
    
    size_t ySize = data->GetStreamWidth() * data->GetStreamHeight();
    size_t uvSize = ySize / 4;
    
    file.write(data->GetYBuffer(), ySize);
    file.write(data->GetUBuffer(), uvSize);
    file.write(data->GetVBuffer(), uvSize);
    
    file.close();
}
```

**Play back with ffplay**:
```bash
ffplay -f rawvideo -pixel_format yuv420p -video_size 1920x1080 -framerate 30 output.yuv
```

### Save as PNG Images (Using OpenCV)

```cpp
#include <opencv2/opencv.hpp>

void SaveAsPNG(YUVRawDataI420* data, int frameNumber) {
    int width = data->GetStreamWidth();
    int height = data->GetStreamHeight();
    
    // Create YUV Mat
    cv::Mat yuvImage(height + height/2, width, CV_8UC1);
    
    // Copy Y plane
    memcpy(yuvImage.data, data->GetYBuffer(), width * height);
    
    // Copy U plane
    memcpy(yuvImage.data + width * height, data->GetUBuffer(), width * height / 4);
    
    // Copy V plane
    memcpy(yuvImage.data + width * height * 5/4, data->GetVBuffer(), width * height / 4);
    
    // Convert to BGR
    cv::Mat bgrImage;
    cv::cvtColor(yuvImage, bgrImage, cv::COLOR_YUV2BGR_I420);
    
    // Save as PNG
    std::string filename = "frame_" + std::to_string(frameNumber) + ".png";
    cv::imwrite(filename, bgrImage);
}
```

---

## Handling Video Rotation

Video streams may be rotated (0°, 90°, 180°, 270°):

```cpp
void ProcessFrame(YUVRawDataI420* data) {
    int rotation = data->GetRotation();  // 0, 90, 180, or 270
    
    if (rotation == 0) {
        // Normal orientation, no rotation needed
        SaveFrame(data);
    } else {
        // Need to rotate frame before displaying/processing
        RotateFrame(data, rotation);
        SaveFrame(data);
    }
}
```

**OpenCV rotation**:
```cpp
cv::Mat RotateImage(cv::Mat& image, int rotation) {
    cv::Mat rotated;
    switch (rotation) {
        case 90:
            cv::rotate(image, rotated, cv::ROTATE_90_CLOCKWISE);
            break;
        case 180:
            cv::rotate(image, rotated, cv::ROTATE_180);
            break;
        case 270:
            cv::rotate(image, rotated, cv::ROTATE_90_COUNTERCLOCKWISE);
            break;
        default:
            rotated = image;
            break;
    }
    return rotated;
}
```

---

## Performance Considerations

### Frame Rate

Video typically arrives at:
- **720p**: ~30 fps
- **1080p**: ~30 fps
- **Lower resolutions**: ~15-30 fps

Process frames quickly to avoid dropping:
```cpp
void onRawDataFrameReceived(YUVRawDataI420* data) {
    // Fast: Just save to buffer/queue
    frameQueue.push(data);  // Process in separate thread
    
    // Slow: Heavy processing here
    ConvertToRGB(data);     // May drop frames!
    EncodeToH264(data);
    SaveToDisk(data);
}
```

### Memory Usage

**Per frame**:
- 720p (1280x720): 1.38 MB
- 1080p (1920x1080): 3.11 MB

**At 30 fps**:
- 720p: ~41 MB/sec
- 1080p: ~93 MB/sec

Use buffering and separate processing threads for high performance.

### Resolution Selection

```cpp
// Lower resolution = less CPU/bandwidth
videoHelper->setRawDataResolution(ZoomSDKResolution_360P);  // Good for analysis

// Higher resolution = better quality
videoHelper->setRawDataResolution(ZoomSDKResolution_1080P); // Good for recording
```

---

## Unsubscribing and Cleanup

### Stop Capturing Video

```cpp
// Unsubscribe from video stream
if (videoHelper) {
    videoHelper->unSubscribe(userId, RAW_DATA_TYPE_VIDEO);
}

// Stop raw recording
if (recordingCtrl) {
    recordingCtrl->StopRawRecording();
}
```

### Cleanup

```cpp
// Renderer delegate is automatically deleted by SDK
// Don't call delete on videoDelegate yourself!

// Just null out the pointer
videoHelper = nullptr;
videoDelegate = nullptr;
```

---

## Troubleshooting

### No Frames Received

**Checklist**:
- [ ] Called `StartRawRecording()` BEFORE subscribing
- [ ] Waited ~500ms after `StartRawRecording()` before subscribing
- [ ] User ID is valid (not 0, exists in participant list)
- [ ] User has their video turned on
- [ ] Subscribed to correct data type (`RAW_DATA_TYPE_VIDEO`)
- [ ] Renderer delegate implements `onRawDataFrameReceived()` correctly

**Test**: Subscribe to your own video stream first (easier to control)

### Frames Look Corrupted

**Checklist**:
- [ ] Using YUV420 (I420) format, not RGB
- [ ] Buffer size is `width * height * 1.5` bytes
- [ ] Writing/reading planes in correct order: Y, U, V
- [ ] U and V planes are quarter size each, not half size
- [ ] Handling rotation correctly

**Test**: Save raw YUV and play with ffplay to verify format

### Performance Issues / Dropped Frames

**Solutions**:
- Lower resolution: `setRawDataResolution(ZoomSDKResolution_360P)`
- Process frames in separate thread
- Use frame queue/buffer
- Skip frames if processing is slow (process every 2nd or 3rd frame)

---

## Complete Working Example

See the full working implementation in:
```
C:\tempsdk\zoom-windows-sdk-sample\src\
├── ZoomSDKRendererDelegate.h
├── ZoomSDKRendererDelegate.cpp
└── main.cpp (OnInMeeting function)
```

Key files to reference:
- Renderer delegate implementation
- Subscription workflow in `OnInMeeting()`
- YUV file saving logic

---

## Related Documentation

- [Authentication Pattern](authentication-pattern.md) - How to join meetings first
- [Windows Message Loop](../troubleshooting/windows-message-loop.md) - Required for callbacks
- [Interface Methods](../references/interface-methods.md) - Required virtual methods
- [Common Issues](../troubleshooting/common-issues.md) - Troubleshooting guide

---

**Last Updated**: Based on Zoom Windows Meeting SDK v6.7.2.26830

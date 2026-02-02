# Raw Recording

Access raw audio and video data from Zoom meetings and sessions for custom processing.

## Overview

Raw recording allows you to capture unprocessed audio and video frames directly from the SDK, enabling custom recording solutions, AI processing, and media pipelines.

## Platform Support

| Platform | Support Level | SDK |
|----------|---------------|-----|
| **Linux** | Primary | Meeting SDK, Video SDK |
| **Windows** | Primary | Meeting SDK, Video SDK |
| **macOS** | Primary | Meeting SDK, Video SDK |
| **iOS** | Light | Meeting SDK, Video SDK |
| **Android** | Light | Meeting SDK, Video SDK |
| **Web** | No native support | Use 3rd party browser recording; must call recording API for compliance notification |

## Desktop Platforms (Primary)

### Linux

```cpp
// Subscribe to raw audio
class AudioRawDataDelegate : public IZoomSDKAudioRawDataDelegate {
public:
    void onMixedAudioRawDataReceived(AudioRawData *data) override {
        // Format: 16-bit PCM, 16kHz or 32kHz, mono
        std::ofstream file("meeting.pcm", std::ios::binary | std::ios::app);
        file.write(data->GetBuffer(), data->GetBufferLen());
    }
};

// Subscribe to raw video
class VideoRawDataDelegate : public IZoomSDKRendererDelegate {
public:
    void onRawDataFrameReceived(YUVRawDataI420 *data) override {
        // Format: I420 (YUV 4:2:0)
        // Convert to BGR for OpenCV processing
        cv::Mat I420(data->GetStreamHeight() * 3/2, 
                   data->GetStreamWidth(), CV_8UC1, data->GetBuffer());
        cv::Mat colorFrame;
        cv::cvtColor(I420, colorFrame, cv::COLOR_YUV2BGR_I420);
        videoWriter.write(colorFrame);
    }
};

// Enable raw recording
auto recCtl = m_meetingService->GetMeetingRecordingController();
recCtl->StartRawRecording();

// Subscribe
GetAudioRawdataHelper()->subscribe(new AudioRawDataDelegate());
GetRawdataRendererHelper()->subscribe(userId, RAW_DATA_TYPE_VIDEO, new VideoRawDataDelegate());
```

### Windows

```cpp
// Same API as Linux
// Subscribe to raw data after joining meeting
auto* pRawDataHelper = GetAudioRawdataHelper();
pRawDataHelper->subscribe(new AudioRawDataDelegate());

auto* pVideoHelper = GetRawdataRendererHelper();
pVideoHelper->setRawDataResolution(ZoomSDKResolution_720P);
pVideoHelper->subscribe(userId, RAW_DATA_TYPE_VIDEO, new VideoRawDataDelegate());
```

### macOS

```swift
// Get raw data controller
let rawDataCtrl = ZoomSDK.shared().getRawDataController()

// Subscribe to audio
rawDataCtrl?.subscribeAudioRawData { audioData in
    // Process PCM audio
    let buffer = audioData.getBuffer()
    let length = audioData.getBufferLen()
}

// Subscribe to video
rawDataCtrl?.subscribeVideoRawData(forUser: userId) { videoData in
    // Process YUV frames
    let width = videoData.getStreamWidth()
    let height = videoData.getStreamHeight()
}
```

## Mobile Platforms (Light)

### iOS

Raw data access on iOS is more limited than desktop:

```swift
// Video raw data via ZoomVideoSDKVideoCanvas
let canvas = ZoomVideoSDKVideoCanvas()
canvas.delegate = self

// Implement delegate
func onRawDataFrameReceived(_ pixelBuffer: CVPixelBuffer) {
    // Process video frame
    // Note: Performance-intensive on mobile
}
```

**Limitations:**
- Higher battery consumption
- May impact app performance
- Not recommended for long recordings

### Android

```kotlin
// Video raw data via ZoomVideoSDKVideoCanvas
val canvas = ZoomVideoSDKVideoCanvas(context)
canvas.setDelegate(object : ZoomVideoSDKRawDataPipeDelegate {
    override fun onRawDataFrameReceived(rawData: ZoomVideoSDKVideoRawData) {
        // Process YUV frame
        // Note: Performance-intensive on mobile
    }
})
```

**Limitations:**
- Same as iOS - battery and performance concerns
- Consider cloud recording instead for mobile apps

## Web Platform

There is no native SDK support for raw recording on Web. For browser-based recording:

1. Use 3rd party browser recording solutions
2. **Important**: Call the recording API to trigger the "This meeting is being recorded" notification for compliance

## Common Use Cases

- Meeting bots for transcription
- Custom recording pipelines
- AI/ML processing (sentiment analysis, summarization)
- Media archival solutions

## Resources

- **Meeting SDK docs**: https://developers.zoom.us/docs/meeting-sdk/
- **Video SDK docs**: https://developers.zoom.us/docs/video-sdk/

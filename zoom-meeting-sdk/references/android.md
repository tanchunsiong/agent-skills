# Meeting SDK - Android

Embed Zoom meetings in Android apps.

## Overview

Native Android SDK for embedding the full Zoom meeting experience with WebRTC support.

## Prerequisites

- Meeting SDK downloaded from [Marketplace](https://marketplace.zoom.us/) (sign-in required)
- Android Studio
- Android 5.0+ (API 21+)
- Valid SDK credentials

## Installation

### Gradle

Add SDK AAR to your project after downloading from Marketplace.

```gradle
dependencies {
    implementation files('libs/mobilertc.aar')
    implementation files('libs/commonlib.aar')
}
```

## Quick Start

```kotlin
import us.zoom.sdk.*

// Initialize with JWT token
val initParams = ZoomSDKInitParams().apply {
    jwtToken = "your-jwt-token"     // JWT auth (recommended)
    domain = "zoom.us"
    enableLog = true
    enableGenerateDump = true
    logSize = 5
    videoRawDataMemoryMode = ZoomSDKRawDataMemoryMode.ZoomSDKRawDataMemoryModeStack
}
ZoomSDK.getInstance().initialize(context, object : ZoomSDKInitializeListener {
    override fun onZoomSDKInitializeResult(errorCode: Int, internalErrorCode: Int) {
        if (errorCode == ZoomError.ZOOM_ERROR_SUCCESS) {
            // SDK initialized successfully
        }
    }
    
    override fun onZoomAuthIdentityExpired() {
        // JWT expired, refresh token
    }
}, initParams)

// Join meeting
val joinParams = JoinMeetingParams().apply {
    meetingNo = meetingNumber
    displayName = "User"
    password = meetingPassword
    join_token = zakToken  // Optional: ZAK token for authentication
}
ZoomSDK.getInstance().meetingService.joinMeetingWithParams(context, joinParams, JoinMeetingOptions())

// Join by Vanity ID
val params = JoinMeetingParams().apply {
    vanityID = "company-meeting-room"
    displayName = "User"
    password = meetingPassword
}
```

## WebRTC Support

Meeting SDK Android supports WebRTC for improved real-time communication:
- Better audio/video quality
- Lower latency
- Adaptive streaming

## Listener Pattern

```kotlin
class MeetingListener : MeetingServiceListener {
    override fun onMeetingStatusChanged(
        meetingStatus: MeetingStatus?,
        errorCode: Int,
        internalErrorCode: Int
    ) {
        when (meetingStatus) {
            MeetingStatus.MEETING_STATUS_IDLE -> Log.d(TAG, "Idle")
            MeetingStatus.MEETING_STATUS_CONNECTING -> Log.d(TAG, "Connecting")
            MeetingStatus.MEETING_STATUS_INMEETING -> Log.d(TAG, "In meeting")
            else -> {}
        }
    }
}
```

## Common Tasks

### Custom UI Integration

```kotlin
// Enable Custom UI during initialization
val initParams = ZoomSDKInitParams().apply {
    enableCustomizedUI = true  // Enable custom UI
}
ZoomSDK.getInstance().initialize(context, this, initParams)

// Access custom UI service
val customUIService = ZoomSDK.getInstance().inMeetingService.inMeetingCustomUIService

// Build your own video layout
class CustomMeetingUI : AppCompatActivity() {
    private lateinit var videoContainer: FrameLayout
    
    fun setupVideoViews() {
        // Get video unit for active user
        val activeUserId = ZoomSDK.getInstance().inMeetingService.activeVideoUserID()
        val videoUnit = customUIService?.createVideoUnit(this)
        
        videoUnit?.let { unit ->
            videoContainer.addView(unit.asView())
            unit.subscribe(activeUserId)
        }
    }
}
```

### Audio/Video Controls

```kotlin
// Get in-meeting service
val inMeetingService = ZoomSDK.getInstance().inMeetingService
val audioController = inMeetingService.inMeetingAudioController
val videoController = inMeetingService.inMeetingVideoController

// Mute/unmute audio
fun toggleAudio() {
    val myUserId = inMeetingService.myUserID
    
    if (audioController.isMyAudioMuted) {
        audioController.muteMyAudio(false)  // Unmute
    } else {
        audioController.muteMyAudio(true)   // Mute
    }
}

// Start/stop video
fun toggleVideo() {
    if (videoController.isMyVideoMuted) {
        videoController.muteMyVideo(false)  // Start video
    } else {
        videoController.muteMyVideo(true)   // Stop video
    }
}

// Switch camera
fun switchCamera() {
    videoController.switchCamera()
}

// Select audio source
fun selectSpeaker(useSpeaker: Boolean) {
    audioController.setAudioOutputDevice(
        if (useSpeaker) AudioOutputDevice.Speaker 
        else AudioOutputDevice.Earpiece
    )
}
```

### Screen Sharing

```kotlin
// Start screen share
fun startScreenShare() {
    val shareController = ZoomSDK.getInstance().inMeetingService.inMeetingShareController
    
    if (shareController.isShareStartEnabled) {
        shareController.startShareScreenSession()
    }
}

// Stop screen share
fun stopScreenShare() {
    ZoomSDK.getInstance().inMeetingService.inMeetingShareController.stopShareScreen()
}

// Handle screen share intent (API 21+)
override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
    if (requestCode == SCREEN_SHARE_REQUEST_CODE && resultCode == RESULT_OK) {
        ZoomSDK.getInstance().inMeetingService
            .inMeetingShareController
            .startShareScreenSession(data)
    }
}
```

### Meeting Controls

```kotlin
// Leave meeting
fun leaveMeeting() {
    ZoomSDK.getInstance().inMeetingService.leaveCurrentMeeting(false)
}

// End meeting (host only)
fun endMeeting() {
    ZoomSDK.getInstance().inMeetingService.leaveCurrentMeeting(true)
}

// Get participant list
fun getParticipants(): List<InMeetingUserInfo> {
    val participants = mutableListOf<InMeetingUserInfo>()
    val userList = ZoomSDK.getInstance().inMeetingService.inMeetingUserList
    
    userList?.forEach { userId ->
        ZoomSDK.getInstance().inMeetingService.getUserInfoById(userId)?.let {
            participants.add(it)
        }
    }
    
    return participants
}

// Chat
fun sendChatMessage(message: String, userId: Long = 0) {
    // userId = 0 sends to everyone
    ZoomSDK.getInstance().inMeetingService
        .inMeetingChatController
        .sendChatToUser(userId, message)
}
```

## Raw Data (Virtual Video Source)

Send custom video frames using `ZoomSDKVideoSource`:

```java
public class VirtualVideoSource implements ZoomSDKVideoSource {
    private ZoomSDKVideoSender sender;
    private int fps = 25;
    private HandlerThread virtualSourceThread;
    private Handler virtualHandler;
    
    @Override
    public void onInitialize(ZoomSDKVideoSender sender, 
                             List<ZoomSDKVideoCapability> supportCapList, 
                             ZoomSDKVideoCapability suggestCap) {
        this.sender = sender;
        this.fps = suggestCap.getFrame();
        
        // Start sending frames
        virtualHandler.postDelayed(frameTask, 1000 / fps);
    }
    
    @Override
    public void onStartSend() {
        virtualHandler.postDelayed(frameTask, 1000 / fps);
    }
    
    @Override
    public void onStopSend() {
        virtualHandler.removeCallbacks(frameTask);
    }
    
    Runnable frameTask = () -> {
        if (sender != null) {
            ByteBuffer yuvData = // ... YUV I420 frame data
            sender.sendVideoFrame(yuvData, width, height, 
                yuvData.capacity(), 0, 
                ExternalSourceDataFormat.ExternalSourceDataFormat_I420_FULL);
            
            virtualHandler.postDelayed(frameTask, 1000 / fps);
        }
    };
}
```

### YUV Conversion Helper

```java
public class YUVConvert {
    public static byte[] convertBitmapToYuv(Bitmap bitmap) {
        int width = bitmap.getWidth();
        int height = bitmap.getHeight();
        int[] argb = new int[width * height];
        bitmap.getPixels(argb, 0, width, 0, 0, width, height);
        
        byte[] yuv = new byte[width * height * 3 / 2]; // I420 format
        // ... conversion logic
        return yuv;
    }
}
```

## Common Gotchas

- **Enum 0 = Success**: Check return values - 0 often means success
- **ProGuard/R8**: Disable for Zoom SDK classes or app may crash
- **Permissions**: Request CAMERA and RECORD_AUDIO before joining
- **Raw data memory mode**: Set `videoRawDataMemoryMode` in init params

## ProGuard Rules

Add these rules to `proguard-rules.pro`:

```proguard
-keep class us.zoom.** { *; }
-keep class com.zipow.** { *; }
-keep class us.zipow.** { *; }
-keep class org.webrtc.** { *; }
-keep class us.google.protobuf.** { *; }
-keep class com.google.crypto.tink.** { *; }
-keep class androidx.security.crypto.** { *; }
-keep class androidx.** { *; }
-keep class com.google.** { *; }

-dontwarn com.android.**
-dontwarn com.google.**
-dontwarn com.zipow.**
-dontwarn us.zoom.**
-dontwarn org.**
```

## Resources

- **Android docs**: https://developers.zoom.us/docs/meeting-sdk/android/
- **API Reference**: https://marketplacefront.zoom.us/sdk/meeting/android/

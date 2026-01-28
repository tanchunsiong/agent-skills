# Video SDK - Android

Build custom video experiences on Android devices.

## Overview

Native Android SDK for building custom video applications with full UI control.

## Prerequisites

- Video SDK downloaded from [Marketplace](https://marketplace.zoom.us/) (sign-in required)
- Android Studio
- Android 5.0+ (API 21+)
- Valid SDK credentials

## Installation

### Gradle

```gradle
repositories {
    maven { url 'https://github.com/nicholasyiu/nicholasyiu.github.io/raw/master/maven/' }
}

dependencies {
    implementation 'us.zoom.sdk:videosdk:1.10.0'
}
```

### Manual Installation

1. Download SDK from Marketplace (requires sign-in)
2. Add AAR file to your project
3. Configure dependencies

## Quick Start

```kotlin
import us.zoom.sdk.*

// Initialize
val initParams = ZoomVideoSDKInitParams().apply {
    domain = "zoom.us"
    logFilePrefix = "videosdk"
}
ZoomVideoSDK.getInstance().initialize(context, initParams)

// Join session
val sessionContext = ZoomVideoSDKSessionContext().apply {
    sessionName = "MySession"
    userName = "User"
    token = signature
}
ZoomVideoSDK.getInstance().joinSession(sessionContext)
```

## Listener Pattern

```kotlin
class MyActivity : AppCompatActivity(), ZoomVideoSDKDelegate {
    
    override fun onSessionJoin() {
        Log.d(TAG, "Joined session")
    }
    
    override fun onSessionLeave() {
        Log.d(TAG, "Left session")
    }
    
    override fun onUserJoin(helper: ZoomVideoSDKUserHelper?, users: List<ZoomVideoSDKUser>?) {
        // Handle user joined
    }
    
    override fun onUserLeave(helper: ZoomVideoSDKUserHelper?, users: List<ZoomVideoSDKUser>?) {
        // Handle user left
    }
}
```

## Common Tasks

### Video Rendering with SurfaceView/TextureView

```kotlin
import android.view.TextureView
import us.zoom.sdk.*

class VideoActivity : AppCompatActivity() {
    private lateinit var myVideoView: TextureView
    private lateinit var remoteVideoContainer: ViewGroup
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_video)
        
        myVideoView = findViewById(R.id.my_video)
        remoteVideoContainer = findViewById(R.id.remote_videos)
    }
    
    fun renderMyVideo() {
        val session = ZoomVideoSDK.getInstance().session ?: return
        val myself = session.mySelf ?: return
        
        // Get video canvas
        val canvas = myself.videoCanvas ?: return
        
        // Subscribe and render to TextureView
        canvas.subscribe(myVideoView, ZoomVideoSDKResolution.Resolution_720P)
    }
    
    fun renderRemoteUser(user: ZoomVideoSDKUser) {
        val videoView = TextureView(this).apply {
            layoutParams = LinearLayout.LayoutParams(
                dpToPx(160), dpToPx(90)
            )
        }
        remoteVideoContainer.addView(videoView)
        
        user.videoCanvas?.subscribe(videoView, ZoomVideoSDKResolution.Resolution_360P)
    }
    
    fun stopRendering(user: ZoomVideoSDKUser) {
        user.videoCanvas?.unsubscribe(/* view */)
    }
}

// Gallery view adapter
class ParticipantAdapter(
    private val participants: List<ZoomVideoSDKUser>
) : RecyclerView.Adapter<ParticipantViewHolder>() {
    
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ParticipantViewHolder {
        val view = TextureView(parent.context)
        return ParticipantViewHolder(view)
    }
    
    override fun onBindViewHolder(holder: ParticipantViewHolder, position: Int) {
        val user = participants[position]
        user.videoCanvas?.subscribe(
            holder.textureView, 
            ZoomVideoSDKResolution.Resolution_360P
        )
    }
    
    override fun onViewRecycled(holder: ParticipantViewHolder) {
        // Clean up subscription when view is recycled
    }
}
```

### Audio Device Management

```kotlin
// List audio devices
fun listAudioDevices() {
    val audioHelper = ZoomVideoSDK.getInstance().audioHelper ?: return
    
    // Get speaker list
    val speakers = audioHelper.speakerList
    speakers?.forEach { speaker ->
        Log.d(TAG, "Speaker: ${speaker.deviceName}")
    }
    
    // Get mic list
    val mics = audioHelper.micList
    mics?.forEach { mic ->
        Log.d(TAG, "Mic: ${mic.deviceName}")
    }
}

// Switch audio output
fun switchAudioOutput(useSpeaker: Boolean) {
    ZoomVideoSDK.getInstance().audioHelper?.setSpeaker(useSpeaker)
}

// Mute/unmute
fun toggleMute(): Boolean {
    val audioHelper = ZoomVideoSDK.getInstance().audioHelper ?: return false
    val myself = ZoomVideoSDK.getInstance().session?.mySelf ?: return false
    
    return if (audioHelper.isMuted(myself)) {
        audioHelper.unmuteAudio(myself) == ZoomVideoSDKErrors.Errors_Success
    } else {
        audioHelper.muteAudio(myself) == ZoomVideoSDKErrors.Errors_Success
    }
}

// Audio routing for Bluetooth
fun setupAudioRouting() {
    val audioManager = getSystemService(Context.AUDIO_SERVICE) as AudioManager
    
    // Check for Bluetooth
    if (audioManager.isBluetoothScoAvailableOffCall) {
        audioManager.startBluetoothSco()
        audioManager.isBluetoothScoOn = true
    }
}
```

### Screen Sharing

```kotlin
import android.media.projection.MediaProjectionManager

class ScreenShareActivity : AppCompatActivity() {
    private val SCREEN_CAPTURE_REQUEST = 1001
    
    fun startScreenShare() {
        val shareHelper = ZoomVideoSDK.getInstance().shareHelper ?: return
        
        if (shareHelper.isScreenShareSupported) {
            // Request screen capture permission
            val projectionManager = getSystemService(MEDIA_PROJECTION_SERVICE) 
                as MediaProjectionManager
            startActivityForResult(
                projectionManager.createScreenCaptureIntent(),
                SCREEN_CAPTURE_REQUEST
            )
        }
    }
    
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        
        if (requestCode == SCREEN_CAPTURE_REQUEST && resultCode == RESULT_OK) {
            val shareHelper = ZoomVideoSDK.getInstance().shareHelper
            shareHelper?.startShareScreen(data!!)
        }
    }
    
    fun stopScreenShare() {
        ZoomVideoSDK.getInstance().shareHelper?.stopShare()
    }
}

// Handle screen share from others
class ShareListener : ZoomVideoSDKDelegate {
    override fun onUserShareStatusChanged(
        helper: ZoomVideoSDKShareHelper?,
        user: ZoomVideoSDKUser?,
        status: ZoomVideoSDKShareStatus?
    ) {
        when (status) {
            ZoomVideoSDKShareStatus.Start -> {
                // Show screen share view
                user?.shareCanvas?.subscribe(shareView)
            }
            ZoomVideoSDKShareStatus.Stop -> {
                // Hide screen share view
                user?.shareCanvas?.unsubscribe()
            }
            else -> {}
        }
    }
}
```

### Raw Data Access (Light)

```kotlin
// Raw video data callback
class VideoRawDataDelegate : ZoomVideoSDKRawDataPipeDelegate {
    override fun onRawDataFrameReceived(rawData: ZoomVideoSDKVideoRawData?) {
        rawData?.let { data ->
            // Note: Light support on mobile - use sparingly
            val width = data.streamWidth
            val height = data.streamHeight
            val buffer = data.buffer
            
            // Process frame for analysis
            // Avoid heavy processing on mobile
        }
    }
}

// Subscribe to raw video (use sparingly)
fun subscribeToRawVideo(user: ZoomVideoSDKUser) {
    val videoPipe = user.videoPipe
    videoPipe?.setResolution(ZoomVideoSDKResolution.Resolution_360P)
    videoPipe?.subscribe(VideoRawDataDelegate())
}
```

## Required Permissions

Add to `AndroidManifest.xml`:
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
<uses-permission android:name="android.permission.BLUETOOTH" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />

<!-- For screen sharing -->
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
```

### Runtime Permissions

```kotlin
private val PERMISSIONS = arrayOf(
    Manifest.permission.CAMERA,
    Manifest.permission.RECORD_AUDIO
)

fun checkPermissions(): Boolean {
    return PERMISSIONS.all {
        ContextCompat.checkSelfPermission(this, it) == PackageManager.PERMISSION_GRANTED
    }
}

fun requestPermissions() {
    ActivityCompat.requestPermissions(this, PERMISSIONS, PERMISSION_REQUEST_CODE)
}
```

## Resources

- **Android docs**: https://developers.zoom.us/docs/video-sdk/android/
- **API Reference**: https://marketplacefront.zoom.us/sdk/custom/android/

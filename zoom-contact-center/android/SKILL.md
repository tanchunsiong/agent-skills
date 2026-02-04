# Contact Center SDK for Android

Native Android SDK for video and chat customer engagement.

> **Official docs:** https://developers.zoom.us/docs/contact-center/android/
> **SDK Download:** https://marketplace.zoom.us/ (Create Contact Center SDK app type)

## Requirements

- **Android 8.0+** (API 26+)
- Android Studio
- Contact Center license with [entry ID](https://support.zoom.us/hc/en-us/articles/4470447059597)
- SDK version **1.12.0+** (must update every 9 months)
- Supported architectures:
  - SDK 3.3.0+: `arm64-v8a`, `armeabi-v7a`
  - SDK 3.2.0 or earlier: `arm64-v8a`, `armeabi-v7a`, `x86`, `x86_64`

## Installation

Download SDK from Marketplace. The zip file `android-zccsdk-X.X.X.zip` contains:

| Folder | Contents | Required |
|--------|----------|----------|
| `cci/` | `cciSDK.aar`, `build.gradle` | Yes |
| `mobilertc/` | `mobilertc.aar`, `build.gradle` | Yes (for video) |
| `video-effects/` | `video-effects.aar`, `build.gradle` | Optional (blur) |
| `zm-annoter/` | `zm-annoter.aar`, `build.gradle` | Optional (annotation) |
| `sample/` | Sample project | Reference |
| `version.txt` | SDK version | Info |

### settings.gradle

```groovy
include ':app'

// Required: Contact Center SDK
include ':cci'
project(':cci').projectDir = new File(settingsDir, '../cci')

// Required for video: Video SDK
include ':mobilertc'
project(':mobilertc').projectDir = new File(settingsDir, '../mobilertc')

// Optional: Blur effects
include ':video-effects'
project(':video-effects').projectDir = new File(settingsDir, '../video-effects')

// Optional: Annotation
include ':zm-annoter'
project(':zm-annoter').projectDir = new File(settingsDir, '../zm-annoter')
```

### app/build.gradle

```groovy
android {
    namespace 'your.package.name'
    compileSdk 35
    
    defaultConfig {
        minSdk 26  // Required: minimum SDK 26
        targetSdk 35
    }
    
    // Required: cci and mobilertc share native libs
    packagingOptions {
        pickFirst 'lib/*/libzReflection.so'
        pickFirst 'lib/*/libc++_shared.so'
        pickFirst 'lib/*/libcrypto_sb.so'
        pickFirst 'lib/*/libssl_sb.so'
        pickFirst 'lib/*/libzoom_util.so'
        pickFirst 'lib/*/libcmmlib.so'
        pickFirst 'lib/*/libzlib.so'
    }
    
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
    
    kotlinOptions {
        jvmTarget = '17'
    }
    
    // Required: cci module needs viewBinding
    // Alternative: add dependencies.add("default","androidx.databinding:viewbinding:7.3.1") to cci/build.gradle
    buildFeatures {
        buildConfig = true
        viewBinding true
    }
}

dependencies {
    implementation project(':cci')
    implementation project(':mobilertc')           // For video
    implementation project(':video-effects')       // Optional: blur
    implementation project(':zm-annoter')          // Optional: annotation
}
```

### project/build.gradle

```groovy
buildscript {
    dependencies {
        classpath "com.android.tools.build:gradle:8.2.2"
    }
}
```

### proguard-rules.pro

```proguard
-keep class us.zoom** { *; }
-keep interface us.zoom** { *; }
-keep class org.webrtc** { *; }
-keep class com.zipow** { *; }
```

## Quick Start

### 1. Initialize SDK (Application)

**Kotlin:**
```kotlin
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        ZoomCCInterface.INSTANCE.init(this, "User Name")
    }
}
```

**Java:**
```java
public class MyApplication extends Application {
    @Override
    public void onCreate() {
        super.onCreate();
        ZoomCCInterface.INSTANCE.init(getApplicationContext(), "User Name");
    }
}
```

### 2. AndroidManifest.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">
    
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-feature android:glEsVersion="0x00020000" />
    
    <application
        android:name=".MyApplication"
        tools:replace="android:allowBackup"
        android:allowBackup="true">
        <!-- Activities -->
    </application>
</manifest>
```

### 3. Start Chat Engagement

**Kotlin:**
```kotlin
private fun createChatEntry() {
    // 1. Get chat service
    var service = ZoomCCInterface.getZoomCCChatService()
    
    // 2. Configure with ZoomCCItem
    service.init(
        ZoomCCItem(
            entryId = "your-chat-entry-id",
            sdkType = ZoomCCIInterfaceType.CHAT,
            serverType = CCServerType.CCServerWWW
        )
    )
    
    // 3. Add listener
    service.addListener(object : ZoomCCChatListener {
        override fun unreadMsgCountChanged(count: Int) {
            // Update UI with unread count
        }
        override fun onClientEvent(event: ClientEvent) {}
        override fun onEngagementEnd(engagementId: String) {}
        override fun onEngagementStart(engagementId: String) {}
        override fun onLoginStatus(status: IMStatus?) {}
        override fun onError(error: Int, detail: Long, description: String) {}
    })
}

private fun joinOrCreateChatSession() {
    // 4. Show chat UI
    val service = ZoomCCInterface.getZoomCCChatService()
    service.fetchUI()
}
```

### 4. Start Video Engagement

**Kotlin:**
```kotlin
private fun createVideoEntry() {
    var service = ZoomCCInterface.getZoomCCVideoService()
    
    service.init(
        ZoomCCItem(
            entryId = "your-video-entry-id",
            sdkType = ZoomCCIInterfaceType.VIDEO,
            serverType = CCServerType.CCServerWWW
        )
    )
    
    service.addListener(object : ZoomCCVideoListener {
        override fun unreadMsgCountChanged(count: Int) {}
        override fun onClientEvent(event: ClientEvent) {}
        override fun onEngagementEnd(engagementId: String) {}
        override fun onEngagementStart(engagementId: String) {}
        override fun onLoginStatus(status: IMStatus?) {}
        override fun onError(error: Int, detail: Long, description: String) {}
    })
}

private fun joinOrCreateSession() {
    val service = ZoomCCInterface.getZoomCCVideoService()
    service.fetchUI()
}
```

### 5. Start ZVA (Virtual Agent)

**Kotlin:**
```kotlin
private fun createZVAEntry() {
    var service = ZoomCCInterface.getZoomCCZVAService()
    
    service.init(
        ZoomCCItem(
            entryId = "your-zva-entry-id",
            sdkType = ZoomCCIInterfaceType.ZVA,
            serverType = CCServerType.CCServerWWW
        )
    )
    
    service.addListener(object : ZoomCCChatListener {
        override fun unreadMsgCountChanged(count: Int) {}
        override fun onClientEvent(event: ClientEvent) {}
        override fun onEngagementEnd(engagementId: String) {}
        override fun onEngagementStart(engagementId: String) {}
        override fun onLoginStatus(status: IMStatus?) {}
        override fun onError(error: Int, detail: Long, description: String) {}
    })
}

private fun joinOrCreateZVASession() {
    val service = ZoomCCInterface.getZoomCCZVAService()
    service.fetchUI()
}
```

### 6. Scheduled Callback

**Kotlin:**
```kotlin
private fun scheduledCallback() {
    val service = ZoomCCInterface.getZoomCCScheduledCallbackService()
    
    service.init(
        ZoomCCItem(
            apiKey = "your-api-key",
            sdkType = ZoomCCIInterfaceType.SCHEDULED_CALLBACK,
            serverType = CCServerType.CCServerWWW
        )
    )
    
    service.fetchUI()
}
```

## Available Services

| Service | SDK Type | Description |
|---------|----------|-------------|
| `getZoomCCChatService()` | `CHAT` | Text chat with agents |
| `getZoomCCVideoService()` | `VIDEO` | Video calls with agents |
| `getZoomCCZVAService()` | `ZVA` | Zoom Virtual Agent (AI chatbot) |
| `getZoomCCScheduledCallbackService()` | `SCHEDULED_CALLBACK` | Schedule callback requests |

## ZoomCCItem Configuration

```kotlin
ZoomCCItem(
    entryId = "your-entry-id",           // From Contact Center Management
    apiKey = "your-api-key",             // For scheduled callbacks & campaigns
    sdkType = ZoomCCIInterfaceType.CHAT, // CHAT, VIDEO, ZVA, SCHEDULED_CALLBACK
    serverType = CCServerType.CCServerWWW,
    useCampaignMode = false,             // Enable for Web Campaigns
    campaignInfo = null                  // Set when using campaign mode
)
```

## Listeners

### ZoomCCChatListener

```kotlin
interface ZoomCCChatListener {
    fun unreadMsgCountChanged(count: Int)
    fun onClientEvent(event: ClientEvent)
    fun onEngagementEnd(engagementId: String)
    fun onEngagementStart(engagementId: String)
    fun onLoginStatus(status: IMStatus?)
    fun onError(error: Int, detail: Long, description: String)
}
```

### ZoomCCVideoListener

```kotlin
interface ZoomCCVideoListener {
    fun unreadMsgCountChanged(count: Int)
    fun onClientEvent(event: ClientEvent)
    fun onEngagementEnd(engagementId: String)
    fun onEngagementStart(engagementId: String)
    fun onLoginStatus(status: IMStatus?)
    fun onError(error: Int, detail: Long, description: String)
}
```

## Logout & Release

```kotlin
// Logout services
val chatService = ZoomCCInterface.getZoomCCChatService()
chatService.logoff()

val videoService = ZoomCCInterface.getZoomCCVideoService()
videoService.logoff()

val zvaService = ZoomCCInterface.getZoomCCZVAService()
zvaService.logoff()

// Release resources on destroy
override fun onDestroy() {
    ZoomCCInterface.releaseZoomCCService(chatEntryId)
    ZoomCCInterface.releaseZoomCCService(videoEntryId)
    ZoomCCInterface.releaseZoomCCService(zvaEntryId)
    ZoomCCInterface.releaseZoomCCService(apiKey)
    super.onDestroy()
}
```

## Change User Name

```kotlin
// Option 1: During init
ZoomCCInterface.INSTANCE.init(context, "New User Name")

// Option 2: Before fetchUI
ZoomCCInterface.INSTANCE.setContext(ZoomCCContext("New User Name"))
```

## Web Campaigns

```kotlin
private fun createWebCampaign() {
    val intent = Intent(this, CampaignActivity::class.java).apply {
        putExtra("API_KEY", campaignApiKey)
        putExtra("SERVER_TYPE", CCServerType.CCServerWWW.value)
    }
    startActivity(intent)
}
```

## Deep Link for Rejoin

Configure in AndroidManifest.xml:

```xml
<activity
    android:name="us.zoom.contactscenter.activity.CCRejoinActivity"
    android:exported="true">
    <!-- Deep link -->
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:host="rejoin" android:scheme="myscheme" />
    </intent-filter>
    <!-- App link -->
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data
            android:host="your-domain.com"
            android:pathPattern="/rejoin/.*"
            android:scheme="https" />
    </intent-filter>
</activity>
```

## Server Types

| Server | Use Case |
|--------|----------|
| `CCServerWWW` | Default (US cluster) |
| `CCServerEU01` | Europe cluster |

## Resources

- **Get Started:** https://developers.zoom.us/docs/contact-center/android/get-started/
- **Chat:** https://developers.zoom.us/docs/contact-center/android/chat/
- **Video:** https://developers.zoom.us/docs/contact-center/android/video/
- **Rejoin:** See `sample/docs/rejoin.md` in SDK download

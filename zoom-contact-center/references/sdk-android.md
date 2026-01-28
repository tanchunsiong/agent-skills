# Contact Center - Android SDK

Native Android Contact Center integration.

## Overview

Integrate Zoom Contact Center into Android apps.

## Prerequisites

- Zoom Contact Center license
- SDK downloaded from [Marketplace](https://marketplace.zoom.us/) (sign-in required)
- Android Studio
- Android 5.0+ (API 21+)

## Installation

1. Download SDK from Marketplace (requires sign-in)
2. Add AAR to your project
3. Configure dependencies

## Quick Start

```kotlin
import com.zoom.contactcenter.*

// Initialize
val config = ZCCConfig().apply {
    clientId = "YOUR_CLIENT_ID"
    domain = "your-domain.zoom.us"
}
ZoomContactCenter.getInstance().initialize(context, config)

// Start engagement
val request = ZCCEngagementRequest().apply {
    queueId = "QUEUE_ID"
    customerName = "Customer Name"
}
ZoomContactCenter.getInstance().startEngagement(request)
```

## Listener Pattern

```kotlin
class ContactCenterListener : ZCCListener {
    override fun onEngagementStarted(engagement: ZCCEngagement) {
        Log.d(TAG, "Engagement started")
    }
    
    override fun onEngagementEnded(engagement: ZCCEngagement) {
        Log.d(TAG, "Engagement ended")
    }
    
    override fun onAgentJoined(agent: ZCCAgent) {
        Log.d(TAG, "Agent joined: ${agent.name}")
    }
}
```

## Common Tasks

### Starting Video Engagement

```kotlin
import com.zoom.contactcenter.*

class ContactCenterManager(private val context: Context) {
    
    fun startVideoEngagement(customerInfo: CustomerInfo, queueId: String) {
        val request = ZCCEngagementRequest().apply {
            this.queueId = queueId
            this.customerName = customerInfo.name
            this.customerEmail = customerInfo.email
            this.customerPhone = customerInfo.phone
            this.engagementType = ZCCEngagementType.VIDEO
            
            // Custom metadata
            this.metadata = mapOf(
                "accountId" to customerInfo.accountId,
                "orderNumber" to customerInfo.orderNumber
            )
        }
        
        ZoomContactCenter.getInstance().startEngagement(request, object : ZCCCallback<ZCCEngagement> {
            override fun onSuccess(engagement: ZCCEngagement) {
                handleEngagementStarted(engagement)
            }
            
            override fun onError(error: ZCCError) {
                handleError(error)
            }
        })
    }
    
    private fun handleError(error: ZCCError) {
        val message = when (error.code) {
            ZCCErrorCode.QUEUE_CLOSED -> "Support is currently closed"
            ZCCErrorCode.NO_AGENTS_AVAILABLE -> "All agents are busy"
            ZCCErrorCode.QUEUE_FULL -> "Queue is full"
            else -> "Unable to connect"
        }
        showAlert(message)
    }
}
```

### Firebase Cloud Messaging Integration

```kotlin
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage

class ContactCenterMessagingService : FirebaseMessagingService() {
    
    override fun onNewToken(token: String) {
        // Register token with Zoom Contact Center
        ZoomContactCenter.getInstance().registerPushToken(token)
    }
    
    override fun onMessageReceived(message: RemoteMessage) {
        val data = message.data
        
        if (data.containsKey("engagementId")) {
            // Handle Contact Center notification
            val engagementId = data["engagementId"]
            
            // Show notification
            showNotification(
                title = data["title"] ?: "Support",
                body = data["body"] ?: "You have a new message"
            )
            
            // Or resume engagement directly
            ZoomContactCenter.getInstance().resumeEngagement(engagementId!!)
        }
    }
    
    private fun showNotification(title: String, body: String) {
        val intent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        }
        
        val pendingIntent = PendingIntent.getActivity(
            this, 0, intent,
            PendingIntent.FLAG_IMMUTABLE
        )
        
        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_support)
            .setContentTitle(title)
            .setContentText(body)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .build()
        
        NotificationManagerCompat.from(this).notify(NOTIFICATION_ID, notification)
    }
}
```

### Voice and Video Controls

```kotlin
// Toggle video
fun toggleVideo() {
    ZoomContactCenter.getInstance().toggleVideo { isVideoOn ->
        runOnUiThread {
            updateVideoButton(isVideoOn)
        }
    }
}

// Toggle mute
fun toggleMute() {
    ZoomContactCenter.getInstance().toggleMute { isMuted ->
        runOnUiThread {
            updateMuteButton(isMuted)
        }
    }
}

// Switch camera
fun switchCamera() {
    ZoomContactCenter.getInstance().switchCamera()
}

// End engagement
fun endCall() {
    ZoomContactCenter.getInstance().endEngagement { result ->
        runOnUiThread {
            showSurvey()
        }
    }
}
```

### Chat Integration

```kotlin
// Send message
fun sendMessage(text: String) {
    ZoomContactCenter.getInstance().sendChatMessage(text, object : ZCCCallback<Unit> {
        override fun onSuccess(result: Unit) {
            clearMessageInput()
        }
        
        override fun onError(error: ZCCError) {
            showError(error)
        }
    })
}

// Chat listener
class ChatListener : ZCCChatListener {
    override fun onMessageReceived(message: ZCCChatMessage) {
        runOnUiThread {
            displayMessage(message)
        }
    }
    
    override fun onAgentTyping(isTyping: Boolean) {
        runOnUiThread {
            showTypingIndicator(isTyping)
        }
    }
}

// Register listener
ZoomContactCenter.getInstance().addChatListener(ChatListener())
```

### Foreground Service for Active Calls

```kotlin
// Service for keeping call alive in background
class ContactCenterService : Service() {
    
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val notification = createNotification()
        startForeground(NOTIFICATION_ID, notification)
        return START_STICKY
    }
    
    private fun createNotification(): Notification {
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("Support Call Active")
            .setContentText("Tap to return to call")
            .setSmallIcon(R.drawable.ic_call)
            .setOngoing(true)
            .build()
    }
    
    override fun onBind(intent: Intent?): IBinder? = null
}

// Start service when engagement starts
fun onEngagementStarted() {
    val intent = Intent(this, ContactCenterService::class.java)
    startForegroundService(intent)
}
```

## Required Permissions

Add to `AndroidManifest.xml`:
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />

<service
    android:name=".ContactCenterService"
    android:foregroundServiceType="mediaPlayback" />
```

## Resources

- **Contact Center docs**: https://developers.zoom.us/docs/contact-center/

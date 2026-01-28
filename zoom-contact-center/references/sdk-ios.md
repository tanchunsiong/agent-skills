# Contact Center - iOS SDK

Native iOS Contact Center integration.

## Overview

Integrate Zoom Contact Center into iPhone and iPad apps.

## Prerequisites

- Zoom Contact Center license
- SDK downloaded from [Marketplace](https://marketplace.zoom.us/) (sign-in required)
- Xcode 13+
- iOS 12.0+

## Installation

1. Download SDK from Marketplace (requires sign-in)
2. Add framework to your project
3. Configure entitlements

## Quick Start

```swift
import ZoomContactCenterSDK

// Initialize
let config = ZCCConfig()
config.clientId = "YOUR_CLIENT_ID"
config.domain = "your-domain.zoom.us"
ZoomContactCenter.shared.initialize(config)

// Start engagement
let request = ZCCEngagementRequest()
request.queueId = "QUEUE_ID"
request.customerName = "Customer Name"
ZoomContactCenter.shared.startEngagement(request)
```

## Delegate Pattern

```swift
class ContactCenterDelegate: ZCCDelegate {
    func engagementDidStart(_ engagement: ZCCEngagement) {
        print("Engagement started")
    }
    
    func engagementDidEnd(_ engagement: ZCCEngagement) {
        print("Engagement ended")
    }
    
    func agentDidJoin(_ agent: ZCCAgent) {
        print("Agent joined: \(agent.name)")
    }
}
```

## Common Tasks

### Starting Video Engagement

```swift
import ZoomContactCenterSDK

class ContactCenterManager {
    func startVideoEngagement(customerInfo: CustomerInfo, queueId: String) {
        let request = ZCCEngagementRequest()
        request.queueId = queueId
        request.customerName = customerInfo.name
        request.customerEmail = customerInfo.email
        request.customerPhone = customerInfo.phone
        request.engagementType = .video
        
        // Custom metadata for agent
        request.metadata = [
            "accountId": customerInfo.accountId,
            "orderNumber": customerInfo.orderNumber
        ]
        
        ZoomContactCenter.shared.startEngagement(request) { result in
            switch result {
            case .success(let engagement):
                self.handleEngagementStarted(engagement)
            case .failure(let error):
                self.handleError(error)
            }
        }
    }
    
    private func handleError(_ error: ZCCError) {
        switch error.code {
        case .queueClosed:
            showAlert("Support is currently closed")
        case .noAgentsAvailable:
            showAlert("All agents are busy")
        default:
            showAlert("Unable to connect")
        }
    }
}
```

### Push Notification Integration

```swift
import UserNotifications

// Register for push notifications
func registerForPushNotifications() {
    UNUserNotificationCenter.current().requestAuthorization(
        options: [.alert, .sound, .badge]
    ) { granted, error in
        guard granted else { return }
        
        DispatchQueue.main.async {
            UIApplication.shared.registerForRemoteNotifications()
        }
    }
}

// Handle device token
func application(_ application: UIApplication,
                 didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data) {
    // Register token with Zoom Contact Center
    ZoomContactCenter.shared.registerPushToken(deviceToken)
}

// Handle incoming notification
func userNotificationCenter(_ center: UNUserNotificationCenter,
                           didReceive response: UNNotificationResponse) {
    let userInfo = response.notification.request.content.userInfo
    
    if let engagementId = userInfo["engagementId"] as? String {
        // Resume engagement
        ZoomContactCenter.shared.resumeEngagement(engagementId)
    }
}
```

### Voice and Video Controls

```swift
// Toggle video
func toggleVideo() {
    ZoomContactCenter.shared.toggleVideo { isVideoOn in
        updateVideoButton(isOn: isVideoOn)
    }
}

// Toggle audio mute
func toggleMute() {
    ZoomContactCenter.shared.toggleMute { isMuted in
        updateMuteButton(isMuted: isMuted)
    }
}

// Switch camera
func switchCamera() {
    ZoomContactCenter.shared.switchCamera()
}

// End engagement
func endCall() {
    ZoomContactCenter.shared.endEngagement { result in
        self.showSurvey()
    }
}
```

### Chat Integration

```swift
// Send text message
func sendMessage(_ text: String) {
    ZoomContactCenter.shared.sendChatMessage(text) { result in
        switch result {
        case .success:
            self.clearMessageInput()
        case .failure(let error):
            self.showError(error)
        }
    }
}

// Receive messages
class ChatDelegate: ZCCChatDelegate {
    func didReceiveMessage(_ message: ZCCChatMessage) {
        DispatchQueue.main.async {
            self.displayMessage(message)
        }
    }
    
    func agentIsTyping(_ isTyping: Bool) {
        DispatchQueue.main.async {
            self.showTypingIndicator(isTyping)
        }
    }
}
```

## Required Permissions

Add to `Info.plist`:
```xml
<key>NSCameraUsageDescription</key>
<string>Camera for video support calls</string>
<key>NSMicrophoneUsageDescription</key>
<string>Microphone for support calls</string>
```

## Resources

- **Contact Center docs**: https://developers.zoom.us/docs/contact-center/

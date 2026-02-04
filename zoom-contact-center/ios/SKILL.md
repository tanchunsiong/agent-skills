# Contact Center SDK for iOS

Native iOS SDK for video and chat customer engagement.

> **Parent skill:** [zoom-contact-center](../SKILL.md)
> **Official docs:** https://developers.zoom.us/docs/contact-center/ios/
> **SDK Download:** https://marketplace.zoom.us/ (Create Contact Center SDK app type)

## Requirements

- Physical 64-bit iOS device (iPhone or iPad) with **iOS 13.0+**
- Contact Center license with [entry ID](https://support.zoom.us/hc/en-us/articles/4470447059597)
- SDK version **1.12.0+** (must update every 9 months)
- Bitcode NOT supported
- 32-bit devices NOT supported (since v1.4.0)

## Installation

Download SDK from Marketplace and drag these files into your Xcode project:

| File | Required | Description |
|------|----------|-------------|
| `ZoomCCSDK.framework` | Yes | Contact Center SDK |
| `ZoomVideoSDK.framework` | Yes | Video SDK (dependency) |
| `ZoomCCSDKResources.bundle` | Yes | SDK resources |
| `CptShare.xcframework` | Yes | Sharing support |
| `ZoomVideoSDKScreenShare.xcframework` | Optional | Mobile screen sharing |
| `zm_annoter_dynamic.xcframework` | Optional | Annotation during screen sharing |

Add frameworks under **Targets > General > Embedded Binaries**.

## Quick Start

### 1. Import SDK

**Swift:**
```swift
import ZoomCCSDK

let APP_GROUPID = "<#Your App group id#>"
let APP_DEVICE_SHARE_BUNDLE_ID = "<#Your App share screen extension bundle id#>"
let APP_CHAT_ENTRY_ID = "<#Your App chat entry id#>"
let APP_VIDEO_ENTRY_ID = "<#Your App video entry id#>"
let APP_USER_NAME = "<#Your App user name#>"
```

**Objective-C:**
```objc
#import <ZoomCCSDK/ZoomCCSDK.h>

#define APP_GROUPID @"<#Your app group id#>"
#define APP_DEVICE_SHARE_BUNDLE_ID @"<#Your app share extension bundle id#>"
#define APP_CHAT_ENTRY_ID @"<#Your app chat entry id#>"
#define APP_VIDEO_ENTRY_ID @"<#Your app video entry id#>"
#define APP_USR_NAME @"<#Your app user name#>"
```

### 2. Set Up Context

**Swift:**
```swift
func configCCSDKContext() {
    let userContext = ZoomCCContext.init()
    userContext.cacheFolder = NSSearchPathForDirectoriesInDomains(.documentDirectory, .userDomainMask, true).first!
    userContext.appGroupID = APP_GROUPID
    userContext.deviceShareBundleID = APP_DEVICE_SHARE_BUNDLE_ID
    userContext.userName = APP_USER_NAME
    // Default is US01. Use EU01 for Europe cluster
    userContext.domainType = .US01
    ZoomCCInterface.sharedInstance().context = userContext
}
```

**Objective-C:**
```objc
ZoomCCContext *userContext = [[ZoomCCContext alloc] init];
userContext.cacheFolder = [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) firstObject];
userContext.appGroupID = APP_GROUPID;
userContext.deviceShareBundleID = APP_DEVICE_SHARE_BUNDLE_ID;
userContext.userName = APP_USR_NAME;
userContext.domainType = ZoomCCSDKDomainType_US01;
[[ZoomCCInterface sharedInstance] setContext:userContext];
```

### 3. Start Chat Engagement

**Swift:**
```swift
func showChatChannel() {
    // 1. Create ZoomCCItem with chat configuration
    let item = ZoomCCItem.init()
    item.sdkType = .chat
    item.entryId = APP_CHAT_ENTRY_ID
    
    // 2. Get chat service and set delegate
    let chatService = ZoomCCInterface.sharedInstance().chatService()
    chatService.chatDelegate = self
    
    // 3. Initialize and login
    if (chatService.status == .initial) {
        chatService.initialize(with: item)
        chatService.login()
    }
    
    // 4. Show chat UI
    chatService.fetchUI { vc in
        if let vc = vc {
            self.navigationController?.pushViewController(vc, animated: true)
        }
    }
}
```

### 4. Start Video Engagement

**Swift:**
```swift
func showVideoChannel() {
    // 1. Create ZoomCCItem with video configuration
    let item = ZoomCCItem.init()
    item.sdkType = .video
    item.entryId = APP_VIDEO_ENTRY_ID
    
    // 2. Get video service and set delegate
    let videoService = ZoomCCInterface.sharedInstance().videoService()
    videoService.videoDelegate = self
    
    // 3. Initialize
    if (videoService.status == .initial) {
        videoService.initialize(with: item)
    }
    
    // 4. Show video UI (auto-joins when ready)
    videoService.fetchUI { vc in
        if let vc = vc {
            self.navigationController?.pushViewController(vc, animated: true)
        }
    }
}
```

## Available Services

| Service | SDK Type | Description |
|---------|----------|-------------|
| `chatService()` | `.chat` | Text chat with agents |
| `videoService()` | `.video` | Video calls with agents |
| `zvaService()` | `.ZVA` | Zoom Virtual Agent (AI chatbot) |
| `scheduledCallbackService()` | `.scheduledCallback` | Schedule callback requests |

## ZoomCCItem Configuration

```swift
let item = ZoomCCItem.init()
item.sdkType = .chat              // .chat, .video, .ZVA, .scheduledCallback
item.entryId = "your-entry-id"    // From Contact Center Management
item.apiKey = "your-api-key"      // For scheduled callbacks & campaigns
item.useCampaignMode = false      // Enable for Web Campaigns
item.campaignInfo = nil           // Set when using campaign mode
```

## Delegates

### ZoomCCChatServiceDelegate

```swift
extension ViewController: ZoomCCChatServiceDelegate {
    func onChatService(_ service: ZoomCCChatService, unreadMsgCountChanged count: UInt) {
        // Update unread badge
    }
    
    func onService(_ service: ZoomCCService, engagementStart engagementId: String) {
        // Engagement started
    }
    
    func onService(_ service: ZoomCCService, engagementEnd engagementId: String) {
        // Engagement ended
    }
    
    func onService(_ service: ZoomCCService, error: UInt, detail: Int, description: String?) {
        // Handle error
    }
    
    func onService(_ service: ZoomCCService, loginStatusChanged status: ZoomCCSDKStatus) {
        // Login status changed
    }
}
```

### ZoomCCVideoServiceDelegate

```swift
extension ViewController: ZoomCCVideoServiceDelegate {
    func onService(_ service: ZoomCCService, engagementStart engagementId: String) {
        // Video engagement started
    }
    
    func onService(_ service: ZoomCCService, engagementEnd engagementId: String) {
        // Video engagement ended
    }
    
    func onService(_ service: ZoomCCService, error: UInt, detail: Int, description: String?) {
        // Handle error
    }
}
```

## End Service

```swift
// End chat
let chatService = ZoomCCInterface.sharedInstance().chatService()
chatService.endChat()

// End video
let videoService = ZoomCCInterface.sharedInstance().videoService()
videoService.endVideo()

// End ZVA
let zvaService = ZoomCCInterface.sharedInstance().zvaService()
zvaService.endChat()

// End scheduled callback
let scheduleService = ZoomCCInterface.sharedInstance().scheduledCallbackService()
scheduleService.endScheduledCallback()
```

## AppDelegate Lifecycle

```swift
@main
class AppDelegate: UIResponder, UIApplicationDelegate {
    
    func applicationDidBecomeActive(_ application: UIApplication) {
        ZoomCCInterface.sharedInstance().appDidBecomeActive()
    }
    
    func applicationWillTerminate(_ application: UIApplication) {
        ZoomCCInterface.sharedInstance().appWillTerminate()
    }
    
    func applicationWillResignActive(_ application: UIApplication) {
        ZoomCCInterface.sharedInstance().appWillResignActive()
    }
    
    func applicationDidEnterBackground(_ application: UIApplication) {
        ZoomCCInterface.sharedInstance().appDidEnterBackgroud()
    }
}
```

## Background Modes

To stay in meetings when app goes to background:

1. Open Xcode project > **Targets** > **Signing Capabilities**
2. Click **Add Capability** > **Background Modes**
3. Enable:
   - **Audio, AirPlay, and Picture in Picture**
   - **Voice over IP**

## Rejoin Video Call

Handle deep links for rejoining disconnected video calls:

```swift
// In AppDelegate
func application(_ app: UIApplication, open url: URL, options: [UIApplication.OpenURLOptionsKey : Any] = [:]) -> Bool {
    return rootVC.handleRejoinVideoOpenURL(url)
}

// In ViewController
func handleRejoinVideoOpenURL(_ rejoinURL: URL) -> Bool {
    let item = ZoomCCItem()
    item.sdkType = .video
    item.entryId = APP_VIDEO_ENTRY_ID
    
    return ZoomCCInterface.sharedInstance().videoService().handleRejoinVideoOpen(
        rejoinURL,
        item: item,
        videoDelegate: self
    ) { vc in
        self.navigationController?.pushViewController(vc, animated: true)
    }
}
```

Configure URL scheme in Xcode: **Target** > **Info** > **URL Types** > **URL Schemes** (e.g., `zmcc`)

## Domain Types

| Domain | Use Case |
|--------|----------|
| `.US01` | Default (US cluster) |
| `.EU01` | Europe cluster |

## Resources

- **Get Started:** https://developers.zoom.us/docs/contact-center/ios/get-started/
- **Chat:** https://developers.zoom.us/docs/contact-center/ios/chat/
- **Video:** https://developers.zoom.us/docs/contact-center/ios/video/
- **Screen Share:** https://developers.zoom.us/docs/video-sdk/ios/share/

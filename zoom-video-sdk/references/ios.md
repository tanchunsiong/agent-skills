# Video SDK - iOS

Build custom video experiences on iPhone and iPad.

## Overview

Native iOS SDK for building custom video applications with full UI control.

## Prerequisites

- Video SDK downloaded from [Marketplace](https://marketplace.zoom.us/) (sign-in required)
- Xcode 13+
- iOS 12.0+
- Valid SDK credentials

## Installation

### CocoaPods

```ruby
pod 'ZoomVideoSDK'
```

### Manual Installation

1. Download SDK from Marketplace (requires sign-in)
2. Add `ZoomVideoSDK.xcframework` to your project
3. Add required frameworks

## Quick Start

```swift
import ZoomVideoSDK

// Initialize
let initParams = ZoomVideoSDKInitParams()
initParams.domain = "zoom.us"
ZoomVideoSDK.shareInstance()?.initialize(initParams)

// Join session
let sessionContext = ZoomVideoSDKSessionContext()
sessionContext.sessionName = "MySession"
sessionContext.userName = "User"
sessionContext.token = signature
ZoomVideoSDK.shareInstance()?.joinSession(sessionContext)
```

## Delegate Pattern

```swift
class MyViewController: UIViewController, ZoomVideoSDKDelegate {
    
    func onSessionJoin() {
        print("Joined session")
    }
    
    func onSessionLeave() {
        print("Left session")
    }
    
    func onUserJoin(_ helper: ZoomVideoSDKUserHelper?, users: [ZoomVideoSDKUser]?) {
        // Handle user joined
    }
    
    func onUserLeave(_ helper: ZoomVideoSDKUserHelper?, users: [ZoomVideoSDKUser]?) {
        // Handle user left
    }
}
```

## Common Tasks

### Video Rendering with UIView

```swift
import ZoomVideoSDK
import UIKit

class VideoViewController: UIViewController {
    private var videoView: UIView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setupVideoView()
    }
    
    func setupVideoView() {
        videoView = UIView(frame: view.bounds)
        videoView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        view.addSubview(videoView)
    }
    
    func renderUser(_ user: ZoomVideoSDKUser) {
        // Get video canvas
        guard let canvas = user.getVideoCanvas() else { return }
        
        // Set parent view
        canvas.setParentView(videoView)
        
        // Subscribe at desired resolution
        canvas.subscribe(._720P)
    }
    
    func stopRendering(_ user: ZoomVideoSDKUser) {
        user.getVideoCanvas()?.unsubscribe()
    }
}

// Gallery view with multiple videos
class GalleryViewController: UIViewController {
    private var videoViews: [UIView] = []
    
    func updateLayout(participants: [ZoomVideoSDKUser]) {
        // Clear existing views
        videoViews.forEach { $0.removeFromSuperview() }
        videoViews.removeAll()
        
        // Calculate grid layout
        let count = participants.count
        let cols = Int(ceil(sqrt(Double(count))))
        let rows = Int(ceil(Double(count) / Double(cols)))
        
        let width = view.bounds.width / CGFloat(cols)
        let height = view.bounds.height / CGFloat(rows)
        
        for (index, user) in participants.enumerated() {
            let row = index / cols
            let col = index % cols
            
            let frame = CGRect(
                x: CGFloat(col) * width,
                y: CGFloat(row) * height,
                width: width,
                height: height
            )
            
            let videoView = UIView(frame: frame)
            view.addSubview(videoView)
            videoViews.append(videoView)
            
            user.getVideoCanvas()?.setParentView(videoView)
            user.getVideoCanvas()?.subscribe(._360P)
        }
    }
}
```

### Audio Device Management

```swift
// List audio devices
func listAudioDevices() {
    guard let audioHelper = ZoomVideoSDK.shareInstance()?.getAudioHelper() else { return }
    
    // Get speaker list
    if let speakers = audioHelper.getSpeakerList() {
        for i in 0..<speakers.getCount() {
            if let speaker = speakers.getItem(i) {
                print("Speaker: \(speaker.getDeviceName() ?? "")")
            }
        }
    }
}

// Switch audio output
func switchToSpeaker() {
    ZoomVideoSDK.shareInstance()?.getAudioHelper()?.setSpeaker(true)
}

func switchToEarpiece() {
    ZoomVideoSDK.shareInstance()?.getAudioHelper()?.setSpeaker(false)
}

// Mute/unmute
func toggleMute() {
    guard let audioHelper = ZoomVideoSDK.shareInstance()?.getAudioHelper() else { return }
    
    if audioHelper.isMuted() {
        audioHelper.unmuteAudio(ZoomVideoSDK.shareInstance()?.getSession()?.getMySelf())
    } else {
        audioHelper.muteAudio(ZoomVideoSDK.shareInstance()?.getSession()?.getMySelf())
    }
}
```

### Screen Sharing

```swift
import ReplayKit

// Start screen sharing
func startScreenShare() {
    guard let shareHelper = ZoomVideoSDK.shareInstance()?.getShareHelper() else { return }
    
    // Check if screen share is supported
    if shareHelper.isScreenShareSupported() {
        shareHelper.startShare()
    }
}

// Stop screen sharing
func stopScreenShare() {
    ZoomVideoSDK.shareInstance()?.getShareHelper()?.stopShare()
}

// View screen share from another user
func viewScreenShare(user: ZoomVideoSDKUser, container: UIView) {
    guard let shareCanvas = user.getShareCanvas() else { return }
    shareCanvas.setParentView(container)
    shareCanvas.subscribe()
}

// Handle screen share events
extension YourClass: ZoomVideoSDKDelegate {
    func onUserShareStatusChanged(_ helper: ZoomVideoSDKShareHelper?, 
                                   user: ZoomVideoSDKUser?, 
                                   status: ZoomVideoSDKReceiveSharingStatus) {
        switch status {
        case .started:
            // User started sharing
            if let user = user {
                showScreenShare(user)
            }
        case .stopped:
            // User stopped sharing
            hideScreenShare()
        default:
            break
        }
    }
}
```

### Raw Data Access (Light)

```swift
// Raw video data delegate
class VideoRawDataDelegate: NSObject, ZoomVideoSDKRawDataPipeDelegate {
    func onRawDataFrameReceived(_ data: ZoomVideoSDKYUVRawDataI420?) {
        guard let data = data else { return }
        
        // Note: Raw data access is light on iOS
        // Use sparingly due to battery/performance impact
        let width = data.getStreamWidth()
        let height = data.getStreamHeight()
        let buffer = data.getBuffer()
        
        // Process frame (e.g., for analysis)
        // Avoid heavy processing on mobile
    }
}

// Subscribe to raw video (use sparingly)
func subscribeToRawVideo(user: ZoomVideoSDKUser) {
    let videoPipe = user.getVideoPipe()
    videoPipe?.setRawDataResolution(._360P)  // Lower resolution for mobile
    videoPipe?.subscribe(VideoRawDataDelegate())
}
```

## Required Permissions

Add to `Info.plist`:
```xml
<key>NSCameraUsageDescription</key>
<string>Camera for video calls</string>
<key>NSMicrophoneUsageDescription</key>
<string>Microphone for audio</string>
```

## Resources

- **iOS docs**: https://developers.zoom.us/docs/video-sdk/ios/
- **API Reference**: https://marketplacefront.zoom.us/sdk/custom/ios/

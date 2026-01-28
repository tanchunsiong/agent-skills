# Video SDK - macOS

Desktop video applications on Mac with raw data access.

## Overview

macOS SDK for building custom video applications with full UI control and raw audio/video data access.

## Prerequisites

- Video SDK downloaded from [Marketplace](https://marketplace.zoom.us/) (sign-in required)
- Xcode 13+
- macOS 10.13+
- Valid SDK credentials

## Installation

1. Download SDK from Marketplace (requires sign-in)
2. Add `ZoomVideoSDK.framework` to your project
3. Configure entitlements for camera/microphone

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

## Raw Recording / Raw Data Access

Access raw audio and video frames:

```swift
class MyRawDataDelegate: NSObject, ZoomVideoSDKRawDataPipeDelegate {
    func onRawDataReceived(_ data: ZoomVideoSDKYUVRawDataI420?) {
        // Process raw video frames
    }
    
    func onRawAudioDataReceived(_ data: ZoomVideoSDKAudioRawData?) {
        // Process raw audio samples
    }
}
```

## Common Tasks

### NSView Integration

```swift
import ZoomVideoSDK
import AppKit

class VideoView: NSView {
    private var videoCanvas: ZoomVideoSDKVideoCanvas?
    
    func attachUser(_ user: ZoomVideoSDKUser) {
        // Create canvas for this view
        videoCanvas = user.getVideoCanvas()
        videoCanvas?.setParentView(self)
        videoCanvas?.subscribe(._720P)
    }
    
    func detach() {
        videoCanvas?.unsubscribe()
        videoCanvas = nil
    }
    
    override func resizeSubviews(withOldSize oldSize: NSSize) {
        super.resizeSubviews(withOldSize: oldSize)
        // Canvas auto-resizes with parent view
    }
}

// Usage in your view controller
func setupVideoView(for user: ZoomVideoSDKUser) {
    let videoView = VideoView(frame: containerView.bounds)
    containerView.addSubview(videoView)
    videoView.attachUser(user)
}
```

### Raw Audio Processing

```swift
class AudioDelegate: NSObject, ZoomVideoSDKRawDataPipeDelegate {
    func onRawAudioDataReceived(_ data: ZoomVideoSDKAudioRawData?) {
        guard let data = data else { return }
        
        // Format: 16-bit PCM
        let buffer = data.getBuffer()
        let length = data.getBufferLen()
        let sampleRate = data.getSampleRate()
        let channels = data.getChannelNum()
        
        // Process audio (e.g., send to transcription)
        processAudio(buffer: buffer, length: length, sampleRate: sampleRate)
    }
}

// Subscribe to user's audio
func subscribeToAudio(user: ZoomVideoSDKUser) {
    let audioPipe = user.getAudioPipe()
    audioPipe?.subscribe(audioDelegate)
}
```

### Raw Video Processing

```swift
class VideoDelegate: NSObject, ZoomVideoSDKRawDataPipeDelegate {
    func onRawDataReceived(_ data: ZoomVideoSDKYUVRawDataI420?) {
        guard let data = data else { return }
        
        // Format: I420 (YUV 4:2:0)
        let width = data.getStreamWidth()
        let height = data.getStreamHeight()
        let buffer = data.getBuffer()
        
        // Convert to CGImage for display
        if let cgImage = convertI420toCGImage(buffer, width: width, height: height) {
            DispatchQueue.main.async {
                self.displayImage(cgImage)
            }
        }
    }
}

// Subscribe at specific resolution
func subscribeToVideo(user: ZoomVideoSDKUser) {
    let videoPipe = user.getVideoPipe()
    videoPipe?.setRawDataResolution(._720P)
    videoPipe?.subscribe(videoDelegate)
}
```

### Device Management

```swift
// List devices
func listDevices() {
    let videoHelper = ZoomVideoSDK.shareInstance()?.getVideoHelper()
    let audioHelper = ZoomVideoSDK.shareInstance()?.getAudioHelper()
    
    // Cameras
    if let cameras = videoHelper?.getCameraList() {
        for i in 0..<cameras.getCount() {
            if let camera = cameras.getItem(i) {
                print("Camera: \(camera.getDeviceName() ?? "")")
            }
        }
    }
    
    // Microphones
    if let mics = audioHelper?.getMicList() {
        for i in 0..<mics.getCount() {
            if let mic = mics.getItem(i) {
                print("Mic: \(mic.getDeviceName() ?? "")")
            }
        }
    }
    
    // Speakers
    if let speakers = audioHelper?.getSpeakerList() {
        // ...
    }
}

// Switch devices
func switchCamera(deviceId: String) {
    ZoomVideoSDK.shareInstance()?.getVideoHelper()?.selectCamera(deviceId)
}

func switchMicrophone(deviceId: String) {
    ZoomVideoSDK.shareInstance()?.getAudioHelper()?.selectMic(deviceId)
}
```

## Required Permissions

Add to `Info.plist`:

```xml
<key>NSCameraUsageDescription</key>
<string>Need camera access for video</string>

<key>NSMicrophoneUsageDescription</key>
<string>Need microphone access for audio</string>
```

## Delegate Pattern

```swift
class VideoController: NSObject, ZoomVideoSDKDelegate {
    
    override init() {
        super.init()
        ZoomVideoSDK.shareInstance()?.delegate = self
    }
    
    // MARK: - Session Events
    
    func onSessionJoin() {
        print("Joined session")
    }
    
    func onSessionLeave() {
        print("Left session")
    }
    
    func onError(_ errorType: ZoomVideoSDKError, detail: Int32) {
        print("Error: \(errorType), detail: \(detail)")
    }
    
    // MARK: - User Events
    
    func onUserJoin(_ userHelper: ZoomVideoSDKUserHelper?, users: [ZoomVideoSDKUser]?) {
        users?.forEach { user in
            print("User joined: \(user.getUserName() ?? "")")
        }
    }
    
    func onUserLeave(_ userHelper: ZoomVideoSDKUserHelper?, users: [ZoomVideoSDKUser]?) {
        users?.forEach { user in
            print("User left: \(user.getUserName() ?? "")")
        }
    }
    
    // MARK: - Video Events
    
    func onUserVideoStatusChanged(_ videoHelper: ZoomVideoSDKVideoHelper?, user: [ZoomVideoSDKUser]?) {
        user?.forEach { u in
            let isOn = u.getVideoStatus()?.on ?? false
            print("\(u.getUserName() ?? "") video: \(isOn)")
        }
    }
    
    // MARK: - Audio Events
    
    func onUserAudioStatusChanged(_ audioHelper: ZoomVideoSDKAudioHelper?, user: [ZoomVideoSDKUser]?) {
        user?.forEach { u in
            let isMuted = u.getAudioStatus()?.isMuted ?? true
            print("\(u.getUserName() ?? "") muted: \(isMuted)")
        }
    }
    
    // MARK: - Share Events
    
    func onUserShareStatusChanged(_ shareHelper: ZoomVideoSDKShareHelper?,
                                   user: ZoomVideoSDKUser?,
                                   status: ZoomVideoSDKReceiveSharingStatus) {
        switch status {
        case .start:
            print("\(user?.getUserName() ?? "") started sharing")
        case .stop:
            print("Sharing stopped")
        @unknown default:
            break
        }
    }
}
```

## Screen Sharing

```swift
class ScreenShareController {
    
    func startScreenShare() {
        guard let shareHelper = ZoomVideoSDK.shareInstance()?.getShareHelper() else { return }
        
        // Share main monitor
        if let mainScreen = NSScreen.main {
            let displayID = mainScreen.deviceDescription[NSDeviceDescriptionKey("NSScreenNumber")] as? CGDirectDisplayID ?? 0
            shareHelper.startShare(withMonitorID: displayID)
        }
    }
    
    func stopShare() {
        ZoomVideoSDK.shareInstance()?.getShareHelper()?.stopShare()
    }
    
    // View someone else's share
    func viewScreenShare(user: ZoomVideoSDKUser, container: NSView) {
        guard let shareCanvas = user.getShareCanvas() else { return }
        shareCanvas.subscribe(with: container, aspectMode: .panAndScan)
    }
}
```

## Gallery View Layout

```swift
class GalleryView: NSView {
    private var videoViews: [NSView] = []
    
    func updateLayout(participants: [ZoomVideoSDKUser]) {
        // Clear existing
        videoViews.forEach { $0.removeFromSuperview() }
        videoViews.removeAll()
        
        guard !participants.isEmpty else { return }
        
        // Calculate grid
        let count = participants.count
        let cols = Int(ceil(sqrt(Double(count))))
        let rows = Int(ceil(Double(count) / Double(cols)))
        
        let width = bounds.width / CGFloat(cols)
        let height = bounds.height / CGFloat(rows)
        
        for (index, user) in participants.enumerated() {
            let row = index / cols
            let col = index % cols
            
            let frame = CGRect(
                x: CGFloat(col) * width,
                y: bounds.height - CGFloat(row + 1) * height,
                width: width,
                height: height
            )
            
            let videoView = NSView(frame: frame)
            videoView.wantsLayer = true
            videoView.layer?.backgroundColor = NSColor.black.cgColor
            addSubview(videoView)
            videoViews.append(videoView)
            
            user.getVideoCanvas()?.subscribe(with: videoView,
                                              aspectMode: .panAndScan,
                                              resolution: ._360P)
        }
    }
}
```

## SwiftUI Integration

```swift
import SwiftUI
import ZoomVideoSDK

struct VideoViewRepresentable: NSViewRepresentable {
    let user: ZoomVideoSDKUser
    
    func makeNSView(context: Context) -> NSView {
        let view = NSView()
        view.wantsLayer = true
        view.layer?.backgroundColor = NSColor.black.cgColor
        return view
    }
    
    func updateNSView(_ nsView: NSView, context: Context) {
        user.getVideoCanvas()?.subscribe(with: nsView,
                                          aspectMode: .panAndScan,
                                          resolution: ._720P)
    }
}

struct VideoCallView: View {
    @StateObject private var viewModel = VideoViewModel()
    
    var body: some View {
        VStack {
            // Video grid
            LazyVGrid(columns: [GridItem(.adaptive(minimum: 200))]) {
                ForEach(viewModel.participants, id: \.getUserId()) { user in
                    VideoViewRepresentable(user: user)
                        .frame(height: 150)
                        .cornerRadius(8)
                }
            }
            .padding()
            
            // Controls
            HStack(spacing: 20) {
                Button(action: viewModel.toggleMute) {
                    Image(systemName: viewModel.isMuted ? "mic.slash.fill" : "mic.fill")
                }
                Button(action: viewModel.toggleVideo) {
                    Image(systemName: viewModel.isVideoOn ? "video.fill" : "video.slash.fill")
                }
                Button(action: viewModel.leaveSession) {
                    Image(systemName: "phone.down.fill")
                        .foregroundColor(.red)
                }
            }
            .padding()
        }
    }
}

class VideoViewModel: ObservableObject {
    @Published var participants: [ZoomVideoSDKUser] = []
    @Published var isMuted = false
    @Published var isVideoOn = true
    
    func toggleMute() {
        guard let audioHelper = ZoomVideoSDK.shareInstance()?.getAudioHelper(),
              let myself = ZoomVideoSDK.shareInstance()?.getSession()?.getMySelf() else { return }
        
        if isMuted {
            audioHelper.unmuteAudio(myself)
        } else {
            audioHelper.muteAudio(myself)
        }
        isMuted.toggle()
    }
    
    func toggleVideo() {
        guard let videoHelper = ZoomVideoSDK.shareInstance()?.getVideoHelper() else { return }
        
        if isVideoOn {
            videoHelper.stopVideo()
        } else {
            videoHelper.startVideo()
        }
        isVideoOn.toggle()
    }
    
    func leaveSession() {
        ZoomVideoSDK.shareInstance()?.leaveSession(false)
    }
}
```

## App Sandbox Entitlements

For App Store distribution, add to entitlements:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.app-sandbox</key>
    <true/>
    <key>com.apple.security.device.camera</key>
    <true/>
    <key>com.apple.security.device.audio-input</key>
    <true/>
    <key>com.apple.security.network.client</key>
    <true/>
</dict>
</plist>
```

## Resources

- **macOS docs**: https://developers.zoom.us/docs/video-sdk/macos/
- **API Reference**: https://marketplacefront.zoom.us/sdk/custom/macos/
- **Sample**: [videosdk-macos-uikit-quickstart](https://github.com/zoom/videosdk-macos-uikit-quickstart)

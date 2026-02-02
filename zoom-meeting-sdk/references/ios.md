# Meeting SDK - iOS

Embed Zoom meetings in iPhone and iPad apps.

## Overview

Native iOS SDK for embedding the full Zoom meeting experience into your app.

## Prerequisites

- Meeting SDK downloaded from [Marketplace](https://marketplace.zoom.us/) (sign-in required)
- Xcode 13+
- iOS 12.0+
- Valid SDK credentials

## Installation

### CocoaPods

```ruby
pod 'ZoomSDK'
```

### Manual Installation

1. Download SDK from Marketplace (requires sign-in)
2. Add `MobileRTC.xcframework` to your project
3. Add required frameworks

## Quick Start

```swift
import MobileRTC

// Initialize
let context = MobileRTCSDKInitContext()
context.domain = "zoom.us"
MobileRTC.shared().initialize(context)

// Set delegate
MobileRTC.shared().setMobileRTCRootController(navigationController)

// Authenticate with JWT
let authService = MobileRTC.shared().getAuthService()
authService?.delegate = self
authService?.jwtToken = "your-jwt-token"
authService?.sdkAuth()

// Join meeting (after auth succeeds)
let joinParams = MobileRTCMeetingJoinParam()
joinParams.meetingNumber = meetingNumber
joinParams.password = password
joinParams.userName = "User"
MobileRTC.shared().getMeetingService()?.joinMeeting(with: joinParams)
```

## Authentication

```swift
class AuthDelegate: NSObject, MobileRTCAuthDelegate {
    func onMobileRTCAuthReturn(_ returnValue: MobileRTCAuthError) {
        switch returnValue {
        case .success:
            print("SDK authenticated successfully")
        case .keyOrSecretEmpty:
            print("JWT token is empty")
        case .keyOrSecretWrong:
            print("Invalid JWT token")
        case .unknown:
            print("Auth timeout or network error")
        default:
            print("Auth error: \(returnValue)")
        }
    }
}
```

## Delegate Pattern

```swift
class MeetingDelegate: NSObject, MobileRTCMeetingServiceDelegate {
    func onMeetingStateChange(_ state: MobileRTCMeetingState) {
        switch state {
        case .idle:
            print("Meeting idle")
        case .connecting:
            print("Connecting...")
        case .inMeeting:
            print("In meeting")
        default:
            break
        }
    }
    
    func onMeetingError(_ error: MobileRTCMeetError, message: String?) {
        print("Meeting error: \(error)")
    }
}
```

## Common Tasks

### Custom UI Integration

```swift
// Enable Custom UI mode during initialization
let context = MobileRTCSDKInitContext()
context.domain = "zoom.us"
context.enableCustomizedUI = true  // Enable custom UI
MobileRTC.shared().initialize(context)

// Build your own UI using MobileRTC APIs
class CustomMeetingUI: UIViewController {
    var videoView: UIView!
    
    func setupVideoView() {
        // Get active video user
        if let activeUser = MobileRTC.shared().getMeetingService()?.activeVideoUserID() {
            // Render their video
            let canvas = MobileRTCVideoView(frame: videoView.bounds)
            videoView.addSubview(canvas)
            canvas.showAttendeeVideo(withUserID: activeUser)
        }
    }
}
```

### Audio/Video Controls

```swift
// Mute/unmute audio
func toggleAudio() {
    let meetingService = MobileRTC.shared().getMeetingService()
    
    if meetingService?.isMyAudioMuted() == true {
        meetingService?.muteMyAudio(false)  // Unmute
    } else {
        meetingService?.muteMyAudio(true)   // Mute
    }
}

// Start/stop video
func toggleVideo() {
    let meetingService = MobileRTC.shared().getMeetingService()
    
    if meetingService?.isMyVideoMuted() == true {
        meetingService?.muteMyVideo(false)  // Start video
    } else {
        meetingService?.muteMyVideo(true)   // Stop video
    }
}

// Switch camera
func switchCamera() {
    MobileRTC.shared().getMeetingService()?.switchMyCamera()
}
```

### Screen Sharing

```swift
import ReplayKit

// Start screen share
func startScreenShare() {
    let meetingService = MobileRTC.shared().getMeetingService()
    
    if meetingService?.isStartShareScreenEnabled() == true {
        meetingService?.startAppShare()
    }
}

// Stop screen share
func stopScreenShare() {
    MobileRTC.shared().getMeetingService()?.stopAppShare()
}

// Broadcast screen (requires Broadcast Extension)
func startBroadcast() {
    RPBroadcastActivityViewController.load { controller, error in
        if let controller = controller {
            controller.delegate = self
            self.present(controller, animated: true)
        }
    }
}
```

### Meeting Controls

```swift
// Leave meeting
func leaveMeeting() {
    MobileRTC.shared().getMeetingService()?.leaveMeeting(with: .leave)
}

// End meeting (host only)
func endMeeting() {
    MobileRTC.shared().getMeetingService()?.leaveMeeting(with: .end)
}

// Get participant list
func getParticipants() -> [MobileRTCMeetingUserInfo] {
    var participants: [MobileRTCMeetingUserInfo] = []
    
    if let userList = MobileRTC.shared().getMeetingService()?.getInMeetingUserList() {
        for userId in userList {
            if let info = MobileRTC.shared().getMeetingService()?.userInfo(byID: userId as! UInt) {
                participants.append(info)
            }
        }
    }
    
    return participants
}

// Chat
func sendChatMessage(_ message: String, to userId: UInt = 0) {
    // userId = 0 sends to everyone
    MobileRTC.shared().getMeetingService()?.sendChatMessage(message, toUserId: userId)
}
```

## Raw Data (Video/Audio)

### Send Custom Video

```objc
// Implement MobileRTCVideoSourceDelegate
@interface SendYUVAdapter : NSObject <MobileRTCVideoSourceDelegate>
@property (nonatomic, strong) MobileRTCVideoSender *videoRawdataSender;
@end

@implementation SendYUVAdapter

- (void)onInitialize:(MobileRTCVideoSender *)rawDataSender 
    supportCapabilityArray:(NSArray *)supportCapabilityArray 
    suggestCapabilityItem:(MobileRTCVideoCapabilityItem *)suggestCapabilityItem {
    self.videoRawdataSender = rawDataSender;
}

- (void)onStartSend {
    // Start sending video frames
    [self beginPullVideo];
}

- (void)sendFrame:(char *)yuvFrame width:(int)width height:(int)height {
    [self.videoRawdataSender sendVideoFrame:yuvFrame 
                                      width:width 
                                     height:height 
                                 dataLength:width * height * 1.5 
                                   rotation:MobileRTCVideoRawDataRotationNone 
                                     format:MobileRTCFrameDataFormat_I420];
}
@end
```

### Save Audio Raw Data

```objc
// Save raw audio to file
- (void)saveAudioRawdata:(MobileRTCAudioRawData *)rawData {
    NSData *data = [NSData dataWithBytes:rawData.buffer length:rawData.bufferLen];
    NSFileHandle *handle = [NSFileHandle fileHandleForWritingAtPath:self.filePath];
    [handle seekToEndOfFile];
    [handle writeData:data];
    [handle closeFile];
}
```

## Delegate Categories

The SDK provides specialized delegate protocols:

| Delegate | Purpose |
|----------|---------|
| `MobileRTCMeetingServiceDelegate` | Core meeting events |
| `MobileRTCVideoServiceDelegate` | Video state changes |
| `MobileRTCAudioServiceDelegate` | Audio state changes |
| `MobileRTCShareServiceDelegate` | Screen sharing events |
| `MobileRTCUserServiceDelegate` | Participant events |
| `MobileRTCWebinarServiceDelegate` | Webinar-specific events |
| `MobileRTCBOServiceDelegate` | Breakout room events |
| `MobileRTCCustomizedUIMeetingDelegate` | Custom UI events |

## Join Options

```swift
let joinParams = MobileRTCMeetingJoinParam()
joinParams.userName = UIDevice.current.name
joinParams.meetingNumber = "123456789"
joinParams.password = "password"

// Optional parameters
joinParams.zak = zakToken           // For ZAK authentication
joinParams.customerKey = "custom"   // Custom participant key
joinParams.webinarToken = "token"   // Webinar registration token
joinParams.noAudio = true           // Join with audio off
joinParams.noVideo = true           // Join with video off
joinParams.isMyVoiceInMix = true    // Include self in mixed audio
```

## Common Gotchas

- **Enum 0 = Success**: Check return values - 0 often means success
- **Background mode**: Enable "Audio" background mode for background audio
- **App Store submission**: SDK is compatible with App Store (unlike macOS)
- **Raw data enable**: Call `enableSendRawdata:YES` in MeetingSettings before joining

## Resources

- **iOS docs**: https://developers.zoom.us/docs/meeting-sdk/ios/
- **API Reference**: https://marketplacefront.zoom.us/sdk/meeting/ios/

# Singleton Hierarchy: Navigation Guide

## Overview

The Zoom Video SDK uses a **service locator pattern** - a tree of singletons where you navigate from the root SDK object down to specific features. You don't construct objects; you traverse to them.

```
You want to...              You navigate to...
─────────────────────────────────────────────────────
Start your camera           IZoomVideoSDK → IZoomVideoSDKVideoHelper
Mute a user                 IZoomVideoSDK → IZoomVideoSDKAudioHelper
Subscribe to video          IZoomVideoSDKUser → IZoomVideoSDKCanvas
Get raw YUV frames          IZoomVideoSDKUser → IZoomVideoSDKRawDataPipe
Send chat message           IZoomVideoSDK → IZoomVideoSDKChatHelper
Start screen share          IZoomVideoSDK → IZoomVideoSDKShareHelper
Subscribe to remote share   IZoomVideoSDKShareAction → subscribeWithView()
```

---

## Complete Hierarchy (5 Levels Deep)

```
Level 0: Global Factory Function
│
└─► CreateZoomVideoSDKObj() ──────────────────────────────────► IZoomVideoSDK*
    │
    ├─► Level 1: Session & Lifecycle
    │   ├── initialize(params)           → ZoomVideoSDKErrors
    │   ├── joinSession(context)         → IZoomVideoSDKSession*
    │   ├── leaveSession(end)            → ZoomVideoSDKErrors
    │   ├── addListener(delegate)        → void
    │   ├── getSessionInfo()             → IZoomVideoSDKSession*
    │   └── isInSession()                → bool
    │
    ├─► Level 1: Core Helpers (Control YOUR streams)
    │   ├── getVideoHelper()             → IZoomVideoSDKVideoHelper*
    │   │   ├── startVideo() / stopVideo()
    │   │   ├── switchCamera(deviceId)
    │   │   ├── getCameraList()          → IVideoSDKVector<IZoomVideoSDKCameraDevice*>*
    │   │   │   └─► Level 4: IZoomVideoSDKCameraDevice
    │   │   │       ├── getDeviceId()
    │   │   │       ├── getDeviceName()
    │   │   │       └── isSelectedDevice()
    │   │   └── startVideoCanvasPreview(hwnd, aspect, resolution)
    │   │
    │   ├── getAudioHelper()             → IZoomVideoSDKAudioHelper*
    │   │   ├── startAudio() / stopAudio()
    │   │   ├── muteAudio(user) / unmuteAudio(user)
    │   │   ├── getMicList()             → IVideoSDKVector<IZoomVideoSDKMicDevice*>*
    │   │   │   └─► Level 4: IZoomVideoSDKMicDevice
    │   │   ├── getSpeakerList()         → IVideoSDKVector<IZoomVideoSDKSpeakerDevice*>*
    │   │   │   └─► Level 4: IZoomVideoSDKSpeakerDevice
    │   │   └── selectMic() / selectSpeaker()
    │   │
    │   ├── getShareHelper()             → IZoomVideoSDKShareHelper*
    │   │   ├── startShareScreen(monitorId)
    │   │   ├── startShareWindow(hwnd)
    │   │   ├── stopShare()
    │   │   └── isOtherSharing()
    │   │
    │   ├── getChatHelper()              → IZoomVideoSDKChatHelper*
    │   │   ├── sendChatToAll(message)
    │   │   └── sendChatToUser(user, message)
    │   │
    │   ├── getUserHelper()              → IZoomVideoSDKUserHelper*
    │   │   ├── removeUser(user)
    │   │   ├── makeHost(user)
    │   │   ├── makeManager(user)
    │   │   └── changeName(user, name)
    │   │
    │   ├── getRecordingHelper()         → IZoomVideoSDKRecordingHelper*
    │   │
    │   └── getCmdChannel()              → IZoomVideoSDKCmdChannel*
    │       ├── sendCommand(user, cmd)
    │       └── sendCommandToAll(cmd)
    │
    └─► Level 1: Session Object
        │
        └── getSessionInfo()             → IZoomVideoSDKSession*
            ├── getSessionName()
            ├── getSessionID()
            ├── getSessionHost()         → IZoomVideoSDKUser*
            ├── getMyself()              → IZoomVideoSDKUser*
            │   │
            │   └─► Level 3: IZoomVideoSDKUser (LOCAL - yourself)
            │       ├── getUserID() / getUserName()
            │       ├── isHost() / isManager()
            │       ├── getVideoStatus()     → ZoomVideoSDKVideoStatus
            │       ├── getAudioStatus()     → ZoomVideoSDKAudioStatus
            │       │
            │       ├── GetVideoCanvas()     → IZoomVideoSDKCanvas*           [SDK RENDERING]
            │       │   └─► Level 4: Canvas API
            │       │       ├── subscribeWithView(hwnd, aspect, resolution)
            │       │       ├── unSubscribeWithView(hwnd)
            │       │       ├── setAspectMode(aspect)
            │       │       └── setResolution(resolution)
            │       │
            │       ├── GetVideoPipe()       → IZoomVideoSDKRawDataPipe*      [RAW DATA]
            │       │   └─► Level 4: Raw Data Pipe
            │       │       ├── subscribe(resolution, delegate)
            │       │       ├── unSubscribe(delegate)
            │       │       ├── getVideoStatus()
            │       │       │
            │       │       └─► Level 5: IZoomVideoSDKRawDataPipeDelegate (your callback)
            │       │           ├── onRawDataFrameReceived(YUVRawDataI420*)
            │       │           └── onRawDataStatusChanged(status)
            │       │
            │       ├── GetShareCanvas()     → IZoomVideoSDKCanvas*
            │       └── GetSharePipe()       → IZoomVideoSDKRawDataPipe*
            │
            └── getRemoteUsers()         → IVideoSDKVector<IZoomVideoSDKUser*>*
                │
                └─► Level 3: IZoomVideoSDKUser (REMOTE - other participants)
                    ├── [Same methods as local user]
                    ├── GetVideoCanvas()     → Subscribe to their video
                    └── GetVideoPipe()       → Get their raw frames

    ┌─────────────────────────────────────────────────────────────────────────┐
    │  CALLBACK PATH (from IZoomVideoSDKDelegate)                             │
    │                                                                         │
    │  onUserShareStatusChanged(helper, user, pShareAction)                   │
    │      │                                                                  │
    │      └─► IZoomVideoSDKShareAction* (received in callback)               │
    │          ├── subscribe() / unSubscribe()                                │
    │          ├── subscribeWithView(hwnd, aspect)                            │
    │          ├── unSubscribeWithView(hwnd)                                  │
    │          ├── getShareCanvas()      → IZoomVideoSDKCanvas*               │
    │          ├── getSharePipe()        → IZoomVideoSDKRawDataPipe*          │
    │          └── getShareType()        → ZoomVideoSDKShareType              │
    └─────────────────────────────────────────────────────────────────────────┘
```

---

## Key Difference from Meeting SDK

| Aspect | Meeting SDK | Video SDK |
|--------|-------------|-----------|
| **Root Object** | `IMeetingService` | `IZoomVideoSDK` |
| **Feature Access** | Controllers (`GetMeetingAudioController()`) | Helpers (`getAudioHelper()`) |
| **Video Subscription** | Per-user renderers | Per-user Canvas/Pipe |
| **Share Subscription** | Via callback's `IZoomVideoSDKShareAction` | Via callback's `IZoomVideoSDKShareAction` |
| **Depth** | 4 levels max | 5 levels max |

---

## When to Use Each Level

| Level | When | Example |
|-------|------|---------|
| **Level 1** | After SDK init, control YOUR streams | `sdk->getVideoHelper()->startVideo()` |
| **Level 2** | After session join, get session info | `sdk->getSessionInfo()->getMyself()` |
| **Level 3** | Get user objects | `session->getRemoteUsers()` |
| **Level 4** | Subscribe to video/share | `user->GetVideoCanvas()->subscribeWithView()` |
| **Level 5** | Receive raw frames | `pipe->subscribe(res, myDelegate)` |

---

## Two Rendering Paths

The SDK provides **two distinct paths** for video rendering:

### Path A: Canvas API (SDK-Rendered)

```
IZoomVideoSDKUser
    └── GetVideoCanvas()
        └── IZoomVideoSDKCanvas
            └── subscribeWithView(HWND, aspect, resolution)
                └── SDK renders directly to your window
```

**Pros**: Best quality, no CPU overhead, automatic scaling
**Use for**: Standard video conferencing UI

### Path B: Raw Data Pipe (Self-Rendered)

```
IZoomVideoSDKUser
    └── GetVideoPipe()
        └── IZoomVideoSDKRawDataPipe
            └── subscribe(resolution, delegate)
                └── Your IZoomVideoSDKRawDataPipeDelegate
                    └── onRawDataFrameReceived(YUVRawDataI420*)
                        └── You convert YUV→RGB and render
```

**Pros**: Full control over frames, can process/filter/record
**Use for**: Custom effects, AI processing, recording

---

## Universal Pattern (3 Steps)

Every feature follows the **same pattern**:

```cpp
// Step 1: Navigate to the helper (singleton)
IZoomVideoSDKVideoHelper* videoHelper = sdk->getVideoHelper();

// Step 2: Use it
videoHelper->startVideo();

// For subscriptions, get user first:
IZoomVideoSDKUser* user = sdk->getSessionInfo()->getMyself();
IZoomVideoSDKCanvas* canvas = user->GetVideoCanvas();
canvas->subscribeWithView(hwnd, aspect, resolution);
```

For **event-driven features**, implement `IZoomVideoSDKDelegate`:

```cpp
// Step 1: Implement delegate
class MyDelegate : public IZoomVideoSDKDelegate {
    void onUserVideoStatusChanged(...) override {
        // React to video status changes
    }
    // ... 60+ other callbacks
};

// Step 2: Register
sdk->addListener(new MyDelegate());

// Step 3: Events arrive automatically
```

---

## Navigation by Feature

| Feature | Navigation Path |
|---------|-----------------|
| **Start camera** | `sdk->getVideoHelper()->startVideo()` |
| **Stop camera** | `sdk->getVideoHelper()->stopVideo()` |
| **Switch camera** | `sdk->getVideoHelper()->switchCamera(deviceId)` |
| **Camera list** | `sdk->getVideoHelper()->getCameraList()` |
| **Mute audio** | `sdk->getAudioHelper()->muteAudio(user)` |
| **Unmute audio** | `sdk->getAudioHelper()->unmuteAudio(user)` |
| **Start audio** | `sdk->getAudioHelper()->startAudio()` |
| **Mic list** | `sdk->getAudioHelper()->getMicList()` |
| **Speaker list** | `sdk->getAudioHelper()->getSpeakerList()` |
| **Send chat** | `sdk->getChatHelper()->sendChatToAll(msg)` |
| **Start share** | `sdk->getShareHelper()->startShareScreen(monitorId)` |
| **Stop share** | `sdk->getShareHelper()->stopShare()` |
| **Subscribe video** | `user->GetVideoCanvas()->subscribeWithView(hwnd, ...)` |
| **Get raw frames** | `user->GetVideoPipe()->subscribe(res, delegate)` |
| **Subscribe share** | `shareAction->subscribeWithView(hwnd, aspect)` (from callback) |
| **Kick user** | `sdk->getUserHelper()->removeUser(user)` |
| **Make host** | `sdk->getUserHelper()->makeHost(user)` |
| **Send command** | `sdk->getCmdChannel()->sendCommandToAll(cmd)` |
| **Get myself** | `sdk->getSessionInfo()->getMyself()` |
| **Get remote users** | `sdk->getSessionInfo()->getRemoteUsers()` |

---

## Critical Timing Rules

### 1. Helpers Control YOUR Streams Only

```cpp
// videoHelper controls YOUR camera, not others'
sdk->getVideoHelper()->startVideo();  // Starts YOUR camera
sdk->getVideoHelper()->stopVideo();   // Stops YOUR camera

// To SEE other users' video, subscribe via their Canvas/Pipe
IZoomVideoSDKUser* remoteUser = ...;
remoteUser->GetVideoCanvas()->subscribeWithView(hwnd, ...);
```

### 2. Subscribe in onUserVideoStatusChanged, NOT onUserJoin

```cpp
// WRONG - user's video may not be ready yet
void onUserJoin(..., userList) {
    user->GetVideoCanvas()->subscribeWithView(hwnd, ...);  // Error 2!
}

// CORRECT - wait for video status change
void onUserVideoStatusChanged(..., userList) {
    for (auto user : userList) {
        if (user->GetVideoPipe()->getVideoStatus().isOn) {
            user->GetVideoCanvas()->subscribeWithView(hwnd, ...);  // Works!
        }
    }
}
```

### 3. ShareAction Comes from Callback

```cpp
// You don't navigate to ShareAction - it's given to you in the callback
void onUserShareStatusChanged(IZoomVideoSDKShareHelper* helper,
                               IZoomVideoSDKUser* user,
                               IZoomVideoSDKShareAction* shareAction) {
    // Subscribe to remote user's screen share
    shareAction->subscribeWithView(shareHwnd, ZoomVideoSDKVideoAspect_Original);
}
```

### 4. Check nullptr Before Use

```cpp
IZoomVideoSDKCanvas* canvas = user->GetVideoCanvas();
if (canvas) {
    canvas->subscribeWithView(hwnd, aspect, resolution);
}
```

---

## Practical Rules

### 1. Get Helpers After Initialize

```cpp
// WRONG - SDK not initialized
IZoomVideoSDKVideoHelper* helper = sdk->getVideoHelper();  // nullptr!
sdk->initialize(params);

// CORRECT
sdk->initialize(params);
IZoomVideoSDKVideoHelper* helper = sdk->getVideoHelper();  // Valid
```

### 2. Get Session/Users After Join

```cpp
// WRONG - not in session yet
IZoomVideoSDKSession* session = sdk->getSessionInfo();  // nullptr!
sdk->joinSession(context);

// CORRECT - wait for onSessionJoin callback
void onSessionJoin() {
    IZoomVideoSDKSession* session = sdk->getSessionInfo();  // Valid
    IZoomVideoSDKUser* myself = session->getMyself();       // Valid
}
```

### 3. One HWND Per Video Stream

```cpp
// Each user needs their own window
HWND selfWindow = CreateWindow(...);
HWND user1Window = CreateWindow(...);
HWND user2Window = CreateWindow(...);

myself->GetVideoCanvas()->subscribeWithView(selfWindow, ...);
user1->GetVideoCanvas()->subscribeWithView(user1Window, ...);
user2->GetVideoCanvas()->subscribeWithView(user2Window, ...);
```

---

## Deepest Paths (Maximum Depth = 5)

| Path | Use Case |
|------|----------|
| `IZoomVideoSDK` → `getVideoHelper()` → `getCameraList()` → `IZoomVideoSDKCameraDevice` → `getDeviceId()` | Enumerate cameras |
| `IZoomVideoSDK` → `getSessionInfo()` → `getMyself()` → `GetVideoPipe()` → `subscribe(delegate)` | Raw self video |
| `IZoomVideoSDK` → `getSessionInfo()` → `getRemoteUsers()` → `user->GetVideoCanvas()` → `subscribeWithView()` | Remote video display |

---

## Related Documentation

- [API Reference](../references/windows-reference.md) - Complete method signatures
- [SKILL.md](../SKILL.md) - Main skill overview with code examples
- [Video Rendering Guide](../SKILL.md#video-rendering---two-approaches) - Canvas vs Raw Data comparison

---

**TL;DR**: Start at `IZoomVideoSDK`, navigate to helpers for YOUR streams, navigate to users for THEIR streams. Subscribe to video in `onUserVideoStatusChanged`, not `onUserJoin`.

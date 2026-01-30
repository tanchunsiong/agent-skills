# Video SDK - Electron

Build cross-platform desktop video applications with Zoom Video SDK and Electron.

## Overview

The Zoom Video SDK Electron integration uses native Node.js addons (`.node` files) with protobuf serialization to provide full Video SDK functionality. This enables building desktop applications for Windows, macOS, and Linux with custom video experiences.

**Current Version**: v2.4.5 (January 2025)

**Sample Repository**: [zoom/videosdk-electron-sample](https://github.com/zoom/videosdk-electron-sample)

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Node.js | 20.17.0 |
| Electron | 33.0.0 |
| Protobuf | 22.3 |
| Python | 3.x (below 3.12 recommended) |

### Platform-Specific Requirements

| Platform | Additional Requirements |
|----------|------------------------|
| **Windows** | Visual Studio 2019+ OR Windows Build Tools |
| **macOS** | Xcode 14+ |
| **Linux** | Build essentials (`build-essential` package) |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Electron Application                         │
├─────────────────────────────────────────────────────────────────┤
│  Main Process (background.js)                                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ZoomVideoSDK.getInstance()                                  ││
│  │   ├── createZoomVideoSDKObj()                               ││
│  │   ├── initialize({ domain, enableLog, ... })                ││
│  │   ├── joinSession({ sessionName, token, username, ... })    ││
│  │   ├── leaveSession({ bEnd })                                ││
│  │   ├── cleanup() / destroyZoomVideoSDKObj()                  ││
│  │   └── setNodeAddonCallbacks(callback)                       ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                     @electron/remote                             │
│                              │                                   │
│  Renderer Process (Vue 2.x)                                      │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ const zoomVideoSdk = remote.app.zoomVideoSdk                ││
│  │   ├── getVideoHelper() → startVideo(), stopVideo()          ││
│  │   ├── getAudioHelper() → startAudio(), muteAudio()          ││
│  │   ├── getShareHelper() → startShare(), stopShare()          ││
│  │   ├── getChatHelper() → sendChat()                          ││
│  │   └── getSessionInfo() → getMyself(), getAllUsers()         ││
│  └─────────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────────┤
│  Native SDK (lib/*.js → sdk/*.node)                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Platform-specific native addons:                            ││
│  │   • sdk/win32/zoomvideosdk.node (Windows 32-bit)            ││
│  │   • sdk/win64/zoomvideosdk.node (Windows 64-bit)            ││
│  │   • sdk/mac/zoomvideosdk.node (macOS x64/arm64)             ││
│  │   • sdk/linux/zoomvideosdk.node (Linux x64)                 ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
videosdk-electron-sample/
├── config.json              # SDK domain configuration
├── package.json             # Dependencies (Electron 33, Vue 2.6)
├── binding.gyp              # Native addon build config
├── vue.config.js            # Vue CLI Electron builder config
├── lib/
│   ├── zoom_video_sdk.js           # Main SDK singleton
│   ├── zoom_video_sdk_video.js     # Video helper
│   ├── zoom_video_sdk_audio.js     # Audio helper
│   ├── zoom_video_sdk_share.js     # Screen share helper
│   ├── zoom_video_sdk_chat.js      # Chat helper
│   ├── zoom_video_sdk_defines.js   # Error codes & enums
│   ├── electron_zoomvideosdk_pb.js # Protobuf messages
│   └── node_add_on/
│       └── protobuf_src/           # Protobuf source files
├── sdk/                     # Native SDK libraries per platform
│   ├── win32/
│   ├── win64/
│   ├── mac/
│   └── linux/
├── src/
│   ├── background.js        # Electron main process entry
│   ├── main.js              # Vue app entry
│   ├── App.vue
│   └── views/
│       ├── Index.vue        # Home screen
│       ├── CreateOrJoin.vue # Join session form
│       ├── Meeting.vue      # Meeting view
│       └── Meeting_HandleCallbackEvents.js  # Event handlers
└── public/
    └── index.html
```

## Installation

### Step 1: Install Node.js and Electron

```bash
# Install Node.js 20.17.0 from https://nodejs.org/

# Install Electron globally (optional)
npm install -g electron@33.0.0
```

### Step 2: Install Protobuf 22.3

This is required for the native addon build:

```bash
# Download protobuf 22.3
wget https://github.com/protocolbuffers/protobuf/releases/download/v22.3/protobuf-22.3.tar.gz
tar -xzf protobuf-22.3.tar.gz

# Rename src folder
mv protobuf-22.3/src protobuf_src

# Download and add abseil-cpp
wget https://github.com/abseil/abseil-cpp/archive/refs/tags/20230802.1.tar.gz
tar -xzf 20230802.1.tar.gz
cp -r abseil-cpp-20230802.1/absl protobuf_src/

# Copy to lib/node_add_on
mkdir -p lib/node_add_on
cp -r protobuf_src lib/node_add_on/
```

### Step 3: Platform-Specific Setup

#### Windows

```bash
# Option 1: Install Windows Build Tools
npm install --global --production windows-build-tools

# Option 2: Install Visual Studio 2019+
# Download from https://visualstudio.microsoft.com/
# Include "Desktop development with C++" workload
```

#### macOS

```bash
# Install Xcode from App Store or Apple Developer site
xcode-select --install
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install build-essential
```

### Step 4: Configure and Run

```bash
# Clone the sample app
git clone https://github.com/zoom/videosdk-electron-sample.git
cd videosdk-electron-sample

# Configure domain in config.json
# Default: "zoom.us"

# Install dependencies and run
npm run electron:serve
```

## Configuration

### config.json

```json
{
  "domain": "zoom.us"
}
```

### package.json

Key configuration options:

```json
{
  "name": "videosdk-electron-sample",
  "version": "1.0.0",
  "main": "src/main/index.js",
  "scripts": {
    "electron:serve": "node scripts/electron_sdk_install.js && electron ."
  },
  "devDependencies": {
    "electron": "33.0.0",
    "node-gyp": "^10.0.0"
  }
}
```

## Code Examples

### Main Process (background.js)

The main process initializes the SDK and exposes it via `app.zoomVideoSdk`:

```javascript
'use strict'

import { app, protocol, ipcMain, BrowserWindow, screen } from 'electron'
import ZoomVideoSDK from '../lib/zoom_video_sdk.js'
import { configDomain } from '../config.json'

const remote = require('@electron/remote/main')
remote.initialize()

const { platform, arch } = process
app.platform = platform
app.arch = arch

// Get SDK singleton instance
const zoomVideoSdk = ZoomVideoSDK.getInstance()
app.zoomVideoSdk = zoomVideoSdk  // Expose to renderer via @electron/remote

// Create SDK object (loads native addon based on platform)
const createResult = zoomVideoSdk.createZoomVideoSDKObj()
console.log('createZoomVideoSDKObj:', createResult)

// Initialize SDK
const domain = configDomain || 'https://www.zoom.us'
const initResult = zoomVideoSdk.initialize({
  domain: domain,
  logFilePrefix: 'sdk',
  enableLog: true,
  audioRawDataMemoryMode: 0,  // 0 = stack, 1 = heap
  videoRawDataMemoryMode: 0,
  shareRawDataMemoryMode: 0
})
console.log('initialize:', initResult)  // 0 = success

let mainWindow

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 480,
    height: 630,
    frame: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true
    }
  })
  
  mainWindow.loadURL('app://./index.html')
  
  mainWindow.on('close', () => {
    // Leave session when window closes
    zoomVideoSdk.leaveSession({ bEnd: false })
  })
}

app.on('ready', () => {
  createWindow()
})

app.on('will-quit', () => {
  // Cleanup SDK
  const cleanup = zoomVideoSdk.cleanup()
  if (cleanup === 0) {
    zoomVideoSdk.destroyZoomVideoSDKObj()
  }
})

// Enable @electron/remote for renderer
app.on('web-contents-created', (e, webContents) => {
  remote.enable(webContents)
})
```

### Renderer Process (Vue Component)

Access SDK from renderer via `@electron/remote`:

```javascript
// In Vue component
const remote = window.require('@electron/remote')
const zoomVideoSdk = remote.app.zoomVideoSdk

export default {
  data() {
    return {
      form: {
        sessionName: '',
        username: '',
        sessionPassword: '',
        token: '',
        isVideoMute: false,
        mute: false
      }
    }
  },
  
  methods: {
    // Join a session
    joinSession() {
      const result = zoomVideoSdk.joinSession({
        sessionName: this.form.sessionName,
        sessionPassword: this.form.sessionPassword,
        token: this.form.token,
        username: this.form.username,
        localVideoOn: !this.form.isVideoMute,  // Start with video on/off
        connect: true,                          // Connect audio
        mute: this.form.mute,                   // Start muted
        sessionIdleTimeoutMins: 40              // Session timeout (0 = never)
      })
      
      // Returns 0 on success, error code otherwise
      if (result === 0) {
        console.log('Join initiated successfully')
        // Wait for onSessionJoin callback
      } else {
        console.error('Join failed:', result)
      }
    },
    
    // Leave session
    leaveSession(endSession = false) {
      const result = zoomVideoSdk.leaveSession({
        bEnd: endSession  // true = end for all, false = just leave
      })
      console.log('Leave result:', result)
    },
    
    // Check if in session
    checkSession() {
      return zoomVideoSdk.isInSession()  // Returns boolean
    },
    
    // Get SDK version
    getVersion() {
      return zoomVideoSdk.getSDKVersion()
    }
  }
}
```

### Event Callbacks

Register callbacks to handle session events:

```javascript
import { ZoomVideoSDKCallback, ZoomVideoSDKErrors } from '../lib/zoom_video_sdk_defines'

// Set callback handler (call once in main mixin)
zoomVideoSdk.setNodeAddonCallbacks(onNodeAddonCallbacks)

function onNodeAddonCallbacks(result) {
  // Deserialize protobuf message
  const message = messages.CallbackBody.deserializeBinary(result)
  const callbackType = message.getMsgtype()
  
  switch (callbackType) {
    case ZoomVideoSDKCallback.onSessionJoin:
      console.log('Session joined successfully')
      // Get session info, initialize UI
      break
      
    case ZoomVideoSDKCallback.onSessionLeave:
      const reason = message.getOnsessionleaveparam().getEreason()
      console.log('Session left, reason:', reason)
      break
      
    case ZoomVideoSDKCallback.onError:
      const errorCode = message.getOnerrorparam().getErrorcode()
      console.error('Error:', errorCode)
      break
      
    case ZoomVideoSDKCallback.onUserJoin:
      const joinedUsers = message.getOnuserjoinparam().getZnUserlist().getUserList()
      console.log('Users joined:', joinedUsers.length)
      break
      
    case ZoomVideoSDKCallback.onUserLeave:
      const leftUsers = message.getOnuserleaveparam().getZnUserlist().getUserList()
      console.log('Users left:', leftUsers.length)
      break
      
    case ZoomVideoSDKCallback.onUserVideoStatusChanged:
      // Handle video on/off changes
      break
      
    case ZoomVideoSDKCallback.onUserAudioStatusChanged:
      // Handle audio mute/unmute changes
      break
      
    case ZoomVideoSDKCallback.onUserShareStatusChanged:
      // Handle screen share start/stop
      break
      
    case ZoomVideoSDKCallback.onSessionNeedPassword:
      // Prompt user for password
      break
      
    case ZoomVideoSDKCallback.onSessionPasswordWrong:
      // Show password error
      break
  }
}
```

### Video Helper

Control local and remote video:

```javascript
// Get video helper (after SDK initialized)
const videoHelper = zoomVideoSdk.getVideoHelper()

// Start/stop local video
videoHelper.startVideo()  // Returns 0 on success
videoHelper.stopVideo()

// Get available cameras
const cameras = videoHelper.getCameraList()
// Returns: [{ deviceID, deviceName, isSelectedDevice }, ...]

// Switch camera
videoHelper.selectCamera({ deviceID: 'camera-id' })

// Number of cameras
const count = videoHelper.getNumberOfCameras()

// Spotlight a user's video
videoHelper.spotLightVideo({ user: userObject })
videoHelper.unSpotLightVideo({ user: userObject })
videoHelper.unSpotlightAllVideos()

// Video quality preference
videoHelper.setVideoQualityPreference({
  mode: 0,  // 0=Balance, 1=Smoothness, 2=Sharpness, 3=Custom
  minimum_frame_rate: 15,  // 0-30
  maximum_frame_rate: 30
})

// Virtual background
videoHelper.addVirtualBackgroundItem({ imagePath: '/path/to/image.jpg' })
videoHelper.setVirtualBackgroundItem({ vbItemHandle: handle })
const vbItems = videoHelper.getVirtualBackgroundItemList()
```

### Audio Helper

Control audio devices and muting:

```javascript
// Get audio helper
const audioHelper = zoomVideoSdk.getAudioHelper()

// Start/stop audio
audioHelper.startAudio()
audioHelper.stopAudio()

// Mute/unmute (pass user object, or null for self)
audioHelper.muteAudio({ user: userObject })
audioHelper.unMuteAudio({ user: userObject })

// Get available speakers
const speakers = audioHelper.getSpeakerList()
// Returns: [{ deviceID, deviceName, isSelectedDevice }, ...]

// Get available microphones
const mics = audioHelper.getMicList()
// Returns: [{ deviceID, deviceName, isSelectedDevice }, ...]

// Select devices
audioHelper.selectSpeaker({ deviceID: 'speaker-id', deviceName: 'Speaker Name' })
audioHelper.selectMic({ deviceID: 'mic-id', deviceName: 'Mic Name' })

// Subscribe to raw audio data
audioHelper.subscribe()
audioHelper.unSubscribe()
```

### Session Info Helper

Get information about current session and users:

```javascript
// Get session info helper
const sessionInfo = zoomVideoSdk.getSessionInfo()

// Get current user
const myself = sessionInfo.getMyself()
// Returns: { userid, username, isHost, isVideoOn, isAudioMuted, ... }

// Get all users in session
const allUsers = sessionInfo.getAllUsers()

// Get session details
const sessionName = sessionInfo.getSessionName()
const sessionID = sessionInfo.getSessionID()
const sessionPassword = sessionInfo.getSessionPassword()
const sessionHostName = sessionInfo.getSessionHostName()
const sessionHost = sessionInfo.getSessionHost()
```

### Share Helper

Screen and window sharing:

```javascript
// Get share helper
const shareHelper = zoomVideoSdk.getShareHelper()

// Start sharing entire screen
shareHelper.startShareScreen({
  monitorID: 'monitor-id'  // From getShareableScreens()
})

// Start sharing specific window
shareHelper.startShareView({
  windowHandle: handle
})

// Stop sharing
shareHelper.stopShare()

// Get shareable screens/windows
const screens = shareHelper.getShareableScreens()
const windows = shareHelper.getShareableWindows()
```

## JWT Token Generation

Generate session tokens server-side:

```javascript
const KJUR = require('jsrsasign');

function generateSignature(sdkKey, sdkSecret, sessionName, role = 1) {
  const iat = Math.round(new Date().getTime() / 1000) - 30;
  const exp = iat + 60 * 60 * 2; // 2 hours

  const header = { alg: 'HS256', typ: 'JWT' };

  const payload = {
    app_key: sdkKey,
    tpc: sessionName,
    role_type: role, // 1 = host, 0 = participant
    version: 1,
    iat: iat,
    exp: exp
  };

  const sHeader = JSON.stringify(header);
  const sPayload = JSON.stringify(payload);
  
  return KJUR.jws.JWS.sign('HS256', sHeader, sPayload, sdkSecret);
}
```

## Error Codes

Common error codes from `ZoomVideoSDKErrors`:

| Error Code | Name | Description |
|------------|------|-------------|
| 0 | `ZoomVideoSDKErrors_Success` | Operation succeeded |
| 1 | `ZoomVideoSDKErrors_Wrong_Usage` | Incorrect usage of feature |
| 2 | `ZoomVideoSDKErrors_Internal_Error` | Internal SDK error |
| 3 | `ZoomVideoSDKErrors_Uninitialize` | SDK not initialized |
| 7 | `ZoomVideoSDKErrors_Invalid_Parameter` | Invalid parameter passed |
| 1001 | `ZoomVideoSDKErrors_Auth_Error` | General auth failure |
| 1003 | `ZoomVideoSDKErrors_Auth_Wrong_Key_or_Secret` | Invalid SDK credentials |
| 1500 | `ZoomVideoSDKErrors_JoinSession_NoSessionName` | Missing session name |
| 1501 | `ZoomVideoSDKErrors_JoinSession_NoSessionToken` | Missing JWT token |
| 1502 | `ZoomVideoSDKErrors_JoinSession_NoUserName` | Missing username |
| 1505 | `ZoomVideoSDKErrors_JoinSession_Invalid_SessionToken` | Invalid JWT token |
| 2003 | `ZoomVideoSDKErrors_Session_Join_Failed` | Failed to join session |
| 2010 | `ZoomVideoSDKErrors_Session_Need_Password` | Session requires password |
| 2011 | `ZoomVideoSDKErrors_Session_Password_Wrong` | Incorrect password |

## Raw Data Access

The SDK provides access to raw audio/video data for custom processing. Memory mode is configured during initialization:

```javascript
// Initialize with raw data memory mode
zoomVideoSdk.initialize({
  domain: 'https://www.zoom.us',
  audioRawDataMemoryMode: 0,  // 0 = stack (faster), 1 = heap (safer)
  videoRawDataMemoryMode: 0,
  shareRawDataMemoryMode: 0
})

// Subscribe to raw video/audio data
const videoHelper = zoomVideoSdk.getVideoHelper()
const audioHelper = zoomVideoSdk.getAudioHelper()

// Subscribe user's video (for custom rendering)
const userHelper = zoomVideoSdk.getUserHelper()
userHelper.subscribe({
  user: userObject,
  recv_handle: handleId,      // Unique handle for this subscription
  resolution: 1,              // 0=90P, 1=180P, 2=360P, 3=720P, 4=1080P
  dataType: 0                 // 0=video, 1=share
})

userHelper.unSubscribe({
  user: userObject,
  recv_handle: handleId,
  dataType: 0
})

// Raw data is delivered via onRawDataStatusChanged callback
```

**Security Note**: Raw data transmitted between the native addon and Electron is not encrypted by default in the sample app. For production use, implement additional protection for raw data transmission.

## Additional Helpers

### Chat Helper

```javascript
const chatHelper = zoomVideoSdk.getChatHelper()

// Send chat message
chatHelper.sendChat({
  content: 'Hello everyone!',
  receiver: null  // null = send to everyone, or userObject for private
})

// Chat messages arrive via onChatNewMessageNotify callback
```

### Recording Helper

```javascript
const recordingHelper = zoomVideoSdk.getRecordingHelper()

// Cloud recording (if enabled)
recordingHelper.startCloudRecording()
recordingHelper.stopCloudRecording()

// Check recording status
recordingHelper.canStartRecording()
```

### Live Transcription Helper

```javascript
const transcriptionHelper = zoomVideoSdk.getLiveTranscriptionHelper()

// Enable live transcription
transcriptionHelper.startLiveTranscription()
transcriptionHelper.stopLiveTranscription()

// Check if available
transcriptionHelper.canStartLiveTranscription()
```

### Command Channel

Send custom commands between participants:

```javascript
const cmdHelper = zoomVideoSdk.getCmdHelper()

// Send command to all or specific user
cmdHelper.sendCommand({
  strCmd: 'my-custom-command|data',
  receiver: null  // null = all, or userObject for specific
})

// Commands arrive via onCommandReceived callback
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `Cannot find module '*.node'` | Native addon not built | Run `npm run electron:serve` to rebuild |
| `Python not found` | Python not in PATH | Add Python to system PATH |
| `distutils module missing` | Python 3.12+ | Use Python < 3.12 |
| `node-gyp build failed` | Missing build tools | Install Visual Studio (Windows) or Xcode (macOS) |
| `Protobuf errors` | Missing protobuf source | Follow protobuf installation steps |
| `@electron/remote` errors | Remote not initialized | Call `remote.initialize()` in main process |
| Join returns error 1505 | Invalid JWT token | Check token generation, ensure `tpc` matches session name |

### Build Errors

```bash
# Clean and rebuild
rm -rf node_modules
rm -rf build
npm cache clean --force
npm install
npm run electron:serve
```

### Debug Logging

Enable SDK logging during initialization:

```javascript
zoomVideoSdk.initialize({
  domain: 'https://www.zoom.us',
  enableLog: true,
  logFilePrefix: 'videosdk'  // Creates videosdk_*.log files
})
```

Logs are written to:
- **Windows**: `%APPDATA%/videosdk/`
- **macOS**: `~/Library/Logs/videosdk/`
- **Linux**: `~/.videosdk/logs/`

## Dependencies

From `package.json` (v2.4.5):

```json
{
  "dependencies": {
    "@electron/remote": "^2.0.5",
    "electron": "^33.0.0",
    "element-ui": "^2.13.0",
    "google-protobuf": "^3.21.4",
    "vue": "~2.6.11",
    "vue-router": "^3.1.5",
    "vuex": "^3.1.2"
  },
  "devDependencies": {
    "@vue/cli-service": "^5.0.8",
    "native-ext-loader": "^2.3.0",
    "sass": "~1.32.6",
    "sass-loader": "^8.0.2",
    "vue-cli-plugin-electron-builder": "^2.1.1",
    "vue-template-compiler": "~2.6.11"
  }
}
```

## Supported Platforms

| Platform | Architecture | Support Status |
|----------|--------------|----------------|
| Windows | x64 | ✅ Supported |
| Windows | x86 (ia32) | ✅ Supported |
| macOS | x64 | ✅ Supported |
| macOS | arm64 (Apple Silicon) | ✅ Supported |
| Linux | x64 | ✅ Supported |

## Supported Electron Versions

| Electron Version | Support Status |
|------------------|----------------|
| 33.0.0 | ✅ Recommended |
| 28.x - 32.x | ✅ Supported |
| 10.x - 27.x | ⚠️ May work, not officially supported |
| < 10.x | ❌ Not supported |

## Resources

| Resource | URL |
|----------|-----|
| **Sample Repository** | [zoom/videosdk-electron-sample](https://github.com/zoom/videosdk-electron-sample) |
| **Video SDK docs** | https://developers.zoom.us/docs/video-sdk/ |
| **Electron changelog** | https://devsupport.zoom.us/hc/en-us/sections/11766697610765-Electron-demo |
| **Developer forum** | https://devforum.zoom.us/ |

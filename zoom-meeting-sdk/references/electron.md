# Meeting SDK - Electron

Build cross-platform desktop applications with Zoom Meeting SDK and Electron.

## Overview

The Zoom Meeting SDK for Electron allows you to embed the full Zoom meeting experience into Electron desktop applications for Windows and macOS.

**Current Version**: 6.7.2.72402 (December 2025)

> **Note**: The GitHub repo ([zoom-sdk-electron](https://github.com/zoom/zoom-sdk-electron)) is archived, but the SDK is **actively maintained** and distributed via [Zoom Marketplace](https://marketplace.zoom.us/).

## Getting the SDK

**Important**: Download from Zoom Marketplace (not GitHub):

1. Log in to [Zoom Marketplace](https://marketplace.zoom.us/)
2. Go to **Develop** → **Build App**
3. Create or select a **Meeting SDK** app
4. Go to **Download** section
5. Download **Electron** SDK package

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Node.js | 20.17.0 |
| Electron | 39.2.2 (per package.json) |
| Protobuf | 22.3 |
| Python | 3.x (below 3.12) |

### Platform-Specific

| Platform | Requirements |
|----------|-------------|
| **Windows** | Visual Studio 2019+ OR Windows Build Tools |
| **macOS** | Xcode 14+ |

## SDK Architecture

The SDK uses a singleton pattern with these main modules:

```
ZoomSDK (singleton)
├── InitSDK()           # Initialize SDK
├── CleanUPSDK()        # Cleanup
├── GetAuth()           # → ZoomAuth module
├── GetMeeting()        # → ZoomMeeting module
├── GetSetting()        # → ZoomSetting module
└── RawData()           # → Raw data access
```

## Installation

### Step 1: Extract SDK

```bash
unzip zoom-sdk-electron-6.7.2.72402.zip
cd zoom-sdk-electron
```

### Step 2: Install Protobuf 22.3

```bash
# Download protobuf
wget https://github.com/protocolbuffers/protobuf/releases/download/v22.3/protobuf-22.3.tar.gz
tar -xzf protobuf-22.3.tar.gz
mv protobuf-22.3/src protobuf_src

# Add abseil-cpp
wget https://github.com/abseil/abseil-cpp/archive/refs/tags/20230802.1.tar.gz
tar -xzf 20230802.1.tar.gz
cp -r abseil-cpp-20230802.1/absl protobuf_src/

# Copy to lib
mkdir -p lib/node_add_on
cp -r protobuf_src lib/node_add_on/
```

### Step 3: Run

```bash
npm run electron:serve
```

## Code Examples (from SDK source)

### Initialize SDK

```javascript
const { ZoomSDK } = require('./lib/zoom_sdk.js');

// Get singleton instance
const zoomSdk = ZoomSDK.getInstance();

// Initialize SDK
const initResult = zoomSdk.InitSDK({
  path: './sdk',                    // Path to native SDK files
  domain: 'https://www.zoom.us',    // Zoom domain
  enable_log: true,                 // Enable logging
  langid: 1,                        // Language (1 = English)
  logfilesize: 5,                   // Log file size in MB
  enableGenerateDump: false,        // Generate dump on crash
  useCustomUI: false                // Use default Zoom UI
});

if (initResult === 0) { // SDKERR_SUCCESS
  console.log('SDK initialized');
}
```

### Authenticate with JWT

```javascript
// Get Auth module
const zoomAuth = zoomSdk.GetAuth({
  authcb: (result) => {
    // 0 = AUTHRET_SUCCESS
    if (result === 0) {
      console.log('Authentication successful');
    }
  },
  onZoomIdentityExpired: () => {
    console.log('Identity expired - re-authenticate');
  }
});

// Authenticate with JWT token
const authResult = zoomAuth.AuthWithJwtToken(jwtToken);
```

### Join Meeting

```javascript
// Get Meeting module (after auth success)
const zoomMeeting = zoomSdk.GetMeeting({
  meetingstatuscb: (status, result) => {
    // Status codes from ZoomMeetingStatus enum
    switch (status) {
      case 1: console.log('Connecting...'); break;
      case 2: console.log('Waiting for host...'); break;
      case 3: console.log('In meeting'); break;
      case 4: console.log('Disconnecting...'); break;
      case 5: console.log('Reconnecting...'); break;
      case 6: console.log('Meeting ended'); break;
      case 7: console.log('Meeting failed', result); break;
    }
  }
});

// Join with login
const joinResult = zoomMeeting.JoinMeeting({
  meetingnum: 1234567890,           // Meeting number
  username: 'John Doe',             // Display name
  psw: 'password123',               // Meeting password
  isvideooff: false,                // Start with video on
  isaudiooff: false                 // Start with audio on
});

// Or join WITHOUT login (most common for SDK apps)
const joinResult = zoomMeeting.JoinMeetingWithoutLogin({
  meetingnum: 1234567890,
  username: 'John Doe',
  psw: 'password123',
  userZAK: '',                      // ZAK token (optional)
  isvideooff: false,
  isaudiooff: false
});
```

### Start Meeting (as Host)

```javascript
// Start meeting (requires login)
const startResult = zoomMeeting.StartMeeting({
  meetingnum: 1234567890,
  isvideooff: false,
  isaudiooff: false
});

// Or start WITHOUT login (using ZAK token)
const startResult = zoomMeeting.StartMeetingWithOutLogin({
  zoomaccesstoken: 'YOUR_ZAK_TOKEN',  // Host's ZAK token
  username: 'Host Name',
  zoomusertype: 0,                     // ZoomUserType_APIUSER
  meetingnum: 1234567890
});
```

### Leave Meeting

```javascript
// Leave meeting (participant)
zoomMeeting.LeaveMeeting({ endMeeting: false });

// End meeting (host only)
zoomMeeting.LeaveMeeting({ endMeeting: true });
```

### Cleanup

```javascript
// On app quit
app.on('will-quit', () => {
  zoomSdk.CleanUPSDK();
});
```

## Available Modules

After authentication, access these sub-modules via `GetMeeting()`:

| Module | Access Method | Purpose |
|--------|---------------|---------|
| Audio | `GetMeetingAudio()` | Mute/unmute, audio settings |
| Video | `GetMeetingVideo()` | Start/stop video, spotlight |
| Share | `GetMeetingShare()` | Screen sharing |
| Chat | `GetMeetingChat()` | In-meeting chat |
| Participants | `GetMeetingParticipantsCtrl()` | Participant management |
| Recording | `GetMeetingRecording()` | Local/cloud recording |
| Webinar | `GetMeetingWebinar()` | Webinar controls |
| AI Companion | `GetMeetingAICompanion()` | AI features |
| Whiteboard | `GetMeetingWhiteboard()` | Whiteboard controls |
| Polling | `GetMeetingPolling()` | Meeting polls |
| Waiting Room | `GetMeetingWaitingRoom()` | Waiting room controls |
| Breakout Rooms | Via configuration | Breakout room management |

## Raw Data Access

For custom video/audio processing:

```javascript
// Set pipe names BEFORE joining
zoomMeeting.SetPipeName({
  videoPipeName: 'zoom_video_pipe',
  sharePipeName: 'zoom_share_pipe',
  audioPipeName: 'zoom_audio_pipe',
  maxReadLength: 1920 * 1080 * 3 / 2  // YUV420 frame size
});

// Join with raw data enabled
zoomMeeting.JoinMeetingWithoutLogin({
  meetingnum: 1234567890,
  username: 'Bot',
  withRawdata: true  // Enable raw data
});
```

**Note**: Raw data is transmitted via named pipes. Add encryption for production.

## JWT Token Generation

Generate server-side:

```javascript
const KJUR = require('jsrsasign');

function generateSignature(sdkKey, sdkSecret, meetingNumber, role) {
  const iat = Math.round(Date.now() / 1000) - 30;
  const exp = iat + 60 * 60 * 2; // 2 hours

  const payload = {
    sdkKey: sdkKey,
    appKey: sdkKey,
    mn: meetingNumber,
    role: role,  // 0 = participant, 1 = host
    iat: iat,
    exp: exp,
    tokenExp: exp
  };

  return KJUR.jws.JWS.sign('HS256', 
    JSON.stringify({ alg: 'HS256', typ: 'JWT' }), 
    JSON.stringify(payload), 
    sdkSecret
  );
}
```

## Error Codes

| Code | Constant | Meaning |
|------|----------|---------|
| 0 | SDKERR_SUCCESS | Success |
| 3 | SDKERR_INVALID_PARAMETER | Bad parameter |
| 7 | SDKERR_UNINITIALIZE | SDK not initialized |
| 8 | SDKERR_UNAUTHENTICATION | Not authenticated |
| 12 | SDKERR_NO_PERMISSION | No permission |

## Supported Platforms

| Platform | Architecture | Status |
|----------|--------------|--------|
| Windows | x64, x86 | Supported |
| macOS | x64, arm64 | Supported |
| Linux | - | Not supported |

## Resources

- **Docs**: https://developers.zoom.us/docs/meeting-sdk/electron/
- **Changelog**: https://devsupport.zoom.us/hc/en-us/sections/11766698871693-Electron
- **Forum**: https://devforum.zoom.us/

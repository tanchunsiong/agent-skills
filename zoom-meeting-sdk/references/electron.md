# Meeting SDK - Electron

Build cross-platform desktop applications with Zoom Meeting SDK and Electron.

## Overview

The Zoom Meeting SDK for Electron allows you to embed the full Zoom meeting experience into Electron desktop applications for Windows and macOS.

**Current Version**: 6.7.2.72402 (December 2025)

> **Note**: The GitHub repo ([zoom-sdk-electron](https://github.com/zoom/zoom-sdk-electron)) is archived, but the SDK is **actively maintained** and distributed via [Zoom Marketplace](https://marketplace.zoom.us/).

## Meeting SDK vs Video SDK for Electron

| Aspect | Meeting SDK Electron | Video SDK Electron |
|--------|---------------------|-------------------|
| **UI** | Zoom's meeting UI | Fully custom UI |
| **Experience** | Full Zoom meetings | Video sessions |
| **Features** | All Zoom features (breakouts, reactions, etc.) | Core video features |
| **Platforms** | Windows, macOS | Windows, macOS, Linux |
| **Distribution** | Marketplace download | GitHub |

**Choose Meeting SDK** if you want the full Zoom meeting experience with Zoom's UI.
**Choose Video SDK** if you need full UI customization or Linux support.

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

## Getting the SDK

**Important**: The Electron SDK is not available on GitHub. Download from Zoom Marketplace:

1. Log in to [Zoom Marketplace](https://marketplace.zoom.us/)
2. Go to **Develop** → **Build App**
3. Create or select a **Meeting SDK** app
4. Go to **Download** section
5. Download **Electron** SDK package

The download will be a ZIP file like `zoom-sdk-electron-6.7.2.72402.zip`.

## Project Structure

```
zoom-sdk-electron/
├── README.md
├── package.json
├── binding.gyp              # Native addon build config
├── public/
│   └── index.html
├── sdk/
│   ├── win64/              # Windows native libraries
│   │   ├── *.dll
│   │   └── language/       # Language packs
│   └── mac/                # macOS native libraries
├── lib/
│   └── node_add_on/
│       └── protobuf_src/   # Protobuf source (you add this)
├── src/
│   ├── main/              # Electron main process
│   └── renderer/          # Electron renderer process
└── scripts/
    └── electron_sdk_install.js
```

## Installation

### Step 1: Extract the SDK

```bash
unzip zoom-sdk-electron-6.7.2.72402.zip -d zoom-sdk-electron
cd zoom-sdk-electron
```

### Step 2: Install Protobuf 22.3

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
# Install Xcode from App Store or:
xcode-select --install
```

### Step 4: Run the Sample App

```bash
npm run electron:serve
```

This command:
1. Runs `scripts/electron_sdk_install.js`
2. Installs dependencies based on `package.json`
3. Builds native addons
4. Launches the sample app

## Code Examples

### Main Process (main.js)

```javascript
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

// Load Meeting SDK native addon
const ZoomMeetingSDK = require('./sdk/zoomsdk.node');

let mainWindow;

app.whenReady().then(() => {
  // Initialize SDK
  const initResult = ZoomMeetingSDK.InitSDK({
    path: path.join(__dirname, 'sdk'),
    domain: 'zoom.us'
  });
  
  console.log('SDK Init:', initResult);
  createWindow();
});

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 720,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });
  
  mainWindow.loadFile('public/index.html');
}

// Handle join meeting request from renderer
ipcMain.handle('join-meeting', async (event, config) => {
  const authResult = ZoomMeetingSDK.Auth({
    sdkKey: config.sdkKey,
    signature: config.signature
  });
  
  if (authResult === 0) {
    const joinResult = ZoomMeetingSDK.JoinMeeting({
      meetingNumber: config.meetingNumber,
      userName: config.userName,
      passWord: config.passWord
    });
    return { success: joinResult === 0, code: joinResult };
  }
  
  return { success: false, code: authResult };
});

app.on('window-all-closed', () => {
  ZoomMeetingSDK.CleanUPSDK();
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
```

### Renderer Process

```javascript
const { ipcRenderer } = require('electron');

async function joinMeeting() {
  const config = {
    sdkKey: 'YOUR_SDK_KEY',
    signature: await getSignatureFromServer(), // Get from your auth server
    meetingNumber: document.getElementById('meetingNumber').value,
    userName: document.getElementById('userName').value,
    passWord: document.getElementById('password').value
  };
  
  const result = await ipcRenderer.invoke('join-meeting', config);
  
  if (result.success) {
    console.log('Joined meeting successfully');
  } else {
    console.error('Failed to join meeting:', result.code);
  }
}
```

### JWT Signature Generation (Server-Side)

```javascript
const KJUR = require('jsrsasign');

function generateSignature(sdkKey, sdkSecret, meetingNumber, role) {
  const iat = Math.round(new Date().getTime() / 1000) - 30;
  const exp = iat + 60 * 60 * 2; // 2 hours

  const header = { alg: 'HS256', typ: 'JWT' };

  const payload = {
    sdkKey: sdkKey,
    appKey: sdkKey,
    mn: meetingNumber,
    role: role, // 0 = participant, 1 = host
    iat: iat,
    exp: exp,
    tokenExp: exp
  };

  return KJUR.jws.JWS.sign('HS256', JSON.stringify(header), JSON.stringify(payload), sdkSecret);
}
```

## Raw Data Access

Access raw audio/video data for custom processing:

```javascript
// Enable raw data in initialization
ZoomMeetingSDK.InitSDK({
  path: path.join(__dirname, 'sdk'),
  domain: 'zoom.us',
  enableRawData: true
});

// Set up raw data callbacks
ZoomMeetingSDK.SetRawDataCallback({
  onVideoRawDataReceived: (userId, data, width, height) => {
    // Process video frame (YUV420)
  },
  onAudioRawDataReceived: (data, sampleRate, channels) => {
    // Process audio (PCM)
  }
});
```

**Security Note**: Raw data is not encrypted in the demo. Add protection for production use.

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `Cannot find module '*.node'` | Native addon not built | Run `npm run electron:serve` |
| `Python not found` | Python not in PATH | Add Python to system PATH |
| `distutils module missing` | Python 3.12+ | Use Python < 3.12 |
| `node-gyp build failed` | Missing build tools | Install Visual Studio (Windows) or Xcode (macOS) |
| `Protobuf errors` | Missing protobuf source | Follow protobuf installation steps |
| `SDK Auth failed` | Invalid credentials | Verify SDK Key and signature |

### Debug Logging

Enable SDK logging:

```javascript
ZoomMeetingSDK.InitSDK({
  path: path.join(__dirname, 'sdk'),
  domain: 'zoom.us',
  enableLog: true,
  logFilePrefix: 'meetingsdk'
});
```

Log locations:
- **Windows**: `%APPDATA%/zoomsdk/`
- **macOS**: `~/Library/Logs/zoomsdk/`

## Supported Platforms

| Platform | Architecture | Status |
|----------|--------------|--------|
| Windows | x64 | Supported |
| macOS | x64, arm64 | Supported |
| Linux | - | Not supported (use Video SDK) |

## Electron Version Compatibility

| Electron Version | Support Status |
|------------------|----------------|
| 33.0.0 | Recommended |
| 28.x - 32.x | Supported |
| < 28.x | May work, not officially tested |

## Resources

- **Official docs**: https://developers.zoom.us/docs/meeting-sdk/electron/
- **Changelog**: https://devsupport.zoom.us/hc/en-us/sections/11766698871693-Electron
- **Developer forum**: https://devforum.zoom.us/
- **Download SDK**: [Zoom Marketplace](https://marketplace.zoom.us/)

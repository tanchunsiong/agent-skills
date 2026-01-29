# Video SDK - Electron

Build cross-platform desktop video applications with Zoom Video SDK and Electron.

## Overview

The Zoom Video SDK Electron integration uses native Node.js addons to provide full Video SDK functionality in Electron apps. This enables building desktop applications for Windows, macOS, and Linux with custom video experiences.

**Current Version**: v2.4.5 (December 2025)

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

## Project Structure

```
your-electron-app/
├── config.json              # SDK configuration (domain)
├── package.json             # Dependencies and scripts
├── binding.gyp              # Native addon build config
├── lib/
│   └── node_add_on/
│       └── protobuf_src/    # Protobuf source files
├── sdk/                     # Video SDK native libraries
├── src/
│   ├── main/               # Electron main process
│   └── renderer/           # Electron renderer process
└── public/                 # Static assets
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

### Main Process (main.js)

```javascript
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

// Load Video SDK native addon
const ZoomVideoSDK = require('./sdk/zoomvideosdk.node');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 720,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  mainWindow.loadFile('public/index.html');
}

app.whenReady().then(() => {
  createWindow();
  
  // Initialize Video SDK
  const initResult = ZoomVideoSDK.InitSDK({
    domain: 'zoom.us',
    enableLog: true
  });
  
  console.log('SDK Init Result:', initResult);
});

// Handle IPC from renderer
ipcMain.handle('join-session', async (event, { topic, token, userName }) => {
  const joinResult = ZoomVideoSDK.JoinSession({
    sessionName: topic,
    sessionToken: token,
    userName: userName
  });
  return joinResult;
});

ipcMain.handle('leave-session', async () => {
  return ZoomVideoSDK.LeaveSession();
});

app.on('window-all-closed', () => {
  ZoomVideoSDK.CleanUpSDK();
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
```

### Renderer Process (renderer.js)

```javascript
const { ipcRenderer } = require('electron');

// Join a video session
async function joinSession() {
  const topic = document.getElementById('topic').value;
  const token = document.getElementById('token').value;
  const userName = document.getElementById('userName').value;
  
  try {
    const result = await ipcRenderer.invoke('join-session', {
      topic,
      token,
      userName
    });
    
    if (result.success) {
      console.log('Joined session successfully');
      startVideo();
    } else {
      console.error('Failed to join:', result.error);
    }
  } catch (error) {
    console.error('Join error:', error);
  }
}

// Leave session
async function leaveSession() {
  await ipcRenderer.invoke('leave-session');
}

// Start video
function startVideo() {
  // Video rendering is handled by the native addon
  // The video canvas is rendered to the specified element
}
```

### HTML Template

```html
<!DOCTYPE html>
<html>
<head>
  <title>Video SDK Electron App</title>
</head>
<body>
  <div id="app">
    <div id="join-form">
      <input type="text" id="topic" placeholder="Session Topic" />
      <input type="text" id="token" placeholder="JWT Token" />
      <input type="text" id="userName" placeholder="Your Name" />
      <button onclick="joinSession()">Join</button>
    </div>
    
    <div id="video-container">
      <!-- Video will be rendered here by native addon -->
      <canvas id="video-canvas"></canvas>
    </div>
    
    <div id="controls">
      <button onclick="leaveSession()">Leave</button>
    </div>
  </div>
  
  <script src="renderer.js"></script>
</body>
</html>
```

## JWT Token Generation

Generate session tokens server-side:

```javascript
const KJUR = require('jsrsasign');

function generateSignature(sdkKey, sdkSecret, topic, role = 1) {
  const iat = Math.round(new Date().getTime() / 1000) - 30;
  const exp = iat + 60 * 60 * 2; // 2 hours

  const header = { alg: 'HS256', typ: 'JWT' };

  const payload = {
    app_key: sdkKey,
    tpc: topic,
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

## Raw Data Access

The Electron SDK provides access to raw audio/video data for custom processing:

```javascript
// In main process
ZoomVideoSDK.SetRawDataCallback({
  onVideoRawDataReceived: (userId, data, width, height) => {
    // Process raw video frame (YUV420 format)
    // data is a Buffer containing the frame data
    processVideoFrame(userId, data, width, height);
  },
  
  onAudioRawDataReceived: (data, sampleRate, channels) => {
    // Process raw audio (PCM format)
    processAudioData(data, sampleRate, channels);
  }
});
```

**Security Note**: Raw data transmitted between the native addon and Electron is not encrypted by default in the sample app. For production use, implement additional protection for raw data transmission.

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `Cannot find module '*.node'` | Native addon not built | Run `npm run electron:serve` to rebuild |
| `Python not found` | Python not in PATH | Add Python to system PATH |
| `distutils module missing` | Python 3.12+ | Use Python < 3.12 |
| `node-gyp build failed` | Missing build tools | Install Visual Studio (Windows) or Xcode (macOS) |
| `Protobuf errors` | Missing protobuf source | Follow protobuf installation steps |

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

Enable SDK logging in config:

```javascript
ZoomVideoSDK.InitSDK({
  domain: 'zoom.us',
  enableLog: true,
  logFilePrefix: 'videosdk'
});
```

Logs are written to:
- **Windows**: `%APPDATA%/videosdk/`
- **macOS**: `~/Library/Logs/videosdk/`
- **Linux**: `~/.videosdk/logs/`

## Supported Electron Versions

| Electron Version | Support Status |
|------------------|----------------|
| 33.0.0 | ✅ Recommended |
| 28.x - 32.x | ✅ Supported |
| 10.x - 27.x | ⚠️ May work, not officially supported |
| < 10.x | ❌ Not supported |

## Sample Repository

| Repository | Description |
|------------|-------------|
| [zoom/videosdk-electron-sample](https://github.com/zoom/videosdk-electron-sample) | Official Electron sample app |

## Resources

- **Video SDK docs**: https://developers.zoom.us/docs/video-sdk/
- **Electron changelog**: https://devsupport.zoom.us/hc/en-us/sections/11766697610765-Electron-demo
- **Developer forum**: https://devforum.zoom.us/

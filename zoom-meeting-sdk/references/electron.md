# Meeting SDK - Electron

Desktop meeting applications with Electron.

## Overview

Electron SDK for building cross-platform desktop meeting applications using web technologies.

## Prerequisites

- Meeting SDK Electron package
- Electron 12+
- Node.js 14+
- Valid SDK credentials from [Marketplace](https://marketplace.zoom.us/) (sign-in required)

## Installation

```bash
npm install @zoom/meetingsdk-electron
```

## Quick Start

```javascript
const { ZoomSDK } = require('@zoom/meetingsdk-electron');

// Initialize
const zoomSDK = new ZoomSDK();
zoomSDK.config({
  sdkKey: SDK_KEY,
  sdkSecret: SDK_SECRET,
  webEndpoint: 'zoom.us',
});

// Join meeting
zoomSDK.joinMeeting({
  meetingNumber: meetingNumber,
  userName: 'User',
  password: password,
});
```

## Event Handling

```javascript
zoomSDK.on('meeting-status-changed', (status) => {
  console.log('Meeting status:', status);
});

zoomSDK.on('user-join', (user) => {
  console.log('User joined:', user);
});
```

## Common Tasks

### Main/Renderer Process Communication (IPC)

**Main process (main.js)**:
```javascript
const { app, BrowserWindow, ipcMain } = require('electron');
const { ZoomSDK } = require('@zoom/meetingsdk-electron');

let zoomSDK;

app.whenReady().then(() => {
    zoomSDK = new ZoomSDK();
    zoomSDK.config({
        sdkKey: SDK_KEY,
        sdkSecret: SDK_SECRET,
    });
    
    createWindow();
});

// Handle renderer requests
ipcMain.handle('join-meeting', async (event, data) => {
    const result = await zoomSDK.joinMeeting({
        meetingNumber: data.number,
        password: data.password,
        displayName: data.name
    });
    return result;
});

ipcMain.handle('leave-meeting', async () => {
    return await zoomSDK.leaveMeeting();
});
```

**Preload script (preload.js)**:
```javascript
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('zoomAPI', {
    joinMeeting: (data) => ipcRenderer.invoke('join-meeting', data),
    leaveMeeting: () => ipcRenderer.invoke('leave-meeting'),
    onMeetingStatus: (callback) => ipcRenderer.on('meeting-status', callback)
});
```

**Renderer process**:
```javascript
// Access via window.zoomAPI
window.zoomAPI.joinMeeting({
    number: '123456789',
    password: 'pass',
    name: 'John Doe'
}).then(result => {
    console.log('Joined:', result);
});
```

### Window Management

```javascript
// Create meeting window
function createMeetingWindow() {
    const meetingWindow = new BrowserWindow({
        width: 1024,
        height: 768,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: false,
            contextIsolation: true
        }
    });
    
    // Handle close - leave meeting first
    meetingWindow.on('close', async (e) => {
        if (zoomSDK.isInMeeting()) {
            e.preventDefault();
            await zoomSDK.leaveMeeting();
            meetingWindow.close();
        }
    });
}
```

### Native Module Compilation

**Common issue**: Node.js version mismatch

```json
{
  "engines": {
    "node": ">=16.0.0 <19.0.0"
  },
  "devDependencies": {
    "electron-rebuild": "^3.2.9"
  },
  "scripts": {
    "postinstall": "electron-rebuild -f -w @zoom/meetingsdk-electron"
  }
}
```

**Rebuild after Electron update**:
```bash
npx electron-rebuild -f -w @zoom/meetingsdk-electron
```

### Packaging with electron-builder

```json
{
  "build": {
    "appId": "com.yourcompany.zoomapp",
    "productName": "Your Zoom App",
    "files": [
      "dist/**/*",
      "node_modules/@zoom/**/*"
    ],
    "win": {
      "target": ["nsis", "portable"],
      "extraFiles": [{
        "from": "resources/zoom-sdk-binaries",
        "to": "resources"
      }]
    },
    "mac": {
      "target": ["dmg"],
      "extendInfo": {
        "NSCameraUsageDescription": "Need camera for meetings",
        "NSMicrophoneUsageDescription": "Need mic for meetings"
      }
    },
    "linux": {
      "target": ["AppImage", "deb"]
    }
  }
}
```

## Cross-Platform Considerations

| Platform | Key Consideration |
|----------|-------------------|
| **Windows** | Copy all DLLs from SDK to resources folder; handle code signing |
| **macOS** | Cannot sandbox for App Store; notarize for Gatekeeper |
| **Linux** | Package as AppImage with dependencies; test on multiple distros |

## Important Notice

**The Meeting SDK for Electron was archived in May 2025**. For new projects, consider using:
- **Video SDK Electron**: https://github.com/zoom/videosdk-electron-sample
- **Meeting SDK Web**: Embedded in Electron via webview

## Resources

- **Electron docs**: https://developers.zoom.us/docs/meeting-sdk/electron/
- **Video SDK Electron Sample**: https://github.com/zoom/videosdk-electron-sample

# SDK Logs & Troubleshooting

Collecting SDK logs for debugging and support.

## Overview

SDK logs help diagnose issues during development and for Zoom support escalations.

## Enabling Logs

### Web SDK

```javascript
// Enable verbose logging
ZoomMtg.setLogLevel('verbose');

// Or for Video SDK
client.init('en-US', 'CDN', { debug: true });
```

### iOS SDK

```swift
// Set log file path
let initParams = MobileRTCSDKInitParams()
initParams.enableLog = true
initParams.logFilePrefix = "zoom_sdk"
```

### Android SDK

```kotlin
val initParams = ZoomSDKInitParams().apply {
    enableLog = true
    logSize = 5 // MB
}
```

### Desktop SDKs (Windows/macOS/Linux)

```cpp
initParam.enableLogByDefault = true;
initParam.logFilePrefix = L"zoom_sdk";
```

## Log Locations

| Platform | Default Location |
|----------|------------------|
| iOS | App's Documents directory |
| Android | App's files directory |
| Windows | `%APPDATA%\ZoomSDK\` |
| macOS | `~/Library/Logs/ZoomSDK/` |
| Linux | Working directory |

## Common Issues and Solutions

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| Join failed | Invalid signature | Check JWT generation (exp should be ~10s after iat, but iat can be up to 2 hours in past) |
| Join failed | Meeting not found | Verify meeting number and that meeting hasn't ended |
| No audio | Permission denied | Request microphone permission before joining |
| No video | Permission denied | Request camera permission before joining |
| Video scales down | Container too small | Ensure container is at least 1280x720 for 720p |
| SharedArrayBuffer error | Missing headers | Add COOP/COEP headers to server |
| Error code 0 | Actually success | Check SDK docs - 0 often means success, not error |
| SDK crash | ProGuard enabled | Disable ProGuard/R8 for Zoom SDK classes |
| DLL not found | Missing files | Copy ALL DLLs from SDK bin folder |

### Debugging Join Failures

```javascript
// Web SDK - enable verbose logging
ZoomMtg.setLogLevel('verbose');

// Check signature
console.log('Signature:', signature);
console.log('Meeting:', meetingNumber);

// Verify callback
client.join({
  // ...params
  success: (res) => console.log('Join success:', res),
  error: (err) => console.error('Join error:', err)
});
```

### Debugging Audio/Video Issues

```javascript
// Check device availability
const devices = await navigator.mediaDevices.enumerateDevices();
console.log('Audio inputs:', devices.filter(d => d.kind === 'audioinput'));
console.log('Video inputs:', devices.filter(d => d.kind === 'videoinput'));

// Check permissions
const micPermission = await navigator.permissions.query({ name: 'microphone' });
const camPermission = await navigator.permissions.query({ name: 'camera' });
console.log('Mic:', micPermission.state);
console.log('Cam:', camPermission.state);
```

### Native SDK Crash Debugging

**iOS**:
```swift
// Enable crash reporting
MobileRTC.shared().setEnableCrashReport(true)

// Get logs
let logPath = MobileRTC.shared().getLogPath()
print("Logs at: \(logPath)")
```

**Android**:
```kotlin
// Check logcat for crashes
adb logcat -s ZoomSDK:V

// Disable ProGuard for Zoom
// In proguard-rules.pro:
-keep class us.zoom.** { *; }
-keep interface us.zoom.** { *; }
```

### Error Code Reference

| Code | Meaning | Platform |
|------|---------|----------|
| 0 | Success (NOT error!) | All |
| 1 | Generic error | All |
| 2 | Invalid argument | All |
| 3 | Invalid token | All |
| 4 | Timeout | All |
| 8 | SDK not authorized | Windows |
| 100000400 | Meeting join failed | Windows |
| MobileRTCMeetError_Success | Success | iOS |
| MEETING_STATUS_INMEETING | In meeting | Android |

## Getting Support

When contacting Zoom support:

1. Include SDK version
2. Attach log files
3. Describe steps to reproduce
4. Include error codes (check if 0 means success!)

## Resources

- **Developer support**: https://devsupport.zoom.us/
- **Developer forum**: https://devforum.zoom.us/

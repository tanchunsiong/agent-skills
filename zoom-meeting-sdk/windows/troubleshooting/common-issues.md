# Common Issues & Troubleshooting Checklist

## Quick Diagnostic Workflow

### Build Issues vs Runtime Issues

**Build issues** = Problems during compilation (Visual Studio errors)
**Runtime issues** = Problems when running the executable (authentication, joining meetings)

Use this flowchart:

```
Does your code compile?
├─ NO  → See "Build Issues Checklist" below
└─ YES → Does authentication succeed?
          ├─ NO  → See "Authentication Issues" below
          └─ YES → Does meeting join succeed?
                   ├─ NO  → See "Meeting Join Issues" below
                   └─ YES → Does video capture work?
                            ├─ NO  → See "Video Capture Issues" below
                            └─ YES → You're all set!
```

---

## Build Issues Checklist

### ✅ Compiler Errors with `uint32_t`, `AudioType`, or `YUVRawDataI420`

**Symptoms**:
- `Error C2061: syntax error: identifier 'uint32_t'`
- `Error C3646: 'GetAudioJoinType': unknown override specifier`
- `Error: use of undefined type 'YUVRawDataI420'`

**Checklist**:
- [ ] `#include <windows.h>` is the FIRST include in every file
- [ ] `#include <cstdint>` is right after `<windows.h>` in every file
- [ ] `meeting_audio_interface.h` is included BEFORE `meeting_participants_ctrl_interface.h`
- [ ] `zoom_sdk_raw_data_def.h` is included when using raw video data

**Fix**: See [Build Errors Guide](build-errors.md) for detailed solutions.

---

### ✅ "Cannot Instantiate Abstract Class" Error

**Symptoms**:
- `Error C2259: 'AuthServiceEventListener': cannot instantiate abstract class`
- `note: due to following members: 'void IAuthServiceEvent::onNotificationServiceStatus(...)': is abstract`

**Checklist**:
- [ ] Implemented ALL pure virtual methods from `IAuthServiceEvent` (6 methods)
- [ ] Implemented ALL pure virtual methods from `IMeetingServiceEvent` (9 methods)
- [ ] Included WIN32-conditional methods (even though they're in `#if defined(WIN32)`)
- [ ] Used `override` keyword to catch signature mismatches
- [ ] Verified method signatures match SDK headers exactly

**Fix**: See [Interface Methods Guide](../references/interface-methods.md) for complete method lists.

---

### ✅ Linker Errors

**Symptoms**:
- `LNK2019: unresolved external symbol`
- `Error: Cannot open file 'sdk.lib'`

**Checklist**:
- [ ] Added SDK library directory to Project Properties → Linker → General → Additional Library Directories
  - `$(SolutionDir)SDK\x64\lib`
- [ ] Added `sdk.lib` to Project Properties → Linker → Input → Additional Dependencies
- [ ] Verified SDK architecture matches project architecture (both x64)
- [ ] SDK DLL (`sdk.dll`) is in the same directory as the executable or in PATH

**Fix**:
1. Right-click project → Properties
2. Configuration: All Configurations, Platform: x64
3. Linker → General → Additional Library Directories: Add `$(SolutionDir)SDK\x64\lib`
4. Linker → Input → Additional Dependencies: Add `sdk.lib`
5. Copy `SDK\x64\bin\sdk.dll` to your output directory

---

## Runtime Issues

### ✅ Authentication Timeout (CRITICAL!)

**Symptoms**:
- "Still waiting..." messages keep printing
- "ERROR: Authentication timeout after 30 seconds"
- `onAuthenticationReturn()` callback NEVER fires

**Root Cause**: 99% of the time, this is a **missing Windows message loop**, NOT a JWT token issue!

**Checklist**:
- [ ] Added `PeekMessage()` loop during authentication wait
- [ ] Added `PeekMessage()` loop in main event loop
- [ ] Using `PM_REMOVE` flag with `PeekMessage()`
- [ ] Calling `TranslateMessage()` and `DispatchMessage()` for each message

**Fix**: See [Windows Message Loop Guide](windows-message-loop.md) for complete solution.

**Quick test**: Add this minimal message loop:
```cpp
while (!g_authenticated) {
    MSG msg;
    while (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}
```

If `onAuthenticationReturn()` suddenly fires, you confirmed the issue was the message loop.

---

### ✅ Authentication Fails with Error Code

**Symptoms**:
- `onAuthenticationReturn()` fires but with non-success code
- "Authentication failed: [error code]"

**Authentication Error Codes**:

| Code | Enum Value | Meaning | Solution |
|------|------------|---------|----------|
| 0 | `AUTHRET_SUCCESS` | ✅ Success | N/A |
| 1 | `AUTHRET_KEYORSECRETEMPTY` | JWT token or app secret is empty | Verify JWT token string is not empty |
| 2 | `AUTHRET_JWTTOKENWRONG` | Invalid JWT token format or signature | Regenerate JWT token, verify app credentials |
| 3 | `AUTHRET_OVERTIME` | JWT token expired | Regenerate JWT with fresh timestamp |
| 4 | `AUTHRET_NETWORKISSUE` | Network connection problem | Check firewall, proxy settings, internet connection |
| 16 | `AUTHRET_CLIENT_INCOMPATIBLE` | SDK version incompatible with Zoom service | Update SDK to latest version |

**Checklist**:
- [ ] JWT token is correctly formatted (3 parts separated by dots)
- [ ] JWT token was generated within the last hour
- [ ] App credentials (SDK Key/Secret) match JWT token generation
- [ ] System clock is accurate (JWT validation is time-sensitive)
- [ ] Not behind a firewall blocking Zoom domains (*.zoom.us, *.zoomgov.com)

**How to regenerate JWT token**:
```javascript
// Node.js example
const jwt = require('jsonwebtoken');
const token = jwt.sign(
  { 
    appKey: 'YOUR_SDK_KEY',
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor(Date.now() / 1000) + 7200,  // 2 hours
    tokenExp: Math.floor(Date.now() / 1000) + 7200
  },
  'YOUR_SDK_SECRET'
);
```

---

### ✅ Meeting Join Fails

**Symptoms**:
- `onMeetingStatusChanged()` fires with `MEETING_STATUS_FAILED`
- "Join meeting failed: [error code]"

**Meeting Error Codes**:

| Code | Enum Value | Meaning | Solution |
|------|------------|---------|----------|
| 0 | `MEETING_SUCCESS` | ✅ Success | N/A |
| 1 | `MEETING_FAIL_NETWORK_ERR` | Network error | Check internet connection |
| 2 | `MEETING_FAIL_RECONNECT_ERR` | Reconnection failed | Retry joining |
| 3 | `MEETING_FAIL_MMR_ERR` | Multi-media router error | Contact Zoom support |
| 4 | `MEETING_FAIL_PASSWORD_ERR` | Wrong meeting password | Verify password |
| 5 | `MEETING_FAIL_SESSION_ERR` | Invalid meeting session | Verify meeting number |
| 6 | `MEETING_FAIL_MEETING_OVER` | Meeting has ended | Join a different meeting |
| 7 | `MEETING_FAIL_MEETING_NOT_START` | Meeting hasn't started | Wait for host to start |
| 8 | `MEETING_FAIL_MEETING_NOT_EXIST` | Invalid meeting number | Verify meeting number |
| 9 | `MEETING_FAIL_MEETING_USER_FULL` | Meeting at capacity | Wait for slot or use livestream |
| 10 | `MEETING_FAIL_CLIENT_INCOMPATIBLE` | SDK version incompatible | Update SDK |

**Checklist**:
- [ ] Meeting number is correct (10-11 digits)
- [ ] Meeting password is correct (if required)
- [ ] Authenticated successfully before joining
- [ ] Meeting is currently active (host has started it)
- [ ] Meeting hasn't reached capacity
- [ ] Using `SDK_UT_WITHOUT_LOGIN` user type for JWT auth

**Fix for common issues**:
```cpp
// Correct join pattern
JoinParam joinParam;
joinParam.userType = SDK_UT_WITHOUT_LOGIN;  // REQUIRED for JWT auth

JoinParam4WithoutLogin withoutLoginParam;
withoutLoginParam.meetingNumber = 1234567890;  // Your meeting number
withoutLoginParam.userName = L"Bot User";
withoutLoginParam.psw = L"meeting_password";  // Empty if no password
withoutLoginParam.vanityID = nullptr;
withoutLoginParam.customer_key = nullptr;
withoutLoginParam.webinarToken = nullptr;
withoutLoginParam.isVideoOff = false;
withoutLoginParam.isAudioOff = false;

joinParam.param.withoutloginuserJoin = withoutLoginParam;
meetingService->Join(joinParam);
```

---

### ✅ Callbacks Not Firing

**Symptoms**:
- `SetEvent()` called but callbacks never execute
- Authentication/meeting status changes but no output

**Checklist**:
- [ ] Windows message loop is running (see Authentication Timeout above)
- [ ] Event listener pointer is valid (not deleted prematurely)
- [ ] Event listener is set BEFORE calling SDK methods
- [ ] Using `new` to allocate listener (SDK manages lifecycle)

**Fix**:
```cpp
// CORRECT: Set listener before SDK actions
AuthServiceEventListener* authListener = new AuthServiceEventListener(&OnAuthComplete);
authService->SetEvent(authListener);
authService->SDKAuth(authContext);  // Now callbacks will work

// WRONG: Set listener after
authService->SDKAuth(authContext);
authService->SetEvent(authListener);  // Too late!
```

---

## Video Capture Issues

### ✅ Raw Video Data Not Received

**Symptoms**:
- `onRawDataFrameReceived()` never fires
- `onRawDataStatusChanged()` fires but no frames

**Checklist**:
- [ ] Called `StartRawRecording()` after joining meeting
- [ ] Subscribed to video streams using `Subscribe(userId, Raw_Video_On)`
- [ ] Implemented `IZoomSDKRendererDelegate` interface correctly
- [ ] Created raw data helper: `CreateRawdataRenderer()`
- [ ] Set renderer delegate: `setRawDataResolution(...)` and `subscribe(...)`

**Fix**: See [Raw Video Capture Guide](../examples/raw-video-capture.md) for complete workflow.

**Quick test**:
```cpp
// After successfully joining meeting
IMeetingRecordingController* recordingCtrl = meetingService->GetMeetingRecordingController();
recordingCtrl->StartRawRecording();

IZoomSDKVideoSource* videoSource = rawDataHelper->GetRawdataVideoSourceHelper();
videoSource->subscribe(userId, Raw_Video_On);
```

---

### ✅ Video Data Format Issues

**Symptoms**:
- Receiving frames but video looks corrupted
- Wrong frame size or color

**Checklist**:
- [ ] Using YUV420 (I420) format, not RGB
- [ ] Buffer size is `width * height * 1.5` bytes (not `width * height * 3`)
- [ ] Y plane: `width * height` bytes
- [ ] U plane: `(width/2) * (height/2)` bytes  
- [ ] V plane: `(width/2) * (height/2)` bytes
- [ ] Rotation is handled correctly (0°, 90°, 180°, 270°)

**YUV420 Layout**:
```
Width: 1920, Height: 1080
Total bytes: 1920 * 1080 * 1.5 = 3,110,400 bytes

Y plane: [0 to 2,073,599]       (1920 * 1080 bytes)
U plane: [2,073,600 to 2,592,639]  (960 * 540 bytes)
V plane: [2,592,640 to 3,110,399]  (960 * 540 bytes)
```

---

## Network & Firewall Issues

### ✅ SDK Network Requirements

**Symptoms**:
- `AUTHRET_NETWORKISSUE` error code
- `MEETING_FAIL_NETWORK_ERR` error code
- Timeouts during initialization

**Required Firewall Rules**:
- [ ] Allow outbound HTTPS (port 443) to `*.zoom.us`
- [ ] Allow outbound HTTPS (port 443) to `*.zoomgov.com` (for government)
- [ ] Allow UDP ports 8801-8810 for media
- [ ] Not behind a proxy requiring authentication (or proxy configured)

**How to test connectivity**:
```bash
# Test DNS resolution
ping zoom.us
ping us01web.zoom.us

# Test HTTPS connectivity
curl https://zoom.us
curl https://us01web.zoom.us
```

**Proxy configuration** (if required):
```cpp
InitParam initParam;
initParam.strWebDomain = L"https://zoom.us";
// Add proxy settings if needed
// initParam.proxy = ...; 
```

---

## General Debugging Tips

### Enable SDK Logging

```cpp
InitParam initParam;
initParam.enableLogByDefault = true;  // Enable logs
initParam.enableGenerateDump = true;   // Enable crash dumps
```

Logs location: `%APPDATA%\Zoom\logs\` or `C:\Users\[username]\AppData\Roaming\Zoom\logs\`

### Add Debug Output to Callbacks

```cpp
void AuthServiceEventListener::onAuthenticationReturn(AuthResult ret) {
    std::cout << "[DEBUG] onAuthenticationReturn called! Code: " << ret << std::endl;
    // Your logic here
}
```

### Use Windows Debugger

Set breakpoints in callback methods to verify they're being called:
- `onAuthenticationReturn()`
- `onMeetingStatusChanged()`

If breakpoints never hit → Message loop issue
If breakpoints hit but code is wrong → Logic issue

### Verify SDK Version

Check `SDK/x64/version.txt` or `sdk.dll` properties → Details tab

Different versions have different:
- Required callback methods
- Error codes
- API behavior

This guide is for **SDK v6.7.2.26830**.

---

## "If You See X, Do Y" Quick Reference

| You See | Do This |
|---------|---------|
| `uint32_t` error | Add `#include <cstdint>` after `<windows.h>` |
| `AudioType` error | Include `meeting_audio_interface.h` before `meeting_participants_ctrl_interface.h` |
| `YUVRawDataI420` error | Include `zoom_sdk_raw_data_def.h` |
| Abstract class error | Implement ALL virtual methods (see [Interface Methods Guide](../references/interface-methods.md)) |
| Authentication timeout | Add Windows message loop (see [Message Loop Guide](windows-message-loop.md)) |
| `AUTHRET_JWTTOKENWRONG` | Regenerate JWT token with correct app credentials |
| `AUTHRET_OVERTIME` | JWT token expired, generate a fresh one |
| `MEETING_FAIL_PASSWORD_ERR` | Wrong meeting password or no password provided |
| `MEETING_FAIL_MEETING_NOT_EXIST` | Invalid meeting number, verify 10-11 digits |
| Callbacks not firing | Add Windows message loop, verify `SetEvent()` called first |
| No video frames | Call `StartRawRecording()` and `Subscribe()` after joining |

---

## Still Having Issues?

1. **Check SDK logs**: `%APPDATA%\Zoom\logs\`
2. **Enable debug output**: Add `std::cout` to all callbacks
3. **Verify SDK version**: Different versions have different requirements
4. **Review working example**: See complete working code in [Authentication Pattern](../examples/authentication-pattern.md)
5. **Check Zoom Developer Forums**: https://devforum.zoom.us/

---

## Related Documentation

- [Windows Message Loop](windows-message-loop.md) - Why callbacks don't fire
- [Build Errors Guide](build-errors.md) - Header dependency issues
- [Interface Methods Guide](../references/interface-methods.md) - Required virtual methods
- [Authentication Pattern](../examples/authentication-pattern.md) - Complete working auth code

---

**Last Updated**: Based on Zoom Windows Meeting SDK v6.7.2.26830

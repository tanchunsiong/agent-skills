# Authentication Flow Pattern

Complete guide to authenticating with the Zoom Windows SDK using JWT tokens.

---

## Overview

Authentication is the first required step before joining meetings. The SDK uses JWT (JSON Web Token) authentication for Meeting SDK apps.

### Flow Sequence

```
1. Initialize SDK (InitSDK)
2. Create Auth Service (CreateAuthService)
3. Set Event Listener (SetEvent)
4. Call SDKAuth with JWT token
5. Process Windows messages (CRITICAL!)
6. Wait for onAuthenticationReturn callback
7. Proceed to join meeting
```

---

## Complete Working Example

```cpp
#include <windows.h>
#include <cstdint>
#include <zoom_sdk.h>
#include <auth_service_interface.h>
#include <iostream>
#include <chrono>
#include <thread>

using namespace ZOOM_SDK_NAMESPACE;

// Global state
bool g_authenticated = false;
bool g_exit = false;
IAuthService* g_authService = nullptr;

// Step 1: Create Event Listener
class MyAuthListener : public IAuthServiceEvent {
public:
    void onAuthenticationReturn(AuthResult ret) override {
        std::cout << "[AUTH] Callback received! Result: " << ret << std::endl;
        
        switch (ret) {
        case AUTHRET_SUCCESS:
            std::cout << "[AUTH] Authentication successful!" << std::endl;
            g_authenticated = true;
            break;
        case AUTHRET_KEYORSECRETEMPTY:
            std::cerr << "[AUTH] ERROR: SDK Key or Secret is empty" << std::endl;
            break;
        case AUTHRET_JWTTOKENWRONG:
            std::cerr << "[AUTH] ERROR: JWT token is invalid" << std::endl;
            break;
        case AUTHRET_OVERTIME:
            std::cerr << "[AUTH] ERROR: Authentication timeout" << std::endl;
            break;
        case AUTHRET_NETWORKISSUE:
            std::cerr << "[AUTH] ERROR: Network connection issue" << std::endl;
            break;
        default:
            std::cerr << "[AUTH] ERROR: Unknown error: " << ret << std::endl;
        }
    }
    
    void onLoginReturnWithReason(LOGINSTATUS ret, IAccountInfo* info, LoginFailReason reason) override {
        // Not used for JWT auth
    }
    
    void onLogout() override {
        std::cout << "[AUTH] Logged out" << std::endl;
    }
    
    void onZoomIdentityExpired() override {
        std::cout << "[AUTH] Zoom identity expired" << std::endl;
    }
    
    void onZoomAuthIdentityExpired() override {
        std::cout << "[AUTH] Zoom auth identity expired" << std::endl;
    }
    
    #if defined(WIN32)
    void onNotificationServiceStatus(SDKNotificationServiceStatus status, 
                                     SDKNotificationServiceError error) override {
        std::cout << "[AUTH] Notification service status: " << status << std::endl;
    }
    #endif
};

// Step 2: Initialize SDK
bool InitializeSDK() {
    std::cout << "[1/3] Initializing SDK..." << std::endl;
    
    InitParam initParam;
    initParam.strWebDomain = L"https://zoom.us";
    initParam.strSupportUrl = L"https://zoom.us";
    initParam.emLanguageID = LANGUAGE_English;
    initParam.enableLogByDefault = true;
    initParam.enableGenerateDump = true;
    
    SDKError err = InitSDK(initParam);
    if (err != SDKERR_SUCCESS) {
        std::cerr << "ERROR: InitSDK failed: " << err << std::endl;
        return false;
    }
    
    std::cout << "SDK initialized successfully" << std::endl;
    return true;
}

// Step 3: Authenticate
bool AuthenticateSDK(const std::wstring& jwt_token) {
    std::cout << "[2/3] Authenticating..." << std::endl;
    
    // Create auth service
    SDKError err = CreateAuthService(&g_authService);
    if (err != SDKERR_SUCCESS || !g_authService) {
        std::cerr << "ERROR: CreateAuthService failed: " << err << std::endl;
        return false;
    }
    std::cout << "Auth service created" << std::endl;
    
    // Set event listener
    err = g_authService->SetEvent(new MyAuthListener());
    if (err != SDKERR_SUCCESS) {
        std::cerr << "ERROR: SetEvent failed: " << err << std::endl;
        return false;
    }
    std::cout << "Event listener set" << std::endl;
    
    // Validate JWT token
    if (jwt_token.empty()) {
        std::cerr << "ERROR: JWT token is empty!" << std::endl;
        return false;
    }
    std::cout << "JWT token length: " << jwt_token.length() << " characters" << std::endl;
    
    // Create auth context
    AuthContext authContext;
    authContext.jwt_token = jwt_token.c_str();
    
    // Call SDKAuth
    err = g_authService->SDKAuth(authContext);
    if (err != SDKERR_SUCCESS) {
        std::cerr << "ERROR: SDKAuth failed: " << err << std::endl;
        return false;
    }
    
    std::cout << "SDKAuth called successfully, waiting for callback..." << std::endl;
    return true;
}

// Step 4: Wait for Authentication (WITH MESSAGE LOOP!)
bool WaitForAuthentication(int timeoutSeconds = 30) {
    std::cout << "[3/3] Waiting for authentication..." << std::endl;
    
    auto startTime = std::chrono::steady_clock::now();
    
    while (!g_authenticated && !g_exit) {
        // CRITICAL: Process Windows messages for SDK callbacks!
        MSG msg;
        while (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE)) {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }
        
        // Check timeout
        auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(
            std::chrono::steady_clock::now() - startTime).count();
        
        if (elapsed >= timeoutSeconds) {
            std::cerr << "ERROR: Authentication timeout after " << timeoutSeconds << " seconds" << std::endl;
            return false;
        }
        
        // Small sleep to avoid CPU spinning
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    
    return g_authenticated;
}

// Main function
int main() {
    // Your JWT token here
    std::wstring jwt_token = L"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...";
    
    // Step 1: Initialize SDK
    if (!InitializeSDK()) {
        return 1;
    }
    
    // Step 2: Authenticate
    if (!AuthenticateSDK(jwt_token)) {
        return 1;
    }
    
    // Step 3: Wait for callback
    if (!WaitForAuthentication()) {
        return 1;
    }
    
    std::cout << "\n✓ Authentication complete! Ready to join meeting." << std::endl;
    
    // Now you can join meetings...
    
    // Cleanup
    if (g_authService) {
        DestroyAuthService(g_authService);
    }
    CleanUPSDK();
    
    return 0;
}
```

---

## JWT Token Setup

### Generating JWT Token

1. **Go to Zoom Marketplace**: https://marketplace.zoom.us/
2. **Create/Select App**: Go to "Develop" → "Build App" → "Meeting SDK"
3. **Get Credentials**: Find "App Credentials" tab
   - SDK Key (Client ID)
   - SDK Secret (Client Secret)
4. **Generate JWT**: Use the built-in JWT generator or create manually

### JWT Token Format

Valid JWT token:
- **Length**: 200-500 characters
- **Starts with**: `eyJ`
- **Contains**: Two periods (`.`) separating three parts
- **Example**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBLZXk...`

### Loading from Configuration File

```cpp
#include <json/json.h>
#include <fstream>

bool LoadJWTFromConfig(std::wstring& jwt_token) {
    std::ifstream f("config.json");
    if (!f.is_open()) {
        std::cerr << "ERROR: config.json not found" << std::endl;
        return false;
    }
    
    Json::Value config;
    try {
        f >> config;
    } catch (const std::exception& e) {
        std::cerr << "ERROR: Failed to parse config.json: " << e.what() << std::endl;
        return false;
    }
    
    if (config["sdk_jwt"].empty()) {
        std::cerr << "ERROR: sdk_jwt not found in config.json" << std::endl;
        return false;
    }
    
    std::string jwt_str = config["sdk_jwt"].asString();
    jwt_token = std::wstring(jwt_str.begin(), jwt_str.end());
    
    return true;
}
```

**config.json**:
```json
{
  "sdk_jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "meeting_number": "1234567890",
  "passcode": "meeting_password"
}
```

---

## Common Authentication Errors

### AuthResult Error Codes

| Code | Enum | Meaning | Solution |
|------|------|---------|----------|
| 0 | `AUTHRET_SUCCESS` | ✓ Success | Continue to join meeting |
| 1 | `AUTHRET_KEYORSECRETEMPTY` | SDK Key/Secret empty | Check JWT token |
| 3 | `AUTHRET_JWTTOKENWRONG` | Invalid JWT | Regenerate token |
| 4 | `AUTHRET_OVERTIME` | Request timeout | Check network |
| 5 | `AUTHRET_NETWORKISSUE` | Network problem | Check firewall/internet |
| 7 | `AUTHRET_CLIENT_INCOMPATIBLE` | SDK version mismatch | Update SDK |
| 10 | `AUTHRET_JWTTOKENEXPIRED` | JWT expired | Generate fresh token |

### Timeout (No Callback)

**Symptom**: Waiting forever, no callback received

**Causes**:
1. **Missing Windows message loop** (most common!)
2. Network/firewall blocking
3. Invalid JWT format

**Debug**:
```cpp
void onAuthenticationReturn(AuthResult ret) override {
    std::cout << "CALLBACK FIRED! Result: " << ret << std::endl;  // Does this print?
}
```

If you never see "CALLBACK FIRED!", you're not processing Windows messages!

### Invalid JWT Token

**Symptom**: `AUTHRET_JWTTOKENWRONG` (code 3)

**Causes**:
1. Token expired (typically 24-48 hours)
2. Wrong SDK Key/Secret used to generate token
3. Token generated for different app
4. Malformed token

**Solution**:
- Generate fresh JWT token from Zoom Marketplace
- Verify SDK credentials match
- Check token format (starts with "eyJ", has two dots)

### Network Issues

**Symptom**: `AUTHRET_NETWORKISSUE` (code 5) or timeout

**Solutions**:
- Check internet connection
- Verify can access zoom.us from browser
- Check Windows Firewall settings
- If behind corporate proxy, may need proxy configuration
- Temporarily disable antivirus to test

---

## Best Practices

### 1. Validate JWT Before Using

```cpp
bool ValidateJWT(const std::wstring& jwt_token) {
    // Check length
    if (jwt_token.length() < 100) {
        std::cerr << "JWT token too short: " << jwt_token.length() << std::endl;
        return false;
    }
    
    // Check starts with "eyJ"
    if (jwt_token.substr(0, 3) != L"eyJ") {
        std::cerr << "JWT token doesn't start with 'eyJ'" << std::endl;
        return false;
    }
    
    // Check has two dots (three parts)
    int dotCount = 0;
    for (wchar_t c : jwt_token) {
        if (c == L'.') dotCount++;
    }
    if (dotCount != 2) {
        std::cerr << "JWT token should have 2 dots, found: " << dotCount << std::endl;
        return false;
    }
    
    return true;
}
```

### 2. Add Timeout with Progress Updates

```cpp
bool WaitForAuthenticationWithProgress(int timeoutSeconds = 30) {
    auto startTime = std::chrono::steady_clock::now();
    int lastProgressSeconds = 0;
    
    while (!g_authenticated && !g_exit) {
        // Process messages
        MSG msg;
        while (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE)) {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }
        
        // Show progress every 5 seconds
        auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(
            std::chrono::steady_clock::now() - startTime).count();
        
        if (elapsed > lastProgressSeconds && elapsed % 5 == 0) {
            std::cout << "Still waiting... (" << elapsed << "s)" << std::endl;
            lastProgressSeconds = elapsed;
        }
        
        if (elapsed >= timeoutSeconds) {
            return false;
        }
        
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    
    return g_authenticated;
}
```

### 3. Cleanup on Failure

```cpp
void Cleanup() {
    if (g_authService) {
        DestroyAuthService(g_authService);
        g_authService = nullptr;
    }
    CleanUPSDK();
}

int main() {
    if (!InitializeSDK()) {
        return 1;
    }
    
    if (!AuthenticateSDK(jwt_token)) {
        Cleanup();  // Always cleanup on failure
        return 1;
    }
    
    if (!WaitForAuthentication()) {
        Cleanup();
        return 1;
    }
    
    // ... use SDK ...
    
    Cleanup();  // Cleanup on success too
    return 0;
}
```

---

## Troubleshooting Steps

### Step 1: Check JWT Token

```cpp
std::cout << "JWT length: " << jwt_token.length() << std::endl;
std::cout << "JWT preview: " << jwt_token.substr(0, 30) << "..." << std::endl;
```

Expected output:
```
JWT length: 358
JWT preview: eyJhbGciOiJIUzI1NiIsInR5cCI...
```

### Step 2: Verify SDKAuth Return

```cpp
SDKError err = g_authService->SDKAuth(authContext);
std::cout << "SDKAuth returned: " << err << std::endl;
```

- `0` (SDKERR_SUCCESS): Good, wait for callback
- Non-zero: Immediate error, check JWT format

### Step 3: Confirm Callback Fires

Add logging in `onAuthenticationReturn`:
```cpp
void onAuthenticationReturn(AuthResult ret) override {
    std::cout << "*** CALLBACK RECEIVED ***" << std::endl;  // First line!
    // ... rest of code ...
}
```

If you never see "CALLBACK RECEIVED", you need a message loop!

### Step 4: Test Network

```cpp
// Before SDKAuth
std::cout << "Testing network..." << std::endl;
// Try to access zoom.us or check internet connection
```

---

## See Also

- [Windows Message Loop](../troubleshooting/windows-message-loop.md) - Why callbacks don't fire
- [Build Errors](../troubleshooting/build-errors.md) - Compilation issues
- [JWT Token Generation](../../zoom-oauth/SKILL.md) - Creating JWT tokens
- [Joining Meetings](joining-meeting.md) - Next steps after authentication

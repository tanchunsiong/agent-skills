---
name: zoom-apps-sdk
description: |
  Zoom Apps SDK for building apps that run inside the Zoom client. JavaScript SDK for 
  in-meeting experiences and Layers API for immersive apps. Use when you want your app 
  to appear within Zoom meetings or the Zoom client.
---

# Zoom Apps SDK

Build apps that run inside the Zoom client.

## Prerequisites

- Zoom app configured as "Zoom App" type in Marketplace
- OAuth credentials with Zoom Apps scopes
- Web application to serve your Zoom App
- **Your hosted URL whitelisted in Marketplace** (see below)

## Quick Start

```html
<script src="https://appssdk.zoom.us/sdk.js"></script>

<script>
// IMPORTANT: Do NOT declare "let zoomSdk" - the SDK defines window.zoomSdk globally
// Using "let zoomSdk = ..." causes: SyntaxError: redeclaration of non-configurable global property zoomSdk
let sdk = null;  // Use a different variable name

async function init() {
  try {
    sdk = window.zoomSdk;
    
    const configResponse = await sdk.config({
      capabilities: ['shareApp', 'getMeetingContext', 'getUserContext'],
      version: '0.16'
    });
    
    console.log('Running context:', configResponse.runningContext);
    
    const context = await sdk.getMeetingContext();
    console.log('Meeting ID:', context.meetingID);
    
  } catch (error) {
    // SDK only works inside Zoom client - show fallback UI
    console.error('Not running inside Zoom:', error.message);
    showDemoMode();
  }
}

function showDemoMode() {
  // Display preview UI with mock data when outside Zoom
  document.body.innerHTML = '<h1>Preview Mode</h1><p>Open this app inside Zoom client to use.</p>';
}

// Initialize with timeout fallback
document.addEventListener('DOMContentLoaded', () => {
  init();
  // Fallback if SDK hangs
  setTimeout(() => {
    if (!sdk) showDemoMode();
  }, 3000);
});
</script>
```

## Critical: Global Variable Conflict

The SDK script defines `window.zoomSdk` globally. **Do NOT redeclare it:**

```javascript
// WRONG - causes SyntaxError
let zoomSdk = null;
zoomSdk = window.zoomSdk;

// CORRECT - use different variable name
let sdk = null;
sdk = window.zoomSdk;
```

## Browser Preview / Demo Mode

The SDK only functions inside the Zoom client. When accessed in a regular browser:
- `window.zoomSdk` exists but `sdk.config()` throws an error
- Always implement try/catch with fallback UI
- Add timeout (3 seconds) in case SDK hangs

## URL Whitelisting (Required)

**Your app will NOT load in Zoom unless the URL is whitelisted.**

1. Go to [Zoom Marketplace](https://marketplace.zoom.us/)
2. Open your app > **Feature** tab
3. Under **Zoom App**, find **Add Allow List**
4. Add your domain (e.g., `https://www.aiweshipcode.com`)

Without this, the Zoom client will refuse to load your app's URL.

## OAuth Scopes (Required)

**Capabilities require matching OAuth scopes enabled in Marketplace.**

| Capability | Required Scope |
|------------|----------------|
| `getMeetingContext` | `zoomapp:inmeeting` |
| `getUserContext` | `zoomapp:inmeeting` |
| `shareApp` | `zoomapp:inmeeting` |
| `openUrl` | `zoomapp:inmeeting` |
| `sendAppInvitation` | `zoomapp:inmeeting` |
| `runRenderingContext` | `zoomapp:inmeeting` |

**To add scopes:**
1. Marketplace > Your App > **Scopes** tab
2. Add required scopes for your capabilities
3. Users must re-authorize if you add new scopes

Missing scopes = capability fails silently or throws error.

## Key Concepts

| Concept | Description |
|---------|-------------|
| Zoom App | Web app running in Zoom's embedded browser |
| Capabilities | Permissions your app requests |
| Context | Meeting/user information |
| Layers API | Immersive visual experiences |

## Common APIs

| API | Description |
|-----|-------------|
| `config()` | Initialize SDK, request capabilities |
| `getMeetingContext()` | Get meeting info |
| `shareApp()` | Share app with participants |
| `openUrl()` | Open URL in browser |
| `runRenderingContext()` | Start Layers API |

## Detailed References

- **[references/apis.md](references/apis.md)** - Complete API reference
- **[references/events.md](references/events.md)** - SDK events
- **[references/layers-api.md](references/layers-api.md)** - Immersive experiences
- **[references/oauth.md](references/oauth.md)** - Zoom Apps OAuth flow
- **[references/zmail-sdk.md](references/zmail-sdk.md)** - ZMail integration for email

## Sample Repositories

### Official (by Zoom)

| Type | Repository | Stars |
|------|------------|-------|
| Hello World | [zoomapps-sample-js](https://github.com/zoom/zoomapps-sample-js) | 66 |
| Advanced React | [zoomapps-advancedsample-react](https://github.com/zoom/zoomapps-advancedsample-react) | 55 |
| SDK NPM | [appssdk](https://github.com/zoom/appssdk) | 49 |
| Collaborate Mode | [zoomapps-texteditor-vuejs](https://github.com/zoom/zoomapps-texteditor-vuejs) | 16 |
| Layers API | [zoomapps-customlayout-js](https://github.com/zoom/zoomapps-customlayout-js) | 16 |
| Serverless | [zoomapps-serverless-vuejs](https://github.com/zoom/zoomapps-serverless-vuejs) | 6 |
| Camera Mode | [zoomapps-cameramode-vuejs](https://github.com/zoom/zoomapps-cameramode-vuejs) | 6 |
| Workshop | [zoomapps-workshop-sample](https://github.com/zoom/zoomapps-workshop-sample) | 6 |
| RTMS Assistant | [arlo-meeting-assistant](https://github.com/zoom/arlo-meeting-assistant) | 2 |
| Recall.ai Bot | [meetingbot-recall-sample](https://github.com/zoom/meetingbot-recall-sample) | 2 |

### Community

| Type | Repository | Description |
|------|------------|-------------|
| Library | [harvard-edtech/zaccl](https://github.com/harvard-edtech/zaccl) | Zoom App Complete Connection Library |
| AI Demo | [inworld-ai/zoom-demeanor-evaluator-node](https://github.com/inworld-ai/zoom-demeanor-evaluator-node) | RTMS + Inworld AI |

**Full list**: See [zoom-general/references/community-repos.md](../zoom-general/references/community-repos.md)

## Resources

- **Official docs**: https://developers.zoom.us/docs/zoom-apps/
- **SDK reference**: https://appssdk.zoom.us/
- **Developer forum**: https://devforum.zoom.us/

---
name: zoom-apps-sdk
description: |
  Zoom Apps SDK for building web apps that run inside the Zoom client. JavaScript SDK (@zoom/appssdk)
  for in-meeting experiences, Layers API for immersive visuals, Collaborate Mode for shared state,
  and In-Client OAuth for seamless authorization. Use when building apps that appear within Zoom
  meetings, webinars, the main client, or Zoom Phone.
triggers:
  - "zoom app"
  - "in-meeting app"
  - "app inside zoom"
  - "zoom client app"
  - "layers api"
  - "immersive mode"
  - "camera mode"
  - "collaborate mode"
  - "appssdk"
  - "in-client oauth"
  - "zoom mail"
---

# Zoom Apps SDK

Build web apps that run inside the Zoom client - meetings, webinars, main client, and Zoom Phone.

**Official Documentation**: https://developers.zoom.us/docs/zoom-apps/
**SDK Reference**: https://appssdk.zoom.us/
**NPM Package**: https://www.npmjs.com/package/@zoom/appssdk

## Quick Links

**New to Zoom Apps? Follow this path:**

1. **[Architecture](concepts/architecture.md)** - Frontend/backend pattern, embedded browser, deep linking
2. **[Quick Start](examples/quick-start.md)** - Complete working Express + SDK app
3. **[Running Contexts](concepts/running-contexts.md)** - Where your app runs (inMeeting, inMainClient, etc.)
4. **[In-Client OAuth](examples/in-client-oauth.md)** - Seamless authorization with PKCE
5. **[API Reference](references/apis.md)** - 100+ SDK methods
6. **[INDEX.md](INDEX.md)** - Complete documentation navigation

**Reference:**
- **[API Reference](references/apis.md)** - All SDK methods by category
- **[Events Reference](references/events.md)** - All SDK event listeners
- **[Layers API](references/layers-api.md)** - Immersive and camera mode rendering
- **[OAuth Reference](references/oauth.md)** - OAuth flows for Zoom Apps
- **[Zoom Mail](references/zmail-sdk.md)** - Mail plugin integration

**Having issues?**
- App won't load in Zoom → Check [Domain Allowlist](#url-whitelisting-required) below
- SDK errors → [Common Issues](troubleshooting/common-issues.md)
- Local dev setup → [Debugging Guide](troubleshooting/debugging.md)
- Version upgrade → [Migration Guide](troubleshooting/migration.md)

**Building immersive experiences?**
- [Layers Immersive Mode](examples/layers-immersive.md) - Custom video layouts
- [Camera Mode](examples/layers-camera.md) - Virtual camera overlays

> **Need help with OAuth?** See the **[zoom-oauth](../zoom-oauth/SKILL.md)** skill for authentication flows.

## SDK Overview

The Zoom Apps SDK (`@zoom/appssdk`) provides JavaScript APIs for web apps running in Zoom's embedded browser:

- **Context APIs** - Get meeting, user, and participant info
- **Meeting Actions** - Share app, invite participants, open URLs
- **Authorization** - In-Client OAuth with PKCE (no browser redirect)
- **Layers API** - Immersive video layouts and camera mode overlays
- **Collaborate Mode** - Shared app state across participants
- **App Communication** - Message passing between app instances (main client <-> meeting)
- **Media Controls** - Virtual backgrounds, camera listing, recording control
- **UI Controls** - Expand app, notifications, popout
- **Events** - React to meeting state, participants, sharing, and more

## Prerequisites

- Zoom app configured as **"Zoom App"** type in [Marketplace](https://marketplace.zoom.us/)
- OAuth credentials (Client ID + Secret) with Zoom Apps scopes
- Web application (Node.js + Express recommended)
- **Your domain whitelisted** in Marketplace domain allowlist
- ngrok or HTTPS tunnel for local development
- Node.js 18+ (for the backend server)

## Quick Start

### Option A: NPM (Recommended for frameworks)

```bash
npm install @zoom/appssdk
```

```javascript
import zoomSdk from '@zoom/appssdk';

async function init() {
  try {
    const configResponse = await zoomSdk.config({
      capabilities: [
        'shareApp',
        'getMeetingContext',
        'getUserContext',
        'openUrl'
      ],
      version: '0.16'
    });

    console.log('Running context:', configResponse.runningContext);
    // 'inMeeting' | 'inMainClient' | 'inWebinar' | 'inImmersive' | ...

    const context = await zoomSdk.getMeetingContext();
    console.log('Meeting ID:', context.meetingID);
  } catch (error) {
    console.error('Not running inside Zoom:', error.message);
    showDemoMode();
  }
}
```

### Option B: CDN (Vanilla JS)

```html
<script src="https://appssdk.zoom.us/sdk.js"></script>

<script>
// CRITICAL: Do NOT declare "let zoomSdk" - the SDK defines window.zoomSdk globally
// Using "let zoomSdk = ..." causes: SyntaxError: redeclaration of non-configurable global property
let sdk = window.zoomSdk;  // Use a different variable name

async function init() {
  try {
    const configResponse = await sdk.config({
      capabilities: ['shareApp', 'getMeetingContext', 'getUserContext'],
      version: '0.16'
    });

    console.log('Running context:', configResponse.runningContext);
  } catch (error) {
    console.error('Not running inside Zoom:', error.message);
    showDemoMode();
  }
}

function showDemoMode() {
  document.body.innerHTML = '<h1>Preview Mode</h1><p>Open this app inside Zoom to use.</p>';
}

document.addEventListener('DOMContentLoaded', () => {
  init();
  setTimeout(() => { if (!sdk) showDemoMode(); }, 3000);
});
</script>
```

## Critical: Global Variable Conflict

The CDN script defines `window.zoomSdk` globally. **Do NOT redeclare it:**

```javascript
// WRONG - causes SyntaxError in Zoom's embedded browser
let zoomSdk = null;
zoomSdk = window.zoomSdk;

// CORRECT - use different variable name
let sdk = window.zoomSdk;

// ALSO CORRECT - NPM import (no conflict)
import zoomSdk from '@zoom/appssdk';
```

This only applies to the CDN approach. The NPM import creates a module-scoped variable, no conflict.

## Browser Preview / Demo Mode

The SDK only functions inside the Zoom client. When accessed in a regular browser:
- `window.zoomSdk` exists but `sdk.config()` throws an error
- Always implement try/catch with fallback UI
- Add timeout (3 seconds) in case SDK hangs

## URL Whitelisting (Required)

**Your app will NOT load in Zoom unless the domain is whitelisted.**

1. Go to [Zoom Marketplace](https://marketplace.zoom.us/)
2. Open your app -> **Feature** tab
3. Under **Zoom App**, find **Add Allow List**
4. Add your domain (e.g., `yourdomain.com` for production, `xxxxx.ngrok.io` for dev)

Without this, the Zoom client shows a blank panel with no error message.

## OAuth Scopes (Required)

Capabilities require matching OAuth scopes enabled in Marketplace:

| Capability | Required Scope |
|------------|----------------|
| `getMeetingContext` | `zoomapp:inmeeting` |
| `getUserContext` | `zoomapp:inmeeting` |
| `shareApp` | `zoomapp:inmeeting` |
| `openUrl` | `zoomapp:inmeeting` |
| `sendAppInvitation` | `zoomapp:inmeeting` |
| `runRenderingContext` | `zoomapp:inmeeting` |
| `authorize` | `zoomapp:inmeeting` |
| `getMeetingParticipants` | `zoomapp:inmeeting` |

**To add scopes:** Marketplace -> Your App -> **Scopes** tab -> Add required scopes.

Missing scopes = capability fails silently or throws error. Users must re-authorize if you add new scopes.

## Running Contexts

Your app runs in different surfaces within Zoom. The `configResponse.runningContext` tells you where:

| Context | Surface | Description |
|---------|---------|-------------|
| `inMeeting` | Meeting sidebar | Most common. Full meeting APIs available |
| `inMainClient` | Main client panel | Home tab. No meeting context APIs |
| `inWebinar` | Webinar sidebar | Host/panelist. Meeting + webinar APIs |
| `inImmersive` | Layers API | Full-screen custom rendering |
| `inCamera` | Camera mode | Virtual camera overlay |
| `inCollaborate` | Collaborate mode | Shared state context |
| `inPhone` | Zoom Phone | Phone call app |
| `inChat` | Team Chat | Chat sidebar |

See **[Running Contexts](concepts/running-contexts.md)** for context-specific behavior and APIs.

## SDK Initialization Pattern

Every Zoom App starts with `config()`:

```javascript
import zoomSdk from '@zoom/appssdk';

const configResponse = await zoomSdk.config({
  capabilities: [
    // List ALL APIs you will use
    'getMeetingContext',
    'getUserContext',
    'shareApp',
    'openUrl',
    'authorize',
    'onAuthorized'
  ],
  version: '0.16'
});

// configResponse contains:
// {
//   runningContext: 'inMeeting',
//   clientVersion: '5.x.x',
//   unsupportedApis: []  // APIs not supported in this client version
// }
```

**Rules:**
1. `config()` MUST be called before any other SDK method
2. Only capabilities listed in `config()` are available
3. Capabilities must match OAuth scopes in Marketplace
4. Check `unsupportedApis` for graceful degradation

## In-Client OAuth (Summary)

Best UX for authorization - no browser redirect:

```javascript
// 1. Get code challenge from your backend
const { codeChallenge, state } = await fetch('/api/auth/challenge').then(r => r.json());

// 2. Trigger in-client authorization
await zoomSdk.authorize({ codeChallenge, state });

// 3. Listen for authorization result
zoomSdk.addEventListener('onAuthorized', async (event) => {
  const { code, state } = event;
  // 4. Send code to backend for token exchange
  await fetch('/api/auth/token', {
    method: 'POST',
    body: JSON.stringify({ code, state })
  });
});
```

See **[In-Client OAuth Guide](examples/in-client-oauth.md)** for complete implementation.

## Layers API (Summary)

Build immersive video layouts and camera overlays:

```javascript
// Start immersive mode - replaces gallery view
await zoomSdk.runRenderingContext({ view: 'immersive' });

// Position participant video feeds
await zoomSdk.drawParticipant({
  participantUUID: 'user-uuid',
  x: 0, y: 0, width: 640, height: 480, zIndex: 1
});

// Add overlay images
await zoomSdk.drawImage({
  imageData: canvas.toDataURL(),
  x: 0, y: 0, width: 1280, height: 720, zIndex: 0
});

// Exit immersive mode
await zoomSdk.closeRenderingContext();
```

See **[Layers Immersive](examples/layers-immersive.md)** and **[Camera Mode](examples/layers-camera.md)**.

## Environment Variables

| Variable | Description | Where to Find |
|----------|-------------|---------------|
| `ZOOM_APP_CLIENT_ID` | App client ID | Marketplace -> App -> App Credentials |
| `ZOOM_APP_CLIENT_SECRET` | App client secret | Marketplace -> App -> App Credentials |
| `ZOOM_APP_REDIRECT_URI` | OAuth redirect URL | Your server URL + `/auth` |
| `SESSION_SECRET` | Cookie signing secret | Generate random string |
| `ZOOM_HOST` | Zoom host URL | `https://zoom.us` (or `https://zoomgov.com`) |

## Common APIs

| API | Description |
|-----|-------------|
| `config()` | Initialize SDK, request capabilities |
| `getMeetingContext()` | Get meeting ID, topic, status |
| `getUserContext()` | Get user name, role, participant ID |
| `getRunningContext()` | Get current running context |
| `getMeetingParticipants()` | List participants |
| `shareApp()` | Share app screen with participants |
| `openUrl({ url })` | Open URL in external browser |
| `sendAppInvitation()` | Invite users to open your app |
| `authorize()` | Trigger In-Client OAuth |
| `connect()` | Connect to other app instances |
| `postMessage()` | Send message to connected instances |
| `runRenderingContext()` | Start Layers API (immersive/camera) |
| `expandApp({ action })` | Expand/collapse app panel |
| `showNotification()` | Show notification in Zoom |

## Complete Documentation Library

### Core Concepts
- **[Architecture](concepts/architecture.md)** - Frontend/backend pattern, embedded browser, deep linking, X-Zoom-App-Context
- **[Running Contexts](concepts/running-contexts.md)** - All contexts, context-specific APIs, multi-instance communication
- **[Security](concepts/security.md)** - OWASP headers, CSP, cookie security, PKCE, token storage

### Complete Examples
- **[Quick Start](examples/quick-start.md)** - Hello World Express + SDK app
- **[In-Client OAuth](examples/in-client-oauth.md)** - PKCE authorization flow
- **[Layers Immersive](examples/layers-immersive.md)** - Custom video layouts
- **[Camera Mode](examples/layers-camera.md)** - Virtual camera overlays
- **[Collaborate Mode](examples/collaborate-mode.md)** - Shared state across participants
- **[Guest Mode](examples/guest-mode.md)** - Unauthenticated/authenticated/authorized states
- **[Breakout Rooms](examples/breakout-rooms.md)** - Room detection and cross-room state
- **[App Communication](examples/app-communication.md)** - connect + postMessage between instances

### Troubleshooting
- **[Common Issues](troubleshooting/common-issues.md)** - Quick diagnostics and error codes
- **[Debugging](troubleshooting/debugging.md)** - Local dev, ngrok, browser preview
- **[Migration](troubleshooting/migration.md)** - SDK version upgrade notes

### References
- **[API Reference](references/apis.md)** - All 100+ SDK methods
- **[Events Reference](references/events.md)** - All SDK event listeners
- **[Layers API Reference](references/layers-api.md)** - Drawing and rendering methods
- **[OAuth Reference](references/oauth.md)** - OAuth flows for Zoom Apps
- **[Zoom Mail](references/zmail-sdk.md)** - Mail plugin integration

## Sample Repositories

### Official (by Zoom)

| Repository | Type | Last Updated | Status | SDK Version |
|-----------|------|-------------|--------|-------------|
| [zoomapps-sample-js](https://github.com/zoom/zoomapps-sample-js) | Hello World (Vanilla JS) | Dec 2025 | Active | ^0.16.26 |
| [zoomapps-advancedsample-react](https://github.com/zoom/zoomapps-advancedsample-react) | Advanced (React + Redis) | Oct 2025 | Active | 0.16.0 |
| [zoomapps-customlayout-js](https://github.com/zoom/zoomapps-customlayout-js) | Layers API | Nov 2023 | Stale | ^0.16.8 |
| [zoomapps-texteditor-vuejs](https://github.com/zoom/zoomapps-texteditor-vuejs) | Collaborate (Vue + Y.js) | Oct 2023 | Stale | ^0.16.7 |
| [zoomapps-serverless-vuejs](https://github.com/zoom/zoomapps-serverless-vuejs) | Serverless (Firebase) | Aug 2024 | Stale | ^0.16.21 |
| [zoomapps-cameramode-vuejs](https://github.com/zoom/zoomapps-cameramode-vuejs) | Camera Mode | - | - | - |
| [zoomapps-workshop-sample](https://github.com/zoom/zoomapps-workshop-sample) | Workshop | - | - | - |

**Recommended for new projects:** Use `@zoom/appssdk` version `^0.16.26`.

### Community

| Type | Repository | Description |
|------|------------|-------------|
| Library | [harvard-edtech/zaccl](https://github.com/harvard-edtech/zaccl) | Zoom App Complete Connection Library |

**Full list**: See [zoom-general/references/community-repos.md](../zoom-general/references/community-repos.md)

### Learning Path

1. **Start**: `zoomapps-sample-js` - Simplest, most up-to-date
2. **Advanced**: `zoomapps-advancedsample-react` - Comprehensive (In-Client OAuth, Guest Mode, Collaborate)
3. **Specialized**: Pick based on feature (Layers, Serverless, Camera Mode)

## Critical Gotchas (From Real Development)

### 1. Global Variable Conflict
The CDN script defines `window.zoomSdk`. Declaring `let zoomSdk` in your code causes `SyntaxError: redeclaration of non-configurable global property`. Use `let sdk = window.zoomSdk` or the NPM import.

### 2. Domain Allowlist
Your app URL **must** be in the Marketplace domain allowlist. Without it, Zoom shows a blank panel with no error. Also add `appssdk.zoom.us` and any CDN domains you use.

### 3. Capabilities Must Be Listed
Only APIs listed in `config({ capabilities: [...] })` are available. Calling an unlisted API throws an error. This is also true for event listeners.

### 4. SDK Only Works Inside Zoom
`zoomSdk.config()` throws outside the Zoom client. Always wrap in try/catch with browser fallback:
```javascript
try { await zoomSdk.config({...}); } catch { showBrowserPreview(); }
```

### 5. ngrok URL Changes
Free ngrok URLs change on restart. You must update 4 places in Marketplace: Home URL, Redirect URL, OAuth Allow List, Domain Allow List. Consider ngrok paid plan for stable subdomain.

### 6. In-Client OAuth vs Web OAuth
Use `zoomSdk.authorize()` (In-Client) for best UX - no browser redirect. Only fall back to web redirect for initial install from Marketplace.

### 7. Camera Mode CEF Race Condition
Camera mode uses CEF which takes time to initialize. `drawImage`/`drawWebView` may fail if called too early. Implement retry with exponential backoff.

### 8. Cookie Configuration
Zoom's embedded browser requires cookies with `SameSite=None` and `Secure=true`. Without this, sessions break silently.

### 9. State Validation
Always validate the OAuth `state` parameter to prevent CSRF attacks. Generate cryptographically random state, store it, and verify on callback.

## Resources

- **Official docs**: https://developers.zoom.us/docs/zoom-apps/
- **SDK reference**: https://appssdk.zoom.us/
- **NPM package**: https://www.npmjs.com/package/@zoom/appssdk
- **Developer forum**: https://devforum.zoom.us/
- **GitHub SDK source**: https://github.com/zoom/appssdk

---

**Need help?** Start with [INDEX.md](INDEX.md) for complete navigation.

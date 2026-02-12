# Zoom Apps SDK - Complete Documentation Index

## Quick Start Path

**If you're new to Zoom Apps, follow this order:**

1. **Read the architecture** -> [concepts/architecture.md](concepts/architecture.md)
   - Frontend/backend pattern, embedded browser, deep linking
   - Understand how Zoom loads and communicates with your app

2. **Build your first app** -> [examples/quick-start.md](examples/quick-start.md)
   - Complete Express + SDK Hello World
   - ngrok setup for local development

3. **Understand running contexts** -> [concepts/running-contexts.md](concepts/running-contexts.md)
   - Where your app runs (inMeeting, inMainClient, inWebinar, etc.)
   - Context-specific APIs and limitations

4. **Implement OAuth** -> [examples/in-client-oauth.md](examples/in-client-oauth.md)
   - In-Client OAuth with PKCE (best UX)
   - Token exchange and storage

5. **Add features** -> [references/apis.md](references/apis.md)
   - 100+ SDK methods organized by category
   - Code examples for each

6. **Troubleshoot** -> [troubleshooting/common-issues.md](troubleshooting/common-issues.md)
   - Quick diagnostics for common problems

---

## Documentation Structure

```
zoom-apps-sdk/
├── SKILL.md                           # Main skill overview
├── INDEX.md                           # This file - navigation guide
│
├── concepts/                          # Core architectural patterns
│   ├── architecture.md               # Frontend/backend, embedded browser, OAuth flow
│   ├── running-contexts.md           # Where your app runs + context-specific APIs
│   └── security.md                   # OWASP headers, CSP, data access layers
│
├── examples/                          # Complete working code
│   ├── quick-start.md                # Hello World - minimal Express + SDK app
│   ├── in-client-oauth.md            # In-Client OAuth with PKCE
│   ├── layers-immersive.md           # Layers API - immersive mode (custom layouts)
│   ├── layers-camera.md              # Layers API - camera mode (virtual camera)
│   ├── collaborate-mode.md           # Collaborate mode (shared state)
│   ├── guest-mode.md                 # Guest mode (unauthenticated -> authorized)
│   ├── breakout-rooms.md             # Breakout room integration
│   └── app-communication.md          # connect + postMessage between instances
│
├── troubleshooting/                   # Problem solving guides
│   ├── common-issues.md              # Quick diagnostics, error codes
│   ├── debugging.md                  # Local dev setup, ngrok, browser preview
│   └── migration.md                  # SDK version migration notes
│
└── references/                        # Reference documentation
    ├── apis.md                        # Complete API reference (100+ methods)
    ├── events.md                      # All SDK events
    ├── layers-api.md                  # Layers API detailed reference
    ├── oauth.md                       # OAuth flows for Zoom Apps
    └── zmail-sdk.md                   # Zoom Mail integration
```

---

## By Use Case

### I want to build a basic Zoom App
1. [Architecture](concepts/architecture.md) - Understand the pattern
2. [Quick Start](examples/quick-start.md) - Build Hello World
3. [In-Client OAuth](examples/in-client-oauth.md) - Add authorization
4. [Security](concepts/security.md) - Required headers

### I want immersive video layouts (Layers API)
1. [Layers Immersive](examples/layers-immersive.md) - Custom video positions
2. [Layers API Reference](references/layers-api.md) - All drawing methods
3. [App Communication](examples/app-communication.md) - Sync layout across participants

### I want a virtual camera overlay
1. [Camera Mode](examples/layers-camera.md) - Camera mode rendering
2. [Layers API Reference](references/layers-api.md) - Drawing methods

### I want real-time collaboration
1. [Collaborate Mode](examples/collaborate-mode.md) - Shared state APIs
2. [App Communication](examples/app-communication.md) - Instance messaging

### I want guest/anonymous access
1. [Guest Mode](examples/guest-mode.md) - Three authorization states
2. [In-Client OAuth](examples/in-client-oauth.md) - promptAuthorize flow

### I want breakout room support
1. [Breakout Rooms](examples/breakout-rooms.md) - Room detection and state sync

### I want to sync between main client and meeting
1. [App Communication](examples/app-communication.md) - connect + postMessage
2. [Running Contexts](concepts/running-contexts.md) - Multi-instance behavior

### I want serverless deployment
1. [Quick Start](examples/quick-start.md) - Understand the base pattern first
2. Sample: [zoomapps-serverless-vuejs](https://github.com/zoom/zoomapps-serverless-vuejs) - Firebase pattern

### I want to add Zoom Mail integration
1. [Zoom Mail Reference](references/zmail-sdk.md) - REST API + mail plugins

### I'm getting errors
1. [Common Issues](troubleshooting/common-issues.md) - Quick diagnostic table
2. [Debugging](troubleshooting/debugging.md) - Local dev setup, DevTools
3. [Migration](troubleshooting/migration.md) - Version compatibility

---

## Most Critical Documents

### 1. Architecture (FOUNDATION)
**[concepts/architecture.md](concepts/architecture.md)**

Understand how Zoom Apps work: Frontend in embedded browser, backend for OAuth/API, SDK as the bridge. Without this, nothing else makes sense.

### 2. Quick Start (FIRST APP)
**[examples/quick-start.md](examples/quick-start.md)**

Complete working code. Get something running before diving into advanced features.

### 3. Common Issues (MOST COMMON PROBLEMS)
**[troubleshooting/common-issues.md](troubleshooting/common-issues.md)**

90% of Zoom Apps issues are: domain allowlist, global variable conflict, or missing capabilities.

---

## Key Learnings

### Critical Discoveries:

1. **Global Variable Conflict is the #1 Gotcha**
   - CDN script defines `window.zoomSdk` globally
   - `let zoomSdk = ...` causes SyntaxError in Zoom's browser
   - Use `let sdk = window.zoomSdk` or NPM import

2. **Domain Allowlist is Non-Negotiable**
   - App shows blank panel with zero error if domain not whitelisted
   - Must include your domain AND `appssdk.zoom.us` AND any CDN domains
   - ngrok URLs change on restart - must update Marketplace each time

3. **config() Gates Everything**
   - Must be called first, must list all capabilities
   - Unlisted capabilities throw errors
   - Check `unsupportedApis` for client version compatibility

4. **In-Client OAuth > Web OAuth for UX**
   - `authorize()` keeps user in Zoom (no browser redirect)
   - Web redirect only needed for initial Marketplace install
   - Always implement PKCE (code_verifier + code_challenge)

5. **Two App Instances Can Run Simultaneously**
   - Main client instance + meeting instance
   - Use `connect()` + `postMessage()` to sync between them
   - Pre-meeting setup in main client, use in meeting

6. **Camera Mode Has CEF Quirks**
   - CEF initialization takes time
   - Draw calls may fail if too early
   - Use retry with exponential backoff

7. **Cookie Settings Matter**
   - `SameSite=None` + `Secure=true` required
   - Without this, sessions silently fail in embedded browser

---

## Quick Reference

### "App shows blank panel"
-> [Domain Allowlist](troubleshooting/common-issues.md) - add domain to Marketplace

### "SyntaxError: redeclaration"
-> [Global Variable](troubleshooting/common-issues.md) - use `let sdk = window.zoomSdk`

### "config() throws error"
-> [Browser Preview](troubleshooting/debugging.md) - SDK only works inside Zoom

### "API call fails silently"
-> [OAuth Scopes](troubleshooting/common-issues.md) - add required scopes in Marketplace

### "How do I implement [feature]?"
-> [API Reference](references/apis.md) - find the method, check capabilities needed

### "How do I test locally?"
-> [Debugging Guide](troubleshooting/debugging.md) - ngrok + Marketplace config

---

## Document Version

Based on **@zoom/appssdk v0.16.x** (latest: 0.16.26+)

---

**Happy coding!**

Start with [Architecture](concepts/architecture.md) to understand the pattern, then [Quick Start](examples/quick-start.md) to build your first app.

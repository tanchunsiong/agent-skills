---
name: zoom-ui-toolkit/web
description: "Zoom Video SDK UI Toolkit - Pre-built React-based video conferencing UI for web applications. Instant video sessions with minimal code - composite UI or individual components."
triggers:
  - "ui toolkit"
  - "zoom ui"
  - "prebuilt video ui"
  - "video conferencing ui"
  - "zoom video ui toolkit"
  - "uitoolkit"
  - "ready-made zoom ui"
---

# Zoom Video SDK UI Toolkit

Pre-built video conferencing UI powered by Zoom Video SDK. Drop-in solution for web applications.

**Official Documentation**: https://developers.zoom.us/docs/zoom-video-sdk/web/zoom-ui-toolkit/
**API Reference**: https://marketplacefront.zoom.us/sdk/uitoolkit/web/
**NPM Package**: https://www.npmjs.com/package/@zoom/videosdk-zoom-ui-toolkit
**Live Demo**: https://sdk.zoom.com/videosdk-uitoolkit

## Quick Links

**New to UI Toolkit? Follow this path:**

1. **Quick Start** - Get running in 5 minutes (see below)
2. **JWT Authentication** - Server-side token generation (required)
3. **Composite vs Components** - Choose your approach  
4. **Framework Integration** - React, Vue, Angular, Next.js patterns

**Having issues?**
- Session not joining → Check JWT Authentication (most common issue)
- React 18 peer dependency error → See Installation section
- CSS not loading → See [Troubleshooting](troubleshooting/common-issues.md)
- Components not showing → Check Component Lifecycle

## Overview

The Zoom Video SDK UI Toolkit is a **pre-built video UI library** that renders complete video conferencing experiences with minimal code. Unlike the raw Video SDK, the UI Toolkit provides:

- ✅ **Ready-to-use UI** - Professional video interface out of the box
- ✅ **Zero UI code** - No need to build video layouts, controls, or participant management
- ✅ **Framework agnostic** - Works with React, Vue, Angular, Next.js, vanilla JS
- ✅ **Highly customizable** - Choose which features to enable, customize themes
- ✅ **Built-in features** - Chat, screen share, settings, virtual backgrounds included

**When to use UI Toolkit:**
- You want a complete video solution quickly
- You need Zoom-like UI consistency
- You don't want to build custom video UI
- You need standard features (chat, share, participants)

**When to use raw Video SDK instead:**
- You need complete custom UI control
- You're building a non-standard video experience
- You need access to raw video/audio data
- You want to build your own rendering pipeline

## Installation

```bash
npm install @zoom/videosdk-zoom-ui-toolkit jsrsasign
npm install -D @types/jsrsasign
```

**Note**: React support depends on the UI Toolkit version. Check the package peer dependencies for your installed version (React 18 is commonly required).

## Quick Start

### Basic Usage (Vanilla JS)

```javascript
import uitoolkit from "@zoom/videosdk-zoom-ui-toolkit";
import "@zoom/videosdk-zoom-ui-toolkit/dist/videosdk-zoom-ui-toolkit.css";

const container = document.getElementById("sessionContainer");

const config = {
  videoSDKJWT: "your_jwt_token",
  sessionName: "my-session",
  userName: "John Doe",
  sessionPasscode: "",
  features: ["video", "audio", "share", "chat", "users", "settings"],
};

uitoolkit.joinSession(container, config);

uitoolkit.onSessionJoined(() => {
  console.log("Session joined");
});

uitoolkit.onSessionClosed(() => {
  console.log("Session closed");
});
```

### Next.js / React Integration

```typescript
'use client';

import { useEffect, useRef } from 'react';

export default function VideoSession({ jwt, sessionName, userName }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const uitoolkitRef = useRef<any>(null);

  useEffect(() => {
    let isMounted = true;

    const init = async () => {
      const uitoolkitModule = await import('@zoom/videosdk-zoom-ui-toolkit');
      const uitoolkit = uitoolkitModule.default;
      uitoolkitRef.current = uitoolkit;
      
      // If TypeScript complains about CSS imports, configure your app to allow them
      // (for example via a global `declare module \"*.css\";`), or import the CSS from
      // a global entrypoint (Next.js layout/_app) instead of inlining here.
      await import('@zoom/videosdk-zoom-ui-toolkit/dist/videosdk-zoom-ui-toolkit.css');

      if (!isMounted || !containerRef.current) return;

      const config: any = {
        videoSDKJWT: jwt,
        sessionName: sessionName,
        userName: userName,
        sessionPasscode: '',
        features: ['video', 'audio', 'share', 'chat', 'users', 'settings'],
      };

      uitoolkit.joinSession(containerRef.current, config);
      uitoolkit.onSessionJoined(() => console.log('Joined'));
      uitoolkit.onSessionClosed(() => console.log('Closed'));
    };

    init();

    return () => {
      isMounted = false;
      if (uitoolkitRef.current && containerRef.current) {
        try {
          uitoolkitRef.current.closeSession(containerRef.current);
        } catch (e) {}
      }
    };
  }, [jwt, sessionName, userName]);

  return <div ref={containerRef} style={{ width: '100%', height: '100vh' }} />;
}
```

## Available Features

| Feature | Description |
|---------|-------------|
| `video` | Enable video layout and send/receive video |
| `audio` | Show audio button, send/receive audio |
| `share` | Screen sharing |
| `chat` | In-session messaging |
| `users` | Participant list |
| `settings` | Device selection, virtual background |
| `preview` | Pre-join camera/mic preview |
| `recording` | Cloud recording (paid plan) |
| `leave` | Leave/end session button |

## Troubleshooting

- **[troubleshooting/common-issues.md](troubleshooting/common-issues.md)** - CSS, SSR, JWT/session join, customization limits

## JWT Token Generation (Server-Side)

**Required**: Generate JWT tokens on your server, never expose SDK secret client-side.

### Node.js / Next.js API Route

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { KJUR } from 'jsrsasign';

const ZOOM_VIDEO_SDK_KEY = process.env.ZOOM_VIDEO_SDK_KEY;
const ZOOM_VIDEO_SDK_SECRET = process.env.ZOOM_VIDEO_SDK_SECRET;

export async function POST(request: NextRequest) {
  const { sessionName, role, userName } = await request.json();

  if (!sessionName || role === undefined) {
    return NextResponse.json({ error: 'Missing params' }, { status: 400 });
  }

  const iat = Math.floor(Date.now() / 1000);
  const exp = iat + 60 * 60 * 2; // 2 hours

  const oHeader = { alg: 'HS256', typ: 'JWT' };
  const oPayload = {
    app_key: ZOOM_VIDEO_SDK_KEY,
    role_type: role, // 0 = participant, 1 = host
    tpc: sessionName,
    version: 1,
    iat,
    exp,
    user_identity: userName || 'User',
  };

  const signature = KJUR.jws.JWS.sign(
    'HS256',
    JSON.stringify(oHeader),
    JSON.stringify(oPayload),
    ZOOM_VIDEO_SDK_SECRET
  );

  return NextResponse.json({ signature });
}
```

### JWT Payload Fields

| Field | Required | Description |
|-------|----------|-------------|
| `app_key` | Yes | Your Video SDK Key |
| `role_type` | Yes | 0 = participant, 1 = host |
| `tpc` | Yes | Session/topic name |
| `version` | Yes | Always 1 |
| `iat` | Yes | Issued at (Unix timestamp) |
| `exp` | Yes | Expiration (Unix timestamp) |
| `user_identity` | No | User identifier |

## API Reference

### Core Methods

```javascript
uitoolkit.joinSession(container, config);
uitoolkit.closeSession(container);
```

### Event Listeners

```javascript
uitoolkit.onSessionJoined(callback);
uitoolkit.onSessionClosed(callback);
uitoolkit.offSessionJoined(callback);
uitoolkit.offSessionClosed(callback);
```

### Component Methods

```javascript
uitoolkit.showChatComponent(container);
uitoolkit.hideChatComponent(container);
uitoolkit.showUsersComponent(container);
uitoolkit.hideUsersComponent(container);
uitoolkit.showControlsComponent(container);
uitoolkit.hideControlsComponent(container);
uitoolkit.showSettingsComponent(container);
uitoolkit.hideSettingsComponent(container);
uitoolkit.hideAllComponents();
```

## CDN Usage (No Build Step)

```html
<link rel="stylesheet" href="https://source.zoom.us/uitoolkit/2.3.5-1/videosdk-zoom-ui-toolkit.css" />
<script src="https://source.zoom.us/uitoolkit/2.3.5-1/videosdk-zoom-ui-toolkit.min.umd.js"></script>

<div id="sessionContainer"></div>

<script>
  const uitoolkit = window.UIToolkit;
  
  uitoolkit.joinSession(document.getElementById('sessionContainer'), {
    videoSDKJWT: 'your_jwt',
    sessionName: 'my-session',
    userName: 'User',
    features: ['video', 'audio', 'chat']
  });
</script>
```

## Next.js with basePath

When deploying Next.js under a subpath:

```typescript
// next.config.ts
const nextConfig = {
  basePath: "/your-app-path",
  assetPrefix: "/your-app-path",
};
```

Fetch API routes with full path:
```typescript
fetch('/your-app-path/api/token', { ... })
```

## Prerequisites

1. **Zoom Video SDK credentials** from [Zoom Marketplace](https://marketplace.zoom.us/)
2. **React** version compatible with your installed UI Toolkit package (check peer deps; React 18 is common)
3. **Server-side JWT generation** (never expose SDK secret)
4. **Modern browser** with WebRTC support

## Browser Support

| Browser | Version |
|---------|---------|
| Chrome | 78+ |
| Firefox | 76+ |
| Safari | 14.1+ |
| Edge | 79+ |

## Common Issues

| Issue | Solution |
|-------|----------|
| `peer react@"^18.0.0"` error | Use the React version required by the installed UI Toolkit package (check peer deps; React 18 is common) |
| CSS import TypeScript error | Configure TS/CSS handling (prefer a global `*.css` module declaration); avoid `@ts-ignore` except in throwaway demos |
| Config type error | Type config as `any` |
| API returns HTML not JSON | Check basePath in fetch URL |

## Resources

- **GitHub**: https://github.com/zoom/videosdk-zoom-ui-toolkit-web
- **UI Toolkit Docs**: https://developers.zoom.us/docs/zoom-video-sdk/web/zoom-ui-toolkit/
- **Auth Endpoint Sample**: https://github.com/zoom/videosdk-auth-endpoint-sample
- **Marketplace**: https://marketplace.zoom.us/

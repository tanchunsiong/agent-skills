---
name: zoom-ui-toolkit
description: |
  Zoom Video SDK UI Toolkit - a vanilla JavaScript library that renders pre-built video UI
  into DOM containers. NOT a React component library. Use for quick video app integration
  with minimal code. Requires server-side JWT generation.
---

# Zoom Video SDK UI Toolkit

Pre-built video UI powered by Zoom Video SDK. Renders into DOM containers via JavaScript API.

## Overview

Zoom UI Toolkit provides:
- Ready-to-use video conferencing UI
- Consistent Zoom-like experience
- Vanilla JavaScript API (works with any framework)
- Built-in controls, chat, participants list
- Requires React 18 as peer dependency

## Installation

```bash
npm install @zoom/videosdk-ui-toolkit jsrsasign
npm install -D @types/jsrsasign
```

**Note**: Requires React 18 specifically (not 17, not 19).

## Quick Start

### Basic Usage (Vanilla JS)

```javascript
import uitoolkit from "@zoom/videosdk-ui-toolkit";
import "@zoom/videosdk-ui-toolkit/dist/videosdk-ui-toolkit.css";

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
      const uitoolkitModule = await import('@zoom/videosdk-ui-toolkit');
      const uitoolkit = uitoolkitModule.default;
      uitoolkitRef.current = uitoolkit;
      
      // @ts-ignore
      await import('@zoom/videosdk-ui-toolkit/dist/videosdk-ui-toolkit.css');

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
<link rel="stylesheet" href="https://source.zoom.us/uitoolkit/2.3.5/videosdk-ui-toolkit.css" />
<script src="https://source.zoom.us/uitoolkit/2.3.5/videosdk-ui-toolkit.min.umd.js"></script>

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
2. **React 18** as peer dependency
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
| `peer react@"^18.0.0"` error | Use React 18, not 17 or 19 |
| CSS import TypeScript error | Add `// @ts-ignore` before import |
| Config type error | Type config as `any` |
| API returns HTML not JSON | Check basePath in fetch URL |

## Resources

- **GitHub**: https://github.com/zoom/videosdk-ui-toolkit-web
- **UI Toolkit Docs**: https://developers.zoom.us/docs/video-sdk/web/ui-toolkit/
- **Auth Endpoint Sample**: https://github.com/zoom/videosdk-auth-endpoint-sample
- **Marketplace**: https://marketplace.zoom.us/

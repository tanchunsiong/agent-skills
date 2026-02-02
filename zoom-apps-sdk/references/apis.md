# Zoom Apps SDK - APIs

JavaScript SDK API reference for Zoom Apps.

## Overview

The Zoom Apps SDK provides JavaScript APIs for apps running inside the Zoom client.

## Initialization

```javascript
// IMPORTANT: SDK defines window.zoomSdk globally
// Do NOT use "let zoomSdk = ..." - causes redeclaration error
let sdk = window.zoomSdk;

const configResponse = await sdk.config({
  capabilities: [
    'shareApp',
    'getMeetingContext',
    'getUserContext',
    'openUrl'
  ],
  version: '0.16'
});

// configResponse contains:
// { runningContext: 'inMeeting' | 'inMainClient' | 'inWebClient', clientVersion: '...' }
```

## Context APIs

### getMeetingContext

Get current meeting information.

```javascript
const context = await sdk.getMeetingContext();
// { meetingID, meetingTopic, meetingStatus }
```

### getUserContext

Get current user information.

```javascript
const user = await sdk.getUserContext();
// { screenName, role, participantId }
```

## Action APIs

### shareApp

Share your app with meeting participants.

```javascript
await sdk.shareApp();
```

### openUrl

Open URL in external browser.

```javascript
await sdk.openUrl({ url: 'https://example.com' });
```

### sendAppInvitation

Invite participants to use your app.

```javascript
await sdk.sendAppInvitation({
  participantIds: ['user1', 'user2']
});
```

## Rendering APIs

### runRenderingContext

Start Layers API rendering context.

```javascript
await sdk.runRenderingContext({
  view: 'immersive'
});
```

## Resources

- **SDK Reference**: https://appssdk.zoom.us/
- **Capabilities list**: https://developers.zoom.us/docs/zoom-apps/capabilities/

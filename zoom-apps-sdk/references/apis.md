# Zoom Apps SDK - APIs

JavaScript SDK API reference for Zoom Apps.

## Overview

The Zoom Apps SDK provides JavaScript APIs for apps running inside the Zoom client.

## Initialization

```javascript
const zoomSdk = new ZoomSdk({ version: '0.16' });

const configResponse = await zoomSdk.config({
  capabilities: [
    'shareApp',
    'getMeetingContext',
    'getUserContext',
    'openUrl'
  ]
});
```

## Context APIs

### getMeetingContext

Get current meeting information.

```javascript
const context = await zoomSdk.getMeetingContext();
// { meetingID, meetingTopic, meetingStatus }
```

### getUserContext

Get current user information.

```javascript
const user = await zoomSdk.getUserContext();
// { screenName, role, participantId }
```

## Action APIs

### shareApp

Share your app with meeting participants.

```javascript
await zoomSdk.shareApp();
```

### openUrl

Open URL in external browser.

```javascript
await zoomSdk.openUrl({ url: 'https://example.com' });
```

### sendAppInvitation

Invite participants to use your app.

```javascript
await zoomSdk.sendAppInvitation({
  participantIds: ['user1', 'user2']
});
```

## Rendering APIs

### runRenderingContext

Start Layers API rendering context.

```javascript
await zoomSdk.runRenderingContext({
  view: 'immersive'
});
```

## Resources

- **SDK Reference**: https://appssdk.zoom.us/
- **Capabilities list**: https://developers.zoom.us/docs/zoom-apps/capabilities/

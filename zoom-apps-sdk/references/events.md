# Zoom Apps SDK - Events

Event listeners for Zoom Apps.

## Overview

Subscribe to events to respond to meeting and user actions.

**IMPORTANT**: Register event listeners AFTER successful `sdk.config()` call.

## Subscribing to Events

```javascript
// sdk = window.zoomSdk (see apis.md for initialization)
sdk.addEventListener('onMeetingChange', (event) => {
  console.log('Meeting changed:', event);
});
```

## Meeting Events

### onMeetingChange

Fired when meeting state changes.

```javascript
sdk.addEventListener('onMeetingChange', (event) => {
  const { meetingStatus } = event;
  // meetingStatus: 'started', 'ended', etc.
});
```

### onParticipantChange

Fired when participants join or leave.

```javascript
sdk.addEventListener('onParticipantChange', (event) => {
  const { participants, action } = event;
  // action: 'join', 'leave'
});
```

## User Events

### onMyUserContextChange

Fired when current user's context changes.

```javascript
sdk.addEventListener('onMyUserContextChange', (event) => {
  const { role, screenName } = event;
});
```

## App Events

### onShareApp

Fired when app is shared/unshared.

```javascript
sdk.addEventListener('onShareApp', (event) => {
  const { isShared } = event;
});
```

### onAppPopout

Fired when app is popped out/in.

```javascript
sdk.addEventListener('onAppPopout', (event) => {
  const { isPopout } = event;
});
```

## Removing Listeners

```javascript
const listener = sdk.addEventListener('onMeetingChange', handler);

// Later, remove it
sdk.removeEventListener('onMeetingChange', listener);
```

## Resources

- **Events reference**: https://appssdk.zoom.us/

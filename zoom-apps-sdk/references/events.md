# Zoom Apps SDK - Events

Event listeners for Zoom Apps.

## Overview

Subscribe to events to respond to meeting and user actions.

## Subscribing to Events

```javascript
zoomSdk.addEventListener('onMeetingChange', (event) => {
  console.log('Meeting changed:', event);
});
```

## Meeting Events

### onMeetingChange

Fired when meeting state changes.

```javascript
zoomSdk.addEventListener('onMeetingChange', (event) => {
  const { meetingStatus } = event;
  // meetingStatus: 'started', 'ended', etc.
});
```

### onParticipantChange

Fired when participants join or leave.

```javascript
zoomSdk.addEventListener('onParticipantChange', (event) => {
  const { participants, action } = event;
  // action: 'join', 'leave'
});
```

## User Events

### onMyUserContextChange

Fired when current user's context changes.

```javascript
zoomSdk.addEventListener('onMyUserContextChange', (event) => {
  const { role, screenName } = event;
});
```

## App Events

### onShareApp

Fired when app is shared/unshared.

```javascript
zoomSdk.addEventListener('onShareApp', (event) => {
  const { isShared } = event;
});
```

### onAppPopout

Fired when app is popped out/in.

```javascript
zoomSdk.addEventListener('onAppPopout', (event) => {
  const { isPopout } = event;
});
```

## Removing Listeners

```javascript
const listener = zoomSdk.addEventListener('onMeetingChange', handler);

// Later, remove it
zoomSdk.removeEventListener('onMeetingChange', listener);
```

## Resources

- **Events reference**: https://appssdk.zoom.us/

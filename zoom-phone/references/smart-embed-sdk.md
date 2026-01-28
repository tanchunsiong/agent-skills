# Zoom Phone Smart Embed SDK

Embed Zoom Phone calling capabilities directly into your web application.

## Overview

Smart Embed SDK provides a pre-built phone UI that you can embed in your app, or use headless mode for custom UI.

## Installation

### Script Tag

```html
<script src="https://static.zoom.us/phone/embed/v1/zp-embed.js"></script>
```

### NPM

```bash
npm install @zoom/phone-embed-sdk
```

```javascript
import { ZoomPhoneEmbed } from '@zoom/phone-embed-sdk';
```

## Initialization

```javascript
const phone = new ZoomPhoneEmbed({
  clientId: 'YOUR_OAUTH_CLIENT_ID',
  redirectUri: 'https://yourapp.com/callback',
  
  // Optional: customize UI
  container: document.getElementById('phone-container'),
  theme: 'light',  // or 'dark'
  
  // Optional: headless mode (no UI)
  headless: false
});

// Initialize and authenticate
await phone.init();
```

## Authentication Flow

Smart Embed uses OAuth 2.0:

1. User clicks "Connect Zoom Phone"
2. SDK redirects to Zoom authorization
3. User approves permissions
4. Zoom redirects back with auth code
5. SDK exchanges code for tokens

```javascript
// Check if already authenticated
if (phone.isAuthenticated()) {
  console.log('User is logged in');
} else {
  // Start OAuth flow
  phone.authorize();
}

// Handle OAuth callback
phone.on('authorized', (user) => {
  console.log('Logged in as:', user.email);
});
```

## Making Calls

### Basic Call

```javascript
// Dial a number
const call = await phone.makeCall('+14155551234');

// With caller ID (if multiple numbers assigned)
const call = await phone.makeCall('+14155551234', {
  callerId: '+14155550001'
});
```

### Call Controls

```javascript
// Mute/unmute
call.mute();
call.unmute();

// Hold/resume
call.hold();
call.resume();

// Send DTMF tones
call.sendDTMF('1234#');

// End call
call.hangup();
```

### Transfer Calls

```javascript
// Blind transfer
call.transfer('+14155559999');

// Warm transfer (consultation first)
const consultCall = await call.consultTransfer('+14155559999');
// After consulting:
consultCall.completeTransfer();  // Complete transfer
// or
consultCall.cancelTransfer();   // Return to original call
```

## Handling Incoming Calls

```javascript
phone.on('incomingCall', (call) => {
  console.log('Incoming call from:', call.callerNumber);
  console.log('Caller name:', call.callerName);
  
  // Answer
  call.answer();
  
  // Or decline
  call.decline();
  
  // Or send to voicemail
  call.sendToVoicemail();
});

// Call state changes
phone.on('callStateChanged', (call) => {
  console.log('Call state:', call.state);
  // States: ringing, connecting, connected, holding, ended
});

phone.on('callEnded', (call) => {
  console.log('Call ended, duration:', call.duration);
});
```

## Call Recording

```javascript
// Start recording (if permitted)
await call.startRecording();

// Stop recording
await call.stopRecording();

// Recording events
phone.on('recordingStarted', (call) => {
  console.log('Recording started');
});

phone.on('recordingStopped', (call) => {
  console.log('Recording stopped');
});
```

## Presence and Status

```javascript
// Get current status
const status = phone.getPresence();
// Returns: 'available', 'busy', 'dnd', 'away', 'offline'

// Set status
phone.setPresence('dnd');  // Do Not Disturb

// Watch status changes
phone.on('presenceChanged', (status) => {
  console.log('Status changed to:', status);
});
```

## Contacts and Directory

```javascript
// Search contacts
const contacts = await phone.searchContacts('John');

// Get contact details
const contact = await phone.getContact(contactId);

// Dial contact
phone.makeCall(contact.phoneNumber);
```

## Voicemail

```javascript
// Get voicemail list
const voicemails = await phone.getVoicemails();

// Play voicemail
voicemails[0].play();

// Mark as read
voicemails[0].markAsRead();

// Delete
voicemails[0].delete();
```

## Headless Mode

For custom UI, use headless mode:

```javascript
const phone = new ZoomPhoneEmbed({
  clientId: 'YOUR_CLIENT_ID',
  redirectUri: 'YOUR_REDIRECT_URI',
  headless: true  // No default UI
});

await phone.init();

// Build your own UI and call SDK methods
document.getElementById('dial-btn').onclick = () => {
  const number = document.getElementById('phone-input').value;
  phone.makeCall(number);
};
```

## Events Reference

| Event | Description | Payload |
|-------|-------------|---------|
| `authorized` | OAuth completed | User info |
| `incomingCall` | New incoming call | Call object |
| `callStateChanged` | Call state change | Call object |
| `callEnded` | Call terminated | Call object |
| `presenceChanged` | Status changed | Status string |
| `recordingStarted` | Recording began | Call object |
| `recordingStopped` | Recording ended | Call object |
| `error` | Error occurred | Error object |

## Error Handling

```javascript
phone.on('error', (error) => {
  console.error('Phone error:', error.code, error.message);
});

// Common error codes
// UNAUTHORIZED - Need to re-authenticate
// CALL_FAILED - Call could not connect
// NO_MICROPHONE - Microphone access denied
// NETWORK_ERROR - Connection issue
```

## Required Scopes

| Scope | Description |
|-------|-------------|
| `phone:read` | Read phone data |
| `phone:write` | Make calls, update settings |
| `phone_sms:read` | Read SMS |
| `phone_sms:write` | Send SMS |
| `phone_recording:read` | Access recordings |

## Browser Requirements

- Chrome 70+
- Firefox 60+
- Safari 14+
- Edge 79+
- Microphone permission required

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No audio | Check microphone permissions in browser |
| Call fails immediately | Verify OAuth scopes include `phone:write` |
| Can't receive calls | Ensure browser tab is active and not sleeping |
| Echo/feedback | Use headphones or enable echo cancellation |

## Resources

- **Official docs**: https://developers.zoom.us/docs/zoom-phone/smart-embed/
- **Sample app**: https://github.com/zoom/phone-embed-sample

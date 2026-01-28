---
name: zoom-phone
description: |
  Zoom Phone SDK and API integration guide. Covers Smart Embed (web-only) for embedding phone 
  functionality, REST APIs for call management, call logs, voicemail, and phone system configuration.
  Use when building cloud phone integrations, call center solutions, or embedding calling 
  capabilities into web applications.
---

# Zoom Phone SDK & API

Build cloud phone system integrations with Zoom Phone APIs and embed calling functionality with Smart Embed.

## Overview

Zoom Phone is a cloud phone system that provides:
- VoIP calling with HD voice
- SMS/MMS messaging (read-only via API, no send endpoint)
- Voicemail with transcription
- Call recording and analytics
- Auto-attendant and IVR
- Call queues and routing

## Important Limitations

| Feature | Status |
|---------|--------|
| **Send SMS via API** | NOT available (read-only) |
| **Native mobile SDK** | NOT available (web Smart Embed only) |
| **Phone number provisioning** | Admin Console only (limited API) |
| **has_recording field** | Deprecated (use webhooks) |

## Choose Your Integration

| I want to... | Use this |
|--------------|----------|
| Embed click-to-dial in my **web** app | **Smart Embed** (web only) |
| Read call logs programmatically | **Phone REST API** |
| Read SMS history | **Phone REST API** |
| Receive incoming SMS notifications | **Webhooks** |
| Access voicemail | **Phone REST API** |
| Build mobile app with phone | **REST API + Zoom mobile app** |
| Automate phone system configuration | **Phone REST API** |
| Get call analytics and reports | **Phone REST API** + **zoom-webhooks** |

## Smart Embed (Web Only)

Smart Embed allows you to embed Zoom Phone calling capabilities directly into your **web application**. There are no native iOS/Android SDKs for Zoom Phone.

### Key Features

| Feature | Description |
|---------|-------------|
| **Click-to-dial** | Initiate calls from your app |
| **Incoming call handling** | Receive and answer calls |
| **Call controls** | Hold, transfer, mute, DTMF |
| **Call recording** | Start/stop recording |
| **Presence** | User availability status |

### Quick Start

```html
<!-- Include Smart Embed -->
<script src="https://static.zoom.us/phone/embed/v1/zp-embed.js"></script>

<script>
const phone = new ZoomPhoneEmbed({
  clientId: 'YOUR_CLIENT_ID',
  redirectUri: 'YOUR_REDIRECT_URI'
});

// Initialize
await phone.init();

// Make a call
await phone.makeCall('+14155551234');

// Handle incoming calls
phone.on('incomingCall', (call) => {
  console.log('Incoming call from:', call.callerNumber);
  call.answer();
});
</script>
```

## Phone REST API

Programmatic access to Zoom Phone data (primarily read operations).

### Capabilities

| Category | Endpoints | Description |
|----------|-----------|-------------|
| **Call Logs** | `/phone/users/{userId}/call_logs` | Historical call data |
| **Call History** | `/phone/call_history` | Account call history |
| **SMS Sessions** | `/phone/users/{userId}/sms/sessions` | SMS thread history (READ ONLY) |
| **Voicemail** | `/phone/users/{userId}/voicemails` | Access voicemail messages |
| **Recordings** | `/phone/users/{userId}/recordings` | Call recordings |
| **Users** | `/phone/users` | Phone user management |
| **Call Queues** | `/phone/call_queues` | Queue configuration |
| **Auto Receptionist** | `/phone/auto_receptionists` | IVR setup |

### Example: Get Call History

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/phone/users/me/call_logs?from=2024-01-01&to=2024-01-31',
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const logs = await response.json();
// logs.call_logs contains call history
```

### Example: Get SMS Sessions

```javascript
// NOTE: Read-only - no send SMS API exists
const response = await fetch(
  'https://api.zoom.us/v2/phone/users/me/sms/sessions?from=2024-01-01&to=2024-01-31',
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);
```

## URI Redirect (Initiate Calls/SMS)

For web apps, use URI schemes to open Zoom Phone client:

```javascript
// Initiate call (opens Zoom Phone)
window.location.href = 'zoomphonecall://call?number=+14155551234';

// Initiate SMS (opens Zoom Phone SMS composer)
window.location.href = 'zoomphonecall://sms?number=+14155551234';
```

## Prerequisites

1. **Zoom Phone license** - Users need Zoom Phone enabled
2. **OAuth app** - Create in [Zoom App Marketplace](https://marketplace.zoom.us/)
3. **Scopes** - See [references/scopes.md](references/scopes.md) for required permissions

## Common Use Cases

| Use Case | Description | Integration |
|----------|-------------|-------------|
| **CRM Click-to-Dial** | Call contacts from web CRM | Smart Embed |
| **Call Analytics Dashboard** | View call metrics and history | REST API |
| **SMS History Viewer** | Read SMS conversations | REST API |
| **Incoming SMS Logging** | Log all incoming SMS | Webhooks |
| **Call Recording Access** | Download/manage recordings | REST API + Webhooks |
| **IVR Configuration** | Read auto-receptionist setup | REST API |

## Webhooks

Zoom Phone sends real-time events via webhooks:

| Event | Trigger |
|-------|---------|
| `phone.callee_answered` | Call answered |
| `phone.callee_ended` | Call ended |
| `phone.callee_missed` | Missed call |
| `phone.voicemail_received` | New voicemail |
| `phone.sms_received` | Incoming SMS |
| `phone.recording_completed` | Recording ready |

**Important**: Use `phone.recording_completed` webhook to know when recordings are ready. The `has_recording` field in call logs is deprecated.

See **zoom-webhooks** skill for webhook setup.

## Mobile Integration

Since there's no native Zoom Phone SDK for iOS/Android:

1. Use REST APIs from your backend
2. Users make/receive calls via Zoom mobile app
3. Your app can read call logs, recordings, SMS history via API
4. Use webhooks for real-time notifications

## Detailed References

- **[references/smart-embed-sdk.md](references/smart-embed-sdk.md)** - Smart Embed guide (web only)
- **[references/rest-api.md](references/rest-api.md)** - Phone API endpoints
- **[references/sms.md](references/sms.md)** - SMS integration (READ ONLY)
- **[references/call-handling.md](references/call-handling.md)** - Call flows and controls
- **[references/scopes.md](references/scopes.md)** - Required OAuth scopes

## Resources

- **Official docs**: https://developers.zoom.us/docs/zoom-phone/
- **Smart Embed Guide**: https://developers.zoom.us/docs/zoom-phone/smart-embed-guide/
- **API Reference**: https://developers.zoom.us/docs/api/rest/reference/phone/methods/
- **Smart Embed Demo**: https://github.com/PandaBacon21/zoom-smartembeddemo
- **Marketplace**: https://marketplace.zoom.us/

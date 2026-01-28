# Zoom Phone SMS/MMS

Read SMS history and initiate SMS via URI redirect (no send API).

## Overview

Zoom Phone supports SMS (text) and MMS (multimedia) messaging for US and Canadian phone numbers.

**IMPORTANT LIMITATION**: As of 2025, there is **NO REST API to send SMS programmatically**. You can only:
- Read SMS history via API
- Get SMS sessions/threads via API
- Initiate SMS via URI redirect (opens Zoom client)
- Receive incoming SMS via webhooks

## Prerequisites

- Zoom Phone license with SMS enabled
- US or Canadian phone number assigned
- OAuth app with `phone_sms:read` scope

## API Capabilities

### What You CAN Do

| Action | Method | Available |
|--------|--------|-----------|
| Read SMS history | API | Yes |
| Get SMS sessions | API | Yes |
| Receive SMS notification | Webhook | Yes |
| Initiate SMS (opens Zoom) | URI redirect | Yes |
| **Send SMS programmatically** | API | **NO** |

## Read SMS Sessions

```javascript
// GET /phone/users/{userId}/sms/sessions
const params = new URLSearchParams({
  from: '2024-01-01',
  to: '2024-01-31',
  page_size: 50
});

const response = await fetch(
  `https://api.zoom.us/v2/phone/users/${userId}/sms/sessions?${params}`,
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const sessions = await response.json();
// {
//   "sms_sessions": [
//     {
//       "session_id": "sess_123",
//       "phone_number": "+14155559999",
//       "last_message": "Thanks for the info!",
//       "last_message_time": "2024-01-15T10:00:00Z",
//       "unread_count": 0
//     }
//   ],
//   "total_records": 50
// }
```

## Receive SMS via Webhook

Configure webhook to receive `phone.sms_received` events:

```javascript
// Webhook payload for incoming SMS
{
  "event": "phone.sms_received",
  "payload": {
    "account_id": "abc123",
    "object": {
      "id": "msg_xyz789",
      "from_phone_number": "+14155559999",
      "to_phone_number": "+14155551234",
      "message": "Yes, I'll be there!",
      "date_time": "2024-01-15T10:30:00Z",
      "direction": "inbound"
    }
  }
}
```

### Webhook Handler Example

```javascript
// Express.js webhook handler
app.post('/webhook/sms', async (req, res) => {
  const { event, payload } = req.body;
  
  if (event === 'phone.sms_received') {
    const { from_phone_number, message, date_time } = payload.object;
    
    // Log incoming SMS
    console.log(`SMS from ${from_phone_number}: ${message}`);
    
    // Store in your database
    await db.smsMessages.create({
      from: from_phone_number,
      message: message,
      receivedAt: date_time
    });
    
    // NOTE: Cannot auto-reply via API - no send endpoint exists
  }
  
  res.sendStatus(200);
});
```

## Initiate SMS via URI Redirect

Open Zoom client with pre-filled SMS:

```javascript
// URI scheme to initiate SMS
const phoneNumber = '+14155551234';
const smsUri = `zoomphonecall://sms?number=${encodeURIComponent(phoneNumber)}`;

// In web app
window.location.href = smsUri;

// Or as a link
<a href="zoomphonecall://sms?number=%2B14155551234">Send SMS</a>
```

This opens the Zoom Phone app with the SMS composer. User must manually send.

## Use Cases (Given Limitations)

### SMS Analytics Dashboard

Since you can read SMS history, build analytics:

```javascript
async function getSMSStats(userId, from, to) {
  const sessions = await fetch(
    `https://api.zoom.us/v2/phone/users/${userId}/sms/sessions?from=${from}&to=${to}`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  ).then(r => r.json());
  
  return {
    totalConversations: sessions.total_records,
    unreadMessages: sessions.sms_sessions.reduce(
      (sum, s) => sum + s.unread_count, 0
    )
  };
}
```

### Incoming SMS Logging

Log all incoming SMS for compliance:

```javascript
app.post('/webhook/sms', async (req, res) => {
  if (req.body.event === 'phone.sms_received') {
    const msg = req.body.payload.object;
    
    await auditLog.create({
      type: 'sms_received',
      from: msg.from_phone_number,
      to: msg.to_phone_number,
      content: msg.message,
      timestamp: msg.date_time
    });
  }
  res.sendStatus(200);
});
```

### Click-to-SMS in CRM

Add SMS buttons that open Zoom:

```javascript
function renderSMSButton(contact) {
  return `
    <a href="zoomphonecall://sms?number=${encodeURIComponent(contact.phone)}" 
       class="btn btn-sms">
      SMS ${contact.name}
    </a>
  `;
}
```

## Limitations

| Limitation | Value |
|------------|-------|
| **Send SMS via API** | **NOT AVAILABLE** |
| Geographic support | US, Canada only |
| Max message length | 1600 characters |
| MMS file size | 5 MB max |
| Supported media types | JPEG, PNG, GIF, MP4 |

## Feature Request Status

The community has requested a Send SMS API endpoint. Check the Zoom Developer Forum for updates:
- [Forum Discussion: SMS Send API Request](https://devforum.zoom.us/t/is-there-any-possible-timeline-for-a-zoom-phone-send-sms-api-endpoint/106386)

## Required Scopes

| Scope | Operations |
|-------|------------|
| `phone_sms:read` | Read SMS sessions/history |
| `phone_sms:read:admin` | Read all account SMS |

Note: `phone_sms:write` scope exists but there's no write endpoint currently.

## Webhooks

| Event | Trigger |
|-------|---------|
| `phone.sms_received` | Incoming SMS received |

## Resources

- **API Reference**: https://developers.zoom.us/docs/api/rest/reference/phone/methods/#tag/SMS
- **URI Redirect Guide**: https://developers.zoom.us/docs/zoom-phone/

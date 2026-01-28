# Zoom Phone Call Handling

Call flows, controls, and advanced call management.

## Call States

```
Initiating → Ringing → Connected → Ended
                ↓           ↓
              Declined    Holding → Connected
                           ↓
                      Transferred
```

| State | Description |
|-------|-------------|
| `initiating` | Call being set up |
| `ringing` | Ringing at destination |
| `connected` | Call active |
| `holding` | Call on hold |
| `ended` | Call terminated |

## Outbound Calls

### Make Call via API

```javascript
// POST /phone/users/{userId}/calls
const call = await fetch(
  `https://api.zoom.us/v2/phone/users/${userId}/calls`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      callee: '+14155551234',
      caller_id: '+14155550001'  // Optional: specific number to display
    })
  }
).then(r => r.json());

// { "call_id": "abc123", "status": "ringing" }
```

### With Smart Embed SDK

```javascript
const call = await phone.makeCall('+14155551234');

call.on('ringing', () => console.log('Ringing...'));
call.on('connected', () => console.log('Connected!'));
call.on('ended', () => console.log('Call ended'));
```

## Inbound Calls

### Via Smart Embed SDK

```javascript
phone.on('incomingCall', (call) => {
  // Get caller info
  console.log('From:', call.callerNumber);
  console.log('Name:', call.callerName);
  console.log('Via:', call.dialedNumber);  // Which of your numbers was called
  
  // Options:
  call.answer();          // Answer call
  call.decline();         // Reject call
  call.sendToVoicemail(); // Send to voicemail
});
```

### Via Webhook

```javascript
// phone.callee_ringing webhook
{
  "event": "phone.callee_ringing",
  "payload": {
    "object": {
      "call_id": "abc123",
      "caller_number": "+14155551234",
      "caller_name": "John Doe",
      "callee_number": "+14155550001",
      "date_time": "2024-01-15T10:30:00Z"
    }
  }
}
```

## Call Controls

### Hold/Resume

```javascript
// API: Put on hold
await fetch(
  `https://api.zoom.us/v2/phone/users/${userId}/calls/${callId}`,
  {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ action: 'hold' })
  }
);

// API: Resume
await fetch(
  `https://api.zoom.us/v2/phone/users/${userId}/calls/${callId}`,
  {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ action: 'resume' })
  }
);

// SDK
call.hold();
call.resume();
```

### Mute/Unmute

```javascript
// SDK only (no API for mute)
call.mute();
call.unmute();
call.isMuted;  // Check status
```

### DTMF (Dial Tones)

```javascript
// For IVR navigation
call.sendDTMF('1');      // Press 1
call.sendDTMF('1234#');  // Enter PIN + #
```

## Call Transfer

### Blind Transfer

Transfer immediately without consulting:

```javascript
// API
await fetch(
  `https://api.zoom.us/v2/phone/users/${userId}/calls/${callId}`,
  {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      action: 'transfer',
      transfer_to: '+14155559999'
    })
  }
);

// SDK
call.transfer('+14155559999');
```

### Warm Transfer (Consultation)

Speak with transfer target before completing:

```javascript
// SDK: Start consultation call
const consultCall = await call.consultTransfer('+14155559999');

// Original call is on hold
// consultCall is connected

// Option 1: Complete transfer
consultCall.completeTransfer();

// Option 2: Cancel and return to original
consultCall.cancelTransfer();
```

### Transfer to Voicemail

```javascript
// Transfer to another user's voicemail
await fetch(
  `https://api.zoom.us/v2/phone/users/${userId}/calls/${callId}`,
  {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      action: 'transfer_voicemail',
      transfer_to_user_id: 'user_xyz'
    })
  }
);
```

## Call Recording

### Start/Stop Recording

```javascript
// API: Start recording
await fetch(
  `https://api.zoom.us/v2/phone/users/${userId}/calls/${callId}/recordings`,
  {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

// API: Stop recording
await fetch(
  `https://api.zoom.us/v2/phone/users/${userId}/calls/${callId}/recordings`,
  {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

// SDK
await call.startRecording();
await call.stopRecording();
```

### Automatic Recording

Configure in account settings for:
- All calls
- Inbound only
- Outbound only

### Recording Webhook

```javascript
// phone.recording_completed
{
  "event": "phone.recording_completed",
  "payload": {
    "object": {
      "call_id": "abc123",
      "recording_id": "rec_xyz",
      "duration": 180,
      "download_url": "https://zoom.us/...",
      "date_time": "2024-01-15T10:35:00Z"
    }
  }
}
```

## Call Queues

### Overview

Call queues distribute incoming calls to a group of agents.

```
Incoming Call → Queue → Ring Agents → Connect
                  ↓
              (Wait Music)
                  ↓
              (Max Wait) → Overflow
```

### Queue Ring Modes

| Mode | Description |
|------|-------------|
| `simultaneous` | Ring all agents at once |
| `sequential` | Ring agents in order |
| `rotating` | Round-robin distribution |
| `longest_idle` | Ring agent idle longest |

### Agent Queue Management

```javascript
// List queues user belongs to
const queues = await fetch(
  `https://api.zoom.us/v2/phone/users/${userId}/call_queues`,
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
).then(r => r.json());

// Log in/out of queue
await fetch(
  `https://api.zoom.us/v2/phone/users/${userId}/call_queues/${queueId}/status`,
  {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      status: 'logged_in'  // or 'logged_out'
    })
  }
);
```

## Auto Receptionist (IVR)

### Create IVR Menu

```javascript
// POST /phone/auto_receptionists
const ivr = await fetch(
  'https://api.zoom.us/v2/phone/auto_receptionists',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: 'Main Menu',
      extension_number: '1000',
      greeting_prompt: 'custom',  // or 'default'
      greeting_audio_id: 'audio_123',  // If custom
      key_actions: [
        {
          key: '1',
          action: 'transfer_user',
          target_id: 'user_sales'
        },
        {
          key: '2',
          action: 'transfer_call_queue',
          target_id: 'queue_support'
        },
        {
          key: '0',
          action: 'transfer_user',
          target_id: 'user_operator'
        }
      ]
    })
  }
).then(r => r.json());
```

### IVR Key Actions

| Action | Description |
|--------|-------------|
| `transfer_user` | Transfer to user extension |
| `transfer_call_queue` | Transfer to call queue |
| `transfer_common_area` | Transfer to common area phone |
| `transfer_auto_receptionist` | Transfer to another IVR |
| `transfer_voicemail` | Send to voicemail |
| `leave_voicemail` | Leave voicemail for user |
| `play_message` | Play audio message |
| `external_number` | Dial external number |

## Call Forwarding

### Configure Forwarding

```javascript
// PATCH /phone/users/{userId}/settings
await fetch(
  `https://api.zoom.us/v2/phone/users/${userId}/settings`,
  {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      call_forwarding: {
        enable: true,
        settings: [
          {
            description: 'Forward to mobile',
            phone_number: '+14155559999',
            enable: true
          }
        ]
      }
    })
  }
);
```

### Forwarding Types

| Type | Setting |
|------|---------|
| Always forward | `call_forwarding.enable = true` |
| Forward when busy | `call_forwarding.busy.enable = true` |
| Forward when no answer | `call_forwarding.no_answer.enable = true` |
| Forward when offline | `call_forwarding.not_reachable.enable = true` |

## Webhooks Reference

| Event | Trigger |
|-------|---------|
| `phone.callee_ringing` | Incoming call ringing |
| `phone.callee_answered` | Call answered |
| `phone.callee_missed` | Missed call |
| `phone.callee_ended` | Call ended |
| `phone.caller_ringing` | Outbound call ringing |
| `phone.caller_answered` | Outbound call connected |
| `phone.caller_ended` | Outbound call ended |
| `phone.call_transferred` | Call was transferred |
| `phone.recording_started` | Recording began |
| `phone.recording_completed` | Recording finished |
| `phone.voicemail_received` | New voicemail |

## Resources

- **Call handling docs**: https://developers.zoom.us/docs/zoom-phone/
- **API reference**: https://developers.zoom.us/docs/api/rest/reference/phone/methods/

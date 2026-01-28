# Zoom Phone REST API

Programmatic access to Zoom Phone functionality.

## Base URL

```
https://api.zoom.us/v2/phone
```

## Authentication

Use OAuth 2.0 access token:

```
Authorization: Bearer {access_token}
```

See **zoom-platform** → **authentication.md** for OAuth setup.

## Core Endpoints

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/phone/users` | List phone users |
| GET | `/phone/users/{userId}` | Get user details |
| PATCH | `/phone/users/{userId}` | Update user settings |
| GET | `/phone/users/{userId}/settings` | Get calling settings |

### Calls

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/phone/users/{userId}/calls` | Initiate outbound call |
| GET | `/phone/users/{userId}/calls` | List active calls |
| PATCH | `/phone/users/{userId}/calls/{callId}` | Update call (hold, transfer) |
| DELETE | `/phone/users/{userId}/calls/{callId}` | End call |

### Call Logs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/phone/users/{userId}/call_logs` | User's call history |
| GET | `/phone/call_logs` | Account call logs (admin) |
| GET | `/phone/call_logs/{callLogId}` | Specific call details |
| DELETE | `/phone/users/{userId}/call_logs` | Delete call history |

### Voicemail

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/phone/users/{userId}/voice_mails` | List voicemails |
| GET | `/phone/users/{userId}/voice_mails/{voicemailId}` | Get voicemail |
| DELETE | `/phone/users/{userId}/voice_mails/{voicemailId}` | Delete voicemail |
| PATCH | `/phone/users/{userId}/voice_mails/{voicemailId}` | Update status (read/unread) |

### Recordings

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/phone/users/{userId}/recordings` | List recordings |
| GET | `/phone/users/{userId}/recordings/{recordingId}` | Get recording details |
| DELETE | `/phone/users/{userId}/recordings/{recordingId}` | Delete recording |
| GET | `/phone/recordings/{recordingId}/transcript` | Get transcript |

### Phone Numbers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/phone/numbers` | List all numbers |
| POST | `/phone/numbers` | Add number |
| GET | `/phone/numbers/{numberId}` | Get number details |
| PATCH | `/phone/numbers/{numberId}` | Update number assignment |
| DELETE | `/phone/numbers/{numberId}` | Remove number |

### Call Queues

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/phone/call_queues` | List call queues |
| POST | `/phone/call_queues` | Create queue |
| GET | `/phone/call_queues/{queueId}` | Get queue |
| PATCH | `/phone/call_queues/{queueId}` | Update queue |
| DELETE | `/phone/call_queues/{queueId}` | Delete queue |
| GET | `/phone/call_queues/{queueId}/members` | List members |
| POST | `/phone/call_queues/{queueId}/members` | Add members |

### Auto Receptionist

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/phone/auto_receptionists` | List auto receptionists |
| POST | `/phone/auto_receptionists` | Create IVR |
| GET | `/phone/auto_receptionists/{arId}` | Get IVR |
| PATCH | `/phone/auto_receptionists/{arId}` | Update IVR |
| DELETE | `/phone/auto_receptionists/{arId}` | Delete IVR |

## Common Operations

### Make Outbound Call

```javascript
// POST /phone/users/{userId}/calls
const response = await fetch(
  `https://api.zoom.us/v2/phone/users/${userId}/calls`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      callee: '+14155551234',
      caller_id: '+14155550001'  // Optional: which number to show
    })
  }
);

const call = await response.json();
// { "call_id": "abc123", "status": "ringing" }
```

### Get Call History

```javascript
// GET /phone/users/{userId}/call_logs
const params = new URLSearchParams({
  from: '2024-01-01',
  to: '2024-01-31',
  page_size: 30,
  type: 'all'  // 'all', 'missed', 'voicemail'
});

const response = await fetch(
  `https://api.zoom.us/v2/phone/users/${userId}/call_logs?${params}`,
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const logs = await response.json();
// {
//   "call_logs": [
//     {
//       "id": "log123",
//       "caller_number": "+14155551234",
//       "callee_number": "+14155559999",
//       "direction": "outbound",
//       "duration": 180,
//       "result": "connected",
//       "date_time": "2024-01-15T10:30:00Z"
//     }
//   ],
//   "page_count": 5,
//   "page_number": 1,
//   "page_size": 30,
//   "total_records": 142
// }
```

### Transfer Call

```javascript
// PATCH /phone/users/{userId}/calls/{callId}
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
```

### Create Call Queue

```javascript
// POST /phone/call_queues
const response = await fetch(
  'https://api.zoom.us/v2/phone/call_queues',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: 'Sales Queue',
      extension_number: '5001',
      site_id: 'site_abc123',
      status: 'active',
      settings: {
        max_wait_time: 300,  // 5 minutes
        wrap_up_time: 60,
        ring_mode: 'simultaneous'  // or 'sequential', 'rotating'
      }
    })
  }
);
```

### Download Recording

```javascript
// GET /phone/users/{userId}/recordings/{recordingId}
const recording = await fetch(
  `https://api.zoom.us/v2/phone/users/${userId}/recordings/${recordingId}`,
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
).then(r => r.json());

// Download the audio file
const audioResponse = await fetch(recording.download_url, {
  headers: { 'Authorization': `Bearer ${accessToken}` }
});
const audioBlob = await audioResponse.blob();
```

## Pagination

List endpoints support pagination:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `page_size` | Results per page | 30 |
| `page_number` | Page number | 1 |
| `next_page_token` | Token for next page | - |

```javascript
// Using next_page_token
let allLogs = [];
let nextPageToken = null;

do {
  const url = `https://api.zoom.us/v2/phone/call_logs?page_size=100${
    nextPageToken ? `&next_page_token=${nextPageToken}` : ''
  }`;
  
  const response = await fetch(url, { headers: { 'Authorization': `Bearer ${token}` } });
  const data = await response.json();
  
  allLogs.push(...data.call_logs);
  nextPageToken = data.next_page_token;
} while (nextPageToken);
```

## Rate Limits

| Endpoint Type | Rate Limit |
|---------------|------------|
| Light | 30 req/sec |
| Medium | 20 req/sec |
| Heavy | 10 req/sec |

Call management endpoints are typically Medium. See **zoom-rest-api** → **rate-limits.md**.

## Error Responses

| Code | Meaning |
|------|---------|
| 400 | Invalid request |
| 401 | Unauthorized |
| 403 | Forbidden (missing scope) |
| 404 | Resource not found |
| 429 | Rate limit exceeded |

```json
{
  "code": 403,
  "message": "Forbidden: Missing scope phone:write"
}
```

## Required Scopes

| Scope | Operations |
|-------|------------|
| `phone:read` | Get users, call logs, settings |
| `phone:write` | Make calls, update settings |
| `phone:read:admin` | Account-wide read access |
| `phone:write:admin` | Account-wide write access |
| `phone_call_log:read` | Read call logs |
| `phone_call_log:read:admin` | Account call logs |
| `phone_recording:read` | Access recordings |
| `phone_voicemail:read` | Access voicemails |

## Resources

- **API Reference**: https://developers.zoom.us/docs/api/rest/reference/phone/methods/
- **Postman Collection**: https://marketplace.zoom.us/docs/guides/tools-resources/postman/

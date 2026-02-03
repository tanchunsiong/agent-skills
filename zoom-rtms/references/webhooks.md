# RTMS - Webhooks

RTMS-related webhook events and configuration.

## CRITICAL: Respond 200 IMMEDIATELY!

**The #1 cause of random disconnects:**

If your webhook handler takes too long to respond, Zoom assumes failure and retries. The retry creates a second connection, which kicks out your first connection (only 1 connection allowed per stream).

```javascript
// CORRECT: Respond first, process async
app.post('/webhook', (req, res) => {
  res.status(200).send();  // IMMEDIATELY!
  
  // Then process asynchronously
  handleRTMSEvent(req.body);
});

// WRONG: Processing before responding
app.post('/webhook', async (req, res) => {
  await heavyProcessing(req.body);  // Zoom may retry while waiting!
  res.status(200).send();
});
```

## URL Validation Challenge

When configuring your webhook URL, Zoom sends a validation challenge:

```javascript
app.post('/webhook', (req, res) => {
  const { event, payload } = req.body;
  
  // Handle URL validation
  if (event === 'endpoint.url_validation') {
    const hash = crypto
      .createHmac('sha256', process.env.ZOOM_SECRET_TOKEN)
      .update(payload.plainToken)
      .digest('hex');
    
    return res.json({ 
      plainToken: payload.plainToken, 
      encryptedToken: hash 
    });
  }
  
  res.status(200).send();
  // ... handle other events
});
```

## Events

### meeting.rtms_started

Sent when RTMS stream is ready for a meeting.

```json
{
  "event": "meeting.rtms_started",
  "payload": {
    "account_id": "account_id",
    "object": {
      "meeting_id": "meeting_id",
      "meeting_uuid": "meeting_uuid",
      "host_id": "host_user_id",
      "rtms_stream_id": "stream_id",
      "server_urls": "wss://rtms-sjc1.zoom.us/...",
      "signature": "auth_signature"
    }
  }
}
```

### meeting.rtms_stopped

Sent when RTMS stream ends.

```json
{
  "event": "meeting.rtms_stopped",
  "payload": {
    "account_id": "account_id",
    "object": {
      "meeting_id": "meeting_id",
      "rtms_stream_id": "stream_id"
    }
  }
}
```

### Screen Share Events (via msg_type 5)

Subscribe to receive `SHARING_START` and `SHARING_STOP` events when participants start/stop screen sharing.

## Payload Fields

| Field | Description |
|-------|-------------|
| `rtms_stream_id` | Unique stream identifier |
| `server_urls` | WebSocket signaling server URL |
| `meeting_uuid` | Meeting unique identifier (needed for signature) |
| `signature` | Pre-computed auth signature (alternative to self-generating) |

## Server URL Geo-Routing

Server URLs contain airport/region codes:

| Code | Location |
|------|----------|
| `sjc` | San Jose, California |
| `iad` | Washington DC |
| `sin` | Singapore |
| `fra` | Frankfurt, Germany |
| `syd` | Sydney, Australia |

```javascript
// Extract region from server URL
const hostname = new URL(serverUrl).hostname;  // rtms-sjc1.zoom.us
const region = hostname.split('-')[1].replace(/[0-9]/g, '');  // sjc
```

**Tip**: For production, route webhooks to workers in the same region as the Zoom server.

## Subscribing to RTMS Events

### In Zoom Marketplace

1. Go to your app settings
2. Navigate to **Features** → **Access**
3. **Enable Event Subscription**
4. Click **Add Event Subscription**
5. Enter your webhook endpoint URL
6. Search "rtms" and select:
   - `meeting.rtms_started`
   - `meeting.rtms_stopped`
7. Click **Done** then **Save**

### Required Scopes

Add these scopes (Features → Scopes → Add Scopes → search "rtms"):

| Scope | Purpose |
|-------|---------|
| `meeting:read:meeting_audio` | Access meeting audio |
| `meeting:read:meeting_video` | Access meeting video |
| `meeting:read:meeting_transcript` | Access transcripts |
| `meeting:read:meeting_chat` | Access chat messages |

## Products Supporting RTMS

| Product | Webhook Event Prefix |
|---------|---------------------|
| Zoom Meetings | `meeting.rtms_*` |
| Zoom Webinars | `webinar.rtms_*` |
| Zoom Video SDK | `videosdk.rtms_*` |
| Zoom Contact Center | `contactcenter.rtms_*` |
| Zoom Phone | `phone.rtms_*` |

## Resources

- **Event reference**: https://developers.zoom.us/docs/rtms/event-reference/
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

# Setup RTMS Webhook Endpoint

Configure a webhook endpoint to receive RTMS connection details.

## Overview

RTMS sends a webhook when streams are ready. Your endpoint receives connection credentials.

## Skills Needed

- **zoom-rtms** - Primary
- **zoom-webhooks** - Webhook handling

## Webhook Events

| Event | Description |
|-------|-------------|
| `meeting.rtms_started` | Stream ready, contains connection info |
| `meeting.rtms_stopped` | Stream ended |

## Implementation

### JavaScript (Express)

```javascript
const express = require('express');
const crypto = require('crypto');

const app = express();
app.use(express.json());

const ZOOM_WEBHOOK_SECRET = process.env.ZOOM_WEBHOOK_SECRET;

// Webhook signature validation middleware
function validateZoomWebhook(req, res, next) {
  const signature = req.headers['x-zm-signature'];
  const timestamp = req.headers['x-zm-request-timestamp'];
  
  const message = `v0:${timestamp}:${JSON.stringify(req.body)}`;
  const hash = crypto
    .createHmac('sha256', ZOOM_WEBHOOK_SECRET)
    .update(message)
    .digest('hex');
  
  if (`v0=${hash}` !== signature) {
    return res.status(401).send('Invalid signature');
  }
  
  next();
}

app.post('/webhook/zoom', validateZoomWebhook, (req, res) => {
  const { event, payload } = req.body;
  
  // Handle Zoom webhook validation challenge
  if (event === 'endpoint.url_validation') {
    const hashForValidate = crypto
      .createHmac('sha256', ZOOM_WEBHOOK_SECRET)
      .update(payload.plainToken)
      .digest('hex');
    
    return res.json({
      plainToken: payload.plainToken,
      encryptedToken: hashForValidate
    });
  }
  
  // Handle RTMS events
  switch (event) {
    case 'meeting.rtms_started':
      handleRTMSStarted(payload);
      break;
    case 'meeting.rtms_stopped':
      handleRTMSStopped(payload);
      break;
  }
  
  res.status(200).send();
});

function handleRTMSStarted(payload) {
  const {
    meeting_uuid,
    rtms_stream_id,
    server_urls,
    signature
  } = payload.object;
  
  console.log(`RTMS started for meeting: ${meeting_uuid}`);
  
  // Connect to RTMS WebSocket
  connectToRTMS({
    meetingId: meeting_uuid,
    streamId: rtms_stream_id,
    url: server_urls,
    signature: signature
  });
}

function handleRTMSStopped(payload) {
  const { meeting_uuid, rtms_stream_id } = payload.object;
  console.log(`RTMS stopped for meeting: ${meeting_uuid}`);
  
  // Cleanup connection
  disconnectRTMS(meeting_uuid);
}

app.listen(3000, () => {
  console.log('Webhook server running on port 3000');
});
```

### Python (Flask)

```python
from flask import Flask, request, jsonify
import hashlib
import hmac
import os

app = Flask(__name__)
WEBHOOK_SECRET = os.environ.get('ZOOM_WEBHOOK_SECRET')

def validate_webhook(request):
    signature = request.headers.get('x-zm-signature')
    timestamp = request.headers.get('x-zm-request-timestamp')
    
    message = f"v0:{timestamp}:{request.get_data(as_text=True)}"
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return f"v0={expected}" == signature

@app.route('/webhook/zoom', methods=['POST'])
def webhook():
    if not validate_webhook(request):
        return 'Invalid signature', 401
    
    data = request.json
    event = data.get('event')
    payload = data.get('payload')
    
    # Handle validation challenge
    if event == 'endpoint.url_validation':
        plain_token = payload['plainToken']
        encrypted = hmac.new(
            WEBHOOK_SECRET.encode(),
            plain_token.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return jsonify({
            'plainToken': plain_token,
            'encryptedToken': encrypted
        })
    
    # Handle RTMS events
    if event == 'meeting.rtms_started':
        handle_rtms_started(payload)
    elif event == 'meeting.rtms_stopped':
        handle_rtms_stopped(payload)
    
    return '', 200

def handle_rtms_started(payload):
    obj = payload['object']
    print(f"RTMS started: {obj['meeting_uuid']}")
    
    connect_to_rtms(
        meeting_id=obj['meeting_uuid'],
        stream_id=obj['rtms_stream_id'],
        url=obj['server_urls'],
        signature=obj['signature']
    )

def handle_rtms_stopped(payload):
    obj = payload['object']
    print(f"RTMS stopped: {obj['meeting_uuid']}")
    disconnect_rtms(obj['meeting_uuid'])

if __name__ == '__main__':
    app.run(port=3000)
```

## Webhook Payload

```json
{
  "event": "meeting.rtms_started",
  "payload": {
    "account_id": "abc123",
    "object": {
      "meeting_uuid": "meeting-uuid",
      "meeting_id": 123456789,
      "host_id": "host-user-id",
      "rtms_stream_id": "stream-id",
      "server_urls": "wss://rtms.zoom.us/...",
      "signature": "auth-signature"
    }
  }
}
```

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/
- **Webhook docs**: https://developers.zoom.us/docs/api/rest/webhook-reference/

# Validate Webhook Signature

Securely validate incoming Zoom webhooks to prevent spoofing.

## Overview

Zoom signs all webhooks with HMAC-SHA256. Always validate signatures before processing.

## Skills Needed

- **zoom-rtms** - Primary
- **zoom-webhooks** - Webhook security

## Signature Format

```
x-zm-signature: v0=<hmac_sha256_hash>
x-zm-request-timestamp: <unix_timestamp>
```

## Implementation

### JavaScript (Express)

```javascript
const crypto = require('crypto');

const WEBHOOK_SECRET = process.env.ZOOM_WEBHOOK_SECRET;

function validateZoomWebhook(req, res, next) {
  const signature = req.headers['x-zm-signature'];
  const timestamp = req.headers['x-zm-request-timestamp'];
  
  // Check timestamp to prevent replay attacks (5 min window)
  const currentTime = Math.floor(Date.now() / 1000);
  if (Math.abs(currentTime - parseInt(timestamp)) > 300) {
    return res.status(401).json({ error: 'Request timestamp too old' });
  }
  
  // Compute expected signature
  const message = `v0:${timestamp}:${JSON.stringify(req.body)}`;
  const expectedSignature = 'v0=' + crypto
    .createHmac('sha256', WEBHOOK_SECRET)
    .update(message)
    .digest('hex');
  
  // Constant-time comparison to prevent timing attacks
  if (!crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expectedSignature)
  )) {
    return res.status(401).json({ error: 'Invalid signature' });
  }
  
  next();
}

// Apply middleware
app.post('/webhook', validateZoomWebhook, (req, res) => {
  const { event, payload } = req.body;
  
  if (event === 'meeting.rtms_started') {
    // Safe to process - signature validated
    handleRTMSStarted(payload);
  }
  
  res.status(200).send();
});
```

### JavaScript (Raw Body)

```javascript
// For raw body validation (recommended)
const express = require('express');
const crypto = require('crypto');

const app = express();

// Capture raw body for signature validation
app.use('/webhook', express.json({
  verify: (req, res, buf) => {
    req.rawBody = buf.toString();
  }
}));

function validateSignature(req) {
  const signature = req.headers['x-zm-signature'];
  const timestamp = req.headers['x-zm-request-timestamp'];
  
  const message = `v0:${timestamp}:${req.rawBody}`;
  const expected = 'v0=' + crypto
    .createHmac('sha256', WEBHOOK_SECRET)
    .update(message)
    .digest('hex');
  
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expected)
  );
}
```

### Python (Flask)

```python
import hashlib
import hmac
import time
from flask import Flask, request, jsonify

app = Flask(__name__)
WEBHOOK_SECRET = os.environ.get('ZOOM_WEBHOOK_SECRET')

def validate_zoom_webhook():
    signature = request.headers.get('x-zm-signature')
    timestamp = request.headers.get('x-zm-request-timestamp')
    
    if not signature or not timestamp:
        return False
    
    # Check timestamp (5 min window)
    current_time = int(time.time())
    if abs(current_time - int(timestamp)) > 300:
        return False
    
    # Compute expected signature
    message = f"v0:{timestamp}:{request.get_data(as_text=True)}"
    expected = 'v0=' + hmac.new(
        WEBHOOK_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Constant-time comparison
    return hmac.compare_digest(signature, expected)

@app.route('/webhook', methods=['POST'])
def webhook():
    if not validate_zoom_webhook():
        return jsonify({'error': 'Invalid signature'}), 401
    
    data = request.json
    event = data.get('event')
    
    if event == 'meeting.rtms_started':
        handle_rtms_started(data['payload'])
    
    return '', 200
```

### Python (FastAPI)

```python
from fastapi import FastAPI, Request, HTTPException
import hashlib
import hmac

app = FastAPI()

async def validate_webhook(request: Request) -> bool:
    signature = request.headers.get('x-zm-signature')
    timestamp = request.headers.get('x-zm-request-timestamp')
    body = await request.body()
    
    message = f"v0:{timestamp}:{body.decode()}"
    expected = 'v0=' + hmac.new(
        WEBHOOK_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected)

@app.post('/webhook')
async def webhook(request: Request):
    if not await validate_webhook(request):
        raise HTTPException(status_code=401, detail='Invalid signature')
    
    data = await request.json()
    # Process webhook...
    return {'status': 'ok'}
```

## URL Validation Challenge

When setting up webhooks, Zoom sends a validation challenge:

```javascript
app.post('/webhook', (req, res) => {
  const { event, payload } = req.body;
  
  if (event === 'endpoint.url_validation') {
    const hashForValidate = crypto
      .createHmac('sha256', WEBHOOK_SECRET)
      .update(payload.plainToken)
      .digest('hex');
    
    return res.json({
      plainToken: payload.plainToken,
      encryptedToken: hashForValidate
    });
  }
  
  // Handle other events...
});
```

## Security Best Practices

1. **Always validate signatures** - Never skip in production
2. **Check timestamps** - Prevent replay attacks
3. **Use constant-time comparison** - Prevent timing attacks
4. **Store secret securely** - Use environment variables
5. **Log validation failures** - Monitor for attacks

## Resources

- **Webhook security**: https://developers.zoom.us/docs/api/rest/webhook-reference/
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

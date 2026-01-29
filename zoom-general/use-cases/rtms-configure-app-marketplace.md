# Configure RTMS App in Marketplace

Set up your Zoom app with RTMS capabilities in the Marketplace.

## Overview

Enable RTMS features and configure webhooks for your Zoom app to receive real-time media streams.

## Skills Needed

- **zoom-rtms** - Primary

## Setup Steps

### 1. Create or Edit App

1. Go to [Zoom Marketplace](https://marketplace.zoom.us/)
2. Click "Develop" → "Build App"
3. Select app type (Server-to-Server OAuth recommended)
4. Complete app information

### 2. Enable RTMS Feature

1. Navigate to "Features" tab
2. Find "Real-Time Media Streams (RTMS)"
3. Toggle to enable
4. Select required media types:
   - ☑️ Audio stream
   - ☑️ Video stream
   - ☑️ Transcript stream

### 3. Configure Scopes

Required scopes for RTMS:

| Scope | Description |
|-------|-------------|
| `meeting:read:rtms` | Access RTMS for meetings |
| `webinar:read:rtms` | Access RTMS for webinars |

### 4. Set Up Webhooks

1. Go to "Feature" → "Event Subscriptions"
2. Add event subscription
3. Enter your webhook endpoint URL
4. Subscribe to events:
   - `meeting.rtms_started`
   - `meeting.rtms_stopped`

### 5. Configure Webhook Validation

```javascript
// Your webhook endpoint must handle validation
app.post('/webhook', (req, res) => {
  const { event, payload } = req.body;
  
  // Handle URL validation challenge
  if (event === 'endpoint.url_validation') {
    const crypto = require('crypto');
    const hashForValidate = crypto
      .createHmac('sha256', ZOOM_WEBHOOK_SECRET)
      .update(payload.plainToken)
      .digest('hex');
    
    return res.json({
      plainToken: payload.plainToken,
      encryptedToken: hashForValidate
    });
  }
  
  // Handle other events...
  res.status(200).send();
});
```

## App Configuration Checklist

```
☐ App created in Marketplace
☐ RTMS feature enabled
☐ Media types selected (audio/video/transcript)
☐ Required scopes added
☐ Webhook endpoint configured
☐ RTMS events subscribed
☐ Webhook validation implemented
☐ App activated/published
```

## Environment Variables

```bash
# .env
ZOOM_CLIENT_ID=your_client_id
ZOOM_CLIENT_SECRET=your_client_secret
ZOOM_WEBHOOK_SECRET=your_webhook_secret
ZOOM_ACCOUNT_ID=your_account_id  # For Server-to-Server OAuth
```

## Testing

### Local Development

```bash
# Use ngrok for local webhook testing
ngrok http 3000

# Update webhook URL in Marketplace
# https://abc123.ngrok.io/webhook
```

### Verify RTMS is Working

1. Start a meeting as account admin
2. Check webhook endpoint for `meeting.rtms_started`
3. Verify payload contains:
   - `server_urls`
   - `rtms_stream_id`
   - `signature`

## Common Issues

| Issue | Solution |
|-------|----------|
| No webhook received | Check URL is public, verify event subscription |
| 401 on connect | Signature expired, request new via webhook |
| RTMS not available | Feature not enabled or not approved |

## Resources

- **Marketplace**: https://marketplace.zoom.us/
- **RTMS docs**: https://developers.zoom.us/docs/rtms/
- **App creation guide**: https://developers.zoom.us/docs/integrations/create/

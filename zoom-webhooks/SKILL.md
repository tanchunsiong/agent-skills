---
name: zoom-webhooks
description: |
  Zoom webhooks for real-time event notifications. Covers webhook verification, event types,
  and subscription management. Use when you need to receive notifications about meetings,
  users, recordings, or other Zoom events.
---

# Zoom Webhooks

Receive real-time event notifications from Zoom services.

## Prerequisites

- Zoom app with Event Subscriptions enabled
- HTTPS endpoint to receive webhooks
- Webhook secret token for verification

## Quick Start

```javascript
// Express.js webhook handler
const crypto = require('crypto');

app.post('/webhook', (req, res) => {
  // Verify webhook signature
  const signature = req.headers['x-zm-signature'];
  const timestamp = req.headers['x-zm-request-timestamp'];
  const payload = `v0:${timestamp}:${JSON.stringify(req.body)}`;
  const hash = crypto.createHmac('sha256', WEBHOOK_SECRET)
    .update(payload).digest('hex');
  
  if (signature !== `v0=${hash}`) {
    return res.status(401).send('Invalid signature');
  }

  // Handle event
  const { event, payload } = req.body;
  console.log(`Received: ${event}`);
  
  res.status(200).send();
});
```

## Common Events

| Event | Description |
|-------|-------------|
| `meeting.started` | Meeting has started |
| `meeting.ended` | Meeting has ended |
| `meeting.participant_joined` | Participant joined meeting |
| `recording.completed` | Cloud recording ready |
| `user.created` | New user added |

## Detailed References

- **[references/events.md](references/events.md)** - Complete event types reference
- **[references/verification.md](references/verification.md)** - Webhook URL validation
- **[references/subscriptions.md](references/subscriptions.md)** - Event subscriptions API

## Sample Repositories

### Official (by Zoom)

| Type | Repository | Stars |
|------|------------|-------|
| Node.js | [webhook-sample](https://github.com/zoom/webhook-sample) | 34 |
| PostgreSQL | [webhook-to-postgres](https://github.com/zoom/webhook-to-postgres) | 5 |
| Go/Fiber | [Go-Webhooks](https://github.com/zoom/Go-Webhooks) | - |
| Header Auth | [zoom-webhook-verification-headers](https://github.com/zoom/zoom-webhook-verification-headers) | - |

### Community

| Language | Repository | Description |
|----------|------------|-------------|
| Laravel | [binary-cats/laravel-zoom-webhooks](https://github.com/binary-cats/laravel-zoom-webhooks) | Laravel webhook handler |
| AWS Lambda | [splunk/zoom-webhook-to-hec](https://github.com/splunk/zoom-webhook-to-hec) | Serverless to Splunk HEC |
| Node.js | [Will4950/zoom-webhook-listener](https://github.com/Will4950/zoom-webhook-listener) | Webhook forwarder |
| Express+Redis | [ojusave/eventSubscriptionPlayground](https://github.com/ojusave/eventSubscriptionPlayground) | Socket.io + Redis |

### Multi-Language Samples (by tanchunsiong)

| Language | Repository |
|----------|------------|
| Node.js | [Zoom-Webhook-Signature-OAuth-and-REST-API-Development-Sample-In-NodeJS](https://github.com/tanchunsiong/Zoom-Webhook-Signature-OAuth-and-REST-API-Development-Sample-In-NodeJS) |
| C# | [Zoom-Webhook-Signature-OAuth-and-REST-API-Development-Sample-In-ASP.NET-Core-C-](https://github.com/tanchunsiong/Zoom-Webhook-Signature-OAuth-and-REST-API-Development-Sample-In-ASP.NET-Core-C-) |
| Java | [Zoom-Webhook-Signature-OAuth-and-REST-API-Development-Sample-In-Java-Spring-Boot](https://github.com/tanchunsiong/Zoom-Webhook-Signature-OAuth-and-REST-API-Development-Sample-In-Java-Spring-Boot) |
| Python | [Zoom-Webhook-Signature-OAuth-and-REST-API-Development-Sample-In-Python](https://github.com/tanchunsiong/Zoom-Webhook-Signature-OAuth-and-REST-API-Development-Sample-In-Python) |
| PHP | [Zoom-Webhook-Signature-OAuth-and-REST-API-Development-Sample-In-PHP](https://github.com/tanchunsiong/Zoom-Webhook-Signature-OAuth-and-REST-API-Development-Sample-In-PHP) |

**Full list**: See [zoom-platform/references/community-repos.md](../zoom-platform/references/community-repos.md)

## Resources

- **Webhook docs**: https://developers.zoom.us/docs/api/webhooks/
- **Event reference**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/events/
- **Developer forum**: https://devforum.zoom.us/

# Webhooks - Subscriptions

Configure webhook event subscriptions.

## Overview

Subscribe to specific events to receive notifications at your webhook endpoint.

## Configuring Subscriptions

### Via Marketplace Portal

1. Go to your app in [Marketplace](https://marketplace.zoom.us/)
2. Navigate to **Feature** → **Event Subscriptions**
3. Add subscription name and endpoint URL
4. Select events to subscribe to
5. Save and activate

### Subscription Settings

| Setting | Description |
|---------|-------------|
| **Subscription name** | Identifier for this subscription |
| **Event notification endpoint URL** | Your HTTPS endpoint |
| **Events** | Select which events to receive |

## Event Categories

### Meeting Events
- Meeting lifecycle (created, started, ended)
- Participant events (joined, left)
- Sharing events

### Recording Events
- Recording lifecycle (started, stopped, completed)
- Useful for BYOS and processing pipelines

### User Events
- User lifecycle (created, updated, deleted)

### Webinar Events
- Webinar lifecycle and participant events

## Multiple Subscriptions

You can create multiple subscriptions to:
- Send different events to different endpoints
- Separate production and development endpoints
- Organize by event type

## Testing Webhooks

1. Use tools like ngrok for local development
2. Check webhook logs in Marketplace portal
3. Verify signature handling

## Resources

- **Webhooks docs**: https://developers.zoom.us/docs/api/rest/webhook-reference/

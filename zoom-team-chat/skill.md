---
name: zoom-team-chat
description: "Zoom Team Chat - Build messaging integrations, chatbots with rich cards/buttons, and apps. Covers Team Chat API (user-level messaging) and Chatbot API (bot-level interactions with webhooks)."
triggers:
  - "zoom team chat"
  - "zoom chatbot"
  - "zoom messaging"
  - "team chat api"
  - "chatbot api"
  - "zoom slash commands"
  - "zoom chat integration"
---

# Zoom Team Chat Development

Build powerful messaging integrations and interactive chatbots for Zoom Team Chat. This skill covers **two distinct APIs** - make sure to choose the right one for your use case.

**Official Documentation**: https://developers.zoom.us/docs/zoom-team-chat/  
**Chatbot Documentation**: https://developers.zoom.us/docs/zoom-team-chat/chatbot/extend/  
**API Reference**: https://developers.zoom.us/docs/api/rest/reference/chatbot/

## Quick Links

**New to Team Chat? Follow this path:**

1. **[Choose Your API](concepts/api-selection.md)** - Team Chat API vs Chatbot API
2. **[Environment Setup](concepts/environment-setup.md)** - Credentials, scopes, app configuration
3. **[OAuth Setup](examples/oauth-setup.md)** - Complete authentication flow
4. **[Send First Message](examples/send-message.md)** - Working code to send messages

**Reference:**
- **[Chatbot Message Cards](references/message-cards.md)** - Complete card component reference
- **[Webhook Events](references/webhook-events.md)** - All webhook event types
- **[API Reference](references/api-reference.md)** - Endpoints, methods, parameters
- **[Sample Applications](references/samples.md)** - 10+ official sample apps
- **[INDEX.md](INDEX.md)** - Complete documentation navigation

**Having issues?**
- Authentication errors → [OAuth Troubleshooting](troubleshooting/oauth-issues.md)
- Webhook not receiving events → [Webhook Setup Guide](troubleshooting/webhook-issues.md)
- Messages not sending → [Common Issues](troubleshooting/common-issues.md)

**Building Interactive Bots?**
- [Button Actions](examples/button-actions.md) - Handle button clicks
- [Form Submissions](examples/form-submissions.md) - Process form data
- [Slash Commands](examples/slash-commands.md) - Create custom commands

## Quick Decision: Which API?

| Use Case | API to Use |
|----------|------------|
| Send notifications from scripts/CI/CD | **Team Chat API** |
| Automate messages as a user | **Team Chat API** |
| Build an interactive chatbot | **Chatbot API** |
| Respond to slash commands | **Chatbot API** |
| Create messages with buttons/forms | **Chatbot API** |
| Handle user interactions | **Chatbot API** |

### Team Chat API (User-Level)
- Messages appear as sent by **authenticated user**
- Requires **User OAuth** (authorization_code flow)
- Endpoint: `POST https://api.zoom.us/v2/chat/users/me/messages`
- Scopes: `chat_message:write`, `chat_channel:read`

### Chatbot API (Bot-Level)
- Messages appear as sent by your **bot**
- Requires **Client Credentials** grant
- Endpoint: `POST https://api.zoom.us/v2/im/chat/messages`
- Scopes: `imchat:bot` (auto-added)
- **Rich cards**: buttons, forms, dropdowns, images

## Prerequisites

### System Requirements

- Zoom account
- Account owner, admin, or **Zoom for developers** role enabled
  - To enable: **User Management** → **Roles** → **Role Settings** → **Advanced features** → Enable **Zoom for developers**

### Create Zoom App

1. Go to [Zoom App Marketplace](https://marketplace.zoom.us/)
2. Click **Develop** → **Build App**
3. Select **General App** (OAuth)

> ⚠️ **Do NOT use Server-to-Server OAuth** - S2S apps don't have the Chatbot/Team Chat feature. Only General App (OAuth) supports chatbots.

### Required Credentials

From Zoom Marketplace → Your App:

| Credential | Location | Used By |
|------------|----------|---------|
| Client ID | App Credentials → Development | Both APIs |
| Client Secret | App Credentials → Development | Both APIs |
| Account ID | App Credentials → Development | Chatbot API |
| Bot JID | Features → Chatbot → Bot Credentials | Chatbot API |
| Secret Token | Features → Team Chat Subscriptions | Chatbot API |

**See**: [Environment Setup Guide](concepts/environment-setup.md) for complete configuration steps.

## Quick Start: Team Chat API

Send a message as a user:

```javascript
// 1. Get access token via OAuth
const accessToken = await getOAuthToken(); // See examples/oauth-setup.md

// 2. Send message to channel
const response = await fetch('https://api.zoom.us/v2/chat/users/me/messages', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: 'Hello from CI/CD pipeline!',
    to_channel: 'CHANNEL_ID'
  })
});

const data = await response.json();
// { "id": "msg_abc123", "date_time": "2024-01-15T10:30:00Z" }
```

**Complete example**: [Send Message Guide](examples/send-message.md)

## Quick Start: Chatbot API

Build an interactive chatbot:

```javascript
// 1. Get chatbot token (client_credentials)
async function getChatbotToken() {
  const credentials = Buffer.from(
    `${CLIENT_ID}:${CLIENT_SECRET}`
  ).toString('base64');
  
  const response = await fetch('https://zoom.us/zoom-oauth/token', {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${credentials}`,
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: 'grant_type=client_credentials'
  });
  
  return (await response.json()).access_token;
}

// 2. Send chatbot message with buttons
const response = await fetch('https://api.zoom.us/v2/im/chat/messages', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    robot_jid: process.env.ZOOM_BOT_JID,
    to_jid: payload.toJid,           // From webhook
    account_id: payload.accountId,   // From webhook
    content: {
      head: {
        text: 'Build Notification',
        sub_head: { text: 'CI/CD Pipeline' }
      },
      body: [
        { type: 'message', text: 'Deployment successful!' },
        {
          type: 'fields',
          items: [
            { key: 'Branch', value: 'main' },
            { key: 'Commit', value: 'abc123' }
          ]
        },
        {
          type: 'actions',
          items: [
            { text: 'View Logs', value: 'view_logs', style: 'Primary' },
            { text: 'Dismiss', value: 'dismiss', style: 'Default' }
          ]
        }
      ]
    }
  })
});
```

**Complete example**: [Chatbot Setup Guide](examples/chatbot-setup.md)

## Key Features

### Team Chat API

| Feature | Description |
|---------|-------------|
| **Send Messages** | Post messages to channels or direct messages |
| **List Channels** | Get user's channels with metadata |
| **Create Channels** | Create public/private channels programmatically |
| **Threaded Replies** | Reply to specific messages in threads |
| **Edit/Delete** | Modify or remove messages |

### Chatbot API

| Feature | Description |
|---------|-------------|
| **Rich Message Cards** | Headers, images, fields, buttons, forms |
| **Slash Commands** | Custom `/commands` trigger webhooks |
| **Button Actions** | Interactive buttons with webhook callbacks |
| **Form Submissions** | Collect user input with forms |
| **Dropdown Selects** | Channel, member, date/time pickers |
| **LLM Integration** | Easy integration with Claude, GPT, etc. |

## Webhook Events (Chatbot API)

| Event | Trigger | Use Case |
|-------|---------|----------|
| `bot_notification` | User messages bot or uses slash command | Process commands, integrate LLM |
| `bot_installed` | Bot added to account | Initialize bot state |
| `interactive_message_actions` | Button clicked | Handle button actions |
| `chat_message.submit` | Form submitted | Process form data |
| `app_deauthorized` | Bot removed | Cleanup |

**See**: [Webhook Events Reference](references/webhook-events.md)

## Message Card Components

Build rich interactive messages with these components:

| Component | Description |
|-----------|-------------|
| **header** | Title and subtitle |
| **message** | Plain text |
| **fields** | Key-value pairs |
| **actions** | Buttons (Primary, Danger, Default styles) |
| **section** | Colored sidebar grouping |
| **attachments** | Images with links |
| **divider** | Horizontal line |
| **form_field** | Text input |
| **dropdown** | Select menu |
| **date_picker** | Date selection |

**See**: [Message Cards Reference](references/message-cards.md) for complete component catalog

## Architecture Patterns

### Chatbot Lifecycle

```
User types /command → Webhook receives bot_notification
                            ↓
                     payload.cmd = "user's input"
                            ↓
                     Process command
                            ↓
                     Send response via sendChatbotMessage()
```

### LLM Integration Pattern

```javascript
case 'bot_notification': {
  const { toJid, cmd, accountId } = payload;
  
  // 1. Call your LLM
  const llmResponse = await callClaude(cmd);
  
  // 2. Send response back
  await sendChatbotMessage(toJid, accountId, {
    body: [{ type: 'message', text: llmResponse }]
  });
}
```

**See**: [LLM Integration Guide](examples/llm-integration.md)

## Sample Applications

| Sample | Description | Link |
|--------|-------------|------|
| **Chatbot Quickstart** | Official tutorial (recommended start) | [GitHub](https://github.com/zoom/chatbot-nodejs-quickstart) |
| **Claude Chatbot** | AI chatbot with Anthropic Claude | [GitHub](https://github.com/zoom/zoom-chatbot-claude-sample) |
| **Unsplash Chatbot** | Image search with database | [GitHub](https://github.com/zoom/unsplash-chatbot) |
| **ERP Chatbot** | Oracle ERP with scheduled alerts | [GitHub](https://github.com/zoom/zoom-erp-chatbot-sample) |
| **Task Manager** | Full CRUD app | [GitHub](https://github.com/zoom/task-manager-sample) |

**See**: [Sample Applications Guide](references/samples.md) for analysis of all 10 samples

## Common Operations

### Send Message to Channel

```javascript
// Team Chat API
await fetch('https://api.zoom.us/v2/chat/users/me/messages', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` },
  body: JSON.stringify({
    message: 'Hello!',
    to_channel: 'CHANNEL_ID'
  })
});
```

### Handle Button Click

```javascript
// Webhook handler
case 'interactive_message_actions': {
  const { actionItem, toJid, accountId } = payload;
  
  if (actionItem.value === 'approve') {
    await sendChatbotMessage(toJid, accountId, {
      body: [{ type: 'message', text: '✅ Approved!' }]
    });
  }
}
```

### Verify Webhook Signature

```javascript
function verifyWebhook(req) {
  const message = `v0:${req.headers['x-zm-request-timestamp']}:${JSON.stringify(req.body)}`;
  const hash = crypto.createHmac('sha256', process.env.ZOOM_VERIFICATION_TOKEN)
    .update(message)
    .digest('hex');
  return req.headers['x-zm-signature'] === `v0=${hash}`;
}
```

## Deployment

### ngrok for Local Development

```bash
# Install ngrok
npm install -g ngrok

# Expose local server
ngrok http 4000

# Use HTTPS URL as Bot Endpoint URL in Zoom Marketplace
# Example: https://abc123.ngrok.io/webhook
```

### Production Deployment

**See**: [Deployment Guide](concepts/deployment.md) for:
- Nginx reverse proxy setup
- Base path configuration
- OAuth redirect URI setup

## Limitations

| Limit | Value |
|-------|-------|
| Message length | 4,096 characters |
| File size | 512 MB |
| Members per channel | 10,000 |
| Channels per user | 500 |

## Security Best Practices

1. **Verify webhook signatures** - Always validate using `x-zm-signature` header
2. **Sanitize messages** - Limit to 4096 chars, remove control characters
3. **Validate JIDs** - Check format: `user@domain` or `channel@domain`
4. **Environment variables** - Never hardcode credentials
5. **Use HTTPS** - Required for production webhooks

**See**: [Security Best Practices](concepts/security.md)

## Complete Documentation Library

### Core Concepts (Start Here!)
- **[API Selection Guide](concepts/api-selection.md)** - Choose Team Chat API vs Chatbot API
- **[Environment Setup](concepts/environment-setup.md)** - Complete credentials guide
- **[Authentication Flows](concepts/authentication.md)** - OAuth vs Client Credentials
- **[Webhook Architecture](concepts/webhooks.md)** - How webhooks work
- **[Message Card Structure](concepts/message-structure.md)** - Card component hierarchy

### Complete Examples
- **[OAuth Setup](examples/oauth-setup.md)** - Full OAuth implementation
- **[Send Message](examples/send-message.md)** - Team Chat API message sending
- **[Chatbot Setup](examples/chatbot-setup.md)** - Complete chatbot with webhooks
- **[Button Actions](examples/button-actions.md)** - Handle interactive buttons
- **[Form Submissions](examples/form-submissions.md)** - Process form data
- **[Slash Commands](examples/slash-commands.md)** - Create custom commands
- **[LLM Integration](examples/llm-integration.md)** - Claude/GPT integration
- **[Scheduled Alerts](examples/scheduled-alerts.md)** - Cron + incoming webhooks
- **[Channel Management](examples/channel-management.md)** - Create/manage channels

### References
- **[API Reference](references/api-reference.md)** - All endpoints and methods
- **[Webhook Events](references/webhook-events.md)** - Complete event reference
- **[Message Cards](references/message-cards.md)** - All card components
- **[Sample Applications](references/samples.md)** - Analysis of 10 official samples
- **[Error Codes](references/error-codes.md)** - Error handling guide

### Troubleshooting
- **[OAuth Issues](troubleshooting/oauth-issues.md)** - Authentication failures
- **[Webhook Issues](troubleshooting/webhook-issues.md)** - Webhook debugging
- **[Common Issues](troubleshooting/common-issues.md)** - Quick diagnostics

## Resources

- **Official Docs**: https://developers.zoom.us/docs/zoom-team-chat/
- **API Reference**: https://developers.zoom.us/docs/api/rest/reference/chatbot/
- **Dev Forum**: https://devforum.zoom.us/
- **App Marketplace**: https://marketplace.zoom.us/

---

**Need help?** Start with [INDEX.md](INDEX.md) for complete navigation.

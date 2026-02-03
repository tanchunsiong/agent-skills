---
name: zoom-team-chat
description: |
  Zoom Team Chat integration guide covering TWO distinct APIs:
  1. Team Chat API - Send messages as a USER to channels/contacts
  2. Chatbot API - Build interactive BOTS with rich cards and buttons
  Interview the user to determine which API fits their use case before proceeding.
---

# Zoom Team Chat Integration

Build messaging integrations with Zoom Team Chat. This skill covers two distinct APIs - make sure to identify which one fits your use case.

## Choose Your API (IMPORTANT)

**Ask the user**: What do you want to build?

| Use Case | API to Use |
|----------|------------|
| Send notifications from scripts/CI/CD | **Team Chat API** |
| Automate messages as a user | **Team Chat API** |
| Build an interactive chatbot | **Chatbot API** |
| Respond to slash commands | **Chatbot API** |
| Create messages with buttons/forms | **Chatbot API** |
| Handle user interactions | **Chatbot API** |

### Quick Decision

- **"I want to send simple messages programmatically"** → Team Chat API (Section A)
- **"I want to build a bot that users interact with"** → Chatbot API (Section B)

---

# Environment Setup

## Prerequisites

- Zoom account
- Account owner, admin, or **Zoom for developers** role enabled
  - To enable: **User Management** → **Roles** → **Role Settings** → **Advanced features** → Enable **Zoom for developers**

## Step 1: Create Zoom App

1. Go to [Zoom App Marketplace](https://marketplace.zoom.us/)
2. Click **Develop** → **Build App**
3. Select **General App** (OAuth)

> ⚠️ **Do NOT use Server-to-Server OAuth** - S2S apps don't have the Chatbot/Team Chat feature. Only General App (OAuth) supports chatbots.

## Step 2: Basic Information

On the **Basic Info** page:

1. **App Name**: Update the auto-generated name
2. **App Management Type**:
   - **Admin-managed**: App manages data for all users on account (recommended for chatbots)
   - **User-managed**: App only accesses individual user's data
3. **App Credentials**: Auto-generated Client ID & Client Secret
4. **OAuth Information**:
   - **OAuth redirect URL**: Your callback endpoint (e.g., `http://localhost:4000/auth/callback`)
   - **OAuth allow lists**: Add allowed redirect URLs

## Step 3: Enable Team Chat Surface (Chatbot Only)

On the **Features** page → **Surface** tab:

1. In **Select where to use your app**, check **Team Chat**
2. Enter **Home URL**: Your app's home page
3. Enter **Domain Allow List**: URLs the Zoom client should accept
4. Enable **Team Chat Subscription**:
   - **Slash Command**: e.g., `/mybot`
   - **Bot Endpoint URL**: Your webhook endpoint (e.g., `https://your-domain.com/webhook`)

> **Important**: Your bot will NOT appear in Team Chat unless you enable it in the Surface section!

## Step 4: Get Credentials

### App Credentials Page

Navigate to **App Credentials** → **Development**:

| Credential | Location |
|------------|----------|
| Client ID | App Credentials → Development |
| Client Secret | App Credentials → Development |
| Account ID | App Credentials → Development |

### Bot JID (Chatbot API Only)

> **Important**: Bot JID only appears after enabling the Chatbot feature!

1. Go to **Features** tab in left sidebar
2. Ensure **Chatbot** toggle is **ON**
3. Click **Chatbot** section to expand
4. Scroll to **Bot Credentials** (or "Chatbot Information")
5. You'll see two JIDs:
   - **Bot JID (Development)**: Use for testing
   - **Bot JID (Production)**: Use for live/distributed apps

Format: `v1abc123xyz@xmpp.zoom.us`

### Webhook Secret Token (Chatbot API Only)

Navigate to **Features** → **Team Chat Subscriptions** → **Secret Token**

| Credential | Location | Used By |
|------------|----------|---------|
| Client ID | App Credentials → Development | Both APIs |
| Client Secret | App Credentials → Development | Both APIs |
| Account ID | App Credentials → Development | Chatbot API |
| Bot JID | Features → Chatbot → Bot Credentials | Chatbot API |
| Secret Token | Features → Team Chat Subscriptions | Chatbot API |

## Step 5: Create .env File

```bash
# Copy the template
cp .env.example .env
```

### For Team Chat API (User-Level)

```bash
# .env file
ZOOM_CLIENT_ID=your_client_id_here
ZOOM_CLIENT_SECRET=your_client_secret_here
ZOOM_REDIRECT_URI=http://localhost:4000/auth/callback

PORT=4000
```

### For Chatbot API (Bot-Level)

```bash
# .env file
ZOOM_CLIENT_ID=your_client_id_here
ZOOM_CLIENT_SECRET=your_client_secret_here
ZOOM_BOT_JID=v1abc123xyz@xmpp.zoom.us
ZOOM_VERIFICATION_TOKEN=your_webhook_secret_token
ZOOM_ACCOUNT_ID=your_account_id

PORT=4000
```

## Step 6: Add Scopes

In your app's **Scopes** section:

### Team Chat API Scopes
- `chat_message:write`
- `chat_message:read`
- `chat_channel:read`
- `chat_channel:write`

### Chatbot API Scopes (Auto-added when Team Chat enabled)
- `imchat:bot` (automatically added)
- `team_chat:read:list_user_channels:admin`
- `team_chat:read:list_members:admin`

## Step 7: Test Your App

On the **Local Test** page:

1. Click **Add App Now** → **Allow** to add the app to your account
2. Click **Preview Your App Listing Page** to see how it will appear
3. To share with others on your account: Generate an **Authorization URL**

---

# Section A: Team Chat API (User-Level)

Send messages as a **user account** to channels or contacts. Messages appear as if sent by the authenticated user.

## Endpoint

```
POST https://api.zoom.us/v2/chat/users/me/messages
```

## Authentication

Requires **User OAuth** (authorization_code flow):

```javascript
// 1. Redirect user to authorize
const authUrl = `https://zoom.us/oauth/authorize?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}`;

// 2. Exchange code for token
const tokenResponse = await fetch('https://zoom.us/oauth/token', {
  method: 'POST',
  headers: {
    'Authorization': `Basic ${Buffer.from(`${CLIENT_ID}:${CLIENT_SECRET}`).toString('base64')}`,
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  body: `grant_type=authorization_code&code=${code}&redirect_uri=${REDIRECT_URI}`
});
```

## Required Scopes

| Scope | Purpose |
|-------|---------|
| `chat_message:write` | Send messages |
| `chat_message:read` | Read messages |
| `chat_channel:read` | List channels |
| `chat_channel:write` | Create/manage channels |

## Send Message to Channel

```javascript
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

## Send Message to Contact

```javascript
const response = await fetch('https://api.zoom.us/v2/chat/users/me/messages', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: 'Hello!',
    to_contact: 'user@example.com'
  })
});
```

## Reply to Thread

```javascript
const response = await fetch('https://api.zoom.us/v2/chat/users/me/messages', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: 'This is a reply',
    to_channel: 'CHANNEL_ID',
    reply_to: 'PARENT_MESSAGE_ID'
  })
});
```

## List User's Channels

```javascript
const response = await fetch('https://api.zoom.us/v2/chat/users/me/channels', {
  headers: { 'Authorization': `Bearer ${accessToken}` }
});

const data = await response.json();
// { "channels": [{ "id": "...", "name": "...", "type": 1 }] }
```

## Channel Types

| Type | Value | Description |
|------|-------|-------------|
| Private | 1 | Invite-only |
| Public | 2 | Anyone can join |
| DM | 3 | Direct message |
| Group | 4 | Group chat |

---

# Section B: Chatbot API (Bot-Level)

Build interactive chatbots with rich cards, buttons, and slash commands. Messages appear as sent by your **bot**.

## Endpoint

```
POST https://api.zoom.us/v2/im/chat/messages
```

## Authentication

Uses **Client Credentials** grant to get access tokens (no user login required):

> **Note**: This uses a **General App (OAuth)** with Team Chat enabled - NOT a Server-to-Server OAuth app. S2S apps don't support chatbots.

```javascript
async function getAccessToken() {
  const credentials = Buffer.from(`${CLIENT_ID}:${CLIENT_SECRET}`).toString('base64');
  
  const response = await fetch('https://zoom.us/oauth/token', {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${credentials}`,
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: 'grant_type=client_credentials'
  });
  
  return (await response.json()).access_token;
}
```

## Required Credentials

From [Zoom App Marketplace](https://marketplace.zoom.us/):

```bash
ZOOM_CLIENT_ID=xxx
ZOOM_CLIENT_SECRET=xxx
ZOOM_BOT_JID=xxx                    # Your bot's JID
ZOOM_VERIFICATION_TOKEN=xxx       # For webhook verification
ACCOUNT_ID=xxx
```

## Required Scopes

| Scope | Purpose |
|-------|---------|
| `imchat:bot` | Basic chatbot functionality |
| `team_chat:read:list_user_channels:admin` | List channels |
| `team_chat:read:list_members:admin` | List members |

## Send Chatbot Message

```javascript
const response = await fetch('https://api.zoom.us/v2/im/chat/messages', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    robot_jid: process.env.ZOOM_BOT_JID,
    to_jid: payload.toJid,           // From webhook payload
    account_id: payload.accountId,   // From webhook payload
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

## App Card Message Format

```javascript
{
  content: {
    head: {
      text: "Title",
      sub_head: { text: "Subtitle" },
      style: { bold: true }
    },
    body: [
      // Message text
      { type: "message", text: "Hello world!" },
      
      // Colored section
      {
        type: "section",
        sidebar_color: "#8b5cf6",
        sections: [{ type: "message", text: "Section content" }]
      },
      
      // Key-value fields
      {
        type: "fields",
        items: [
          { key: "Status", value: "Active" },
          { key: "Priority", value: "High" }
        ]
      },
      
      // Action buttons
      {
        type: "actions",
        items: [
          { text: "Approve", value: "approve", style: "Primary" },
          { text: "Reject", value: "reject", style: "Danger" }
        ]
      },
      
      // Horizontal divider
      { type: "divider" },
      
      // Image attachment
      {
        type: "attachments",
        img_url: "https://example.com/image.png",
        resource_url: "https://example.com",
        information: {
          title: { text: "Image Title" },
          description: { text: "Click to view" }
        }
      }
    ]
  }
}
```

## Webhook Setup

### 1. Verify Webhook Signature

```javascript
const crypto = require('crypto');

function verifyWebhook(req) {
  const message = `v0:${req.headers['x-zm-request-timestamp']}:${JSON.stringify(req.body)}`;
  const hash = crypto.createHmac('sha256', process.env.ZOOM_VERIFICATION_TOKEN)
    .update(message)
    .digest('hex');
  return req.headers['x-zm-signature'] === `v0=${hash}`;
}
```

### 2. Handle Webhook Events

```javascript
app.post('/webhook', (req, res) => {
  if (!verifyWebhook(req)) {
    return res.status(401).json({ error: 'Invalid signature' });
  }
  
  const { event, payload } = req.body;
  
  switch (event) {
    case 'endpoint.url_validation':
      // Zoom verifying your endpoint
      return res.json({
        message: {
          plainToken: payload.plainToken,
          encryptedToken: crypto.createHmac('sha256', process.env.ZOOM_VERIFICATION_TOKEN)
            .update(payload.plainToken)
            .digest('hex')
        }
      });
      
    case 'bot_installed':
      console.log('Bot installed!');
      break;
      
    case 'bot_notification':
      // User sent a message to the bot
      const { toJid, cmd, userName, accountId } = payload;
      await sendChatbotMessage(toJid, `You said: ${cmd}`, accountId);
      break;
      
    case 'interactive_message_actions':
      // User clicked a button
      const action = payload.actionItem?.value;
      console.log(`User clicked: ${action}`);
      break;
      
    case 'app_deauthorized':
      console.log('Bot uninstalled');
      break;
  }
  
  res.status(200).json({ success: true });
});
```

## Webhook Events

| Event | Trigger | Payload Fields |
|-------|---------|----------------|
| `bot_notification` | User messages bot | `toJid`, `cmd`, `userName`, `accountId` |
| `bot_installed` | Bot added | `accountId` |
| `interactive_message_actions` | Button clicked | `actionItem`, `messageId` |
| `chat_message.submit` | Form submitted | Form field values |
| `app_deauthorized` | Bot removed | `account_id` |
| `endpoint.url_validation` | Setup verification | `plainToken` |

## Handling Button Clicks (interactive_message_actions)

When users click action buttons in your bot messages:

```javascript
case 'interactive_message_actions': {
  const { toJid, accountId } = payload;
  const action = payload.actionItem?.value;  // The button's value
  
  switch (action) {
    case 'approve':
      await sendChatbotMessage(toJid, accountId, {
        body: [{ type: 'message', text: '✅ Approved!' }]
      });
      break;
    case 'reject':
      await sendChatbotMessage(toJid, accountId, {
        body: [{ type: 'message', text: '❌ Rejected' }]
      });
      break;
  }
  break;
}
```

## Displaying Images and Attachments

Use `attachments` inside a `section` for images with links:

```javascript
{
  type: 'section',
  sidebar_color: '#3b82f6',  // Blue sidebar
  sections: [
    {
      type: 'attachments',
      img_url: 'https://example.com/photo.jpg',
      resource_url: 'https://example.com/full-photo',
      information: {
        title: { text: 'Photo by John Doe' },
        description: { text: 'Click to view on website' }
      }
    }
  ]
}
```

## Error Display Pattern

Use red sidebar color for error messages:

```javascript
// Success message
{
  type: 'section',
  sidebar_color: '#10b981',  // Green
  sections: [{ type: 'message', text: 'Operation successful!' }]
}

// Error message  
{
  type: 'section',
  sidebar_color: '#ef4444',  // Red
  sections: [{ type: 'message', text: 'Error: Something went wrong' }]
}
```

## Incoming Webhooks (Scheduled Alerts)

For sending scheduled alerts without user interaction, use Zoom's Incoming Webhook:

1. **Add Incoming Webhook app** to your Zoom account
2. **Create connection**: Type `/inc connect` in Team Chat
3. **Get endpoint URL and verification token**
4. **Send POST requests** to trigger alerts:

```javascript
// Send scheduled alert via Incoming Webhook
async function sendScheduledAlert(webhookUrl, verificationToken, message) {
  await fetch(webhookUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': verificationToken
    },
    body: JSON.stringify({
      head: { text: 'Scheduled Alert' },
      body: [{ type: 'message', text: message }]
    })
  });
}

// Schedule with cron
const cron = require('node-cron');
cron.schedule('0 9 * * *', () => {  // Every day at 9 AM
  sendScheduledAlert(WEBHOOK_URL, TOKEN, 'Daily report ready!');
});
```

## Integrating LLMs (Claude, GPT, etc.)

To add AI capabilities to your chatbot, integrate an LLM in the `bot_notification` handler:

```
User sends message → Webhook receives bot_notification
                            ↓
                     payload.cmd = "user's question"
                            ↓
                     ┌─────────────────────┐
                     │  CALL LLM HERE      │  ← Integration point
                     │  (Claude, GPT, etc) │
                     └─────────────────────┘
                            ↓
                     Send LLM response back via sendChatbotMessage()
```

### Code Example

```javascript
case 'bot_notification': {
  const { toJid, cmd, userName, accountId } = payload;
  
  // 1. Call your LLM with user's message (cmd)
  const llmResponse = await callLLM(cmd);
  
  // 2. Send LLM response back to Zoom
  await sendChatbotMessage(toJid, accountId, {
    head: { text: 'AI Response' },
    body: [{ type: 'message', text: llmResponse }]
  });
  break;
}
```

### Example: Claude Integration

```javascript
const Anthropic = require('@anthropic-ai/sdk');
const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

async function callLLM(userMessage) {
  const response = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    messages: [{ role: 'user', content: userMessage }]
  });
  return response.content[0].text;
}
```

### Example: OpenAI Integration

```javascript
const OpenAI = require('openai');
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function callLLM(userMessage) {
  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [{ role: 'user', content: userMessage }]
  });
  return response.choices[0].message.content;
}
```

### Conversation History (Optional)

To maintain context across messages:

```javascript
const conversationHistory = {}; // Store per user

case 'bot_notification': {
  const { toJid, cmd, accountId } = payload;
  
  // Initialize or get history
  if (!conversationHistory[toJid]) {
    conversationHistory[toJid] = [];
  }
  
  // Add user message
  conversationHistory[toJid].push({ role: 'user', content: cmd });
  
  // Call LLM with full history
  const llmResponse = await callLLMWithHistory(conversationHistory[toJid]);
  
  // Add assistant response to history
  conversationHistory[toJid].push({ role: 'assistant', content: llmResponse });
  
  // Send response
  await sendChatbotMessage(toJid, accountId, {
    body: [{ type: 'message', text: llmResponse }]
  });
}
```

## Local Development with ngrok

```bash
# Install ngrok
npm install -g ngrok

# Expose local server
ngrok http 4000

# Use the HTTPS URL as your Bot Endpoint URL in Zoom Marketplace
# Example: https://abc123.ngrok.io/webhook
```

## Chatbot Setup Checklist

### 1. App Type (IMPORTANT)

| App Type | Chatbot Support |
|----------|-----------------|
| **General App (OAuth)** | ✅ Yes - has Team Chat/Chatbot feature |
| Server-to-Server OAuth | ❌ No - does NOT support chatbots |

### 2. App Management Type

| Type | Use Case | Token Flow |
|------|----------|------------|
| **Admin-managed** | Company-wide bots (notifications, helpdesk) | client_credentials |
| User-managed | Personal bots (individual user only) | authorization_code |

**Most chatbots use Admin-managed** - installed once by admin, available to all users.

### 3. Required Credentials

| Credential | Required | Where to Find |
|------------|----------|---------------|
| Client ID | ✅ Yes | App Credentials page |
| Client Secret | ✅ Yes | App Credentials page |
| Account ID | ✅ Yes | App Credentials page |
| Bot JID | ✅ Yes | Features → Chatbot → Bot Credentials |
| Webhook Secret Token | Optional | Features → Team Chat Subscriptions |

### 4. Scopes

For basic chatbot functionality, only **`imchat:bot`** is needed.

This scope is **automatically added** when you create a slash command in Team Chat Subscriptions.

### 5. OAuth Redirect URL

**Not used** by chatbots (client_credentials doesn't need user login), but Zoom may require you to fill it in. Enter any valid URL you control.

### 6. Team Chat Subscription Setup

In Zoom Marketplace → Features → Team Chat Subscriptions:

| Field | Value |
|-------|-------|
| Bot Endpoint URL | `https://yourdomain.com/webhook` |
| Slash Command | `/yourbot` (what users type) |

### 7. Testing the Webhook

```bash
# ❌ GET request (browser) - returns "Cannot GET /webhook"
curl https://yourdomain.com/webhook

# ✅ POST request - returns "Invalid signature" (expected without valid Zoom signature)
curl -X POST https://yourdomain.com/webhook \
  -H "Content-Type: application/json" \
  -d '{"event":"test"}'
```

**"Invalid signature" = webhook is working correctly** (rejecting unsigned requests)

### 8. Verification Flow

When you save the Bot Endpoint URL, Zoom sends a validation request:

```json
{
  "event": "endpoint.url_validation",
  "payload": { "plainToken": "xyz123" }
}
```

Your server must respond with:

```json
{
  "plainToken": "xyz123",
  "encryptedToken": "hmac_sha256(plainToken, webhook_secret)"
}
```

### 9. Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Cannot GET /webhook" | Browser sends GET, webhook is POST-only | Normal - test with POST or use Zoom |
| "Invalid signature" | Request not signed by Zoom | Normal for manual tests; real Zoom requests will work |
| Bot JID not found | Team Chat not enabled | Enable in Features → Surface → Team Chat |
| Token error | Wrong credentials | Verify Client ID/Secret match your app |
| Messages not sending | Missing Account ID or Bot JID | Check `.env` has all required values |

---

# Common Operations (Both APIs)

## List Messages

```javascript
// Team Chat API
const response = await fetch(
  `https://api.zoom.us/v2/chat/users/me/messages?to_channel=${channelId}&from=2024-01-01&to=2024-01-31`,
  { headers: { 'Authorization': `Bearer ${accessToken}` } }
);
```

## Create Channel

```javascript
const response = await fetch('https://api.zoom.us/v2/chat/users/me/channels', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Project Alpha',
    type: 1,  // 1=private, 2=public
    members: [
      { email: 'user1@example.com' },
      { email: 'user2@example.com' }
    ]
  })
});
```

## Add Members to Channel

```javascript
const response = await fetch(
  `https://api.zoom.us/v2/chat/channels/${channelId}/members`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      members: [{ email: 'newuser@example.com' }]
    })
  }
);
```

## Threaded Replies

Use `reply_to` parameter to create threaded conversations:

```javascript
const body = {
  robot_jid: process.env.ZOOM_BOT_JID,
  to_jid: toJid,
  account_id: process.env.ACCOUNT_ID,
  content: {
    body: [{ type: 'message', text: 'This is a reply in the thread' }]
  },
  reply_to: 'original_message_id'  // Creates a thread under this message
};

await fetch('https://api.zoom.us/v2/im/chat/messages', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(body)
});
```

---

# Security Best Practices

## Message Sanitization

```javascript
// Zoom message limit is 4096 characters
function sanitizeMessage(message) {
  if (typeof message !== 'string') return '';
  return message
    .trim()
    .replace(/[\x00-\x1F\x7F]/g, '')  // Remove control characters
    .substring(0, 4096);
}
```

## JID Validation

```javascript
function isValidJID(jid) {
  if (typeof jid !== 'string' || !jid.trim()) return false;
  // Zoom JIDs follow pattern: user@domain or channel@domain
  return /^[^@\s]+@[^@\s]+$/.test(jid);
}
```

## Environment Variable Validation

```javascript
function validateEnvironmentVariables() {
  const required = [
    'ZOOM_CLIENT_ID',
    'ZOOM_CLIENT_SECRET',
    'ZOOM_BOT_JID',
    'ZOOM_VERIFICATION_TOKEN',
    'ACCOUNT_ID'
  ];
  const missing = required.filter(v => !process.env[v]);
  if (missing.length) {
    console.error('Missing env vars:', missing);
    process.exit(1);
  }
}
```

---

# App Manifest API

Configure apps programmatically instead of manually in Zoom Marketplace UI:

```bash
PUT /marketplace/apps/{appId}/manifest
```

Example manifest for Team Chat chatbot:

```json
{
  "manifest": {
    "display_information": {
      "display_name": "My Chatbot"
    },
    "oauth_information": {
      "usage": "USER_OPERATION",
      "development_redirect_uri": "https://example.ngrok.app/auth/callback",
      "scopes": [
        { "scope": "imchat:bot", "optional": false }
      ]
    },
    "features": {
      "products": ["ZOOM_CHAT"],
      "team_chat_subscription": {
        "enable": true,
        "slash_command": {
          "command": "/mybot",
          "development_message_url": "https://example.ngrok.app/webhook",
          "sender_type": "zoom"
        }
      }
    }
  }
}
```

---

# Deployment

## Nginx Reverse Proxy Setup

When deploying behind nginx at a subpath (e.g., `/zoom-team-chat/project/team-chat-api/`), configure proxy rules for API routes:

```nginx
# Team Chat API (User OAuth - port 4001)
location /zoom-team-chat/project/team-chat-api/auth/ {
    proxy_pass http://localhost:4001/auth/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

location /zoom-team-chat/project/team-chat-api/api/ {
    proxy_pass http://localhost:4001/api/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# Static files
location /zoom-team-chat {
    alias /var/www/zoom-team-chat;
    index index.html;
    try_files $uri $uri/ =404;
}
```

## Frontend Base Path (IMPORTANT)

When serving from a subpath, **frontend JavaScript must use the correct base path** for API calls:

```javascript
// ❌ WRONG - Goes to domain root
fetch('/auth/status');
fetch('/api/channels');

// ✅ CORRECT - Use base path constant
const BASE_PATH = '/zoom-team-chat/project/team-chat-api';
fetch(`${BASE_PATH}/auth/status`);
fetch(`${BASE_PATH}/api/channels`);
```

**Common symptoms of incorrect base path:**
- OAuth succeeds but page shows "Not authenticated"
- API calls return 404
- Login redirects to wrong page

## OAuth Redirect URI

The redirect URI must be configured in **three places**:

1. **Server `.env` file**:
   ```bash
   ZOOM_REDIRECT_URI=https://yourdomain.com/zoom-team-chat/project/team-chat-api/auth/callback
   ```

2. **Zoom Marketplace** → Your App → OAuth Information:
   - OAuth redirect URL: `https://yourdomain.com/zoom-team-chat/project/team-chat-api/auth/callback`
   - OAuth allow list: Same URL

3. **Server redirect after auth** (in callback handler):
   ```javascript
   // Redirect to the correct subpath, not root
   res.redirect('/zoom-team-chat/project/team-chat-api/?authenticated=true');
   ```

---

# Limitations

| Limit | Value |
|-------|-------|
| Message length | 4,096 characters |
| File size | 512 MB |
| Members per channel | 10,000 |
| Channels per user | 500 |

---

# Sample Applications

| Sample | Description | Link |
|--------|-------------|------|
| **Chatbot Quickstart** | Official tutorial series (recommended starting point) | [GitHub](https://github.com/zoom/chatbot-nodejs-quickstart) |
| Claude Chatbot | AI-powered chatbot with Anthropic Claude | [GitHub](https://github.com/zoom/zoom-chatbot-claude-sample) |
| Unsplash Chatbot | Image search bot with database storage | [GitHub](https://github.com/zoom/unsplash-chatbot) |
| ERP Chatbot | Oracle ERP integration with scheduled alerts | [GitHub](https://github.com/zoom/zoom-erp-chatbot-sample) |
| Task Manager | Full-featured app | [GitHub](https://github.com/zoom/task-manager-sample) |
| Rivet Sample | Using Zoom Rivet SDK | [GitHub](https://github.com/zoom/rivet-javascript-sample) |

---

# Resources

## Official Documentation
- [Team Chat Overview](https://developers.zoom.us/docs/team-chat/)
- [Team Chat API Reference](https://developers.zoom.us/docs/api/rest/reference/chat/methods/)
- [Chatbot API Reference](https://developers.zoom.us/docs/api/rest/reference/chatbot/methods/)
- [App Manifest API](https://developers.zoom.us/docs/api/marketplace/)

## Developer Support
- [Zoom App Marketplace](https://marketplace.zoom.us/)
- [Developer Support](https://devsupport.zoom.us)
- [Developer Forum](https://devforum.zoom.us)

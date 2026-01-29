---
name: zoom-team-chat
description: |
  Zoom Team Chat API integration guide. Covers sending messages to users and channels, 
  creating and managing channels, sharing files, and building chat integrations. 
  Use when building notification systems, chatbots, workflow automation, or integrating 
  external tools with Zoom's messaging platform.
---

# Zoom Team Chat API

Build messaging integrations with Zoom Team Chat. Send messages, manage channels, and automate team communication.

## Overview

Zoom Team Chat (formerly Zoom Chat) is Zoom's messaging platform. The API allows you to:
- Send messages to users and channels
- Create and manage channels
- Share files and attachments
- Manage contact lists
- Build chat integrations and bots
- Receive real-time events via webhooks

## Key Features

| Feature | Description |
|---------|-------------|
| **Direct Messages** | Send 1:1 messages to users |
| **Channel Messages** | Post to public and private channels |
| **Rich Text** | Format messages with bold, italic, links |
| **Mentions** | @mention users in messages |
| **File Sharing** | Upload and share files up to 512 MB |
| **Channel Management** | Create, update, delete channels |
| **Member Management** | Add/remove members from channels |
| **Message Editing** | Update or delete sent messages |
| **Webhooks** | Real-time event notifications |

## Choose Your Integration

| I want to... | Use this |
|--------------|----------|
| Send alerts to a channel | **Messages API** |
| Create channels programmatically | **Channels API** |
| Build a notification bot | **Messages API + Webhooks** |
| Integrate external tools | **Messages API** |
| Manage team communication | **Channels + Members API** |
| Receive chat events | **Webhooks** |
| Share files from your app | **File Upload API** |

## Core Endpoints

### Messages

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat/users/{userId}/messages` | Send message |
| GET | `/chat/users/{userId}/messages` | List messages |
| PUT | `/chat/users/{userId}/messages/{messageId}` | Update message |
| DELETE | `/chat/users/{userId}/messages/{messageId}` | Delete message |
| POST | `/chat/users/{userId}/messages/files` | Share file |

### Channels

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/chat/users/{userId}/channels` | List user's channels |
| POST | `/chat/users/{userId}/channels` | Create channel |
| GET | `/chat/channels/{channelId}` | Get channel details |
| PATCH | `/chat/channels/{channelId}` | Update channel |
| DELETE | `/chat/channels/{channelId}` | Delete channel |
| GET | `/chat/channels/{channelId}/members` | List members |
| POST | `/chat/channels/{channelId}/members` | Add members |
| DELETE | `/chat/channels/{channelId}/members/{memberId}` | Remove member |

### Contacts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/chat/users/{userId}/contacts` | List contacts |
| GET | `/chat/users/{userId}/contacts/{contactId}` | Get contact |

## Common Operations

### Send Message to User

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/chat/users/me/messages',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      to_jid: 'user_jid@xmpp.zoom.us',  // Recipient JID
      message: 'Hello from the API!'
    })
  }
);

const result = await response.json();
// { "id": "msg_123", "date_time": "2024-01-15T10:30:00Z" }
```

### Send Message to Channel

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/chat/users/me/messages',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      to_channel: 'channel_id_123',
      message: 'Team announcement!'
    })
  }
);
```

### Send Rich Message with Formatting

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/chat/users/me/messages',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      to_channel: 'channel_id_123',
      message: 'New deployment completed!',
      rich_text: [
        {
          start_position: 0,
          end_position: 3,
          format_type: 'Bold'
        }
      ],
      at_items: [
        {
          at_type: 1,  // 1 = @mention user
          at_contact: 'user_jid@xmpp.zoom.us',
          start_position: 25,
          end_position: 30
        }
      ]
    })
  }
);
```

### Create Channel

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/chat/users/me/channels',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: 'Project Alpha',
      type: 1,  // 1 = private, 2 = public
      members: [
        { email: 'user1@example.com' },
        { email: 'user2@example.com' }
      ]
    })
  }
);

const channel = await response.json();
// { "id": "channel_123", "jid": "channel_jid@xmpp.zoom.us", "name": "Project Alpha" }
```

### List Messages in Channel

```javascript
const params = new URLSearchParams({
  to_channel: 'channel_id_123',
  from: '2024-01-01T00:00:00Z',
  to: '2024-01-31T23:59:59Z',
  page_size: 50
});

const response = await fetch(
  `https://api.zoom.us/v2/chat/users/me/messages?${params}`,
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const messages = await response.json();
// { "messages": [...], "next_page_token": "..." }
```

### Share File

```javascript
const formData = new FormData();
formData.append('to_channel', 'channel_id_123');
formData.append('files', fileBlob, 'document.pdf');

const response = await fetch(
  'https://api.zoom.us/v2/chat/users/me/messages/files',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`
    },
    body: formData
  }
);
```

### Add Members to Channel

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/chat/channels/channel_id_123/members',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      members: [
        { email: 'newuser@example.com' }
      ]
    })
  }
);
```

## Message Types

| Type | Description |
|------|-------------|
| **Text** | Plain text message |
| **File** | File attachment |
| **Image** | Image attachment |
| **Code snippet** | Code block with syntax highlighting |
| **Interactive** | Message with action buttons (Chatbot only) |

## Channel Types

| Type | Value | Description |
|------|-------|-------------|
| **Private** | 1 | Invite-only channel |
| **Public** | 2 | Anyone in org can join |
| **Member** | 3 | Direct message (1:1) |
| **Group** | 4 | Group chat (no channel) |

## Webhooks

Team Chat events via webhooks:

| Event | Trigger |
|-------|---------|
| `chat_message.sent` | New message sent |
| `chat_message.updated` | Message edited |
| `chat_message.deleted` | Message deleted |
| `chat_channel.created` | New channel created |
| `chat_channel.updated` | Channel updated |
| `chat_channel.deleted` | Channel deleted |
| `chat_channel.member_added` | Member joined |
| `chat_channel.member_removed` | Member left |

### Webhook Payload Example

```json
{
  "event": "chat_message.sent",
  "payload": {
    "account_id": "abc123",
    "object": {
      "id": "msg_xyz",
      "type": "to_channel",
      "channel_id": "channel_123",
      "sender": "user_jid@xmpp.zoom.us",
      "message": "Hello team!",
      "date_time": "2024-01-15T10:30:00Z"
    }
  }
}
```

## Required Scopes

| Scope | Description |
|-------|-------------|
| `chat_message:read` | Read messages |
| `chat_message:write` | Send messages |
| `chat_channel:read` | Read channels |
| `chat_channel:write` | Create/manage channels |
| `chat_contact:read` | Read contacts |
| `chat_message:read:admin` | Read all messages (admin) |
| `chat_message:write:admin` | Send as any user (admin) |

## Limitations

| Limitation | Value |
|------------|-------|
| **Message length** | 4096 characters |
| **File size** | 512 MB |
| **Members per channel** | 10,000 |
| **Channels per user** | 500 |

## Common Use Cases

| Use Case | Description | Integration |
|----------|-------------|-------------|
| **Alert Notifications** | Send alerts to channels | Messages API |
| **Onboarding Bot** | Welcome new team members | Messages API + Webhooks |
| **Incident Management** | Create channels for incidents | Channels API |
| **Workflow Automation** | Post updates from CI/CD | Messages API |
| **Integration Hub** | Connect external tools | Messages API + Webhooks |
| **Team Announcements** | Broadcast to multiple channels | Messages API |
| **File Distribution** | Share files programmatically | File Upload API |

## Prerequisites

1. **Zoom account** - Team Chat enabled
2. **OAuth app** - Create in [Zoom App Marketplace](https://marketplace.zoom.us/)
3. **Scopes** - Request required Team Chat scopes
4. **Access token** - OAuth 2.0 bearer token

## Detailed References

- **[references/messages.md](references/messages.md)** - Message API guide
- **[references/channels.md](references/channels.md)** - Channel management
- **[references/webhooks.md](references/webhooks.md)** - Webhook setup
- **[references/scopes.md](references/scopes.md)** - Required OAuth scopes

## Resources

- **Official docs**: https://developers.zoom.us/docs/team-chat/
- **API Reference**: https://developers.zoom.us/docs/api/rest/reference/team-chat/methods/
- **Chatbots**: https://developers.zoom.us/docs/team-chat/chatbots/
- **Webhooks**: https://developers.zoom.us/docs/api/webhooks/
- **Marketplace**: https://marketplace.zoom.us/

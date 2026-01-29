# Rivet

Zoom's official API library for accelerating server-side development.

## Overview

Rivet is a framework that simplifies server-side Zoom app development with built-in authentication, API integration, and webhook event management. It lets you focus on business logic instead of boilerplate.

## Features

| Feature | Description |
|---------|-------------|
| **Authentication** | Built-in Server-to-Server OAuth and OAuth 2.0 |
| **API Integration** | Pre-built methods for Zoom APIs |
| **Webhook Server** | Handle webhook events with minimal setup |
| **Event Management** | Subscribe and respond to Zoom events easily |

## Installation

```bash
npm install @zoom/rivet
```

## Quick Start

### Initialize Client

```javascript
import { Rivet } from '@zoom/rivet';

const rivet = new Rivet({
  clientId: 'YOUR_CLIENT_ID',
  clientSecret: 'YOUR_CLIENT_SECRET',
  accountId: 'YOUR_ACCOUNT_ID'  // For S2S OAuth
});
```

### Make API Calls

```javascript
// Create a meeting
const meeting = await rivet.meetings.create({
  userId: 'me',
  topic: 'My Meeting',
  type: 2,
  duration: 60
});

// List users
const users = await rivet.users.list();
```

### Handle Webhooks

```javascript
import { createWebhookServer } from '@zoom/rivet';

const server = createWebhookServer({
  secretToken: 'YOUR_WEBHOOK_SECRET'
});

server.on('meeting.started', (event) => {
  console.log('Meeting started:', event.payload);
});

server.on('recording.completed', (event) => {
  console.log('Recording ready:', event.payload);
});

server.listen(3000);
```

## Supported APIs

- Meetings
- Users
- Accounts
- Phone
- Team Chat
- Video SDK
- Chatbot

## When to Use Rivet

| Use Case | Rivet? |
|----------|--------|
| Server-side API integration | ✅ Yes |
| Webhook handling | ✅ Yes |
| Quick prototyping | ✅ Yes |
| Client-side (browser) | ❌ No - use REST API directly |
| Meeting/Video SDK apps | ❌ No - use respective SDKs |

## Resources

- **Documentation**: https://developers.zoom.us/docs/rivet/
- **GitHub**: https://github.com/zoom/rivet-javascript
- **npm**: https://www.npmjs.com/package/@zoom/rivet

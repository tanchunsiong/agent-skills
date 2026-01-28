---
name: zoom-cobrowse-sdk
description: |
  Zoom Cobrowse SDK for collaborative browsing. Enables agents to view and interact with 
  customer's browser in real-time for support, form completion, and guided walkthroughs.
  Web-based, no plugins required.
---

# Zoom Cobrowse SDK

Enable collaborative browsing between agents and customers on your website.

## Overview

Cobrowse (collaborative browsing) allows support agents to see and interact with a customer's browser session in real-time. The SDK provides secure screen sharing limited to your website, with annotation tools and privacy masking.

## Key Features

| Feature | Description |
|---------|-------------|
| **Real-time co-browsing** | Agent sees customer's browser live |
| **Annotations** | Draw, highlight, point on screen |
| **Privacy masking** | Hide sensitive fields from agents |
| **PIN-based access** | Secure session initiation |
| **No plugins** | Pure JavaScript, no downloads |

## Roles

| Role | Description |
|------|-------------|
| **Customer** | User on your website who shares their session |
| **Agent** | Support staff who views/assists customer |
| **Admin** | Configures SDK settings |

## Prerequisites

- SDK Universal Credit added to Zoom Workplace account
- SDK Key and Secret from web portal
- Website to integrate SDK

## Quick Start

### 1. Get Credentials

1. Add SDK Universal Credit to your Zoom account
2. Go to **Advanced** → **Zoom CPaaS** → **Manage**
3. Click **Build App** and get SDK Key/Secret

### 2. Generate JWT

```javascript
// Customer JWT payload
{
  "user_id": "customer_123",
  "app_key": "YOUR_SDK_KEY",
  "role_type": 1,  // 1 = customer
  "user_name": "Customer Name",
  "exp": 1723103759,
  "iat": 1723102859
}

// Agent JWT payload
{
  "user_id": "agent_456",
  "app_key": "YOUR_SDK_KEY",
  "role_type": 2,  // 2 = agent
  "user_name": "Agent Name",
  "exp": 1723103759,
  "iat": 1723102859
}
```

### 3. Integrate SDK (Customer Side)

```html
<script src="https://cobrowse.zoom.us/sdk.js"></script>

<script>
const cobrowse = new ZoomCobrowse({
  sdkKey: 'YOUR_SDK_KEY',
  token: customerJWT
});

// Start session and get PIN
const session = await cobrowse.startSession();
console.log('Share this PIN with agent:', session.pin);
</script>
```

### 4. Agent Joins

Agent uses the PIN to join via embedded iframe or agent portal.

## Use Cases

- Customer support troubleshooting
- Form completion assistance
- Product demos and walkthroughs
- Onboarding guidance
- Technical support

## Detailed References

- **[references/get-started.md](references/get-started.md)** - Setup guide
- **[references/authorization.md](references/authorization.md)** - JWT generation
- **[references/features.md](references/features.md)** - Annotations, masking, BYOP
- **[references/api.md](references/api.md)** - SDK API reference

## Resources

- **Official docs**: https://developers.zoom.us/docs/cobrowse-sdk/
- **Quickstart**: https://github.com/zoom/CobrowseSDK-Quickstart

---
name: zoom-contact-center
description: |
  Zoom Contact Center SDK and APIs for building customer engagement solutions. 
  SDKs for Web, iOS, and Android. Use when integrating Zoom Contact Center 
  video/chat capabilities into your application.
---

# Zoom Contact Center

Build customer engagement solutions with Zoom Contact Center.

## Prerequisites

- Zoom Contact Center license
- Contact Center SDK credentials
- Platform-specific development environment

## Choose Your Integration

| Integration | Use Case |
|-------------|----------|
| **Web SDK** | Browser-based contact center UI |
| **iOS SDK** | Contact center on iPhone/iPad |
| **Android SDK** | Contact center on Android |
| **APIs** | Server-side contact center management |

## Quick Start (Web)

```javascript
import { ZoomContactCenter } from '@zoom/contact-center-sdk';

const client = new ZoomContactCenter();

await client.init({
  clientId: 'YOUR_CLIENT_ID',
  domain: 'your-domain.zoom.us'
});

// Start a video engagement
await client.startVideoEngagement({
  queueId: 'QUEUE_ID',
  customerInfo: {
    name: 'Customer Name',
    email: 'customer@example.com'
  }
});
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| Engagement | Customer-agent interaction |
| Queue | Routing destination for engagements |
| Agent | Contact center representative |
| Flow | Call/chat routing logic |

## Detailed References

- **[references/sdk-web.md](references/sdk-web.md)** - Web SDK integration
- **[references/sdk-ios.md](references/sdk-ios.md)** - iOS SDK integration
- **[references/sdk-android.md](references/sdk-android.md)** - Android SDK integration
- **[references/apis.md](references/apis.md)** - Contact Center APIs
- **[references/virtual-agent.md](references/virtual-agent.md)** - Zoom Virtual Agent (AI chatbot)

## Resources

- **Official docs**: https://developers.zoom.us/docs/contact-center/
- **Developer forum**: https://devforum.zoom.us/

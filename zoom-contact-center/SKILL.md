---
name: zoom-contact-center
description: |
  Zoom Contact Center SDK for building customer engagement experiences. Supports voice, video, 
  and chat on web, iOS, and Android. Use for consumer-facing support portals, agent integrations, 
  and CRM connectivity.
---

# Zoom Contact Center

AI-powered customer engagement platform for voice, video, and chat.

> **Official docs:** https://developers.zoom.us/docs/contact-center/
> **Sample CRM app:** https://github.com/zoom/CRM-Sample (branch: `Contact-Center`)

## Two Roles

| Role | Description | Integration Options |
|------|-------------|---------------------|
| **Agents** | Internal users (support, sales) | Zoom Workplace App, Smart Embed, CRM APIs |
| **Consumers** | External users (customers) | Web SDK, iOS SDK, Android SDK |

## Integration Options

### For Agents

| Option | Description | Best For |
|--------|-------------|----------|
| **Zoom Workplace App** | Native desktop experience with Contact Center Apps | Agent tools, knowledge assistants |
| **Smart Embed** | Embed softphone via iframe into your web app | Custom CRM, agent dashboards |
| **CRM Integration** | REST APIs and webhooks | Salesforce, HubSpot, custom CRMs |

### For Consumers

| Platform | Description | Docs |
|----------|-------------|------|
| **Web** | JavaScript SDK for video/chat in browsers | [web/](web/) |
| **iOS** | Native iOS SDK | [ios/](ios/) |
| **Android** | Native Android SDK | [android/](android/) |

## Prerequisites

- Zoom Contact Center license
- Verified subdomain (see [Managing verified domains](https://support.zoom.us/hc/en-us/articles/6985492329357))
- Entry ID (identifies your video/chat flow)
- Video or chat flow configured

## Quick Start (Web)

### 1. Add CSP Header

Configure your web server to allow Zoom SDK:

```nginx
add_header 'Content-Security-Policy' "default-src 'self';base-uri 'self';worker-src blob:;style-src 'self' 'unsafe-inline';script-src 'self' 'unsafe-inline' 'unsafe-eval' https://zoom.us *.zoom.us dmogdx0jrul3u.cloudfront.net blob:;connect-src 'self' https://zoom.us https://*.zoom.us wss://*.zoom.us;img-src 'self' https:;media-src 'self' https:;font-src 'self' https:;";
```

### 2. Add SDK Script

```html
<script src="https://static.zoom.us/zcc/web-sdk/v2/zcc-web-sdk.min.js"></script>
```

### 3. Initialize Client

```javascript
const client = new ZoomContactCenterClient();
await client.init({
  entryId: 'your-entry-id',
  // Additional config
});
```

See [web/get-started.md](web/get-started.md) for complete setup.

## Platform Guides

| Platform | Guide |
|----------|-------|
| Web | [web/get-started.md](web/get-started.md) |
| iOS | [ios/get-started.md](ios/get-started.md) |
| Android | [android/get-started.md](android/get-started.md) |

## Features by Platform

| Feature | Web | iOS | Android |
|---------|-----|-----|---------|
| Video calls | Yes | Yes | Yes |
| Chat | Yes | Yes | Yes |
| Screen share | Yes | Yes | Yes |
| Push notifications | N/A | Yes | Yes |
| Background mode | N/A | Yes | Yes |

## Smart Embed (Agent UI)

Embed the Contact Center softphone into your web app:

```html
<iframe 
  id="zoom-embeddable-phone-iframe"
  src="https://zoom.us/cci/callbar/crm/?origin=https://your-app-domain.com"
  sandbox="allow-forms allow-popups allow-popups-to-escape-sandbox allow-scripts allow-same-origin allow-downloads"
  allow=";autoplay;microphone;camera;display-capture;midi;encrypted-media;clipboard-write;"
  style="width: 840px; height: 700px; border: none;"
></iframe>
```

See [references/smart-embed.md](references/smart-embed.md) for setup and configuration.

## APIs & Webhooks

| Resource | Description |
|----------|-------------|
| [Contact Center API](https://developers.zoom.us/docs/api/contact-center/) | REST endpoints for engagements, queues, agents |
| [REST API Guide](references/rest-api.md) | Implementation examples with NextAuth.js |
| Webhooks | Real-time events for engagement lifecycle |

### OAuth Scopes for Contact Center

```
contact_center_contact:read:admin
contact_center_report:read:admin
user:read:user:admin
```

See [zoom-oauth skill](/zoom-oauth/SKILL.md) for OAuth setup.

## Sample Application

The official [CRM-Sample](https://github.com/zoom/CRM-Sample) demonstrates a full CRM integration:

```bash
git clone --branch Contact-Center --single-branch https://github.com/zoom/CRM-Sample.git
cd CRM-Sample
npm install
cp .env.sample .env
# Edit .env with your credentials
npm run dev
```

**Tech stack:** Next.js, React, TailwindCSS, NextAuth.js, Zoom Smart Embed

## Resources

- **Official docs:** https://developers.zoom.us/docs/contact-center/
- **Sample CRM app:** https://github.com/zoom/CRM-Sample (branch: Contact-Center)
- **Admin setup:** https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060897
- **Developer forum:** https://devforum.zoom.us/
- **API reference:** https://developers.zoom.us/docs/api/contact-center/

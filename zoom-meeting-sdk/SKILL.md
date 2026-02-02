---
name: zoom-meeting-sdk
description: |
  Zoom Meeting SDK for embedding Zoom meetings into your web application. 
  Use when you want to integrate the full Zoom meeting experience into your app.
---

# Zoom Meeting SDK (Web)

Embed the full Zoom meeting experience into your web application.

## Prerequisites

- Zoom app with Meeting SDK credentials
- SDK Key and Secret from Marketplace
- Web development environment

## Quick Start (Web)

```html
<script src="https://source.zoom.us/2.18.0/lib/vendor/react.min.js"></script>
<script src="https://source.zoom.us/2.18.0/lib/vendor/react-dom.min.js"></script>
<script src="https://source.zoom.us/2.18.0/lib/vendor/redux.min.js"></script>
<script src="https://source.zoom.us/2.18.0/lib/vendor/redux-thunk.min.js"></script>
<script src="https://source.zoom.us/2.18.0/lib/vendor/lodash.min.js"></script>
<script src="https://source.zoom.us/zoom-meeting-2.18.0.min.js"></script>

<script>
const client = ZoomMtgEmbedded.createClient();

client.init({
  zoomAppRoot: document.getElementById('meetingSDKElement'),
  language: 'en-US',
});

client.join({
  sdkKey: 'YOUR_SDK_KEY',
  signature: 'YOUR_SIGNATURE',
  meetingNumber: 'MEETING_NUMBER',
  userName: 'User Name',
});
</script>
```

## UI Options (Web)

Meeting SDK provides **Zoom's UI with customization options**:

| View | Description |
|------|-------------|
| **Component View** | Extractable, customizable UI - embed meeting in a div |
| **Client View** | Full-page Zoom UI experience |

**Note**: Unlike Video SDK where you build the UI from scratch, Meeting SDK uses Zoom's UI as the base with customization on top.

## Key Concepts

| Concept | Description |
|---------|-------------|
| SDK Key/Secret | Credentials from Marketplace |
| Signature | JWT signed with SDK Secret |
| Component View | Extractable, customizable UI (Web) |
| Client View | Full-page Zoom UI (Web) |

## Detailed References

### Platform Guide
- **[references/web.md](references/web.md)** - Web SDK (Component + Client View)
- **[references/web-tracking-id.md](references/web-tracking-id.md)** - Tracking ID configuration

### Features
- **[references/authorization.md](references/authorization.md)** - SDK JWT generation
- **[references/bot-authentication.md](references/bot-authentication.md)** - ZAK vs OBF vs JWT tokens for bots
- **[references/breakout-rooms.md](references/breakout-rooms.md)** - Programmatic breakout room management
- **[references/ai-companion.md](references/ai-companion.md)** - AI Companion controls in meetings
- **[references/webinars.md](references/webinars.md)** - Webinar SDK features
- **[references/troubleshooting.md](references/troubleshooting.md)** - Common issues and solutions

## Sample Repositories

### Official (by Zoom)

| Type | Repository | Stars |
|------|------------|-------|
| Web | [meetingsdk-web-sample](https://github.com/zoom/meetingsdk-web-sample) | 643 |
| Web NPM | [meetingsdk-web](https://github.com/zoom/meetingsdk-web) | 324 |
| React | [meetingsdk-react-sample](https://github.com/zoom/meetingsdk-react-sample) | 177 |
| Auth | [meetingsdk-auth-endpoint-sample](https://github.com/zoom/meetingsdk-auth-endpoint-sample) | 124 |
| Angular | [meetingsdk-angular-sample](https://github.com/zoom/meetingsdk-angular-sample) | 60 |
| Vue.js | [meetingsdk-vuejs-sample](https://github.com/zoom/meetingsdk-vuejs-sample) | 42 |

**Full list**: See [zoom-general/references/community-repos.md](../zoom-general/references/community-repos.md)

## Resources

- **Official docs**: https://developers.zoom.us/docs/meeting-sdk/
- **Developer forum**: https://devforum.zoom.us/

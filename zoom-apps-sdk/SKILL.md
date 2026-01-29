---
name: zoom-apps-sdk
description: |
  Zoom Apps SDK for building apps that run inside the Zoom client. JavaScript SDK for 
  in-meeting experiences and Layers API for immersive apps. Use when you want your app 
  to appear within Zoom meetings or the Zoom client.
---

# Zoom Apps SDK

Build apps that run inside the Zoom client.

## Prerequisites

- Zoom app configured as "Zoom App" type in Marketplace
- OAuth credentials with Zoom Apps scopes
- Web application to serve your Zoom App

## Quick Start

```html
<script src="https://appssdk.zoom.us/sdk.min.js"></script>

<script>
const zoomSdk = new ZoomSdk({ version: '0.16' });

async function init() {
  const configResponse = await zoomSdk.config({
    capabilities: ['shareApp', 'getMeetingContext']
  });
  
  const context = await zoomSdk.getMeetingContext();
  console.log('Meeting ID:', context.meetingID);
}

init();
</script>
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| Zoom App | Web app running in Zoom's embedded browser |
| Capabilities | Permissions your app requests |
| Context | Meeting/user information |
| Layers API | Immersive visual experiences |

## Common APIs

| API | Description |
|-----|-------------|
| `config()` | Initialize SDK, request capabilities |
| `getMeetingContext()` | Get meeting info |
| `shareApp()` | Share app with participants |
| `openUrl()` | Open URL in browser |
| `runRenderingContext()` | Start Layers API |

## Detailed References

- **[references/apis.md](references/apis.md)** - Complete API reference
- **[references/events.md](references/events.md)** - SDK events
- **[references/layers-api.md](references/layers-api.md)** - Immersive experiences
- **[references/oauth.md](references/oauth.md)** - Zoom Apps OAuth flow
- **[references/zmail-sdk.md](references/zmail-sdk.md)** - ZMail integration for email

## Sample Repositories

### Official (by Zoom)

| Type | Repository | Stars |
|------|------------|-------|
| Hello World | [zoomapps-sample-js](https://github.com/zoom/zoomapps-sample-js) | 66 |
| Advanced React | [zoomapps-advancedsample-react](https://github.com/zoom/zoomapps-advancedsample-react) | 55 |
| SDK NPM | [appssdk](https://github.com/zoom/appssdk) | 49 |
| Collaborate Mode | [zoomapps-texteditor-vuejs](https://github.com/zoom/zoomapps-texteditor-vuejs) | 16 |
| Layers API | [zoomapps-customlayout-js](https://github.com/zoom/zoomapps-customlayout-js) | 16 |
| Serverless | [zoomapps-serverless-vuejs](https://github.com/zoom/zoomapps-serverless-vuejs) | 6 |
| Camera Mode | [zoomapps-cameramode-vuejs](https://github.com/zoom/zoomapps-cameramode-vuejs) | 6 |
| Workshop | [zoomapps-workshop-sample](https://github.com/zoom/zoomapps-workshop-sample) | 6 |
| RTMS Assistant | [arlo-meeting-assistant](https://github.com/zoom/arlo-meeting-assistant) | 2 |
| Recall.ai Bot | [meetingbot-recall-sample](https://github.com/zoom/meetingbot-recall-sample) | 2 |

### Community

| Type | Repository | Description |
|------|------------|-------------|
| Library | [harvard-edtech/zaccl](https://github.com/harvard-edtech/zaccl) | Zoom App Complete Connection Library |
| AI Demo | [inworld-ai/zoom-demeanor-evaluator-node](https://github.com/inworld-ai/zoom-demeanor-evaluator-node) | RTMS + Inworld AI |

**Full list**: See [zoom-general/references/community-repos.md](../zoom-general/references/community-repos.md)

## Resources

- **Official docs**: https://developers.zoom.us/docs/zoom-apps/
- **SDK reference**: https://appssdk.zoom.us/
- **Developer forum**: https://devforum.zoom.us/

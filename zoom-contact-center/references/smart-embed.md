# Smart Embed

Embed the Zoom Contact Center agent softphone directly into your web application via iframe.

> **Official docs:** https://developers.zoom.us/docs/contact-center/smart-embed/
> **Sample repo:** https://github.com/zoom/CRM-Sample (branch: `Contact-Center`)

## Overview

Smart Embed lets you integrate the full Contact Center agent interface into your custom CRM or dashboard. Agents can handle calls, view customer info, and manage engagements without leaving your app.

## Use Cases

- Custom CRM integration
- Agent dashboards
- Internal support tools
- Unified agent workspace

## Quick Start

The Contact Center Smart Embed uses the CRM Call Bar URL:

```html
<iframe 
  id="zoom-embeddable-phone-iframe"
  src="https://zoom.us/cci/callbar/crm/?origin=https://your-app-domain.com"
  sandbox="allow-forms allow-popups allow-popups-to-escape-sandbox allow-scripts allow-same-origin allow-downloads"
  allow=";autoplay;microphone;camera;display-capture;midi;encrypted-media;clipboard-write;"
  style="width: 840px; height: 700px; border: none;"
></iframe>
```

### React Component Example

From [Zoom CRM-Sample](https://github.com/zoom/CRM-Sample/blob/Contact-Center/src/components/SmartEmbed.js):

```jsx
export default function SmartEmbed() {
  return (
    <div className="flex justify-center items-center min-h-screen">
      <iframe
        src="https://zoom.us/cci/callbar/crm/?origin=https://your-ngrok-url.ngrok-free.app"
        sandbox="allow-forms allow-popups allow-popups-to-escape-sandbox allow-scripts allow-same-origin allow-downloads"
        allow=";autoplay;microphone;camera;display-capture;midi;encrypted-media;clipboard-write;"
        id="zoom-embeddable-phone-iframe"
        className="w-[840px] h-[700px] border-none"
      ></iframe>
    </div>
  );
}
```

## Setup Prerequisites

### 1. Create Admin-Level OAuth App

1. Go to [Zoom App Marketplace](https://marketplace.zoom.us/)
2. Create an **Admin-level OAuth App**
3. Add required scopes:
   ```
   contact_center_contact:read:admin
   contact_center_report:read:admin
   user:read:user:admin
   ```
4. Set redirect URI to your callback endpoint

### 2. Configure Smart Embed Integration

1. Log in to [zoom.us/myhome](https://zoom.us/myhome)
2. Go to **Contact Center Management** tab
3. Navigate to **Integrations**
4. Create a new integration with your app's home URL (e.g., ngrok link)
5. Under **Contact Center Management** → select your agent user
6. Under **Client Integration**, add the previously created integration

### 3. Environment Variables

```env
# .env
ZOOM_CLIENT_ID={clientID}
ZOOM_CLIENT_SECRET={clientSecret}
NEXTAUTH_URL=https://your-app-url.com/api/auth/callback/zoom
NEXTAUTH_SECRET=your_nextauth_secret
```

## URL Format

| Smart Embed Type | URL Pattern |
|------------------|-------------|
| Contact Center CRM Bar | `https://zoom.us/cci/callbar/crm/?origin={YOUR_APP_ORIGIN}` |
| Phone Embeddable | `https://applications.zoom.us/integration/phone/embeddablephone/home` |

**Important:** The `origin` parameter must match your app's domain exactly.

## PostMessage API

Communicate with the embedded softphone via postMessage:

### Send Commands

```javascript
const iframe = document.getElementById('zoom-embeddable-phone-iframe');

// Make outbound call
iframe.contentWindow.postMessage({
  type: 'ZCC_COMMAND',
  action: 'dial',
  payload: {
    phoneNumber: '+1234567890'
  }
}, 'https://zoom.us');

// Set agent status
iframe.contentWindow.postMessage({
  type: 'ZCC_COMMAND',
  action: 'setStatus',
  payload: {
    status: 'available' // 'available', 'busy', 'away'
  }
}, 'https://zoom.us');
```

### Receive Events

```javascript
window.addEventListener('message', (event) => {
  if (event.origin !== 'https://zoom.us') return;
  
  const { type, data } = event.data;
  
  switch (type) {
    case 'ZCC_READY':
      console.log('Softphone ready');
      break;
      
    case 'ZCC_ENGAGEMENT_START':
      console.log('Engagement started:', data.engagementId);
      // Update your CRM with call info
      break;
      
    case 'ZCC_ENGAGEMENT_END':
      console.log('Engagement ended:', data.engagementId);
      // Log call in your system
      break;
      
    case 'ZCC_STATUS_CHANGE':
      console.log('Agent status:', data.status);
      break;
  }
});
```

## Events Reference

| Event | Description | Payload |
|-------|-------------|---------|
| `ZCC_READY` | Softphone initialized | `{ version }` |
| `ZCC_ENGAGEMENT_START` | Call/chat started | `{ engagementId, type, customerId }` |
| `ZCC_ENGAGEMENT_END` | Call/chat ended | `{ engagementId, duration, disposition }` |
| `ZCC_STATUS_CHANGE` | Agent status changed | `{ status, previousStatus }` |
| `ZCC_INCOMING` | Incoming engagement | `{ engagementId, type, customerId }` |
| `ZCC_ERROR` | Error occurred | `{ code, message }` |

## Commands Reference

| Command | Description | Payload |
|---------|-------------|---------|
| `dial` | Make outbound call | `{ phoneNumber }` |
| `answer` | Answer incoming call | `{ engagementId }` |
| `hangup` | End current call | `{ engagementId }` |
| `hold` | Put call on hold | `{ engagementId }` |
| `transfer` | Transfer call | `{ engagementId, targetAgent }` |
| `setStatus` | Change agent status | `{ status }` |
| `sendDTMF` | Send DTMF tones | `{ digits }` |

## Iframe Permissions

Required `allow` attributes:

```html
<iframe 
  allow="camera; microphone; display-capture; autoplay"
  ...
></iframe>
```

| Permission | Required For |
|------------|--------------|
| `camera` | Video calls |
| `microphone` | Voice and video calls |
| `display-capture` | Screen sharing |
| `autoplay` | Media playback |

## Security

### CSP Configuration

If using Content Security Policy, allow Zoom domains:

```
frame-src https://zoom.us https://*.zoom.us;
connect-src https://zoom.us https://*.zoom.us wss://*.zoom.us;
```

### Origin Validation

Always validate message origin:

```javascript
window.addEventListener('message', (event) => {
  // Only accept messages from Zoom
  if (event.origin !== 'https://zoom.us') {
    return;
  }
  // Process message
});
```

## Styling

### Responsive Container

```css
.zcc-container {
  position: relative;
  width: 100%;
  max-width: 400px;
  height: 600px;
}

.zcc-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
```

### Collapsible Panel

```javascript
function toggleSoftphone() {
  const container = document.querySelector('.zcc-container');
  container.classList.toggle('collapsed');
}
```

```css
.zcc-container.collapsed {
  width: 60px;
  height: 60px;
}

.zcc-container.collapsed iframe {
  display: none;
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Iframe blank | Check CSP allows frame-src for zoom.us |
| No audio/video | Ensure allow attributes include camera/microphone |
| PostMessage not working | Verify origin is exactly 'https://zoom.us' |
| Agent not authenticated | Check SSO/OAuth integration |

## Sample Application

See the official [Zoom CRM-Sample](https://github.com/zoom/CRM-Sample) for a complete Next.js implementation.

**Branch:** `Contact-Center`

```bash
git clone --branch Contact-Center --single-branch https://github.com/zoom/CRM-Sample.git
cd CRM-Sample
npm install
cp .env.sample .env
# Edit .env with your credentials
npm run dev
```

### Key Files

| File | Description |
|------|-------------|
| `src/components/SmartEmbed.js` | Smart Embed iframe component |
| `src/app/layout.js` | App layout with Smart Embed sidebar |
| `src/app/api/auth/[...nextauth]/route.js` | NextAuth Zoom OAuth with token refresh |
| `src/app/api/call-history/route.js` | Contact Center engagement history API |

## Resources

- **Smart Embed docs:** https://developers.zoom.us/docs/contact-center/smart-embed/
- **CRM Sample repo:** https://github.com/zoom/CRM-Sample (branch: Contact-Center)
- **CRM Integration guide:** https://support.zoom.us/hc/en-us/categories/4423802887949

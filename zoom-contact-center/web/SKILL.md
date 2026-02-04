# Contact Center SDK for Web

JavaScript SDK for embedding video and chat engagement in web applications.

> **Parent skill:** [zoom-contact-center](../SKILL.md)
> **Official docs:** https://developers.zoom.us/docs/contact-center/web/

## Prerequisites

- Contact Center license with entry ID
- Verified subdomain
- CSP headers configured on your web server

## CSP Configuration

Add to your web server (nginx example):

```nginx
add_header 'Content-Security-Policy' "default-src 'self';base-uri 'self';worker-src blob:;style-src 'self' 'unsafe-inline';script-src 'self' 'unsafe-inline' 'unsafe-eval' https://zoom.us *.zoom.us dmogdx0jrul3u.cloudfront.net blob:;connect-src 'self' https://zoom.us https://*.zoom.us wss://*.zoom.us;img-src 'self' https:;media-src 'self' https:;font-src 'self' https:;";
```

**Note:** Use `wasm-unsafe-eval` instead of `unsafe-eval` if browser supports it.

### CSP Error

If you see this error, CSP is not configured:

```
CompileError: WebAssembly.instantiate(): Refused to compile or instantiate WebAssembly module because 'unsafe-eval' is not an allowed source...
```

## Installation

### CDN

```html
<script src="https://static.zoom.us/zcc/web-sdk/v2/zcc-web-sdk.min.js"></script>
```

### NPM

```bash
npm install @zoom/contact-center-sdk
```

## Quick Start

### Video Client

```javascript
const client = new ZoomContactCenterClient();

await client.init({
  entryId: 'your-video-entry-id',
  onReady: () => {
    console.log('Client ready');
  },
  onError: (error) => {
    console.error('Error:', error);
  }
});

// Start video engagement
await client.startVideoEngagement({
  displayName: 'Customer Name',
  // Optional: custom data
  customData: {
    accountId: '12345',
    priority: 'high'
  }
});
```

### Chat Client

```javascript
const chatClient = new ZoomContactCenterChatClient();

await chatClient.init({
  entryId: 'your-chat-entry-id'
});

// Start chat
await chatClient.startChat({
  displayName: 'Customer Name'
});

// Send message
await chatClient.sendMessage('Hello, I need help');

// Listen for messages
chatClient.on('message', (message) => {
  console.log('Agent:', message.content);
});
```

## Events

### Video Events

| Event | Description |
|-------|-------------|
| `onReady` | Client initialized and ready |
| `onError` | Error occurred |
| `onConnected` | Connected to agent |
| `onDisconnected` | Call ended |
| `onWaiting` | In queue waiting for agent |
| `onAgentJoined` | Agent joined the call |

### Chat Events

| Event | Description |
|-------|-------------|
| `message` | New message received |
| `typing` | Agent is typing |
| `connected` | Connected to agent |
| `ended` | Chat session ended |

## UI Customization

### Custom Button

```html
<button id="contact-us" onclick="startSupport()">
  Contact Us
</button>

<script>
async function startSupport() {
  await client.startVideoEngagement({
    displayName: 'Customer'
  });
}
</script>
```

### Embed in Container

```html
<div id="zcc-container"></div>

<script>
await client.init({
  entryId: 'your-entry-id',
  container: document.getElementById('zcc-container')
});
</script>
```

## Browser Support

| Browser | Minimum Version |
|---------|-----------------|
| Chrome | 80+ |
| Firefox | 78+ |
| Safari | 14+ |
| Edge | 80+ |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| WebAssembly error | Add CSP header with `unsafe-eval` |
| Camera/mic blocked | Ensure HTTPS and permissions granted |
| Connection failed | Check entry ID and verified domain |

## Resources

- **Get Started:** https://developers.zoom.us/docs/contact-center/web/get-started/
- **Chat:** https://developers.zoom.us/docs/contact-center/web/chat/
- **Video:** https://developers.zoom.us/docs/contact-center/web/video/

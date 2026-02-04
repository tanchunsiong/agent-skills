# Contact Center SDK Learnings

Critical discoveries made during implementation that should inform future development.

## CSP Headers (CRITICAL)

The Contact Center Web SDK uses WebAssembly, which requires specific Content Security Policy headers:

```javascript
const CSP_HEADER = [
  "default-src 'self'",
  "base-uri 'self'",
  "worker-src blob:",
  "style-src 'self' 'unsafe-inline'",
  // WebAssembly requires unsafe-eval (or wasm-unsafe-eval if browser supports)
  "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://zoom.us https://*.zoom.us https://dmogdx0jrul3u.cloudfront.net blob:",
  "connect-src 'self' https://zoom.us https://*.zoom.us wss://*.zoom.us",
  "frame-src 'self' https://zoom.us https://*.zoom.us https://applications.zoom.us",
  "img-src 'self' https: data: blob:",
  "media-src 'self' https: blob:",
  "font-src 'self' https: data:",
].join(';');
```

**Without these headers**: SDK loads but fails with "WebAssembly compilation error" or silent failures.

## SDK CDN URL

**Web SDK**: `https://static.zoom.us/zcc/web-sdk/v2/zcc-web-sdk.min.js`

This provides:
- `ZoomContactCenterClient` - For video engagements
- `ZoomContactCenterChatClient` - For chat and ZVA engagements

## Smart Embed URL (Agent-facing)

**Contact Center Smart Embed**: 
```
https://zoom.us/cci/callbar/crm/?origin={YOUR_ORIGIN}
```

**NOT the same as Zoom Phone** (which uses a different URL pattern at applications.zoom.us).

### Required iframe Attributes

```html
<iframe 
  src="https://zoom.us/cci/callbar/crm/?origin=https://your-app.com"
  sandbox="allow-forms allow-popups allow-popups-to-escape-sandbox allow-scripts allow-same-origin allow-downloads"
  allow="autoplay; microphone; camera; display-capture; midi; encrypted-media; clipboard-write;"
></iframe>
```

## Entry ID Locations

| Entry Type | Admin Panel Location |
|------------|---------------------|
| Video | Contact Center > Digital Channels > Video Engagement > Entry ID |
| Chat | Contact Center > Digital Channels > Chat Widget > Entry ID |
| ZVA | AI Management > Virtual Agents > Preferences > Entry ID |

## SDK API Patterns

### Consumer Video Engagement

```javascript
const client = new ZoomContactCenterClient();

await client.init({
  entryId: 'your-video-entry-id',
  onReady: () => console.log('Ready'),
  onError: (error) => console.error('Error:', error)
});

await client.startVideoEngagement({
  displayName: 'Customer Name',
  container: document.getElementById('video-container'),
  customData: { source: 'web', timestamp: new Date().toISOString() }
});
```

### Consumer Chat Engagement

```javascript
const chatClient = new ZoomContactCenterChatClient();

await chatClient.init({ entryId: 'your-chat-entry-id' });

await chatClient.startChat({
  displayName: 'Customer Name',
  container: document.getElementById('chat-container')
});

chatClient.on('message', (msg) => console.log('Message:', msg));
chatClient.on('connected', () => console.log('Connected to agent'));
chatClient.on('ended', () => console.log('Chat ended'));
```

## iOS SDK Corrections

The iOS SDK uses `ZoomCCInterface.sharedInstance()`, NOT a fictional `ZoomContactCenter.shared` pattern.

**Correct pattern**:
```swift
let zccInterface = ZoomCCInterface.sharedInstance()
let item = ZoomCCItem(id: "entry-id", type: .chat, isVideoOn: false)
let context = ZoomCCContext(displayName: "Customer", items: [item])
zccInterface.join(with: context)
```

## Android SDK Corrections

The Android SDK uses `ZoomCCInterface.INSTANCE`, NOT a builder pattern.

**Correct pattern**:
```kotlin
val item = ZoomCCItem("entry-id", ZoomCCItem.ServiceType.CHAT, false)
ZoomCCInterface.INSTANCE.init(context, items = listOf(item)) { success, error ->
    if (success) {
        ZoomCCInterface.INSTANCE.getZoomCCChatService()?.startChat(displayName = "Customer")
    }
}
```

## CRM-Sample Repository

Official Zoom sample code: `https://github.com/zoom/CRM-Sample`

**Branch**: `Contact-Center` (capitalized, not lowercase)

Contains:
- Smart Embed iframe integration
- Token generation for authenticated users
- Event listeners for call state changes

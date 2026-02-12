---
name: zoom-cobrowse-sdk
description: "Zoom Cobrowse SDK for web - JavaScript SDK for real-time collaborative browsing between agents and customers. Features include annotation tools, privacy masking, remote assist, and PIN-based session sharing."
triggers:
  - "cobrowse"
  - "co-browse"
  - "collaborative browsing"
  - "agent assist"
  - "customer support screen share"
  - "zoom cobrowse"
---

# Zoom Cobrowse SDK - Web Development

Expert guidance for implementing collaborative browsing with the Zoom Cobrowse SDK. This SDK enables support agents to view and interact with a customer's browser session in real-time, with privacy controls and annotation tools.

**Official Documentation**: https://developers.zoom.us/docs/zoom-cobrowse-sdk/  
**API Reference**: https://marketplacefront.zoom.us/sdk/cobrowse/  
**Quickstart Repository**: https://github.com/zoom/CobrowseSDK-Quickstart  
**Auth Endpoint Sample**: https://github.com/zoom/cobrowsesdk-auth-endpoint-sample

## Quick Links

**New to Cobrowse SDK? Follow this path:**

1. **[Get Started Guide](get-started.md)** - Complete setup from credentials to first session
2. **[Session Lifecycle](concepts/session-lifecycle.md)** - Understanding customer and agent flows
3. **[JWT Authentication](concepts/jwt-authentication.md)** - Token generation and security
4. **[Customer Integration](examples/customer-integration.md)** - Integrate SDK into your website
5. **[Agent Integration](examples/agent-integration.md)** - Set up agent portal (iframe or npm)

**Core Concepts:**
- **[Two Roles Pattern](concepts/two-roles-pattern.md)** - Customer vs Agent architecture
- **[Session Lifecycle](concepts/session-lifecycle.md)** - PIN generation, connection, reconnection
- **[JWT Authentication](concepts/jwt-authentication.md)** - SDK Key vs API Key, role_type, claims
- **[Distribution Methods](concepts/distribution-methods.md)** - CDN vs npm (BYOP)

**Features:**
- **[Annotation Tools](examples/annotations.md)** - Drawing, highlighting, pointer tools
- **[Privacy Masking](examples/privacy-masking.md)** - Hide sensitive fields from agents
- **[Remote Assist](examples/remote-assist.md)** - Agent can scroll customer's page
- **[Multi-Tab Persistence](examples/multi-tab-persistence.md)** - Session continues across tabs
- **[BYOP Mode](examples/byop-custom-pin.md)** - Bring Your Own PIN with npm integration

**Troubleshooting:**
- **[Common Issues](troubleshooting/common-issues.md)** - Quick diagnostics and solutions
- **[Error Codes](troubleshooting/error-codes.md)** - Complete error reference
- **[CORS and CSP](troubleshooting/cors-csp.md)** - Cross-origin and security policy configuration
- **[Browser Compatibility](troubleshooting/browser-compatibility.md)** - Supported browsers and limitations

**Reference:**
- **[API Reference](references/api-reference.md)** - Complete SDK methods and events
- **[Settings Reference](references/settings-reference.md)** - All initialization settings
- **[INDEX.md](INDEX.md)** - Complete documentation navigation

## SDK Overview

The Zoom Cobrowse SDK is a JavaScript library that provides:

- **Real-Time Co-Browsing**: Agent sees customer's browser activity live
- **PIN-Based Sessions**: Secure 6-digit PIN for customer-to-agent connection
- **Annotation Tools**: Drawing, highlighting, vanishing pen, rectangle, color picker
- **Privacy Masking**: CSS selector-based masking of sensitive form fields
- **Remote Assist**: Agent can scroll customer's page (with consent)
- **Multi-Tab Persistence**: Session continues when customer opens new tabs
- **Auto-Reconnection**: Session recovers from page refresh (2-minute window)
- **Session Events**: Real-time events for session state changes
- **HTTPS Required**: Secure connections (HTTP only works on localhost)
- **No Plugins**: Pure JavaScript, no browser extensions needed

## Two Roles Architecture

Cobrowse has **two distinct roles**, each with different integration patterns:

| Role | role_type | Integration | JWT Required | Purpose |
|------|-----------|-------------|--------------|---------|
| **Customer** | 1 | Website integration (CDN or npm) | Yes | User who shares their browser session |
| **Agent** | 2 | Iframe (CDN) or npm (BYOP only) | Yes | Support staff who views/assists customer |

**Key Insight**: Customer and agent use **different integration methods** but the same JWT authentication pattern.

## Prerequisites

### Platform Requirements

- **Supported Browsers**:
  - Chrome 80+ ✓
  - Firefox 78+ ✓
  - Safari 14+ ✓
  - Edge 80+ ✓
  - Internet Explorer ✗ (not supported)

- **Network Requirements**:
  - HTTPS required (HTTP works on localhost only)
  - Allow cross-origin requests to `*.zoom.us`
  - CSP headers must allow Zoom domains (see [CORS and CSP guide](troubleshooting/cors-csp.md))

- **Third-Party Cookies**:
  - Must enable third-party cookies for refresh reconnection
  - Privacy mode may limit certain features

### Zoom Account Requirements

1. **Zoom Workplace Account** with SDK Universal Credit
2. **Video SDK App** created in Zoom Marketplace
3. **Cobrowse SDK Credentials** from the app's Cobrowse tab

**Note**: Cobrowse SDK is a **feature of Video SDK** (not a separate product).

### Credentials Overview

You'll receive **4 credentials** from Zoom Marketplace → Video SDK App → Cobrowse tab:

| Credential | Type | Used For | Exposure Safe? |
|------------|------|----------|----------------|
| **SDK Key** | Public | CDN URL, JWT `app_key` claim | ✓ Yes (client-side) |
| **SDK Secret** | Private | Sign JWTs | ✗ No (server-side only) |
| **API Key** | Private | REST API calls (optional) | ✗ No (server-side only) |
| **API Secret** | Private | REST API calls (optional) | ✗ No (server-side only) |

**Critical**: SDK Key is **public** (embedded in CDN URL), but SDK Secret must **never** be exposed client-side.

## Quick Start

### Step 1: Get SDK Credentials

1. Go to [Zoom Marketplace](https://marketplace.zoom.us/)
2. Open your **Video SDK App** (or create one)
3. Navigate to the **Cobrowse** tab
4. Copy your credentials:
   - SDK Key
   - SDK Secret
   - API Key (optional)
   - API Secret (optional)

### Step 2: Set Up Token Server

Deploy a server-side endpoint to generate JWTs. Use the official sample:

```bash
git clone https://github.com/zoom/cobrowsesdk-auth-endpoint-sample.git
cd cobrowsesdk-auth-endpoint-sample
npm install

# Create .env file
cat > .env << EOF
ZOOM_SDK_KEY=your_sdk_key_here
ZOOM_SDK_SECRET=your_sdk_secret_here
PORT=4000
EOF

npm start
```

**Token endpoint:**
```javascript
// POST http://localhost:4000
{
  "role": 1,           // 1 = customer, 2 = agent
  "userId": "user123",
  "userName": "John Doe"
}

// Response
{
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Step 3: Customer Side Integration (CDN)

```html
<!DOCTYPE html>
<html>
<head>
  <title>Customer - Cobrowse Demo</title>
  <script type="module">
    const ZOOM_SDK_KEY = 'YOUR_SDK_KEY';
    
    // Load SDK from CDN
    (function(r, a, b, f, c, d) {
      r[f] = r[f] || { init: function() { r.ZoomCobrowseSDKInitArgs = arguments }};
      var fragment = a.createDocumentFragment();
      function loadJs(url) {
        c = a.createElement(b);
        d = a.getElementsByTagName(b)[0];
        c["async"] = false;
        c.src = url;
        fragment.appendChild(c);
      }
      loadJs(`https://us01-zcb.zoom.us/static/resource/sdk/${ZOOM_SDK_KEY}/js/2.13.2`);
      d.parentNode.insertBefore(fragment, d);
    })(window, document, "script", "ZoomCobrowseSDK");
  </script>
</head>
<body>
  <h1>Customer Support</h1>
  <button id="cobrowse-btn" disabled>Loading...</button>
  
  <!-- Sensitive fields - will be masked from agent -->
  <label>SSN: <input type="text" class="pii-mask" placeholder="XXX-XX-XXXX"></label>
  <label>Credit Card: <input type="text" class="pii-mask" placeholder="XXXX-XXXX-XXXX-XXXX"></label>
  
  <script type="module">
    let sessionRef = null;
    
    const settings = {
      allowAgentAnnotation: true,
      allowCustomerAnnotation: true,
      piiMask: {
        maskCssSelectors: ".pii-mask",
        maskType: "custom_input"
      }
    };
    
    ZoomCobrowseSDK.init(settings, function({ success, session, error }) {
      if (success) {
        sessionRef = session;
        
        // Listen for PIN code
        session.on("pincode_updated", (payload) => {
          console.log("PIN Code:", payload.pincode);
          alert(`Share this PIN with agent: ${payload.pincode}`);
        });
        
        // Listen for session events
        session.on("session_started", () => console.log("Session started"));
        session.on("agent_joined", () => console.log("Agent joined"));
        session.on("agent_left", () => console.log("Agent left"));
        session.on("session_ended", () => console.log("Session ended"));
        
        document.getElementById("cobrowse-btn").disabled = false;
        document.getElementById("cobrowse-btn").innerText = "Start Cobrowse Session";
      } else {
        console.error("SDK init failed:", error);
      }
    });
    
    document.getElementById("cobrowse-btn").addEventListener("click", async () => {
      // Fetch JWT from your server
      const response = await fetch("http://localhost:4000", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          role: 1,
          userId: "customer_" + Date.now(),
          userName: "Customer"
        })
      });
      const { token } = await response.json();
      
      // Start cobrowse session
      sessionRef.start({ sdkToken: token });
    });
  </script>
</body>
</html>
```

### Step 4: Agent Side Integration (Iframe)

```html
<!DOCTYPE html>
<html>
<head>
  <title>Agent Portal</title>
</head>
<body>
  <h1>Agent Portal</h1>
  <iframe 
    id="agent-iframe"
    width="1024" 
    height="768"
    allow="autoplay *; camera *; microphone *; display-capture *; geolocation *;"
  ></iframe>
  
  <script>
    async function connectAgent() {
      // Fetch JWT from your server
      const response = await fetch("http://localhost:4000", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          role: 2,
          userId: "agent_" + Date.now(),
          userName: "Support Agent"
        })
      });
      const { token } = await response.json();
      
      // Load Zoom agent portal
      const iframe = document.getElementById("agent-iframe");
      iframe.src = `https://us01-zcb.zoom.us/sdkapi/zcb/frame-templates/desk?access_token=${token}`;
    }
    
    connectAgent();
  </script>
</body>
</html>
```

### Step 5: Test the Integration

1. Open **two separate browsers** (or incognito + normal)
2. **Customer browser**: Open customer page, click "Start Cobrowse Session"
3. **Customer browser**: Note the 6-digit PIN displayed
4. **Agent browser**: Open agent page, enter the PIN code
5. **Both browsers**: Session connects, agent can see customer's page
6. **Test features**: Annotations, data masking, remote assist

## Key Features

### 1. Annotation Tools

Both customer and agent can draw on the shared screen:

```javascript
const settings = {
  allowAgentAnnotation: true,      // Agent can draw
  allowCustomerAnnotation: true    // Customer can draw
};
```

**Available tools**:
- Pen (persistent)
- Vanishing pen (disappears after 4 seconds)
- Rectangle
- Color picker
- Eraser
- Undo/Redo

### 2. Privacy Masking

Hide sensitive fields from agents using CSS selectors:

```javascript
const settings = {
  piiMask: {
    maskType: "custom_input",           // Mask specific fields
    maskCssSelectors: ".pii-mask, #ssn", // CSS selectors
    maskHTMLAttributes: "data-sensitive=true" // HTML attributes
  }
};
```

**Supported masking**:
- Text nodes ✓
- Form inputs ✓
- Select elements ✓
- Images ✗ (not supported)
- Links ✗ (not supported)

### 3. Remote Assist

Agent can scroll the customer's page:

```javascript
const settings = {
  remoteAssist: {
    enable: true,
    enableCustomerConsent: true,        // Customer must approve
    remoteAssistTypes: ['scroll_page'], // Only scroll supported
    requireStopConfirmation: false      // Confirmation when stopping
  }
};
```

### 4. Multi-Tab Session Persistence

Session continues when customer opens new tabs:

```javascript
const settings = {
  multiTabSessionPersistence: {
    enable: true,
    stateCookieKey: '$$ZCB_SESSION$$'  // Cookie key (base64 encoded)
  }
};
```

## Session Lifecycle

### Customer Flow

1. **Load SDK** → CDN script loads `ZoomCobrowseSDK`
2. **Initialize** → `ZoomCobrowseSDK.init(settings, callback)`
3. **Fetch JWT** → Request token from your server (role_type=1)
4. **Start Session** → `session.start({ sdkToken })`
5. **PIN Generated** → `pincode_updated` event fires
6. **Share PIN** → Customer gives 6-digit PIN to agent
7. **Agent Joins** → `agent_joined` event fires
8. **Session Active** → Real-time synchronization begins
9. **End Session** → `session.end()` or agent leaves

### Agent Flow

1. **Fetch JWT** → Request token from your server (role_type=2)
2. **Load Iframe** → Point to Zoom agent portal with token
3. **Enter PIN** → Agent inputs customer's 6-digit PIN
4. **Connect** → `session_joined` event fires
5. **View Session** → Agent sees customer's browser
6. **Use Tools** → Annotations, remote assist, zoom
7. **Leave Session** → Click "Leave Cobrowse" button

### Session Recovery (Auto-Reconnect)

When customer refreshes the page:

```javascript
ZoomCobrowseSDK.init(settings, function({ success, session, error }) {
  if (success) {
    const sessionInfo = session.getSessionInfo();
    
    // Check if session is recoverable
    if (sessionInfo.sessionStatus === 'session_recoverable') {
      session.join();  // Auto-rejoin previous session
    } else {
      // Start new session
      session.start({ sdkToken });
    }
  }
});
```

**Recovery window**: 2 minutes. After 2 minutes, session ends.

## Critical Gotchas and Best Practices

### ⚠️ CRITICAL: SDK Secret Must Stay Server-Side

**Problem**: Developers often accidentally embed SDK Secret in frontend code.

**Solution**:
- ✓ **SDK Key** → Safe to expose (embedded in CDN URL)
- ✗ **SDK Secret** → Never expose (use for JWT signing server-side)

```javascript
// ❌ WRONG - Secret exposed in frontend
const jwt = signJWT(payload, 'YOUR_SDK_SECRET');  // Security risk!

// ✅ CORRECT - Secret stays on server
const response = await fetch('/api/token', {
  method: 'POST',
  body: JSON.stringify({ role: 1, userId, userName })
});
const { token } = await response.json();
```

### SDK Key vs API Key (Different Purposes!)

| Credential | Used For | JWT Claim |
|------------|----------|-----------|
| **SDK Key** | CDN URL, JWT `app_key` | `app_key: "SDK_KEY"` |
| **API Key** | REST API calls (optional) | Not used in JWT |

**Common mistake**: Using API Key instead of SDK Key in JWT `app_key` claim.

### Session Limits

| Limit | Value | What Happens |
|-------|-------|--------------|
| Customers per session | 1 | Error 1012: `SESSION_CUSTOMER_COUNT_LIMIT` |
| Agents per session | 5 | Error 1013: `SESSION_AGENT_COUNT_LIMIT` |
| Active sessions per browser | 1 | Error 1004: `SESSION_COUNT_LIMIT` |
| PIN code length | 10 chars max | Error 1008: `SESSION_PIN_INVALID_FORMAT` |

### Session Timeout Behavior

| Event | Timeout | What Happens |
|-------|---------|--------------|
| Agent waiting for customer | 3 minutes | Session ends automatically |
| Page refresh reconnection | 2 minutes | Session ends if not reconnected |
| Reconnection attempts | 2 times max | Session ends after 2 failed attempts |

### HTTPS Requirement

**Problem**: SDK doesn't load on HTTP sites.

**Solution**:
- Production: Use HTTPS ✓
- Development: Use `localhost` (HTTP works) ✓
- Development: Use `https://127.0.0.1` with self-signed cert ✓

### Third-Party Cookies Required

**Problem**: Refresh reconnection doesn't work.

**Solution**: Enable third-party cookies in browser settings.

**Affected scenarios**:
- Browser privacy mode
- Safari with "Prevent cross-site tracking" enabled
- Chrome with "Block third-party cookies" enabled

### Distribution Method Confusion

| Method | Use Case | Agent Integration | BYOP Required |
|--------|----------|-------------------|---------------|
| **CDN** | Most use cases | Zoom-hosted iframe | No (auto PIN) |
| **npm** | Custom agent UI, full control | Custom npm integration | Yes (required) |

**Key Insight**: If you want **npm** integration, you **must** use BYOP (Bring Your Own PIN) mode.

### Cross-Origin Iframe Handling

**Problem**: Cobrowse doesn't work in cross-origin iframes.

**Solution**: Inject SDK snippet into cross-origin iframes:

```html
<script>
const ZOOM_SDK_KEY = "YOUR_SDK_KEY_HERE";

(function(r,a,b,f,c,d){r[f]=r[f]||{init:function(){r.ZoomCobrowseSDKInitArgs=arguments}};
var fragment=a.createDocumentFragment();function loadJs(url) {c=a.createElement(b);d=a.getElementsByTagName(b)[0];c.async=false;c.src=url;fragment.appendChild(c);};
loadJs('https://us01-zcb.zoom.us/static/resource/sdk/${ZOOM_SDK_KEY}/js');d.parentNode.insertBefore(fragment,d);})(window,document,'script','ZoomCobrowseSDK');
</script>
```

**Same-origin iframes**: No extra setup needed.

## Known Limitations

### Synchronization Limits

**Not synchronized**:
- HTML5 Canvas elements
- WebGL content
- Audio and Video elements
- Shadow DOM
- PDF rendered with Canvas
- Web Components

**Partially synchronized**:
- Drop-down boxes (only selected result)
- Date pickers (only selected result)
- Color pickers (only selected result)

### Rendering Limits

- High-resolution images may be compressed
- Different screen sizes may cause CSS media query differences
- Cross-origin images may not render (CORS restrictions)
- Cross-origin fonts may not render (CORS restrictions)

### Masking Limits

**Supported**:
- Text nodes ✓
- Form inputs ✓
- Select elements ✓

**Not supported**:
- `<img>` elements ✗
- Links ✗

## Complete Documentation Library

This skill includes comprehensive guides organized by category:

### Core Concepts
- **[Two Roles Pattern](concepts/two-roles-pattern.md)** - Customer vs Agent architecture
- **[Session Lifecycle](concepts/session-lifecycle.md)** - Complete flow from start to end
- **[JWT Authentication](concepts/jwt-authentication.md)** - Token structure and signing
- **[Distribution Methods](concepts/distribution-methods.md)** - CDN vs npm (BYOP)

### Examples
- **[Customer Integration](examples/customer-integration.md)** - Complete customer-side setup
- **[Agent Integration](examples/agent-integration.md)** - Iframe and npm agent setups
- **[Annotations](examples/annotations.md)** - Drawing tools configuration
- **[Privacy Masking](examples/privacy-masking.md)** - Field masking patterns
- **[Remote Assist](examples/remote-assist.md)** - Agent page control
- **[Multi-Tab Persistence](examples/multi-tab-persistence.md)** - Cross-tab sessions
- **[BYOP Custom PIN](examples/byop-custom-pin.md)** - Custom PIN codes

### References
- **[API Reference](references/api-reference.md)** - Complete SDK methods and events
- **[Settings Reference](references/settings-reference.md)** - All initialization settings
- **[Error Codes](references/error-codes.md)** - Complete error reference
- **[Session Events](references/session-events.md)** - All event types

### Troubleshooting
- **[Common Issues](troubleshooting/common-issues.md)** - Quick diagnostics
- **[Error Codes](troubleshooting/error-codes.md)** - Error code reference
- **[CORS and CSP](troubleshooting/cors-csp.md)** - Cross-origin configuration
- **[Browser Compatibility](troubleshooting/browser-compatibility.md)** - Browser support

## Resources

- **Official Docs**: https://developers.zoom.us/docs/zoom-cobrowse-sdk/
- **API Reference**: https://marketplacefront.zoom.us/sdk/cobrowse/
- **Quickstart Repo**: https://github.com/zoom/CobrowseSDK-Quickstart
- **Auth Endpoint Sample**: https://github.com/zoom/cobrowsesdk-auth-endpoint-sample
- **Dev Forum**: https://devforum.zoom.us/
- **Developer Blog**: https://developers.zoom.us/blog/?category=zoom-cobrowse-sdk

---

**Need help?** Start with [INDEX.md](INDEX.md) for complete navigation.

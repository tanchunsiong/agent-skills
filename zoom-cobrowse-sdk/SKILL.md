---
name: zoom-cobrowse-sdk
description: |
  Zoom Cobrowse SDK for collaborative browsing. Enables agents to view and interact with 
  customer's browser in real-time for support, form completion, and guided walkthroughs.
  Web-based, no plugins required. Feature of Video SDK.
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
| **Privacy masking** | Hide sensitive fields (CSS selector-based) |
| **PIN-based access** | Secure session initiation |
| **No plugins** | Pure JavaScript CDN, no npm package |

## Platform Support

| Platform | Supported |
|----------|-----------|
| Web (Chrome 80+) | Yes |
| Web (Firefox 78+) | Yes |
| Web (Safari 14+) | Yes |
| Web (Edge 80+) | Yes |
| iOS Native | No |
| Android Native | No |

**Requirements**: HTTPS required (HTTP only works on localhost)

## Roles

| Role | role_type | Description |
|------|-----------|-------------|
| **Customer** | 1 | User on your website who shares their session |
| **Agent** | 2 | Support staff who views/assists customer |

## Credentials

Cobrowse SDK is a **feature of Video SDK** (not a separate product). Get credentials from:

**Zoom Marketplace → Your Video SDK App → Cobrowse tab**

You will find **4 credentials**:

| Credential | Type | Purpose |
|------------|------|---------|
| **SDK Key** | Public | Used in CDN URL and JWT `app_key` claim. Safe to expose client-side. |
| **SDK Secret** | Private | Used to sign JWTs. **Never expose client-side.** |
| **API Key** | Private | REST API authentication for session management (optional) |
| **API Secret** | Private | REST API authentication for session management (optional) |

### .env Template

```env
# SDK Credentials (Required for JWT generation)
ZOOM_SDK_KEY=your_sdk_key_here
ZOOM_SDK_SECRET=your_sdk_secret_here

# API Credentials (Optional - for REST API session management)
ZOOM_API_KEY=your_api_key_here
ZOOM_API_SECRET=your_api_secret_here

# Server Config
PORT=4000
```

### When to Use Each Credential

| Task | Credentials Needed |
|------|-------------------|
| Load SDK in browser | SDK Key (embedded in CDN URL) |
| Generate customer/agent JWT | SDK Key + SDK Secret |
| Create sessions via REST API | API Key + API Secret |
| Get session reports via REST API | API Key + API Secret |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ CUSTOMER (Browser)                                          │
│ • SDK Key → Embedded in CDN URL                             │
│ • JWT Token → Received from your server                     │
│ • ZoomCobrowseSDK.init() → session.start({sdkToken})        │
│ • Generates PIN → Share with agent                          │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼ fetch token (role=1)
┌─────────────────────────────────────────────────────────────┐
│ YOUR SERVER                                                 │
│ • SDK Key + SDK Secret → Generate JWT                       │
│ • API Key + API Secret → REST API calls (optional)          │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼ fetch token (role=2)
┌─────────────────────────────────────────────────────────────┐
│ AGENT (Browser)                                             │
│ • JWT Token → Received from your server                     │
│ • iframe src → Zoom agent portal with access_token          │
│ • Enter PIN → Connect to customer session                   │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Get Credentials

1. Go to [Zoom Marketplace](https://marketplace.zoom.us/)
2. Open your **Video SDK App** (or create one)
3. Navigate to the **Cobrowse** tab
4. Copy SDK Key, SDK Secret (and optionally API Key, API Secret)

### 2. Set Up Token Server

Deploy the auth endpoint: [cobrowsesdk-auth-endpoint-sample](https://github.com/zoom/cobrowsesdk-auth-endpoint-sample)

```bash
git clone https://github.com/zoom/cobrowsesdk-auth-endpoint-sample.git
cd cobrowsesdk-auth-endpoint-sample
npm install
# Add ZOOM_SDK_KEY and ZOOM_SDK_SECRET to .env
npm run start
```

**Token Request:**
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

### 3. Customer Side Integration

```html
<!DOCTYPE html>
<html>
<head>
  <script type="module">
    const ZOOM_SDK_KEY = 'YOUR_SDK_KEY';
    
    // Load SDK from CDN (no npm package available)
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
      loadJs(`https://us01-zcb.zoom.us/static/resource/sdk/${ZOOM_SDK_KEY}/js/2.10.0`);
      d.parentNode.insertBefore(fragment, d);
    })(window, document, "script", "ZoomCobrowseSDK");
  </script>
</head>
<body>
  <button id="cobrowse-btn" disabled>Loading...</button>
  
  <!-- Sensitive fields - will be masked from agent -->
  <input type="text" class="hide-me" placeholder="SSN">
  
  <script type="module">
    let sessionRef = null;
    
    const settings = {
      allowAgentAnnotation: true,
      allowCustomerAnnotation: true,
      piiMask: {
        maskCssSelectors: ".hide-me",
        maskType: "custom_input"
      }
    };
    
    ZoomCobrowseSDK.init(settings, function({ success, session, error }) {
      if (success) {
        sessionRef = session;
        
        session.on("pincode_updated", (payload) => {
          console.log("PIN Code:", payload.pincode);
          alert(`Share this PIN with agent: ${payload.pincode}`);
        });
        
        document.getElementById("cobrowse-btn").disabled = false;
        document.getElementById("cobrowse-btn").innerText = "Start Cobrowse";
      } else {
        console.error("SDK init failed:", error);
      }
    });
    
    document.getElementById("cobrowse-btn").addEventListener("click", async () => {
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
      
      sessionRef.start({ sdkToken: token });
    });
  </script>
</body>
</html>
```

### 4. Agent Side Integration

Agent uses an iframe to connect:

```html
<!DOCTYPE html>
<html>
<head>
  <title>Agent Portal</title>
</head>
<body>
  <iframe 
    id="agent-iframe"
    width="1024" 
    height="768"
    allow="autoplay *; camera *; microphone *; display-capture *; geolocation *;"
  ></iframe>
  
  <script>
    async function connectAgent() {
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
      
      const iframe = document.getElementById("agent-iframe");
      iframe.src = `https://us01-zcb.zoom.us/sdkapi/zcb/frame-templates/desk?access_token=${token}`;
    }
    
    connectAgent();
  </script>
</body>
</html>
```

## SDK Distribution

**CDN only** - No npm package exists.

The SDK Key is embedded in the CDN URL:
```
https://us01-zcb.zoom.us/static/resource/sdk/${SDK_KEY}/js/2.10.0
```

## SDK Settings

| Setting | Type | Description |
|---------|------|-------------|
| `allowAgentAnnotation` | boolean | Allow agent to draw/annotate |
| `allowCustomerAnnotation` | boolean | Allow customer to draw/annotate |
| `piiMask.maskCssSelectors` | string | CSS selector for fields to mask |
| `piiMask.maskType` | string | `"custom_input"` for input masking |

## Session Events

| Event | Payload | Description |
|-------|---------|-------------|
| `pincode_updated` | `{ pincode }` | PIN code generated/updated |
| `session_started` | - | Co-browse session started |
| `session_ended` | - | Co-browse session ended |
| `agent_joined` | - | Agent connected to session |
| `agent_left` | - | Agent disconnected |

## JWT Token Structure

```javascript
// Header
{ "alg": "HS256", "typ": "JWT" }

// Payload
{
  "app_key": "YOUR_SDK_KEY",    // SDK Key (not API Key)
  "role_type": 1,               // 1 = customer, 2 = agent
  "user_id": "unique_user_id",
  "user_name": "Display Name",
  "iat": 1729159092,            // Issued at
  "exp": 1729166292             // Expiration (30min - 48hr)
}
```

**Sign with**: SDK Secret (not API Secret)

## Privacy Masking

Hide sensitive fields from agents using CSS selectors:

```html
<input type="text" class="pii-field" placeholder="SSN">
<input type="password" class="pii-field" placeholder="Password">
<div class="pii-field">Credit Card: 4111-xxxx-xxxx-1234</div>
```

```javascript
const settings = {
  piiMask: {
    maskCssSelectors: ".pii-field",
    maskType: "custom_input"
  }
};
```

## Common Issues

| Issue | Solution |
|-------|----------|
| SDK not loading | Verify SDK Key is correct and embedded in CDN URL |
| Token generation fails | Use SDK Secret (not API Secret) to sign JWT |
| Agent can't connect | Check PIN is correct and token hasn't expired |
| Fields not masked | Verify CSS selector matches elements |

## Use Cases

- Customer support troubleshooting
- Form completion assistance
- Product demos and walkthroughs
- Onboarding guidance
- Technical support

## Sample Repositories

| Repository | Description |
|------------|-------------|
| [CobrowseSDK-Quickstart](https://github.com/zoom/CobrowseSDK-Quickstart) | Customer + Agent demo app |
| [cobrowsesdk-auth-endpoint-sample](https://github.com/zoom/cobrowsesdk-auth-endpoint-sample) | JWT token server |

## Resources

- **Official docs**: https://developers.zoom.us/docs/cobrowse-sdk/
- **Quickstart repo**: https://github.com/zoom/CobrowseSDK-Quickstart
- **Auth endpoint**: https://github.com/zoom/cobrowsesdk-auth-endpoint-sample
- **Developer blog**: https://developers.zoom.us/blog/?category=cobrowse-sdk

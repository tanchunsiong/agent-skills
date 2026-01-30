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
| **Privacy masking** | Hide sensitive fields (CSS selector-based) |
| **PIN-based access** | Secure session initiation |
| **No plugins** | Pure JavaScript, no downloads |

## Roles

| Role | role_type | Description |
|------|-----------|-------------|
| **Customer** | 1 | User on your website who shares their session |
| **Agent** | 2 | Support staff who views/assists customer |

## Prerequisites

- SDK Universal Credit added to Zoom Workplace account
- SDK Key and Secret from web portal
- Token server for JWT generation
- Website to integrate SDK

## Architecture

```
Customer Side                    Agent Side
─────────────                    ──────────
ZoomCobrowseSDK.init()          iframe with access_token
       │                               │
session.start({sdkToken})        Agent Portal UI
       │                               │
   PIN generated ──────────────► Enter PIN to connect
       │                               │
   Co-browse session ◄─────────► View & annotate
```

## Quick Start

### 1. Get Credentials

1. Add SDK Universal Credit to your Zoom account
2. Go to **Advanced** → **Zoom CPaaS** → **Manage**
3. Click **Build App** and get SDK Key/Secret

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
    
    // Load SDK dynamically
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
    
    // SDK settings
    const settings = {
      allowAgentAnnotation: true,
      allowCustomerAnnotation: true,
      piiMask: {
        maskCssSelectors: ".hide-me",  // CSS selector for fields to mask
        maskType: "custom_input"
      }
    };
    
    // Initialize SDK
    ZoomCobrowseSDK.init(settings, function({ success, session, error }) {
      if (success) {
        sessionRef = session;
        
        // Listen for PIN code updates
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
    
    // Start session on button click
    document.getElementById("cobrowse-btn").addEventListener("click", async () => {
      // Get token from your auth server
      const response = await fetch("http://localhost:4000", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          role: 1,  // Customer
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
    // Get agent token from your auth server
    async function connectAgent() {
      const response = await fetch("http://localhost:4000", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          role: 2,  // Agent
          userId: "agent_" + Date.now(),
          userName: "Support Agent"
        })
      });
      const { token } = await response.json();
      
      // Load agent portal in iframe
      const iframe = document.getElementById("agent-iframe");
      iframe.src = `https://us01-zcb.zoom.us/sdkapi/zcb/frame-templates/desk?access_token=${token}`;
    }
    
    connectAgent();
  </script>
</body>
</html>
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
  "app_key": "YOUR_SDK_KEY",
  "role_type": 1,              // 1 = customer, 2 = agent
  "user_id": "unique_user_id",
  "user_name": "Display Name",
  "iat": 1729159092,           // Issued at
  "exp": 1729166292            // Expiration (30min - 48hr)
}
```

## Privacy Masking

Hide sensitive fields from agents using CSS selectors:

```html
<!-- Add class to sensitive elements -->
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

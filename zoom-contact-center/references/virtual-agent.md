# Zoom Virtual Agent

AI-powered conversational chatbot for customer self-service.

## Overview

Zoom Virtual Agent (ZVA) is an AI-powered conversational agent that provides automated customer support across chat and voice channels. It can be deployed standalone or as part of Zoom Contact Center.

## Key Capabilities

| Capability | Description |
|------------|-------------|
| **Natural Language Understanding** | Context-aware conversations with intent recognition |
| **Multi-Channel** | Works on chat and voice (including Zoom Phone) |
| **Task Execution** | Book appointments, check inventory, process requests |
| **Seamless Handoff** | Transfer to human agents with full context |
| **24/7 Availability** | Always-on automated support |
| **Multi-Language** | Growing list of supported languages |

## Deployment Options

| Option | Description |
|--------|-------------|
| **Standalone** | ZVA without full Contact Center |
| **Contact Center Add-On** | Integrated with Zoom Contact Center |

## SDKs

### Web SDK

Embed Virtual Agent chat widget in web pages.

```javascript
// Initialize Virtual Agent widget
const zva = new ZoomVirtualAgent({
  apiKey: 'YOUR_API_KEY',
  agentId: 'YOUR_AGENT_ID'
});

// Open chat widget
zva.open();

// Send message programmatically
zva.sendMessage('Help me with my order');

// Close widget
zva.close();
```

**Documentation**: https://developers.zoom.us/docs/virtual-agent/web/chat/

### iOS SDK

Native iOS integration for Virtual Agent.

**Sample Repository**: https://github.com/zoom/virtual-assistant-iOS-sample

```swift
import ZoomVirtualAgent

let virtualAgent = ZVAClient(
    apiKey: "YOUR_API_KEY",
    agentId: "YOUR_AGENT_ID"
)

// Start conversation
virtualAgent.startConversation { result in
    switch result {
    case .success(let session):
        print("Session started: \(session.id)")
    case .failure(let error):
        print("Error: \(error)")
    }
}
```

### Android SDK

Native Android integration for Virtual Agent.

**Sample Repository**: https://github.com/zoom/virtual-assistant-android-sample

```kotlin
import com.zoom.virtualagent.ZVAClient

val virtualAgent = ZVAClient.Builder()
    .apiKey("YOUR_API_KEY")
    .agentId("YOUR_AGENT_ID")
    .build()

// Start conversation
virtualAgent.startConversation(object : ZVACallback {
    override fun onSuccess(session: ZVASession) {
        Log.d("ZVA", "Session started: ${session.id}")
    }
    
    override fun onError(error: ZVAError) {
        Log.e("ZVA", "Error: ${error.message}")
    }
})
```

## REST API

### Base URL

```
https://api.zoom.us/v2/
```

### Authentication

Server-to-Server OAuth (JWT apps deprecated).

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/virtual_agent/agents` | List virtual agents |
| GET | `/virtual_agent/agents/{agentId}` | Get agent details |
| POST | `/virtual_agent/conversations` | Start conversation |
| GET | `/virtual_agent/conversations/{id}` | Get conversation |
| POST | `/virtual_agent/knowledge_bases` | Create knowledge base |
| GET | `/virtual_agent/reports` | Get analytics |

### Example: Start Conversation

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/virtual_agent/conversations',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      agent_id: 'agent_abc123',
      channel: 'web',
      customer: {
        name: 'John Doe',
        email: 'john@example.com'
      },
      initial_message: 'I need help with my order'
    })
  }
);

const conversation = await response.json();
// { "conversation_id": "conv_xyz", "session_url": "..." }
```

## Knowledge Base Integration

### Web Sync

Sync existing documentation to Virtual Agent:

```javascript
// Create knowledge base from web content
await fetch('https://api.zoom.us/v2/virtual_agent/knowledge_bases', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Product Documentation',
    type: 'web_sync',
    source_url: 'https://docs.yourcompany.com',
    sync_frequency: 'daily'
  })
});
```

### Custom API

Connect to your backend systems:

```javascript
// Create API-connected knowledge base
await fetch('https://api.zoom.us/v2/virtual_agent/knowledge_bases', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Order System',
    type: 'api',
    api_endpoint: 'https://api.yourcompany.com/orders',
    auth_type: 'bearer'
  })
});
```

## Webhooks

| Event | Trigger |
|-------|---------|
| `virtual_agent.conversation_started` | New conversation began |
| `virtual_agent.conversation_ended` | Conversation completed |
| `virtual_agent.handoff_requested` | Transfer to human requested |
| `virtual_agent.intent_detected` | Customer intent identified |

### Webhook Payload Example

```json
{
  "event": "virtual_agent.handoff_requested",
  "payload": {
    "conversation_id": "conv_xyz",
    "agent_id": "agent_abc",
    "customer": {
      "name": "John Doe",
      "email": "john@example.com"
    },
    "reason": "complex_issue",
    "context": {
      "intent": "order_complaint",
      "summary": "Customer has issue with delayed order #12345"
    }
  }
}
```

## AI Concierge for Zoom Phone

Virtual Agent can serve as an AI receptionist for Zoom Phone:

| Feature | Description |
|---------|-------------|
| **Call Answering** | Automatically answer incoming calls 24/7 |
| **Natural Conversations** | Voice-based AI interactions |
| **Intelligent Routing** | Route callers based on intent |
| **Task Execution** | Book appointments, check info |
| **Seamless Handoff** | Transfer to human with context |

## Use Cases

| Use Case | Description |
|----------|-------------|
| **Customer Support** | Handle FAQs and common issues |
| **Appointment Booking** | Schedule and manage appointments |
| **Order Status** | Check order and shipping status |
| **Account Self-Service** | Password resets, account updates |
| **Product Information** | Answer product questions |
| **HR/IT Support** | Internal employee assistance |
| **Lead Qualification** | Qualify and route sales leads |

## Third-Party Integrations

Native integrations available:
- Salesforce
- Zendesk
- Intercom
- ServiceNow
- Jira
- Asana
- Box

## Required Scopes

| Scope | Description |
|-------|-------------|
| `virtual_agent:read` | Read agent and conversation data |
| `virtual_agent:write` | Create/update agents and knowledge bases |
| `virtual_agent:read:admin` | Account-wide read access |
| `virtual_agent:write:admin` | Account-wide write access |

## Resources

- **Official Documentation**: https://developers.zoom.us/docs/virtual-agent/
- **API Reference**: https://developers.zoom.us/docs/api/rest/reference/virtual-agent/methods/
- **Product Page**: https://zoom.com/en/products/virtual-agent/
- **iOS Sample**: https://github.com/zoom/virtual-assistant-iOS-sample
- **Android Sample**: https://github.com/zoom/virtual-assistant-android-sample

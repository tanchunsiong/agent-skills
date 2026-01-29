---
name: zoom-virtual-agent
description: |
  Zoom Virtual Agent API integration guide. Covers AI-powered conversational chatbots for automated 
  customer service, including intent management, knowledge bases, conversation flows, and analytics.
  Use when building AI customer service bots, automated support systems, or integrating conversational 
  AI into Zoom Contact Center workflows.
---

# Zoom Virtual Agent API

Build AI-powered customer service solutions with Zoom Virtual Agent APIs.

## Overview

Zoom Virtual Agent (ZVA) is an AI-driven conversational chatbot that handles customer inquiries using natural language processing:
- Automated customer support with NLP
- Intent recognition and entity extraction
- Knowledge base integration
- Conversation flow management
- Analytics and resolution tracking
- Multi-channel deployment

## Choose Your Integration

| I want to... | Use this |
|--------------|----------|
| Create and manage virtual agents | **Virtual Agents API** |
| Define customer intents | **Intents API** |
| Build knowledge bases | **Knowledge Base API** |
| Design conversation flows | **Flows API** |
| Track performance metrics | **Analytics API** |
| Access conversation history | **Conversations API** |

## API Endpoints

### Virtual Agents

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/virtual_agents` | List virtual agents |
| POST | `/virtual_agents` | Create virtual agent |
| GET | `/virtual_agents/{agentId}` | Get agent details |
| PATCH | `/virtual_agents/{agentId}` | Update agent |
| DELETE | `/virtual_agents/{agentId}` | Delete agent |
| POST | `/virtual_agents/{agentId}/publish` | Publish agent |

### Intents

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/virtual_agents/{agentId}/intents` | List intents |
| POST | `/virtual_agents/{agentId}/intents` | Create intent |
| GET | `/virtual_agents/{agentId}/intents/{intentId}` | Get intent details |
| PATCH | `/virtual_agents/{agentId}/intents/{intentId}` | Update intent |
| DELETE | `/virtual_agents/{agentId}/intents/{intentId}` | Delete intent |

### Entities

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/virtual_agents/{agentId}/entities` | List entities |
| POST | `/virtual_agents/{agentId}/entities` | Create entity |
| GET | `/virtual_agents/{agentId}/entities/{entityId}` | Get entity details |
| PATCH | `/virtual_agents/{agentId}/entities/{entityId}` | Update entity |
| DELETE | `/virtual_agents/{agentId}/entities/{entityId}` | Delete entity |

### Knowledge Base

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/virtual_agents/{agentId}/knowledge_base` | Get knowledge base |
| POST | `/virtual_agents/{agentId}/knowledge_base/articles` | Add article |
| PATCH | `/virtual_agents/{agentId}/knowledge_base/articles/{articleId}` | Update article |
| DELETE | `/virtual_agents/{agentId}/knowledge_base/articles/{articleId}` | Delete article |
| POST | `/virtual_agents/{agentId}/knowledge_base/sync` | Sync external KB |

### Conversations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/virtual_agents/{agentId}/conversations` | List conversations |
| GET | `/virtual_agents/{agentId}/conversations/{conversationId}` | Get conversation |
| GET | `/virtual_agents/{agentId}/conversations/{conversationId}/transcript` | Get transcript |

### Flows

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/virtual_agents/{agentId}/flows` | List conversation flows |
| POST | `/virtual_agents/{agentId}/flows` | Create flow |
| GET | `/virtual_agents/{agentId}/flows/{flowId}` | Get flow details |
| PATCH | `/virtual_agents/{agentId}/flows/{flowId}` | Update flow |

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/virtual_agents/{agentId}/analytics` | Get agent analytics |
| GET | `/virtual_agents/{agentId}/analytics/intents` | Intent analytics |
| GET | `/virtual_agents/{agentId}/analytics/resolution` | Resolution rates |

## Example: Create an Intent

```bash
curl -X POST "https://api.zoom.us/v2/virtual_agents/{agentId}/intents" \
  -H "Authorization: Bearer {accessToken}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "check_order_status",
    "display_name": "Check Order Status",
    "training_phrases": [
      "Where is my order?",
      "Track my package",
      "What is my order status?"
    ],
    "responses": [
      {
        "type": "text",
        "text": "I can help you check your order status. Could you please provide your order number?"
      }
    ]
  }'
```

## Example: Add Knowledge Base Article

```bash
curl -X POST "https://api.zoom.us/v2/virtual_agents/{agentId}/knowledge_base/articles" \
  -H "Authorization: Bearer {accessToken}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Return Policy",
    "content": "Our return policy allows returns within 30 days of purchase...",
    "category": "Policies",
    "keywords": ["return", "refund", "exchange"],
    "url": "https://example.com/help/returns"
  }'
```

## Example: Get Agent Analytics

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/virtual_agents/{agentId}/analytics?from=2024-01-01&to=2024-01-31',
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const analytics = await response.json();
// analytics.resolution_rate, analytics.total_conversations, etc.
```

## Response Types

| Type | Description |
|------|-------------|
| `text` | Plain text response |
| `card` | Rich card with buttons |
| `carousel` | Multiple cards |
| `quick_replies` | Suggested responses |
| `handoff` | Escalate to human agent |
| `api_call` | Call external API |

## Entity Types

| Type | Description |
|------|-------------|
| `system` | Built-in entities (date, number, etc.) |
| `custom` | Custom defined entities |
| `regex` | Pattern-based entities |
| `list` | List of values |

## Conversation Status

| Status | Description |
|--------|-------------|
| `active` | Conversation in progress |
| `resolved` | Resolved by virtual agent |
| `escalated` | Handed off to human |
| `abandoned` | Customer left |

## Prerequisites

1. **Zoom Virtual Agent license** - Account must have ZVA enabled
2. **OAuth app** - Create in [Zoom App Marketplace](https://marketplace.zoom.us/)
3. **Scopes** - Required OAuth scopes:
   - `virtual_agent:read` - Read virtual agent data
   - `virtual_agent:write` - Manage virtual agents
   - `virtual_agent:read:admin` - Admin read access
   - `virtual_agent:write:admin` - Admin write access

## Channel Integration

Virtual Agent can be deployed across:
- Web chat widget
- Mobile app
- Zoom Contact Center
- Messaging platforms

## Common Use Cases

| Use Case | Description | Integration |
|----------|-------------|-------------|
| **Customer Support Bot** | Automated FAQ handling | Intents + Knowledge Base |
| **Order Tracking** | Self-service order status | Intents + API Calls |
| **Appointment Scheduling** | Book/modify appointments | Flows + Entities |
| **IT Helpdesk** | Troubleshooting workflows | Flows + Knowledge Base |
| **Lead Qualification** | Pre-qualify sales leads | Intents + Handoff |
| **Performance Monitoring** | Track bot effectiveness | Analytics API |

## Detailed References

- **[references/virtual-agent.md](references/virtual-agent.md)** - Full API reference

## Resources

- **API Reference**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Virtual-Agent
- **Virtual Agent Documentation**: https://developers.zoom.us/docs/virtual-agent/
- **Bot Building Guide**: https://developers.zoom.us/docs/virtual-agent/building/
- **Marketplace**: https://marketplace.zoom.us/

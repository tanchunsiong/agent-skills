---
name: zoom-chatbot-studio
description: |
  Zoom Chatbot Studio guide for building Team Chat bots without code. Covers the visual
  bot builder, message templates, workflow automation, and integration triggers. Use when
  building simple to moderate chatbots for Zoom Team Chat without writing code.
---

# Zoom Chatbot Studio

Build Zoom Team Chat bots visually without writing code.

## Overview

Chatbot Studio provides:
- Visual drag-and-drop bot builder
- Pre-built message templates
- Workflow automation triggers
- Integration with Zoom Team Chat
- No coding required
- Quick deployment to Marketplace

## Key Features

| Feature | Description |
|---------|-------------|
| **Visual Builder** | Drag-and-drop conversation flows |
| **Message Templates** | Pre-designed message formats |
| **Triggers** | Respond to keywords, commands, events |
| **Actions** | Send messages, call APIs, set variables |
| **Conditions** | Branch logic based on user input |
| **Quick Deploy** | Publish directly to Team Chat |

## When to Use Chatbot Studio

| Scenario | Use Chatbot Studio? |
|----------|---------------------|
| Simple FAQ bot | Yes |
| Slash command responses | Yes |
| Form data collection | Yes |
| Workflow notifications | Yes |
| Complex API integrations | No - Use Chatbot API |
| Custom authentication | No - Use Chatbot API |
| Real-time data processing | No - Use Chatbot API |

## Getting Started

### 1. Access Chatbot Studio

1. Go to [Zoom App Marketplace](https://marketplace.zoom.us/)
2. Click **Develop** -> **Build App**
3. Select **Team Chat Apps** -> **Chatbot**
4. Choose **Chatbot Studio** (no-code)

### 2. Create Your Bot

1. Name your bot and add description
2. Configure bot avatar and display name
3. Set up slash commands (e.g., `/mybot`)
4. Open the visual builder

### 3. Build Conversation Flows

```
[Trigger: /help command]
    |
[Send Message: "How can I help you?"]
    |
[Button Options]
    |-- "FAQ" -> [Show FAQ Menu]
    |-- "Support" -> [Create Ticket Flow]
    +-- "Status" -> [Check Status API]
```

## Visual Builder Components

### Triggers

| Trigger | Description |
|---------|-------------|
| **Slash Command** | User types `/command` |
| **Keyword** | Message contains keyword |
| **Button Click** | User clicks interactive button |
| **Scheduled** | Time-based trigger |
| **Webhook** | External system triggers |

### Actions

| Action | Description |
|--------|-------------|
| **Send Message** | Send text/rich message |
| **Send Card** | Send interactive card |
| **API Call** | Make HTTP request |
| **Set Variable** | Store data for flow |
| **Delay** | Wait before next action |

### Conditions

| Condition | Description |
|-----------|-------------|
| **Text Match** | Check user input |
| **Variable Check** | Compare stored values |
| **API Response** | Branch on API result |
| **User Attribute** | Check user properties |

## Message Types

### Text Message

```yaml
Type: Text
Content: "Hello! Welcome to our support bot."
```

### Interactive Card

```yaml
Type: Card
Header: "Support Options"
Body: "What do you need help with?"
Buttons:
  - Label: "Technical Support"
    Action: goto_flow("technical")
  - Label: "Billing"
    Action: goto_flow("billing")
  - Label: "General Inquiry"
    Action: goto_flow("general")
```

### Form Collection

```yaml
Type: Form
Title: "Create Support Ticket"
Fields:
  - Name: "issue_type"
    Type: dropdown
    Options: ["Bug", "Feature Request", "Question"]
  - Name: "description"
    Type: textarea
    Required: true
  - Name: "priority"
    Type: dropdown
    Options: ["Low", "Medium", "High"]
Submit: create_ticket_flow
```

## Example Flows

### FAQ Bot

```
Trigger: /faq
  |
Send Card:
  Title: "Frequently Asked Questions"
  Buttons:
    - "How do I reset password?" -> send_text("Go to Settings > Security...")
    - "What are business hours?" -> send_text("Mon-Fri, 9am-5pm PST")
    - "How to contact support?" -> send_text("Email support@example.com")
```

### Status Check Bot

```
Trigger: /status
  |
API Call: GET https://api.example.com/status
  |
Condition: response.status == "operational"
  |-- True -> send_text("All systems operational")
  +-- False -> send_text("Service degradation detected")
```

### Ticket Creation Bot

```
Trigger: /ticket
  |
Send Form:
  - Issue Type (dropdown)
  - Description (textarea)
  - Priority (dropdown)
  |
On Submit:
  API Call: POST https://api.example.com/tickets
    Body: {form_data}
  |
  Send Text: "Ticket #{response.id} created!"
```

## Variables and Data

### Built-in Variables

| Variable | Description |
|----------|-------------|
| `{{user.name}}` | User's display name |
| `{{user.email}}` | User's email |
| `{{user.id}}` | User's Zoom ID |
| `{{channel.name}}` | Channel name |
| `{{channel.id}}` | Channel ID |
| `{{timestamp}}` | Current timestamp |

### Custom Variables

```yaml
# Set variable
Action: Set Variable
Name: ticket_id
Value: {{api_response.id}}

# Use variable
Action: Send Text
Content: "Your ticket ID is {{ticket_id}}"
```

## API Integration

### Making API Calls

```yaml
Action: API Call
Method: POST
URL: https://api.example.com/data
Headers:
  Authorization: Bearer {{secrets.API_KEY}}
  Content-Type: application/json
Body:
  user_email: "{{user.email}}"
  request: "{{user_input}}"
Save Response As: api_result
```

### Using API Responses

```yaml
Condition: {{api_result.success}} == true
  |-- True -> Send: "Success! Result: {{api_result.data}}"
  +-- False -> Send: "Error: {{api_result.error}}"
```

## Secrets Management

Store sensitive data securely:

1. Go to **Bot Settings** -> **Secrets**
2. Add secrets (API keys, tokens)
3. Reference in flows: `{{secrets.MY_API_KEY}}`

## Testing

### Preview Mode

1. Click **Preview** in builder
2. Simulate user interactions
3. View flow execution
4. Check variable values

### Test in Team Chat

1. Click **Test** -> **Install to Workspace**
2. Open Zoom Team Chat
3. Find your bot in contacts
4. Send commands to test

## Publishing

### To Your Organization

1. Complete all required fields
2. Click **Submit for Review**
3. Once approved, install org-wide

### To Marketplace

1. Add marketing materials
2. Set pricing (free/paid)
3. Submit for Zoom review
4. Published once approved

## Limitations

| Limitation | Workaround |
|------------|------------|
| Complex logic | Use Chatbot API instead |
| Custom OAuth | Use Chatbot API instead |
| High volume | Use Chatbot API with webhooks |
| Real-time websockets | Not supported |
| File uploads | Limited support |

## Prerequisites

1. **Zoom Account** - Admin or developer access
2. **Team Chat** - Enabled for organization
3. **Marketplace Access** - Developer account

## Common Use Cases

| Use Case | Description |
|----------|-------------|
| **IT Helpdesk** | Password resets, ticket creation |
| **HR Bot** | PTO requests, policy questions |
| **Sales Bot** | Lead qualification, meeting scheduling |
| **Notification Bot** | System alerts, reminders |
| **Onboarding Bot** | New employee assistance |

## Resources

- **Chatbot Studio Guide**: https://developers.zoom.us/docs/team-chat-apps/chatbot-studio/
- **Team Chat Apps**: https://developers.zoom.us/docs/team-chat-apps/
- **Message Formats**: https://developers.zoom.us/docs/team-chat-apps/customizing-messages/
- **Marketplace**: https://marketplace.zoom.us/

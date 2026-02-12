# Zoom Team Chat Documentation Index

Complete navigation guide for the Zoom Team Chat skill.

## Quick Start Paths

### Path 1: Team Chat API (User-Level Messaging)

For sending messages as a user account.

1. [API Selection Guide](concepts/api-selection.md) - Confirm Team Chat API is right
2. [Environment Setup](concepts/environment-setup.md) - Get credentials
3. [OAuth Setup Example](examples/oauth-setup.md) - Implement authentication *(File pending)*
4. [Send Message Example](examples/send-message.md) - Send your first message *(File pending)*

### Path 2: Chatbot API (Interactive Bots)

For building interactive chatbots with rich messages.

1. [API Selection Guide](concepts/api-selection.md) - Confirm Chatbot API is right
2. [Environment Setup](concepts/environment-setup.md) - Get credentials (including Bot JID)
3. [Webhook Architecture](concepts/webhooks.md) - Understand webhook events
4. [Chatbot Setup Example](examples/chatbot-setup.md) - Build your first bot
5. [Message Cards Reference](references/message-cards.md) - Create rich messages

## Core Concepts

Essential understanding for both APIs.

| Document | Description |
|----------|-------------|
| [API Selection Guide](concepts/api-selection.md) | Choose Team Chat API vs Chatbot API |
| [Environment Setup](concepts/environment-setup.md) | Complete credentials and app configuration |
| [Authentication Flows](concepts/authentication.md) | OAuth vs Client Credentials *(File pending)* |
| [Webhook Architecture](concepts/webhooks.md) | How webhooks work (Chatbot API) |
| [Message Card Structure](concepts/message-structure.md) | Card component hierarchy *(File pending)* |
| [Deployment Guide](concepts/deployment.md) | Production deployment strategies *(File pending)* |
| [Security Best Practices](concepts/security.md) | Secure your integration *(File pending)* |

## Complete Examples

Working code for common scenarios.

### Authentication
| Example | Description |
|---------|-------------|
| [OAuth Setup](examples/oauth-setup.md) | User OAuth flow implementation *(File pending)* |
| [Token Management](examples/token-management.md) | Refresh tokens, expiration handling *(File pending)* |

### Basic Operations
| Example | Description |
|---------|-------------|
| [Send Message](examples/send-message.md) | Team Chat API message sending *(File pending)* |
| [Chatbot Setup](examples/chatbot-setup.md) | Complete chatbot with webhooks |
| [List Channels](examples/channel-management.md) | Get user's channels *(File pending)* |
| [Create Channel](examples/channel-management.md) | Create public/private channels *(File pending)* |

### Interactive Features (Chatbot API)
| Example | Description |
|---------|-------------|
| [Button Actions](examples/button-actions.md) | Handle button clicks *(File pending)* |
| [Form Submissions](examples/form-submissions.md) | Process form data *(File pending)* |
| [Slash Commands](examples/slash-commands.md) | Create custom commands *(File pending)* |
| [Dropdown Selects](examples/dropdown-selects.md) | Channel/member pickers *(File pending)* |

### Advanced Integration
| Example | Description |
|---------|-------------|
| [LLM Integration](examples/llm-integration.md) | Integrate Claude/GPT *(File pending)* |
| [Scheduled Alerts](examples/scheduled-alerts.md) | Cron + incoming webhooks *(File pending)* |
| [Database Integration](examples/database-integration.md) | Store conversation state *(File pending)* |
| [Multi-Step Workflows](examples/multi-step-workflows.md) | Complex user interactions *(File pending)* |

## References

### API Documentation
| Reference | Description |
|-----------|-------------|
| [API Reference](references/api-reference.md) | All endpoints and methods *(File pending)* |
| [Webhook Events](references/webhook-events.md) | Complete event reference *(File pending)* |
| [Message Cards](references/message-cards.md) | All card components |
| [Error Codes](references/error-codes.md) | Error handling guide *(File pending)* |

### Sample Applications
| Reference | Description |
|-----------|-------------|
| [Sample Applications](references/samples.md) | Analysis of 10 official samples *(File pending)* |
| [Sample Comparison](references/sample-comparison.md) | Feature comparison matrix *(File pending)* |

### Field Guides
| Reference | Description |
|-----------|-------------|
| [JID Formats](references/jid-formats.md) | Understanding JID identifiers *(File pending)* |
| [Scopes Reference](references/scopes.md) | All available scopes *(File pending)* |
| [Rate Limits](references/rate-limits.md) | API limits and quotas *(File pending)* |

## Troubleshooting

| Guide | Description |
|-------|-------------|
| [Common Issues](troubleshooting/common-issues.md) | Quick diagnostics and solutions |
| [OAuth Issues](troubleshooting/oauth-issues.md) | Authentication failures *(File pending)* |
| [Webhook Issues](troubleshooting/webhook-issues.md) | Webhook debugging *(File pending)* |
| [Message Issues](troubleshooting/message-issues.md) | Message sending problems *(File pending)* |
| [Deployment Issues](troubleshooting/deployment-issues.md) | Production problems *(File pending)* |

## Architecture Patterns

### Chatbot Lifecycle

```
User Action → Webhook → Process → Response
```

### LLM Integration Pattern

```
User Input → Chatbot receives → Call LLM → Send response
```

### Approval Workflow Pattern

```
Request → Send card with buttons → User clicks → Update status → Notify
```

## Common Use Cases

### Notifications
- CI/CD build notifications
- Server monitoring alerts
- Scheduled reports
- System health checks

### Workflows
- Approval requests
- Task assignment
- Status updates
- Form submissions

### Integrations
- LLM-powered assistants
- Database queries
- External API integration
- File/image sharing

### Automation
- Scheduled messages
- Auto-responses
- Data collection
- Report generation

## Resource Links

### Official Documentation
- **[Team Chat Docs](https://developers.zoom.us/docs/zoom-team-chat/)** - Official overview
- **[Chatbot Docs](https://developers.zoom.us/docs/zoom-team-chat/chatbot/extend/)** - Chatbot guide
- **[API Reference](https://developers.zoom.us/docs/api/rest/reference/chatbot/)** - REST API docs
- **[App Marketplace](https://marketplace.zoom.us/)** - Create and manage apps

### Sample Code
- **[Chatbot Quickstart](https://github.com/zoom/chatbot-nodejs-quickstart)** - Official tutorial
- **[Claude Chatbot](https://github.com/zoom/zoom-chatbot-claude-sample)** - AI integration
- **[Unsplash Chatbot](https://github.com/zoom/unsplash-chatbot)** - Image search bot
- **[ERP Chatbot](https://github.com/zoom/zoom-erp-chatbot-sample)** - Enterprise integration
- **[Task Manager](https://github.com/zoom/task-manager-sample)** - Full CRUD app

### Tools
- **[App Card Builder](https://appssdk.zoom.us/cardbuilder/)** - Visual card designer
- **[ngrok](https://ngrok.com/)** - Local webhook testing
- **[Postman](https://www.postman.com/)** - API testing

### Community
- **[Developer Forum](https://devforum.zoom.us/)** - Ask questions
- **[GitHub Discussions](https://github.com/zoom)** - Community support
- **[Developer Support](https://devsupport.zoom.us)** - Official support

## Documentation Status

### ✅ Complete
- Main skill.md entry point
- API Selection Guide
- Environment Setup
- Webhook Architecture
- Chatbot Setup Example (complete working code)
- Message Cards Reference
- Common Issues Troubleshooting

### 📝 Pending (High Priority)
- OAuth Setup Example
- Send Message Example
- Button Actions Example
- LLM Integration Example
- Webhook Events Reference
- API Reference
- Sample Applications Analysis

### 📋 Planned (Lower Priority)
- Form Submissions Example
- Channel Management Examples
- Database Integration Example
- Error Codes Reference
- Rate Limits Guide
- Deployment troubleshooting

## Getting Started Checklist

### For Team Chat API

- [ ] Read [API Selection Guide](concepts/api-selection.md)
- [ ] Complete [Environment Setup](concepts/environment-setup.md)
- [ ] Obtain Client ID, Client Secret
- [ ] Add required scopes
- [ ] Implement OAuth flow
- [ ] Send first message

### For Chatbot API

- [ ] Read [API Selection Guide](concepts/api-selection.md)
- [ ] Complete [Environment Setup](concepts/environment-setup.md)
- [ ] Obtain Client ID, Client Secret, Bot JID, Secret Token, Account ID
- [ ] Enable Team Chat in Features
- [ ] Configure Bot Endpoint URL and Slash Command
- [ ] Set up ngrok for local testing
- [ ] Implement webhook handler
- [ ] Send first chatbot message

## Version History

- **v1.0** (2026-02-09) - Initial comprehensive documentation
  - Core concepts (API selection, environment setup, webhooks)
  - Complete chatbot setup example
  - Message cards reference
  - Common issues troubleshooting

## Contributing

This skill is part of the agent-skills repository. Improvements welcome!

## Support

For skill-related questions or improvements, please reference this INDEX.md for navigation.

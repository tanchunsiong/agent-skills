# OAuth Scopes

OAuth scopes define what your app can access.

## Overview

Scopes are permissions requested during OAuth authorization. Request only the scopes you need.

## Common Scopes

### Meetings

| Scope | Description |
|-------|-------------|
| `meeting:read` | View meeting details |
| `meeting:write` | Create, update, delete meetings |
| `meeting:master` | Full meeting access |

### Users

| Scope | Description |
|-------|-------------|
| `user:read` | View user profile |
| `user:write` | Update user settings |
| `user:master` | Full user access |

### Recordings

| Scope | Description |
|-------|-------------|
| `recording:read` | View/download recordings |
| `recording:write` | Delete recordings |
| `recording:master` | Full recording access |

### Webinars

| Scope | Description |
|-------|-------------|
| `webinar:read` | View webinar details |
| `webinar:write` | Create, update webinars |
| `webinar:master` | Full webinar access |

### Reports

| Scope | Description |
|-------|-------------|
| `report:read` | View reports and analytics |
| `report:master` | Full report access |

## Scope Patterns

| Pattern | Meaning |
|---------|---------|
| `resource:read` | Read-only access |
| `resource:write` | Read and write access |
| `resource:master` | Full access including delete |

## Best Practices

1. **Request minimum scopes** - Only what you need
2. **Explain to users** - Why you need each scope
3. **Handle denied scopes** - Graceful fallback

## Resources

- **Scopes reference**: https://developers.zoom.us/docs/integrations/oauth-scopes/

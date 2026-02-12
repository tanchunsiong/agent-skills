---
name: zoom-rest-api
description: "Zoom REST API - 600+ endpoints for meetings, users, webinars, recordings, reports, and more. Server-side API for managing Zoom resources programmatically with OAuth 2.0 authentication."
triggers:
  - "api call"
  - "rest api"
  - "create meeting"
  - "get meeting"
  - "list meetings"
  - "update meeting"
  - "delete meeting"
  - "create user"
  - "zoom api"
  - "api endpoint"
  - "recordings api"
  - "users api"
  - "webinars api"
---

# Zoom REST API

Expert guidance for building server-side integrations with the Zoom REST API. This API provides 600+ endpoints for managing meetings, users, webinars, recordings, reports, and all Zoom platform resources programmatically.

**Official Documentation**: https://developers.zoom.us/docs/api/
**API Reference**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/
**OpenAPI Spec**: https://marketplace.zoom.us/docs/api-reference/using-zoom-apis/

## Quick Links

**New to Zoom REST API? Follow this path:**

1. **[API Architecture](concepts/api-architecture.md)** - Base URLs, regional URLs, `me` keyword, ID vs UUID, time formats
2. **[Authentication Flows](concepts/authentication-flows.md)** - OAuth setup (S2S, User, PKCE, Device Code)
3. **[Meeting Lifecycle](examples/meeting-lifecycle.md)** - Create → Update → Start → End → Delete with webhooks
4. **[Rate Limiting Strategy](concepts/rate-limiting-strategy.md)** - Plan tiers, per-user limits, retry patterns

**Reference:**
- **[Meetings](references/meetings.md)** - Meeting CRUD, types, settings
- **[Users](references/users.md)** - User provisioning and management
- **[Recordings](references/recordings.md)** - Cloud recording access and download
- **[GraphQL Queries](examples/graphql-queries.md)** - Alternative query API (beta)
- **[INDEX.md](INDEX.md)** - Complete documentation navigation

**Having issues?**
- 401 Unauthorized → [Authentication Flows](concepts/authentication-flows.md) (check token expiry, scopes)
- 429 Too Many Requests → [Rate Limiting Strategy](concepts/rate-limiting-strategy.md)
- Error codes → [Common Errors](troubleshooting/common-errors.md)
- Pagination confusion → [Common Issues](troubleshooting/common-issues.md)
- Webhooks not arriving → [Webhook Server](examples/webhook-server.md)

**Building event-driven integrations?**
- [Webhook Server](examples/webhook-server.md) - Express.js server with CRC validation
- [Recording Pipeline](examples/recording-pipeline.md) - Auto-download via webhook events

## Quick Start

### Get an Access Token (Server-to-Server OAuth)

```bash
curl -X POST "https://zoom.us/zoom-oauth/token" \
  -H "Authorization: Basic $(echo -n 'CLIENT_ID:CLIENT_SECRET' | base64)" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=account_credentials&account_id=ACCOUNT_ID"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "scope": "meeting:read meeting:write user:read"
}
```

### Create a Meeting

```bash
curl -X POST "https://api.zoom.us/v2/users/me/meetings" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Team Standup",
    "type": 2,
    "start_time": "2025-03-15T10:00:00Z",
    "duration": 30,
    "settings": {
      "join_before_host": false,
      "waiting_room": true
    }
  }'
```

### List Users with Pagination

```bash
curl "https://api.zoom.us/v2/users?page_size=300&status=active" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

## Base URL

```
https://api.zoom.us/v2
```

### Regional Base URLs

The `api_url` field in OAuth token responses indicates the user's region. Use regional URLs for data residency compliance:

| Region | URL |
|--------|-----|
| Global (default) | `https://api.zoom.us/v2` |
| Australia | `https://api-au.zoom.us/v2` |
| Canada | `https://api-ca.zoom.us/v2` |
| European Union | `https://api-eu.zoom.us/v2` |
| India | `https://api-in.zoom.us/v2` |
| Saudi Arabia | `https://api-sa.zoom.us/v2` |
| Singapore | `https://api-sg.zoom.us/v2` |
| United Kingdom | `https://api-uk.zoom.us/v2` |
| United States | `https://api-us.zoom.us/v2` |

**Note:** You can always use the global URL `https://api.zoom.us` regardless of the `api_url` value.

## Key Features

| Feature | Description |
|---------|-------------|
| **Meeting Management** | Create, read, update, delete meetings with full scheduling control |
| **User Provisioning** | Automated user lifecycle (create, update, deactivate, delete) |
| **Webinar Operations** | Webinar CRUD, registrant management, panelist control |
| **Cloud Recordings** | List, download, delete recordings with file-type filtering |
| **Reports & Analytics** | Usage reports, participant data, daily statistics |
| **Team Chat** | Channel management, messaging, chatbot integration |
| **Zoom Phone** | Call management, voicemail, call routing |
| **Zoom Rooms** | Room management, device control, scheduling |
| **Webhooks** | Real-time event notifications for 100+ event types |
| **WebSockets** | Persistent event streaming without public endpoints |
| **GraphQL (Beta)** | Single-endpoint flexible queries at `v3/graphql` |
| **AI Companion** | Meeting summaries, transcripts, AI-generated content |

## Prerequisites

- Zoom account (Free tier has API access with lower rate limits)
- App registered on [Zoom App Marketplace](https://marketplace.zoom.us/)
- OAuth credentials (Server-to-Server OAuth or User OAuth)
- Appropriate scopes for target endpoints

> **Need help with authentication?** See the **[zoom-oauth](../zoom-oauth/SKILL.md)** skill for complete OAuth flow implementation.

## Critical Gotchas and Best Practices

### ⚠️ JWT App Type is Deprecated

The JWT app type is deprecated. Migrate to **Server-to-Server OAuth**. This does NOT affect JWT token signatures used in Video SDK — only the Marketplace "JWT" app type for REST API access.

```javascript
// OLD (JWT app type - DEPRECATED)
const token = jwt.sign({ iss: apiKey, exp: expiry }, apiSecret);

// NEW (Server-to-Server OAuth)
const token = await getServerToServerToken(accountId, clientId, clientSecret);
```

### ⚠️ The `me` Keyword Rules

- **User-level OAuth apps**: MUST use `me` instead of `userId` (otherwise: invalid token error)
- **Server-to-Server OAuth apps**: MUST NOT use `me` — provide the actual `userId` or email
- **Account-level OAuth apps**: Can use either `me` or `userId`

### ⚠️ Meeting ID vs UUID — Double Encoding

UUIDs that begin with `/` or contain `//` must be **double URL-encoded**:

```javascript
// UUID: /abc==
// Single encode: %2Fabc%3D%3D
// Double encode: %252Fabc%253D%253D  ← USE THIS

const uuid = '/abc==';
const encoded = encodeURIComponent(encodeURIComponent(uuid));
const url = `https://api.zoom.us/v2/meetings/${encoded}`;
```

### ⚠️ Time Formats

- `yyyy-MM-ddTHH:mm:ssZ` — **UTC time** (note the `Z` suffix)
- `yyyy-MM-ddTHH:mm:ss` — **Local time** (no `Z`, uses `timezone` field)
- Some report APIs only accept UTC. Check the API reference for each endpoint.

### ⚠️ Rate Limits Are Per-Account, Not Per-App

All apps on the same Zoom account **share** rate limits. One heavy app can impact others. Monitor `X-RateLimit-Remaining` headers proactively.

### ⚠️ Per-User Daily Limits

Meeting/Webinar create/update operations are limited to **100 per day per user** (resets at 00:00 UTC). Distribute operations across different host users when doing bulk operations.

### ⚠️ Download URLs Require Auth and Follow Redirects

Recording `download_url` values require Bearer token authentication and may redirect. Always follow redirects:

```bash
curl -L -H "Authorization: Bearer ACCESS_TOKEN" "https://zoom.us/rec/download/..."
```

### Use Webhooks Instead of Polling

```javascript
// DON'T: Poll every minute (wastes API quota)
setInterval(() => getMeetings(), 60000);

// DO: Receive webhook events in real-time
app.post('/webhook', (req, res) => {
  if (req.body.event === 'meeting.started') {
    handleMeetingStarted(req.body.payload);
  }
  res.status(200).send();
});
```

> **Webhook setup details:** See the **[zoom-webhooks](../zoom-webhooks/SKILL.md)** skill for comprehensive webhook implementation.

## Complete Documentation Library

This skill includes comprehensive guides organized by category:

### Core Concepts
- **[API Architecture](concepts/api-architecture.md)** - REST design, base URLs, regional routing, `me` keyword, ID vs UUID, time formats
- **[Authentication Flows](concepts/authentication-flows.md)** - All OAuth flows (S2S, User, PKCE, Device Code)
- **[Rate Limiting Strategy](concepts/rate-limiting-strategy.md)** - Limits by plan, retry patterns, request queuing

### Complete Examples
- **[Meeting Lifecycle](examples/meeting-lifecycle.md)** - Full Create → Update → Start → End → Delete flow with webhook events
- **[User Management](examples/user-management.md)** - CRUD users, list with pagination, bulk operations
- **[Recording Pipeline](examples/recording-pipeline.md)** - Download recordings via webhooks + API
- **[Webhook Server](examples/webhook-server.md)** - Express.js server with CRC validation and signature verification
- **[GraphQL Queries](examples/graphql-queries.md)** - GraphQL queries, mutations, cursor pagination

### Troubleshooting
- **[Common Errors](troubleshooting/common-errors.md)** - HTTP status codes, Zoom error codes, error response formats
- **[Common Issues](troubleshooting/common-issues.md)** - Rate limits, token refresh, pagination pitfalls, gotchas

### References (39 files covering all Zoom API domains)

#### Core APIs
- **[references/meetings.md](references/meetings.md)** - Meeting CRUD, types, settings
- **[references/users.md](references/users.md)** - User provisioning, types, scopes
- **[references/webinars.md](references/webinars.md)** - Webinar management, registrants
- **[references/recordings.md](references/recordings.md)** - Cloud recording access
- **[references/reports.md](references/reports.md)** - Usage reports, analytics
- **[references/accounts.md](references/accounts.md)** - Account management

#### Communication
- **[references/team-chat.md](references/team-chat.md)** - Team Chat messaging
- **[references/chatbot.md](references/chatbot.md)** - Interactive chatbots
- **[references/phone.md](references/phone.md)** - Zoom Phone
- **[references/mail.md](references/mail.md)** - Zoom Mail
- **[references/calendar.md](references/calendar.md)** - Zoom Calendar

#### Infrastructure
- **[references/rooms.md](references/rooms.md)** - Zoom Rooms
- **[references/rate-limits.md](references/rate-limits.md)** - Rate limit details
- **[references/qss.md](references/qss.md)** - Quality of Service Subscription

#### Advanced
- **[references/graphql.md](references/graphql.md)** - GraphQL API (beta)
- **[references/ai-companion.md](references/ai-companion.md)** - AI features
- **[references/authentication.md](references/authentication.md)** - Auth reference
- **[references/openapi.md](references/openapi.md)** - OpenAPI specs, Postman, code generation

#### Additional API Domains
- **[references/events.md](references/events.md)** - Events and event platform APIs
- **[references/scheduler.md](references/scheduler.md)** - Zoom Scheduler APIs
- **[references/tasks.md](references/tasks.md)** - Tasks APIs
- **[references/whiteboard.md](references/whiteboard.md)** - Whiteboard APIs
- **[references/video-management.md](references/video-management.md)** - Video management APIs
- **[references/video-sdk-api.md](references/video-sdk-api.md)** - Video SDK REST APIs
- **[references/marketplace-apps.md](references/marketplace-apps.md)** - Marketplace app management
- **[references/commerce.md](references/commerce.md)** - Commerce and billing APIs
- **[references/contact-center.md](references/contact-center.md)** - Contact Center APIs
- **[references/quality-management.md](references/quality-management.md)** - Quality management APIs
- **[references/workforce-management.md](references/workforce-management.md)** - Workforce management APIs
- **[references/healthcare.md](references/healthcare.md)** - Healthcare APIs
- **[references/auto-dialer.md](references/auto-dialer.md)** - Auto dialer APIs
- **[references/number-management.md](references/number-management.md)** - Number management APIs
- **[references/revenue-accelerator.md](references/revenue-accelerator.md)** - Revenue Accelerator APIs
- **[references/virtual-agent.md](references/virtual-agent.md)** - Virtual Agent APIs
- **[references/cobrowse-sdk-api.md](references/cobrowse-sdk-api.md)** - Cobrowse SDK APIs
- **[references/crc.md](references/crc.md)** - Cloud Room Connector APIs
- **[references/clips.md](references/clips.md)** - Clips APIs
- **[references/zoom-docs.md](references/zoom-docs.md)** - Zoom docs and source references

## Sample Repositories

### Official (by Zoom)

| Type | Repository |
|------|------------|
| OAuth Sample | [oauth-sample-app](https://github.com/zoom/oauth-sample-app) |
| S2S OAuth Starter | [server-to-server-oauth-starter-api](https://github.com/zoom/server-to-server-oauth-starter-api) |
| User OAuth | [user-level-oauth-starter](https://github.com/zoom/user-level-oauth-starter) |
| S2S Token | [server-to-server-oauth-token](https://github.com/zoom/server-to-server-oauth-token) |
| Rivet Library | [rivet-javascript](https://github.com/zoom/rivet-javascript) |
| WebSocket Sample | [websocket-js-sample](https://github.com/zoom/websocket-js-sample) |
| Webhook Sample | [webhook-sample-node.js](https://github.com/zoom/webhook-sample-node.js) |
| Python S2S | [server-to-server-python-sample](https://github.com/zoom/server-to-server-python-sample) |

## Resources

- **API Reference**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/
- **GraphQL Playground**: https://nws.zoom.us/graphql/playground
- **Postman Collection**: https://marketplace.zoom.us/docs/api-reference/postman
- **Developer Forum**: https://devforum.zoom.us/
- **Changelog**: https://developers.zoom.us/changelog/
- **Status Page**: https://status.zoom.us/

---

**Need help?** Start with [INDEX.md](INDEX.md) for complete navigation.

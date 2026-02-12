# Zoom REST API - Complete Documentation Index

## Quick Start Path

**If you're new to the Zoom REST API, follow this order:**

1. **Understand the API design** → [concepts/api-architecture.md](concepts/api-architecture.md)
   - Base URLs, regional endpoints, `me` keyword rules
   - Meeting ID vs UUID, double-encoding, time formats

2. **Set up authentication** → [concepts/authentication-flows.md](concepts/authentication-flows.md)
   - Server-to-Server OAuth (backend automation)
   - User OAuth with PKCE (user-facing apps)
   - Cross-reference: [zoom-oauth](../zoom-oauth/SKILL.md)

3. **Create your first meeting** → [examples/meeting-lifecycle.md](examples/meeting-lifecycle.md)
   - Full CRUD with curl and Node.js examples
   - Webhook event integration

4. **Handle rate limits** → [concepts/rate-limiting-strategy.md](concepts/rate-limiting-strategy.md)
   - Plan-based limits, retry patterns, request queuing

5. **Set up webhooks** → [examples/webhook-server.md](examples/webhook-server.md)
   - CRC validation, signature verification, event handling

6. **Troubleshoot issues** → [troubleshooting/common-issues.md](troubleshooting/common-issues.md)
   - Token refresh, pagination pitfalls, common gotchas

---

## Documentation Structure

```
zoom-rest-api/
├── SKILL.md                              # Main skill overview + quick start
├── INDEX.md                              # This file - navigation guide
│
├── concepts/                             # Core architectural concepts
│   ├── api-architecture.md              # REST design, URLs, IDs, time formats
│   ├── authentication-flows.md          # OAuth flows (S2S, User, PKCE, Device)
│   └── rate-limiting-strategy.md        # Limits by plan, retry, queuing
│
├── examples/                             # Complete working code
│   ├── meeting-lifecycle.md             # Create→Update→Start→End→Delete
│   ├── user-management.md              # CRUD users, pagination, bulk ops
│   ├── recording-pipeline.md           # Download recordings via webhooks
│   ├── webhook-server.md               # Express.js CRC + signature verification
│   └── graphql-queries.md              # GraphQL queries, mutations, pagination
│
├── troubleshooting/                      # Problem solving
│   ├── common-errors.md                # HTTP codes, Zoom error codes table
│   └── common-issues.md               # Rate limits, tokens, pagination pitfalls
│
└── references/                           # 39 domain-specific reference files
    ├── authentication.md                # Auth methods reference
    ├── meetings.md                      # Meeting endpoints
    ├── users.md                         # User management endpoints
    ├── webinars.md                      # Webinar endpoints
    ├── recordings.md                    # Cloud recording endpoints
    ├── reports.md                       # Reports & analytics
    ├── accounts.md                      # Account management
    ├── rate-limits.md                   # Rate limit details
    ├── graphql.md                       # GraphQL API (beta)
    ├── zoom-team-chat.md                     # Team Chat messaging
    ├── chatbot.md                       # Chatbot integration
    ├── phone.md                         # Zoom Phone
    ├── rooms.md                         # Zoom Rooms
    ├── calendar.md                      # Zoom Calendar
    ├── mail.md                          # Zoom Mail
    ├── ai-companion.md                  # AI features
    ├── openapi.md                       # OpenAPI specs
    ├── qss.md                           # Quality of Service
    ├── contact-center.md                # Contact Center
    ├── events.md                        # Zoom Events
    ├── whiteboard.md                    # Whiteboard
    ├── clips.md                         # Zoom Clips
    ├── scheduler.md                     # Scheduler
    ├── scim2.md                         # SCIM 2.0
    ├── marketplace-apps.md              # App management
    ├── zoom-video-sdk-api.md                 # Video SDK REST
    └── ... (39 total files)
```

---

## By Use Case

### I want to create and manage meetings
1. [API Architecture](concepts/api-architecture.md) - Base URL, time formats
2. [Meeting Lifecycle](examples/meeting-lifecycle.md) - Full CRUD + webhook events
3. [Meetings Reference](references/meetings.md) - All endpoints, types, settings

### I want to manage users programmatically
1. [User Management](examples/user-management.md) - CRUD, pagination, bulk ops
2. [Users Reference](references/users.md) - Endpoints, user types, scopes

### I want to download recordings automatically
1. [Recording Pipeline](examples/recording-pipeline.md) - Webhook-triggered downloads
2. [Recordings Reference](references/recordings.md) - File types, download auth

### I want to receive real-time events
1. [Webhook Server](examples/webhook-server.md) - CRC validation, signature check
2. Cross-reference: [zoom-webhooks](../zoom-webhooks/SKILL.md) for comprehensive webhook docs
3. Cross-reference: [zoom-websockets](../zoom-websockets/SKILL.md) for WebSocket events

### I want to use GraphQL instead of REST
1. [GraphQL Queries](examples/graphql-queries.md) - Queries, mutations, pagination
2. [GraphQL Reference](references/graphql.md) - Available entities, scopes, rate limits

### I want to set up authentication
1. [Authentication Flows](concepts/authentication-flows.md) - All OAuth methods
2. Cross-reference: [zoom-oauth](../zoom-oauth/SKILL.md) for full OAuth implementation

### I'm hitting rate limits
1. [Rate Limiting Strategy](concepts/rate-limiting-strategy.md) - Limits by plan, strategies
2. [Rate Limits Reference](references/rate-limits.md) - Detailed tables
3. [Common Issues](troubleshooting/common-issues.md) - Practical solutions

### I'm getting errors
1. [Common Errors](troubleshooting/common-errors.md) - Error code tables
2. [Common Issues](troubleshooting/common-issues.md) - Diagnostic workflow

### I want to build webinars
1. [Webinars Reference](references/webinars.md) - Endpoints, types, registrants
2. [Meeting Lifecycle](examples/meeting-lifecycle.md) - Similar patterns apply

### I want to integrate Zoom Phone
1. [Phone Reference](references/phone.md) - Phone API endpoints
2. [Rate Limiting Strategy](concepts/rate-limiting-strategy.md) - Separate Phone rate limits

---

## Most Critical Documents

### 1. API Architecture (FOUNDATION)
**[concepts/api-architecture.md](concepts/api-architecture.md)**

Essential knowledge before making any API call:
- Base URLs and regional endpoints
- The `me` keyword rules (different per app type!)
- Meeting ID vs UUID double-encoding
- ISO 8601 time formats (UTC vs local)
- Download URL authentication

### 2. Rate Limiting Strategy (MOST COMMON PRODUCTION ISSUE)
**[concepts/rate-limiting-strategy.md](concepts/rate-limiting-strategy.md)**

Rate limits are per-account, shared across all apps:
- Free: 4/sec Light, 2/sec Medium, 1/sec Heavy
- Pro: 30/sec Light, 20/sec Medium, 10/sec Heavy
- Business+: 80/sec Light, 60/sec Medium, 40/sec Heavy
- Per-user: 100 meeting create/update per day

### 3. Meeting Lifecycle (MOST COMMON TASK)
**[examples/meeting-lifecycle.md](examples/meeting-lifecycle.md)**

Complete CRUD with webhook integration — the pattern most developers need first.

---

## Key Learnings

### Critical Discoveries:

1. **JWT app type is deprecated** — use Server-to-Server OAuth
   - The JWT *app type* on Marketplace is deprecated, NOT JWT token signatures
   - See: [Authentication Flows](concepts/authentication-flows.md)

2. **`me` keyword behaves differently by app type**
   - User OAuth: MUST use `me`
   - S2S OAuth: MUST NOT use `me`
   - See: [API Architecture](concepts/api-architecture.md)

3. **Rate limiting is nuanced (don’t assume a single global rule)**
   - Limits can vary by endpoint and may be enforced at account/app/user levels
   - Treat quotas as potentially shared across your account and implement backoff
   - Monitor rate limit response headers (for example `X-RateLimit-Remaining`)
   - See: [Rate Limiting Strategy](concepts/rate-limiting-strategy.md)

4. **100 meeting creates per user per day**
   - This is a hard per-user limit, not related to rate limits
   - Distribute across host users for bulk operations
   - See: [Rate Limiting Strategy](concepts/rate-limiting-strategy.md)

5. **UUID double-encoding is required for certain UUIDs**
   - UUIDs starting with `/` or containing `//` must be double-encoded
   - See: [API Architecture](concepts/api-architecture.md)

6. **Pagination: use `next_page_token`, not `page_number`**
   - `page_number` is legacy and being phased out
   - `next_page_token` is the recommended approach
   - See: [Common Issues](troubleshooting/common-issues.md)

7. **GraphQL is at `/v3/graphql`, not `/v2/`**
   - Single endpoint, cursor-based pagination
   - Rate limits apply per-field (each field = one REST equivalent)
   - See: [GraphQL Queries](examples/graphql-queries.md)

---

## Quick Reference

### "401 Unauthorized"
→ [Authentication Flows](concepts/authentication-flows.md) - Token expired or wrong scopes

### "429 Too Many Requests"
→ [Rate Limiting Strategy](concepts/rate-limiting-strategy.md) - Check headers for reset time

### "Invalid token" when using userId
→ [API Architecture](concepts/api-architecture.md) - User OAuth apps must use `me`

### "How do I paginate results?"
→ [Common Issues](troubleshooting/common-issues.md) - Use `next_page_token`

### "Webhooks not arriving"
→ [Webhook Server](examples/webhook-server.md) - CRC validation required

### "Recording download fails"
→ [Recording Pipeline](examples/recording-pipeline.md) - Bearer auth + follow redirects

### "How do I create a meeting?"
→ [Meeting Lifecycle](examples/meeting-lifecycle.md) - Full working examples

---

## Related Skills

| Skill | Use When |
|-------|----------|
| **[zoom-oauth](../zoom-oauth/SKILL.md)** | Implementing OAuth flows, token management |
| **[zoom-webhooks](../zoom-webhooks/SKILL.md)** | Deep webhook implementation, event catalog |
| **[zoom-websockets](../zoom-websockets/SKILL.md)** | WebSocket event streaming |
| **[zoom-general](../zoom-general/SKILL.md)** | Cross-product patterns, community repos |

---

**Based on Zoom REST API v2 (current) and GraphQL v3 (beta)**

# Zoom OAuth - Complete Documentation Index

## Quick Start Path

**If you're new to Zoom OAuth, follow this order:**

1. **Choose your OAuth flow** → [concepts/oauth-flows.md](concepts/oauth-flows.md)
   - 4 flows: S2S (backend), User (SaaS), Device (no browser), Chatbot
   - Decision matrix: Which flow fits your use case?

2. **Understand token lifecycle** → [concepts/token-lifecycle.md](concepts/token-lifecycle.md)
   - **CRITICAL**: How tokens expire, refresh, and revoke
   - Common pitfalls: refresh token rotation

3. **Implement your flow** → Jump to examples:
   - Backend automation → [examples/s2s-oauth-redis.md](examples/s2s-oauth-redis.md)
   - SaaS app → [examples/user-oauth-mysql.md](examples/user-oauth-mysql.md)
   - Mobile/SPA → [examples/pkce-implementation.md](examples/pkce-implementation.md)
   - Device (TV/kiosk) → [examples/device-flow.md](examples/device-flow.md)

4. **Fix redirect URI issues** → [troubleshooting/redirect-uri-issues.md](troubleshooting/redirect-uri-issues.md)
   - Most common OAuth error: Redirect URI mismatch

5. **Implement token refresh** → [examples/token-refresh.md](examples/token-refresh.md)
   - Automatic middleware pattern
   - Handle refresh token rotation

6. **Troubleshoot errors** → [troubleshooting/common-errors.md](troubleshooting/common-errors.md)
   - Error code tables (4700-4741 range)
   - Quick diagnostic workflow

---

## Documentation Structure

```
zoom-oauth/
├── SKILL.md                           # Main skill overview
├── INDEX.md                           # This file - navigation guide
│
├── concepts/                          # Core OAuth concepts
│   ├── oauth-flows.md                # 4 flows: S2S, User, Device, Chatbot
│   ├── token-lifecycle.md            # Expiration, refresh, revocation
│   ├── pkce.md                       # PKCE security for public clients
│   ├── scopes-architecture.md        # Classic vs Granular scopes
│   └── state-parameter.md            # CSRF protection with state
│
├── examples/                          # Complete working code
│   ├── s2s-oauth-basic.md            # S2S OAuth minimal example
│   ├── s2s-oauth-redis.md            # S2S OAuth with Redis caching (production)
│   ├── user-oauth-basic.md           # User OAuth minimal example
│   ├── user-oauth-mysql.md           # User OAuth with MySQL + encryption (production)
│   ├── device-flow.md                # Device authorization flow
│   ├── pkce-implementation.md        # PKCE for SPAs/mobile apps
│   └── token-refresh.md              # Auto-refresh middleware pattern
│
├── troubleshooting/                   # Problem solving guides
│   ├── common-errors.md              # Error codes 4700-4741
│   ├── redirect-uri-issues.md        # Most common OAuth error
│   ├── token-issues.md               # Expired, revoked, invalid tokens
│   └── scope-issues.md               # Scope mismatch errors
│
└── references/                        # Reference documentation
    ├── oauth-errors.md                # Complete error code reference
    ├── classic-scopes.md              # Classic scope reference
    └── granular-scopes.md             # Granular scope reference
```

---

## By Use Case

### I want to automate Zoom tasks on my own account
1. [OAuth Flows](concepts/oauth-flows.md#server-to-server-s2s-oauth) - S2S OAuth explained
2. [S2S OAuth Redis](examples/s2s-oauth-redis.md) - Production pattern with Redis caching
3. [Token Lifecycle](concepts/token-lifecycle.md) - 1hr token, no refresh

### I want to build a SaaS app for other Zoom users
1. [OAuth Flows](concepts/oauth-flows.md#user-authorization-oauth) - User OAuth explained
2. [User OAuth MySQL](examples/user-oauth-mysql.md) - Production pattern with encryption
3. [Token Refresh](examples/token-refresh.md) - Automatic refresh middleware
4. [Redirect URI Issues](troubleshooting/redirect-uri-issues.md) - Fix most common error

### I want to build a mobile or SPA app
1. [PKCE](concepts/pkce.md) - Why PKCE is required for public clients
2. [PKCE Implementation](examples/pkce-implementation.md) - Complete code example
3. [State Parameter](concepts/state-parameter.md) - CSRF protection

### I want to build an app for devices without browsers (TV, kiosk)
1. [OAuth Flows](concepts/oauth-flows.md#device-authorization-flow) - Device flow explained
2. [Device Flow Example](examples/device-flow.md) - Complete polling implementation
3. [Common Errors](troubleshooting/common-errors.md) - Device-specific errors

### I'm building a Team Chat bot
1. [OAuth Flows](concepts/oauth-flows.md#client-authorization-chatbot) - Chatbot flow explained
2. [S2S OAuth Basic](examples/s2s-oauth-basic.md) - Similar pattern, different grant type
3. [Scopes Architecture](concepts/scopes-architecture.md) - Chatbot-specific scopes

### I'm getting redirect URI errors (4709)
1. [Redirect URI Issues](troubleshooting/redirect-uri-issues.md) - **START HERE!**
2. [Common Errors](troubleshooting/common-errors.md#4709-redirect-uri-mismatch) - Error details
3. [User OAuth Basic](examples/user-oauth-basic.md) - See correct pattern

### I'm getting token errors (4700-4741)
1. [Token Issues](troubleshooting/token-issues.md) - Diagnostic workflow
2. [Token Lifecycle](concepts/token-lifecycle.md) - Understand expiration
3. [Token Refresh](examples/token-refresh.md) - Implement auto-refresh
4. [Common Errors](troubleshooting/common-errors.md) - Error code tables

### I'm getting scope errors (4711)
1. [Scope Issues](troubleshooting/scope-issues.md) - Mismatch causes
2. [Scopes Architecture](concepts/scopes-architecture.md) - Classic vs Granular
3. [Classic Scopes](references/classic-scopes.md) - Complete scope reference
4. [Granular Scopes](references/granular-scopes.md) - Granular scope reference

### I need to refresh tokens
1. [Token Lifecycle](concepts/token-lifecycle.md#refresh-strategy) - When to refresh
2. [Token Refresh](examples/token-refresh.md) - Middleware pattern
3. [Token Issues](troubleshooting/token-issues.md#refresh-token-problems) - Common mistakes

### I want to understand the difference between Classic and Granular scopes
1. [Scopes Architecture](concepts/scopes-architecture.md) - **Complete comparison**
2. [Classic Scopes](references/classic-scopes.md) - `resource:level` format
3. [Granular Scopes](references/granular-scopes.md) - `service:action:data_claim:access` format

### I need to secure my OAuth implementation
1. [PKCE](concepts/pkce.md) - Public client security
2. [State Parameter](concepts/state-parameter.md) - CSRF protection
3. [User OAuth MySQL](examples/user-oauth-mysql.md#token-encryption) - Token encryption at rest

### I want to migrate from JWT app to S2S OAuth
1. [S2S OAuth Redis](examples/s2s-oauth-redis.md) - Modern replacement
2. [Token Lifecycle](concepts/token-lifecycle.md) - Different token behavior

> **Note**: JWT App Type was deprecated in June 2023. Migrate to S2S OAuth for server-to-server automation.

---

## Most Critical Documents

### 1. OAuth Flows (DECISION DOCUMENT)
**[concepts/oauth-flows.md](concepts/oauth-flows.md)**

Understand which of the 4 flows to use:
- **S2S OAuth**: Backend automation (your account)
- **User OAuth**: SaaS apps (users authorize you)
- **Device Flow**: Devices without browsers
- **Chatbot**: Team Chat bots only

### 2. Token Lifecycle (MOST COMMON ISSUE)
**[concepts/token-lifecycle.md](concepts/token-lifecycle.md)**

99% of OAuth issues stem from misunderstanding:
- Token expiration (1 hour for all flows)
- Refresh token rotation (must save new refresh token)
- Revocation behavior (invalidates all tokens)

### 3. Redirect URI Issues (MOST COMMON ERROR)
**[troubleshooting/redirect-uri-issues.md](troubleshooting/redirect-uri-issues.md)**

Error 4709 ("Redirect URI mismatch") is the #1 OAuth error.
Must match EXACTLY (including trailing slash, http vs https).

---

## Key Learnings

### Critical Discoveries:

1. **Refresh Token Rotation**
   - Each refresh returns a NEW refresh token
   - Old refresh token becomes invalid
   - Failure to save new token causes 4735 errors
   - See: [Token Refresh](examples/token-refresh.md)

2. **S2S OAuth Uses Redis, User OAuth Uses Database**
   - S2S: Single token for entire account → Redis (ephemeral)
   - User: Per-user tokens → Database (persistent)
   - See: [S2S OAuth Redis](examples/s2s-oauth-redis.md) vs [User OAuth MySQL](examples/user-oauth-mysql.md)

3. **Redirect URI Must Match EXACTLY**
   - Trailing slash matters: `/callback` ≠ `/callback/`
   - Protocol matters: `http://` ≠ `https://`
   - Port matters: `:3000` ≠ `:3001`
   - See: [Redirect URI Issues](troubleshooting/redirect-uri-issues.md)

4. **PKCE Required for Public Clients**
   - Mobile apps CANNOT keep secrets
   - SPAs CANNOT keep secrets
   - PKCE prevents authorization code interception
   - See: [PKCE](concepts/pkce.md)

5. **State Parameter Prevents CSRF**
   - Generate random state before redirect
   - Store in session
   - Verify on callback
   - See: [State Parameter](concepts/state-parameter.md)

6. **Token Storage Must Be Encrypted**
   - NEVER store tokens in plain text
   - Use AES-256 minimum
   - See: [User OAuth MySQL](examples/user-oauth-mysql.md#token-encryption)

7. **JWT App Type is Deprecated (June 2023)**
   - No new JWT apps can be created
   - Existing apps still work but will eventually be sunset
   - Migrate to S2S OAuth or User OAuth

8. **Scope Levels Determine Authorization Requirements**
   - No suffix (user-level): Any user can authorize
   - `:admin`: Requires admin role
   - `:master`: Requires account owner (multi-account)
   - See: [Scopes Architecture](concepts/scopes-architecture.md)

9. **Authorization Codes Expire in 5 Minutes**
   - Exchange code for token immediately
   - Don't cache authorization codes
   - See: [Token Lifecycle](concepts/token-lifecycle.md#authorization-code-expiration)

10. **Device Flow Requires Polling**
    - Poll at interval returned by `/devicecode` (usually 5s)
    - Handle `authorization_pending`, `slow_down`, `expired_token`
    - See: [Device Flow](examples/device-flow.md)

---

## Quick Reference

### "Which OAuth flow should I use?"
→ [OAuth Flows](concepts/oauth-flows.md)

### "Redirect URI mismatch error (4709)"
→ [Redirect URI Issues](troubleshooting/redirect-uri-issues.md)

### "Token expired or invalid"
→ [Token Issues](troubleshooting/token-issues.md)

### "Refresh token invalid (4735)"
→ [Token Refresh](examples/token-refresh.md) - Must save new refresh token

### "Scope mismatch error (4711)"
→ [Scope Issues](troubleshooting/scope-issues.md)

### "How do I secure my OAuth app?"
→ [PKCE](concepts/pkce.md) + [State Parameter](concepts/state-parameter.md)

### "How do I implement auto-refresh?"
→ [Token Refresh](examples/token-refresh.md)

### "What's the difference between Classic and Granular scopes?"
→ [Scopes Architecture](concepts/scopes-architecture.md)

### "What error code means what?"
→ [Common Errors](troubleshooting/common-errors.md)

---

## Document Version

Based on **Zoom OAuth API v2** (2024+)

**Deprecated:** JWT App Type (June 2023)

---

**Happy coding!**

Remember: Start with [OAuth Flows](concepts/oauth-flows.md) to understand which flow fits your use case!

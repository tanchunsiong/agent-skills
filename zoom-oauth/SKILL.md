---
name: zoom-oauth
description: |
  Zoom OAuth authentication and authorization. Covers four authorization flows: Account (S2S), 
  User (authorization code), Device (device flow), and Client (chatbot). Use when implementing 
  authentication for Zoom APIs, managing access tokens, or understanding OAuth flows.
triggers:
  - zoom oauth
  - zoom authentication
  - zoom authorization
  - server to server oauth
  - s2s oauth
  - zoom access token
  - zoom refresh token
  - authorization code flow
  - device authorization
  - pkce
  - zoom api authentication
  - oauth error 4709
  - oauth error 4733
  - oauth error 4735
  - redirect uri mismatch
---

# Zoom OAuth

Authentication and authorization for Zoom APIs.

## 📖 Complete Documentation

For comprehensive guides, production patterns, and troubleshooting, see **[INDEX.md](INDEX.md)**.

Quick navigation:
- **[OAuth Flows](concepts/oauth-flows.md)** - Which flow to use and how each works
- **[Token Lifecycle](concepts/token-lifecycle.md)** - Expiration, refresh, and revocation
- **[Production Examples](examples/s2s-oauth-redis.md)** - Redis caching, MySQL storage, auto-refresh
- **[Troubleshooting](troubleshooting/common-errors.md)** - Error codes 4700-4741

## Prerequisites

- Zoom app created in [Marketplace](https://marketplace.zoom.us/)
- Client ID and Client Secret
- For S2S OAuth: Account ID

## Four Authorization Use Cases

| Use Case | App Type | Grant Type | Industry Name |
|----------|----------|------------|---------------|
| **Account Authorization** | Server-to-Server | `account_credentials` | Client Credentials Grant, M2M, Two-legged OAuth |
| **User Authorization** | General | `authorization_code` | Authorization Code Grant, Three-legged OAuth |
| **Device Authorization** | General | `urn:ietf:params:oauth:grant-type:device_code` | Device Authorization Grant (RFC 8628) |
| **Client Authorization** | General | `client_credentials` | Client Credentials Grant (chatbot-scoped) |

### Industry Terminology

| Term | Meaning |
|------|---------|
| **Two-legged OAuth** | No user involved (client ↔ server) |
| **Three-legged OAuth** | User involved (user ↔ client ↔ server) |
| **M2M** | Machine-to-Machine (backend services) |
| **Public client** | Can't keep secrets (mobile, SPA) → use PKCE |
| **Confidential client** | Can keep secrets (backend servers) |
| **PKCE** | Proof Key for Code Exchange (RFC 7636), pronounced "pixy" |

### Which Flow Should I Use?

```
                              ┌─────────────────────┐
                              │  What are you       │
                              │  building?          │
                              └──────────┬──────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                    ▼                    ▼                    ▼
          ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
          │  Backend        │  │  App for other  │  │  Chatbot only   │
          │  automation     │  │  users/accounts │  │  (Team Chat)    │
          │  (your account) │  │                 │  │                 │
          └────────┬────────┘  └────────┬────────┘  └────────┬────────┘
                   │                    │                    │
                   ▼                    │                    ▼
          ┌─────────────────┐           │           ┌─────────────────┐
          │    ACCOUNT      │           │           │     CLIENT      │
          │   (S2S OAuth)   │           │           │   (Chatbot)     │
          └─────────────────┘           │           └─────────────────┘
                                        │
                                        ▼
                              ┌─────────────────────┐
                              │  Does device have   │
                              │  a browser?         │
                              └──────────┬──────────┘
                                         │
                         ┌───────────────┴───────────────┐
                         │ NO                         YES│
                         ▼                               ▼
          ┌─────────────────────────┐         ┌─────────────────┐
          │        DEVICE           │         │      USER       │
          │     (Device Flow)       │         │  (Auth Code)    │
          │                         │         │                 │
          │ Examples:               │         │ + PKCE if       │
          │ • Smart TV              │         │   public client │
          │ • Meeting SDK device    │         │                 │
          └─────────────────────────┘         └─────────────────┘
```

---

## Account Authorization (Server-to-Server OAuth)

For backend automation without user interaction.

### Request Access Token

```bash
POST https://zoom.us/zoom-oauth/token?grant_type=account_credentials&account_id={ACCOUNT_ID}

Headers:
Authorization: Basic {Base64(ClientID:ClientSecret)}
```

### Response

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 3600,
  "scope": "user:read:user:admin",
  "api_url": "https://api.zoom.us"
}
```

### Refresh

Access tokens expire after **1 hour**. No separate refresh flow - just request a new token.

---

## User Authorization (Authorization Code Flow)

For apps that act on behalf of users.

### Step 1: Redirect User to Authorize

```
https://zoom.us/zoom-oauth/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}
```

**Optional Parameters:**

| Parameter | Description |
|-----------|-------------|
| `state` | CSRF protection, maintains state through flow |
| `code_challenge` | For PKCE (see below) |
| `code_challenge_method` | `S256` or `plain` (default: plain) |

### Step 2: User Authorizes

- User signs in and grants permission
- Redirects to `redirect_uri` with authorization code:
  ```
  https://example.com/?code={AUTHORIZATION_CODE}
  ```

### Step 3: Exchange Code for Token

```bash
POST https://zoom.us/zoom-oauth/token?grant_type=authorization_code&code={CODE}&redirect_uri={REDIRECT_URI}

Headers:
Authorization: Basic {Base64(ClientID:ClientSecret)}
```

**With PKCE:** Add `code_verifier` parameter.

### Response

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "refresh_token": "eyJ...",
  "expires_in": 3600,
  "scope": "user:read:user",
  "api_url": "https://api.zoom.us"
}
```

### Refresh Token

```bash
POST https://zoom.us/zoom-oauth/token?grant_type=refresh_token&refresh_token={REFRESH_TOKEN}

Headers:
Authorization: Basic {Base64(ClientID:ClientSecret)}
```

- Access tokens expire after **1 hour**
- Refresh token lifetime can vary; ~90 days is common for some user-based flows. Treat it as configuration/behavior that can change and rely on runtime errors + re-auth fallback.
- Always use the latest refresh token for the next request
- If refresh token expires, redirect user to authorization URL to restart flow

### User-Level vs Account-Level Apps

| Type | Who Can Authorize | Scope Access |
|------|-------------------|--------------|
| **User-level** | Any individual user | Scoped to themselves |
| **Account-level** | User with admin permissions | Account-wide access (admin scopes) |

---

## Device Authorization (Device Flow)

For devices without browsers (e.g., Meeting SDK apps).

### Prerequisites

Enable "Use App on Device" in: Features > Embed > Enable Meeting SDK

### Step 1: Request Device Code

```bash
POST https://zoom.us/zoom-oauth/devicecode?client_id={CLIENT_ID}

Headers:
Authorization: Basic {Base64(ClientID:ClientSecret)}
```

### Response

```json
{
  "device_code": "DEVICE_CODE",
  "user_code": "abcd1234",
  "verification_uri": "https://zoom.us/oauth_device",
  "verification_uri_complete": "https://zoom.us/zoom-oauth/device/complete/{CODE}",
  "expires_in": 900,
  "interval": 5
}
```

### Step 2: User Authorization

Direct user to:
- `verification_uri` and display `user_code` for manual entry, OR
- `verification_uri_complete` (user code prefilled)

User signs in and allows the app.

### Step 3: Poll for Token

Poll at the `interval` (5 seconds) until user authorizes:

```bash
POST https://zoom.us/zoom-oauth/token?grant_type=urn:ietf:params:oauth:grant-type:device_code&device_code={DEVICE_CODE}

Headers:
Authorization: Basic {Base64(ClientID:ClientSecret)}
```

### Response

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "refresh_token": "eyJ...",
  "expires_in": 3599,
  "scope": "user:read:user user:read:token",
  "api_url": "https://api.zoom.us"
}
```

### Polling Responses

| Response | Meaning | Action |
|----------|---------|--------|
| Token returned | User authorized | Store tokens, done |
| `error: authorization_pending` | User hasn't authorized yet | Keep polling at interval |
| `error: slow_down` | Polling too fast | Increase interval by 5 seconds |
| `error: expired_token` | Device code expired (15 min) | Restart flow from Step 1 |
| `error: access_denied` | User denied authorization | Handle denial, don't retry |

### Polling Implementation

```javascript
async function pollForToken(deviceCode, interval) {
  while (true) {
    await sleep(interval * 1000);
    
    try {
      const response = await axios.post(
        `https://zoom.us/zoom-oauth/token?grant_type=urn:ietf:params:oauth:grant-type:device_code&device_code=${deviceCode}`,
        null,
        { headers: { 'Authorization': `Basic ${credentials}` } }
      );
      return response.data; // Success - got tokens
    } catch (error) {
      const err = error.response?.data?.error;
      if (err === 'authorization_pending') continue;
      if (err === 'slow_down') { interval += 5; continue; }
      throw error; // expired_token or access_denied
    }
  }
}
```

### Refresh

Same as User Authorization. If refresh token expires, restart device flow from Step 1.

---

## Client Authorization (Chatbot)

For chatbot message operations only.

### Request Token

```bash
POST https://zoom.us/zoom-oauth/token?grant_type=client_credentials

Headers:
Authorization: Basic {Base64(ClientID:ClientSecret)}
```

### Response

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 3600,
  "scope": "imchat:bot",
  "api_url": "https://api.zoom.us"
}
```

### Refresh

Tokens expire after **1 hour**. No refresh flow - just request a new token.

---

## Using Access Tokens

### Call API

```bash
GET https://api.zoom.us/v2/users/me

Headers:
Authorization: Bearer {ACCESS_TOKEN}
```

### Me Context

Replace `userID` with `me` to target the token's associated user:

| Endpoint | Methods |
|----------|---------|
| `/v2/users/me` | GET, PATCH |
| `/v2/users/me/token` | GET |
| `/v2/users/me/meetings` | GET, POST |

---

## Revoke Access Token

Works for all authorization types.

```bash
POST https://zoom.us/zoom-oauth/revoke?token={ACCESS_TOKEN}

Headers:
Authorization: Basic {Base64(ClientID:ClientSecret)}
```

### Response

```json
{
  "status": "success"
}
```

---

## PKCE (Proof Key for Code Exchange)

For public clients that can't securely store secrets (mobile apps, SPAs, desktop apps).

### When to Use PKCE

| Client Type | Use PKCE? | Why |
|-------------|-----------|-----|
| Mobile app | **Yes** | Can't securely store client secret |
| Single Page App (SPA) | **Yes** | JavaScript is visible to users |
| Desktop app | **Yes** | Binary can be decompiled |
| Meeting SDK (client-side) | **Yes** | Runs on user's device |
| Backend server | Optional | Can keep secrets, but PKCE adds security |

### How PKCE Works

```
┌──────────┐                              ┌──────────┐                    ┌──────────┐
│  Client  │                              │   Zoom   │                    │   Zoom   │
│   App    │                              │  Auth    │                    │  Token   │
└────┬─────┘                              └────┬─────┘                    └────┬─────┘
     │                                         │                              │
     │ 1. Generate code_verifier (random)      │                              │
     │ 2. Create code_challenge = SHA256(verifier)                            │
     │                                         │                              │
     │ ─────── /authorize + code_challenge ──► │                              │
     │                                         │                              │
     │ ◄────── authorization_code ──────────── │                              │
     │                                         │                              │
     │ ─────────────── /token + code_verifier ─┼────────────────────────────► │
     │                                         │                              │
     │                                         │     Verify: SHA256(verifier) │
     │                                         │            == challenge      │
     │                                         │                              │
     │ ◄───────────────────────────────────────┼─────── access_token ──────── │
     │                                         │                              │
```

### Implementation (Node.js)

```javascript
const crypto = require('crypto');

function generatePKCE() {
  const verifier = crypto.randomBytes(32).toString('base64url');
  const challenge = crypto.createHash('sha256').update(verifier).digest('base64url');
  return { verifier, challenge };
}

const pkce = generatePKCE();

const authUrl = `https://zoom.us/zoom-oauth/authorize?` +
  `response_type=code&` +
  `client_id=${CLIENT_ID}&` +
  `redirect_uri=${REDIRECT_URI}&` +
  `code_challenge=${pkce.challenge}&` +
  `code_challenge_method=S256`;

// Store pkce.verifier in session for callback
```

### Token Exchange with PKCE

```bash
POST https://zoom.us/zoom-oauth/token?grant_type=authorization_code&code={CODE}&redirect_uri={REDIRECT_URI}&code_verifier={VERIFIER}

Headers:
Authorization: Basic {Base64(ClientID:ClientSecret)}
```

---

## Deauthorization

When a user removes your app, Zoom sends a webhook to your Deauthorization Notification Endpoint URL.

### Webhook Event

```json
{
  "event": "app_deauthorized",
  "event_ts": 1740439732278,
  "payload": {
    "account_id": "ACCOUNT_ID",
    "user_id": "USER_ID",
    "signature": "SIGNATURE",
    "deauthorization_time": "2019-06-17T13:52:28.632Z",
    "client_id": "CLIENT_ID"
  }
}
```

### Requirements

- **Delete all associated user data** after receiving this event
- **Verify webhook signature** (use secret token, verification token deprecated Oct 2023)
- Only public apps receive deauthorization webhooks (not private/dev apps)

---

## Pre-Approval Flow

Some Zoom accounts require Marketplace admin pre-approval before users can authorize apps.

- Users can request pre-approval from their admin
- Account-level apps (admin scopes) require appropriate role permissions

---

## Active Apps Notifier (AAN)

In-meeting feature showing apps with real-time access to content.

- Displays icon + tooltip with app info, content type being accessed, approving account
- Supported: Zoom client 5.6.7+, Meeting SDK 5.9.0+

---

## OAuth Scopes

### Scope Types

| Type | Description | For |
|------|-------------|-----|
| **Classic scopes** | Legacy scopes (user, admin, master levels) | Existing apps |
| **Granular scopes** | New fine-grained scopes with optional support | New apps |

### Classic Scopes

For previously-created apps. Three levels:
- **User-level**: Access to individual user's data
- **Admin-level**: Account-wide access, requires admin role
- **Master-level**: For master-sub account setups, requires account owner

Full list: https://developers.zoom.us/docs/integrations/oauth-scopes/

### Granular Scopes

For new apps. Format: `<service>:<action>:<data_claim>:<access>`

| Component | Values |
|-----------|--------|
| **service** | `meeting`, `webinar`, `user`, `recording`, etc. |
| **action** | `read`, `write`, `update`, `delete` |
| **data_claim** | Data category (e.g., `participants`, `settings`) |
| **access** | empty (user), `admin`, `master` |

Example: `meeting:read:list_meetings:admin`

Full list: https://developers.zoom.us/docs/integrations/oauth-scopes-granular/

### Optional Scopes

Granular scopes can be marked as **optional** - users choose whether to grant them.

**Basic authorization** (uses build flow defaults):
```
https://zoom.us/zoom-oauth/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}
```

**Advanced authorization** (custom scopes per request):
```
https://zoom.us/zoom-oauth/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={required_scopes}&optional_scope={optional_scopes}
```

**Include previously granted scopes:**
```
https://zoom.us/zoom-oauth/authorize?...&include_granted_scopes&scope={additional_scopes}
```

### Migrating Classic to Granular

1. Manage > select app > edit
2. Scope page > Development tab > click **Migrate**
3. Review auto-assigned granular scopes, remove unnecessary, mark optional
4. Test
5. Production tab > click **Migrate**

**Notes:**
- No review needed if only migrating or reducing scopes
- Existing user tokens continue with classic scope values until re-authorization
- New users get granular scopes after migration

---

## Common Error Codes

| Code | Message | Solution |
|------|---------|----------|
| 4700 | Token cannot be empty | Check Authorization header has valid token |
| 4702/4704 | Invalid client | Verify Client ID and Client Secret |
| 4705 | Grant type not supported | Use: `account_credentials`, `authorization_code`, `urn:ietf:params:oauth:grant-type:device_code`, or `client_credentials` |
| 4706 | Client ID or secret missing | Add credentials to header or request params |
| 4709 | Redirect URI mismatch | Ensure redirect_uri matches app configuration exactly (including trailing slash) |
| 4711 | Refresh token invalid | Token scopes don't match client scopes |
| 4717 | App has been disabled | Contact Zoom support |
| 4733 | Code is expired | Authorization codes expire in 5 minutes - restart flow |
| 4734 | Invalid authorization code | Regenerate authorization code |
| 4735 | Owner of token does not exist | User was removed from account - re-authorize |
| 4741 | Token has been revoked | Use the most recent token from latest authorization |

See `references/oauth-errors.md` for complete error list.

---

## Quick Reference

| Flow | Grant Type | Token Expiry | Refresh |
|------|------------|--------------|---------|
| Account (S2S) | `account_credentials` | 1 hour | Request new token |
| User | `authorization_code` | 1 hour | Use refresh_token (90 day expiry) |
| Device | `urn:ietf:params:oauth:grant-type:device_code` | 1 hour | Use refresh_token (90 day expiry) |
| Client (Chatbot) | `client_credentials` | 1 hour | Request new token |

---

## Live Demo

Interactive demo of all 4 OAuth flows: **http://www.aiweshipcode.com/zoom-oauth/project/**

## Resources

- **OAuth docs**: https://developers.zoom.us/docs/integrations/zoom-oauth/
- **S2S OAuth docs**: https://developers.zoom.us/docs/internal-apps/s2s-zoom-oauth/
- **PKCE blog**: https://developers.zoom.us/blog/pcke-oauth-with-postman-zoom-rest-api/
- **Classic scopes**: https://developers.zoom.us/docs/integrations/oauth-scopes/
- **Granular scopes**: https://developers.zoom.us/docs/integrations/oauth-scopes-granular/

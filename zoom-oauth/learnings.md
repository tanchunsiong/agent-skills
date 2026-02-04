# Zoom OAuth Learnings

Key insights and patterns discovered while implementing Zoom OAuth flows.

## Authorization Flow Selection

### Decision Matrix

| Scenario | Flow | Why |
|----------|------|-----|
| Backend automation (own account) | S2S OAuth | No user interaction needed, account-wide access |
| SaaS app for other users | User Auth | Users authorize your app to act on their behalf |
| Device without browser (TV, kiosk) | Device Flow | User authorizes on separate device |
| Team Chat bot only | Chatbot | Simple, scoped to `imchat:bot` |
| Mobile/SPA app | User Auth + PKCE | Public client can't keep secrets |

### Two-Legged vs Three-Legged

| Type | User Involved? | Zoom Flows |
|------|----------------|------------|
| Two-legged | No | S2S OAuth, Chatbot |
| Three-legged | Yes | User Auth, Device Flow |

## Token Behavior

### Expiration Summary

| Flow | Access Token | Refresh Token |
|------|--------------|---------------|
| S2S OAuth | 1 hour | None (request new) |
| User Auth | 1 hour | 90 days |
| Device Flow | 1 hour | 90 days |
| Chatbot | 1 hour | None (request new) |

### Refresh Strategy

**S2S/Chatbot:** Just request a new token before expiry. Simple.

**User/Device:** 
- Store refresh token securely
- Use refresh token to get new access token
- Always use the LATEST refresh token (each refresh returns a new one)
- If refresh token expires (90 days), user must re-authorize

## Common Implementation Patterns

### Base64 Encoding Credentials

```javascript
const credentials = Buffer.from(`${clientId}:${clientSecret}`).toString('base64');
// Use in header: Authorization: Basic {credentials}
```

### PKCE Implementation

```javascript
const crypto = require('crypto');

function generatePKCE() {
  const verifier = crypto.randomBytes(32).toString('base64url');
  const challenge = crypto.createHash('sha256').update(verifier).digest('base64url');
  return { verifier, challenge };
}
```

### State Parameter (CSRF Protection)

```javascript
const state = crypto.randomBytes(16).toString('hex');
// Store in session, verify on callback
```

## Device Flow Polling

Device flow requires polling with specific handling:

| Response | Meaning | Action |
|----------|---------|--------|
| Token returned | User authorized | Store tokens, done |
| `authorization_pending` | User hasn't authorized yet | Keep polling |
| `slow_down` | Polling too fast | Increase interval |
| `expired_token` | Code expired (15 min) | Restart flow |

```javascript
// Poll at the interval returned by devicecode endpoint (usually 5 seconds)
const interval = response.data.interval * 1000; // Convert to ms
```

## Error Code Patterns

| Code Range | Category |
|------------|----------|
| 4700 | Token issues |
| 4702-4706 | Client/credentials issues |
| 4709 | Redirect URI issues |
| 4711 | Scope mismatch |
| 4717 | App disabled |
| 4724 | JWT issues |
| 4732-4734 | Authorization code issues |
| 4735-4741 | Token lifecycle issues |

### Most Common Errors

1. **4709 Redirect URI mismatch** - URL must match EXACTLY (including trailing slash)
2. **4733 Code expired** - Auth codes only valid for 5 minutes
3. **4741 Token revoked** - Using old token after re-authorization

## Scope Patterns

### Classic vs Granular

| Type | Format | Example |
|------|--------|---------|
| Classic | `resource:level` | `meeting:write:admin` |
| Granular | `service:action:data_claim:access` | `meeting:write:meeting:admin` |

### Scope Levels

| Level | Access | Who Can Authorize |
|-------|--------|-------------------|
| (none/user) | Own data only | Any user |
| `:admin` | Account-wide | Admin role |
| `:master` | Sub-accounts | Account owner (MA) |

## Integration Tips

### Nginx Proxy Setup

```nginx
location /zoom-oauth/project/auth/ {
    proxy_pass http://localhost:4004/auth/;
    proxy_set_header X-Forwarded-Proto $scheme;  # Critical for OAuth redirects
}
```

### Session Management

- Store tokens server-side (never expose to client)
- Use session ID to key user tokens
- Clear tokens on logout/revoke

### Token Storage (Production)

| Environment | Storage |
|-------------|---------|
| Development | In-memory object |
| Production | Redis/Database with encryption |

## Gotchas

1. **S2S Account ID** - Must be the Zoom Account ID, not user ID
2. **Redirect URI encoding** - Must URL-encode in the request
3. **PKCE code_verifier** - Must store between authorize and callback
4. **Multiple authorizations** - Each new auth invalidates previous tokens
5. **Device flow prerequisite** - Must enable "Use App on Device" in app settings

## Testing Checklist

- [ ] Token acquisition works
- [ ] Token refresh works (User/Device flows)
- [ ] Token revocation works
- [ ] API calls succeed with token
- [ ] Error handling for expired tokens
- [ ] Error handling for invalid credentials
- [ ] State parameter validates correctly
- [ ] PKCE challenge/verifier matches

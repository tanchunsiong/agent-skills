# Zoom Apps SDK - OAuth

OAuth flow for Zoom Apps.

## Overview

Zoom Apps use OAuth for user authentication and API access.

## OAuth Flow

```
1. User opens your Zoom App
          ↓
2. App redirects to Zoom authorization
          ↓
3. User grants permission
          ↓
4. Zoom redirects back with auth code
          ↓
5. Exchange code for tokens
          ↓
6. Use tokens to access Zoom APIs
```

## In-Client Authorization

For apps running inside Zoom client:

```javascript
// Check if user is authorized
const auth = await zoomSdk.authorize();

if (!auth.isAuthorized) {
  // Trigger OAuth flow
  await zoomSdk.promptAuthorize();
}
```

## Token Exchange

Server-side token exchange:

```javascript
const response = await fetch('https://zoom.us/oauth/token', {
  method: 'POST',
  headers: {
    'Authorization': `Basic ${base64(clientId + ':' + clientSecret)}`,
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    code: authCode,
    redirect_uri: redirectUri
  })
});

const { access_token, refresh_token } = await response.json();
```

## Token Refresh

```javascript
const response = await fetch('https://zoom.us/oauth/token', {
  method: 'POST',
  headers: {
    'Authorization': `Basic ${base64(clientId + ':' + clientSecret)}`,
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  body: new URLSearchParams({
    grant_type: 'refresh_token',
    refresh_token: refreshToken
  })
});
```

## Scopes for Zoom Apps

Common scopes for Zoom Apps:
- `zoomapp:inmeeting` - In-meeting functionality
- `user:read` - Read user profile

## Resources

- **OAuth docs**: https://developers.zoom.us/docs/zoom-apps/guides/auth/

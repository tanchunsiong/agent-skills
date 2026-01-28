# Zoom Phone OAuth Scopes

Required OAuth scopes for Zoom Phone API operations.

## Scope Categories

### User-Level Scopes

Access user's own data:

| Scope | Description | Use For |
|-------|-------------|---------|
| `phone:read` | Read phone settings | Get user's phone config |
| `phone:write` | Write phone settings | Update settings, make calls |
| `phone_call_log:read` | Read call logs | Get call history |
| `phone_recording:read` | Read recordings | Download call recordings |
| `phone_voicemail:read` | Read voicemails | Access voicemail |
| `phone_voicemail:write` | Write voicemails | Update voicemail status |
| `phone_sms:read` | Read SMS | Get SMS history |
| `phone_sms:write` | Write SMS | Send SMS messages |

### Admin-Level Scopes

Access account-wide data (admin accounts only):

| Scope | Description | Use For |
|-------|-------------|---------|
| `phone:read:admin` | Read all phone data | List all users, numbers |
| `phone:write:admin` | Write all phone data | Manage users, settings |
| `phone_call_log:read:admin` | Read all call logs | Account-wide call history |
| `phone_recording:read:admin` | Read all recordings | Access any recording |
| `phone_sms:read:admin` | Read all SMS | Account-wide SMS history |
| `phone_sms:write:admin` | Write SMS as any user | Send SMS from any user |
| `phone_call_queue:read:admin` | Read call queues | List queues, members |
| `phone_call_queue:write:admin` | Write call queues | Create, update queues |
| `phone_auto_receptionist:read:admin` | Read IVR | List auto receptionists |
| `phone_auto_receptionist:write:admin` | Write IVR | Create, update IVR |
| `phone_number:read:admin` | Read phone numbers | List all numbers |
| `phone_number:write:admin` | Write phone numbers | Assign, update numbers |

## Common Combinations

### Smart Embed SDK (User Calling)

```
phone:read
phone:write
phone_sms:read
phone_sms:write
```

### CRM Integration (User + History)

```
phone:read
phone:write
phone_call_log:read
phone_sms:read
phone_sms:write
```

### Admin Dashboard (Full Account)

```
phone:read:admin
phone:write:admin
phone_call_log:read:admin
phone_recording:read:admin
phone_call_queue:read:admin
phone_number:read:admin
```

### SMS Notifications Only

```
phone_sms:write
```

### Call Recording Access

```
phone_recording:read
phone_call_log:read
```

## Scope by Endpoint

| Endpoint | Required Scope |
|----------|----------------|
| `GET /phone/users` | `phone:read:admin` |
| `GET /phone/users/me` | `phone:read` |
| `POST /phone/users/{userId}/calls` | `phone:write` |
| `GET /phone/users/{userId}/call_logs` | `phone_call_log:read` |
| `GET /phone/call_logs` | `phone_call_log:read:admin` |
| `GET /phone/users/{userId}/recordings` | `phone_recording:read` |
| `POST /phone/users/{userId}/sms/messages` | `phone_sms:write` |
| `GET /phone/users/{userId}/sms/messages` | `phone_sms:read` |
| `GET /phone/call_queues` | `phone_call_queue:read:admin` |
| `POST /phone/call_queues` | `phone_call_queue:write:admin` |
| `GET /phone/auto_receptionists` | `phone_auto_receptionist:read:admin` |
| `GET /phone/numbers` | `phone_number:read:admin` |
| `PATCH /phone/numbers/{numberId}` | `phone_number:write:admin` |

## Requesting Scopes

### OAuth 2.0 Authorization URL

```
https://zoom.us/oauth/authorize?
  response_type=code&
  client_id=YOUR_CLIENT_ID&
  redirect_uri=YOUR_REDIRECT_URI&
  scope=phone:read%20phone:write%20phone_sms:write
```

### Server-to-Server OAuth

For Server-to-Server OAuth apps, request scopes during app creation in the Marketplace. These are automatically included in the token.

## Scope Errors

```json
{
  "code": 403,
  "message": "Forbidden: Missing scope phone:write"
}
```

If you see this error, your OAuth token is missing the required scope. Either:
1. Re-authorize with the correct scopes (user OAuth)
2. Update app scopes in Marketplace and regenerate token (S2S OAuth)

## Resources

- **OAuth setup**: See `zoom-platform/references/authentication.md`
- **Marketplace**: https://marketplace.zoom.us/

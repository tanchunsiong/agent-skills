# Error Codes Reference

Comprehensive reference for error codes across Zoom APIs and SDKs.

## Important: Error Code 0 = Success

**The enum value 0 typically represents SUCCESS, not failure.**

```cpp
// Meeting SDK
SDKERR_SUCCESS = 0        // Success!
SDKERR_UNKNOWN = 1        // Unknown error

// Video SDK  
Errors_Success = 0        // Success!
Errors_Unknown = 1        // Unknown error
```

Always check SDK enum definitions - don't assume 0 is an error.

---

## REST API Errors

### HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Request completed |
| 201 | Created | Resource created |
| 204 | No Content | Success, no body |
| 400 | Bad Request | Check request body/params |
| 401 | Unauthorized | Refresh token or re-auth |
| 403 | Forbidden | Check scopes/permissions |
| 404 | Not Found | Resource doesn't exist |
| 429 | Rate Limited | Back off and retry |
| 500 | Server Error | Retry with backoff |

### Common API Error Codes

| Code | Message | Cause | Solution |
|------|---------|-------|----------|
| 124 | Invalid access token | Token expired/invalid | Refresh OAuth token |
| 200 | No permission | Missing scope | Add required scope |
| 300 | Meeting not found | Invalid meeting ID | Verify meeting exists |
| 1001 | User not found | Invalid user ID/email | Check user exists |
| 3001 | Meeting is over | Meeting ended | Cannot modify ended meeting |
| 3161 | Meeting host key invalid | Wrong host key | Verify host key |

### Rate Limit Response

```json
{
  "code": 429,
  "message": "Rate limit exceeded"
}
```

**Headers to check:**
- `X-RateLimit-Limit` - Max requests allowed
- `X-RateLimit-Remaining` - Requests remaining
- `Retry-After` - Seconds to wait

---

## Meeting SDK Error Codes

### Authentication Errors (AuthResult)

| Code | Enum | Cause | Solution |
|------|------|-------|----------|
| 0 | AUTHRET_SUCCESS | Auth succeeded | - |
| 1 | AUTHRET_KEYORSECRETEMPTY | Missing credentials | Provide SDK key/secret |
| 2 | AUTHRET_KEYORSECRETWRONG | Invalid credentials | Check key/secret |
| 3 | AUTHRET_ACCOUNTNOTSUPPORT | Account restriction | Contact Zoom support |
| 4 | AUTHRET_ACCOUNTNOTENABLESDK | SDK not enabled | Enable SDK in Marketplace |
| 5 | AUTHRET_TOKENWRONG | Invalid JWT | Regenerate signature |
| 6 | AUTHRET_TOKENEXPIRED | JWT expired | Generate fresh signature |
| 7 | AUTHRET_NETWORKISSUE | Network error | Check connectivity |
| 8 | AUTHRET_UNKNOWN | Unknown error | Check logs |

### Join Meeting Errors (SDKError)

| Code | Enum | Cause | Solution |
|------|------|-------|----------|
| 0 | SDKERR_SUCCESS | Join succeeded | - |
| 1 | SDKERR_NO_IMPL | Not implemented | Check SDK version |
| 2 | SDKERR_WRONG_USAGE | API misuse | Check API call sequence |
| 3 | SDKERR_INVALID_PARAMETER | Bad parameter | Verify all params |
| 4 | SDKERR_MODULE_LOAD_FAILED | Module failed | Check SDK installation |
| 5 | SDKERR_MEMORY_FAILED | Memory error | Free resources |
| 6 | SDKERR_SERVICE_FAILED | Service error | Retry |
| 7 | SDKERR_UNINITIALIZE | Not initialized | Call initialize first |

### Meeting Status Codes (MeetingStatus)

| Code | Enum | Description |
|------|------|-------------|
| 0 | MEETING_STATUS_IDLE | Not in meeting |
| 1 | MEETING_STATUS_CONNECTING | Connecting |
| 2 | MEETING_STATUS_WAITINGFORHOST | Waiting for host |
| 3 | MEETING_STATUS_INMEETING | In meeting |
| 4 | MEETING_STATUS_DISCONNECTING | Disconnecting |
| 5 | MEETING_STATUS_RECONNECTING | Reconnecting |
| 6 | MEETING_STATUS_FAILED | Join failed |
| 7 | MEETING_STATUS_ENDED | Meeting ended |

### Meeting Failure Codes (MeetingFailCode)

| Code | Enum | Cause | Solution |
|------|------|-------|----------|
| 0 | MEETING_SUCCESS | No failure | - |
| 1 | MEETING_FAIL_NETWORK_ERR | Network error | Check connectivity |
| 2 | MEETING_FAIL_RECONNECT_ERR | Reconnect failed | Rejoin meeting |
| 3 | MEETING_FAIL_MMR_ERR | Media server error | Retry |
| 4 | MEETING_FAIL_PASSWORD_ERR | Wrong password | Check password |
| 5 | MEETING_FAIL_SESSION_ERR | Session error | Rejoin |
| 6 | MEETING_FAIL_MEETING_OVER | Meeting ended | - |
| 7 | MEETING_FAIL_MEETING_NOT_START | Not started | Wait for host |
| 8 | MEETING_FAIL_MEETING_NOT_EXIST | Meeting not found | Check meeting ID |
| 9 | MEETING_FAIL_USER_FULL | Meeting at capacity | - |
| 10 | MEETING_FAIL_NO_MMR | No media server | Internal error |
| 11 | MEETING_FAIL_CONFLOCKED | Meeting locked | Ask host to unlock |
| 12 | MEETING_FAIL_MEETING_RESTRICTED | Restricted | Check account settings |
| 13 | MEETING_FAIL_JBH_DISABLED | JBH disabled | Wait for host |
| 14 | MEETING_FAIL_NEED_REGISTER | Registration required | Register first |
| 15 | MEETING_FAIL_WEBINAR_DENIED | Webinar denied | Check registration |
| 16 | MEETING_FAIL_HOST_DENY | Host denied entry | Ask host for access |
| 17 | MEETING_FAIL_REMOVED_BY_HOST | Removed by host | - |

---

## Video SDK Error Codes

### Session Errors (Errors)

| Code | Enum | Cause | Solution |
|------|------|-------|----------|
| 0 | Errors_Success | Success | - |
| 1 | Errors_Wrong_Usage | API misuse | Check call sequence |
| 2 | Errors_Internal_Error | Internal error | Check logs |
| 3 | Errors_Uninitialize | Not initialized | Call init first |
| 4 | Errors_Invalid_Parameter | Bad param | Verify parameters |
| 5 | Errors_Call_Too_Frequently | Rate limited | Add delay |
| 6 | Errors_No_Impl | Not implemented | Check platform support |
| 7 | Errors_Dont_Support_Feature | Feature unsupported | Check plan/platform |
| 8 | Errors_Unknown | Unknown | Check logs |

### Session Join Errors

| Code | Enum | Cause | Solution |
|------|------|-------|----------|
| 0 | SessionJoinSuccess | Joined | - |
| 1 | SessionJoinFailed_InvalidSession | Bad session name | Check topic string |
| 2 | SessionJoinFailed_InvalidJWT | Invalid signature | Regenerate JWT |
| 3 | SessionJoinFailed_SessionExpired | Session expired | Rejoin |
| 4 | SessionJoinFailed_Timeout | Connection timeout | Check network |
| 5 | SessionJoinFailed_RemovedByHost | Removed | - |
| 6 | SessionJoinFailed_MaxParticipants | At capacity | - |

---

## Webhook Errors

### Webhook Validation Errors

| Scenario | Response Code | Fix |
|----------|---------------|-----|
| Signature mismatch | 401 | Check WEBHOOK_SECRET |
| Timestamp too old | 401 | Server clock sync |
| Invalid payload | 400 | Check JSON parsing |

### Validation Code Example

```javascript
const crypto = require('crypto');

function verifyWebhook(req) {
  const signature = req.headers['x-zm-signature'];
  const timestamp = req.headers['x-zm-request-timestamp'];
  
  // Check timestamp (reject if >5 min old)
  const now = Math.floor(Date.now() / 1000);
  if (Math.abs(now - parseInt(timestamp)) > 300) {
    return { valid: false, error: 'Timestamp too old' };
  }
  
  // Verify signature
  const payload = `v0:${timestamp}:${JSON.stringify(req.body)}`;
  const expectedSig = 'v0=' + crypto
    .createHmac('sha256', WEBHOOK_SECRET)
    .update(payload)
    .digest('hex');
  
  if (signature !== expectedSig) {
    return { valid: false, error: 'Signature mismatch' };
  }
  
  return { valid: true };
}
```

---

## Error Handling Best Practices

### Retry Strategy

```javascript
async function callWithRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.response?.status === 429) {
        // Rate limited - wait and retry
        const retryAfter = error.response.headers['retry-after'] || 60;
        await sleep(retryAfter * 1000);
        continue;
      }
      if (error.response?.status >= 500) {
        // Server error - exponential backoff
        await sleep(Math.pow(2, i) * 1000);
        continue;
      }
      throw error; // Don't retry client errors
    }
  }
  throw new Error('Max retries exceeded');
}
```

### Error Logging Pattern

```javascript
function logZoomError(context, error) {
  console.error({
    context,
    timestamp: new Date().toISOString(),
    httpStatus: error.response?.status,
    zoomCode: error.response?.data?.code,
    zoomMessage: error.response?.data?.message,
    requestId: error.response?.headers?.['x-zm-request-id'],
  });
}
```

## Resources

- **API Error Codes**: https://developers.zoom.us/docs/api/rest/error-handling/
- **SDK Documentation**: https://developers.zoom.us/docs/meeting-sdk/
- **Developer Forum**: https://devforum.zoom.us/

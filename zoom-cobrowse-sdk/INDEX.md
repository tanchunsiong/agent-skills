# Zoom Cobrowse SDK - Complete Documentation Index

**Complete navigation guide for all Cobrowse SDK documentation.**

## Getting Started (Start Here!)

If you're new to Zoom Cobrowse SDK, follow this learning path:

1. **[SKILL.md](SKILL.md)** - Main overview and quick start
2. **[Get Started Guide](get-started.md)** - Step-by-step setup from credentials to first session
3. **[Session Lifecycle](concepts/session-lifecycle.md)** - Understand the complete customer and agent flow
4. **[Customer Integration](examples/customer-integration.md)** - Integrate SDK into your website
5. **[Agent Integration](examples/agent-integration.md)** - Set up agent portal

## Core Concepts

Foundational concepts you need to understand:

- **[Two Roles Pattern](concepts/two-roles-pattern.md)** - Customer (role_type=1) vs Agent (role_type=2) architecture
- **[Session Lifecycle](concepts/session-lifecycle.md)** - Complete flow: init → start → PIN → connect → end
- **[JWT Authentication](concepts/jwt-authentication.md)** - Token structure, signing, SDK Key vs API Key
- **[Distribution Methods](concepts/distribution-methods.md)** - CDN vs npm (BYOP mode)

## Examples and Patterns

Complete working examples for common scenarios:

### Session Management
- **[Customer Integration](examples/customer-integration.md)** - Complete customer-side implementation (CDN and npm)
- **[Agent Integration](examples/agent-integration.md)** - Iframe and npm agent setup patterns
- **[Session Events](examples/session-events.md)** - Handle all session lifecycle events
- **[Auto-Reconnection](examples/auto-reconnection.md)** - Page refresh and session recovery

### Features
- **[Annotation Tools](examples/annotations.md)** - Enable drawing, highlighting, vanishing pen
- **[Privacy Masking](examples/privacy-masking.md)** - Mask sensitive fields with CSS selectors
- **[Remote Assist](examples/remote-assist.md)** - Agent can scroll customer's page
- **[Multi-Tab Persistence](examples/multi-tab-persistence.md)** - Session continues across browser tabs
- **[BYOP Custom PIN](examples/byop-custom-pin.md)** - Bring Your Own PIN with npm integration

## References

Complete API and configuration references:

### SDK Reference
- **[API Reference](references/api-reference.md)** - All SDK methods and interfaces
  - ZoomCobrowseSDK.init()
  - session.start()
  - session.join()
  - session.end()
  - session.on()
  - session.getSessionInfo()
  
- **[Settings Reference](references/settings-reference.md)** - All initialization settings
  - allowAgentAnnotation
  - allowCustomerAnnotation
  - piiMask
  - remoteAssist
  - multiTabSessionPersistence

- **[Session Events Reference](references/session-events.md)** - All event types
  - pincode_updated
  - session_started
  - session_ended
  - agent_joined
  - agent_left
  - session_error
  - session_reconnecting
  - remote_assist_started
  - remote_assist_stopped

### Error Reference
- **[Error Codes](references/error-codes.md)** - Complete error code reference
  - 1001-1017: Session errors
  - 2001: Token errors
  - 9999: Service errors

### Official Documentation
- **[Get Started](references/get-started.md)** - Official get started documentation (crawled)
- **[Features](references/features.md)** - Official features documentation (crawled)
- **[Authorization](references/authorization.md)** - Official JWT authorization docs (crawled)
- **[API Documentation](references/api.md)** - Crawled API reference docs

## Troubleshooting

Quick diagnostics and common issue resolution:

- **[Common Issues](troubleshooting/common-issues.md)** - Quick fixes for frequent problems
  - SDK not loading
  - Token generation fails
  - Agent can't connect
  - Fields not masked
  - Session doesn't reconnect after refresh

- **[Error Codes](troubleshooting/error-codes.md)** - Error code lookup and solutions
  - Session start/join failures (1001, 1011, 1016)
  - Session limit errors (1002, 1004, 1012, 1013, 1015)
  - PIN code errors (1006, 1008, 1009, 1010)
  - Token errors (2001)

- **[CORS and CSP](troubleshooting/cors-csp.md)** - Cross-origin and Content Security Policy setup
  - Access-Control-Allow-Origin headers
  - Content-Security-Policy headers
  - Cross-origin iframe handling
  - Same-origin iframe handling

- **[Browser Compatibility](troubleshooting/browser-compatibility.md)** - Browser requirements and limitations
  - Supported browsers (Chrome 80+, Firefox 78+, Safari 14+, Edge 80+)
  - Internet Explorer not supported
  - Privacy mode limitations
  - Third-party cookie requirements

## By Use Case

Find documentation by what you're trying to do:

### I want to...

**Set up cobrowse for the first time:**
- [Get Started Guide](get-started.md)
- [JWT Authentication](concepts/jwt-authentication.md)
- [Customer Integration](examples/customer-integration.md)
- [Agent Integration](examples/agent-integration.md)

**Add annotation tools:**
- [Annotation Tools Example](examples/annotations.md)
- [Settings Reference - allowAgentAnnotation](references/settings-reference.md#allowa gentannotation)
- [Settings Reference - allowCustomerAnnotation](references/settings-reference.md#allowcustomerannotation)

**Hide sensitive data from agents:**
- [Privacy Masking Example](examples/privacy-masking.md)
- [Settings Reference - piiMask](references/settings-reference.md#piimask)

**Let agents control customer's page:**
- [Remote Assist Example](examples/remote-assist.md)
- [Settings Reference - remoteAssist](references/settings-reference.md#remoteassist)

**Use custom PIN codes:**
- [BYOP Custom PIN Example](examples/byop-custom-pin.md)
- [JWT Authentication - enable_byop](concepts/jwt-authentication.md#enable-byop)

**Handle page refreshes:**
- [Auto-Reconnection Example](examples/auto-reconnection.md)
- [Session Lifecycle - Recovery](concepts/session-lifecycle.md#session-recovery)

**Integrate with npm (not CDN):**
- [BYOP Custom PIN Example](examples/byop-custom-pin.md)
- [Distribution Methods](concepts/distribution-methods.md#npm-integration)

**Debug session connection issues:**
- [Common Issues](troubleshooting/common-issues.md)
- [Error Codes](troubleshooting/error-codes.md)
- [Session Events - session_error](examples/session-events.md#session-error)

**Configure CORS and CSP headers:**
- [CORS and CSP Guide](troubleshooting/cors-csp.md)
- [Browser Compatibility](troubleshooting/browser-compatibility.md)

## By Error Code

Quick lookup for error code solutions:

### Session Errors
- **1001** (SESSION_START_FAILED) → [Error Codes](troubleshooting/error-codes.md#1001-session-start-failed)
- **1002** (SESSION_CONNECTING_IN_PROGRESS) → [Error Codes](troubleshooting/error-codes.md#1002-session-connecting-in-progress)
- **1004** (SESSION_COUNT_LIMIT) → [Error Codes](troubleshooting/error-codes.md#1004-session-count-limit)
- **1011** (SESSION_JOIN_FAILED) → [Error Codes](troubleshooting/error-codes.md#1011-session-join-failed)
- **1012** (SESSION_CUSTOMER_COUNT_LIMIT) → [Error Codes](troubleshooting/error-codes.md#1012-session-customer-count-limit)
- **1013** (SESSION_AGENT_COUNT_LIMIT) → [Error Codes](troubleshooting/error-codes.md#1013-session-agent-count-limit)
- **1015** (SESSION_DUPLICATE_USER) → [Error Codes](troubleshooting/error-codes.md#1015-session-duplicate-user)
- **1016** (NETWORK_ERROR) → [Error Codes](troubleshooting/error-codes.md#1016-network-error)
- **1017** (SESSION_CANCELING_IN_PROGRESS) → [Error Codes](troubleshooting/error-codes.md#1017-session-canceling-in-progress)

### PIN Errors
- **1006** (SESSION_JOIN_PIN_NOT_FOUND) → [Error Codes](troubleshooting/error-codes.md#1006-session-join-pin-not-found)
- **1008** (SESSION_PIN_INVALID_FORMAT) → [Error Codes](troubleshooting/error-codes.md#1008-session-pin-invalid-format)
- **1009** (SESSION_START_PIN_REQUIRED) → [Error Codes](troubleshooting/error-codes.md#1009-session-start-pin-required)
- **1010** (SESSION_START_PIN_CONFLICT) → [Error Codes](troubleshooting/error-codes.md#1010-session-start-pin-conflict)

### Auth Errors
- **2001** (TOKEN_INVALID) → [Error Codes](troubleshooting/error-codes.md#2001-token-invalid)

### Service Errors
- **9999** (UNDEFINED) → [Error Codes](troubleshooting/error-codes.md#9999-undefined)

## Official Resources

External documentation and samples:

- **Official Docs**: https://developers.zoom.us/docs/zoom-cobrowse-sdk/
- **API Reference**: https://marketplacefront.zoom.us/sdk/cobrowse/
- **Quickstart Repo**: https://github.com/zoom/CobrowseSDK-Quickstart
- **Auth Endpoint Sample**: https://github.com/zoom/cobrowsesdk-auth-endpoint-sample
- **Dev Forum**: https://devforum.zoom.us/
- **Developer Blog**: https://developers.zoom.us/blog/?category=zoom-cobrowse-sdk

## Documentation Structure

```
zoom-cobrowse-sdk/
├── SKILL.md                    # Main skill entry point
├── INDEX.md                    # This file - complete navigation
├── get-started.md              # Step-by-step setup guide
│
├── concepts/                   # Core concepts
│   ├── two-roles-pattern.md
│   ├── session-lifecycle.md
│   ├── jwt-authentication.md
│   └── distribution-methods.md
│
├── examples/                   # Working examples
│   ├── customer-integration.md
│   ├── agent-integration.md
│   ├── annotations.md
│   ├── privacy-masking.md
│   ├── remote-assist.md
│   ├── multi-tab-persistence.md
│   ├── byop-custom-pin.md
│   ├── session-events.md
│   └── auto-reconnection.md
│
├── references/                 # API and config references
│   ├── api-reference.md        # SDK methods
│   ├── settings-reference.md   # Init settings
│   ├── session-events.md       # Event types
│   ├── error-codes.md          # Error reference
│   ├── get-started.md          # Official docs (crawled)
│   ├── features.md             # Official docs (crawled)
│   ├── authorization.md        # Official docs (crawled)
│   └── api.md                  # API docs (crawled)
│
└── troubleshooting/            # Problem resolution
    ├── common-issues.md
    ├── error-codes.md
    ├── cors-csp.md
    └── browser-compatibility.md
```

## Search Tips

**Find by keyword:**
- "annotation" → [Annotation Tools](examples/annotations.md)
- "mask" or "privacy" → [Privacy Masking](examples/privacy-masking.md)
- "PIN" or "custom PIN" → [BYOP Custom PIN](examples/byop-custom-pin.md)
- "JWT" or "token" → [JWT Authentication](concepts/jwt-authentication.md)
- "error" → [Error Codes](troubleshooting/error-codes.md)
- "CORS" or "CSP" → [CORS and CSP](troubleshooting/cors-csp.md)
- "iframe" → [Agent Integration](examples/agent-integration.md)
- "npm" → [Distribution Methods](concepts/distribution-methods.md), [BYOP](examples/byop-custom-pin.md)
- "refresh" or "reconnect" → [Auto-Reconnection](examples/auto-reconnection.md)
- "agent" → [Agent Integration](examples/agent-integration.md), [Two Roles Pattern](concepts/two-roles-pattern.md)
- "customer" → [Customer Integration](examples/customer-integration.md), [Two Roles Pattern](concepts/two-roles-pattern.md)

---

**Not finding what you need?** Check the [Official Documentation](https://developers.zoom.us/docs/zoom-cobrowse-sdk/) or ask on the [Dev Forum](https://devforum.zoom.us/).

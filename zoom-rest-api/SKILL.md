---
name: zoom-rest-api
description: |
  Zoom REST API with 600+ endpoints for meetings, users, webinars, recordings, and reports.
  Use when making server-side API calls to Zoom services, creating meetings programmatically,
  or managing Zoom resources.
---

# Zoom REST API

Server-side API for managing Zoom resources programmatically.

## Prerequisites

- Zoom app with OAuth or Server-to-Server OAuth credentials
- Appropriate scopes for the endpoints you need

## Quick Start

```bash
# Get access token (Server-to-Server OAuth)
curl -X POST "https://zoom.us/oauth/token?grant_type=account_credentials&account_id={accountId}" \
  -H "Authorization: Basic {base64(clientId:clientSecret)}"

# Create a meeting
curl -X POST "https://api.zoom.us/v2/users/me/meetings" \
  -H "Authorization: Bearer {accessToken}" \
  -H "Content-Type: application/json" \
  -d '{"topic": "My Meeting", "type": 2}'
```

## Base URL

```
https://api.zoom.us/v2
```

## Quick Reference

| Task | Endpoint |
|------|----------|
| Create meeting | `POST /users/{userId}/meetings` |
| Get meeting | `GET /meetings/{meetingId}` |
| List users | `GET /users` |
| Get recordings | `GET /users/{userId}/recordings` |

## Detailed References

### Core APIs
- **[references/meetings.md](references/meetings.md)** - Meeting operations
- **[references/users.md](references/users.md)** - User management
- **[references/webinars.md](references/webinars.md)** - Webinar operations
- **[references/recordings.md](references/recordings.md)** - Cloud recordings
- **[references/reports.md](references/reports.md)** - Usage reports
- **[references/calendar.md](references/calendar.md)** - Zoom Calendar API

### Team Communication
- **[references/team-chat.md](references/team-chat.md)** - Team Chat messaging API
- **[references/chatbot.md](references/chatbot.md)** - Build interactive chatbots

### Infrastructure
- **[references/rooms.md](references/rooms.md)** - Zoom Rooms management
- **[references/rate-limits.md](references/rate-limits.md)** - API rate limits
- **[references/qss.md](references/qss.md)** - Quality of Service Subscription

### AI Features
- **[references/ai-companion.md](references/ai-companion.md)** - Meeting summaries, transcripts, AI content

### Alternative APIs
- **[references/graphql.md](references/graphql.md)** - GraphQL API (beta) - flexible queries

### Developer Tools
- **[references/openapi.md](references/openapi.md)** - OpenAPI/Swagger specs, Postman, code generation

## Sample Repositories

### Official (by Zoom)

| Type | Repository | Stars |
|------|------------|-------|
| OAuth | [zoom-oauth-sample-app](https://github.com/zoom/zoom-oauth-sample-app) | 91 |
| S2S OAuth Starter | [server-to-server-oauth-starter-api](https://github.com/zoom/server-to-server-oauth-starter-api) | 54 |
| User OAuth | [user-level-oauth-starter](https://github.com/zoom/user-level-oauth-starter) | 27 |
| S2S Token | [server-to-server-oauth-token](https://github.com/zoom/server-to-server-oauth-token) | 15 |
| Rivet Library | [rivet-javascript](https://github.com/zoom/rivet-javascript) | 13 |
| WebSocket | [websocket-js-sample](https://github.com/zoom/websocket-js-sample) | 5 |
| Python S2S | [server-to-server-python-sample](https://github.com/zoom/server-to-server-python-sample) | 4 |

### Community

| Language | Repository | Description |
|----------|------------|-------------|
| Laravel | [JubaerHossain/zoom-laravel](https://github.com/JubaerHossain/zoom-laravel) | Laravel Zoom API client |
| PHP | [skwirrel/ZoomAPIWrapper](https://github.com/skwirrel/ZoomAPIWrapper) | Simple PHP wrapper |
| PHP | [espresso-dev/zoom-php](https://github.com/espresso-dev/zoom-php) | PHP Zoom API class |
| Python | [slim-python/zoom-api-integration-create-meeting-example-code-in-python](https://github.com/slim-python/zoom-api-integration-create-meeting-example-code-in-python) | Meeting creation example |
| Node.js | [sedenardi/zoomapi](https://github.com/sedenardi/zoomapi) | Node.js API library |
| Spring Boot | [soorya218/zoom_api_integration_using_springboot_webclient](https://github.com/soorya218/zoom_api_integration_using_springboot_webclient) | Spring Boot + WebClient |
| C# | [apresence/ZoomJWT](https://github.com/apresence/ZoomJWT) | JWT library for .NET |

**Full list**: See [zoom-general/references/community-repos.md](../zoom-general/references/community-repos.md)

## Resources

- **API Reference**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/
- **Postman Collection**: https://marketplace.zoom.us/docs/api-reference/postman
- **Developer forum**: https://devforum.zoom.us/

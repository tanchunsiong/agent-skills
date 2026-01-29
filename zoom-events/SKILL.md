---
name: zoom-events
description: |
  Zoom Events API integration guide for large-scale virtual and hybrid events. Covers multi-session 
  conferences, expo halls, registration management, speakers, sponsors, and analytics.
  Use when building event platforms, conference management systems, or integrating with 
  Zoom Events (formerly Zoom Webinars Plus).
---

# Zoom Events API

Build large-scale virtual and hybrid event integrations with Zoom Events APIs.

## Overview

Zoom Events (formerly Zoom Webinars Plus) enables hosting large-scale virtual and hybrid events with:
- Multi-session conferences with tracks
- Expo halls and sponsor booths
- Networking sessions
- Registration management
- Speaker and sponsor management
- Event analytics and engagement metrics

## Key Features

| Feature | Description |
|---------|-------------|
| **Multi-Session Events** | Create conferences with multiple tracks and sessions |
| **Registration Management** | Handle attendee registration with approval workflows |
| **Expo & Booths** | Virtual expo halls with sponsor booths |
| **Speaker Management** | Add and manage event speakers |
| **Analytics** | Track attendance and engagement metrics |
| **Networking** | Built-in networking session support |

## Choose Your Integration

| I want to... | Use this |
|--------------|----------|
| Create and manage events | **Events REST API** |
| Add sessions to events | **Sessions API** |
| Handle registrations | **Registration API** |
| Manage speakers | **Speakers API** |
| Set up sponsor booths | **Expo/Booths API** |
| Track event metrics | **Analytics API** |
| Get real-time event updates | **Webhooks** |

## Core Endpoints

### Events

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/events` | List events |
| POST | `/events` | Create event |
| GET | `/events/{eventId}` | Get event details |
| PATCH | `/events/{eventId}` | Update event |
| DELETE | `/events/{eventId}` | Delete event |
| POST | `/events/{eventId}/publish` | Publish event |

### Sessions

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/events/{eventId}/sessions` | List sessions |
| POST | `/events/{eventId}/sessions` | Create session |
| GET | `/events/{eventId}/sessions/{sessionId}` | Get session details |
| PATCH | `/events/{eventId}/sessions/{sessionId}` | Update session |
| DELETE | `/events/{eventId}/sessions/{sessionId}` | Delete session |

### Registration

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/events/{eventId}/registrants` | List registrants |
| POST | `/events/{eventId}/registrants` | Add registrant |
| GET | `/events/{eventId}/registrants/{registrantId}` | Get registrant details |
| PATCH | `/events/{eventId}/registrants/{registrantId}` | Update registrant |
| DELETE | `/events/{eventId}/registrants/{registrantId}` | Remove registrant |
| PUT | `/events/{eventId}/registrants/status` | Update registrant status |

### Speakers & Sponsors

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/events/{eventId}/speakers` | List speakers |
| POST | `/events/{eventId}/speakers` | Add speaker |
| GET | `/events/{eventId}/sponsors` | List sponsors |
| POST | `/events/{eventId}/sponsors` | Add sponsor |

### Expo & Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/events/{eventId}/expo/booths` | List expo booths |
| POST | `/events/{eventId}/expo/booths` | Create booth |
| GET | `/events/{eventId}/analytics` | Get event analytics |
| GET | `/events/{eventId}/engagement` | Get engagement metrics |

## Common Operations

### Create an Event

```javascript
const response = await fetch('https://api.zoom.us/v2/events', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Annual Tech Conference 2024',
    description: 'Our flagship technology conference',
    start_time: '2024-03-15T09:00:00Z',
    end_time: '2024-03-17T18:00:00Z',
    timezone: 'America/Los_Angeles',
    type: 'multi_session',
    registration_type: 'required',
    settings: {
      approval_type: 'automatic',
      attendee_limit: 5000,
      show_social_share_buttons: true
    }
  })
});

const event = await response.json();
// event.id, event.registration_url, event.hub_url
```

### Add Session to Event

```javascript
const response = await fetch(`https://api.zoom.us/v2/events/${eventId}/sessions`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'Keynote: Future of AI',
    description: 'Opening keynote presentation',
    start_time: '2024-03-15T09:00:00Z',
    duration: 60,
    type: 'webinar',
    track: 'Main Stage',
    speakers: ['speaker_abc']
  })
});
```

### List Registrants

```javascript
const response = await fetch(
  `https://api.zoom.us/v2/events/${eventId}/registrants?status=approved&page_size=100`,
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const data = await response.json();
// data.registrants contains attendee list
```

### Add a Registrant

```javascript
const response = await fetch(`https://api.zoom.us/v2/events/${eventId}/registrants`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'attendee@example.com',
    first_name: 'Jane',
    last_name: 'Smith'
  })
});
```

## Prerequisites

1. **Zoom Events license** - Account must have Zoom Events enabled
2. **OAuth app** - Create in [Zoom App Marketplace](https://marketplace.zoom.us/)
3. **Scopes** - Request appropriate event scopes (see Required Scopes)

## Common Use Cases

| Use Case | Description | Integration |
|----------|-------------|-------------|
| **Conference Platform** | Host multi-day conferences | Events + Sessions API |
| **Registration System** | Manage event sign-ups | Registration API |
| **Speaker Portal** | Manage conference speakers | Speakers API |
| **Sponsor Management** | Handle expo booths and sponsors | Sponsors + Expo API |
| **Event Analytics** | Track attendance and engagement | Analytics API |
| **Attendee Sync** | Sync registrants with CRM | Registration API + Webhooks |

## Required Scopes

| Scope | Description |
|-------|-------------|
| `event:read` | Read event data |
| `event:write` | Create and manage events |
| `event:read:admin` | Admin read access |
| `event:write:admin` | Admin write access |

## Event Types

| Type | Description |
|------|-------------|
| `single_session` | Single webinar/session event |
| `multi_session` | Multi-track conference |
| `series` | Recurring event series |

## Session Types

| Type | Description |
|------|-------------|
| `webinar` | Standard webinar session |
| `meeting` | Interactive meeting session |
| `networking` | Networking session |
| `expo` | Expo/booth session |
| `break` | Break/intermission |

## Event & Registration Status

| Event Status | Description |
|--------------|-------------|
| `draft` | Event in draft mode |
| `published` | Event is live |
| `started` | Event has started |
| `ended` | Event concluded |
| `cancelled` | Event cancelled |

| Registration Status | Description |
|---------------------|-------------|
| `pending` | Awaiting approval |
| `approved` | Registration approved |
| `denied` | Registration denied |
| `cancelled` | Registration cancelled |

## Detailed References

- **[references/events.md](references/events.md)** - Complete Events API reference

## Resources

- **API Reference**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Events
- **Zoom Events Documentation**: https://developers.zoom.us/docs/zoom-events/
- **Event Planning Guide**: https://developers.zoom.us/docs/zoom-events/planning/
- **Marketplace**: https://marketplace.zoom.us/

---
name: zoom-calendar
description: |
  Zoom Calendar API integration guide. Covers calendar events management, secondary/shared calendars,
  access controls, and external calendar integration. Use when building scheduling integrations,
  appointment booking systems, or managing calendar events programmatically.
---

# Zoom Calendar API

Manage calendar events, secondary calendars, and scheduling via Zoom's REST API.

## Overview

Zoom Calendar Service is a fully integrated calendar built into Zoom Workplace. The API allows you to:
- Create and manage calendar events
- Manage secondary/shared calendars
- Configure access controls and permissions
- Integrate with external calendar providers (Google Calendar, Microsoft 365)

## Key Features

| Feature | Description |
|---------|-------------|
| **Event Management** | Create, read, update, delete calendar events |
| **External Booking** | Allow external contacts to schedule appointments |
| **Shared Calendars** | Create team calendars for collaboration |
| **Resource Calendars** | Manage conference rooms, workspaces |
| **Delegate Scheduling** | Schedule on behalf of others |
| **Bi-Directional Sync** | Sync with Google Calendar and Microsoft 365 |

## Choose Your Integration

| I want to... | Use this |
|--------------|----------|
| Create/manage calendar events | **Calendar REST API** |
| Build an appointment booking system | **Calendar REST API + Events** |
| Create shared team calendars | **Calendar REST API** |
| Manage calendar access permissions | **Access Control endpoints** |
| Sync with Google/Outlook | **Calendar Sync** (built-in) |
| Get real-time event notifications | **Webhooks** |
| Schedule meetings with Zoom links | **Calendar API + Meetings API** |

## Core Endpoints

### Events

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/calendars/{calendarId}/events` | List events |
| POST | `/calendars/{calendarId}/events` | Create event |
| GET | `/calendars/{calendarId}/events/{eventId}` | Get event |
| PATCH | `/calendars/{calendarId}/events/{eventId}` | Update event |
| DELETE | `/calendars/{calendarId}/events/{eventId}` | Delete event |

### Calendars

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/{userId}/calendars` | List user's calendars |
| POST | `/users/{userId}/calendars` | Create secondary calendar |
| GET | `/calendars/{calendarId}` | Get calendar details |
| PATCH | `/calendars/{calendarId}` | Update calendar |
| DELETE | `/calendars/{calendarId}` | Delete calendar |

### Access Control

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/calendars/{calendarId}/access` | Get access list |
| POST | `/calendars/{calendarId}/access` | Grant access |
| DELETE | `/calendars/{calendarId}/access/{userId}` | Revoke access |

## Common Operations

### Create Calendar Event

```javascript
async function createCalendarEvent(calendarId, event) {
  const response = await fetch(
    `https://api.zoom.us/v2/calendars/${calendarId}/events`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        summary: event.title,
        description: event.description,
        start: {
          dateTime: event.startTime,  // ISO 8601
          timeZone: event.timeZone
        },
        end: {
          dateTime: event.endTime,
          timeZone: event.timeZone
        },
        attendees: event.attendees.map(email => ({ email })),
        location: event.location,
        reminders: {
          useDefault: false,
          overrides: [
            { method: 'popup', minutes: 15 }
          ]
        }
      })
    }
  );
  
  return response.json();
}

// Usage
await createCalendarEvent('primary', {
  title: 'Team Standup',
  description: 'Daily standup meeting',
  startTime: '2024-01-15T09:00:00',
  endTime: '2024-01-15T09:30:00',
  timeZone: 'America/Los_Angeles',
  attendees: ['john@example.com', 'sarah@example.com'],
  location: 'Zoom Meeting'
});
```

### List Events

```javascript
async function listEvents(calendarId, from, to) {
  const params = new URLSearchParams({
    time_min: from,  // ISO 8601
    time_max: to,
    page_size: 50
  });
  
  const response = await fetch(
    `https://api.zoom.us/v2/calendars/${calendarId}/events?${params}`,
    {
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
  
  return response.json();
}

// Get events for January 2024
const events = await listEvents(
  'primary',
  '2024-01-01T00:00:00Z',
  '2024-01-31T23:59:59Z'
);
```

### Create Secondary Calendar

```javascript
async function createSecondaryCalendar(userId, name, description) {
  const response = await fetch(
    `https://api.zoom.us/v2/users/${userId}/calendars`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: name,
        description: description,
        color: '#4285F4',
        timezone: 'America/Los_Angeles'
      })
    }
  );
  
  return response.json();
}

// Create a team calendar
await createSecondaryCalendar('me', 'Engineering Team', 'Shared engineering calendar');
```

### Share Calendar

```javascript
async function shareCalendar(calendarId, email, role) {
  const response = await fetch(
    `https://api.zoom.us/v2/calendars/${calendarId}/access`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: email,
        role: role  // 'reader', 'writer', 'owner'
      })
    }
  );
  
  return response.json();
}

// Share calendar with a colleague
await shareCalendar('calendar_abc123', 'colleague@example.com', 'writer');
```

### Create Event with Zoom Meeting

```javascript
async function createEventWithZoomMeeting(calendarId, event) {
  // 1. Create Zoom meeting first
  const meetingResponse = await fetch(
    'https://api.zoom.us/v2/users/me/meetings',
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        topic: event.title,
        type: 2,  // Scheduled meeting
        start_time: event.startTime,
        duration: event.duration,
        timezone: event.timeZone
      })
    }
  );
  
  const meeting = await meetingResponse.json();
  
  // 2. Create calendar event with meeting link
  const eventResponse = await fetch(
    `https://api.zoom.us/v2/calendars/${calendarId}/events`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        summary: event.title,
        description: `${event.description}\n\nJoin Zoom Meeting:\n${meeting.join_url}`,
        start: {
          dateTime: event.startTime,
          timeZone: event.timeZone
        },
        end: {
          dateTime: event.endTime,
          timeZone: event.timeZone
        },
        attendees: event.attendees.map(email => ({ email })),
        location: meeting.join_url,
        conferenceData: {
          conferenceId: meeting.id.toString(),
          conferenceSolution: { name: 'Zoom Meeting' },
          entryPoints: [{
            entryPointType: 'video',
            uri: meeting.join_url
          }]
        }
      })
    }
  );
  
  return {
    event: await eventResponse.json(),
    meeting: meeting
  };
}
```

## Prerequisites

1. **Zoom account** with Calendar service enabled
2. **OAuth app** - Create in [Zoom App Marketplace](https://marketplace.zoom.us/)
3. **Scopes** - Request appropriate calendar scopes for your use case

## Common Use Cases

| Use Case | Description | Integration |
|----------|-------------|-------------|
| **Appointment Booking** | External contacts schedule appointments | Calendar API + Events |
| **Team Scheduling** | Shared calendars for team coordination | Secondary Calendars |
| **Meeting Rooms** | Book conference rooms and workspaces | Resource Calendars |
| **Healthcare** | Patient appointment management | Calendar API |
| **Education** | Class schedules, office hours, tutoring | Calendar API |
| **Sales** | Schedule demos and customer meetings | Calendar + Meetings API |
| **HR** | Interview scheduling and onboarding | Calendar API |

## Webhooks

| Event | Trigger |
|-------|---------|
| `calendar.event_created` | New event created |
| `calendar.event_updated` | Event modified |
| `calendar.event_deleted` | Event deleted |
| `calendar.event_reminder` | Event reminder triggered |

See **zoom-webhooks** skill for webhook setup.

## Required Scopes

| Scope | Description |
|-------|-------------|
| `calendar:read` | Read calendar data |
| `calendar:write` | Create/update calendar events |
| `calendar:read:admin` | Account-wide read access |
| `calendar:write:admin` | Account-wide write access |

## Calendar Sync

Zoom Calendar supports bi-directional sync with:
- **Google Calendar** - OAuth-based, automatic sync
- **Microsoft 365 / Outlook** - Graph API integration

Sync features:
- Automatically enabled by default
- Stores up to 24 months of data (6 months past, 18 months future)
- Real-time synchronization via webhooks
- Tokens encrypted at rest (256-bit AES-GCM)

## Resources

- **Official docs**: https://developers.zoom.us/docs/zoom-calendar/
- **API Reference**: https://developers.zoom.us/docs/api/rest/zoom-calendar/
- **Postman Collection**: https://www.postman.com/zoom-developer
- **Marketplace**: https://marketplace.zoom.us/

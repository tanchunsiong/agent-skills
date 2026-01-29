---
name: zoom-whiteboard
description: |
  Zoom Whiteboard API integration guide. Covers creating, managing, and sharing collaborative 
  whiteboards programmatically. Use when building visual collaboration tools, project planning
  integrations, or automating whiteboard workflows within Zoom Workplace.
---

# Zoom Whiteboard API

Build visual collaboration integrations with Zoom Whiteboard's infinite canvas and real-time collaboration features.

## Overview

Zoom Whiteboard provides:
- Infinite canvas for visual collaboration
- Real-time multi-user editing
- Templates and shapes library
- Folder organization
- Export to PDF, PNG, SVG
- Sharing and permission controls

## Key Features

| Feature | Description |
|---------|-------------|
| **Create Whiteboards** | Programmatically create new whiteboards |
| **Manage Collaborators** | Add/remove users with different permission levels |
| **Organize in Folders** | Create folder hierarchies for whiteboard organization |
| **Export** | Export whiteboards to PDF, PNG, or SVG formats |
| **Templates** | Create and use templates for common board layouts |
| **Thumbnails** | Get whiteboard preview thumbnails |

## Choose Your Integration

| I want to... | Use this |
|--------------|----------|
| Create whiteboards programmatically | **Whiteboard REST API** |
| Share whiteboards with users | **Collaborators API** |
| Export whiteboards as images/PDF | **Export API** |
| Organize whiteboards in folders | **Folders API** |
| Create reusable templates | **Templates API** |
| Get real-time whiteboard events | **zoom-webhooks** |

## Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/whiteboards` | List whiteboards |
| POST | `/whiteboards` | Create whiteboard |
| GET | `/whiteboards/{whiteboardId}` | Get whiteboard details |
| PATCH | `/whiteboards/{whiteboardId}` | Update whiteboard |
| DELETE | `/whiteboards/{whiteboardId}` | Delete whiteboard |
| POST | `/whiteboards/{whiteboardId}/duplicate` | Duplicate whiteboard |
| GET | `/whiteboards/{whiteboardId}/sharing` | Get sharing settings |
| PATCH | `/whiteboards/{whiteboardId}/sharing` | Update sharing settings |
| POST | `/whiteboards/{whiteboardId}/collaborators` | Add collaborators |
| POST | `/whiteboards/{whiteboardId}/export` | Export whiteboard |
| GET | `/whiteboards/{whiteboardId}/thumbnail` | Get thumbnail |

## Common Operations

### Create a Whiteboard

```javascript
const response = await fetch('https://api.zoom.us/v2/whiteboards', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Sprint Planning Board',
    folder_id: 'folder_abc'
  })
});

const whiteboard = await response.json();
// whiteboard.id, whiteboard.share_url
```

### Add Collaborators

```javascript
await fetch(`https://api.zoom.us/v2/whiteboards/${whiteboardId}/collaborators`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    collaborators: [
      { email: 'user1@example.com', permission: 'editor' },
      { email: 'user2@example.com', permission: 'viewer' }
    ]
  })
});
```

### Export Whiteboard

```javascript
// Start export
const exportResponse = await fetch(
  `https://api.zoom.us/v2/whiteboards/${whiteboardId}/export`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      format: 'pdf',
      quality: 'high'
    })
  }
);

const { export_id } = await exportResponse.json();

// Check export status
const statusResponse = await fetch(
  `https://api.zoom.us/v2/whiteboards/${whiteboardId}/export/${export_id}`,
  { headers: { 'Authorization': `Bearer ${accessToken}` } }
);
```

## Permission Levels

| Level | Description |
|-------|-------------|
| `owner` | Full control including delete |
| `editor` | Can view and edit content |
| `commenter` | Can view and add comments |
| `viewer` | Can only view |

## Export Formats

| Format | Description |
|--------|-------------|
| `pdf` | PDF document |
| `png` | PNG image |
| `svg` | SVG vector image |

## Sharing Options

| Option | Description |
|--------|-------------|
| `private` | Only owner and collaborators |
| `organization` | All organization members |
| `public` | Anyone with link |

## Prerequisites

1. **Zoom account** with Whiteboard access
2. **OAuth app** - Create in [Zoom App Marketplace](https://marketplace.zoom.us/)
3. **Scopes** - Required permissions:
   - `whiteboard:read` - Read whiteboard data
   - `whiteboard:write` - Create/modify whiteboards
   - `whiteboard:read:admin` - Admin read access
   - `whiteboard:write:admin` - Admin write access

## Common Use Cases

| Use Case | Description | Integration |
|----------|-------------|-------------|
| **Project Planning** | Create sprint/project boards | REST API |
| **Meeting Collaboration** | Create whiteboards for meetings | REST API + Webhooks |
| **Template Library** | Manage organization templates | Templates API |
| **Export Automation** | Auto-export boards after meetings | Export API + Webhooks |
| **Access Management** | Bulk add/remove collaborators | Collaborators API |

## Webhooks

Zoom Whiteboard sends real-time events:

| Event | Trigger |
|-------|---------|
| `whiteboard.created` | New whiteboard created |
| `whiteboard.updated` | Whiteboard modified |
| `whiteboard.deleted` | Whiteboard deleted |
| `whiteboard.shared` | Sharing settings changed |

See **zoom-webhooks** skill for webhook setup.

## Resources

- **Official docs**: https://developers.zoom.us/docs/zoom-whiteboard/
- **API Reference**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Whiteboards
- **Marketplace**: https://marketplace.zoom.us/

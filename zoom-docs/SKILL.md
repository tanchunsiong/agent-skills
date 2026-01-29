---
name: zoom-docs
description: |
  Zoom Docs API integration guide. Covers creating, managing, and sharing collaborative 
  documents programmatically. Use when building document collaboration tools, knowledge base
  integrations, or automating document workflows within Zoom Workplace.
---

# Zoom Docs API

Build document collaboration integrations with Zoom Docs' real-time editing and sharing features.

## Overview

Zoom Docs provides:
- Real-time collaborative document editing
- Rich text formatting and media embedding
- Folder organization and management
- Comments and version history
- Export to multiple formats
- Integration with Zoom Workplace

## Key Features

| Feature | Description |
|---------|-------------|
| **Create Documents** | Programmatically create new documents |
| **Manage Content** | Read and update document content |
| **Collaborators** | Add/remove users with different permission levels |
| **Comments** | Add, resolve, and manage document comments |
| **Version History** | Access and restore previous versions |
| **Export** | Export documents to PDF, DOCX, Markdown, HTML |

## Choose Your Integration

| I want to... | Use this |
|--------------|----------|
| Create documents programmatically | **Docs REST API** |
| Update document content | **Content API** |
| Share documents with users | **Collaborators API** |
| Add/manage comments | **Comments API** |
| Track document changes | **Versions API** |
| Export documents | **Export API** |
| Get real-time document events | **zoom-webhooks** |

## Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/docs` | List documents |
| POST | `/docs` | Create document |
| GET | `/docs/{docId}` | Get document details |
| PATCH | `/docs/{docId}` | Update document metadata |
| DELETE | `/docs/{docId}` | Delete document |
| GET | `/docs/{docId}/content` | Get document content |
| PUT | `/docs/{docId}/content` | Update document content |
| GET | `/docs/{docId}/sharing` | Get sharing settings |
| PATCH | `/docs/{docId}/sharing` | Update sharing settings |
| POST | `/docs/{docId}/collaborators` | Add collaborators |
| GET | `/docs/{docId}/comments` | List comments |
| POST | `/docs/{docId}/comments` | Add comment |
| GET | `/docs/{docId}/versions` | List versions |
| POST | `/docs/{docId}/export` | Export document |

## Common Operations

### Create a Document

```javascript
const response = await fetch('https://api.zoom.us/v2/docs', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'Project Proposal',
    folder_id: 'folder_abc',
    template_id: 'template_xyz' // optional
  })
});

const doc = await response.json();
// doc.id, doc.share_url
```

### Add Collaborators

```javascript
await fetch(`https://api.zoom.us/v2/docs/${docId}/collaborators`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    collaborators: [
      { email: 'editor@example.com', permission: 'editor' },
      { email: 'viewer@example.com', permission: 'viewer' }
    ]
  })
});
```

### Add a Comment

```javascript
await fetch(`https://api.zoom.us/v2/docs/${docId}/comments`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    content: 'Please review this section',
    position: { start: 100, end: 150 } // text range
  })
});
```

### Export Document

```javascript
// Start export
const exportResponse = await fetch(
  `https://api.zoom.us/v2/docs/${docId}/export`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ format: 'pdf' })
  }
);

const { export_id } = await exportResponse.json();

// Check export status for download_url
const statusResponse = await fetch(
  `https://api.zoom.us/v2/docs/${docId}/export/${export_id}`,
  { headers: { 'Authorization': `Bearer ${accessToken}` } }
);
```

### Access Version History

```javascript
// List versions
const versions = await fetch(
  `https://api.zoom.us/v2/docs/${docId}/versions`,
  { headers: { 'Authorization': `Bearer ${accessToken}` } }
).then(r => r.json());

// Restore to a specific version
await fetch(`https://api.zoom.us/v2/docs/${docId}/restore`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ version_id: 'version_xyz' })
});
```

## Permission Levels

| Level | Description |
|-------|-------------|
| `owner` | Full control |
| `editor` | Can view and edit |
| `commenter` | Can view and comment |
| `viewer` | Read-only access |

## Export Formats

| Format | Description |
|--------|-------------|
| `pdf` | PDF document |
| `docx` | Microsoft Word |
| `md` | Markdown |
| `html` | HTML |

## Document Templates

Templates provide pre-formatted starting points:
- Meeting notes
- Project plans
- Team wikis
- Status reports

## Prerequisites

1. **Zoom account** with Docs access
2. **OAuth app** - Create in [Zoom App Marketplace](https://marketplace.zoom.us/)
3. **Scopes** - Required permissions:
   - `docs:read` - Read documents
   - `docs:write` - Create/edit documents
   - `docs:read:admin` - Admin read access
   - `docs:write:admin` - Admin write access

## Common Use Cases

| Use Case | Description | Integration |
|----------|-------------|-------------|
| **Meeting Notes** | Auto-create docs for meetings | REST API + Webhooks |
| **Knowledge Base** | Build searchable doc repository | REST API |
| **Document Automation** | Generate reports from templates | Templates + Content API |
| **Review Workflows** | Manage document review cycles | Comments + Versions API |
| **Export Automation** | Auto-export docs to other systems | Export API + Webhooks |

## Webhooks

Zoom Docs sends real-time events:

| Event | Trigger |
|-------|---------|
| `docs.created` | New document created |
| `docs.updated` | Document modified |
| `docs.deleted` | Document deleted |
| `docs.shared` | Sharing settings changed |
| `docs.comment_added` | New comment added |

See **zoom-webhooks** skill for webhook setup.

## Resources

- **Official docs**: https://developers.zoom.us/docs/zoom-docs/
- **API Reference**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Docs
- **Marketplace**: https://marketplace.zoom.us/

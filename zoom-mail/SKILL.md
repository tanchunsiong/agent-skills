---
name: zoom-mail
description: |
  Zoom Mail API integration guide. Covers email services integrated with Zoom Workplace including
  sending, reading, and managing email messages, folders, drafts, and attachments.
  Use when building email integrations, automated messaging, or email management solutions
  within the Zoom ecosystem.
---

# Zoom Mail API

Build email integrations with Zoom Mail API for reading, sending, and managing email within Zoom Workplace.

## Overview

Zoom Mail is an email service integrated into the Zoom platform that provides:
- Send and receive emails
- Folder management (inbox, sent, drafts, trash, etc.)
- Draft creation and management
- Attachment handling
- Message flagging and organization
- Mailbox settings configuration

## Key Features

| Feature | Description |
|---------|-------------|
| **Send Emails** | Create and send email messages programmatically |
| **Read Messages** | Access inbox, sent, and other folder messages |
| **Manage Folders** | Create, update, and delete custom folders |
| **Draft Support** | Create, edit, and send draft messages |
| **Attachments** | List and download message attachments |
| **Message Actions** | Mark read/unread, star, move between folders |

## Choose Your Integration

| I want to... | Use this |
|--------------|----------|
| Send emails programmatically | **Mail REST API** |
| Read inbox messages | **Mail REST API** |
| Manage email folders | **Mail REST API** |
| Create and send drafts | **Mail REST API** |
| Download attachments | **Mail REST API** |
| Automate email workflows | **Mail REST API** + **zoom-webhooks** |

## Core Endpoints

### Messages

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mail/mailboxes/{mailboxId}/messages` | List messages |
| GET | `/mail/mailboxes/{mailboxId}/messages/{messageId}` | Get message details |
| POST | `/mail/mailboxes/{mailboxId}/messages` | Send/create message |
| DELETE | `/mail/mailboxes/{mailboxId}/messages/{messageId}` | Delete message |
| PATCH | `/mail/mailboxes/{mailboxId}/messages/{messageId}` | Update message (read/unread, move) |

### Folders

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mail/mailboxes/{mailboxId}/folders` | List folders |
| POST | `/mail/mailboxes/{mailboxId}/folders` | Create folder |
| GET | `/mail/mailboxes/{mailboxId}/folders/{folderId}` | Get folder details |
| PATCH | `/mail/mailboxes/{mailboxId}/folders/{folderId}` | Update folder |
| DELETE | `/mail/mailboxes/{mailboxId}/folders/{folderId}` | Delete folder |

### Mailboxes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mail/mailboxes` | List user mailboxes |
| GET | `/mail/mailboxes/{mailboxId}` | Get mailbox details |
| GET | `/mail/mailboxes/{mailboxId}/settings` | Get mailbox settings |
| PATCH | `/mail/mailboxes/{mailboxId}/settings` | Update mailbox settings |

### Attachments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mail/mailboxes/{mailboxId}/messages/{messageId}/attachments` | List attachments |
| GET | `/mail/mailboxes/{mailboxId}/messages/{messageId}/attachments/{attachmentId}` | Download attachment |

### Drafts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mail/mailboxes/{mailboxId}/drafts` | List drafts |
| POST | `/mail/mailboxes/{mailboxId}/drafts` | Create draft |
| PATCH | `/mail/mailboxes/{mailboxId}/drafts/{draftId}` | Update draft |
| DELETE | `/mail/mailboxes/{mailboxId}/drafts/{draftId}` | Delete draft |
| POST | `/mail/mailboxes/{mailboxId}/drafts/{draftId}/send` | Send draft |

## Common Operations

### Send Email

```javascript
const response = await fetch(
  `https://api.zoom.us/v2/mail/mailboxes/${mailboxId}/messages`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      to: [{ email: 'recipient@example.com', name: 'John Doe' }],
      subject: 'Meeting Follow-up',
      body: {
        content_type: 'text/html',
        content: '<p>Thank you for joining the meeting today.</p>'
      },
      cc: [],
      bcc: []
    })
  }
);

const message = await response.json();
// message.id contains the sent message ID
```

### List Messages

```javascript
const response = await fetch(
  `https://api.zoom.us/v2/mail/mailboxes/${mailboxId}/messages?folder_id=inbox&page_size=50`,
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const messages = await response.json();
// messages contains inbox emails
```

### Get Message Details

```javascript
const response = await fetch(
  `https://api.zoom.us/v2/mail/mailboxes/${mailboxId}/messages/${messageId}`,
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const message = await response.json();
// message contains full email details
```

### Create and Send Draft

```javascript
// Create draft
const draftResponse = await fetch(
  `https://api.zoom.us/v2/mail/mailboxes/${mailboxId}/drafts`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      to: [{ email: 'recipient@example.com', name: 'Jane Doe' }],
      subject: 'Draft Email',
      body: {
        content_type: 'text/plain',
        content: 'This is a draft message.'
      }
    })
  }
);

const draft = await draftResponse.json();

// Send draft
await fetch(
  `https://api.zoom.us/v2/mail/mailboxes/${mailboxId}/drafts/${draft.id}/send`,
  {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);
```

### Download Attachment

```javascript
const response = await fetch(
  `https://api.zoom.us/v2/mail/mailboxes/${mailboxId}/messages/${messageId}/attachments/${attachmentId}`,
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const attachmentBlob = await response.blob();
// attachmentBlob contains the file data
```

## Standard Folders

| Folder | Description |
|--------|-------------|
| `inbox` | Incoming messages |
| `sent` | Sent messages |
| `drafts` | Draft messages |
| `trash` | Deleted messages |
| `spam` | Spam/junk messages |
| `archive` | Archived messages |

## Message Flags

| Flag | Description |
|------|-------------|
| `read` | Message has been read |
| `starred` | Message is starred/flagged |
| `important` | Message marked as important |

## Prerequisites

1. **Zoom Mail enabled** - Users need Zoom Mail service enabled
2. **OAuth app** - Create in [Zoom App Marketplace](https://marketplace.zoom.us/)
3. **Mail scopes** - Request appropriate mail permissions

## Common Use Cases

| Use Case | Description | Implementation |
|----------|-------------|----------------|
| **Automated Notifications** | Send emails from your app | POST to messages endpoint |
| **Inbox Monitoring** | Read and process incoming emails | GET messages + webhooks |
| **Email Archival** | Archive/backup email messages | GET messages, move to archive |
| **Draft Templates** | Create reusable draft templates | POST/PATCH drafts |
| **Attachment Processing** | Download and process attachments | GET attachments |
| **Folder Organization** | Create custom folder structures | POST/PATCH folders |

## Required Scopes

| Scope | Description |
|-------|-------------|
| `mail:read` | Read email messages |
| `mail:write` | Send and manage emails |
| `mail:read:admin` | Admin read access (account-level) |
| `mail:write:admin` | Admin write access (account-level) |

## Resources

- **Official docs**: https://developers.zoom.us/docs/zoom-mail/
- **API Reference**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Mail
- **Marketplace**: https://marketplace.zoom.us/

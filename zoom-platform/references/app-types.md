# App Types

Choose the right Zoom app type for your integration.

## Overview

Zoom Marketplace offers different app types based on your use case:

| App Type | Use Case | Distribution |
|----------|----------|--------------|
| **User-managed** | Your own org only | Internal |
| **Admin-managed** | Installed by admins | Internal/Marketplace |
| **OAuth** | User-authorized access | Marketplace |
| **Server-to-Server OAuth** | Server automation | Internal |
| **Meeting SDK** | Embed meetings | Marketplace |
| **Video SDK** | Custom video | Marketplace |
| **Zoom App** | In-client apps | Marketplace |

## Decision Guide

### Need to call REST APIs?

**For your own account only:**
→ Server-to-Server OAuth

**On behalf of users:**
→ OAuth app

### Need to embed video?

**Full Zoom meeting experience:**
→ Meeting SDK app

**Custom UI, your branding:**
→ Video SDK app

### Need an app inside Zoom client?

→ Zoom App

## App Type Details

### Server-to-Server OAuth

- No user interaction required
- Access your account's data only
- Best for: automation, reporting, integrations

### OAuth

- User authorizes access
- Access user's data with permission
- Best for: multi-tenant apps, marketplace apps

### Meeting SDK

- Embed Zoom meetings
- Zoom's UI or Component View
- Best for: white-label meeting solutions

### Video SDK

- Full UI control
- Your branding
- Best for: custom video experiences, telehealth

### Zoom App

- Runs inside Zoom client
- JavaScript SDK
- Best for: in-meeting tools, collaboration

## Resources

- **App types docs**: https://developers.zoom.us/docs/integrations/
- **Marketplace**: https://marketplace.zoom.us/

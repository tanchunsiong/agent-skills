---
name: agent-skills
description: |
  Zoom Developer Platform skills organized by product. Each folder contains product-specific 
  documentation and use cases. The zoom-general folder contains generic, cross-product skills 
  and references.
---

# Zoom Developer Platform Skills

This repository contains skills for building with Zoom APIs and SDKs, focused on web development.

## Folder Structure

| Folder | Description |
|--------|-------------|
| **zoom-general** | **Hub** - Cross-product use cases and shared references |
| **zoom-rest-api** | REST API calls (600+ endpoints) |
| **zoom-webhooks** | Real-time event notifications (HTTP) |
| **zoom-websockets** | Real-time event notifications (WebSocket) |
| **zoom-meeting-sdk** | Embed Zoom meetings in your app (Web) |
| **zoom-video-sdk** | Custom video experiences (Web) |
| **zoom-apps-sdk** | Apps that run inside the Zoom client |
| **zoom-rtms** | Real-Time Media Streams (live audio/video/transcripts) |
| **zoom-team-chat** | Team Chat messaging and channels |
| **zoom-ui-toolkit** | Pre-built React components for Video SDK |
| **zoom-cobrowse-sdk** | Collaborative browsing for support |

## How to Use

1. **Product-specific task?** → Go to that product's folder (e.g., `zoom-meeting-sdk/`)
2. **Cross-product or general task?** → Check `zoom-general/` for generic use cases
3. **Each folder has a `SKILL.md`** → Start there for that product's overview

## zoom-general (Hub)

The `zoom-general` folder contains:

- **Cross-product use cases** - Tasks that span multiple Zoom products
- **Generic references** - Authentication, app types, scopes
- **Shared documentation** - SDK maintenance, troubleshooting, marketplace publishing

Use `zoom-general` when:
- You're starting a new Zoom integration and need to choose the right approach
- Your use case involves multiple Zoom products
- You need general platform documentation (auth, scopes, etc.)

## Quick Reference

| I want to... | Use this skill |
|--------------|----------------|
| Make API calls (create meetings, manage users) | **zoom-rest-api** |
| Receive event notifications (HTTP push) | **zoom-webhooks** |
| Receive event notifications (WebSocket) | **zoom-websockets** |
| Embed Zoom meetings in my app | **zoom-meeting-sdk** |
| Build custom video experiences | **zoom-video-sdk** |
| Build an app inside Zoom client | **zoom-apps-sdk** |
| Access live audio/video/transcripts | **zoom-rtms** |
| Build Team Chat integrations | **zoom-team-chat** |
| Use pre-built video UI components | **zoom-ui-toolkit** |
| Enable co-browsing for support | **zoom-cobrowse-sdk** |
| General/cross-product guidance | **zoom-general** |

## Resources

- **Official docs**: https://developers.zoom.us/
- **Marketplace**: https://marketplace.zoom.us/
- **Developer forum**: https://devforum.zoom.us/

---
name: zoom-skills
description: |
  Zoom Developer Platform skills organized by product. Each folder contains product-specific 
  documentation and use cases. The general folder contains generic, cross-product skills 
  and references.
---

# Zoom Developer Platform Skills

This repository contains skills for building with Zoom APIs and SDKs, focused on web development.

## Folder Structure

| Folder | Description |
|--------|-------------|
| **[zoom-general](zoom-general/SKILL.md)** | **Hub** - Cross-product use cases and shared references |
| **[zoom-rest-api](zoom-rest-api/SKILL.md)** | REST API calls (600+ endpoints) |
| **[zoom-webhooks](zoom-webhooks/SKILL.md)** | Real-time event notifications (HTTP) |
| **[zoom-websockets](zoom-websockets/SKILL.md)** | Real-time event notifications (WebSocket) |
| **[zoom-meeting-sdk](zoom-meeting-sdk/SKILL.md)** | Embed Zoom meetings in your app (Web, React Native, Electron, Linux) |
| **[zoom-video-sdk](zoom-video-sdk/SKILL.md)** | Custom video experiences (Web, React Native, Flutter, Linux) |
| **[zoom-apps-sdk](zoom-apps-sdk/SKILL.md)** | Apps that run inside the Zoom client |
| **[zoom-rtms](zoom-rtms/SKILL.md)** | Real-Time Media Streams (live audio/video/transcripts) |
| **[zoom-team-chat](zoom-team-chat/skill.md)** | Team Chat messaging and channels |
| **[zoom-ui-toolkit](zoom-ui-toolkit/SKILL.md)** | Pre-built React components for Video SDK |
| **[zoom-cobrowse-sdk](zoom-cobrowse-sdk/SKILL.md)** | Collaborative browsing for support |
| **[zoom-oauth](zoom-oauth/SKILL.md)** | OAuth authentication flows (all 4 grant types) |

## How to Use

1. **Product-specific task?** → Go to that product's folder (e.g., `zoom-meeting-sdk/`)
2. **Cross-product or general task?** → Check [zoom-general](zoom-general/SKILL.md) for generic use cases
3. **Each folder has a `SKILL.md`** → Start there for that product's overview

## general (Hub)

The `general` folder contains:

- **Cross-product use cases** - Tasks that span multiple Zoom products
- **Generic references** - Authentication, app types, scopes
- **Shared documentation** - SDK maintenance, troubleshooting, marketplace publishing

Use `general` when:
- You're starting a new Zoom integration and need to choose the right approach
- Your use case involves multiple Zoom products
- You need general platform documentation (auth, scopes, etc.)

## Quick Reference

| I want to... | Use this skill |
|--------------|----------------|
| Make API calls (create meetings, manage users) | **zoom-rest-api** |
| Receive event notifications (HTTP push) | **webhooks** |
| Receive event notifications (WebSocket) | **zoom-websockets** |
| Embed Zoom meetings in my app | **zoom-meeting-sdk** |
| Build custom video experiences | **zoom-video-sdk** |
| Build an app inside Zoom client | **zoom-apps-sdk** |
| Access live audio/video/transcripts | **rtms** |
| Build Team Chat integrations | **zoom-team-chat** |
| Use pre-built video UI components | **zoom-ui-toolkit** |
| Enable co-browsing for support | **zoom-cobrowse-sdk** |
| Implement OAuth authentication | **oauth** |
| General/cross-product guidance | **general** |

## Resources

- **Official docs**: https://developers.zoom.us/
- **Marketplace**: https://marketplace.zoom.us/
- **Developer forum**: https://devforum.zoom.us/

---
name: agent-skills
description: |
  Zoom Developer Platform skills organized by product. Each folder contains product-specific 
  documentation and use cases. The zoom-general folder contains generic, cross-product skills 
  and references.
---

# Zoom Developer Platform Agent Skills

This repository contains skills for building with Zoom APIs and SDKs, organized by product.

## Folder Structure

| Folder | Description |
|--------|-------------|
| **zoom-apps-sdk** | Skills for building apps that run inside the Zoom client |
| **zoom-cobrowse-sdk** | Skills for collaborative browsing/co-browsing support |
| **zoom-contact-center** | Skills for contact center integrations |
| **zoom-general** | **Generic skills** - cross-product use cases and shared references |
| **zoom-meeting-sdk** | Skills for embedding Zoom meetings in your app |
| **zoom-phone** | Skills for cloud phone/VoIP integrations |
| **zoom-rest-api** | Skills for Zoom REST API calls |
| **zoom-rtms** | Skills for Real-Time Media Streams (live audio/video/transcripts) |
| **zoom-video-sdk** | Skills for custom video experiences (not Zoom meetings) |
| **zoom-webhooks** | Skills for real-time event notifications |

## How to Use

1. **Product-specific task?** → Go to that product's folder (e.g., `zoom-meeting-sdk/`)
2. **Cross-product or general task?** → Check `zoom-general/` for generic use cases
3. **Each folder has a `SKILL.md`** → Start there for that product's overview

## zoom-general (Generic Skills)

The `zoom-general` folder is different from other folders. It contains:

- **Cross-product use cases** - Tasks that span multiple Zoom products
- **Generic references** - Authentication, app types, scopes, error codes
- **Shared documentation** - SDK maintenance, troubleshooting, marketplace publishing

Use `zoom-general` when:
- You're starting a new Zoom integration and need to choose the right approach
- Your use case involves multiple Zoom products
- You need general platform documentation (auth, scopes, etc.)

## Quick Reference

| I want to... | Use this skill |
|--------------|----------------|
| Make API calls (create meetings, manage users) | **zoom-rest-api** |
| Receive real-time event notifications | **zoom-webhooks** |
| Embed Zoom meetings in my app | **zoom-meeting-sdk** |
| Build custom video experiences | **zoom-video-sdk** |
| Build an app inside Zoom client | **zoom-apps-sdk** |
| Access live audio/video/transcripts | **zoom-rtms** |
| Build phone/VoIP integrations | **zoom-phone** |
| Enable co-browsing for support | **zoom-cobrowse-sdk** |
| Build contact center integrations | **zoom-contact-center** |
| General/cross-product guidance | **zoom-general** |

## Resources

- **Official docs**: https://developers.zoom.us/
- **Marketplace**: https://marketplace.zoom.us/
- **Developer forum**: https://devforum.zoom.us/

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

### Core SDKs & APIs

| Folder | Description |
|--------|-------------|
| **zoom-rest-api** | Skills for Zoom REST API calls (600+ endpoints) |
| **zoom-webhooks** | Skills for real-time event notifications |
| **zoom-meeting-sdk** | Skills for embedding Zoom meetings in your app |
| **zoom-video-sdk** | Skills for custom video experiences (not Zoom meetings) |
| **zoom-apps-sdk** | Skills for building apps that run inside the Zoom client |
| **zoom-rtms** | Skills for Real-Time Media Streams (live audio/video/transcripts) |

### Zoom Products

| Folder | Description |
|--------|-------------|
| **zoom-phone** | Skills for cloud phone/VoIP integrations |
| **zoom-team-chat** | Skills for Team Chat messaging and channels |
| **zoom-rooms** | Skills for Zoom Rooms device and scheduling management |
| **zoom-calendar** | Skills for Zoom Calendar integrations |
| **zoom-mail** | Skills for Zoom Mail integrations |
| **zoom-whiteboard** | Skills for collaborative whiteboard management |
| **zoom-docs** | Skills for document collaboration |
| **zoom-events** | Skills for Zoom Events and webinar management |
| **zoom-contact-center** | Skills for contact center integrations |
| **zoom-virtual-agent** | Skills for AI-powered virtual agent/chatbot |
| **zoom-crc** | Skills for Cloud Room Connector (H.323/SIP) |

### Developer Tools

| Folder | Description |
|--------|-------------|
| **zoom-rivet** | CLI toolkit for Zoom App development |
| **zoom-chatbot-studio** | No-code chatbot builder for Team Chat |
| **zoom-ui-toolkit** | Pre-built React components for Video SDK |
| **zoom-probe-sdk** | Monitoring and debugging toolkit for Zoom Apps |
| **zoom-commerce** | App monetization and entitlement management |
| **zoom-cobrowse-sdk** | Skills for collaborative browsing/co-browsing support |

### General

| Folder | Description |
|--------|-------------|
| **zoom-general** | **Generic skills** - cross-product use cases and shared references |

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
| Build Team Chat integrations | **zoom-team-chat** |
| Manage Zoom Rooms | **zoom-rooms** |
| Work with calendars | **zoom-calendar** |
| Work with email | **zoom-mail** |
| Manage whiteboards | **zoom-whiteboard** |
| Manage documents | **zoom-docs** |
| Manage events/webinars | **zoom-events** |
| Build contact center solutions | **zoom-contact-center** |
| Build AI chatbots | **zoom-virtual-agent** |
| Connect H.323/SIP rooms | **zoom-crc** |
| Scaffold Zoom Apps quickly | **zoom-rivet** |
| Build no-code chatbots | **zoom-chatbot-studio** |
| Use pre-built video UI components | **zoom-ui-toolkit** |
| Monitor/debug Zoom Apps | **zoom-probe-sdk** |
| Monetize your Zoom App | **zoom-commerce** |
| Enable co-browsing for support | **zoom-cobrowse-sdk** |
| General/cross-product guidance | **zoom-general** |

## Resources

- **Official docs**: https://developers.zoom.us/
- **Marketplace**: https://marketplace.zoom.us/
- **Developer forum**: https://devforum.zoom.us/

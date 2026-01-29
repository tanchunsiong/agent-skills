---
name: zoom-general
description: |
  Generic Zoom Developer Platform guide. Covers cross-product use cases, authentication (OAuth 2.0, 
  Server-to-Server OAuth, JWT), app types, OAuth scopes, and Marketplace setup. Use when starting 
  any Zoom integration, when working on cross-product tasks, or when user needs help choosing 
  between Zoom SDKs and APIs.
---

# Zoom General (Cross-Product Skills)

Entry point for building with Zoom. This skill helps you choose the right SDK or API and provides cross-product guidance.

## Choose Your Path

| I want to... | Use this skill |
|--------------|----------------|
| Make API calls (create meetings, manage users) | **zoom-rest-api** |
| Receive real-time event notifications | **zoom-webhooks** |
| Embed Zoom meetings in my app | **zoom-meeting-sdk** |
| Build custom video experiences (not Zoom meetings) | **zoom-video-sdk** |
| Build an app that runs inside Zoom client | **zoom-apps-sdk** |
| Access live audio/video/transcripts from meetings | **zoom-rtms** |
| Build cloud phone/VoIP integrations | **zoom-phone** |
| Enable collaborative browsing for support | **zoom-cobrowse-sdk** |
| Build contact center integrations | **zoom-contact-center** |

## Common Use Cases

| Use Case | Description | Skills Needed |
|----------|-------------|---------------|
| [Meeting Automation](use-cases/meeting-automation.md) | Schedule, update, delete meetings programmatically | zoom-rest-api |
| [Meeting Bots](use-cases/meeting-bots.md) | Build bots that join meetings for AI/transcription | zoom-meeting-sdk (Linux) + zoom-rtms |
| [Recording & Transcription](use-cases/recording-transcription.md) | Download recordings, get transcripts | zoom-webhooks + zoom-rest-api |
| [BYOS Recording Storage](use-cases/byos-recording-storage.md) | Auto-download recordings to your own storage (S3, GCS, etc.) | zoom-webhooks + zoom-rest-api |
| [Real-Time Media Streams](use-cases/real-time-media-streams.md) | Access live audio, video, transcripts via WebSocket | zoom-rtms + zoom-webhooks |

## Prerequisites

1. Zoom account (Pro, Business, or Enterprise)
2. App created in [Zoom App Marketplace](https://marketplace.zoom.us/)
3. OAuth credentials (Client ID and Secret)

## Quick Start

1. Go to [marketplace.zoom.us](https://marketplace.zoom.us/)
2. Click **Develop** → **Build App**
3. Select app type (see [references/app-types.md](references/app-types.md))
4. Configure OAuth and scopes
5. Copy credentials to your application

## Detailed References

- **[references/authentication.md](references/authentication.md)** - OAuth 2.0, S2S OAuth, JWT patterns
- **[references/app-types.md](references/app-types.md)** - Decision guide for app types
- **[references/scopes.md](references/scopes.md)** - OAuth scopes reference
- **[references/marketplace.md](references/marketplace.md)** - Marketplace portal navigation
- **[references/error-codes.md](references/error-codes.md)** - Common error codes across SDKs

## SDK Maintenance

- **[references/sdk-upgrade-guide.md](references/sdk-upgrade-guide.md)** - Version policy, upgrade steps
- **[references/sdk-logs-troubleshooting.md](references/sdk-logs-troubleshooting.md)** - Collecting SDK logs

## Resources

- **Official docs**: https://developers.zoom.us/
- **Marketplace**: https://marketplace.zoom.us/
- **Developer forum**: https://devforum.zoom.us/

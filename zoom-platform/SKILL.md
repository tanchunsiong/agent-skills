---
name: zoom-platform
description: |
  Core Zoom Developer Platform guide. Covers authentication (OAuth 2.0, Server-to-Server OAuth, JWT), 
  app types, OAuth scopes, and Marketplace setup. Use when starting any Zoom integration or when 
  user needs help choosing between Zoom SDKs and APIs.
---

# Zoom Developer Platform

Entry point for building with Zoom. This skill helps you choose the right SDK or API and set up authentication.

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
| [Raw Recording](use-cases/raw-recording.md) | Access raw audio/video data for custom processing | zoom-meeting-sdk / zoom-video-sdk (Desktop) |
| [Real-Time Media Streams](use-cases/real-time-media-streams.md) | Access live audio, video, transcripts via WebSocket | zoom-rtms + zoom-webhooks |
| [QSS Monitoring](use-cases/qss-monitoring.md) | Real-time quality of service monitoring for IT | zoom-webhooks + zoom-rest-api |
| [Usage Reporting & Analytics](use-cases/usage-reporting-analytics.md) | Meeting counts, minutes used, user stats, billing reports | zoom-rest-api |
| [HD Video Resolution](use-cases/hd-video-resolution.md) | Achieve 720p/1080p video quality, SAB requirements | zoom-meeting-sdk (Web) / zoom-video-sdk (Web) |
| [Web SDK Embedding](use-cases/web-sdk-embedding.md) | Embed SDK in iframe, cross-origin setup, CORS/headers | zoom-meeting-sdk (Web) / zoom-video-sdk (Web) |
| [Embed Meetings](use-cases/embed-meetings.md) | Embed Zoom meetings in your web/mobile app | zoom-meeting-sdk |
| [Custom Video](use-cases/custom-video.md) | Build branded video experiences | zoom-video-sdk |
| [AI Integration](use-cases/ai-integration.md) | Real-time AI features (sentiment, summarization) | zoom-rtms |
| [In-Meeting Apps](use-cases/in-meeting-apps.md) | Apps that run inside Zoom (polls, tools) | zoom-apps-sdk |
| [Contact Center](use-cases/contact-center-integration.md) | Customer support video/chat | zoom-contact-center |
| [AI Companion Integration](use-cases/ai-companion-integration.md) | Meeting summaries, transcripts, AI features | zoom-rest-api + zoom-meeting-sdk |
| [SDK Size Optimization](use-cases/sdk-size-optimization.md) | Reduce mobile SDK binary size (iOS/Android) | zoom-meeting-sdk / zoom-video-sdk |

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
- **[references/rivet.md](references/rivet.md)** - Rivet API library for server-side development
- **[references/community-repos.md](references/community-repos.md)** - Sample repositories catalog (official + community)

## SDK Maintenance

- **[references/sdk-upgrade-guide.md](references/sdk-upgrade-guide.md)** - Version policy, upgrade steps, breaking changes
- **[references/sdk-logs-troubleshooting.md](references/sdk-logs-troubleshooting.md)** - Collecting SDK logs for debugging
- **[references/known-limitations.md](references/known-limitations.md)** - Common gotchas and quirks

## Resources

- **Official docs**: https://developers.zoom.us/
- **Marketplace**: https://marketplace.zoom.us/
- **Developer forum**: https://devforum.zoom.us/

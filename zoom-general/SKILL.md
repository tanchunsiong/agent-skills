---
name: zoom-general
description: |
  Generic Zoom Developer Platform guide. Covers cross-product use cases, authentication (OAuth 2.0, 
  Server-to-Server OAuth, JWT), app types, OAuth scopes, and Marketplace setup. Use when starting 
  any Zoom integration, when working on cross-product tasks, or when user needs help choosing 
  between Zoom SDKs and APIs.
triggers:
  - "zoom integration"
  - "getting started"
  - "which zoom sdk"
  - "zoom platform"
  - "choose zoom api"
  - "zoom authentication"
  - "oauth zoom"
  - "zoom scopes"
  - "marketplace"
  - "cross-product"
---

# Zoom General (Cross-Product Skills)

Entry point for building with Zoom. This skill helps you choose the right SDK or API and provides cross-product guidance.

## Choose Your Path

| I want to... | Use this skill |
|--------------|----------------|
| Make API calls (create meetings, manage users) | **zoom-rest-api** |
| Receive event notifications (HTTP push) | **webhooks** |
| Receive event notifications (WebSocket, low-latency) | **zoom-websockets** |
| Embed Zoom meetings in my app | **zoom-meeting-sdk** |
| Build custom video experiences (Web, React Native, Flutter, or Linux headless) | **zoom-video-sdk** |
| Build an app that runs inside Zoom client | **zoom-apps-sdk** |
| Access live audio/video/transcripts from meetings | **rtms** |
| Enable collaborative browsing for support | **zoom-cobrowse-sdk** |
| Build Team Chat apps and integrations | **[zoom-team-chat](../zoom-team-chat/skill.md)** |
| Add pre-built UI components for Video SDK | **[zoom-ui-toolkit](../zoom-ui-toolkit/SKILL.md)** |
| Implement OAuth authentication (all grant types) | **oauth** |

### Webhooks vs WebSockets

Both receive event notifications, but differ in approach:

| Aspect | webhooks | zoom-websockets |
|--------|---------------|-----------------|
| Connection | HTTP POST to your endpoint | Persistent WebSocket |
| Latency | Higher | Lower |
| Security | Requires public endpoint | No exposed endpoint |
| Setup | Simpler | More complex |
| Best for | Most use cases | Real-time, security-sensitive |

## Common Use Cases

| Use Case | Description | Skills Needed |
|----------|-------------|---------------|
| [Meeting Automation](use-cases/meeting-automation.md) | Schedule, update, delete meetings programmatically | zoom-rest-api |
| [Meeting Bots](use-cases/meeting-bots.md) | Build bots that join meetings for AI/transcription | zoom-meeting-sdk (Linux) + rtms |
| [Recording & Transcription](use-cases/recording-transcription.md) | Download recordings, get transcripts | webhooks + zoom-rest-api |
| [Recording Download Pipeline](use-cases/recording-download-pipeline.md) | Auto-download recordings to your own storage (S3, GCS, etc.) | webhooks + zoom-rest-api |
| [Real-Time Media Streams](use-cases/real-time-media-streams.md) | Access live audio, video, transcripts via WebSocket | rtms + webhooks |
| [In-Meeting Apps](use-cases/in-meeting-apps.md) | Build apps that run inside Zoom meetings | zoom-apps-sdk + oauth |
| [React Native Meeting Embed](use-cases/react-native-meeting-embed.md) | Embed meetings into iOS/Android React Native apps | zoom-meeting-sdk/react-native + oauth |
| [Electron Meeting Embed](use-cases/electron-meeting-embed.md) | Embed meetings into desktop Electron apps | zoom-meeting-sdk/electron + oauth |
| [Flutter Video Sessions](use-cases/flutter-video-sessions.md) | Build custom mobile video sessions in Flutter | zoom-video-sdk/flutter + oauth |
| [React Native Video Sessions](use-cases/react-native-video-sessions.md) | Build custom mobile video sessions in React Native | zoom-video-sdk/react-native + oauth |
| [Immersive Experiences](use-cases/immersive-experiences.md) | Custom video layouts with Layers API | zoom-apps-sdk |
| [Collaborative Apps](use-cases/collaborative-apps.md) | Real-time shared state in meetings | zoom-apps-sdk |

## Complete Use-Case Index

- [ai-companion-integration.md](use-cases/ai-companion-integration.md)
- [ai-integration.md](use-cases/ai-integration.md)
- [backend-automation-s2s-oauth.md](use-cases/backend-automation-s2s-oauth.md)
- [collaborative-apps.md](use-cases/collaborative-apps.md)
- [contact-center-integration.md](use-cases/contact-center-integration.md)
- [custom-video.md](use-cases/custom-video.md)
- [customer-support-cobrowsing.md](use-cases/customer-support-cobrowsing.md)
- [embed-meetings.md](use-cases/embed-meetings.md)
- [form-completion-assistant.md](use-cases/form-completion-assistant.md)
- [hd-video-resolution.md](use-cases/hd-video-resolution.md)
- [immersive-experiences.md](use-cases/immersive-experiences.md)
- [in-meeting-apps.md](use-cases/in-meeting-apps.md)
- [marketplace-publishing.md](use-cases/marketplace-publishing.md)
- [meeting-automation.md](use-cases/meeting-automation.md)
- [meeting-bots.md](use-cases/meeting-bots.md)
- [meeting-details-with-events.md](use-cases/meeting-details-with-events.md)
- [minutes-calculation.md](use-cases/minutes-calculation.md)
- [prebuilt-video-ui.md](use-cases/prebuilt-video-ui.md)
- [qss-monitoring.md](use-cases/qss-monitoring.md)
- [raw-recording.md](use-cases/raw-recording.md)
- [electron-meeting-embed.md](use-cases/electron-meeting-embed.md)
- [flutter-video-sessions.md](use-cases/flutter-video-sessions.md)
- [react-native-meeting-embed.md](use-cases/react-native-meeting-embed.md)
- [react-native-video-sessions.md](use-cases/react-native-video-sessions.md)
- [real-time-media-streams.md](use-cases/real-time-media-streams.md)
- [recording-download-pipeline.md](use-cases/recording-download-pipeline.md)
- [recording-transcription.md](use-cases/recording-transcription.md)
- [retrieve-meeting-and-subscribe-events.md](use-cases/retrieve-meeting-and-subscribe-events.md)
- [saas-app-oauth-integration.md](use-cases/saas-app-oauth-integration.md)
- [sdk-size-optimization.md](use-cases/sdk-size-optimization.md)
- [sdk-wrappers-gui.md](use-cases/sdk-wrappers-gui.md)
- [team-chat-llm-bot.md](use-cases/team-chat-llm-bot.md)
- [testing-development.md](use-cases/testing-development.md)
- [transcription-bot-linux.md](use-cases/transcription-bot-linux.md)
- [usage-reporting-analytics.md](use-cases/usage-reporting-analytics.md)
- [user-and-meeting-creation.md](use-cases/user-and-meeting-creation.md)
- [web-sdk-embedding.md](use-cases/web-sdk-embedding.md)

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

## SDK Maintenance

- **[references/sdk-upgrade-guide.md](references/sdk-upgrade-guide.md)** - Version policy, upgrade steps
- **[references/sdk-logs-troubleshooting.md](references/sdk-logs-troubleshooting.md)** - Collecting SDK logs

## Skill Chaining

Many Zoom integrations require combining multiple skills. Common patterns:

| Chain | Skills | Use Case | Guide |
|-------|--------|----------|-------|
| Meeting + Events | zoom-rest-api → webhooks | Create meeting, track lifecycle events | [meeting-details-with-events.md](use-cases/meeting-details-with-events.md) |
| User + Meeting | zoom-rest-api (users) → zoom-rest-api (meetings) | Provision user, schedule onboarding meetings | [user-and-meeting-creation.md](use-cases/user-and-meeting-creation.md) |
| Meeting + Real-Time | zoom-rest-api → rtms | Create meeting, join with bot for transcription | [meeting-bots.md](use-cases/meeting-bots.md) |
| Recording + Storage | webhooks → zoom-rest-api | Receive completion event, download recording | [recording-download-pipeline.md](use-cases/recording-download-pipeline.md) |

### How Skill Chaining Works

1. **Identify the workflow** - What sequence of actions is needed?
2. **Map to skills** - Which Zoom skills handle each step?
3. **Handle authorization** - Ensure scopes cover all operations (see [authorization-patterns.md](references/authorization-patterns.md))
4. **Connect the chain** - Pass IDs/data between steps

### Example: User Onboarding Chain

```
zoom-rest-api (users)     →     zoom-rest-api (meetings)     →     webhooks
      │                               │                              │
   Create user              Schedule onboarding meeting      Subscribe to events
   Returns: user_id         Uses: user_id                    Track: meeting.started
```

For detailed patterns and code examples, see the use-case guides linked above.

## Resources

- **Official docs**: https://developers.zoom.us/
- **Marketplace**: https://marketplace.zoom.us/
- **Developer forum**: https://devforum.zoom.us/

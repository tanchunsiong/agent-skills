# Zoom Developer Platform Skills

Official Agent Skills for the Zoom Developer Platform - SDKs, APIs, and integrations.

## Overview

This repository contains hub-and-spoke skills for Claude Code, OpenCode, and other agents supporting the Agent Skills standard. These skills provide comprehensive guidance for building with Zoom's developer tools.

**Total Skills: 8**

| # | Skill | Type | Description |
|---|-------|------|-------------|
| 1 | **zoom-platform** | Hub | Core concepts, authentication, app types, scopes, Marketplace setup |
| 2 | **zoom-rest-api** | Spoke | 600+ REST API endpoints for meetings, users, webinars, recordings |
| 3 | **zoom-webhooks** | Spoke | Real-time event notifications and webhook verification |
| 4 | **zoom-meeting-sdk** | Spoke | Embed Zoom meetings (Web, iOS, Android, macOS, Windows, Linux, Electron, React Native, Unreal Engine) |
| 5 | **zoom-video-sdk** | Spoke | Custom video experiences (Web, iOS, Android, macOS, Windows, Linux, Flutter, React Native, Unity) |
| 6 | **zoom-apps-sdk** | Spoke | Apps that run inside Zoom client, Layers API |
| 7 | **zoom-rtms** | Spoke | Realtime Media Streams - live audio, video, transcripts |
| 8 | **zoom-contact-center** | Spoke | Contact Center SDKs and APIs |

---

## Folder Structure

```
zoom-developer-platform/
├── .claude-plugin/
│   └── manifest.json
├── README.md
├── LICENSE
├── PLAN.md
│
├── zoom-platform/                    # Hub: Core Platform
│   ├── SKILL.md
│   └── references/
│       ├── authentication.md
│       ├── app-types.md
│       ├── scopes.md
│       ├── marketplace.md
│       ├── sdk-upgrade-guide.md      # Cross-cutting: version policy, upgrade steps
│       ├── sdk-logs-troubleshooting.md # Cross-cutting: collecting logs
│       └── use-cases/
│           ├── meeting-automation.md
│           ├── meeting-bots.md
│           ├── recording-transcription.md
│           ├── byos-recording-storage.md
│           ├── real-time-media-streams.md
│           ├── usage-reporting-analytics.md
│           ├── embed-meetings.md
│           ├── custom-video.md
│           ├── ai-integration.md
│           ├── in-meeting-apps.md
│           └── contact-center-integration.md
│
├── zoom-rest-api/                    # Spoke: REST API
│   ├── SKILL.md
│   └── references/
│       ├── meetings.md
│       ├── users.md
│       ├── webinars.md
│       ├── recordings.md
│       └── reports.md
│
├── zoom-webhooks/                    # Spoke: Webhooks
│   ├── SKILL.md
│   └── references/
│       ├── events.md
│       ├── verification.md
│       └── subscriptions.md
│
├── zoom-meeting-sdk/                 # Spoke: Meeting SDK
│   ├── SKILL.md
│   └── references/
│       ├── authorization.md
│       ├── web.md
│       ├── ios.md
│       ├── android.md
│       ├── macos.md
│       ├── windows.md
│       ├── linux.md
│       ├── electron.md               # Cross-platform
│       ├── react-native.md           # Cross-platform
│       ├── unreal-engine.md          # Game engine
│       ├── troubleshooting.md        # SDK-specific troubleshooting
│       └── web-tracking-id.md        # Web SDK tracking ID
│
├── zoom-video-sdk/                   # Spoke: Video SDK
│   ├── SKILL.md
│   └── references/
│       ├── authorization.md
│       ├── web.md
│       ├── ios.md
│       ├── android.md
│       ├── macos.md
│       ├── windows.md
│       ├── linux.md
│       ├── flutter.md                # Cross-platform
│       ├── react-native.md           # Cross-platform
│       ├── unity.md                  # Game engine
│       └── troubleshooting.md        # SDK-specific troubleshooting
│
├── zoom-apps-sdk/                    # Spoke: Zoom Apps
│   ├── SKILL.md
│   └── references/
│       ├── apis.md
│       ├── events.md
│       ├── layers-api.md
│       └── oauth.md
│
├── zoom-rtms/                        # Spoke: Realtime Media Streams
│   ├── SKILL.md
│   └── references/
│       ├── quickstart.md
│       ├── webhooks.md
│       ├── media-types.md
│       └── connection.md
│
└── zoom-contact-center/              # Spoke: Contact Center
    ├── SKILL.md
    └── references/
        ├── sdk-web.md
        ├── sdk-ios.md
        ├── sdk-android.md
        └── apis.md
```

---

## Design Decisions

### 1. Structure: SDK-First with Use Cases (Option A + Use Cases)

We follow Cloudflare's pattern - organize by SDK/product, not by scenario. Use cases are added as entry points in the hub skill to help developers find the right SDK.

### 2. Use Cases vs Platforms

| Type | Location | Examples |
|------|----------|----------|
| **Use Cases** (cross-cutting scenarios) | `zoom-platform/references/use-cases/` | Meeting bots, BYOS storage, AI integration |
| **Platforms** (SDK-specific) | Each SDK's `references/` folder | iOS, Android, Unity, Flutter, Electron |

**Rule:** Gaming/VR/Flutter/React Native are **platforms**, not use cases.

### 3. Cross-cutting vs SDK-specific References

| Type | Location | Examples |
|------|----------|----------|
| **Cross-cutting** (applies to all SDKs) | `zoom-platform/references/` | `sdk-upgrade-guide.md`, `sdk-logs-troubleshooting.md` |
| **SDK-specific** | Each SDK's `references/` folder | `troubleshooting.md`, `web-tracking-id.md` |

### 4. Event Handling / Callbacks / Delegates

Platform-specific patterns (callbacks, delegates, listeners) are **included in each platform file**, not as separate files.

Each platform reference (`web.md`, `ios.md`, `android.md`, etc.) should include:

- Singleton/instance initialization
- Event subscription / delegate / listener patterns
- User join/leave handling
- Audio/video rendering
- Resource cleanup

| Platform | Pattern | Terminology |
|----------|---------|-------------|
| Web/JavaScript | Callbacks | Events / Event Listeners |
| iOS (Swift/Obj-C) | Delegate Pattern | Delegates |
| Android (Kotlin/Java) | Interface Pattern | Listeners |
| Desktop (C++) | Callback Pattern | Callbacks / Handlers |

---

## Common Use Cases (11)

| Use Case | Description | Skills Needed |
|----------|-------------|---------------|
| Meeting Automation | Schedule, update, delete meetings programmatically | zoom-rest-api |
| Meeting Bots | Build bots that join meetings for AI/transcription | zoom-meeting-sdk (Linux) + zoom-rtms |
| Recording & Transcription | Download recordings, get transcripts | zoom-webhooks + zoom-rest-api |
| BYOS Recording Storage | Auto-download recordings to your own storage (S3, GCS, etc.) | zoom-webhooks + zoom-rest-api |
| Real-Time Media Streams | Access live audio, video, transcripts via WebSocket | zoom-rtms + zoom-webhooks |
| Usage Reporting & Analytics | Meeting counts, minutes used, user stats, billing reports | zoom-rest-api |
| Embed Meetings | Embed Zoom meetings in your web/mobile app | zoom-meeting-sdk |
| Custom Video | Build branded video experiences | zoom-video-sdk |
| AI Integration | Real-time AI features (sentiment, summarization) | zoom-rtms |
| In-Meeting Apps | Apps that run inside Zoom (polls, tools) | zoom-apps-sdk |
| Contact Center | Customer support video/chat | zoom-contact-center |

---

## Platform Coverage

### Meeting SDK Platforms (10)

| Platform | Type | File |
|----------|------|------|
| Web | Native | `web.md` |
| iOS | Native | `ios.md` |
| Android | Native | `android.md` |
| macOS | Native | `macos.md` |
| Windows | Native | `windows.md` |
| Linux | Native | `linux.md` |
| Electron | Cross-platform | `electron.md` |
| React Native | Cross-platform | `react-native.md` |
| Unreal Engine | Game Engine | `unreal-engine.md` |

### Video SDK Platforms (10)

| Platform | Type | File |
|----------|------|------|
| Web | Native | `web.md` |
| iOS | Native | `ios.md` |
| Android | Native | `android.md` |
| macOS | Native | `macos.md` |
| Windows | Native | `windows.md` |
| Linux | Native | `linux.md` |
| Flutter | Cross-platform | `flutter.md` |
| React Native | Cross-platform | `react-native.md` |
| Unity | Game Engine | `unity.md` |

---

## Platform Reference Template

Each platform file (`web.md`, `ios.md`, `android.md`, etc.) should include these sections:

```markdown
# [SDK Name] - [Platform]

## Overview

Brief description.

## Prerequisites

- Requirements
- Minimum versions

## Installation

How to add the SDK to your project.

## Quick Start

Minimal code to get started.

## Initialization

### Singleton Instance

How to get/create the SDK instance.

## Event Handling

### Subscribe to Events (Web) / Implement Delegates (iOS) / Add Listeners (Android)

Platform-specific event handling patterns.

### User Join/Leave

Handle participant events.

### Audio/Video Rendering

Render participant streams.

### Resource Cleanup

Release resources when done.

## Common Tasks

### Join a Meeting/Session
### Leave a Meeting/Session
### Mute/Unmute Audio
### Start/Stop Video
### Screen Sharing

## Troubleshooting

Common issues and solutions.

## Resources

- Official docs link
- Sample app link
```

---

## SKILL.md Template

```markdown
---
name: skill-name-here
description: |
  Brief description of what this skill does (1-3 sentences).
  Include trigger phrases: Use when user mentions "X", "Y", or "Z".
---

# Skill Title

Brief introduction (1-2 sentences).

## Prerequisites

- Requirement 1
- Requirement 2

## Quick Start

Minimal working example:

\`\`\`language
// Code example here
\`\`\`

## Key Concepts

| Concept | Description |
|---------|-------------|
| Term 1 | Explanation |
| Term 2 | Explanation |

## Quick Reference

| Task | Code/Command |
|------|--------------|
| Do X | `command` |
| Do Y | `command` |

## Common Patterns

### Pattern 1: Name

\`\`\`language
// Code example
\`\`\`

## Detailed References

- **[references/topic1.md](references/topic1.md)** - Description
- **[references/topic2.md](references/topic2.md)** - Description

## Resources

- **Official docs**: https://developers.zoom.us/docs/...
- **Sample app**: https://github.com/zoom/...
- **Developer forum**: https://devforum.zoom.us/

## Common Issues

| Issue | Solution |
|-------|----------|
| Problem 1 | Fix 1 |
| Problem 2 | Fix 2 |

## Best Practices

1. Practice 1
2. Practice 2
3. Practice 3
```

---

## Resources

- [Zoom Developer Platform](https://developers.zoom.us/)
- [Zoom App Marketplace](https://marketplace.zoom.us/)
- [Zoom Developer Forum](https://devforum.zoom.us/)
- [Zoom GitHub](https://github.com/zoom)
- [Agent Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)

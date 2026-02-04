# Agent Skills - Architecture

This document describes the structure and design of the Zoom agent skills repository.

## Overview

Skills for building with Zoom SDKs, APIs, and integrations. Focused on web development.

## Hub-and-Spoke Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              AGENT REQUEST                                   │
│                    "How do I build a meeting bot?"                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           zoom-general (HUB)                                │
│                                                                              │
│  Entry point for all Zoom development questions.                            │
│  Routes to the appropriate spoke skill based on user intent.                │
│                                                                              │
│  "I want to..."                      → "Use this skill..."                  │
│  ─────────────────────────────────────────────────────────────              │
│  Make API calls                      → zoom-rest-api                        │
│  Receive event notifications (HTTP)  → zoom-webhooks                        │
│  Receive event notifications (WS)    → zoom-websockets                      │
│  Embed Zoom meetings                 → zoom-meeting-sdk                     │
│  Build custom video experiences      → zoom-video-sdk                       │
│  Build in-client Zoom apps           → zoom-apps-sdk                        │
│  Access live media streams           → zoom-rtms                            │
│  Build Team Chat integrations        → zoom-team-chat                       │
│  Enable collaborative browsing       → zoom-cobrowse-sdk                    │
│  Add pre-built UI components         → zoom-ui-toolkit                      │
│  Implement OAuth authentication      → zoom-oauth                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
        ┌─────────────┬───────────────┼───────────────┬─────────────┐
        │             │               │               │             │
        ▼             ▼               ▼               ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│zoom-rest-api│ │zoom-webhooks│ │  zoom-      │ │zoom-meeting │ │zoom-video   │
│             │ │             │ │ websockets  │ │    -sdk     │ │    -sdk     │
│ 600+ API    │ │ Events      │ │ Events      │ │ Embed Zoom  │ │ Custom      │
│ endpoints   │ │ (HTTP push) │ │ (WebSocket) │ │ meetings    │ │ video       │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
        │             │               │               │             │
        ▼             ▼               ▼               ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│zoom-apps-sdk│ │  zoom-rtms  │ │zoom-team    │ │zoom-ui      │ │zoom-cobrowse│
│             │ │             │ │   -chat     │ │   -toolkit  │ │    -sdk     │
│ In-client   │ │ Real-time   │ │ Messaging   │ │ Video UI    │ │ Co-browsing │
│ Zoom apps   │ │ media       │ │ & channels  │ │ components  │ │ support     │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

## Directory Structure

```
agent-skills/
│
├── README.md                    # Installation + Getting Started
├── ARCHITECTURE.md              # This file
│
├── zoom-general/               # HUB - Entry point skill
│   ├── SKILL.md                 # Router: "Choose Your Path"
│   ├── references/              # Cross-cutting documentation
│   │   ├── authentication.md
│   │   ├── app-types.md
│   │   ├── scopes.md
│   │   ├── marketplace.md
│   │   └── ...
│   └── use-cases/               # Cross-cutting scenarios
│       ├── meeting-automation.md
│       ├── meeting-bots.md
│       └── ...
│
├── zoom-rest-api/               # SPOKE - REST API
│   ├── SKILL.md
│   └── references/
│
├── zoom-webhooks/               # SPOKE - Webhooks (HTTP push)
│   ├── SKILL.md
│   └── references/
│
├── zoom-websockets/             # SPOKE - WebSockets (persistent connection)
│   ├── SKILL.md
│   └── references/
│
├── zoom-meeting-sdk/            # SPOKE - Meeting SDK (Web)
│   ├── SKILL.md
│   └── references/
│
├── zoom-video-sdk/              # SPOKE - Video SDK (Web)
│   ├── SKILL.md
│   └── references/
│
├── zoom-apps-sdk/               # SPOKE - Apps SDK
│   ├── SKILL.md
│   └── references/
│
├── zoom-rtms/                   # SPOKE - Real-Time Media Streams
│   ├── SKILL.md
│   └── references/
│
├── zoom-team-chat/              # SPOKE - Team Chat
│   ├── SKILL.md
│   └── references/
│
├── zoom-ui-toolkit/             # SPOKE - UI Toolkit
│   ├── SKILL.md
│   └── references/
│
├── zoom-cobrowse-sdk/           # SPOKE - Cobrowse SDK
│   ├── SKILL.md
│   └── references/
│
└── zoom-oauth/                  # SPOKE - OAuth Authentication
    ├── SKILL.md
    ├── references/
    └── learnings.md
```

## Design Principles

### 1. Hub-and-Spoke Routing

The `zoom-general` skill acts as a router. When an agent receives a Zoom-related question, it:
1. Loads `zoom-general/SKILL.md`
2. Reads the "Choose Your Path" table
3. Routes to the appropriate spoke skill by name

### 2. Progressive Disclosure

- **SKILL.md**: Essential information (quick start, key concepts)
- **references/**: Detailed documentation (loaded on-demand)
- **use-cases/**: Cross-cutting scenarios (multi-skill guides)

### 3. Skill Chaining

Skills reference other skills by name in prose. The agent discovers and loads them automatically.

```markdown
For meeting authentication, use the **zoom-meeting-sdk** skill.
```

### 4. Max 3 Levels Deep

```
skill-name/           # Level 1
├── SKILL.md
├── references/       # Level 2
│   └── topic.md      # Level 3 (max)
└── use-cases/        # Level 2
    └── scenario.md   # Level 3 (max)
```

## Skills Summary

| Skill | Purpose | Key Topics |
|-------|---------|------------|
| **zoom-general** | Hub/router | Authentication, app types, use cases |
| **zoom-rest-api** | REST API | 600+ endpoints, rate limits, pagination |
| **zoom-webhooks** | Events (HTTP) | Event types, verification, subscriptions |
| **zoom-websockets** | Events (WebSocket) | Persistent connection, low-latency, S2S OAuth |
| **zoom-meeting-sdk** | Embed meetings (Web) | Component View, Client View, signatures |
| **zoom-video-sdk** | Custom video (Web) | Sessions, raw media, UI customization |
| **zoom-apps-sdk** | In-client apps | APIs, events, layers, OAuth |
| **zoom-rtms** | Live media | Audio, video, transcripts via WebSocket |
| **zoom-team-chat** | Team Chat | Channels, messages, chatbots |
| **zoom-ui-toolkit** | Video UI | Pre-built React components for Video SDK |
| **zoom-cobrowse-sdk** | Co-browsing | Screen sharing, annotation |
| **zoom-oauth** | OAuth | Auth Code, PKCE, Client Credentials, Device Code |

## Use Cases Summary

| Use Case | Skills Needed |
|----------|---------------|
| Meeting Automation | zoom-rest-api |
| Meeting Bots | zoom-meeting-sdk + zoom-rtms |
| Recording & Transcription | zoom-webhooks + zoom-rest-api |
| Real-Time AI Integration | zoom-rtms |
| Team Chat Bots | zoom-team-chat |
| Custom Video Apps | zoom-video-sdk + zoom-ui-toolkit |
| In-Meeting Apps | zoom-apps-sdk |
| Low-Latency Events | zoom-websockets |

## Key Technical Gotchas

| Topic | Gotcha |
|-------|--------|
| JWT | JWT *App Type* deprecated, NOT JWT *Signatures* |
| OBF Token | Required Feb 2026 for external meetings |
| HD Video | Container must be ≥1280×720 for 720p |
| 720p Streams | Max 2 concurrent subscriptions |
| Rate Limits | 100 meeting create/update per user per day |

## Resources

- **Official Docs**: https://developers.zoom.us/
- **Marketplace**: https://marketplace.zoom.us/
- **Developer Forum**: https://devforum.zoom.us/

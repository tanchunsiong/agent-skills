# Zoom Developer Platform Skills - Architecture

This document describes the structure and design of the Zoom Developer Platform agent skills.

## Overview

A collection of **Agent Skills** for building with Zoom SDKs, APIs, and integrations. Follows the [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) open standard for Claude Code, OpenCode, and compatible AI coding agents.

## Hub-and-Spoke Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              AGENT REQUEST                                   │
│                    "How do I build a meeting bot?"                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           zoom-platform (HUB)                                │
│                                                                              │
│  Entry point for all Zoom development questions.                            │
│  Routes to the appropriate spoke skill based on user intent.                │
│                                                                              │
│  "I want to..."                      → "Use this skill..."                  │
│  ─────────────────────────────────────────────────────────────              │
│  Make API calls                      → zoom-rest-api                        │
│  Receive event notifications         → zoom-webhooks                        │
│  Embed Zoom meetings                 → zoom-meeting-sdk                     │
│  Build custom video experiences      → zoom-video-sdk                       │
│  Build in-client Zoom apps           → zoom-apps-sdk                        │
│  Access live media streams           → zoom-rtms                            │
│  Build phone/VoIP integrations       → zoom-phone                           │
│  Enable collaborative browsing       → zoom-cobrowse-sdk                    │
│  Build contact center solutions      → zoom-contact-center                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
        ┌─────────────┬───────────────┼───────────────┬─────────────┐
        │             │               │               │             │
        ▼             ▼               ▼               ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│zoom-rest-api│ │zoom-webhooks│ │zoom-meeting │ │zoom-video   │ │zoom-apps    │
│             │ │             │ │    -sdk     │ │    -sdk     │ │    -sdk     │
│ 600+ API    │ │ Event       │ │ Embed Zoom  │ │ Custom      │ │ In-client   │
│ endpoints   │ │ notifications│ │ meetings    │ │ video       │ │ apps        │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
        │             │               │               │             │
        ▼             ▼               ▼               ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  zoom-rtms  │ │ zoom-phone  │ │zoom-cobrowse│ │zoom-contact │
│             │ │             │ │    -sdk     │ │   -center   │
│ Real-time   │ │ Cloud phone │ │ Co-browsing │ │ Contact     │
│ media       │ │ VoIP, SMS   │ │ support     │ │ center      │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

## Directory Structure

```
zoom-developer-platform/
│
├── README.md                    # Installation + Getting Started
├── ARCHITECTURE.md              # This file
│
├── zoom-platform/               # HUB - Entry point skill
│   ├── SKILL.md                 # Router: "Choose Your Path"
│   ├── references/              # Cross-cutting documentation
│   │   ├── authentication.md
│   │   ├── app-types.md
│   │   ├── scopes.md
│   │   ├── marketplace.md
│   │   ├── rivet.md
│   │   ├── sdk-upgrade-guide.md
│   │   ├── sdk-logs-troubleshooting.md
│   │   └── known-limitations.md
│   └── use-cases/               # Cross-cutting scenarios
│       ├── meeting-automation.md
│       ├── meeting-bots.md
│       ├── recording-transcription.md
│       ├── sdk-size-optimization.md
│       ├── hd-video-resolution.md
│       └── ... (17 use cases)
│
├── zoom-rest-api/               # SPOKE - REST API
│   ├── SKILL.md
│   └── references/
│       ├── meetings.md
│       ├── users.md
│       ├── recordings.md
│       ├── rate-limits.md
│       └── ...
│
├── zoom-webhooks/               # SPOKE - Webhooks
│   ├── SKILL.md
│   └── references/
│
├── zoom-meeting-sdk/            # SPOKE - Meeting SDK
│   ├── SKILL.md
│   └── references/
│       ├── web.md
│       ├── ios.md
│       ├── android.md
│       ├── linux.md
│       ├── bot-authentication.md
│       ├── breakout-rooms.md
│       └── ...
│
├── zoom-video-sdk/              # SPOKE - Video SDK
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
├── zoom-phone/                  # SPOKE - Zoom Phone
│   ├── SKILL.md
│   └── references/
│
├── zoom-cobrowse-sdk/           # SPOKE - Cobrowse SDK
│   ├── SKILL.md
│   └── references/
│
└── zoom-contact-center/         # SPOKE - Contact Center
    ├── SKILL.md
    └── references/
```

## Skill Format

Each skill follows the Agent Skills standard with YAML frontmatter:

```yaml
---
name: skill-name
description: |
  What this skill does and when to use it.
  Include keywords users would naturally say.
---

# Skill Name

[Markdown content with instructions for the agent]
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase, hyphens, 1-64 characters |
| `description` | Yes | 1-1024 characters, include trigger keywords |

## Design Principles

### 1. Hub-and-Spoke Routing

The `zoom-platform` skill acts as a router. When an agent receives a Zoom-related question, it:
1. Loads `zoom-platform/SKILL.md`
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
| **zoom-platform** | Hub/router | Authentication, app types, use cases |
| **zoom-rest-api** | REST API | 600+ endpoints, rate limits, pagination |
| **zoom-webhooks** | Events | Event types, verification, subscriptions |
| **zoom-meeting-sdk** | Embed meetings | Web, iOS, Android, Linux, bot auth |
| **zoom-video-sdk** | Custom video | Sessions, raw media, UI customization |
| **zoom-apps-sdk** | In-client apps | APIs, events, layers, OAuth |
| **zoom-rtms** | Live media | Audio, video, transcripts via WebSocket |
| **zoom-phone** | Cloud phone | VoIP, SMS (read-only), Smart Embed |
| **zoom-cobrowse-sdk** | Co-browsing | Screen sharing, annotation |
| **zoom-contact-center** | Contact center | SDKs, Virtual Agent, APIs |

## Use Cases Summary

| Use Case | Skills Needed |
|----------|---------------|
| Meeting Automation | zoom-rest-api |
| Meeting Bots | zoom-meeting-sdk + zoom-rtms |
| Recording & Transcription | zoom-webhooks + zoom-rest-api |
| HD Video Resolution | zoom-meeting-sdk / zoom-video-sdk |
| SDK Size Optimization | zoom-meeting-sdk / zoom-video-sdk |
| Real-Time AI Integration | zoom-rtms |
| Contact Center | zoom-contact-center |

## Key Technical Gotchas

| Topic | Gotcha |
|-------|--------|
| JWT | JWT *App Type* deprecated, NOT JWT *Signatures* |
| OBF Token | Required Feb 2026 for external meetings |
| HD Video | Container must be ≥1280×720 for 720p |
| 720p Streams | Max 2 concurrent subscriptions |
| Rate Limits | 100 meeting create/update per user per day |
| SDK Size | No feature exclusion; ProGuard causes crashes |
| Breakout Rooms | Cannot auto-open pre-assigned via API |

## Resources

- **Official Docs**: https://developers.zoom.us/
- **Marketplace**: https://marketplace.zoom.us/
- **Developer Forum**: https://devforum.zoom.us/
- **Agent Skills Spec**: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

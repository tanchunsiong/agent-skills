# Agent Skills - Architecture

This document describes the structure and design of the Zoom agent skills repository.

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
│                           zoom-general (HUB)                                │
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
│  Build Team Chat integrations        → zoom-team-chat                       │
│  Manage Zoom Rooms                   → zoom-rooms                           │
│  Work with calendars                 → zoom-calendar                        │
│  Work with email                     → zoom-mail                            │
│  Manage whiteboards                  → zoom-whiteboard                      │
│  Manage documents                    → zoom-docs                            │
│  Manage events/webinars              → zoom-events                          │
│  Build AI chatbots                   → zoom-virtual-agent                   │
│  Connect H.323/SIP rooms             → zoom-crc                             │
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
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  zoom-rtms  │ │ zoom-phone  │ │zoom-team    │ │ zoom-rooms  │ │zoom-calendar│
│             │ │             │ │   -chat     │ │             │ │             │
│ Real-time   │ │ Cloud phone │ │ Messaging   │ │ Room mgmt   │ │ Calendar    │
│ media       │ │ VoIP, SMS   │ │ & channels  │ │ & devices   │ │ integration │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
        │             │               │               │             │
        ▼             ▼               ▼               ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  zoom-mail  │ │zoom-white   │ │ zoom-docs   │ │zoom-events  │ │zoom-contact │
│             │ │   -board    │ │             │ │             │ │   -center   │
│ Email       │ │ Collab      │ │ Document    │ │ Events &    │ │ Contact     │
│ integration │ │ whiteboard  │ │ collab      │ │ webinars    │ │ center      │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
        │             │               │               │             │
        ▼             ▼               ▼               ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│zoom-virtual │ │  zoom-crc   │ │zoom-cobrowse│ │zoom-rivet   │ │zoom-chatbot │
│   -agent    │ │             │ │    -sdk     │ │             │ │   -studio   │
│ AI virtual  │ │ H.323/SIP   │ │ Co-browsing │ │ Dev CLI     │ │ No-code     │
│ agent       │ │ connector   │ │ support     │ │ toolkit     │ │ chatbots    │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
        │             │               │
        ▼             ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│zoom-ui      │ │zoom-probe   │ │zoom-commerce│
│   -toolkit  │ │    -sdk     │ │             │
│ Video UI    │ │ Monitoring  │ │ App         │
│ components  │ │ & debugging │ │ monetization│
└─────────────┘ └─────────────┘ └─────────────┘
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
│       ├── meetings.md
│       ├── users.md
│       ├── recordings.md
│       ├── rate-limits.md
│       ├── authentication.md    # OAuth comprehensive guide
│       ├── quality-management.md
│       ├── workforce-management.md
│       ├── commerce.md
│       ├── healthcare.md
│       ├── video-management.md
│       ├── auto-dialer.md
│       ├── accounts.md
│       ├── scim2.md
│       ├── video-sdk-api.md
│       ├── cobrowse-sdk-api.md
│       ├── marketplace-apps.md
│       └── ...
│
├── zoom-webhooks/               # SPOKE - Webhooks
│   ├── SKILL.md
│   └── references/
│
├── zoom-meeting-sdk/            # SPOKE - Meeting SDK
│   ├── SKILL.md
│   └── references/
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
├── zoom-team-chat/              # SPOKE - Team Chat
│   ├── SKILL.md
│   └── references/
│
├── zoom-rooms/                  # SPOKE - Zoom Rooms
│   ├── SKILL.md
│   └── references/
│
├── zoom-calendar/               # SPOKE - Zoom Calendar
│   ├── SKILL.md
│   └── references/
│
├── zoom-mail/                   # SPOKE - Zoom Mail
│   ├── SKILL.md
│   └── references/
│
├── zoom-whiteboard/             # SPOKE - Zoom Whiteboard
│   ├── SKILL.md
│   └── references/
│
├── zoom-docs/                   # SPOKE - Zoom Docs
│   ├── SKILL.md
│   └── references/
│
├── zoom-events/                 # SPOKE - Zoom Events
│   ├── SKILL.md
│   └── references/
│
├── zoom-contact-center/         # SPOKE - Contact Center
│   ├── SKILL.md
│   └── references/
│
├── zoom-virtual-agent/          # SPOKE - Virtual Agent
│   ├── SKILL.md
│   └── references/
│
├── zoom-crc/                    # SPOKE - Cloud Room Connector
│   ├── SKILL.md
│   └── references/
│
├── zoom-cobrowse-sdk/           # SPOKE - Cobrowse SDK
│   ├── SKILL.md
│   └── references/
│
├── zoom-rivet/                  # SPOKE - Rivet CLI Toolkit
│   ├── SKILL.md
│   └── references/
│
├── zoom-chatbot-studio/         # SPOKE - Chatbot Studio
│   ├── SKILL.md
│   └── references/
│
├── zoom-ui-toolkit/             # SPOKE - UI Toolkit
│   ├── SKILL.md
│   └── references/
│
├── zoom-probe-sdk/              # SPOKE - Probe SDK
│   ├── SKILL.md
│   └── references/
│
└── zoom-commerce/               # SPOKE - Commerce/Monetization
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

## How Skill Discovery Works

Agents need to dynamically discover and load the right skills. This repository supports a three-level loading model:

### Level 1: Hub Routing (Always Load First)

```
Agent receives: "How do I create a meeting?"
Agent loads: zoom-general/SKILL.md
Agent reads: "Choose Your Path" table → routes to zoom-rest-api
```

### Level 2: Spoke Skill Loading

```
Agent loads: zoom-rest-api/SKILL.md
Agent finds: Reference to meetings.md for detailed API docs
```

### Level 3: On-Demand Reference Loading

```
Agent loads: zoom-rest-api/references/meetings.md
Agent now has: Full endpoint documentation
```

### Discovery Patterns for Agents

| Pattern | When to Use | How It Works |
|---------|-------------|--------------|
| **Keyword matching** | User mentions "meeting", "user", "recording" | Match keywords in skill descriptions |
| **Intent routing** | User wants to "embed" vs "build" | zoom-general hub routes based on intent |
| **Skill chaining** | Multi-step workflows | Skills reference other skills by name |
| **Lazy loading** | Detailed docs needed | Load references/ only when needed |

### Skill Discovery Triggers

Agents should load additional skills when they encounter:

1. **Cross-references**: "Use the **zoom-webhooks** skill for event handling"
2. **Combined patterns**: "This use case requires zoom-rest-api + zoom-rtms"
3. **Reference links**: "[See meetings.md](references/meetings.md)"

### Implementation Example

```javascript
// Agent skill discovery pseudocode
function discoverSkills(userQuery) {
  // Always start with hub
  const hubSkill = loadSkill('zoom-general/SKILL.md');
  
  // Route based on intent
  const targetSkill = hubSkill.routeIntent(userQuery);
  
  // Load spoke skill
  const spokeSkill = loadSkill(`${targetSkill}/SKILL.md`);
  
  // Load references on-demand
  if (needsDetailedDocs(userQuery)) {
    const references = spokeSkill.getRelevantReferences(userQuery);
    references.forEach(ref => loadSkill(ref));
  }
  
  return assembledContext;
}
```

For detailed discovery patterns and agent implementation guidance, see [zoom-general/references/skill-discovery.md](zoom-general/references/skill-discovery.md).

## Skills Summary

### Core SDKs & APIs

| Skill | Purpose | Key Topics |
|-------|---------|------------|
| **zoom-general** | Hub/router | Authentication, app types, use cases |
| **zoom-rest-api** | REST API | 600+ endpoints, rate limits, pagination |
| **zoom-webhooks** | Events | Event types, verification, subscriptions |
| **zoom-meeting-sdk** | Embed meetings | Web, iOS, Android, Linux, bot auth |
| **zoom-video-sdk** | Custom video | Sessions, raw media, UI customization |
| **zoom-apps-sdk** | In-client apps | APIs, events, layers, OAuth |
| **zoom-rtms** | Live media | Audio, video, transcripts via WebSocket |

### Zoom Products

| Skill | Purpose | Key Topics |
|-------|---------|------------|
| **zoom-phone** | Cloud phone | VoIP, SMS (read-only), Smart Embed |
| **zoom-team-chat** | Team Chat | Channels, messages, chatbots |
| **zoom-rooms** | Zoom Rooms | Devices, scheduling, controls |
| **zoom-calendar** | Calendar | Calendar sync, scheduling |
| **zoom-mail** | Email | Email integration |
| **zoom-whiteboard** | Whiteboard | Collaborative boards, export |
| **zoom-docs** | Documents | Document collaboration |
| **zoom-events** | Events | Webinars, events management |
| **zoom-contact-center** | Contact center | SDKs, Virtual Agent, APIs |
| **zoom-virtual-agent** | AI chatbot | Conversational AI |
| **zoom-crc** | Room connector | H.323/SIP integration |
| **zoom-cobrowse-sdk** | Co-browsing | Screen sharing, annotation |

### Developer Tools

| Skill | Purpose | Key Topics |
|-------|---------|------------|
| **zoom-rivet** | Dev CLI | Project scaffolding, dev server |
| **zoom-chatbot-studio** | No-code bots | Visual bot builder |
| **zoom-ui-toolkit** | Video UI | React components for Video SDK |
| **zoom-probe-sdk** | Monitoring | Error tracking, performance |
| **zoom-commerce** | Monetization | In-app purchases, subscriptions |

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
| Team Chat Bots | zoom-team-chat + zoom-chatbot-studio |
| Room Management | zoom-rooms + zoom-crc |
| Document Collaboration | zoom-docs + zoom-whiteboard |

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

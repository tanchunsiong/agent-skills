# Zoom Developer Platform Skills

Skills for building with Zoom SDKs, APIs, and integrations. Focused on web development.

Primary skill entrypoint: [SKILL.md](SKILL.md)

## Installation

### Claude Code

```bash
# Clone the repository
git clone https://github.com/tanchunsiong/agent-skills.git

# Copy to Claude Code skills directory
cp -r agent-skills/* ~/.claude/skills/
```

Or install individual skills:
```bash
cp -r agent-skills/general ~/.claude/skills/
cp -r agent-skills/zoom-meeting-sdk ~/.claude/skills/
```

### OpenCode

```bash
# Copy to OpenCode skills directory
cp -r agent-skills/* ~/.config/opencode/skills/
```

### Context7

Skills are automatically discovered when the repository is indexed by Context7.

## Getting Started

### 1. Ask Claude about Zoom development

Once installed, simply ask questions about Zoom development:

```
How do I create a meeting using the Zoom API?
```

```
How do I build a meeting bot that joins and records?
```

```
What's the difference between Meeting SDK and Video SDK?
```

### 2. The agent loads the right skill automatically

The **general** skill acts as a router and directs to the appropriate specialized skill:

| Your Question | Skill Loaded |
|---------------|--------------|
| "Create a meeting via API" | zoom-rest-api |
| "Embed Zoom in my React app" | zoom-meeting-sdk |
| "Build custom video UI" | zoom-video-sdk |
| "Handle webhook events" | webhooks |
| "Build a meeting bot" | zoom-meeting-sdk + rtms |
| "Set up OAuth authentication" | oauth |

### 3. Skills chain automatically

When your task requires multiple skills, the agent loads them as needed. For example, "build a meeting bot" loads:
- **zoom-meeting-sdk** (for joining meetings)
- **rtms** (for real-time audio/video/transcript access)
- **zoom-rest-api** (for creating meetings)

## Skills

| Skill | Description |
|-------|-------------|
| [zoom-general](zoom-general/) | **Hub** - Core concepts, authentication, use cases, routing |
| [zoom-rest-api](zoom-rest-api/) | 600+ REST API endpoints, rate limits, pagination |
| [zoom-webhooks](zoom-webhooks/) | Real-time event notifications |
| [zoom-websockets](zoom-websockets/) | Real-time WebSocket event connections |
| [zoom-meeting-sdk](zoom-meeting-sdk/) | Embed Zoom meetings (Web, React Native, Electron, Linux headless bots) |
| [zoom-video-sdk](zoom-video-sdk/) | Custom video experiences (Web, React Native, Flutter, Linux headless bots) |
| [zoom-apps-sdk](zoom-apps-sdk/) | Apps that run inside Zoom client |
| [zoom-rtms](zoom-rtms/) | Real-time Media Streams (live audio/video/transcripts) |
| [zoom-team-chat](zoom-team-chat/) | Team Chat APIs and integrations |
| [zoom-ui-toolkit](zoom-ui-toolkit/) | Pre-built UI components for Video SDK |
| [zoom-cobrowse-sdk](zoom-cobrowse-sdk/) | Collaborative browsing for support |
| [zoom-oauth](zoom-oauth/) | OAuth authentication (all 4 grant types) |

## Common Use Cases

| Use Case | Skills Needed |
|----------|---------------|
| Schedule meetings programmatically | zoom-rest-api |
| Build meeting bots (AI/transcription) | zoom-meeting-sdk + rtms |
| Embed meetings in your app | zoom-meeting-sdk |
| Custom video experiences | zoom-video-sdk |
| Auto-download recordings to S3/GCS | webhooks + zoom-rest-api |
| Real-time AI processing | rtms |
| In-meeting collaborative apps | zoom-apps-sdk |
| Team Chat integrations | zoom-team-chat |
| Low-latency event notifications | zoom-websockets |
| OAuth authentication setup | oauth |

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full hub-and-spoke structure diagram.

```
zoom-general (HUB)
       │
       ├── zoom-rest-api
       ├── zoom-webhooks
       ├── zoom-websockets
       ├── zoom-meeting-sdk
       ├── zoom-video-sdk
       ├── zoom-apps-sdk
       ├── zoom-rtms
       ├── zoom-team-chat
       ├── zoom-ui-toolkit
       ├── zoom-cobrowse-sdk
       └── zoom-oauth
```

## Directory Structure

```
agent-skills/
├── README.md                 # This file
├── ARCHITECTURE.md           # Full architecture diagram
│
├── zoom-general/            # HUB (entry point)
│   ├── SKILL.md
│   ├── references/           # Cross-cutting docs
│   └── use-cases/            # Multi-skill scenarios
│
└── zoom-*/                   # SPOKES (specialized skills)
    ├── SKILL.md
    └── references/
```

## Resources

- [Zoom Developer Platform](https://developers.zoom.us/)
- [Zoom App Marketplace](https://marketplace.zoom.us/)
- [Zoom Developer Forum](https://devforum.zoom.us/)
- [Zoom GitHub](https://github.com/zoom)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on improving this skill repository.

Quick tips:
- Use `references/` for detailed documentation
- Max 3 directory levels

## License

MIT

# Zoom Developer Platform Skills

Agent Skills for building with Zoom SDKs, APIs, and integrations. Follows the [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) open standard.

## Installation

### Claude Code

```bash
# Clone the repository
git clone https://github.com/user/agent-skills.git

# Copy to Claude Code skills directory
cp -r agent-skills/* ~/.claude/skills/
```

Or install individual skills:
```bash
cp -r agent-skills/zoom-general ~/.claude/skills/
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

The **zoom-general** skill acts as a router and directs to the appropriate specialized skill:

| Your Question | Skill Loaded |
|---------------|--------------|
| "Create a meeting via API" | zoom-rest-api |
| "Embed Zoom in my React app" | zoom-meeting-sdk |
| "Build custom video UI" | zoom-video-sdk |
| "Handle webhook events" | zoom-webhooks |
| "Build a meeting bot" | zoom-meeting-sdk + zoom-rtms |

### 3. Skills chain automatically

When your task requires multiple skills, the agent loads them as needed. For example, "build a meeting bot" loads:
- **zoom-meeting-sdk** (Linux platform for joining meetings)
- **zoom-rtms** (for real-time audio/video/transcript access)
- **zoom-rest-api** (for creating meetings)

## Skills

| Skill | Description |
|-------|-------------|
| [zoom-general](zoom-general/) | **Hub** - Core concepts, authentication, use cases, routing |
| [zoom-rest-api](zoom-rest-api/) | 600+ REST API endpoints, rate limits, pagination |
| [zoom-webhooks](zoom-webhooks/) | Real-time event notifications |
| [zoom-meeting-sdk](zoom-meeting-sdk/) | Embed Zoom meetings (Web, iOS, Android, Desktop, Linux) |
| [zoom-video-sdk](zoom-video-sdk/) | Custom video experiences (not Zoom meetings) |
| [zoom-apps-sdk](zoom-apps-sdk/) | Apps that run inside Zoom client |
| [zoom-rtms](zoom-rtms/) | Real-time Media Streams (live audio/video/transcripts) |
| [zoom-phone](zoom-phone/) | Cloud phone, VoIP, SMS |
| [zoom-cobrowse-sdk](zoom-cobrowse-sdk/) | Collaborative browsing for support |
| [zoom-contact-center](zoom-contact-center/) | Contact Center SDKs and APIs |

## Common Use Cases

| Use Case | Skills Needed |
|----------|---------------|
| Schedule meetings programmatically | zoom-rest-api |
| Build meeting bots (AI/transcription) | zoom-meeting-sdk + zoom-rtms |
| Embed meetings in your app | zoom-meeting-sdk |
| Custom video experiences | zoom-video-sdk |
| Auto-download recordings to S3/GCS | zoom-webhooks + zoom-rest-api |
| Real-time AI processing | zoom-rtms |
| HD video (720p/1080p) | zoom-meeting-sdk / zoom-video-sdk |
| Reduce mobile SDK size | zoom-meeting-sdk / zoom-video-sdk |
| Contact center integration | zoom-contact-center |
| In-meeting collaborative apps | zoom-apps-sdk |

## Documentation Coverage

This skills repository contains comprehensive documentation with code examples for:

- **17 use cases** with implementation patterns
- **10 platform SDKs** (Web, iOS, Android, Windows, macOS, Linux, Electron, React Native, Flutter, Unity)
- **Contact Center SDKs** (Web, iOS, Android) with API documentation
- **Best practices** for authentication, rate limits, and troubleshooting

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full hub-and-spoke structure diagram.

```
zoom-general (HUB)
       │
       ├── zoom-rest-api
       ├── zoom-webhooks
       ├── zoom-meeting-sdk
       ├── zoom-video-sdk
       ├── zoom-apps-sdk
       ├── zoom-rtms
       ├── zoom-phone
       ├── zoom-cobrowse-sdk
       └── zoom-contact-center
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

1. Follow the [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) format
2. Keep SKILL.md under 500 lines
3. Use `references/` for detailed documentation
4. Max 3 directory levels

## License

MIT

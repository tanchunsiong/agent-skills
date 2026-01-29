# How These Skills Were Created

This document describes the process and methodology used to create the Zoom Developer Platform Agent Skills.

## Overview

These skills were created through a **collaborative human-AI process**, combining:
- Human domain expertise and guidance
- AI research and documentation synthesis
- Official Zoom documentation and developer forum insights
- Real-world developer learnings and gotchas

## Creation Process

### 1. Human Input & Direction

**What humans provided:**
- High-level structure decisions (hub-and-spoke model)
- Use case priorities (meeting bots, recording, SDK size optimization)
- Real-world learnings from development experience
- Corrections and clarifications (e.g., "only use Zoom-recommended methods")
- Quality control and validation

**Example human inputs:**
- "zoom sdk and api skills project"
- "another topic is on on behalf token implementation for bots"
- "720p some needs the viewport to be large, if smaller the video scales down"
- "linux sdk for both meeting and video SDK are headless"

### 2. AI Research & Synthesis

**What AI contributed:**
- Research via official documentation, developer forums, GitHub repos
- Cross-referencing multiple sources for accuracy
- Structuring information into the Agent Skills format
- Code examples and API references
- Identifying gotchas and edge cases

**Research sources used:**
- Zoom Developer Documentation (developers.zoom.us)
- Zoom Developer Forum (devforum.zoom.us)
- Zoom GitHub repositories
- Context7 documentation search
- Web search for specific technical details

### 3. Iterative Refinement

Each skill went through multiple rounds:

```
Human Input → AI Draft → Human Review → AI Revision → Final
```

**Example iteration:**
1. Human: "add SDK size optimization use case"
2. AI: Researched and drafted comprehensive guide
3. Human: "use only Zoom-recommended methods, some industry methods don't work"
4. AI: Revised to remove unverified methods, kept only official recommendations

## SDK Archive Extraction Process

### Overview

Official SDK archives were downloaded from the Zoom Marketplace and analyzed to extract:
- Sample code patterns
- API interface definitions
- ProGuard rules and build configurations
- Platform-specific implementation details

### Process

For each SDK archive:

1. **Extract**: Unzip/untar the archive to a temporary directory
2. **Analyze**: Read README, sample code, header files, and configurations
3. **Synthesize**: Merge new patterns and details into existing skill documentation
4. **Clean up**: Remove extracted files and original archive

### SDKs Processed

**Meeting SDK (10 platforms)**:
- Web (zoom-sdk-web) - React/TypeScript patterns, ZFG support, China CDN
- iOS (zoom-sdk-ios) - MobileRTC delegates, raw data interfaces
- Android (zoom-sdk-android) - JoinMeetingHelper, ProGuard rules, VirtualVideoSource
- Windows (zoom-sdk-windows) - DLL dependencies
- macOS (zoom-sdk-macos) - ZoomSDK framework integration
- Linux x86_64/arm64 (zoom-meeting-sdk-linux) - Raw data headers, headless operation
- Electron (zoom-sdk-electron) - IPC patterns
- React Native (meetingsdk-react-native) - Native module bridging
- Unreal Engine (ZM6.1.5-UE5.4) - Blueprint integration
- C# Wrapper (zoom-c-sharp-wrapper) - .NET bindings

**Video SDK (9 platforms)**:
- Web, iOS, Android, Windows, macOS, Linux x86_64/arm64, React Native, Unity

### Key Extractions

| SDK | Key Information Extracted |
|-----|---------------------------|
| Android | Complete ProGuard rules, VirtualVideoSource implementation |
| iOS | MobileRTC delegate categories, raw data saving patterns |
| Linux | IZoomSDKAudioRawDataDelegate, IZoomSDKVideoSource interfaces |
| Web | ZFG endpoints, China CDN, auth endpoint setup |

## Content Sources

### Primary Sources

| Source | Used For |
|--------|----------|
| Zoom Official Docs | API endpoints, SDK methods, configuration |
| Zoom Developer Forum | Gotchas, limitations, community solutions |
| Zoom GitHub Repos | Code examples, type definitions, samples |
| Zoom Blog | Best practices, new features, migration guides |
| **Official SDK Archives** | Sample code, interfaces, build configurations |

### Secondary Sources

| Source | Used For |
|--------|----------|
| Context7 | Documentation search and synthesis |
| Web Search (Exa) | Finding specific technical details |
| GitHub Code Search | Real-world implementation patterns |

## Methodology for Each Skill

### Step 1: Scope Definition
- Identify what the skill should cover
- Define the target audience (developers using AI coding assistants)
- Determine depth (overview in SKILL.md, details in references/)

### Step 2: Research
- Search official documentation
- Check developer forum for common questions/issues
- Find GitHub samples and real implementations
- Cross-reference multiple sources for accuracy

### Step 3: Structure
- Follow Agent Skills standard (YAML frontmatter + Markdown)
- Use hub-and-spoke for routing (zoom-general as hub)
- Keep SKILL.md under 500 lines
- Move detailed content to references/

### Step 4: Write Content
- Start with quick start / minimal example
- Add common tasks and code examples
- Document gotchas and limitations
- Include links to official resources

### Step 5: Validate
- Cross-check with official documentation
- Verify code examples are syntactically correct
- Ensure links are valid
- Get human review for accuracy

## Quality Standards

### What We Prioritized

1. **Accuracy over completeness** - Better to have verified information than comprehensive but incorrect
2. **Practical examples** - Real code that developers can copy-paste
3. **Gotchas first** - Common mistakes and limitations prominently documented
4. **Official sources** - Prefer Zoom's own documentation over third-party

### What We Avoided

1. **Unverified claims** - If not confirmed by official source, marked as such
2. **Outdated information** - Checked deprecation status of APIs/features
3. **Speculation** - Didn't guess at undocumented behavior
4. **Over-engineering** - Simple examples over complex ones

## Statistics

| Metric | Count |
|--------|-------|
| Total Skills | 11 (1 hub + 10 spokes) |
| Use Cases | 21 |
| Reference Documents | ~60+ |
| Total Markdown Files | ~107 |
| Human Review Cycles | Multiple per major topic |

## Key Learnings Documented

Many critical learnings came from human experience and were incorporated:

| Learning | Source |
|----------|--------|
| JWT App Type deprecated ≠ JWT Signatures deprecated | Developer confusion in forum |
| Video scales down if container < 1280×720 | Human testing experience |
| ProGuard crashes with Zoom SDK | Human development experience |
| OBF token requires user to be IN meeting | Official announcement |
| Max 2 concurrent 720p streams | Forum + documentation |
| `renderVideo()` must be called AFTER `startVideo()` | Human development experience |

## Session 3: Gap Analysis & Coverage Expansion

### Coverage Analysis Process

A systematic analysis was performed to identify documentation gaps by comparing the existing skills against common developer scenarios.

**Methodology:**
1. Listed all common Zoom developer tasks
2. Checked if each was covered by existing documentation
3. Prioritized gaps by developer frequency/need

### Files Created/Enhanced

| File | Lines | Description |
|------|-------|-------------|
| `zoom-general/references/error-codes.md` | ~250 | Comprehensive error codes for REST API, Meeting SDK, Video SDK, webhooks |
| `zoom-general/use-cases/testing-development.md` | ~200 | ngrok setup, webhook testing, SDK debug modes, test accounts |
| `zoom-meeting-sdk/references/webinars.md` | ~250 | SDK-specific webinar features (Q&A, raise hand, polling, attendee/panelist roles) |
| `zoom-general/use-cases/marketplace-publishing.md` | ~250 | ISV multi-tenant guide, OAuth token storage, app review process |
| `zoom-general/references/compliance.md` | ~250 | HIPAA, GDPR, security best practices, audit logging |
| `zoom-video-sdk/references/macos.md` | +150 | Enhanced: delegate pattern, screen sharing, gallery view, SwiftUI integration |
| `zoom-video-sdk/references/windows.md` | +350 | Enhanced: event handling, screen sharing, virtual camera/mic/speaker |
| `zoom-general/use-cases/minutes-calculation.md` | ~750 | Video SDK & Meeting SDK usage tracking, YTD calculation, billing/cost estimation |

### Key Topics Added

1. **Error Handling** - Complete error code reference across all SDKs
2. **Testing & Development** - Local development setup, webhook testing with ngrok
3. **Webinar SDK Features** - Q&A, polling, raise hand (SDK-specific, not just API)
4. **Marketplace Publishing** - ISV app submission, multi-tenant OAuth patterns
5. **Compliance** - HIPAA, GDPR, security considerations
6. **Minutes Calculation** - Billing usage tracking, YTD reports, cost projections
7. **Virtual Camera/Mic** - Windows SDK custom video/audio source injection

## Session 4: RTMS Protocol Cleanup

### Overview

A comprehensive audit and cleanup of 100 RTMS use case files was performed to fix fabricated WebSocket protocol patterns.

### Problem Identified

The original RTMS use case files were created without access to real RTMS documentation and contained fabricated patterns:
- **Binary format**: Used `data[0]`, `0x01`, `0x02`, `0x03`, `0x04` byte prefixes (WRONG)
- **Fabricated headers**: Used `X-Zoom-RTMS-Stream-Id`, `X-Zoom-RTMS-Signature` HTTP headers (WRONG)
- **String msg_types**: Used `msg_type: 'SIGNALING'`, `action: 'AUTH'` (WRONG)

### Correct RTMS Protocol

The real RTMS protocol uses:
- **JSON messages** with numeric `msg_type` fields
- **Two-phase WebSocket**: Signaling (msg_type 1→2) then Media (msg_type 3→4→7)
- **HMAC-SHA256 auth**: `crypto.createHmac('sha256', clientSecret).update(`${clientId},${meetingUuid},${streamId}`).digest('hex')`
- **Message types**: 12=keep-alive request, 13=keep-alive response, 14=audio, 15=video, 17=transcript, 18=chat
- **Base64-encoded media content**

### Changes Made

| Action | Count | Description |
|--------|-------|-------------|
| Deleted | 18 | Duplicates, fabricated analytics/compliance APIs, pure utilities |
| Created | 18 | New files based on real rtms-samples repo |
| Fixed | 22 | Binary format → JSON protocol, auth headers → two-phase WebSocket |

### Reference Used

- Cloned official repo: `git clone https://github.com/zoom/rtms-samples`
- Key files: `RTMS_CONNECTION_FLOW.md`, `MEDIA_PARAMETERS.md`
- Working examples: `boilerplate/working_js/`, `working_python/`

### Final State

- **95 RTMS use case files** with correct JSON WebSocket protocol
- All verification checks pass:
  - `grep -l "0x01|0x02|0x03|0x04" rtms-*.md` returns 0 files
  - `grep -l "X-Zoom-RTMS" rtms-*.md` returns 0 files
  - `grep -l "msg_type.*SIGNALING" rtms-*.md` returns 0 files

### Tools Used

| Tool | Purpose |
|------|---------|
| Claude AI (claude-opus-4-5) | Orchestration, analysis, fix generation |
| Sisyphus Work System | Task tracking and delegation |
| Official rtms-samples repo | Reference for correct protocol |

## Maintenance

These skills should be updated when:
- New SDK versions are released
- APIs are deprecated or changed
- New features are announced
- New gotchas are discovered through development

## Format Standard

We followed the [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) open standard:

```yaml
---
name: skill-name          # Required: lowercase, hyphens
description: |            # Required: when to use this skill
  Description here.
---

# Skill Name

[Markdown content]
```

## Tools Used

| Tool | Purpose |
|------|---------|
| Claude AI | Research, synthesis, writing |
| Context7 | Documentation search |
| Exa Web Search | Finding specific technical details |
| GitHub Search | Code examples |
| Human expertise | Direction, validation, real-world learnings |

## Contributing

To add or update skills:

1. Identify the topic and verify with official sources
2. Follow the SKILL.md format
3. Add detailed content to references/ folder
4. Keep max 3 directory levels
5. Test with Claude Code or OpenCode
6. Get human review for accuracy

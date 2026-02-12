# Skill Discovery and Automatic Loading

This document explains how the Agent Skills framework automatically discovers and loads skills based on user queries.

## Overview

The framework uses a **progressive disclosure architecture** where:
1. **Discovery Phase**: Agent scans all `SKILL.md` files and loads frontmatter metadata (name, description, triggers)
2. **Routing Phase**: Agent matches user query against skill metadata using multiple strategies
3. **Activation Phase**: Agent loads the full SKILL.md body only when the skill is relevant
4. **Execution Phase**: Agent follows skill instructions and loads referenced documentation

## How Skills Are Discovered

### 1. SKILL.md Frontmatter Metadata

Every skill defines metadata in YAML frontmatter:

```yaml
---
name: zoom-meeting-sdk
description: |
  Zoom Meeting SDK for embedding Zoom meetings into web, React Native, Electron, and Linux applications. 
  Use when you want to integrate the full Zoom meeting experience into your app.
triggers:
  - "embed meeting"
  - "integrate zoom meeting"
  - "meeting in web app"
  - "meeting sdk"
  - "join meeting programmatically"
---
```

**Fields:**
- **name** (required): Unique skill identifier (kebab-case)
- **description** (required): When to use this skill (1-3 sentences, keyword-rich)
- **triggers** (optional): Explicit phrases that activate this skill

### 2. Query Routing Strategies

The framework uses **multiple strategies** to match queries to skills:

#### A. Hub-and-Spoke Routing (Primary)

The `general` skill acts as the central router with a "Choose Your Path" table:

```markdown
| I want to... | Use this skill |
|--------------|----------------|
| Make API calls | zoom-rest-api |
| Embed Zoom meetings | zoom-meeting-sdk |
| Build custom video experiences | zoom-video-sdk |
| Build an app inside Zoom client | zoom-apps-sdk |
```

**How it works:**
1. User query: "How do I embed a meeting in a web application?"
2. Agent loads `zoom-general/SKILL.md`
3. Agent reads "Choose Your Path" table
4. Agent matches intent: "Embed Zoom meetings" → `zoom-meeting-sdk`
5. Agent loads `zoom-meeting-sdk/SKILL.md` automatically

#### B. Keyword/Trigger Matching (Secondary)

Skills with explicit `triggers` in frontmatter can be matched directly:

```yaml
triggers:
  - "embed meeting"
  - "meeting in web app"
```

**Matching process:**
1. Lowercase and normalize user query
2. Check if any trigger phrase appears in query
3. Score matches by:
   - Exact phrase match (highest)
   - Partial phrase match (medium)
   - Individual keyword match (lowest)

#### C. Description Semantic Matching (Fallback)

When triggers don't match, the agent:
1. Reads skill `description` fields
2. Identifies keywords and concepts
3. Matches against user query semantically

**Example:**
- Query: "How do I add Zoom to my website?"
- Matches `zoom-meeting-sdk` description: "embedding Zoom meetings into **web** applications"

## Configuration Examples

### Example 1: Embedding a Meeting in a Web Application

**User Query:**
> "How do I embed a meeting in a web application?"

**Routing Path:**

```
1. Agent loads zoom-general/SKILL.md (hub)

2. Agent reads "Choose Your Path" table:
   | I want to... | Use this skill |
   |--------------|----------------|
   | Embed Zoom meetings | zoom-meeting-sdk |  ← MATCH

3. Agent loads zoom-meeting-sdk/SKILL.md

4. zoom-meeting-sdk/SKILL.md references:
   - zoom-meeting-sdk/web/SKILL.md (Component View vs Client View)
   
5. Agent loads zoom-meeting-sdk/web/SKILL.md

6. Agent provides Quick Start code examples
```

**Frontmatter Configuration (zoom-meeting-sdk/SKILL.md):**

```yaml
---
name: zoom-meeting-sdk
description: |
  Zoom Meeting SDK for embedding Zoom meetings into web, React Native, Electron, and Linux applications. 
  Use when you want to integrate the full Zoom meeting experience into your app.
  Supports Web (JavaScript), React Native (iOS/Android), Electron desktop apps, Linux (C++ headless bots), and native platforms.
triggers:
  - "embed meeting"
  - "embed zoom meeting"
  - "integrate meeting"
  - "meeting in web app"
  - "meeting in website"
  - "add zoom to website"
  - "meeting sdk"
  - "join meeting programmatically"
---
```

### Example 2: Building a Meeting Bot

**User Query:**
> "How do I build a bot that joins meetings and records audio?"

**Routing Path:**

```
1. Agent loads zoom-general/SKILL.md (hub)

2. Agent reads Use Cases section:
   | Use Case | Skills Needed |
   |----------|---------------|
   | Meeting Bots | zoom-meeting-sdk + rtms |  ← MATCH

3. Agent loads zoom-general/use-cases/meeting-bots.md

4. Use case references:
   - zoom-meeting-sdk (Linux SDK for headless bots)
   - rtms (Real-Time Media Streams for raw audio)

5. Agent loads both skills:
   - zoom-meeting-sdk/linux/zoom-meeting-sdk-bot.md
   - zoom-rtms/examples/rtms-bot.md

6. Agent provides integrated bot implementation guide
```

**Frontmatter Configuration (zoom-meeting-sdk/SKILL.md):**

```yaml
triggers:
  - "meeting bot"
  - "join meeting programmatically"
  - "headless bot"
  - "bot joins meeting"
  - "record meeting audio"
  - "raw media access"
```

**Frontmatter Configuration (zoom-rtms/SKILL.md):**

```yaml
triggers:
  - "real-time media"
  - "rtms"
  - "live audio stream"
  - "live video stream"
  - "meeting transcription"
  - "raw audio"
  - "raw video"
  - "websocket media"
```

### Example 3: Making API Calls

**User Query:**
> "How do I create a meeting using the Zoom API?"

**Routing Path:**

```
1. Agent loads zoom-general/SKILL.md (hub)

2. Agent reads "Choose Your Path" table:
   | I want to... | Use this skill |
   |--------------|----------------|
   | Make API calls | zoom-rest-api |  ← MATCH

3. Agent loads zoom-rest-api/SKILL.md

4. Agent provides:
   - POST /users/{userId}/meetings endpoint
   - Request body schema
   - Authentication requirements
   - Code examples
```

**Frontmatter Configuration (zoom-rest-api/SKILL.md):**

```yaml
---
name: zoom-rest-api
description: |
  Zoom REST API - 600+ endpoints for managing users, meetings, webinars, and more.
  Use when you need to programmatically create, update, or retrieve Zoom resources.
triggers:
  - "api call"
  - "rest api"
  - "create meeting"
  - "get meeting"
  - "list meetings"
  - "update meeting"
  - "create user"
  - "zoom api"
  - "api endpoint"
---
```

## Writing Effective Frontmatter

### Description Field

**Purpose:** Helps the agent decide when to use this skill.

**Best Practices:**
- ✅ Start with skill name/technology
- ✅ Include "Use when..." clause
- ✅ Pack with keywords from user queries
- ✅ Keep to 2-3 sentences max
- ❌ Avoid vague, poetic language
- ❌ Don't include implementation details

**Examples:**

```yaml
# ❌ BAD: Vague, no keywords
description: "A comprehensive guide to building beautiful user interfaces"

# ✅ GOOD: Specific, keyword-rich
description: |
  Zoom Meeting SDK for embedding Zoom meetings into web, React Native, Electron, and Linux applications. 
  Use when you want to integrate the full Zoom meeting experience into your app.
  Supports Web (JavaScript), React Native (iOS/Android), Electron desktop apps, Linux (C++ headless bots), and native platforms.
```

### Triggers Field

**Purpose:** Explicit phrases that activate this skill.

**Best Practices:**
- ✅ Include common variations ("embed meeting", "integrate meeting")
- ✅ Include technical terms ("meeting sdk", "headless bot")
- ✅ Include user intent phrases ("add zoom to website")
- ✅ Use lowercase (framework normalizes automatically)
- ❌ Don't duplicate description content
- ❌ Don't include full sentences

**Examples:**

```yaml
# Meeting SDK Triggers
triggers:
  - "embed meeting"
  - "embed zoom meeting"
  - "integrate meeting"
  - "meeting in web app"
  - "meeting in website"
  - "add zoom to website"
  - "meeting sdk"
  - "join meeting programmatically"

# Video SDK Triggers (different from Meeting SDK!)
triggers:
  - "custom video"
  - "video sdk"
  - "build video app"
  - "video session"
  - "video chat"
  - "video call"
  - "video conferencing"

# REST API Triggers
triggers:
  - "api call"
  - "rest api"
  - "create meeting"
  - "get meeting"
  - "list meetings"
  - "update meeting"
  - "delete meeting"
  - "zoom api"
```

## Skill Chaining

When a task requires multiple skills, the framework chains them automatically.

### Use Case Files

**Location:** `zoom-general/use-cases/`

**Purpose:** Define multi-skill workflows and route to them.

**Example (meeting-bots.md):**

```markdown
---
title: Building Meeting Bots
skills:
  - zoom-meeting-sdk
  - rtms
---

# Building Meeting Bots

Zoom bots are headless applications that join meetings to provide AI features like transcription, 
recording, or real-time analysis.

## Skills Needed

- **zoom-meeting-sdk** (Linux) - Join meetings programmatically
- **rtms** - Access real-time audio/video streams

## Implementation Overview

1. Use `zoom-meeting-sdk` (Linux SDK) to join meeting
2. Use `rtms` to subscribe to audio/video streams via WebSocket
3. Process raw media in real-time
```

### How Chaining Works

```
User Query: "How do I build a meeting bot?"
     ↓
zoom-general/SKILL.md (hub)
     ↓
"Meeting Bots" use case found
     ↓
zoom-general/use-cases/meeting-bots.md loaded
     ↓
References: zoom-meeting-sdk + rtms
     ↓
Agent loads BOTH skills automatically
     ↓
Integrated guidance provided
```

## Testing Skill Discovery

### Manual Testing

Test your frontmatter by asking the agent questions:

```
✅ Should route to zoom-meeting-sdk:
- "How do I embed a meeting in a web application?"
- "I want to add Zoom meetings to my website"
- "Meeting SDK quickstart"

✅ Should route to zoom-video-sdk:
- "How do I build a custom video app?"
- "I want to create my own video chat interface"
- "Video SDK documentation"

✅ Should route to zoom-rest-api:
- "How do I create a meeting using the API?"
- "List all meetings for a user"
- "API endpoint for updating meetings"
```

### Adding New Triggers

1. Identify common user queries that should route to your skill
2. Add trigger phrases to `triggers` array in frontmatter
3. Test with sample queries
4. Update "Choose Your Path" table in `zoom-general/SKILL.md` if adding new intent category

**Example: Adding Twitter Spaces-style trigger**

```yaml
# Before
triggers:
  - "custom video"
  - "video sdk"

# After
triggers:
  - "custom video"
  - "video sdk"
  - "twitter spaces"           # NEW
  - "clubhouse alternative"    # NEW
  - "audio-only room"          # NEW
```

## Advanced: Hierarchical Skills

Some skills have sub-skills for specific platforms or use cases.

### Example: zoom-meeting-sdk Hierarchy

```
zoom-meeting-sdk/                    # Parent skill
├── SKILL.md                          # General overview, routing
├── web/
│   ├── SKILL.md                      # Web SDK (Component + Client View)
│   ├── component-view/SKILL.md       # Component View details
│   └── client-view/SKILL.md          # Client View details
├── windows/SKILL.md                  # Windows SDK (C++)
└── linux/
    ├── linux.md                      # Linux SDK overview
    └── meeting-sdk-bot.md            # Headless bot implementation
```

**Parent skill (zoom-meeting-sdk/SKILL.md)** routes to platform-specific sub-skills:

```markdown
## Detailed References

### Platform Guides
- **[linux/linux.md](zoom-meeting-sdk/linux/linux.md)** - Linux SDK (C++ headless bots)
- **[windows/SKILL.md](zoom-meeting-sdk/windows/SKILL.md)** - Windows SDK (C++ desktop apps)
- **[web/SKILL.md](zoom-meeting-sdk/web/SKILL.md)** - Web SDK (Component + Client View)
```

**Query routing:**
- "How do I embed a meeting in React?" → zoom-meeting-sdk/web/SKILL.md
- "How do I build a Linux bot?" → zoom-meeting-sdk/linux/zoom-meeting-sdk-bot.md
- "Windows Meeting SDK guide" → zoom-meeting-sdk/windows/SKILL.md

## Troubleshooting

### Skill Not Being Loaded

**Problem:** User query doesn't route to expected skill.

**Solutions:**
1. **Check frontmatter:** Ensure `triggers` array includes relevant phrases
2. **Check description:** Add keywords from user query to description
3. **Check hub routing:** Update "Choose Your Path" table in zoom-general/SKILL.md
4. **Add use case:** Create use-case file in zoom-general/use-cases/ if multi-skill workflow

**Example:**

```yaml
# User asks: "How do I add Zoom to my Next.js app?"
# But zoom-meeting-sdk doesn't load.

# Solution: Add framework-specific triggers
triggers:
  - "embed meeting"
  - "meeting sdk"
  - "next.js zoom"        # ADD
  - "react zoom"          # ADD
  - "zoom in nextjs"      # ADD
```

### Wrong Skill Being Loaded

**Problem:** Query routes to incorrect skill.

**Solutions:**
1. **Check trigger overlap:** Ensure triggers don't conflict with other skills
2. **Be more specific:** Add disambiguating keywords
3. **Update description:** Clarify when to use vs not use

**Example:**

```yaml
# Problem: "custom video app" routes to zoom-meeting-sdk instead of zoom-video-sdk

# zoom-meeting-sdk/SKILL.md - Remove overlapping trigger
triggers:
  - "embed meeting"
  - "meeting sdk"
  # REMOVE: "custom video"  # This belongs to Video SDK!

# zoom-video-sdk/SKILL.md - Keep this trigger
triggers:
  - "custom video"
  - "video sdk"
  - "build video app"
```

### Multiple Skills Needed

**Problem:** Task requires multiple skills, but only one loads.

**Solutions:**
1. **Create use case file:** Define multi-skill workflow in zoom-general/use-cases/
2. **Add skill chaining:** Reference other skills by name in SKILL.md body
3. **Update hub:** Add to "Skill Chaining" section in zoom-general/SKILL.md

**Example:**

```markdown
<!-- zoom-general/use-cases/meeting-bots.md -->
# Building Meeting Bots

## Skills Needed

- **zoom-meeting-sdk** (Linux) - Join meetings
- **rtms** - Access raw media streams

[Implementation details...]
```

## Summary

The Agent Skills framework discovers and loads skills using:

1. **Progressive Disclosure**: Load metadata first, full content only when needed
2. **Hub-and-Spoke Routing**: general routes to specialized skills
3. **Multi-Strategy Matching**: Keywords, triggers, semantic similarity
4. **Skill Chaining**: Use cases define multi-skill workflows

**To configure automatic discovery:**
1. Add descriptive frontmatter with `name`, `description`, and `triggers`
2. Include skill in zoom-general/SKILL.md "Choose Your Path" table
3. Create use-case files for multi-skill workflows
4. Test with common user queries

**For the specific example from the feedback:**
- Query: "How do I embed a meeting in a web application?"
- Routes via: general → "Choose Your Path" table → zoom-meeting-sdk
- Triggers: "embed meeting", "meeting in web app", "add zoom to website"
- Result: Agent loads zoom-meeting-sdk/SKILL.md and provides Web SDK guidance

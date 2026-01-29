# Agent Skills Discovery and Loading

How the Agent Skills framework discovers, matches, and loads skills.

## Overview

Agent Skills is an open standard for packaging domain knowledge that AI coding assistants can automatically discover and use. This document explains how skills are found, matched to user requests, and loaded into context.

## The Three-Level Loading Model

Skills are loaded progressively to minimize token usage while maximizing capability:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        THREE-LEVEL SKILL LOADING                         │
└─────────────────────────────────────────────────────────────────────────┘

Level 1: METADATA (Always loaded at startup)
┌─────────────────────────────────────────────────────────────────────────┐
│ • YAML frontmatter only (name + description)                            │
│ • ~50-100 tokens per skill                                              │
│ • Injected into system prompt                                           │
│ • Used for skill matching                                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ (When skill is triggered)
Level 2: INSTRUCTIONS (Loaded on-demand)
┌─────────────────────────────────────────────────────────────────────────┐
│ • Full SKILL.md body content                                            │
│ • Under 5,000 tokens                                                    │
│ • Step-by-step instructions                                             │
│ • Code examples and patterns                                            │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ (As needed during execution)
Level 3+: RESOURCES (Loaded as needed)
┌─────────────────────────────────────────────────────────────────────────┐
│ • Bundled files in references/, scripts/, etc.                          │
│ • Effectively unlimited tokens                                          │
│ • Loaded via tool calls (Read, Bash)                                    │
│ • May include executable scripts                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

## YAML Frontmatter Format

Every skill must have a `SKILL.md` file with YAML frontmatter:

### Required Fields

```yaml
---
name: zoom-meeting-sdk
description: |
  Embed Zoom meetings in web, iOS, Android, and desktop applications using the Meeting SDK.
  Use when building apps that need to join or host Zoom meetings, create meeting bots,
  or integrate video conferencing into your application.
---

# Zoom Meeting SDK

[Skill instructions and documentation...]
```

### Field Specifications

| Field | Required | Constraints | Purpose |
|-------|----------|-------------|---------|
| `name` | **Yes** | 1-64 chars, lowercase, hyphens only | Unique identifier |
| `description` | **Yes** | 1-1024 chars | Skill matching keywords |

### Name Field Rules

- Lowercase letters, numbers, and hyphens only
- Cannot start or end with hyphen
- No consecutive hyphens (`--`)
- Must match parent directory name

**Valid examples:**
```yaml
name: zoom-meeting-sdk
name: data-analysis
name: pdf-processing
```

**Invalid examples:**
```yaml
name: Zoom-Meeting-SDK    # Uppercase not allowed
name: -zoom-sdk           # Cannot start with hyphen
name: zoom--sdk           # Consecutive hyphens not allowed
```

### All Optional Fields

```yaml
---
name: skill-name
description: What this skill does and when to use it.
license: Apache-2.0
compatibility: Requires Node.js 18+, internet access
metadata:
  author: your-org
  version: "1.0.0"
  tags: ["zoom", "video", "meetings"]
allowed-tools: Bash(npm:*) Read Write
---
```

## How Skill Matching Works

### 1. System Prompt Injection

At startup, the agent's system prompt includes all skill metadata:

```xml
<available_skills>
  <skill>
    <name>zoom-meeting-sdk</name>
    <description>Embed Zoom meetings in web, iOS, Android, and desktop applications...</description>
    <location>/path/to/skills/zoom-meeting-sdk/SKILL.md</location>
  </skill>
  <skill>
    <name>zoom-rest-api</name>
    <description>Zoom REST API with 600+ endpoints for meetings, users, recordings...</description>
    <location>/path/to/skills/zoom-rest-api/SKILL.md</location>
  </skill>
</available_skills>
```

### 2. Keyword Matching in Description

When a user asks a question, the agent matches keywords in descriptions:

**User asks:** "How do I embed a Zoom meeting in my React app?"

**Agent matches:** `zoom-meeting-sdk` because description contains:
- "Embed Zoom meetings"
- "web" (React is web)
- "applications"

### 3. Skill Loading

The agent reads the matched skill:

```javascript
// Agent issues tool call to load skill
await readFile('/path/to/skills/zoom-meeting-sdk/SKILL.md');
```

## Writing Effective Descriptions

### Best Practices

**DO: Include WHAT and WHEN**

```yaml
description: |
  Embed Zoom meetings in web, iOS, Android, and desktop applications using the Meeting SDK.
  Use when building apps that need to join or host Zoom meetings, create meeting bots,
  or integrate video conferencing into your application.
```

**DO: Include common trigger phrases**

```yaml
description: |
  Extract text and tables from PDF files, fill forms, merge documents.
  Use when working with PDF files or when the user mentions PDFs, forms,
  document extraction, or .pdf files.
```

**DON'T: Be too vague**

```yaml
# Bad - won't match specific queries
description: Helps with video stuff
description: API documentation
```

**DON'T: Use first/second person**

```yaml
# Bad - descriptions are injected into system prompt
description: I can help you with meetings
description: You can use this to create meetings
```

### Trigger Word Examples

Include words users naturally say:

| Domain | Trigger Words |
|--------|---------------|
| Meeting SDK | embed, meeting, join, host, video call, conferencing |
| REST API | API, endpoint, create meeting, list users, programmatically |
| Webhooks | webhook, event, notification, real-time, trigger |
| Phone | phone, call, VoIP, dial, SMS, voicemail |

## Platform Configuration

### Claude Code

Skills are stored in `~/.claude/skills/` (personal) or `.claude/skills/` (project):

```bash
# Install skills
git clone https://github.com/user/agent-skills.git
cp -r agent-skills/* ~/.claude/skills/

# Directory structure
~/.claude/skills/
├── zoom-meeting-sdk/
│   └── SKILL.md
├── zoom-rest-api/
│   └── SKILL.md
└── zoom-webhooks/
    └── SKILL.md
```

### OpenCode

Skills are stored in `~/.config/opencode/skills/`:

```bash
cp -r agent-skills/* ~/.config/opencode/skills/
```

### Context7

Skills are automatically indexed when the repository is added:

```bash
# Add repository to Context7
context7 add https://github.com/user/agent-skills
```

### Programmatic Integration

For custom agents, implement skill discovery:

```javascript
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

/**
 * Discover all skills in a directory
 */
function discoverSkills(skillsDir) {
  const skills = [];
  
  for (const dir of fs.readdirSync(skillsDir)) {
    const skillPath = path.join(skillsDir, dir, 'SKILL.md');
    
    if (fs.existsSync(skillPath)) {
      const content = fs.readFileSync(skillPath, 'utf-8');
      const metadata = parseYAMLFrontmatter(content);
      
      if (metadata.name && metadata.description) {
        skills.push({
          name: metadata.name,
          description: metadata.description,
          path: skillPath
        });
      }
    }
  }
  
  return skills;
}

/**
 * Parse YAML frontmatter from markdown
 */
function parseYAMLFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (match) {
    return yaml.load(match[1]);
  }
  return {};
}

/**
 * Generate system prompt with available skills
 */
function generateSkillsPrompt(skills) {
  let prompt = '<available_skills>\n';
  
  for (const skill of skills) {
    prompt += `  <skill>\n`;
    prompt += `    <name>${skill.name}</name>\n`;
    prompt += `    <description>${skill.description}</description>\n`;
    prompt += `    <location>${skill.path}</location>\n`;
    prompt += `  </skill>\n`;
  }
  
  prompt += '</available_skills>';
  return prompt;
}

// Usage
const skills = discoverSkills('./skills');
const systemPromptAddition = generateSkillsPrompt(skills);
```

## Skill Directory Structure

```
skill-name/
├── SKILL.md              # Required: Main skill file
├── references/           # Optional: Detailed documentation
│   ├── api-endpoints.md
│   ├── authentication.md
│   └── examples.md
├── scripts/              # Optional: Executable code
│   ├── setup.sh
│   └── validate.js
└── assets/               # Optional: Templates, configs
    └── template.json
```

### Maximum Depth

Skills should be no more than 3 levels deep:

```
skill-name/           # Level 1
├── SKILL.md
├── references/       # Level 2
│   └── topic.md      # Level 3 (max)
└── use-cases/        # Level 2
    └── example.md    # Level 3 (max)
```

## Skill Chaining

Skills can reference other skills by name. The agent automatically loads referenced skills:

```markdown
For webhook event handling, use the **zoom-webhooks** skill.
```

When the agent encounters this, it:
1. Recognizes `zoom-webhooks` as a skill name
2. Loads that skill's SKILL.md
3. Continues with combined context

### Explicit Chaining Table

Skills can include explicit chaining guidance:

```markdown
## Related Skills

| I want to... | Use this skill |
|--------------|----------------|
| Create meetings via API | **zoom-rest-api** |
| Receive meeting events | **zoom-webhooks** |
| Build custom video UI | **zoom-video-sdk** |
```

## Validation

### Validate a Skill

```bash
# Check YAML frontmatter
grep -A 10 "^---" SKILL.md | head -20

# Verify name matches directory
SKILL_NAME=$(grep "^name:" SKILL.md | cut -d: -f2 | tr -d ' ')
DIR_NAME=$(basename $(pwd))
[ "$SKILL_NAME" = "$DIR_NAME" ] && echo "✓ Name matches" || echo "✗ Name mismatch"

# Check description length
DESC_LEN=$(grep -A 100 "^description:" SKILL.md | grep -B 100 "^---" | wc -c)
[ $DESC_LEN -lt 1024 ] && echo "✓ Description length OK" || echo "✗ Description too long"
```

### Reference Implementation

The [agentskills.io](https://agentskills.io) standard provides a reference validator:

```bash
npm install -g skills-ref
skills-ref validate ./my-skill
```

## Resources

- **Agent Skills Spec**: https://agentskills.io
- **Anthropic Blog Post**: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- **Official Docs**: https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview
- **Example Skills**: https://github.com/anthropics/skills

# Test Instructions: zoom-oauth

## Purpose

This is a test session to evaluate the **zoom-oauth** skill. Your task is to use the skill documentation to build a working OAuth integration, then critically assess the skill's quality and suggest improvements.

## Skill Documentation

**Skill file location**: `/home/dreamtcs/agent-skills-lite/zoom-oauth/SKILL.md`

**Additional references**: `/home/dreamtcs/agent-skills-lite/zoom-oauth/references/`

## Your Task

### 1. Build a Project

Create a functional OAuth integration using the skill documentation. Suggested project ideas:

- Server-to-Server OAuth token generator
- User OAuth flow with authorization code exchange
- Admin OAuth app with account-wide access
- Token refresh service with automatic renewal
- Multi-tenant OAuth app supporting multiple accounts

### 2. Document Issues Found

As you build, note any problems with the skill documentation:

- **Missing information**: What did you need that wasn't documented?
- **Outdated content**: Are endpoints, parameters, responses current?
- **Unclear instructions**: What was confusing or ambiguous?
- **Incorrect examples**: Did any code samples fail to work?
- **Missing error handling**: Are token errors, refresh failures covered?
- **Scope gaps**: Are all common scopes documented?

### 3. Suggest Improvements

Be critical but constructive. Consider:

- Is Admin vs User OAuth clearly explained?
- Are token refresh patterns documented for all scenarios?
- Is scope selection guidance provided?
- Are error responses and handling documented?
- Is token storage security covered?
- Are there examples in multiple languages?
- Is the difference between S2S and User OAuth clear?
- Are rate limits on token endpoints mentioned?

## Development Approach

**One-shot implementation preferred**: Gather all necessary requirements and context upfront, then implement in a single, comprehensive pass. Ask clarifying questions BEFORE coding, not during.

**Track back-and-forth as skill quality signal**: If you find yourself going back and forth during implementation (retrying, debugging, searching for missing info), this is a RED FLAG that the skill documentation is unclear, incomplete, or incorrect. Document each instance:

- What caused the back-and-forth?
- What information was missing or wrong?
- How many iterations did it take to resolve?
- What should the skill have said to prevent this?

Excessive iteration = poor skill quality. This feedback is critical for improvement.

## Feedback Destination

**Important**: All feedback and improvements will be incorporated back into the **agent-skills-lite** repository at `/home/dreamtcs/agent-skills-lite/zoom-oauth/`. Your critical analysis helps improve the skill for future users.

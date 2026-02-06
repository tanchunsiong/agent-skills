# Zoom Video SDK Windows - Complete Documentation Index

## Quick Start Path

**If you're new to the SDK, follow this order:**

1. **Read the architecture pattern** → [concepts/sdk-architecture-pattern.md](concepts/sdk-architecture-pattern.md)
   - Universal formula: Singleton → Delegate → Subscribe
   - Once you understand this, you can implement any feature

2. **Fix build errors** → [troubleshooting/build-errors.md](troubleshooting/build-errors.md)
   - SDK header dependencies
   - Required include order

3. **Implement session join** → [examples/session-join-pattern.md](examples/session-join-pattern.md)
   - Complete working JWT + session join code

4. **Fix callback issues** → [troubleshooting/windows-message-loop.md](troubleshooting/windows-message-loop.md)
   - **CRITICAL**: Why callbacks don't fire without Windows message loop

5. **Implement video** → [examples/video-rendering.md](examples/video-rendering.md)
   - Canvas API (SDK-rendered) vs Raw Data Pipe

6. **Troubleshoot any issues** → [troubleshooting/common-issues.md](troubleshooting/common-issues.md)
   - Quick diagnostic checklist
   - Error code tables

---

## Documentation Structure

```
zoom-video-sdk/windows/
├── SKILL.md                           # Main skill overview
├── INDEX.md                           # This file - navigation guide
│
├── concepts/                          # Core architectural patterns
│   ├── sdk-architecture-pattern.md   # Universal formula for ANY feature
│   ├── singleton-hierarchy.md        # 5-level navigation guide
│   └── canvas-vs-raw-data.md         # SDK-rendered vs self-rendered choice
│
├── examples/                          # Complete working code
│   ├── session-join-pattern.md       # JWT auth + session join
│   ├── video-rendering.md            # Canvas API video display
│   └── raw-video-capture.md          # YUV420 raw frame capture
│
├── troubleshooting/                   # Problem solving guides
│   ├── windows-message-loop.md       # CRITICAL - Why callbacks fail
│   ├── build-errors.md               # Header dependency fixes
│   └── common-issues.md              # Quick diagnostic workflow
│
└── references/                        # Reference documentation
    ├── windows-reference.md           # API hierarchy, methods, error codes
    └── delegate-methods.md            # All 60+ callback methods
```

---

## By Use Case

### I want to build a video app
1. [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) - Understand the pattern
2. [Session Join Pattern](examples/session-join-pattern.md) - Join sessions
3. [Video Rendering](examples/video-rendering.md) - Display video
4. [Windows Message Loop](troubleshooting/windows-message-loop.md) - Fix callback issues

### I'm getting build errors
1. [Build Errors Guide](troubleshooting/build-errors.md) - SDK header dependencies
2. [Delegate Methods](references/delegate-methods.md) - Abstract class errors
3. [Common Issues](troubleshooting/common-issues.md) - Linker errors

### I'm getting runtime errors
1. [Windows Message Loop](troubleshooting/windows-message-loop.md) - Callbacks not firing
2. [Common Issues](troubleshooting/common-issues.md) - Error code tables

### I want to capture raw video/audio
1. [Canvas vs Raw Data](concepts/canvas-vs-raw-data.md) - Choose your approach
2. [Raw Video Capture](examples/raw-video-capture.md) - YUV420 frame capture
3. [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) - Subscription pattern

### I want to implement a specific feature
1. [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) - **START HERE!**
2. [Singleton Hierarchy](concepts/singleton-hierarchy.md) - Navigate to the feature
3. [API Reference](references/windows-reference.md) - Method signatures

---

## Most Critical Documents

### 1. SDK Architecture Pattern (MASTER DOCUMENT)
**[concepts/sdk-architecture-pattern.md](concepts/sdk-architecture-pattern.md)**

The universal 3-step pattern:
1. Get singleton (SDK, helpers, session, users)
2. Implement delegate (event callbacks)
3. Subscribe and use

### 2. Windows Message Loop (MOST COMMON ISSUE)
**[troubleshooting/windows-message-loop.md](troubleshooting/windows-message-loop.md)**

99% of "callbacks not firing" issues are caused by missing Windows message loop.

### 3. Singleton Hierarchy (NAVIGATION MAP)
**[concepts/singleton-hierarchy.md](concepts/singleton-hierarchy.md)**

5-level deep navigation showing how to reach every feature.

---

## Key Learnings

### Critical Discoveries:

1. **Windows Message Loop is MANDATORY**
   - SDK uses Windows message pump for callbacks
   - Without it, callbacks are queued but never fire
   - See: [Windows Message Loop Guide](troubleshooting/windows-message-loop.md)

2. **Subscribe in onUserVideoStatusChanged, NOT onUserJoin**
   - Video may not be ready when user joins
   - Wait for video status change callback
   - See: [Video Rendering](examples/video-rendering.md)

3. **Two Rendering Paths**
   - Canvas API: SDK renders to your HWND (recommended)
   - Raw Data Pipe: You receive YUV frames (advanced)
   - See: [Canvas vs Raw Data](concepts/canvas-vs-raw-data.md)

4. **Helpers Control YOUR Streams Only**
   - `videoHelper->startVideo()` starts YOUR camera
   - To see others, subscribe to their Canvas/Pipe
   - See: [Singleton Hierarchy](concepts/singleton-hierarchy.md)

---

## Quick Reference

### "My code won't compile"
→ [Build Errors Guide](troubleshooting/build-errors.md)

### "Callbacks never fire"
→ [Windows Message Loop](troubleshooting/windows-message-loop.md)

### "Video subscription returns error 2"
→ [Video Rendering](examples/video-rendering.md) - Subscribe in onUserVideoStatusChanged

### "Abstract class error"
→ [Delegate Methods](references/delegate-methods.md)

### "How do I implement [feature]?"
→ [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md)

### "How do I navigate to [controller]?"
→ [Singleton Hierarchy](concepts/singleton-hierarchy.md)

### "What error code means what?"
→ [Common Issues](troubleshooting/common-issues.md)

---

## Document Version

Based on **Zoom Video SDK for Windows v2.x**

---

**Happy coding!**

Remember: The [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) is your key to unlocking the entire SDK. Read it first!

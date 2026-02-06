# Zoom Windows Meeting SDK - Complete Documentation Index

## 🚀 Quick Start Path

**If you're new to the SDK, follow this order:**

1. **Read the architecture pattern** → [concepts/sdk-architecture-pattern.md](concepts/sdk-architecture-pattern.md)
   - This teaches you the universal formula that applies to ALL features
   - Once you understand this, you can implement any feature by reading the `.h` files

2. **Fix build errors** → [troubleshooting/build-errors.md](troubleshooting/build-errors.md)
   - SDK header dependencies issues
   - Required include order

3. **Implement authentication** → [examples/authentication-pattern.md](examples/authentication-pattern.md)
   - Complete working JWT authentication code

4. **Fix callback issues** → [troubleshooting/windows-message-loop.md](troubleshooting/windows-message-loop.md)
   - **CRITICAL**: Why callbacks don't fire without Windows message loop
   - This was the hardest issue to diagnose!

5. **Implement virtual methods** → [references/interface-methods.md](references/interface-methods.md)
   - Complete lists of all required methods
   - How to avoid abstract class errors

6. **Capture video (optional)** → [examples/raw-video-capture.md](examples/raw-video-capture.md)
   - YUV420 format explained
   - Complete raw data capture workflow

7. **Troubleshoot any issues** → [troubleshooting/common-issues.md](troubleshooting/common-issues.md)
   - Quick diagnostic checklist
   - Error code tables
   - "If you see X, do Y" reference

---

## 📂 Documentation Structure

```
zoom-meeting-sdk/windows/
├── SKILL.md                           # Main skill overview
├── INDEX.md                           # This file - navigation guide
│
├── concepts/                          # Core architectural patterns
│   └── sdk-architecture-pattern.md   # ⭐ THE MOST IMPORTANT DOC
│                                      # Universal formula for ANY feature
│
├── examples/                          # Complete working code
│   ├── authentication-pattern.md     # JWT auth with full code
│   └── raw-video-capture.md          # Video capture with YUV420 details
│
├── troubleshooting/                   # Problem solving guides
│   ├── windows-message-loop.md       # ⚠️ CRITICAL - Why callbacks fail
│   ├── build-errors.md               # Header dependency fixes
│   └── common-issues.md              # Quick diagnostic workflow
│
└── references/                        # Reference documentation
    ├── interface-methods.md           # Required virtual methods
    ├── windows-reference.md           # Platform setup
    ├── authorization.md               # JWT generation
    ├── bot-authentication.md          # Bot token types
    ├── breakout-rooms.md              # Breakout room features
    └── ai-companion.md                # AI Companion features
```

---

## 🎯 By Use Case

### I want to build a meeting bot
1. [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) - Understand the pattern
2. [Authentication Pattern](examples/authentication-pattern.md) - Join meetings
3. [Windows Message Loop](troubleshooting/windows-message-loop.md) - Fix callback issues
4. [Interface Methods](references/interface-methods.md) - Implement callbacks

### I'm getting build errors
1. [Build Errors Guide](troubleshooting/build-errors.md) - SDK header dependencies
2. [Interface Methods](references/interface-methods.md) - Abstract class errors
3. [Common Issues](troubleshooting/common-issues.md) - Linker errors

### I'm getting runtime errors
1. [Windows Message Loop](troubleshooting/windows-message-loop.md) - Callbacks not firing
2. [Authentication Pattern](examples/authentication-pattern.md) - Auth timeout
3. [Common Issues](troubleshooting/common-issues.md) - Error code tables

### I want to capture video/audio
1. [Raw Video Capture](examples/raw-video-capture.md) - Complete video workflow
2. [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) - Controller pattern
3. [Common Issues](troubleshooting/common-issues.md) - No frames received

### I want to implement a specific feature
1. [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) - **START HERE!**
2. Find the controller in `SDK/x64/h/meeting_service_interface.h`
3. Find the header in `SDK/x64/h/meeting_service_components/`
4. Follow the universal pattern: Get controller → Implement listener → Use methods

### I want to understand the SDK architecture
1. [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) - Complete architecture overview
2. [Interface Methods](references/interface-methods.md) - Event listener pattern
3. [Authentication Pattern](examples/authentication-pattern.md) - Service pattern

---

## 🔥 Most Critical Documents

### 1. SDK Architecture Pattern (⭐ MASTER DOCUMENT)
**[concepts/sdk-architecture-pattern.md](concepts/sdk-architecture-pattern.md)**

This is THE most important document. It teaches the universal 3-step pattern:
1. Get controller (singleton pattern)
2. Implement event listener (observer pattern)
3. Register and use

Once you understand this pattern, you can implement **any of the 35+ features** by just reading the SDK headers.

**Key insight**: The Zoom SDK follows a perfectly consistent architecture. Every feature works the same way.

---

### 2. Windows Message Loop (⚠️ MOST COMMON ISSUE)
**[troubleshooting/windows-message-loop.md](troubleshooting/windows-message-loop.md)**

99% of "callbacks not firing" issues are caused by missing Windows message loop. This document explains:
- Why SDK requires `PeekMessage()` loop
- How to implement it correctly
- How to diagnose callback issues

**This was the hardest bug to find during development** (took ~2 hours).

---

### 3. Build Errors Guide
**[troubleshooting/build-errors.md](troubleshooting/build-errors.md)**

SDK headers have dependency bugs that cause build errors. This document provides:
- Required include order
- Missing `<cstdint>` fix
- Missing `AudioType` fix
- Missing `YUVRawDataI420` fix

---

## 📊 By Document Type

### Concepts (Why and How)
- [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) - Universal implementation pattern

### Examples (Complete Working Code)
- [Authentication Pattern](examples/authentication-pattern.md) - JWT authentication
- [Raw Video Capture](examples/raw-video-capture.md) - Video capture with YUV420

### Troubleshooting (Problem Solving)
- [Windows Message Loop](troubleshooting/windows-message-loop.md) - Callback issues
- [Build Errors](troubleshooting/build-errors.md) - Compilation issues
- [Common Issues](troubleshooting/common-issues.md) - Quick diagnostics

### References (Lookup Information)
- [Interface Methods](references/interface-methods.md) - Required virtual methods
- [Windows Reference](references/windows-reference.md) - Platform setup
- [Authorization](../references/authorization.md) - JWT generation
- [Bot Authentication](../references/bot-authentication.md) - Bot tokens
- [Breakout Rooms](../references/breakout-rooms.md) - Breakout room API
- [AI Companion](../references/ai-companion.md) - AI features

---

## 💡 Key Learnings from Real Debugging

These documents were created from actual debugging of a non-functional Zoom SDK sample. Here are the key insights:

### Critical Discoveries:

1. **Windows Message Loop is MANDATORY** (not optional)
   - SDK uses Windows message pump for callbacks
   - Without it, callbacks are queued but never fire
   - Manifests as "authentication timeout" even with valid JWT
   - See: [Windows Message Loop Guide](troubleshooting/windows-message-loop.md)

2. **SDK Headers Have Dependency Bugs**
   - Missing `#include <cstdint>` in SDK headers
   - `meeting_participants_ctrl_interface.h` doesn't include `meeting_audio_interface.h`
   - `rawdata_renderer_interface.h` only forward-declares `YUVRawDataI420`
   - See: [Build Errors Guide](troubleshooting/build-errors.md)

3. **Include Order is CRITICAL**
   - `<windows.h>` must be FIRST
   - `<cstdint>` must be SECOND
   - Then SDK headers in specific order
   - See: [Build Errors Guide](troubleshooting/build-errors.md)

4. **ALL Virtual Methods Must Be Implemented**
   - Including WIN32-conditional methods
   - SDK v6.7.2 requires 6 auth methods + 9 meeting methods
   - Different versions have different requirements
   - See: [Interface Methods Guide](references/interface-methods.md)

5. **The Architecture is Beautifully Consistent**
   - Every feature follows the same 3-step pattern
   - Controllers are singletons
   - Event listeners use observer pattern
   - Once you learn the pattern, you can implement any feature
   - See: [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md)

---

## 🎓 Learning Path by Skill Level

### Beginner (Never used Zoom SDK)
1. Read [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) to understand the overall design
2. Follow [Authentication Pattern](examples/authentication-pattern.md) to join your first meeting
3. Reference [Common Issues](troubleshooting/common-issues.md) when you hit problems

### Intermediate (Familiar with SDK basics)
1. Deep dive into [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) - implement multiple features
2. Learn [Raw Video Capture](examples/raw-video-capture.md) for media processing
3. Use [Interface Methods](references/interface-methods.md) as reference

### Advanced (Building production bots)
1. Study [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) - learn to implement ANY feature
2. Master [Windows Message Loop](troubleshooting/windows-message-loop.md) - understand async callback flow
3. Reference SDK headers directly using the universal pattern

---

## 🔍 How to Find What You Need

### "My code won't compile"
→ [Build Errors Guide](troubleshooting/build-errors.md)

### "Authentication times out"
→ [Windows Message Loop](troubleshooting/windows-message-loop.md)

### "Callbacks never fire"
→ [Windows Message Loop](troubleshooting/windows-message-loop.md)

### "Abstract class error"
→ [Interface Methods](references/interface-methods.md)

### "How do I implement [feature]?"
→ [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md)

### "How do I join a meeting?"
→ [Authentication Pattern](examples/authentication-pattern.md)

### "How do I capture video?"
→ [Raw Video Capture](examples/raw-video-capture.md)

### "What error code means what?"
→ [Common Issues](troubleshooting/common-issues.md)

### "How does the SDK work?"
→ [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md)

---

## 📝 Document Version

All documents are based on **Zoom Windows Meeting SDK v6.7.2.26830**.

Different SDK versions may have:
- Different required callback methods
- Different error codes
- Different API behavior

If using a different version, use `grep "= 0" SDK/x64/h/*.h` to verify required methods.

---

## 🤝 Contributing

Found an issue or want to add more examples? These skills documentation files are meant to be living documents that grow with the community's experience.

---

**Happy coding!** 🚀

Remember: The [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) is your key to unlocking the entire SDK. Read it first!

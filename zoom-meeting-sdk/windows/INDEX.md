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
│   ├── sdk-architecture-pattern.md   # THE MOST IMPORTANT DOC
│   │                                  # Universal formula for ANY feature
│   ├── singleton-hierarchy.md        # Navigation guide for SDK services
│   │                                  # 4-level deep service tree, when/how
│   ├── custom-ui-architecture.md     # How Custom UI rendering works
│   │                                  # Child HWNDs, D3D, layout, events
│   └── custom-ui-vs-raw-data.md      # SDK-rendered vs self-rendered
│                                      # Decision guide for Custom UI approach
│
├── examples/                          # Complete working code
│   ├── authentication-pattern.md     # JWT auth with full code
│   ├── raw-video-capture.md          # Video capture with YUV420 details
│   │                                  # Recording vs Streaming, permissions
│   ├── custom-ui-video-rendering.md  # Custom UI with video container
│   │                                  # Active speaker + gallery layout
│   ├── breakout-rooms.md             # Complete breakout room guide
│   │                                  # 5 roles, create/manage/join
│   ├── chat.md                       # Send/receive chat messages
│   │                                  # Rich text, threading, file transfer
│   ├── captions-transcription.md     # Live transcription & closed captions
│   │                                  # Multi-language translation
│   ├── local-recording.md            # Local MP4 recording
│   │                                  # Permission flow, encoder monitoring
│   ├── share-raw-data-capture.md     # Screen share raw data capture
│   │                                  # YUV420 frames from shared content
│   └── send-raw-data.md              # Virtual camera/mic/share
│                                      # Send custom video/audio/share
│
├── troubleshooting/                   # Problem solving guides
│   ├── windows-message-loop.md       # CRITICAL - Why callbacks fail
│   ├── build-errors.md               # Header dependency fixes + MSBuild
│   └── common-issues.md              # Quick diagnostic workflow
│
└── references/                        # Reference documentation
    ├── interface-methods.md           # Required virtual methods
    │                                  # Auth(6) + Meeting(9) + CustomUI(13)
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

### I want to build a Custom UI meeting app
1. [Custom UI Architecture](concepts/custom-ui-architecture.md) - How SDK rendering works
2. [SDK-Rendered vs Self-Rendered](concepts/custom-ui-vs-raw-data.md) - Choose your approach
3. [Custom UI Video Rendering](examples/custom-ui-video-rendering.md) - Complete working code
4. [Interface Methods](references/interface-methods.md) - 13 Custom UI virtual methods
5. [Build Errors Guide](troubleshooting/build-errors.md) - MSBuild from git bash

### I want to capture video/audio
1. [Raw Video Capture](examples/raw-video-capture.md) - Complete video workflow
   - Recording vs Streaming approaches
   - Permission requirements (host, OAuth tokens)
   - Audio PCM capture
2. [Share Raw Data Capture](examples/share-raw-data-capture.md) - Screen share capture
   - Subscribe to RAW_DATA_TYPE_SHARE
   - Handle dynamic resolution
3. [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) - Controller pattern
4. [Common Issues](troubleshooting/common-issues.md) - No frames received

### I want to use breakout rooms
1. [Breakout Rooms Guide](examples/breakout-rooms.md) - Complete breakout room workflow
   - 5 roles: Creator, Admin, Data, Assistant, Attendee
   - Create, configure, manage, join/leave rooms
2. [Common Issues](troubleshooting/common-issues.md) - Breakout room error codes

### I want to implement chat
1. [Chat Guide](examples/chat.md) - Send/receive messages
   - Rich text formatting (bold, italic, links)
   - Private messages and threading
   - File transfer events

### I want to use live transcription
1. [Captions & Transcription Guide](examples/captions-transcription.md) - Live transcription
   - Automatic speech-to-text
   - Multi-language translation
   - Manual closed captions (host feature)

### I want to record meetings
1. [Local Recording Guide](examples/local-recording.md) - Local MP4 recording
   - Permission request workflow
   - zTscoder.exe encoder monitoring
   - Gallery view vs active speaker

### I want to implement a specific feature
1. [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) - **START HERE!**
2. Find the controller in `SDK/x64/h/meeting_service_interface.h`
3. Find the header in `SDK/x64/h/meeting_service_components/`
4. Follow the universal pattern: Get controller → Implement listener → Use methods

### I want to understand the SDK architecture
1. [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) - Complete architecture overview
2. [Singleton Hierarchy](concepts/singleton-hierarchy.md) - Navigate the service tree (4 levels)
3. [Interface Methods](references/interface-methods.md) - Event listener pattern
4. [Authentication Pattern](examples/authentication-pattern.md) - Service pattern

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
- [Singleton Hierarchy](concepts/singleton-hierarchy.md) - Navigation guide for SDK services (4 levels deep)

### Examples (Complete Working Code)
- [Authentication Pattern](examples/authentication-pattern.md) - JWT authentication
- [Raw Video Capture](examples/raw-video-capture.md) - Video capture with YUV420, recording vs streaming
- [Custom UI Video Rendering](examples/custom-ui-video-rendering.md) - SDK-rendered video containers
- [Breakout Rooms](examples/breakout-rooms.md) - Create, manage, join breakout rooms
- [Chat](examples/chat.md) - Send/receive messages with rich formatting
- [Captions & Transcription](examples/captions-transcription.md) - Live transcription and closed captions
- [Local Recording](examples/local-recording.md) - Local MP4 recording with permission flow
- [Share Raw Data Capture](examples/share-raw-data-capture.md) - Screen share raw data capture
- [Send Raw Data](examples/send-raw-data.md) - Virtual camera, microphone, and share

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
→ [Common Issues](troubleshooting/common-issues.md) - Comprehensive error code tables (SDKERR, AUTHRET, Login, BO, Phone, OBF)

### "How do I use breakout rooms?"
→ [Breakout Rooms Guide](examples/breakout-rooms.md)

### "How does the SDK work?"
→ [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md)

### "How do I navigate to a specific controller/feature?"
→ [Singleton Hierarchy](concepts/singleton-hierarchy.md)

### "How do I send/receive chat messages?"
→ [Chat Guide](examples/chat.md)

### "How do I use live transcription?"
→ [Captions & Transcription Guide](examples/captions-transcription.md)

### "How do I record locally?"
→ [Local Recording Guide](examples/local-recording.md)

### "How do I capture screen share?"
→ [Share Raw Data Capture](examples/share-raw-data-capture.md)

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

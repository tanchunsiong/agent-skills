# Zoom Video SDK Linux - Complete Documentation Index

## Quick Start Path

**If you're new to the SDK, follow this order:**

1. **Read the architecture pattern** → [concepts/sdk-architecture-pattern.md](concepts/sdk-architecture-pattern.md)
   - Universal formula: Singleton → Delegate → Subscribe
   - Once you understand this, you can implement any feature

2. **Understand Linux specifics** → [concepts/raw-data-vs-canvas.md](concepts/raw-data-vs-canvas.md)
   - **CRITICAL**: Linux has NO Canvas API - raw data ONLY

3. **Implement session join** → [examples/session-join-pattern.md](examples/session-join-pattern.md)
   - Complete working JWT + session join code

4. **Setup environment** → [troubleshooting/pulseaudio-setup.md](troubleshooting/pulseaudio-setup.md)
   - PulseAudio configuration (required for audio)
   - [troubleshooting/qt-dependencies.md](troubleshooting/qt-dependencies.md)
   - Qt5 library setup (bundled with SDK)

5. **Implement features** → Choose from examples below

---

## Documentation Structure

```
zoom-video-sdk/linux/
├── SKILL.md                          # Main skill overview
├── INDEX.md                          # This file - navigation guide
├── linux.md                          # Platform summary
│
├── concepts/                         # Core architectural patterns
│   ├── sdk-architecture-pattern.md  # Universal formula for ANY feature
│   ├── singleton-hierarchy.md       # 5-level navigation guide
│   └── raw-data-vs-canvas.md        # Linux-specific: raw data ONLY
│
├── examples/                         # Complete working code
│   ├── session-join-pattern.md      # JWT auth + session join
│   └── command-channel.md           # Command channel with threading
│
├── troubleshooting/                  # Problem solving guides
│   ├── pulseaudio-setup.md          # Audio configuration
│   ├── qt-dependencies.md           # Qt5 library setup
│   ├── build-errors.md              # Common build issues
│   └── common-issues.md             # Quick diagnostic workflow
│
└── references/                       # Reference documentation
    └── linux-reference.md           # API hierarchy, methods, error codes
```

---

## By Use Case

### I want to build a headless bot
1. [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) - Understand the pattern
2. [Session Join Pattern](examples/session-join-pattern.md) - Join sessions
3. [PulseAudio Setup](troubleshooting/pulseaudio-setup.md) - Configure audio
4. [Raw Data vs Canvas](concepts/raw-data-vs-canvas.md) - Understand Linux differences

### I'm getting build errors
1. [Build Errors Guide](troubleshooting/build-errors.md) - SDK build issues
2. [Qt Dependencies](troubleshooting/qt-dependencies.md) - Qt5 setup
3. [Common Issues](troubleshooting/common-issues.md) - Quick diagnostics

### I'm getting runtime errors
1. [PulseAudio Setup](troubleshooting/pulseaudio-setup.md) - Audio not working
2. [Qt Dependencies](troubleshooting/qt-dependencies.md) - Library not found
3. [Common Issues](troubleshooting/common-issues.md) - Error code tables

### I want to use command channel
1. [Command Channel](examples/command-channel.md) - Send/receive commands
2. [Common Issues](troubleshooting/common-issues.md) - Threading requirements

### I want to implement a specific feature
1. [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) - **START HERE!**
2. [Singleton Hierarchy](concepts/singleton-hierarchy.md) - Navigate to the feature
3. [API Reference](references/linux-reference.md) - Method signatures

---

## Most Critical Documents

### 1. SDK Architecture Pattern (MASTER DOCUMENT)
**[concepts/sdk-architecture-pattern.md](concepts/sdk-architecture-pattern.md)**

The universal 3-step pattern:
1. Get singleton (SDK, helpers, session, users)
2. Implement delegate (event callbacks)
3. Subscribe and use

### 2. Raw Data vs Canvas (LINUX-SPECIFIC)
**[concepts/raw-data-vs-canvas.md](concepts/raw-data-vs-canvas.md)**

**CRITICAL**: Unlike Windows/Mac, Linux SDK has NO Canvas API. You MUST use raw data pipe.

### 3. PulseAudio Setup (MOST COMMON ISSUE)
**[troubleshooting/pulseaudio-setup.md](troubleshooting/pulseaudio-setup.md)**

Audio requires PulseAudio configuration.

### 4. Qt Dependencies
**[troubleshooting/qt-dependencies.md](troubleshooting/qt-dependencies.md)**

SDK requires bundled Qt5 libraries, NOT system Qt5.

---

## Key Learnings

### Critical Discoveries:

1. **Linux has NO Canvas API**
   - Windows/Mac have Canvas API for SDK-rendered video
   - Linux MUST use Raw Data Pipe
   - See: [Raw Data vs Canvas](concepts/raw-data-vs-canvas.md)

2. **PulseAudio is MANDATORY**
   - SDK requires PulseAudio for raw audio
   - Must configure ~/.config/zoomus.conf
   - See: [PulseAudio Setup](troubleshooting/pulseaudio-setup.md)

3. **Use Bundled Qt5, NOT System Qt5**
   - SDK includes specific Qt5 versions
   - Copy from samples/qt_libs/
   - See: [Qt Dependencies](troubleshooting/qt-dependencies.md)

4. **Helpers Control YOUR Streams Only**
   - `videoHelper->startVideo()` starts YOUR camera
   - To see others, subscribe to their VideoPipe
   - See: [Singleton Hierarchy](concepts/singleton-hierarchy.md)

5. **Virtual Devices for Headless**
   - Docker/headless needs virtual audio speaker/mic
   - Set before joining session
   - See: [Session Join Pattern](examples/session-join-pattern.md)

6. **Always Use Heap Memory Mode**
   ```cpp
   init_params.videoRawDataMemoryMode = ZoomVideoSDKRawDataMemoryModeHeap;
   ```

7. **GLib Main Loop Required**
   - while/sleep loops don't dispatch SDK events
   - Must use g_main_loop_run()
   - See: [Common Issues](troubleshooting/common-issues.md)

8. **All SDK Calls Must Be on Main Thread**
   - Background thread SDK calls return error 2 (Internal_Error)
   - Use g_idle_add() to schedule on GLib main thread
   - See: [Command Channel](examples/command-channel.md)

9. **Command Channel is Session-Scoped**
   - Does NOT span across different sessions
   - Both sender and receiver must be in the same session
   - See: [Command Channel](examples/command-channel.md)

---

## Sample Repositories

- **[raw-recording-sample](https://github.com/zoom/videosdk-linux-raw-recording-sample)** - Official raw data sample
- **[qt-quickstart](https://github.com/tanchunsiong/videosdk-linux-qt-quickstart)** - Qt6 UI integration
- **[gtk-quickstart](https://github.com/tanchunsiong/videosdk-linux-gtk-quickstart)** - GTK3 UI integration

---

## Quick Reference

### "My code won't compile"
→ [Build Errors Guide](troubleshooting/build-errors.md)

### "Audio not working"
→ [PulseAudio Setup](troubleshooting/pulseaudio-setup.md)

### "Library not found"
→ [Qt Dependencies](troubleshooting/qt-dependencies.md)

### "How do I implement [feature]?"
→ [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md)

### "What error code means what?"
→ [Common Issues](troubleshooting/common-issues.md)

---

## Document Version

Based on **Zoom Video SDK for Linux v2.x**

---

**Happy coding!**

Remember: The [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) is your key to unlocking the entire SDK. Read it first!

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
│   ├── screen-share-subscription.md  # View remote screen shares
│   ├── raw-video-capture.md          # YUV420 raw frame capture
│   ├── raw-audio-capture.md          # PCM audio capture
│   ├── send-raw-video.md             # Virtual camera (inject video)
│   ├── send-raw-audio.md             # Virtual mic (inject audio)
│   ├── cloud-recording.md            # Cloud recording control
│   ├── command-channel.md            # Custom command messaging
│   ├── transcription.md              # Live transcription/captions
│   └── dotnet-winforms/              # UI Framework integration
│       └── README.md                 # Win32, WinForms, WPF patterns
│                                     # C++/CLI wrapper patterns
│                                     # Production quality guidelines
│
├── troubleshooting/                   # Problem solving guides
│   ├── windows-message-loop.md       # CRITICAL - Why callbacks fail
│   ├── build-errors.md               # Header dependency fixes
│   └── common-issues.md              # Quick diagnostic workflow
│
└── references/                        # Reference documentation
    ├── windows-reference.md           # API hierarchy, methods, error codes
    ├── delegate-methods.md            # All 80+ callback methods
    └── samples.md                     # Official samples guide
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

### I want to view screen shares
1. [Screen Share Subscription](examples/screen-share-subscription.md) - **DIFFERENT from video!**
2. [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) - Event-driven pattern
3. [Video Rendering](examples/video-rendering.md) - Compare with video subscription

### I want to capture raw video/audio
1. [Canvas vs Raw Data](concepts/canvas-vs-raw-data.md) - Choose your approach
2. [Raw Video Capture](examples/raw-video-capture.md) - YUV420 frame capture
3. [Raw Audio Capture](examples/raw-audio-capture.md) - PCM audio capture
4. [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) - Subscription pattern

### I want to send custom video/audio (virtual camera/mic)
1. [Send Raw Video](examples/send-raw-video.md) - Inject custom video frames
2. [Send Raw Audio](examples/send-raw-audio.md) - Inject custom audio
3. [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) - External source pattern

### I want to record sessions
1. [Cloud Recording](examples/cloud-recording.md) - Start/stop cloud recording
2. [API Reference](references/windows-reference.md) - Recording helper methods

### I want to use live transcription
1. [Transcription](examples/transcription.md) - Enable live captions
2. [Delegate Methods](references/delegate-methods.md) - Transcription callbacks

### I want custom messaging between participants
1. [Command Channel](examples/command-channel.md) - Send custom commands
2. [API Reference](references/windows-reference.md) - Command channel methods

### I want to build a Win32 native app
1. [Win32 Integration](examples/dotnet-winforms/README.md#option-1-win32-native-c---direct-sdk) - Direct SDK + Canvas API
2. [Video Rendering](examples/video-rendering.md) - Canvas API patterns
3. [Production Guidelines](examples/dotnet-winforms/README.md#production-quality-review) - Best practices

### I want to build a WinForms (.NET) app
1. [WinForms Integration](examples/dotnet-winforms/README.md#option-2-winforms-c--ccli-wrapper) - C++/CLI wrapper + Raw Data
2. [C++/CLI Patterns](examples/dotnet-winforms/README.md#ccli-wrapper-patterns-for-net-integration) - gcroot, Finalizer, LockBits
3. [Production Guidelines](examples/dotnet-winforms/README.md#production-quality-review) - IDisposable, thread safety

### I want to build a WPF (.NET) app
1. [WPF Integration](examples/dotnet-winforms/README.md#option-3-wpf-c--ccli-wrapper) - C++/CLI + BitmapSource
2. [Bitmap Conversion](examples/dotnet-winforms/README.md#2-bitmap--bitmapsource-conversion) - Freeze(), Dispatcher
3. [Production Guidelines](examples/dotnet-winforms/README.md#production-quality-review) - Performance optimization

### I want to use C# / .NET Framework (general)
1. [.NET Integration Overview](examples/dotnet-winforms/README.md) - **Complete C++/CLI wrapper guide**
2. [Raw Video Capture](examples/raw-video-capture.md) - YUV→RGB conversion patterns
3. [Session Join Pattern](examples/session-join-pattern.md) - SDK initialization flow

### I want to wrap ANY native C++ library for .NET
1. [C++/CLI Wrapper Patterns](examples/dotnet-winforms/README.md#ccli-wrapper-patterns-for-net-integration) - **Complete 8-pattern guide**
2. [Pattern 1: Basic Structure](examples/dotnet-winforms/README.md#pattern-1-basic-wrapper-structure) - Project setup + class layout
3. [Pattern 3: gcroot Callbacks](examples/dotnet-winforms/README.md#pattern-3-gcrootT-for-nativemanaged-callbacks) - Native→Managed events
4. [Pattern 4: IDisposable](examples/dotnet-winforms/README.md#pattern-4-destructor--finalizer-idisposable) - Cleanup pattern
5. [Common Errors](examples/dotnet-winforms/README.md#common-wrapper-errors) - Troubleshooting

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

5. **UI Framework Integration Differs by Platform**
   - **Win32**: Direct SDK, Canvas API (SDK renders to HWND) - best performance
   - **WinForms**: C++/CLI wrapper, Raw Data Pipe, YUV→Bitmap, InvokeRequired
   - **WPF**: Same wrapper + Bitmap→BitmapSource, Dispatcher, Freeze()
   - See: [UI Framework Integration](examples/dotnet-winforms/README.md)

6. **C++/CLI Wrapper Patterns (for ANY native library → .NET)**
   - `void*` pointers - hide native types from managed headers
   - `gcroot<T^>` - prevent GC from collecting managed references in native code
   - Finalizer + Destructor - `~Class()` and `!Class()` for IDisposable cleanup
   - `pin_ptr` + `Marshal::Copy` - array/buffer conversion
   - `LockBits` - 100x faster than SetPixel for image manipulation
   - Thread marshaling - InvokeRequired (WinForms) / Dispatcher (WPF)
   - See: [C++/CLI Wrapper Guide](examples/dotnet-winforms/README.md#ccli-wrapper-patterns-for-net-integration)

7. **Audio Connection Timing**
   - Set `audioOption.connect = false` during join
   - Call `startAudio()` in `onSessionJoin` callback
   - See: [Production Guidelines](examples/dotnet-winforms/README.md#production-quality-review)

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

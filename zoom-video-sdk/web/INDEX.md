# Zoom Video SDK Web - Complete Documentation Index

## Quick Start Path

**If you're new to the SDK, follow this order:**

1. **Read the architecture pattern** → [concepts/sdk-architecture-pattern.md](concepts/sdk-architecture-pattern.md)
   - Universal formula: Create Client → Init → Join → Get Stream → Use
   - Once you understand this, you can implement any feature

2. **Implement session join** → [examples/session-join-pattern.md](examples/session-join-pattern.md)
   - Complete working JWT + session join code

3. **Listen to events** → [examples/event-handling.md](examples/event-handling.md)
   - **CRITICAL**: The SDK is event-driven, you must listen for events

4. **Implement video** → [examples/video-rendering.md](examples/video-rendering.md)
   - Use attachVideo(), NOT renderVideo()

5. **Troubleshoot any issues** → [troubleshooting/common-issues.md](troubleshooting/common-issues.md)
   - Quick diagnostic checklist
   - Error code tables

---

## Documentation Structure

```
zoom-video-sdk/web/
├── SKILL.md                           # Main skill overview
├── INDEX.md                           # This file - navigation guide
│
├── concepts/                          # Core architectural patterns
│   ├── sdk-architecture-pattern.md   # Universal formula for ANY feature
│   └── singleton-hierarchy.md        # 4-level navigation guide
│
├── examples/                          # Complete working code
│   ├── session-join-pattern.md       # JWT auth + session join
│   ├── video-rendering.md            # attachVideo() patterns
│   ├── screen-share.md               # Send and receive screen shares
│   ├── event-handling.md             # Required events
│   ├── chat.md                       # Chat implementation
│   ├── command-channel.md            # Command channel messaging
│   ├── recording.md                  # Cloud recording control
│   ├── transcription.md              # Live transcription/captions
│   ├── react-hooks.md                # Official @zoom/videosdk-react library
│   └── framework-integrations.md     # Next.js, Vue/Nuxt, ZFG patterns
│
├── troubleshooting/                   # Problem solving guides
│   └── common-issues.md              # Quick diagnostic workflow
│
└── references/                        # Reference documentation
    ├── web-reference.md              # API hierarchy, methods, error codes
    └── events-reference.md           # All event types
```

---

## By Use Case

### I want to build a video app
1. [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) - Understand the pattern
2. [Session Join Pattern](examples/session-join-pattern.md) - Join sessions
3. [Video Rendering](examples/video-rendering.md) - Display video
4. [Event Handling](examples/event-handling.md) - Listen for video events

### I'm getting runtime errors
1. [Common Issues](troubleshooting/common-issues.md) - Error code tables
2. "getMediaStream() is undefined" → Call AFTER join() completes

### I want to receive screen shares
1. [Screen Share](examples/screen-share.md) - startShareView() patterns
2. [Event Handling](examples/event-handling.md) - active-share-change event

### I want to send screen shares
1. [Screen Share](examples/screen-share.md) - startShareScreen() patterns
2. Check isStartShareScreenWithVideoElement() for element type

### I want to use chat
1. [Chat](examples/chat.md) - Send/receive messages
2. getChatClient() for ChatClient access

### I want to record sessions
1. [Recording](examples/recording.md) - Cloud recording (host only)
2. getRecordingClient() for RecordingClient access

### I want to use live transcription
1. [Transcription](examples/transcription.md) - Enable live captions
2. getLiveTranscriptionClient() for LiveTranscriptionClient access

### I want to use command channel
1. [Command Channel](examples/command-channel.md) - Custom signaling between participants
2. Must call getCommandClient() AFTER join()

### I want to implement a specific feature
1. [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) - **START HERE!**
2. [Singleton Hierarchy](concepts/singleton-hierarchy.md) - Navigate to the feature
3. [API Reference](references/web-reference.md) - Method signatures

### I'm using React
1. [React Hooks](examples/react-hooks.md) - Official @zoom/videosdk-react library
2. Provides hooks: useSession, useSessionUsers, useVideoState, useAudioState
3. Pre-built components: VideoPlayerComponent, ScreenSharePlayerComponent

### I'm using Next.js or Vue/Nuxt
1. [Framework Integrations](examples/framework-integrations.md) - SSR considerations
2. Server-side JWT generation patterns
3. Client-side only SDK usage

---

## Most Critical Documents

### 1. SDK Architecture Pattern (MASTER DOCUMENT)
**[concepts/sdk-architecture-pattern.md](concepts/sdk-architecture-pattern.md)**

The universal 5-step pattern:
1. Create client
2. Initialize SDK
3. Join session
4. Get stream
5. Use features + listen to events

### 2. Common Issues (MOST COMMON PROBLEMS)
**[troubleshooting/common-issues.md](troubleshooting/common-issues.md)**

Common issues:
- getMediaStream() returns undefined
- Video not displaying
- renderVideo() deprecated

### 3. Singleton Hierarchy (NAVIGATION MAP)
**[concepts/singleton-hierarchy.md](concepts/singleton-hierarchy.md)**

4-level deep navigation showing how to reach every feature.

---

## Key Learnings

### Critical Discoveries:

1. **getMediaStream() ONLY works after join()**
   - The stream object is not available until session is joined
   - See: [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md)

2. **Use attachVideo() NOT renderVideo()**
   - renderVideo() is deprecated
   - attachVideo() returns a VideoPlayer element to append to DOM
   - See: [Video Rendering](examples/video-rendering.md)

3. **The SDK is Event-Driven**
   - You MUST listen for events to render participant videos
   - key events: peer-video-state-change, user-added, user-removed
   - See: [Event Handling](examples/event-handling.md)

4. **Peer Videos on Mid-Session Join**
   - Existing participants' videos won't auto-render
   - Must manually iterate getAllUser() and attachVideo()
   - See: [Video Rendering](examples/video-rendering.md)

5. **CDN vs NPM**
   - CDN exports as `WebVideoSDK.default`, not `ZoomVideo`
   - Some networks/ad blockers may block `source.zoom.us` - allowlist or use a permitted fallback strategy
   - See: [Session Join Pattern](examples/session-join-pattern.md)

6. **SharedArrayBuffer for HD**
   - Required for 720p/1080p video
   - Need COOP/COEP headers on server
   - Check with `stream.isSupportHDVideo()`

7. **Screen Share Element Type**
   - Check `isStartShareScreenWithVideoElement()` for correct element type
   - See: [Screen Share](examples/screen-share.md)

8. **Command Channel Setup Order**
   - Must call getCommandClient() AFTER client.join()
   - Register listeners AFTER join, not before
   - Web uses getCommandClient() not getCmdChannel()
   - See: [Command Channel](examples/command-channel.md)

9. **Command Channel is Session-Scoped**
   - Does NOT span across different sessions
   - Both sender and receiver must be in the same session

---

## Quick Reference

### "getMediaStream() returns undefined"
→ Call AFTER join() completes

### "Video not showing"
→ [Video Rendering](examples/video-rendering.md) - Use attachVideo(), check events

### "renderVideo() doesn't work"
→ [Video Rendering](examples/video-rendering.md) - Use attachVideo() instead

### "How do I implement [feature]?"
→ [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md)

### "How do I navigate to [client]?"
→ [Singleton Hierarchy](concepts/singleton-hierarchy.md)

### "What error code means what?"
→ [Common Issues](troubleshooting/common-issues.md)

---

## Document Version

Based on **Zoom Video SDK for Web v2.3.x**

---

**Happy coding!**

Remember: The [SDK Architecture Pattern](concepts/sdk-architecture-pattern.md) is your key to unlocking the entire SDK. Read it first!

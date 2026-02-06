# RTMS Skill Learnings

Discoveries, challenges, and lessons learned while building the zoom-rtms skill.

## Key Architectural Discoveries

### 1. Two-Phase WebSocket Design

RTMS uses **two separate WebSocket connections** - this is not obvious from initial documentation:

- **Signaling WebSocket**: Control plane (handshake, heartbeat, start/stop)
- **Media WebSocket**: Data plane (audio, video, transcript, chat, share)

**Why?** Separation of concerns, independent scaling, fault isolation.

### 2. SDK vs Manual Approach

| SDK (`@zoom/rtms`) | Manual WebSocket |
|-------------------|------------------|
| Hides complexity | Full protocol control |
| Automatic reconnection | DIY reconnection |
| Limited customization | Full customization |
| Node.js/Python only | Any language |

**Recommendation**: Use SDK unless you need custom protocol handling or unsupported language.

### 3. Screen Share is SEPARATE from Video

This is a common gotcha:
- Video = msg_type 15, media flag 2
- Screen Share = msg_type 16, media flag 4

You must subscribe to both separately!

## Critical Gotchas

### 1. Webhook Response Timing (Most Common Issue)

**Problem**: Random disconnections, duplicate connections.

**Root Cause**: If webhook handler takes too long, Zoom retries. The retry creates a second connection which kicks out the first (only 1 connection allowed per stream).

**Solution**: 
```javascript
app.post('/webhook', (req, res) => {
  res.status(200).send();  // FIRST! Before any processing
  setImmediate(() => handleEvent(req.body));
});
```

### 2. Heartbeat is Mandatory

Both signaling and media connections require heartbeat responses:
- Receive msg_type 12 -> Respond with msg_type 13
- Signaling timeout: ~60 seconds
- Media timeout: ~30 seconds

Failure to respond = connection closed!

### 3. Session Tracking Required

Must track active sessions to prevent duplicate connections:

```javascript
const activeSessions = new Map();

if (activeSessions.has(streamId)) {
  console.log('Already connected, ignoring');
  return;
}
```

### 4. Node.js Version Requirement

SDK requires Node.js 20.3.0+ (N-API v9/v10). Earlier versions cause segmentation faults.

**Recommended**: Node.js 24 LTS

### 5. Platform Support Limitations

Currently supported:
- darwin-arm64 (Apple Silicon)
- linux-x64

NOT yet supported:
- Windows
- darwin-x64 (Intel Mac)
- linux-arm64

For unsupported platforms, use Manual WebSocket implementation.

## SDK-Specific Issues

### 1. Audio Metadata Missing userId

When using AUDIO_MIXED_STREAM, audio metadata doesn't identify speaker.

**Solution**: Use `onActiveSpeakerEvent` callback for speaker identification.

### 2. Video Params Order Bug

`setVideoParams` ignored when called after `setAudioParams`.

**Workaround**: Call `setVideoParams` BEFORE `setAudioParams`.

### 3. SDK Invalid State

"Invalid status" error on join after quick stop/start.

**Solution**: Retry with 2-second delay.

## Transcript Considerations

### Language Auto-Detection Delay

Auto-detect takes 30 seconds before transcription starts.

**Solution**: Set language explicitly:
```javascript
transcript: {
  content_type: 5,
  language: 9  // English
}
```

## Audio Processing

### Gap-Filled Recording

For continuous playback, fill gaps with silence:
- Detect gaps >= 500ms
- Fill with silent frames (20ms each)
- Audio format: 16kHz, 16-bit, mono

## Production Considerations

### Concurrency Limits

| Tier | Limit |
|------|-------|
| Trial | 5 concurrent connections |
| Production | Up to 2000 (more on request) |

### Geo-Routing

Server URLs contain region codes (sjc, sin, iad, fra, syd). Route to nearest worker for lower latency.

## Documentation Gaps Found

1. **SDK platform support** - Not clearly documented which platforms are supported
2. **Video params order bug** - Not documented, discovered through GitHub issues
3. **Heartbeat timeouts** - Exact timeout values not in official docs
4. **Split vs Unified mode** - Limited documentation on when to use which

## Resources That Helped

1. **rtms-samples** - Best resource, includes RTMSManager library
2. **RTMS_CONNECTION_FLOW.md** - Detailed protocol documentation
3. **GitHub Issues** - Real-world problems and solutions
4. **Arlo Meeting Assistant** - Production-quality example

## Future Improvements

1. [ ] Add support for Video SDK RTMS (session.rtms_started)
2. [ ] Add examples for other products (webinars, contact center, phone)
3. [ ] Add production scaling patterns (when requested)
4. [ ] Add Windows platform manual WebSocket examples
5. [ ] Add more AI integration patterns (Azure, Google, etc.)

## Questions for Review

1. Should we include more language-specific examples (Python, C++)?
2. Should we document production scaling architecture?
3. Are there other common use cases to add?

---

*Last updated: February 2026*

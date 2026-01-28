# Fix RTMS Protocol Patterns

## Context

### Original Request
Fix 23 RTMS use case files that have incorrect WebSocket message parsing patterns.

### Interview Summary
**Key Discussions**:
- User wants to fix files that use fabricated binary byte-prefix format (0x01, 0x02, 0x03, 0x04)
- User wants to fix files that use fabricated HTTP auth headers (X-Zoom-RTMS-*)
- User wants to fix files that use fabricated string msg_types ('SIGNALING', 'AUTH')

**Research Findings**:
- Real RTMS protocol uses JSON messages with numeric msg_type fields
- msg_type 12 = keep-alive request (server→client), 13 = keep-alive response
- msg_type 14 = audio, 15 = video, 16 = screen share, 17 = transcript, 18 = chat
- Audio/video content is base64-encoded in `msg.content` field
- Two-phase WebSocket: signaling (msg_type 1→2) then media (msg_type 3→4→7)

---

## Work Objectives

### Core Objective
Fix 23 files to use correct RTMS JSON protocol instead of fabricated binary/header patterns.

### Concrete Deliverables
- 19 files with binary format fixed to use JSON msg_type parsing
- 4 files with auth headers fixed to use correct two-phase WebSocket protocol

### Definition of Done
- [ ] `grep -l "0x01\|0x02\|0x03\|0x04" *.md` returns 0 files
- [ ] `grep -l "X-Zoom-RTMS" *.md` returns 0 files
- [ ] `grep -l "msg_type.*SIGNALING\|action.*AUTH" *.md` returns 0 files

### Must Have
- Keep-alive handling (msg_type 12→13) in all files
- Base64 decoding for audio/video content
- Correct two-phase connection flow in connection tutorial files

### Must NOT Have (Guardrails)
- Do NOT change core processing logic (audio analysis, NLP, video decoding)
- Do NOT rewrite entire files — surgical fixes only
- Do NOT break Python examples while fixing JS or vice versa

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: NO (these are markdown documentation files)
- **User wants tests**: Manual verification via grep
- **QA approach**: Manual verification with grep commands

---

## Task Flow

```
Task 1 (fix binary batch 1) → Task 3 (verify)
Task 2 (fix binary batch 2) → Task 3 (verify)
Task 4 (fix auth headers)   → Task 3 (verify)
```

## Parallelization

| Group | Tasks | Reason |
|-------|-------|--------|
| A | 1, 2, 4 | Independent file sets |

| Task | Depends On | Reason |
|------|------------|--------|
| 3 | 1, 2, 4 | Verification after all fixes |

---

## TODOs

- [ ] 1. Fix binary format in 10 audio files

  **What to do**:
  In each file, find the binary parsing pattern and replace with JSON msg_type parsing.
  
  Pattern to find (JavaScript):
  ```javascript
  const type = data[0];
  if (type === 0x01) {
    const audioData = data.slice(1);
  ```
  
  Replace with:
  ```javascript
  const msg = JSON.parse(data.toString());
  if (msg.msg_type === 12) { ws.send(JSON.stringify({ msg_type: 13, timestamp: msg.timestamp })); return; }
  if (msg.msg_type === 14) {
    const audioData = Buffer.from(msg.content, 'base64');
  ```
  
  Pattern to find (Python):
  ```python
  msg_type = data[0]
  if msg_type == 0x01:
    audio_data = data[1:]
  ```
  
  Replace with:
  ```python
  import base64
  msg = json.loads(data)
  if msg['msg_type'] == 12: ws.send(json.dumps({"msg_type": 13, "timestamp": msg["timestamp"]}))
  if msg['msg_type'] == 14:
    audio_data = base64.b64decode(msg['content'])
  ```
  
  **Files** (in /home/dreamtcs/zoom-developer-platform/zoom-platform/use-cases/):
  1. rtms-audio-buffer-management.md
  2. rtms-audio-export-wav.md
  3. rtms-audio-level-monitoring.md
  4. rtms-audio-noise-reduction.md
  5. rtms-audio-resampling.md
  6. rtms-audio-to-transcription-service.md
  7. rtms-audio-voice-activity-detection.md
  8. rtms-decode-h264-video.md
  9. rtms-decode-pcm-audio.md
  10. rtms-live-captions-display.md

  **Must NOT do**:
  - Do not change audio processing logic (PCM decoding, RMS calculation, etc.)
  - Do not remove existing functionality

  **Parallelizable**: YES (with 2, 4)

  **References**:
  - `/home/dreamtcs/rtms-samples/RTMS_CONNECTION_FLOW.md` - Correct protocol documentation
  - `/home/dreamtcs/rtms-samples/MEDIA_PARAMETERS.md` - Media type constants

  **Acceptance Criteria**:
  - [ ] Each file edited to replace 0x01/0x02/0x03/0x04 patterns with msg_type 14/15/16/17
  - [ ] `grep -c "0x01" [file]` returns 0 for each file
  - [ ] Python examples have `import base64` if using base64.b64decode

  **Commit**: NO (groups with 2, 3, 4)

- [ ] 2. Fix binary format in 9 video/stream files

  **What to do**:
  Same pattern replacement as Task 1, but for video-focused files.
  
  For video (msg_type 15):
  ```javascript
  if (msg.msg_type === 15) {
    const videoData = Buffer.from(msg.content, 'base64');
  ```
  
  For transcript (msg_type 17):
  ```javascript
  if (msg.msg_type === 17) {
    // msg already contains user_name, text, timestamp
    handleTranscript(msg);
  ```

  **Files**:
  1. rtms-receive-audio-stream.md
  2. rtms-receive-transcript-stream.md
  3. rtms-receive-video-stream.md
  4. rtms-subscribe-media-streams.md
  5. rtms-video-export-mp4.md
  6. rtms-video-face-detection.md
  7. rtms-video-frame-extraction.md
  8. rtms-video-thumbnail-generation.md
  9. rtms-screen-share-processing.md

  **Must NOT do**:
  - Do not change H.264 decoding logic
  - Do not change FFmpeg pipeline code

  **Parallelizable**: YES (with 1, 4)

  **References**:
  - `/home/dreamtcs/rtms-samples/RTMS_CONNECTION_FLOW.md:785-855` - Media data handling examples

  **Acceptance Criteria**:
  - [ ] Each file edited to use JSON msg_type parsing
  - [ ] `grep -c "0x01\|0x02\|0x03\|0x04" [file]` returns 0

  **Commit**: NO (groups with 1, 3, 4)

- [ ] 3. Verify all fixes with grep

  **What to do**:
  Run verification commands to confirm all patterns are fixed.

  **Parallelizable**: NO (depends on 1, 2, 4)

  **Acceptance Criteria**:
  - [ ] `grep -l "0x01\|0x02\|0x03\|0x04" /home/dreamtcs/zoom-developer-platform/zoom-platform/use-cases/rtms-*.md | wc -l` returns 0
  - [ ] `grep -l "X-Zoom-RTMS" /home/dreamtcs/zoom-developer-platform/zoom-platform/use-cases/rtms-*.md | wc -l` returns 0  
  - [ ] `grep -l "msg_type.*SIGNALING" /home/dreamtcs/zoom-developer-platform/zoom-platform/use-cases/rtms-*.md | wc -l` returns 0

  **Commit**: YES
  - Message: `fix(rtms): correct WebSocket protocol patterns in 23 use case files`
  - Files: all modified rtms-*.md files
  - Pre-commit: grep verification

- [ ] 4. Fix auth headers in 4 connection files

  **What to do**:
  Replace fabricated auth patterns with correct two-phase WebSocket protocol.
  
  **Pattern to find**:
  ```javascript
  const ws = new WebSocket(serverUrl, {
    headers: {
      'X-Zoom-RTMS-Stream-Id': streamId,
      'X-Zoom-RTMS-Signature': signature
    }
  });
  ```
  
  Or string msg_types:
  ```javascript
  ws.send(JSON.stringify({
    msg_type: 'SIGNALING',
    content: { action: 'AUTH', ... }
  }));
  ```
  
  **Replace with correct two-phase protocol**:
  See `/home/dreamtcs/rtms-samples/RTMS_CONNECTION_FLOW.md` for complete example.
  Key points:
  1. Phase 1: Signaling WebSocket with msg_type 1 (handshake) → receive msg_type 2 (response with media URL)
  2. Phase 2: Media WebSocket with msg_type 3 (handshake) → receive msg_type 4 → send msg_type 7 (start)
  3. HMAC-SHA256 signature: `crypto.createHmac('sha256', clientSecret).update(\`${clientId},${meetingUuid},${streamId}\`).digest('hex')`

  **Files**:
  1. rtms-connect-to-websocket.md - PRIMARY connection tutorial, needs complete rewrite of code sections
  2. rtms-handle-connection-errors.md - Fix auth, keep error handling patterns
  3. rtms-handle-reconnection.md - Fix auth, keep reconnection backoff logic
  4. rtms-multiple-meetings.md - Fix auth AND binary format, keep multi-meeting Map logic

  **Must NOT do**:
  - Do not remove unique teaching content (error codes table, backoff algorithm, etc.)
  - Do not simplify to single-phase WebSocket

  **Parallelizable**: YES (with 1, 2)

  **References**:
  - `/home/dreamtcs/rtms-samples/RTMS_CONNECTION_FLOW.md:265-375` - Signaling connection example
  - `/home/dreamtcs/rtms-samples/RTMS_CONNECTION_FLOW.md:504-560` - Media connection example
  - `/home/dreamtcs/rtms-samples/boilerplate/working_js/index.js` - Working reference

  **Acceptance Criteria**:
  - [ ] `grep -c "X-Zoom-RTMS" [file]` returns 0 for each file
  - [ ] `grep -c "msg_type.*SIGNALING\|action.*AUTH" [file]` returns 0
  - [ ] Connection code shows two-phase (signaling → media) flow

  **Commit**: NO (groups with 1, 2, 3)

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 3 | `fix(rtms): correct WebSocket protocol patterns in 23 use case files` | All modified rtms-*.md | grep verification |

---

## Success Criteria

### Verification Commands
```bash
# Should return 0
grep -l "0x01\|0x02\|0x03\|0x04" /home/dreamtcs/zoom-developer-platform/zoom-platform/use-cases/rtms-*.md | wc -l

# Should return 0
grep -l "X-Zoom-RTMS" /home/dreamtcs/zoom-developer-platform/zoom-platform/use-cases/rtms-*.md | wc -l

# Should return 0
grep -l "msg_type.*SIGNALING\|action.*AUTH\|action.*SUBSCRIBE" /home/dreamtcs/zoom-developer-platform/zoom-platform/use-cases/rtms-*.md | wc -l

# Should return 95
ls /home/dreamtcs/zoom-developer-platform/zoom-platform/use-cases/rtms-*.md | wc -l
```

### Final Checklist
- [ ] All 19 files with binary format are fixed
- [ ] All 4 files with auth headers are fixed
- [ ] No fabricated patterns remain (verified by grep)
- [ ] Core processing logic unchanged in all files
- [ ] Both JS and Python examples fixed in each file

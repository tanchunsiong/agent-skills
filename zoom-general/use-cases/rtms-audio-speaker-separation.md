# Individual Speaker Audio Streams

Receive and manage per-participant audio streams from RTMS for speaker-specific processing.

## Overview

Zoom's Real-Time Media Streams (RTMS) natively provides individual audio streams for each meeting participant alongside a combined mixed stream. Every audio message includes metadata identifying the participant by their `user_id`, so your application always knows exactly who is speaking without any additional processing.

Because RTMS delivers audio on a per-participant basis, there is no need for ML-based speaker diarization or separation techniques. Each participant's audio arrives as a distinct stream that can be independently captured, buffered, and processed. This is a fundamental architectural advantage — speaker identity is resolved at the platform level, not inferred after the fact.

Individual streams unlock a range of use cases: multi-track recording where each speaker gets their own audio file, per-speaker transcription for accurate attribution, real-time voice analysis, and selective audio processing. The mixed stream remains available when you need a single combined output.

## Skills Needed

- **zoom-rtms** - Primary

## Stream Types

| Stream Type | Description | Use Case |
|-------------|-------------|----------|
| Individual | Separate PCM audio per participant, identified by `user_id` | Multi-track recording, per-speaker transcription, voice analysis |
| Mixed | Combined audio from all participants in a single stream | Single-file recording, broadcast, simple playback |

## Implementation

### JavaScript - Individual Audio Manager

```javascript
const WebSocket = require('ws');

class IndividualAudioManager {
  constructor() {
    this.participants = new Map(); // user_id -> participant data
  }

  onAudioMessage(userId, userName, pcmChunk) {
    if (!this.participants.has(userId)) {
      this.participants.set(userId, {
        name: userName,
        chunks: [],
        chunkCount: 0,
        totalBytes: 0,
        startTime: Date.now(),
      });
    }

    const participant = this.participants.get(userId);
    participant.chunks.push(pcmChunk);
    participant.chunkCount += 1;
    participant.totalBytes += pcmChunk.length;
  }

  getParticipantAudio(userId) {
    const participant = this.participants.get(userId);
    if (!participant) return null;

    const durationMs = Date.now() - participant.startTime;
    return {
      name: participant.name,
      audio: Buffer.concat(participant.chunks),
      chunkCount: participant.chunkCount,
      totalBytes: participant.totalBytes,
      durationSeconds: (durationMs / 1000).toFixed(1),
    };
  }

  getActiveParticipants() {
    const result = [];
    for (const [userId, data] of this.participants) {
      result.push({
        userId,
        name: data.name,
        chunkCount: data.chunkCount,
        totalBytes: data.totalBytes,
        durationSeconds: ((Date.now() - data.startTime) / 1000).toFixed(1),
      });
    }
    return result;
  }

  exportAllTracks() {
    const tracks = {};
    for (const [userId, data] of this.participants) {
      tracks[userId] = {
        name: data.name,
        audio: Buffer.concat(data.chunks),
        totalBytes: data.totalBytes,
        chunkCount: data.chunkCount,
      };
    }
    return tracks;
  }
}

// RTMS WebSocket integration
const manager = new IndividualAudioManager();
const ws = new WebSocket(rtmsWebSocketUrl);

ws.on('message', (message) => {
  const parsed = JSON.parse(message);

  if (parsed.type === 'audio' && parsed.content.user_id) {
    const pcmChunk = Buffer.from(parsed.content.data, 'base64');
    manager.onAudioMessage(
      parsed.content.user_id,
      parsed.content.user_name,
      pcmChunk
    );
  }
});

ws.on('close', () => {
  console.log('Active participants:', manager.getActiveParticipants());
  const tracks = manager.exportAllTracks();
  for (const [userId, track] of Object.entries(tracks)) {
    console.log(`${track.name}: ${track.totalBytes} bytes, ${track.chunkCount} chunks`);
  }
});
```

### Python - Individual Audio Manager

```python
from __future__ import annotations

import asyncio
import base64
import json
import time
from dataclasses import dataclass, field

import websockets


@dataclass
class ParticipantStream:
    name: str
    chunks: list[bytes] = field(default_factory=list)
    chunk_count: int = 0
    total_bytes: int = 0
    start_time: float = field(default_factory=time.time)

    @property
    def duration_seconds(self) -> float:
        return round(time.time() - self.start_time, 1)


class IndividualAudioManager:
    def __init__(self) -> None:
        self.participants: dict[str, ParticipantStream] = {}

    def on_audio_message(self, user_id: str, user_name: str, pcm_chunk: bytes) -> None:
        if user_id not in self.participants:
            self.participants[user_id] = ParticipantStream(name=user_name)

        stream = self.participants[user_id]
        stream.chunks.append(pcm_chunk)
        stream.chunk_count += 1
        stream.total_bytes += len(pcm_chunk)

    def get_participant_audio(self, user_id: str) -> dict | None:
        stream = self.participants.get(user_id)
        if stream is None:
            return None

        return {
            "name": stream.name,
            "audio": b"".join(stream.chunks),
            "chunk_count": stream.chunk_count,
            "total_bytes": stream.total_bytes,
            "duration_seconds": stream.duration_seconds,
        }

    def get_active_participants(self) -> list[dict]:
        return [
            {
                "user_id": uid,
                "name": s.name,
                "chunk_count": s.chunk_count,
                "total_bytes": s.total_bytes,
                "duration_seconds": s.duration_seconds,
            }
            for uid, s in self.participants.items()
        ]

    def export_all_tracks(self) -> dict[str, dict]:
        return {
            uid: {
                "name": s.name,
                "audio": b"".join(s.chunks),
                "total_bytes": s.total_bytes,
                "chunk_count": s.chunk_count,
            }
            for uid, s in self.participants.items()
        }


# Async RTMS WebSocket integration
async def connect_rtms(ws_url: str) -> None:
    manager = IndividualAudioManager()

    async with websockets.connect(ws_url) as ws:
        async for raw_message in ws:
            message = json.loads(raw_message)

            if message.get("type") == "audio" and message["content"].get("user_id"):
                pcm_chunk = base64.b64decode(message["content"]["data"])
                manager.on_audio_message(
                    user_id=message["content"]["user_id"],
                    user_name=message["content"]["user_name"],
                    pcm_chunk=pcm_chunk,
                )

    print("Active participants:", manager.get_active_participants())
    tracks = manager.export_all_tracks()
    for user_id, track in tracks.items():
        print(f"{track['name']}: {track['total_bytes']} bytes, {track['chunk_count']} chunks")
```

## Resources

- **RTMS documentation**: https://developers.zoom.us/docs/rtms/

# Receive Transcript Stream

Receive real-time transcription data from RTMS.

## Overview

RTMS provides live transcription as JSON messages with speaker attribution and timestamps.

## Skills Needed

- **zoom-rtms** - Primary

## Transcript Format

```json
{
  "type": "transcript",
  "data": {
    "user_id": "participant_123",
    "user_name": "John Doe",
    "text": "Hello, this is the transcribed text.",
    "timestamp": 1704067200000,
    "is_final": true,
    "language": "en-US"
  }
}
```

## Implementation

### JavaScript

```javascript
class TranscriptReceiver {
  constructor(options = {}) {
    this.transcripts = [];
    this.partialTranscript = new Map(); // Per-speaker partial
    this.onTranscript = options.onTranscript;
    this.onPartial = options.onPartial;
    this.onFinal = options.onFinal;
  }
  
  handleMessage(data) {
     const msgType = data[0];
     
     if (msgType === 17) {
       // msg_type 17: JSON transcript object
       const transcript = JSON.parse(data.slice(1).toString());
       this.processTranscript(transcript);
     } else if (msgType === 13) {
       // msg_type 13: Keep-alive ping
       // No action needed, connection is alive
     }
   }
  
  processTranscript(transcript) {
    const { user_id, user_name, text, timestamp, is_final } = transcript.data;
    
    if (is_final) {
      // Final transcript segment
      const segment = {
        speakerId: user_id,
        speakerName: user_name,
        text: text,
        timestamp: timestamp,
        isFinal: true
      };
      
      this.transcripts.push(segment);
      this.partialTranscript.delete(user_id);
      
      this.onFinal?.(segment);
      this.onTranscript?.(segment);
      
    } else {
      // Partial/interim transcript
      this.partialTranscript.set(user_id, {
        speakerId: user_id,
        speakerName: user_name,
        text: text,
        timestamp: timestamp,
        isFinal: false
      });
      
      this.onPartial?.({
        speakerId: user_id,
        speakerName: user_name,
        text: text
      });
    }
  }
  
  getFullTranscript() {
    return this.transcripts
      .sort((a, b) => a.timestamp - b.timestamp)
      .map(t => `[${t.speakerName}]: ${t.text}`)
      .join('\n');
  }
  
  getTranscriptBySpeaker(speakerId) {
    return this.transcripts.filter(t => t.speakerId === speakerId);
  }
  
  getSpeakers() {
    const speakers = new Map();
    for (const t of this.transcripts) {
      if (!speakers.has(t.speakerId)) {
        speakers.set(t.speakerId, {
          id: t.speakerId,
          name: t.speakerName,
          segments: 0,
          wordCount: 0
        });
      }
      const speaker = speakers.get(t.speakerId);
      speaker.segments++;
      speaker.wordCount += t.text.split(/\s+/).length;
    }
    return Array.from(speakers.values());
  }
  
  getCurrentPartial(speakerId) {
    return this.partialTranscript.get(speakerId);
  }
  
  clear() {
    this.transcripts = [];
    this.partialTranscript.clear();
  }
}

// Usage
const receiver = new TranscriptReceiver({
  onFinal: (segment) => {
    console.log(`[${segment.speakerName}]: ${segment.text}`);
  },
  onPartial: (partial) => {
    // Update live caption display
    updateCaption(partial.speakerName, partial.text);
  }
});

ws.on('message', (data) => {
  receiver.handleMessage(data);
});

// Get full transcript at end
ws.on('close', () => {
  const transcript = receiver.getFullTranscript();
  console.log('Full transcript:', transcript);
  
  const speakers = receiver.getSpeakers();
  console.log('Speakers:', speakers);
});
```

### Python

```python
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from collections import defaultdict

@dataclass
class TranscriptSegment:
    speaker_id: str
    speaker_name: str
    text: str
    timestamp: int
    is_final: bool

class TranscriptReceiver:
    def __init__(self):
        self.transcripts: List[TranscriptSegment] = []
        self.partial_transcripts: Dict[str, TranscriptSegment] = {}
        
        self.on_transcript: Optional[Callable] = None
        self.on_partial: Optional[Callable] = None
        self.on_final: Optional[Callable] = None
    
     def handle_message(self, data: bytes):
         msg_type = data[0]
         
         if msg_type == 17:
             # msg_type 17: JSON transcript object
             transcript = json.loads(data[1:].decode())
             self.process_transcript(transcript)
         elif msg_type == 13:
             # msg_type 13: Keep-alive ping
             # No action needed, connection is alive
             pass
    
    def process_transcript(self, transcript: dict):
        data = transcript.get('data', transcript)
        
        segment = TranscriptSegment(
            speaker_id=data.get('user_id', ''),
            speaker_name=data.get('user_name', 'Unknown'),
            text=data.get('text', ''),
            timestamp=data.get('timestamp', 0),
            is_final=data.get('is_final', False)
        )
        
        if segment.is_final:
            self.transcripts.append(segment)
            self.partial_transcripts.pop(segment.speaker_id, None)
            
            if self.on_final:
                self.on_final(segment)
            if self.on_transcript:
                self.on_transcript(segment)
        else:
            self.partial_transcripts[segment.speaker_id] = segment
            
            if self.on_partial:
                self.on_partial(segment)
    
    def get_full_transcript(self) -> str:
        sorted_transcripts = sorted(self.transcripts, key=lambda t: t.timestamp)
        return '\n'.join(
            f"[{t.speaker_name}]: {t.text}"
            for t in sorted_transcripts
        )
    
    def get_transcript_by_speaker(self, speaker_id: str) -> List[TranscriptSegment]:
        return [t for t in self.transcripts if t.speaker_id == speaker_id]
    
    def get_speakers(self) -> List[dict]:
        speakers = defaultdict(lambda: {'segments': 0, 'word_count': 0})
        
        for t in self.transcripts:
            speakers[t.speaker_id]['id'] = t.speaker_id
            speakers[t.speaker_id]['name'] = t.speaker_name
            speakers[t.speaker_id]['segments'] += 1
            speakers[t.speaker_id]['word_count'] += len(t.text.split())
        
        return list(speakers.values())
    
    def clear(self):
        self.transcripts = []
        self.partial_transcripts = {}

# Usage
receiver = TranscriptReceiver()

def on_final(segment):
    print(f"[{segment.speaker_name}]: {segment.text}")

def on_partial(segment):
    # Update live caption
    update_caption(segment.speaker_name, segment.text)

receiver.on_final = on_final
receiver.on_partial = on_partial

async for message in ws:
    receiver.handle_message(message)

# Get full transcript
print(receiver.get_full_transcript())
```

## Transcript Fields

| Field | Type | Description |
|-------|------|-------------|
| `user_id` | string | Participant ID |
| `user_name` | string | Display name |
| `text` | string | Transcribed text |
| `timestamp` | number | Unix timestamp (ms) |
| `is_final` | boolean | Final vs interim |
| `language` | string | Language code |

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/

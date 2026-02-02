# Active Speaker Video

Track and process the active speaker's video feed.

## Overview

Focus on the current speaker's video for transcription attribution, face analysis, or spotlight recording.

## Skills Needed

- **zoom-rtms** - Primary

## Active Speaker Detection

| Method | Source | Accuracy |
|--------|--------|----------|
| RTMS metadata | Zoom event | 100% |
| Audio level | Audio stream | 90% |
| Face detection | Video analysis | 85% |

## Implementation

### JavaScript

```javascript
class ActiveSpeakerTracker {
  constructor() {
    this.currentSpeaker = null;
    this.speakerHistory = [];
    this.speakerFrames = new Map();
    this.onSpeakerChange = null;
  }
  
  handleRTMSMessage(message) {
    // Check for active speaker metadata
    if (message.type === 'active_speaker') {
      this.updateActiveSpeaker(message.participant_id);
    }
    
    // Store video frames by participant
    if (message.type === 'video' && message.participant_id) {
      this.storeFrame(message.participant_id, message.data);
    }
  }
  
  updateActiveSpeaker(participantId) {
    if (this.currentSpeaker !== participantId) {
      const previous = this.currentSpeaker;
      this.currentSpeaker = participantId;
      
      this.speakerHistory.push({
        speaker: participantId,
        timestamp: Date.now()
      });
      
      this.onSpeakerChange?.({
        current: participantId,
        previous: previous
      });
    }
  }
  
  storeFrame(participantId, frameData) {
    if (!this.speakerFrames.has(participantId)) {
      this.speakerFrames.set(participantId, []);
    }
    
    const frames = this.speakerFrames.get(participantId);
    frames.push({
      data: frameData,
      timestamp: Date.now(),
      isActiveSpeaker: participantId === this.currentSpeaker
    });
    
    // Keep only last 30 frames per participant
    if (frames.length > 30) {
      frames.shift();
    }
  }
  
  getActiveSpeakerFrames() {
    if (!this.currentSpeaker) return [];
    return this.speakerFrames.get(this.currentSpeaker) || [];
  }
  
  getSpeakerStats() {
    const stats = {};
    
    for (let i = 1; i < this.speakerHistory.length; i++) {
      const current = this.speakerHistory[i];
      const previous = this.speakerHistory[i - 1];
      const duration = current.timestamp - previous.timestamp;
      
      if (!stats[previous.speaker]) {
        stats[previous.speaker] = { totalTime: 0, segments: 0 };
      }
      
      stats[previous.speaker].totalTime += duration;
      stats[previous.speaker].segments++;
    }
    
    return stats;
  }
}

// Audio-based active speaker detection
class AudioBasedSpeakerDetector {
  constructor(options = {}) {
    this.threshold = options.threshold || 0.02;
    this.holdTime = options.holdTime || 500; // ms
    this.participantLevels = new Map();
    this.currentSpeaker = null;
    this.lastSpeakerChange = 0;
  }
  
  processAudio(participantId, audioBuffer) {
    const level = this.calculateRMS(audioBuffer);
    
    this.participantLevels.set(participantId, {
      level: level,
      timestamp: Date.now()
    });
    
    // Find loudest participant above threshold
    let loudest = null;
    let loudestLevel = this.threshold;
    
    for (const [id, data] of this.participantLevels) {
      if (data.level > loudestLevel && Date.now() - data.timestamp < 100) {
        loudest = id;
        loudestLevel = data.level;
      }
    }
    
    // Apply hold time
    const now = Date.now();
    if (loudest && (loudest !== this.currentSpeaker || 
        now - this.lastSpeakerChange > this.holdTime)) {
      this.currentSpeaker = loudest;
      this.lastSpeakerChange = now;
      return { changed: true, speaker: loudest };
    }
    
    return { changed: false, speaker: this.currentSpeaker };
  }
  
  calculateRMS(buffer) {
    let sum = 0;
    const samples = buffer.length / 2;
    
    for (let i = 0; i < samples; i++) {
      const sample = buffer.readInt16LE(i * 2) / 32768;
      sum += sample * sample;
    }
    
    return Math.sqrt(sum / samples);
  }
}

// Usage
const tracker = new ActiveSpeakerTracker();
const audioDetector = new AudioBasedSpeakerDetector();

tracker.onSpeakerChange = (change) => {
  console.log(`Active speaker: ${change.current}`);
  // Start recording/highlighting this participant
};

ws.on('message', (data) => {
  const message = parseRTMSMessage(data);
  tracker.handleRTMSMessage(message);
  
  // Fallback to audio detection
  if (message.type === 'audio' && message.participant_id) {
    const result = audioDetector.processAudio(
      message.participant_id,
      message.data
    );
    
    if (result.changed) {
      tracker.updateActiveSpeaker(result.speaker);
    }
  }
});
```

### Python

```python
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Optional, List
import time
import numpy as np

@dataclass
class SpeakerEvent:
    speaker: str
    timestamp: float

class ActiveSpeakerTracker:
    def __init__(self):
        self.current_speaker: Optional[str] = None
        self.speaker_history: List[SpeakerEvent] = []
        self.speaker_frames: Dict[str, List] = defaultdict(list)
        self.on_speaker_change = None
    
    def update_active_speaker(self, participant_id: str):
        if self.current_speaker != participant_id:
            previous = self.current_speaker
            self.current_speaker = participant_id
            
            self.speaker_history.append(SpeakerEvent(
                speaker=participant_id,
                timestamp=time.time()
            ))
            
            if self.on_speaker_change:
                self.on_speaker_change({
                    'current': participant_id,
                    'previous': previous
                })
    
    def store_frame(self, participant_id: str, frame_data: bytes):
        frames = self.speaker_frames[participant_id]
        frames.append({
            'data': frame_data,
            'timestamp': time.time(),
            'is_active': participant_id == self.current_speaker
        })
        
        # Keep only last 30 frames
        if len(frames) > 30:
            frames.pop(0)
    
    def get_speaker_stats(self) -> Dict:
        stats = defaultdict(lambda: {'total_time': 0, 'segments': 0})
        
        for i in range(1, len(self.speaker_history)):
            current = self.speaker_history[i]
            previous = self.speaker_history[i - 1]
            duration = current.timestamp - previous.timestamp
            
            stats[previous.speaker]['total_time'] += duration
            stats[previous.speaker]['segments'] += 1
        
        return dict(stats)

class AudioBasedSpeakerDetector:
    def __init__(self, threshold=0.02, hold_time=0.5):
        self.threshold = threshold
        self.hold_time = hold_time
        self.participant_levels: Dict[str, dict] = {}
        self.current_speaker = None
        self.last_change = 0
    
    def process_audio(self, participant_id: str, audio_buffer: bytes):
        level = self.calculate_rms(audio_buffer)
        now = time.time()
        
        self.participant_levels[participant_id] = {
            'level': level,
            'timestamp': now
        }
        
        # Find loudest above threshold
        loudest = None
        loudest_level = self.threshold
        
        for pid, data in self.participant_levels.items():
            if data['level'] > loudest_level and now - data['timestamp'] < 0.1:
                loudest = pid
                loudest_level = data['level']
        
        # Apply hold time
        if loudest and (loudest != self.current_speaker or 
                       now - self.last_change > self.hold_time):
            self.current_speaker = loudest
            self.last_change = now
            return {'changed': True, 'speaker': loudest}
        
        return {'changed': False, 'speaker': self.current_speaker}
    
    @staticmethod
    def calculate_rms(buffer: bytes) -> float:
        samples = np.frombuffer(buffer, dtype=np.int16).astype(np.float32) / 32768
        return float(np.sqrt(np.mean(samples ** 2)))

# Usage
tracker = ActiveSpeakerTracker()
audio_detector = AudioBasedSpeakerDetector()

def on_change(event):
    print(f"Active speaker: {event['current']}")

tracker.on_speaker_change = on_change

async for message in ws:
    parsed = parse_rtms_message(message)
    
    if parsed['type'] == 'audio' and 'participant_id' in parsed:
        result = audio_detector.process_audio(
            parsed['participant_id'],
            parsed['data']
        )
        if result['changed']:
            tracker.update_active_speaker(result['speaker'])
```

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/

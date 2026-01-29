# Transcript Timestamps

Work with timestamps in RTMS transcripts for synchronization and indexing.

## Overview

Handle transcript timestamps for video sync, navigation, and time-based queries.

## Skills Needed

- **zoom-rtms** - Primary

## Timestamp Operations

| Operation | Use Case |
|-----------|----------|
| Sync with video | Caption timing |
| Time-based search | Jump to moment |
| Duration calculation | Speaking time |
| Timeline generation | Visual index |

## Implementation

### JavaScript

```javascript
class TranscriptTimeline {
  constructor(transcripts, meetingStartTime = null) {
    this.transcripts = transcripts;
    this.startTime = meetingStartTime || (transcripts[0]?.timestamp || 0);
  }
  
  // Get relative time from meeting start
  getRelativeTime(timestamp) {
    return timestamp - this.startTime;
  }
  
  // Format as HH:MM:SS
  formatTime(ms) {
    const totalSeconds = Math.floor(ms / 1000);
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  }
  
  // Get transcript at specific time
  getAtTime(relativeMs) {
    const absoluteTime = this.startTime + relativeMs;
    
    for (let i = this.transcripts.length - 1; i >= 0; i--) {
      if (this.transcripts[i].timestamp <= absoluteTime) {
        return this.transcripts[i];
      }
    }
    return null;
  }
  
  // Get transcripts in time range
  getInRange(startMs, endMs) {
    const absoluteStart = this.startTime + startMs;
    const absoluteEnd = this.startTime + endMs;
    
    return this.transcripts.filter(t =>
      t.timestamp >= absoluteStart && t.timestamp <= absoluteEnd
    );
  }
  
  // Generate timeline with markers
  generateTimeline(intervalMs = 60000) {
    if (this.transcripts.length === 0) return [];
    
    const endTime = this.transcripts[this.transcripts.length - 1].timestamp;
    const duration = endTime - this.startTime;
    const timeline = [];
    
    for (let time = 0; time <= duration; time += intervalMs) {
      const transcriptsInInterval = this.getInRange(time, time + intervalMs);
      
      timeline.push({
        time: time,
        formattedTime: this.formatTime(time),
        transcriptCount: transcriptsInInterval.length,
        speakers: [...new Set(transcriptsInInterval.map(t => t.speakerName))],
        preview: transcriptsInInterval[0]?.text.substring(0, 50) || ''
      });
    }
    
    return timeline;
  }
  
  // Find time of first mention of keyword
  findFirstMention(keyword) {
    const lowerKeyword = keyword.toLowerCase();
    
    for (const t of this.transcripts) {
      if (t.text.toLowerCase().includes(lowerKeyword)) {
        return {
          timestamp: t.timestamp,
          relativeTime: this.getRelativeTime(t.timestamp),
          formattedTime: this.formatTime(this.getRelativeTime(t.timestamp)),
          transcript: t
        };
      }
    }
    return null;
  }
  
  // Get all mentions with timestamps
  findAllMentions(keyword) {
    const lowerKeyword = keyword.toLowerCase();
    
    return this.transcripts
      .filter(t => t.text.toLowerCase().includes(lowerKeyword))
      .map(t => ({
        timestamp: t.timestamp,
        relativeTime: this.getRelativeTime(t.timestamp),
        formattedTime: this.formatTime(this.getRelativeTime(t.timestamp)),
        transcript: t
      }));
  }
  
  // Generate chapter markers based on topic changes
  generateChapters(minGapMs = 60000) {
    const chapters = [];
    let lastTimestamp = this.startTime;
    
    for (const t of this.transcripts) {
      if (t.timestamp - lastTimestamp >= minGapMs) {
        chapters.push({
          time: this.getRelativeTime(t.timestamp),
          formattedTime: this.formatTime(this.getRelativeTime(t.timestamp)),
          speaker: t.speakerName,
          preview: t.text.substring(0, 100)
        });
      }
      lastTimestamp = t.timestamp;
    }
    
    return chapters;
  }
  
  // Sync transcript to video position
  syncToVideo(videoTimeMs) {
    const nearbyTranscripts = [];
    const windowMs = 5000; // 5 second window
    
    for (const t of this.transcripts) {
      const relativeTime = this.getRelativeTime(t.timestamp);
      if (Math.abs(relativeTime - videoTimeMs) <= windowMs) {
        nearbyTranscripts.push({
          ...t,
          relativeTime,
          offset: relativeTime - videoTimeMs
        });
      }
    }
    
    return nearbyTranscripts.sort((a, b) => 
      Math.abs(a.offset) - Math.abs(b.offset)
    );
  }
  
  // Get meeting duration
  getDuration() {
    if (this.transcripts.length === 0) return 0;
    const endTime = this.transcripts[this.transcripts.length - 1].timestamp;
    return endTime - this.startTime;
  }
}

// Usage
const timeline = new TranscriptTimeline(receiver.transcripts);

// Get transcript at 5 minutes
const atFiveMin = timeline.getAtTime(5 * 60 * 1000);

// Find first mention of "budget"
const budgetMention = timeline.findFirstMention('budget');
console.log(`Budget first mentioned at ${budgetMention?.formattedTime}`);

// Generate 1-minute interval timeline
const timelineData = timeline.generateTimeline(60000);

// Sync with video player
videoPlayer.on('timeupdate', () => {
  const currentTime = videoPlayer.currentTime * 1000;
  const synced = timeline.syncToVideo(currentTime);
  updateCaptionDisplay(synced[0]);
});
```

### Python

```python
from typing import List, Optional, Dict
from dataclasses import dataclass

@dataclass
class TimelineMarker:
    time: int
    formatted_time: str
    transcript_count: int
    speakers: List[str]
    preview: str

class TranscriptTimeline:
    def __init__(self, transcripts: List[dict], meeting_start_time: Optional[int] = None):
        self.transcripts = transcripts
        self.start_time = meeting_start_time or (transcripts[0]['timestamp'] if transcripts else 0)
    
    def get_relative_time(self, timestamp: int) -> int:
        return timestamp - self.start_time
    
    def format_time(self, ms: int) -> str:
        total_seconds = ms // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes}:{seconds:02d}"
    
    def get_at_time(self, relative_ms: int) -> Optional[dict]:
        absolute_time = self.start_time + relative_ms
        
        for t in reversed(self.transcripts):
            if t['timestamp'] <= absolute_time:
                return t
        return None
    
    def get_in_range(self, start_ms: int, end_ms: int) -> List[dict]:
        absolute_start = self.start_time + start_ms
        absolute_end = self.start_time + end_ms
        
        return [t for t in self.transcripts 
                if absolute_start <= t['timestamp'] <= absolute_end]
    
    def generate_timeline(self, interval_ms: int = 60000) -> List[TimelineMarker]:
        if not self.transcripts:
            return []
        
        end_time = self.transcripts[-1]['timestamp']
        duration = end_time - self.start_time
        timeline = []
        
        time = 0
        while time <= duration:
            transcripts_in_interval = self.get_in_range(time, time + interval_ms)
            
            timeline.append(TimelineMarker(
                time=time,
                formatted_time=self.format_time(time),
                transcript_count=len(transcripts_in_interval),
                speakers=list(set(t['speaker_name'] for t in transcripts_in_interval)),
                preview=transcripts_in_interval[0]['text'][:50] if transcripts_in_interval else ''
            ))
            
            time += interval_ms
        
        return timeline
    
    def find_first_mention(self, keyword: str) -> Optional[dict]:
        lower_keyword = keyword.lower()
        
        for t in self.transcripts:
            if lower_keyword in t['text'].lower():
                return {
                    'timestamp': t['timestamp'],
                    'relative_time': self.get_relative_time(t['timestamp']),
                    'formatted_time': self.format_time(self.get_relative_time(t['timestamp'])),
                    'transcript': t
                }
        return None
    
    def get_duration(self) -> int:
        if not self.transcripts:
            return 0
        return self.transcripts[-1]['timestamp'] - self.start_time

# Usage
timeline = TranscriptTimeline(receiver.transcripts)

# Get at 5 minutes
at_5min = timeline.get_at_time(5 * 60 * 1000)

# Find mention
mention = timeline.find_first_mention('budget')
if mention:
    print(f"Budget mentioned at {mention['formatted_time']}")

# Generate timeline
markers = timeline.generate_timeline(60000)
```

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/

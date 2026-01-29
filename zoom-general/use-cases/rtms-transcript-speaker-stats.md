# Transcript Speaker Statistics

Analyze speaking patterns and statistics from RTMS transcripts.

## Overview

Calculate talk time, word count, and speaking patterns per participant.

## Skills Needed

- **zoom-rtms** - Primary

## Statistics

| Metric | Description |
|--------|-------------|
| Talk time | Total speaking duration |
| Word count | Total words spoken |
| Turn count | Number of speaking turns |
| Words per minute | Speaking rate |

## Implementation

### JavaScript

```javascript
class SpeakerStats {
  constructor(transcripts = []) {
    this.transcripts = transcripts;
    this.stats = this.calculate();
  }
  
  calculate() {
    const speakers = new Map();
    
    for (let i = 0; i < this.transcripts.length; i++) {
      const t = this.transcripts[i];
      const id = t.speakerId;
      
      if (!speakers.has(id)) {
        speakers.set(id, {
          id: id,
          name: t.speakerName,
          wordCount: 0,
          turnCount: 0,
          segments: [],
          firstSpoke: t.timestamp,
          lastSpoke: t.timestamp
        });
      }
      
      const speaker = speakers.get(id);
      const words = t.text.split(/\s+/).filter(w => w.length > 0);
      
      speaker.wordCount += words.length;
      speaker.turnCount++;
      speaker.lastSpoke = Math.max(speaker.lastSpoke, t.timestamp);
      
      // Calculate segment duration
      const nextTranscript = this.transcripts[i + 1];
      const duration = nextTranscript
        ? Math.min(nextTranscript.timestamp - t.timestamp, 30000)
        : this.estimateDuration(t.text);
      
      speaker.segments.push({
        text: t.text,
        timestamp: t.timestamp,
        duration: duration,
        wordCount: words.length
      });
    }
    
    // Calculate derived stats
    for (const speaker of speakers.values()) {
      speaker.totalDuration = speaker.segments.reduce((sum, s) => sum + s.duration, 0);
      speaker.wordsPerMinute = speaker.totalDuration > 0
        ? (speaker.wordCount / speaker.totalDuration) * 60000
        : 0;
      speaker.averageWordsPerTurn = speaker.wordCount / speaker.turnCount;
    }
    
    return speakers;
  }
  
  estimateDuration(text) {
    // ~150 words per minute
    const words = text.split(/\s+/).length;
    return (words / 150) * 60000;
  }
  
  getSpeakerStats(speakerId) {
    return this.stats.get(speakerId);
  }
  
  getAllStats() {
    return Array.from(this.stats.values());
  }
  
  getRankedBySpeakingTime() {
    return this.getAllStats()
      .sort((a, b) => b.totalDuration - a.totalDuration);
  }
  
  getRankedByWordCount() {
    return this.getAllStats()
      .sort((a, b) => b.wordCount - a.wordCount);
  }
  
  getTalkTimeDistribution() {
    const total = this.getAllStats()
      .reduce((sum, s) => sum + s.totalDuration, 0);
    
    return this.getAllStats().map(s => ({
      id: s.id,
      name: s.name,
      percentage: (s.totalDuration / total) * 100,
      duration: s.totalDuration
    }));
  }
  
  getOverlapAnalysis() {
    // Detect when multiple people spoke at similar times
    const overlaps = [];
    const sorted = [...this.transcripts].sort((a, b) => a.timestamp - b.timestamp);
    
    for (let i = 0; i < sorted.length - 1; i++) {
      const current = sorted[i];
      const next = sorted[i + 1];
      const gap = next.timestamp - current.timestamp;
      
      if (gap < 500 && current.speakerId !== next.speakerId) {
        overlaps.push({
          speakers: [current.speakerName, next.speakerName],
          timestamp: current.timestamp,
          gap: gap
        });
      }
    }
    
    return overlaps;
  }
  
  getSummary() {
    const stats = this.getAllStats();
    const totalWords = stats.reduce((sum, s) => sum + s.wordCount, 0);
    const totalDuration = stats.reduce((sum, s) => sum + s.totalDuration, 0);
    
    return {
      participantCount: stats.length,
      totalWords: totalWords,
      totalDuration: totalDuration,
      totalTurns: stats.reduce((sum, s) => sum + s.turnCount, 0),
      averageWordsPerParticipant: totalWords / stats.length,
      topSpeaker: this.getRankedBySpeakingTime()[0]?.name,
      distribution: this.getTalkTimeDistribution()
    };
  }
  
  formatDuration(ms) {
    const minutes = Math.floor(ms / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);
    return `${minutes}m ${seconds}s`;
  }
  
  printReport() {
    const summary = this.getSummary();
    
    console.log('\n=== Meeting Statistics ===\n');
    console.log(`Participants: ${summary.participantCount}`);
    console.log(`Total words: ${summary.totalWords}`);
    console.log(`Duration: ${this.formatDuration(summary.totalDuration)}`);
    console.log(`\nTalk Time Distribution:`);
    
    for (const dist of summary.distribution) {
      const bar = '█'.repeat(Math.floor(dist.percentage / 5));
      console.log(`  ${dist.name}: ${dist.percentage.toFixed(1)}% ${bar}`);
    }
  }
}

// Usage
const stats = new SpeakerStats(receiver.transcripts);
stats.printReport();

const distribution = stats.getTalkTimeDistribution();
const overlaps = stats.getOverlapAnalysis();
```

### Python

```python
from dataclasses import dataclass, field
from typing import List, Dict
from collections import defaultdict

@dataclass
class SpeakerData:
    id: str
    name: str
    word_count: int = 0
    turn_count: int = 0
    total_duration: float = 0
    segments: List[dict] = field(default_factory=list)
    words_per_minute: float = 0
    average_words_per_turn: float = 0

class SpeakerStats:
    def __init__(self, transcripts: List[dict]):
        self.transcripts = transcripts
        self.stats = self.calculate()
    
    def calculate(self) -> Dict[str, SpeakerData]:
        speakers = {}
        
        for i, t in enumerate(self.transcripts):
            speaker_id = t['speaker_id']
            
            if speaker_id not in speakers:
                speakers[speaker_id] = SpeakerData(
                    id=speaker_id,
                    name=t['speaker_name']
                )
            
            speaker = speakers[speaker_id]
            words = t['text'].split()
            
            speaker.word_count += len(words)
            speaker.turn_count += 1
            
            # Estimate duration
            next_t = self.transcripts[i + 1] if i + 1 < len(self.transcripts) else None
            if next_t:
                duration = min(next_t['timestamp'] - t['timestamp'], 30000)
            else:
                duration = self.estimate_duration(t['text'])
            
            speaker.segments.append({
                'text': t['text'],
                'timestamp': t['timestamp'],
                'duration': duration,
                'word_count': len(words)
            })
        
        # Calculate derived stats
        for speaker in speakers.values():
            speaker.total_duration = sum(s['duration'] for s in speaker.segments)
            
            if speaker.total_duration > 0:
                speaker.words_per_minute = (speaker.word_count / speaker.total_duration) * 60000
            
            if speaker.turn_count > 0:
                speaker.average_words_per_turn = speaker.word_count / speaker.turn_count
        
        return speakers
    
    def estimate_duration(self, text: str) -> float:
        words = len(text.split())
        return (words / 150) * 60000
    
    def get_all_stats(self) -> List[SpeakerData]:
        return list(self.stats.values())
    
    def get_ranked_by_speaking_time(self) -> List[SpeakerData]:
        return sorted(self.get_all_stats(), key=lambda s: s.total_duration, reverse=True)
    
    def get_talk_time_distribution(self) -> List[dict]:
        total = sum(s.total_duration for s in self.stats.values())
        
        return [
            {
                'id': s.id,
                'name': s.name,
                'percentage': (s.total_duration / total) * 100 if total > 0 else 0,
                'duration': s.total_duration
            }
            for s in self.stats.values()
        ]
    
    def get_summary(self) -> dict:
        stats = self.get_all_stats()
        total_words = sum(s.word_count for s in stats)
        total_duration = sum(s.total_duration for s in stats)
        
        ranked = self.get_ranked_by_speaking_time()
        
        return {
            'participant_count': len(stats),
            'total_words': total_words,
            'total_duration': total_duration,
            'total_turns': sum(s.turn_count for s in stats),
            'top_speaker': ranked[0].name if ranked else None,
            'distribution': self.get_talk_time_distribution()
        }
    
    def format_duration(self, ms: float) -> str:
        minutes = int(ms // 60000)
        seconds = int((ms % 60000) // 1000)
        return f"{minutes}m {seconds}s"
    
    def print_report(self):
        summary = self.get_summary()
        
        print("\n=== Meeting Statistics ===\n")
        print(f"Participants: {summary['participant_count']}")
        print(f"Total words: {summary['total_words']}")
        print(f"Duration: {self.format_duration(summary['total_duration'])}")
        print("\nTalk Time Distribution:")
        
        for dist in summary['distribution']:
            bar = '█' * int(dist['percentage'] / 5)
            print(f"  {dist['name']}: {dist['percentage']:.1f}% {bar}")

# Usage
stats = SpeakerStats(receiver.transcripts)
stats.print_report()
```

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/

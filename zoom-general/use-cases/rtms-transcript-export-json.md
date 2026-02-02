# Export Transcript to JSON

Export RTMS transcripts to structured JSON format.

## Overview

Save transcripts as JSON for storage, analysis, or integration with other systems.

## Skills Needed

- **zoom-rtms** - Primary

## JSON Formats

| Format | Use Case |
|--------|----------|
| Full export | Complete data preservation |
| Simple | Human-readable |
| Indexed | Fast lookup |
| Streaming | Real-time export |

## Implementation

### JavaScript

```javascript
class TranscriptJSONExporter {
  constructor(options = {}) {
    this.includeMetadata = options.includeMetadata !== false;
    this.pretty = options.pretty !== false;
    this.format = options.format || 'full'; // full, simple, indexed
  }
  
  export(transcripts, metadata = {}) {
    switch (this.format) {
      case 'simple':
        return this.exportSimple(transcripts, metadata);
      case 'indexed':
        return this.exportIndexed(transcripts, metadata);
      default:
        return this.exportFull(transcripts, metadata);
    }
  }
  
  exportFull(transcripts, metadata) {
    const data = {
      version: '1.0',
      exportedAt: new Date().toISOString(),
      format: 'full',
      metadata: this.includeMetadata ? {
        meetingId: metadata.meetingId,
        meetingTitle: metadata.title,
        startTime: metadata.startTime,
        endTime: metadata.endTime,
        duration: this.calculateDuration(transcripts),
        participantCount: this.getUniqueParticipants(transcripts).length,
        segmentCount: transcripts.length,
        wordCount: this.getTotalWordCount(transcripts),
        ...metadata
      } : undefined,
      participants: this.getParticipantList(transcripts),
      transcripts: transcripts.map((t, i) => ({
        index: i,
        speakerId: t.speakerId,
        speakerName: t.speakerName,
        text: t.text,
        timestamp: t.timestamp,
        relativeTime: this.formatRelativeTime(t.timestamp, transcripts[0]?.timestamp),
        wordCount: t.text.split(/\s+/).length,
        isFinal: t.isFinal ?? true
      }))
    };
    
    return this.stringify(data);
  }
  
  exportSimple(transcripts, metadata) {
    const data = {
      meeting: metadata.title || 'Untitled Meeting',
      date: new Date(transcripts[0]?.timestamp || Date.now()).toISOString().split('T')[0],
      transcript: transcripts.map(t => ({
        time: this.formatRelativeTime(t.timestamp, transcripts[0]?.timestamp),
        speaker: t.speakerName,
        text: t.text
      }))
    };
    
    return this.stringify(data);
  }
  
  exportIndexed(transcripts, metadata) {
    const byTime = {};
    const bySpeaker = {};
    const baseTime = transcripts[0]?.timestamp || 0;
    
    for (let i = 0; i < transcripts.length; i++) {
      const t = transcripts[i];
      const relativeTime = t.timestamp - baseTime;
      const minute = Math.floor(relativeTime / 60000);
      
      // Index by minute
      if (!byTime[minute]) {
        byTime[minute] = [];
      }
      byTime[minute].push(i);
      
      // Index by speaker
      if (!bySpeaker[t.speakerId]) {
        bySpeaker[t.speakerId] = {
          name: t.speakerName,
          indices: []
        };
      }
      bySpeaker[t.speakerId].indices.push(i);
    }
    
    const data = {
      version: '1.0',
      format: 'indexed',
      metadata: this.includeMetadata ? metadata : undefined,
      indices: {
        byMinute: byTime,
        bySpeaker: bySpeaker
      },
      transcripts: transcripts.map((t, i) => ({
        i: i,
        s: t.speakerId,
        t: t.text,
        ts: t.timestamp
      }))
    };
    
    return this.stringify(data);
  }
  
  // Export for streaming/JSONL format
  exportLine(transcript, index) {
    return JSON.stringify({
      i: index,
      s: transcript.speakerId,
      n: transcript.speakerName,
      t: transcript.text,
      ts: transcript.timestamp
    });
  }
  
  // Create streaming exporter
  createStreamExporter(outputPath) {
    const fs = require('fs');
    const stream = fs.createWriteStream(outputPath);
    let index = 0;
    
    return {
      write: (transcript) => {
        stream.write(this.exportLine(transcript, index++) + '\n');
      },
      close: () => {
        stream.end();
        return outputPath;
      }
    };
  }
  
  getUniqueParticipants(transcripts) {
    return [...new Set(transcripts.map(t => t.speakerId))];
  }
  
  getParticipantList(transcripts) {
    const participants = new Map();
    
    for (const t of transcripts) {
      if (!participants.has(t.speakerId)) {
        participants.set(t.speakerId, {
          id: t.speakerId,
          name: t.speakerName,
          segmentCount: 0,
          wordCount: 0
        });
      }
      
      const p = participants.get(t.speakerId);
      p.segmentCount++;
      p.wordCount += t.text.split(/\s+/).length;
    }
    
    return Array.from(participants.values());
  }
  
  calculateDuration(transcripts) {
    if (transcripts.length < 2) return 0;
    return transcripts[transcripts.length - 1].timestamp - transcripts[0].timestamp;
  }
  
  getTotalWordCount(transcripts) {
    return transcripts.reduce((sum, t) => sum + t.text.split(/\s+/).length, 0);
  }
  
  formatRelativeTime(timestamp, baseTime) {
    const ms = timestamp - (baseTime || 0);
    const minutes = Math.floor(ms / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  }
  
  stringify(data) {
    return this.pretty
      ? JSON.stringify(data, null, 2)
      : JSON.stringify(data);
  }
  
  save(transcripts, filename, metadata = {}) {
    const fs = require('fs');
    const content = this.export(transcripts, metadata);
    fs.writeFileSync(filename, content, 'utf8');
    console.log(`Saved JSON: ${filename}`);
    return filename;
  }
}

// Usage
const exporter = new TranscriptJSONExporter({
  format: 'full',
  pretty: true
});

// Full export
const json = exporter.export(receiver.transcripts, {
  meetingId: 'meeting-123',
  title: 'Weekly Standup'
});

exporter.save(receiver.transcripts, 'transcript.json', {
  meetingId: 'meeting-123'
});

// Streaming export
const streamExporter = exporter.createStreamExporter('transcript.jsonl');
receiver.onTranscript = (t) => streamExporter.write(t);
// Later: streamExporter.close();
```

### Python

```python
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

class TranscriptJSONExporter:
    def __init__(
        self,
        include_metadata: bool = True,
        pretty: bool = True,
        format: str = 'full'
    ):
        self.include_metadata = include_metadata
        self.pretty = pretty
        self.format = format
    
    def export(self, transcripts: List[dict], metadata: Dict = None) -> str:
        metadata = metadata or {}
        
        if self.format == 'simple':
            return self.export_simple(transcripts, metadata)
        elif self.format == 'indexed':
            return self.export_indexed(transcripts, metadata)
        else:
            return self.export_full(transcripts, metadata)
    
    def export_full(self, transcripts: List[dict], metadata: Dict) -> str:
        base_time = transcripts[0]['timestamp'] if transcripts else 0
        
        data = {
            'version': '1.0',
            'exportedAt': datetime.now().isoformat(),
            'format': 'full',
            'transcripts': [
                {
                    'index': i,
                    'speakerId': t['speaker_id'],
                    'speakerName': t['speaker_name'],
                    'text': t['text'],
                    'timestamp': t['timestamp'],
                    'relativeTime': self.format_time(t['timestamp'] - base_time),
                    'wordCount': len(t['text'].split())
                }
                for i, t in enumerate(transcripts)
            ]
        }
        
        if self.include_metadata:
            data['metadata'] = {
                'duration': self.calculate_duration(transcripts),
                'participantCount': len(set(t['speaker_id'] for t in transcripts)),
                'segmentCount': len(transcripts),
                **metadata
            }
            data['participants'] = self.get_participant_list(transcripts)
        
        return self.stringify(data)
    
    def export_simple(self, transcripts: List[dict], metadata: Dict) -> str:
        base_time = transcripts[0]['timestamp'] if transcripts else 0
        
        data = {
            'meeting': metadata.get('title', 'Untitled'),
            'transcript': [
                {
                    'time': self.format_time(t['timestamp'] - base_time),
                    'speaker': t['speaker_name'],
                    'text': t['text']
                }
                for t in transcripts
            ]
        }
        
        return self.stringify(data)
    
    def get_participant_list(self, transcripts: List[dict]) -> List[dict]:
        participants = {}
        
        for t in transcripts:
            sid = t['speaker_id']
            if sid not in participants:
                participants[sid] = {
                    'id': sid,
                    'name': t['speaker_name'],
                    'segmentCount': 0,
                    'wordCount': 0
                }
            
            participants[sid]['segmentCount'] += 1
            participants[sid]['wordCount'] += len(t['text'].split())
        
        return list(participants.values())
    
    def calculate_duration(self, transcripts: List[dict]) -> int:
        if len(transcripts) < 2:
            return 0
        return transcripts[-1]['timestamp'] - transcripts[0]['timestamp']
    
    def format_time(self, ms: int) -> str:
        minutes = ms // 60000
        seconds = (ms % 60000) // 1000
        return f"{minutes}:{seconds:02d}"
    
    def stringify(self, data: Dict) -> str:
        if self.pretty:
            return json.dumps(data, indent=2, ensure_ascii=False)
        return json.dumps(data, ensure_ascii=False)
    
    def save(self, transcripts: List[dict], filename: str, metadata: Dict = None) -> str:
        content = self.export(transcripts, metadata or {})
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Saved JSON: {filename}")
        return filename

# Usage
exporter = TranscriptJSONExporter(format='full', pretty=True)

json_content = exporter.export(receiver.transcripts, {
    'meetingId': 'meeting-123',
    'title': 'Weekly Standup'
})

exporter.save(receiver.transcripts, 'transcript.json')
```

## Resources

- **JSON spec**: https://www.json.org/
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

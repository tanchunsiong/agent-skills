# Export Transcript to SRT

Export RTMS transcripts to SRT subtitle format.

## Overview

Create SRT files from transcripts for video subtitles or accessibility.

## Skills Needed

- **zoom-rtms** - Primary

## SRT Format

```
1
00:00:01,000 --> 00:00:04,500
John: Hello everyone, welcome to the meeting.

2
00:00:05,000 --> 00:00:08,200
Jane: Thank you for joining us today.
```

## Implementation

### JavaScript

```javascript
class SRTExporter {
  constructor(options = {}) {
    this.includeSpeaker = options.includeSpeaker !== false;
    this.maxCharsPerLine = options.maxCharsPerLine || 42;
    this.maxDuration = options.maxDuration || 7000; // 7 seconds
    this.minDuration = options.minDuration || 1000; // 1 second
  }
  
  export(transcripts, startTime = null) {
    const baseTime = startTime || (transcripts[0]?.timestamp || 0);
    const subtitles = [];
    let index = 1;
    
    for (const transcript of transcripts) {
      const relativeStart = transcript.timestamp - baseTime;
      const duration = this.calculateDuration(transcript.text);
      const relativeEnd = relativeStart + duration;
      
      const text = this.includeSpeaker
        ? `${transcript.speakerName}: ${transcript.text}`
        : transcript.text;
      
      // Split long text into multiple subtitles
      const chunks = this.splitText(text);
      const chunkDuration = duration / chunks.length;
      
      for (let i = 0; i < chunks.length; i++) {
        const chunkStart = relativeStart + (i * chunkDuration);
        const chunkEnd = chunkStart + chunkDuration;
        
        subtitles.push({
          index: index++,
          start: this.formatTimestamp(chunkStart),
          end: this.formatTimestamp(chunkEnd),
          text: chunks[i]
        });
      }
    }
    
    return this.formatSRT(subtitles);
  }
  
  formatTimestamp(ms) {
    const hours = Math.floor(ms / 3600000);
    const minutes = Math.floor((ms % 3600000) / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);
    const milliseconds = ms % 1000;
    
    return `${hours.toString().padStart(2, '0')}:` +
           `${minutes.toString().padStart(2, '0')}:` +
           `${seconds.toString().padStart(2, '0')},` +
           `${milliseconds.toString().padStart(3, '0')}`;
  }
  
  calculateDuration(text) {
    // Estimate reading time: ~150 words per minute
    const words = text.split(/\s+/).length;
    const duration = (words / 150) * 60 * 1000;
    
    return Math.min(Math.max(duration, this.minDuration), this.maxDuration);
  }
  
  splitText(text) {
    if (text.length <= this.maxCharsPerLine * 2) {
      return [text];
    }
    
    const words = text.split(/\s+/);
    const chunks = [];
    let currentChunk = '';
    
    for (const word of words) {
      if ((currentChunk + ' ' + word).trim().length <= this.maxCharsPerLine * 2) {
        currentChunk = (currentChunk + ' ' + word).trim();
      } else {
        if (currentChunk) chunks.push(currentChunk);
        currentChunk = word;
      }
    }
    
    if (currentChunk) chunks.push(currentChunk);
    
    return chunks;
  }
  
  formatSRT(subtitles) {
    return subtitles.map(sub => 
      `${sub.index}\n${sub.start} --> ${sub.end}\n${sub.text}\n`
    ).join('\n');
  }
  
  save(transcripts, filename) {
    const fs = require('fs');
    const content = this.export(transcripts);
    fs.writeFileSync(filename, content, 'utf8');
    console.log(`Saved SRT: ${filename}`);
    return filename;
  }
}

// Usage
const exporter = new SRTExporter({
  includeSpeaker: true,
  maxCharsPerLine: 42
});

// From transcript receiver
ws.on('close', () => {
  const transcripts = receiver.transcripts;
  const srt = exporter.export(transcripts);
  
  // Save to file
  exporter.save(transcripts, 'meeting_captions.srt');
  
  console.log(srt);
});
```

### Python

```python
from dataclasses import dataclass
from typing import List
import os

@dataclass
class Subtitle:
    index: int
    start: str
    end: str
    text: str

class SRTExporter:
    def __init__(
        self,
        include_speaker=True,
        max_chars_per_line=42,
        max_duration=7000,
        min_duration=1000
    ):
        self.include_speaker = include_speaker
        self.max_chars_per_line = max_chars_per_line
        self.max_duration = max_duration
        self.min_duration = min_duration
    
    def export(self, transcripts, start_time=None) -> str:
        if not transcripts:
            return ""
        
        base_time = start_time or transcripts[0].timestamp
        subtitles = []
        index = 1
        
        for transcript in transcripts:
            relative_start = transcript.timestamp - base_time
            duration = self.calculate_duration(transcript.text)
            
            text = f"{transcript.speaker_name}: {transcript.text}" \
                   if self.include_speaker else transcript.text
            
            # Split long text
            chunks = self.split_text(text)
            chunk_duration = duration / len(chunks)
            
            for i, chunk in enumerate(chunks):
                chunk_start = relative_start + (i * chunk_duration)
                chunk_end = chunk_start + chunk_duration
                
                subtitles.append(Subtitle(
                    index=index,
                    start=self.format_timestamp(chunk_start),
                    end=self.format_timestamp(chunk_end),
                    text=chunk
                ))
                index += 1
        
        return self.format_srt(subtitles)
    
    def format_timestamp(self, ms: float) -> str:
        ms = int(ms)
        hours = ms // 3600000
        minutes = (ms % 3600000) // 60000
        seconds = (ms % 60000) // 1000
        milliseconds = ms % 1000
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    
    def calculate_duration(self, text: str) -> float:
        words = len(text.split())
        duration = (words / 150) * 60 * 1000  # 150 WPM
        return min(max(duration, self.min_duration), self.max_duration)
    
    def split_text(self, text: str) -> List[str]:
        max_len = self.max_chars_per_line * 2
        
        if len(text) <= max_len:
            return [text]
        
        words = text.split()
        chunks = []
        current = ""
        
        for word in words:
            if len(f"{current} {word}".strip()) <= max_len:
                current = f"{current} {word}".strip()
            else:
                if current:
                    chunks.append(current)
                current = word
        
        if current:
            chunks.append(current)
        
        return chunks
    
    def format_srt(self, subtitles: List[Subtitle]) -> str:
        lines = []
        for sub in subtitles:
            lines.append(f"{sub.index}")
            lines.append(f"{sub.start} --> {sub.end}")
            lines.append(sub.text)
            lines.append("")
        
        return "\n".join(lines)
    
    def save(self, transcripts, filename: str) -> str:
        content = self.export(transcripts)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Saved SRT: {filename}")
        return filename

# Usage
exporter = SRTExporter(include_speaker=True)

# After receiving transcripts
srt_content = exporter.export(receiver.transcripts)
exporter.save(receiver.transcripts, "meeting_captions.srt")
```

## SRT Validation

```javascript
function validateSRT(srtContent) {
  const blocks = srtContent.trim().split(/\n\n+/);
  const errors = [];
  
  for (let i = 0; i < blocks.length; i++) {
    const lines = blocks[i].split('\n');
    
    if (lines.length < 3) {
      errors.push(`Block ${i + 1}: Missing lines`);
      continue;
    }
    
    // Check index
    if (!/^\d+$/.test(lines[0])) {
      errors.push(`Block ${i + 1}: Invalid index`);
    }
    
    // Check timestamp
    const timeRegex = /^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$/;
    if (!timeRegex.test(lines[1])) {
      errors.push(`Block ${i + 1}: Invalid timestamp format`);
    }
  }
  
  return { valid: errors.length === 0, errors };
}
```

## Resources

- **SRT spec**: https://en.wikipedia.org/wiki/SubRip
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

# Export Transcript to VTT

Export RTMS transcripts to WebVTT format for web video players.

## Overview

Create VTT files for HTML5 video captions with styling and positioning.

## Skills Needed

- **zoom-rtms** - Primary

## VTT Format

```
WEBVTT

1
00:00:01.000 --> 00:00:04.500
<v John>Hello everyone, welcome to the meeting.

2
00:00:05.000 --> 00:00:08.200
<v Jane>Thank you for joining us today.
```

## Implementation

### JavaScript

```javascript
class VTTExporter {
  constructor(options = {}) {
    this.includeSpeaker = options.includeSpeaker !== false;
    this.useVoiceTags = options.useVoiceTags !== false;
    this.maxCharsPerLine = options.maxCharsPerLine || 42;
    this.styling = options.styling || {};
  }
  
  export(transcripts, startTime = null) {
    const baseTime = startTime || (transcripts[0]?.timestamp || 0);
    const cues = [];
    let index = 1;
    
    for (const transcript of transcripts) {
      const relativeStart = transcript.timestamp - baseTime;
      const duration = this.calculateDuration(transcript.text);
      const relativeEnd = relativeStart + duration;
      
      let text;
      if (this.useVoiceTags) {
        text = `<v ${transcript.speakerName}>${transcript.text}`;
      } else if (this.includeSpeaker) {
        text = `${transcript.speakerName}: ${transcript.text}`;
      } else {
        text = transcript.text;
      }
      
      cues.push({
        index: index++,
        start: this.formatTimestamp(relativeStart),
        end: this.formatTimestamp(relativeEnd),
        text: text,
        speaker: transcript.speakerName
      });
    }
    
    return this.formatVTT(cues);
  }
  
  formatTimestamp(ms) {
    const hours = Math.floor(ms / 3600000);
    const minutes = Math.floor((ms % 3600000) / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);
    const milliseconds = ms % 1000;
    
    return `${hours.toString().padStart(2, '0')}:` +
           `${minutes.toString().padStart(2, '0')}:` +
           `${seconds.toString().padStart(2, '0')}.` +
           `${milliseconds.toString().padStart(3, '0')}`;
  }
  
  calculateDuration(text) {
    const words = text.split(/\s+/).length;
    return Math.min(Math.max((words / 150) * 60000, 1000), 7000);
  }
  
  formatVTT(cues) {
    let output = 'WEBVTT\n';
    
    // Add header metadata
    if (this.styling.region) {
      output += `\nREGION\n`;
      output += `id:${this.styling.region.id || 'bottom'}\n`;
      output += `width:${this.styling.region.width || '100%'}\n`;
      output += `lines:${this.styling.region.lines || 3}\n`;
    }
    
    // Add style block
    if (this.styling.styles) {
      output += '\nSTYLE\n';
      output += this.styling.styles;
      output += '\n';
    }
    
    // Add cues
    for (const cue of cues) {
      output += `\n${cue.index}\n`;
      output += `${cue.start} --> ${cue.end}`;
      
      // Add positioning
      if (this.styling.position) {
        output += ` position:${this.styling.position}`;
      }
      if (this.styling.align) {
        output += ` align:${this.styling.align}`;
      }
      
      output += `\n${cue.text}\n`;
    }
    
    return output;
  }
  
  exportWithStyles(transcripts) {
    // Add CSS styles for speakers
    const speakers = [...new Set(transcripts.map(t => t.speakerName))];
    const colors = ['#4fc3f7', '#81c784', '#ffb74d', '#f06292', '#ba68c8'];
    
    let styles = '';
    speakers.forEach((speaker, i) => {
      const color = colors[i % colors.length];
      styles += `::cue(v[voice="${speaker}"]) { color: ${color}; }\n`;
    });
    
    this.styling.styles = styles;
    return this.export(transcripts);
  }
  
  save(transcripts, filename) {
    const fs = require('fs');
    const content = this.export(transcripts);
    fs.writeFileSync(filename, content, 'utf8');
    console.log(`Saved VTT: ${filename}`);
    return filename;
  }
}

// Usage
const exporter = new VTTExporter({
  useVoiceTags: true,
  styling: {
    position: '50%',
    align: 'center'
  }
});

ws.on('close', () => {
  const vtt = exporter.exportWithStyles(receiver.transcripts);
  exporter.save(receiver.transcripts, 'meeting_captions.vtt');
});
```

### Python

```python
from typing import List, Optional, Dict
from dataclasses import dataclass

@dataclass
class VTTCue:
    index: int
    start: str
    end: str
    text: str
    speaker: str

class VTTExporter:
    def __init__(
        self,
        include_speaker=True,
        use_voice_tags=True,
        max_chars_per_line=42,
        styling=None
    ):
        self.include_speaker = include_speaker
        self.use_voice_tags = use_voice_tags
        self.max_chars_per_line = max_chars_per_line
        self.styling = styling or {}
    
    def export(self, transcripts, start_time=None) -> str:
        if not transcripts:
            return "WEBVTT\n"
        
        base_time = start_time or transcripts[0].timestamp
        cues = []
        index = 1
        
        for transcript in transcripts:
            relative_start = transcript.timestamp - base_time
            duration = self.calculate_duration(transcript.text)
            relative_end = relative_start + duration
            
            if self.use_voice_tags:
                text = f"<v {transcript.speaker_name}>{transcript.text}"
            elif self.include_speaker:
                text = f"{transcript.speaker_name}: {transcript.text}"
            else:
                text = transcript.text
            
            cues.append(VTTCue(
                index=index,
                start=self.format_timestamp(relative_start),
                end=self.format_timestamp(relative_end),
                text=text,
                speaker=transcript.speaker_name
            ))
            index += 1
        
        return self.format_vtt(cues)
    
    def format_timestamp(self, ms: float) -> str:
        ms = int(ms)
        hours = ms // 3600000
        minutes = (ms % 3600000) // 60000
        seconds = (ms % 60000) // 1000
        milliseconds = ms % 1000
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    
    def calculate_duration(self, text: str) -> float:
        words = len(text.split())
        return min(max((words / 150) * 60000, 1000), 7000)
    
    def format_vtt(self, cues: List[VTTCue]) -> str:
        lines = ["WEBVTT", ""]
        
        # Add region if specified
        if 'region' in self.styling:
            region = self.styling['region']
            lines.extend([
                "REGION",
                f"id:{region.get('id', 'bottom')}",
                f"width:{region.get('width', '100%')}",
                f"lines:{region.get('lines', 3)}",
                ""
            ])
        
        # Add styles
        if 'styles' in self.styling:
            lines.extend(["STYLE", self.styling['styles'], ""])
        
        # Add cues
        for cue in cues:
            lines.append(str(cue.index))
            
            timestamp_line = f"{cue.start} --> {cue.end}"
            if 'position' in self.styling:
                timestamp_line += f" position:{self.styling['position']}"
            if 'align' in self.styling:
                timestamp_line += f" align:{self.styling['align']}"
            
            lines.append(timestamp_line)
            lines.append(cue.text)
            lines.append("")
        
        return "\n".join(lines)
    
    def export_with_styles(self, transcripts) -> str:
        speakers = list(set(t.speaker_name for t in transcripts))
        colors = ['#4fc3f7', '#81c784', '#ffb74d', '#f06292', '#ba68c8']
        
        styles = []
        for i, speaker in enumerate(speakers):
            color = colors[i % len(colors)]
            styles.append(f'::cue(v[voice="{speaker}"]) {{ color: {color}; }}')
        
        self.styling['styles'] = "\n".join(styles)
        return self.export(transcripts)
    
    def save(self, transcripts, filename: str) -> str:
        content = self.export(transcripts)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Saved VTT: {filename}")
        return filename

# Usage
exporter = VTTExporter(use_voice_tags=True)
vtt = exporter.export_with_styles(receiver.transcripts)
exporter.save(receiver.transcripts, "meeting_captions.vtt")
```

## HTML5 Video Integration

```html
<video controls>
  <source src="meeting.mp4" type="video/mp4">
  <track kind="captions" src="meeting_captions.vtt" srclang="en" label="English" default>
</video>
```

## Resources

- **WebVTT spec**: https://www.w3.org/TR/webvtt1/
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

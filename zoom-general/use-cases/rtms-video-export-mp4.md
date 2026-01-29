# Export Video to MP4

Export RTMS video streams to MP4 format.

## Overview

Create standard MP4 files from RTMS streams for sharing, archival, or playback.

## Skills Needed

- **zoom-rtms** - Primary

## Export Options

| Quality | Resolution | Bitrate | Size/Hour |
|---------|------------|---------|-----------|
| Low | 640x360 | 500 Kbps | ~220 MB |
| Medium | 1280x720 | 2 Mbps | ~900 MB |
| High | 1920x1080 | 5 Mbps | ~2.2 GB |

## Implementation

### JavaScript - FFmpeg

```javascript
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

class MP4Exporter {
  constructor(options = {}) {
    this.outputDir = options.outputDir || './exports';
    this.quality = options.quality || 'medium'; // low, medium, high
    this.includeAudio = options.includeAudio !== false;
    
    this.videoBuffer = [];
    this.audioBuffer = [];
    
    fs.mkdirSync(this.outputDir, { recursive: true });
  }
  
  addVideoFrame(h264Data) {
    this.videoBuffer.push({
      data: h264Data,
      timestamp: Date.now()
    });
  }
  
  addAudioChunk(pcmData) {
    this.audioBuffer.push({
      data: pcmData,
      timestamp: Date.now()
    });
  }
  
  async export(filename = null) {
    if (!filename) {
      filename = `meeting_${Date.now()}.mp4`;
    }
    
    const outputPath = path.join(this.outputDir, filename);
    const tempVideo = path.join(this.outputDir, 'temp_video.h264');
    const tempAudio = path.join(this.outputDir, 'temp_audio.pcm');
    
    // Write buffers to temp files
    const videoData = Buffer.concat(this.videoBuffer.map(v => v.data));
    fs.writeFileSync(tempVideo, videoData);
    
    const ffmpegArgs = [
      '-y',
      '-f', 'h264',
      '-i', tempVideo
    ];
    
    if (this.includeAudio && this.audioBuffer.length > 0) {
      const audioData = Buffer.concat(this.audioBuffer.map(a => a.data));
      fs.writeFileSync(tempAudio, audioData);
      
      ffmpegArgs.push(
        '-f', 's16le',
        '-ar', '16000',
        '-ac', '1',
        '-i', tempAudio
      );
    }
    
    // Quality settings
    const qualitySettings = this.getQualitySettings();
    ffmpegArgs.push(...qualitySettings);
    
    ffmpegArgs.push(outputPath);
    
    return new Promise((resolve, reject) => {
      const ffmpeg = spawn('ffmpeg', ffmpegArgs);
      
      ffmpeg.on('close', (code) => {
        // Cleanup temp files
        try {
          fs.unlinkSync(tempVideo);
          if (fs.existsSync(tempAudio)) fs.unlinkSync(tempAudio);
        } catch (e) {}
        
        if (code === 0) {
          const stats = fs.statSync(outputPath);
          resolve({
            path: outputPath,
            size: stats.size,
            duration: this.calculateDuration()
          });
        } else {
          reject(new Error(`FFmpeg exited with code ${code}`));
        }
      });
      
      ffmpeg.stderr.on('data', (data) => {
        // Progress info
      });
    });
  }
  
  getQualitySettings() {
    switch (this.quality) {
      case 'low':
        return [
          '-vf', 'scale=640:360',
          '-c:v', 'libx264',
          '-preset', 'fast',
          '-crf', '28',
          '-c:a', 'aac',
          '-b:a', '64k'
        ];
      case 'high':
        return [
          '-vf', 'scale=1920:1080',
          '-c:v', 'libx264',
          '-preset', 'slow',
          '-crf', '18',
          '-c:a', 'aac',
          '-b:a', '192k'
        ];
      default: // medium
        return [
          '-vf', 'scale=1280:720',
          '-c:v', 'libx264',
          '-preset', 'medium',
          '-crf', '23',
          '-c:a', 'aac',
          '-b:a', '128k'
        ];
    }
  }
  
  calculateDuration() {
    if (this.videoBuffer.length < 2) return 0;
    const first = this.videoBuffer[0].timestamp;
    const last = this.videoBuffer[this.videoBuffer.length - 1].timestamp;
    return (last - first) / 1000;
  }
  
  clear() {
    this.videoBuffer = [];
    this.audioBuffer = [];
  }
}

// Streaming export (no buffering)
class StreamingMP4Exporter {
  constructor(outputPath, options = {}) {
    this.outputPath = outputPath;
    this.quality = options.quality || 'medium';
    this.ffmpeg = null;
  }
  
  start() {
    const settings = {
      low: { scale: '640:360', crf: '28', preset: 'fast' },
      medium: { scale: '1280:720', crf: '23', preset: 'medium' },
      high: { scale: '1920:1080', crf: '18', preset: 'slow' }
    };
    
    const s = settings[this.quality];
    
    this.ffmpeg = spawn('ffmpeg', [
      '-y',
      '-f', 'h264',
      '-i', 'pipe:0',
      '-vf', `scale=${s.scale}`,
      '-c:v', 'libx264',
      '-preset', s.preset,
      '-crf', s.crf,
      '-pix_fmt', 'yuv420p',
      '-movflags', '+faststart',
      this.outputPath
    ]);
    
    console.log(`Streaming export to ${this.outputPath}`);
  }
  
  write(h264Data) {
    if (this.ffmpeg && this.ffmpeg.stdin.writable) {
      this.ffmpeg.stdin.write(h264Data);
    }
  }
  
  finish() {
    return new Promise((resolve, reject) => {
      if (!this.ffmpeg) {
        reject(new Error('Not started'));
        return;
      }
      
      this.ffmpeg.stdin.end();
      
      this.ffmpeg.on('close', (code) => {
        if (code === 0) {
          resolve(this.outputPath);
        } else {
          reject(new Error(`FFmpeg error: ${code}`));
        }
      });
    });
  }
}

// Usage with RTMS JSON protocol
const exporter = new StreamingMP4Exporter('./meeting.mp4', { quality: 'medium' });
exporter.start();

ws.on('message', (data) => {
  try {
    const message = JSON.parse(data.toString());
    
    // Handle keep-alive (msg_type 13)
    if (message.msg_type === 13) {
      console.log('Keep-alive received');
      return;
    }
    
    // Handle video frame (msg_type 15)
    if (message.msg_type === 15 && message.data) {
      // Decode base64 video data
      const h264Data = Buffer.from(message.data, 'base64');
      exporter.write(h264Data);
    }
  } catch (e) {
    console.error('Failed to parse message:', e);
  }
});

ws.on('close', async () => {
  const path = await exporter.finish();
  console.log(`Exported: ${path}`);
});
```

### Python

```python
import subprocess
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List
import time

@dataclass
class ExportResult:
    path: str
    size: int
    duration: float

class MP4Exporter:
    def __init__(
        self,
        output_dir='./exports',
        quality='medium',
        include_audio=True
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.quality = quality
        self.include_audio = include_audio
        
        self.video_buffer: List[bytes] = []
        self.audio_buffer: List[bytes] = []
        self.start_time = None
    
    def add_video_frame(self, h264_data: bytes):
        if self.start_time is None:
            self.start_time = time.time()
        self.video_buffer.append(h264_data)
    
    def add_audio_chunk(self, pcm_data: bytes):
        self.audio_buffer.append(pcm_data)
    
    def export(self, filename: Optional[str] = None) -> ExportResult:
        if not filename:
            filename = f"meeting_{int(time.time())}.mp4"
        
        output_path = self.output_dir / filename
        temp_video = self.output_dir / 'temp_video.h264'
        temp_audio = self.output_dir / 'temp_audio.pcm'
        
        # Write video buffer
        with open(temp_video, 'wb') as f:
            for frame in self.video_buffer:
                f.write(frame)
        
        # Build FFmpeg command
        cmd = ['ffmpeg', '-y', '-f', 'h264', '-i', str(temp_video)]
        
        # Add audio if available
        if self.include_audio and self.audio_buffer:
            with open(temp_audio, 'wb') as f:
                for chunk in self.audio_buffer:
                    f.write(chunk)
            
            cmd.extend(['-f', 's16le', '-ar', '16000', '-ac', '1', '-i', str(temp_audio)])
        
        # Quality settings
        cmd.extend(self.get_quality_settings())
        cmd.append(str(output_path))
        
        # Run FFmpeg
        subprocess.run(cmd, check=True, capture_output=True)
        
        # Cleanup
        temp_video.unlink(missing_ok=True)
        temp_audio.unlink(missing_ok=True)
        
        # Get result
        stats = output_path.stat()
        duration = time.time() - self.start_time if self.start_time else 0
        
        return ExportResult(
            path=str(output_path),
            size=stats.st_size,
            duration=duration
        )
    
    def get_quality_settings(self):
        settings = {
            'low': ['-vf', 'scale=640:360', '-crf', '28', '-preset', 'fast'],
            'medium': ['-vf', 'scale=1280:720', '-crf', '23', '-preset', 'medium'],
            'high': ['-vf', 'scale=1920:1080', '-crf', '18', '-preset', 'slow']
        }
        
        base = settings.get(self.quality, settings['medium'])
        return ['-c:v', 'libx264', *base, '-c:a', 'aac', '-movflags', '+faststart']
    
    def clear(self):
        self.video_buffer = []
        self.audio_buffer = []
        self.start_time = None

# Streaming exporter
class StreamingMP4Exporter:
    def __init__(self, output_path: str, quality='medium'):
        self.output_path = output_path
        self.quality = quality
        self.process = None
    
    def start(self):
        settings = {
            'low': ('640:360', '28', 'fast'),
            'medium': ('1280:720', '23', 'medium'),
            'high': ('1920:1080', '18', 'slow')
        }
        
        scale, crf, preset = settings.get(self.quality, settings['medium'])
        
        self.process = subprocess.Popen([
            'ffmpeg', '-y',
            '-f', 'h264',
            '-i', 'pipe:0',
            '-vf', f'scale={scale}',
            '-c:v', 'libx264',
            '-preset', preset,
            '-crf', crf,
            '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart',
            self.output_path
        ], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
        
        print(f"Streaming export to {self.output_path}")
    
    def write(self, h264_data: bytes):
        if self.process and self.process.stdin:
            self.process.stdin.write(h264_data)
    
    def finish(self) -> str:
        if self.process:
            self.process.stdin.close()
            self.process.wait()
            print(f"Export complete: {self.output_path}")
        return self.output_path

# Usage with RTMS JSON protocol
import json
import base64

exporter = StreamingMP4Exporter('./meeting.mp4', quality='medium')
exporter.start()

async for raw_message in ws:
    try:
        message = json.loads(raw_message)
        
        # Handle keep-alive (msg_type 13)
        if message.get('msg_type') == 13:
            print('Keep-alive received')
            continue
        
        # Handle video frame (msg_type 15)
        if message.get('msg_type') == 15 and message.get('data'):
            # Decode base64 video data
            h264_data = base64.b64decode(message['data'])
            exporter.write(h264_data)
    except json.JSONDecodeError as e:
        print(f'Failed to parse message: {e}')

# On close
exporter.finish()
```

## Resources

- **FFmpeg H.264**: https://trac.ffmpeg.org/wiki/Encode/H.264
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

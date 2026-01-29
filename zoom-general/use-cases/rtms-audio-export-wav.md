# Export Audio to WAV

Save RTMS audio streams to WAV files.

## Overview

Convert PCM audio from RTMS to standard WAV format for storage, playback, or processing.

## Skills Needed

- **zoom-rtms** - Primary

## WAV Format

```
WAV File Structure:
┌──────────────────────┐
│ RIFF Header (12 B)   │
├──────────────────────┤
│ fmt  Chunk (24 B)    │
├──────────────────────┤
│ data Chunk Header    │
├──────────────────────┤
│ PCM Audio Data       │
└──────────────────────┘
```

## Implementation

### JavaScript

```javascript
const fs = require('fs');

class WAVExporter {
  constructor(options = {}) {
    this.sampleRate = options.sampleRate || 16000;
    this.channels = options.channels || 1;
    this.bitDepth = options.bitDepth || 16;
    this.chunks = [];
  }
  
  addChunk(pcmData) {
    this.chunks.push(pcmData);
  }
  
  createWAVHeader(dataSize) {
    const buffer = Buffer.alloc(44);
    
    // RIFF header
    buffer.write('RIFF', 0);
    buffer.writeUInt32LE(36 + dataSize, 4);
    buffer.write('WAVE', 8);
    
    // fmt chunk
    buffer.write('fmt ', 12);
    buffer.writeUInt32LE(16, 16);                    // Chunk size
    buffer.writeUInt16LE(1, 20);                     // Audio format (1 = PCM)
    buffer.writeUInt16LE(this.channels, 22);         // Channels
    buffer.writeUInt32LE(this.sampleRate, 24);       // Sample rate
    buffer.writeUInt32LE(
      this.sampleRate * this.channels * this.bitDepth / 8,
      28
    );                                               // Byte rate
    buffer.writeUInt16LE(
      this.channels * this.bitDepth / 8,
      32
    );                                               // Block align
    buffer.writeUInt16LE(this.bitDepth, 34);         // Bits per sample
    
    // data chunk
    buffer.write('data', 36);
    buffer.writeUInt32LE(dataSize, 40);
    
    return buffer;
  }
  
  export(filename) {
    const audioData = Buffer.concat(this.chunks);
    const header = this.createWAVHeader(audioData.length);
    const wavFile = Buffer.concat([header, audioData]);
    
    fs.writeFileSync(filename, wavFile);
    console.log(`Exported ${filename} (${this.getDuration().toFixed(1)}s)`);
    
    return filename;
  }
  
  exportStream(outputStream) {
    const audioData = Buffer.concat(this.chunks);
    const header = this.createWAVHeader(audioData.length);
    
    outputStream.write(header);
    outputStream.write(audioData);
    outputStream.end();
  }
  
  getDuration() {
    const totalBytes = this.chunks.reduce((sum, chunk) => sum + chunk.length, 0);
    const samples = totalBytes / (this.bitDepth / 8) / this.channels;
    return samples / this.sampleRate;
  }
  
  clear() {
    this.chunks = [];
  }
}

// Usage
const exporter = new WAVExporter({ sampleRate: 16000 });

ws.on('message', (data) => {
  const msg = JSON.parse(data.toString());
  
  // Handle keep-alive
  if (msg.msg_type === 12) {
    ws.send(JSON.stringify({ msg_type: 13, timestamp: msg.timestamp }));
    return;
  }
  
  // msg_type 14 = Audio (base64-encoded PCM)
  if (msg.msg_type === 14) {
    const audioData = Buffer.from(msg.content, 'base64');
    exporter.addChunk(audioData);
  }
});

ws.on('close', () => {
  exporter.export(`meeting_${Date.now()}.wav`);
});

// Stream to file (memory efficient)
class StreamingWAVExporter {
  constructor(filename, options = {}) {
    this.filename = filename;
    this.sampleRate = options.sampleRate || 16000;
    this.channels = options.channels || 1;
    this.bitDepth = 16;
    this.dataSize = 0;
    
    // Write placeholder header
    this.stream = fs.createWriteStream(filename);
    this.stream.write(this.createPlaceholderHeader());
  }
  
  createPlaceholderHeader() {
    return Buffer.alloc(44); // Will be overwritten at end
  }
  
  write(pcmData) {
    this.stream.write(pcmData);
    this.dataSize += pcmData.length;
  }
  
  finalize() {
    this.stream.end();
    
    // Go back and write correct header
    const fd = fs.openSync(this.filename, 'r+');
    const header = new WAVExporter({
      sampleRate: this.sampleRate,
      channels: this.channels
    }).createWAVHeader(this.dataSize);
    
    fs.writeSync(fd, header, 0, 44, 0);
    fs.closeSync(fd);
    
    console.log(`Finalized ${this.filename}`);
  }
}
```

### Python

```python
import wave
import struct
import json
import base64
import numpy as np

class WAVExporter:
    def __init__(self, sample_rate=16000, channels=1, bit_depth=16):
        self.sample_rate = sample_rate
        self.channels = channels
        self.bit_depth = bit_depth
        self.chunks = []
    
    def add_chunk(self, pcm_data):
        self.chunks.append(pcm_data)
    
    def export(self, filename):
        audio_data = b''.join(self.chunks)
        
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(self.bit_depth // 8)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_data)
        
        duration = self.get_duration()
        print(f"Exported {filename} ({duration:.1f}s)")
        return filename
    
    def export_numpy(self, filename, audio_array):
        """Export numpy array to WAV"""
        # Convert float to int16 if needed
        if audio_array.dtype == np.float32 or audio_array.dtype == np.float64:
            audio_array = (audio_array * 32767).astype(np.int16)
        
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_array.tobytes())
    
    def get_duration(self):
        total_bytes = sum(len(chunk) for chunk in self.chunks)
        samples = total_bytes // (self.bit_depth // 8) // self.channels
        return samples / self.sample_rate
    
    def clear(self):
        self.chunks = []

# Streaming exporter (memory efficient)
class StreamingWAVExporter:
    def __init__(self, filename, sample_rate=16000, channels=1):
        self.filename = filename
        self.sample_rate = sample_rate
        self.channels = channels
        self.wav_file = wave.open(filename, 'wb')
        self.wav_file.setnchannels(channels)
        self.wav_file.setsampwidth(2)  # 16-bit
        self.wav_file.setframerate(sample_rate)
    
    def write(self, pcm_data):
        self.wav_file.writeframes(pcm_data)
    
    def finalize(self):
        self.wav_file.close()
        print(f"Finalized {self.filename}")

# Usage
exporter = WAVExporter(sample_rate=16000)

async for message in ws:
    msg = json.loads(message)
    
    # Handle keep-alive
    if msg['msg_type'] == 12:
        await ws.send(json.dumps({"msg_type": 13, "timestamp": msg["timestamp"]}))
        continue
    
    # msg_type 14 = Audio (base64-encoded PCM)
    if msg['msg_type'] == 14:
        audio_data = base64.b64decode(msg['content'])
        exporter.add_chunk(audio_data)

# Export when done
exporter.export(f"meeting_{int(time.time())}.wav")

# Or use streaming for large files
streaming = StreamingWAVExporter("meeting.wav")
async for message in ws:
    msg = json.loads(message)
    
    if msg['msg_type'] == 14:
        audio_data = base64.b64decode(msg['content'])
        streaming.write(audio_data)
streaming.finalize()
```

## Export with Speaker Labels

```javascript
async function exportWithSpeakers(segments, audioData, outputDir) {
  // Export per-speaker WAV files
  for (const [speaker, times] of Object.entries(segments)) {
    const speakerAudio = extractSegments(audioData, times);
    const exporter = new WAVExporter();
    exporter.chunks = [speakerAudio];
    exporter.export(`${outputDir}/${speaker}.wav`);
  }
}
```

## Resources

- **WAV format**: https://en.wikipedia.org/wiki/WAV
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

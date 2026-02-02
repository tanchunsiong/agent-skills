# Audio Buffer Management

Efficiently manage audio buffers for RTMS streaming.

## Overview

Proper buffer management ensures smooth audio processing without dropouts or memory issues.

## Skills Needed

- **zoom-rtms** - Primary

## Buffer Strategies

| Strategy | Use Case | Trade-off |
|----------|----------|-----------|
| Ring buffer | Continuous streaming | Fixed memory, may drop |
| Growing buffer | Full recording | Memory grows |
| Chunked buffer | Batch processing | Periodic latency |

## Implementation

### JavaScript - Ring Buffer

```javascript
class RingBuffer {
  constructor(sizeInSeconds, sampleRate = 16000, bytesPerSample = 2) {
    this.size = sizeInSeconds * sampleRate * bytesPerSample;
    this.buffer = Buffer.alloc(this.size);
    this.writePos = 0;
    this.readPos = 0;
    this.available = 0;
  }
  
  write(data) {
    const dataLen = data.length;
    
    if (dataLen > this.size) {
      // Data larger than buffer - only keep latest
      data.copy(this.buffer, 0, dataLen - this.size);
      this.writePos = 0;
      this.readPos = 0;
      this.available = this.size;
      return;
    }
    
    // Check if we need to wrap
    const firstPart = Math.min(dataLen, this.size - this.writePos);
    const secondPart = dataLen - firstPart;
    
    data.copy(this.buffer, this.writePos, 0, firstPart);
    if (secondPart > 0) {
      data.copy(this.buffer, 0, firstPart, dataLen);
    }
    
    this.writePos = (this.writePos + dataLen) % this.size;
    this.available = Math.min(this.available + dataLen, this.size);
    
    // Push read pointer if overwritten
    if (this.available === this.size) {
      this.readPos = this.writePos;
    }
  }
  
  read(length) {
    if (length > this.available) {
      return null;
    }
    
    const result = Buffer.alloc(length);
    const firstPart = Math.min(length, this.size - this.readPos);
    const secondPart = length - firstPart;
    
    this.buffer.copy(result, 0, this.readPos, this.readPos + firstPart);
    if (secondPart > 0) {
      this.buffer.copy(result, firstPart, 0, secondPart);
    }
    
    this.readPos = (this.readPos + length) % this.size;
    this.available -= length;
    
    return result;
  }
  
  peek(length) {
    if (length > this.available) {
      return null;
    }
    
    const result = Buffer.alloc(length);
    let pos = this.readPos;
    
    for (let i = 0; i < length; i++) {
      result[i] = this.buffer[pos];
      pos = (pos + 1) % this.size;
    }
    
    return result;
  }
  
  getAvailable() {
    return this.available;
  }
  
  clear() {
    this.writePos = 0;
    this.readPos = 0;
    this.available = 0;
  }
}

// Usage
const audioBuffer = new RingBuffer(30); // 30 seconds

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
    audioBuffer.write(audioData);
    
    // Process in 1-second chunks
    const chunkSize = 16000 * 2; // 1 second at 16kHz, 16-bit
    while (audioBuffer.getAvailable() >= chunkSize) {
      const chunk = audioBuffer.read(chunkSize);
      processAudioChunk(chunk);
    }
  }
});
```

### JavaScript - Chunked Buffer Manager

```javascript
class ChunkedBufferManager {
  constructor(options = {}) {
    this.chunkDuration = options.chunkDuration || 1000; // ms
    this.sampleRate = options.sampleRate || 16000;
    this.bytesPerSample = 2;
    
    this.chunkSize = (this.chunkDuration / 1000) * this.sampleRate * this.bytesPerSample;
    this.currentChunk = Buffer.alloc(0);
    this.chunks = [];
    this.maxChunks = options.maxChunks || 600; // 10 minutes
    
    this.onChunkReady = options.onChunkReady;
  }
  
  addAudio(pcmData) {
    this.currentChunk = Buffer.concat([this.currentChunk, pcmData]);
    
    while (this.currentChunk.length >= this.chunkSize) {
      const chunk = this.currentChunk.slice(0, this.chunkSize);
      this.currentChunk = this.currentChunk.slice(this.chunkSize);
      
      this.chunks.push({
        data: chunk,
        timestamp: Date.now(),
        index: this.chunks.length
      });
      
      // Enforce max chunks
      if (this.chunks.length > this.maxChunks) {
        this.chunks.shift();
      }
      
      this.onChunkReady?.(chunk, this.chunks.length - 1);
    }
  }
  
  getChunk(index) {
    return this.chunks[index];
  }
  
  getChunks(startIndex, endIndex) {
    return this.chunks.slice(startIndex, endIndex);
  }
  
  getAllAudio() {
    const allChunks = this.chunks.map(c => c.data);
    if (this.currentChunk.length > 0) {
      allChunks.push(this.currentChunk);
    }
    return Buffer.concat(allChunks);
  }
  
  getLastNSeconds(seconds) {
    const bytesNeeded = seconds * this.sampleRate * this.bytesPerSample;
    const allAudio = this.getAllAudio();
    
    if (allAudio.length <= bytesNeeded) {
      return allAudio;
    }
    
    return allAudio.slice(-bytesNeeded);
  }
  
  getDuration() {
    const totalBytes = this.chunks.reduce((sum, c) => sum + c.data.length, 0) + this.currentChunk.length;
    return (totalBytes / this.bytesPerSample) / this.sampleRate;
  }
  
  clear() {
    this.chunks = [];
    this.currentChunk = Buffer.alloc(0);
  }
}

// Usage
const bufferManager = new ChunkedBufferManager({
  chunkDuration: 1000,
  onChunkReady: (chunk, index) => {
    console.log(`Chunk ${index} ready (${chunk.length} bytes)`);
    transcriber.sendAudio(chunk);
  }
});

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
    bufferManager.addAudio(audioData);
  }
});
```

### Python - Ring Buffer

```python
import numpy as np
import json
import base64
from threading import Lock

class RingBuffer:
    def __init__(self, size_seconds, sample_rate=16000, bytes_per_sample=2):
        self.size = size_seconds * sample_rate * bytes_per_sample
        self.buffer = bytearray(self.size)
        self.write_pos = 0
        self.read_pos = 0
        self.available = 0
        self.lock = Lock()
    
    def write(self, data):
        with self.lock:
            data_len = len(data)
            
            if data_len > self.size:
                # Keep only latest data
                self.buffer[:] = data[-self.size:]
                self.write_pos = 0
                self.read_pos = 0
                self.available = self.size
                return
            
            # Write data (may wrap)
            first_part = min(data_len, self.size - self.write_pos)
            self.buffer[self.write_pos:self.write_pos + first_part] = data[:first_part]
            
            if data_len > first_part:
                second_part = data_len - first_part
                self.buffer[:second_part] = data[first_part:]
            
            self.write_pos = (self.write_pos + data_len) % self.size
            self.available = min(self.available + data_len, self.size)
            
            if self.available == self.size:
                self.read_pos = self.write_pos
    
    def read(self, length):
        with self.lock:
            if length > self.available:
                return None
            
            result = bytearray(length)
            first_part = min(length, self.size - self.read_pos)
            result[:first_part] = self.buffer[self.read_pos:self.read_pos + first_part]
            
            if length > first_part:
                second_part = length - first_part
                result[first_part:] = self.buffer[:second_part]
            
            self.read_pos = (self.read_pos + length) % self.size
            self.available -= length
            
            return bytes(result)
    
    def get_available(self):
        return self.available
    
    def clear(self):
        with self.lock:
            self.write_pos = 0
            self.read_pos = 0
            self.available = 0

# Usage
buffer = RingBuffer(30)  # 30 seconds

async for message in ws:
    msg = json.loads(message)
    
    # Handle keep-alive
    if msg['msg_type'] == 12:
        await ws.send(json.dumps({"msg_type": 13, "timestamp": msg["timestamp"]}))
        continue
    
    # msg_type 14 = Audio (base64-encoded PCM)
    if msg['msg_type'] == 14:
        audio_data = base64.b64decode(msg['content'])
        buffer.write(audio_data)
        
        chunk_size = 16000 * 2  # 1 second
        while buffer.get_available() >= chunk_size:
            chunk = buffer.read(chunk_size)
            await process_audio(chunk)
```

## Memory Guidelines

| Duration | Memory (16kHz/16-bit) |
|----------|----------------------|
| 1 second | 32 KB |
| 1 minute | 1.9 MB |
| 10 minutes | 19 MB |
| 1 hour | 115 MB |

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/

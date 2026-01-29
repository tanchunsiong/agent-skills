# Receive Audio Stream

Receive and process raw audio data from RTMS.

## Overview

RTMS delivers audio as PCM 16-bit samples. Process for transcription, analysis, or recording.

## Skills Needed

- **zoom-rtms** - Primary

## Audio Format

| Property | Value |
|----------|-------|
| Format | PCM (Linear) |
| Bit depth | 16-bit signed |
| Sample rate | 16000 Hz or 32000 Hz |
| Channels | Mono |
| Byte order | Little-endian |

## Implementation

### JavaScript

```javascript
class RTMSAudioReceiver {
  constructor(options = {}) {
    this.sampleRate = options.sampleRate || 16000;
    this.channels = options.channels || 1;
    this.bitDepth = 16;
    this.buffer = Buffer.alloc(0);
    this.onAudioChunk = options.onAudioChunk;
  }
  
  handleMessage(data) {
     try {
       const message = JSON.parse(data.toString());
       const msgType = message.msg_type;
       
       if (msgType === 14) {
         // Audio data message
         const audioData = Buffer.from(message.data, 'base64');
         this.processAudio(audioData);
       } else if (msgType === 13) {
         // Keep-alive message
         console.log('Keep-alive received');
       }
     } catch (error) {
       console.error('Failed to parse message:', error);
     }
   }
  
  processAudio(audioBuffer) {
    // Append to buffer
    this.buffer = Buffer.concat([this.buffer, audioBuffer]);
    
    // Process in chunks (e.g., 100ms chunks)
    const chunkSize = (this.sampleRate * this.channels * 2) / 10; // 100ms
    
    while (this.buffer.length >= chunkSize) {
      const chunk = this.buffer.slice(0, chunkSize);
      this.buffer = this.buffer.slice(chunkSize);
      
      this.onAudioChunk?.(chunk, {
        sampleRate: this.sampleRate,
        channels: this.channels,
        bitDepth: this.bitDepth,
        duration: 100 // ms
      });
    }
  }
  
  // Convert PCM to Float32 for Web Audio API
  pcmToFloat32(pcmBuffer) {
    const samples = new Float32Array(pcmBuffer.length / 2);
    for (let i = 0; i < samples.length; i++) {
      const int16 = pcmBuffer.readInt16LE(i * 2);
      samples[i] = int16 / 32768;
    }
    return samples;
  }
  
  // Get audio level (RMS)
  getAudioLevel(pcmBuffer) {
    let sum = 0;
    const samples = pcmBuffer.length / 2;
    
    for (let i = 0; i < samples; i++) {
      const sample = pcmBuffer.readInt16LE(i * 2) / 32768;
      sum += sample * sample;
    }
    
    return Math.sqrt(sum / samples);
  }
}

// Usage
const receiver = new RTMSAudioReceiver({
  sampleRate: 16000,
  onAudioChunk: (chunk, info) => {
    const level = receiver.getAudioLevel(chunk);
    console.log(`Audio chunk: ${info.duration}ms, level: ${level.toFixed(3)}`);
    
    // Send to transcription service
    transcriptionService.sendAudio(chunk);
  }
});

ws.on('message', (data) => {
  receiver.handleMessage(data);
});
```

### Python

```python
import struct
import numpy as np

class RTMSAudioReceiver:
    def __init__(self, sample_rate=16000, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.bit_depth = 16
        self.buffer = b''
        self.on_audio_chunk = None
    
    def handle_message(self, data):
         try:
             import json
             import base64
             
             message = json.loads(data.decode('utf-8'))
             msg_type = message.get('msg_type')
             
             if msg_type == 14:
                 # Audio data message
                 audio_data = base64.b64decode(message.get('data', ''))
                 self.process_audio(audio_data)
             elif msg_type == 13:
                 # Keep-alive message
                 print('Keep-alive received')
         except (json.JSONDecodeError, UnicodeDecodeError) as error:
             print(f'Failed to parse message: {error}')
    
    def process_audio(self, audio_buffer):
        self.buffer += audio_buffer
        
        # Process in 100ms chunks
        chunk_size = int(self.sample_rate * self.channels * 2 / 10)
        
        while len(self.buffer) >= chunk_size:
            chunk = self.buffer[:chunk_size]
            self.buffer = self.buffer[chunk_size:]
            
            if self.on_audio_chunk:
                self.on_audio_chunk(chunk, {
                    'sample_rate': self.sample_rate,
                    'channels': self.channels,
                    'bit_depth': self.bit_depth,
                    'duration': 100
                })
    
    def pcm_to_numpy(self, pcm_buffer):
        """Convert PCM bytes to numpy array"""
        return np.frombuffer(pcm_buffer, dtype=np.int16).astype(np.float32) / 32768
    
    def get_audio_level(self, pcm_buffer):
        """Calculate RMS audio level"""
        samples = self.pcm_to_numpy(pcm_buffer)
        return np.sqrt(np.mean(samples ** 2))
    
    def resample(self, pcm_buffer, target_rate):
        """Resample audio to different rate"""
        from scipy import signal
        
        samples = self.pcm_to_numpy(pcm_buffer)
        num_samples = int(len(samples) * target_rate / self.sample_rate)
        resampled = signal.resample(samples, num_samples)
        
        return (resampled * 32768).astype(np.int16).tobytes()

# Usage
receiver = RTMSAudioReceiver(sample_rate=16000)

def on_chunk(chunk, info):
    level = receiver.get_audio_level(chunk)
    print(f"Audio: {info['duration']}ms, level: {level:.3f}")
    
    # Send to transcription
    transcription_service.send_audio(chunk)

receiver.on_audio_chunk = on_chunk

async for message in ws:
    receiver.handle_message(message)
```

## Audio Processing Tips

| Task | Approach |
|------|----------|
| Transcription | Send chunks to Whisper/Deepgram |
| Voice detection | Check RMS level > threshold |
| Noise reduction | Apply spectral subtraction |
| Resampling | Use scipy.signal.resample |

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/

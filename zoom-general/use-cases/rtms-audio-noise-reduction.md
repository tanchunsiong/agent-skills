# Audio Noise Reduction

Apply noise reduction to RTMS audio streams for cleaner transcription.

## Overview

Reduce background noise from RTMS audio to improve transcription accuracy and audio quality.

## Skills Needed

- **zoom-rtms** - Primary

## Noise Reduction Methods

| Method | Quality | CPU | Real-Time |
|--------|---------|-----|-----------|
| Spectral Subtraction | Good | Low | Yes |
| RNNoise | Excellent | Medium | Yes |
| DeepFilterNet | Best | High | Yes |

## Implementation

### JavaScript - RNNoise

```javascript
const { RNNoise } = require('rnnoise-wasm');

class NoiseReducer {
  constructor() {
    this.rnnoise = null;
    this.frameSize = 480; // RNNoise frame size (30ms at 16kHz)
    this.buffer = Buffer.alloc(0);
  }
  
  async init() {
    this.rnnoise = await RNNoise.create();
    console.log('RNNoise initialized');
  }
  
  process(pcmData) {
    this.buffer = Buffer.concat([this.buffer, pcmData]);
    
    const processedChunks = [];
    const bytesPerFrame = this.frameSize * 2; // 16-bit audio
    
    while (this.buffer.length >= bytesPerFrame) {
      const frame = this.buffer.slice(0, bytesPerFrame);
      this.buffer = this.buffer.slice(bytesPerFrame);
      
      // Convert to float
      const floatFrame = new Float32Array(this.frameSize);
      for (let i = 0; i < this.frameSize; i++) {
        floatFrame[i] = frame.readInt16LE(i * 2) / 32768;
      }
      
      // Apply noise reduction
      const vadProb = this.rnnoise.processFrame(floatFrame);
      
      // Convert back to PCM
      const processedFrame = Buffer.alloc(bytesPerFrame);
      for (let i = 0; i < this.frameSize; i++) {
        const sample = Math.max(-1, Math.min(1, floatFrame[i]));
        processedFrame.writeInt16LE(Math.round(sample * 32767), i * 2);
      }
      
      processedChunks.push({
        audio: processedFrame,
        vadProbability: vadProb
      });
    }
    
    return processedChunks;
  }
  
  destroy() {
    if (this.rnnoise) {
      this.rnnoise.destroy();
    }
  }
}

// Usage with RTMS
const noiseReducer = new NoiseReducer();
await noiseReducer.init();

ws.on('message', (data) => {
  const msg = JSON.parse(data.toString());
  
  // Handle keep-alive
  if (msg.msg_type === 12) {
    ws.send(JSON.stringify({ msg_type: 13, timestamp: msg.timestamp }));
    return;
  }
  
  // Process audio (msg_type 14 = audio with base64-encoded PCM)
  if (msg.msg_type === 14) {
    const audioData = Buffer.from(msg.content, 'base64');
    const processed = noiseReducer.process(audioData);
    
    for (const chunk of processed) {
      // Only process if voice detected
      if (chunk.vadProbability > 0.5) {
        transcriber.sendAudio(chunk.audio);
      }
    }
  }
});
```

### Python - noisereduce Library

```python
import noisereduce as nr
import numpy as np
import json
import base64
from collections import deque

class NoiseReducer:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
        self.noise_profile = None
        self.buffer = deque(maxlen=sample_rate * 2)  # 2 seconds
        self.calibrated = False
    
    def calibrate(self, noise_sample):
        """Capture noise profile from silent period"""
        audio = np.frombuffer(noise_sample, dtype=np.int16).astype(np.float32)
        self.noise_profile = audio
        self.calibrated = True
        print("Noise profile calibrated")
    
    def process(self, pcm_data):
        """Apply noise reduction to audio"""
        audio = np.frombuffer(pcm_data, dtype=np.int16).astype(np.float32)
        
        if self.calibrated:
            # Stationary noise reduction
            reduced = nr.reduce_noise(
                y=audio,
                sr=self.sample_rate,
                y_noise=self.noise_profile,
                prop_decrease=0.8,
                stationary=True
            )
        else:
            # Non-stationary (auto-detect noise)
            reduced = nr.reduce_noise(
                y=audio,
                sr=self.sample_rate,
                stationary=False,
                prop_decrease=0.6
            )
        
        # Convert back to int16
        return reduced.astype(np.int16).tobytes()
    
    def process_realtime(self, pcm_data):
        """Process in real-time with windowing"""
        audio = np.frombuffer(pcm_data, dtype=np.int16)
        self.buffer.extend(audio)
        
        if len(self.buffer) < self.sample_rate:
            # Not enough data yet
            return pcm_data
        
        # Process with context
        context = np.array(self.buffer)
        reduced = nr.reduce_noise(
            y=context.astype(np.float32),
            sr=self.sample_rate,
            stationary=False,
            prop_decrease=0.6
        )
        
        # Return only the new portion
        new_samples = len(audio)
        return reduced[-new_samples:].astype(np.int16).tobytes()

# Usage
reducer = NoiseReducer(sample_rate=16000)

# Calibrate with first 2 seconds (assuming silence)
calibration_audio = b''
async for data in ws:
    msg = json.loads(data)
    
    # Handle keep-alive
    if msg['msg_type'] == 12:
        await ws.send(json.dumps({"msg_type": 13, "timestamp": msg["timestamp"]}))
        continue
    
    # Process audio (msg_type 14 = audio with base64-encoded PCM)
    if msg['msg_type'] == 14:
        audio_data = base64.b64decode(msg['content'])
        calibration_audio += audio_data
        if len(calibration_audio) >= 32000 * 2:  # 2 seconds
            reducer.calibrate(calibration_audio)
            break

# Process rest of audio
async for data in ws:
    msg = json.loads(data)
    
    # Handle keep-alive
    if msg['msg_type'] == 12:
        await ws.send(json.dumps({"msg_type": 13, "timestamp": msg["timestamp"]}))
        continue
    
    # Process audio
    if msg['msg_type'] == 14:
        audio_data = base64.b64decode(msg['content'])
        clean_audio = reducer.process(audio_data)
        await transcriber.send_audio(clean_audio)
```

### Python - DeepFilterNet (Best Quality)

```python
from df import enhance, init_df
import json
import base64

class DeepFilterNoiseReducer:
    def __init__(self):
        self.model, self.df_state, _ = init_df()
        self.sample_rate = self.df_state.sr()
    
    def process(self, pcm_data):
        """Process audio with DeepFilterNet"""
        import torch
        import torchaudio
        
        # Convert PCM to tensor
        audio = torch.frombuffer(pcm_data, dtype=torch.int16).float() / 32768
        audio = audio.unsqueeze(0)  # Add batch dimension
        
        # Resample if needed
        if self.sample_rate != 16000:
            audio = torchaudio.functional.resample(audio, 16000, self.sample_rate)
        
        # Enhance
        enhanced = enhance(self.model, self.df_state, audio)
        
        # Convert back
        enhanced = (enhanced.squeeze() * 32767).to(torch.int16)
        return enhanced.numpy().tobytes()

# Usage
reducer = DeepFilterNoiseReducer()

async for data in ws:
    msg = json.loads(data)
    
    # Handle keep-alive
    if msg['msg_type'] == 12:
        await ws.send(json.dumps({"msg_type": 13, "timestamp": msg["timestamp"]}))
        continue
    
    # Process audio (msg_type 14 = audio with base64-encoded PCM)
    if msg['msg_type'] == 14:
        audio_data = base64.b64decode(msg['content'])
        clean_audio = reducer.process(audio_data)
        await transcriber.send_audio(clean_audio)
```

## Best Practices

| Scenario | Recommendation |
|----------|----------------|
| Office noise | RNNoise or noisereduce |
| Heavy background | DeepFilterNet |
| Low latency needed | RNNoise (real-time) |
| Best quality | DeepFilterNet (GPU) |

## Resources

- **RNNoise**: https://jmvalin.ca/demo/rnnoise/
- **noisereduce**: https://github.com/timsainb/noisereduce
- **DeepFilterNet**: https://github.com/Rikorose/DeepFilterNet
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

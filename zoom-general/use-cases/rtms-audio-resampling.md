# Audio Resampling

Resample RTMS audio to different sample rates for various services.

## Overview

Some services require specific sample rates. Resample RTMS audio (16kHz/32kHz) to match requirements.

## Skills Needed

- **zoom-rtms** - Primary

## Common Sample Rates

| Service | Required Rate |
|---------|---------------|
| Deepgram | 8-48 kHz |
| AssemblyAI | 8-48 kHz |
| OpenAI Whisper | 16 kHz |
| Google Speech | 8-48 kHz |
| Telephony | 8 kHz |
| CD Quality | 44.1 kHz |

## Implementation

### JavaScript - Linear Interpolation

```javascript
class AudioResampler {
  constructor(inputRate, outputRate) {
    this.inputRate = inputRate;
    this.outputRate = outputRate;
    this.ratio = outputRate / inputRate;
  }
  
  resample(pcmBuffer) {
    const inputSamples = pcmBuffer.length / 2;
    const outputSamples = Math.floor(inputSamples * this.ratio);
    const output = Buffer.alloc(outputSamples * 2);
    
    for (let i = 0; i < outputSamples; i++) {
      const srcIndex = i / this.ratio;
      const srcIndexInt = Math.floor(srcIndex);
      const fraction = srcIndex - srcIndexInt;
      
      // Get surrounding samples
      const sample1 = pcmBuffer.readInt16LE(srcIndexInt * 2);
      const sample2Index = Math.min(srcIndexInt + 1, inputSamples - 1);
      const sample2 = pcmBuffer.readInt16LE(sample2Index * 2);
      
      // Linear interpolation
      const interpolated = sample1 + fraction * (sample2 - sample1);
      output.writeInt16LE(Math.round(interpolated), i * 2);
    }
    
    return output;
  }
}

// Usage
const resampler = new AudioResampler(16000, 8000);

ws.on('message', (data) => {
  const msg = JSON.parse(data.toString());
  
  // Handle keep-alive
  if (msg.msg_type === 12) {
    ws.send(JSON.stringify({ msg_type: 13, timestamp: msg.timestamp }));
    return;
  }
  
  // Handle audio data
  if (msg.msg_type === 14) {
    const audio16k = Buffer.from(msg.content, 'base64');
    const audio8k = resampler.resample(audio16k);
    telephonyService.sendAudio(audio8k);
  }
});
```

### JavaScript - High Quality with speex-resampler

```javascript
const { SpeexResampler } = require('speex-resampler');

class HighQualityResampler {
  constructor(inputRate, outputRate, channels = 1, quality = 5) {
    // Quality: 0-10 (0=fastest, 10=best)
    this.resampler = new SpeexResampler(channels, inputRate, outputRate, quality);
    this.inputRate = inputRate;
    this.outputRate = outputRate;
  }
  
  resample(pcmBuffer) {
    // Convert to Int16Array
    const input = new Int16Array(pcmBuffer.buffer, pcmBuffer.byteOffset, pcmBuffer.length / 2);
    
    // Resample
    const output = this.resampler.processInterleaved(input);
    
    // Convert back to Buffer
    return Buffer.from(output.buffer);
  }
  
  destroy() {
    this.resampler.destroy();
  }
}

// Usage
const hqResampler = new HighQualityResampler(16000, 44100, 1, 7);

ws.on('message', (data) => {
  const msg = JSON.parse(data.toString());
  
  // Handle keep-alive
  if (msg.msg_type === 12) {
    ws.send(JSON.stringify({ msg_type: 13, timestamp: msg.timestamp }));
    return;
  }
  
  // Handle audio data
  if (msg.msg_type === 14) {
    const audio16k = Buffer.from(msg.content, 'base64');
    const audio44k = hqResampler.resample(audio16k);
    cdQualityRecorder.write(audio44k);
  }
});
```

### Python - scipy.signal

```python
from scipy import signal
import numpy as np

class AudioResampler:
    def __init__(self, input_rate, output_rate):
        self.input_rate = input_rate
        self.output_rate = output_rate
        self.ratio = output_rate / input_rate
    
    def resample(self, pcm_data):
        """Resample audio using polyphase filtering"""
        # Convert to numpy
        audio = np.frombuffer(pcm_data, dtype=np.int16).astype(np.float32)
        
        # Calculate output length
        output_length = int(len(audio) * self.ratio)
        
        # Resample using polyphase filter (high quality)
        resampled = signal.resample_poly(
            audio,
            self.output_rate,
            self.input_rate
        )
        
        # Convert back to int16
        return resampled.astype(np.int16).tobytes()
    
    def resample_simple(self, pcm_data):
        """Fast resampling using simple interpolation"""
        audio = np.frombuffer(pcm_data, dtype=np.int16).astype(np.float32)
        output_length = int(len(audio) * self.ratio)
        
        resampled = signal.resample(audio, output_length)
        return resampled.astype(np.int16).tobytes()

# Usage
import json
import base64

resampler = AudioResampler(16000, 8000)

async for message in ws:
    msg = json.loads(message)
    
    # Handle keep-alive
    if msg['msg_type'] == 12:
        await ws.send(json.dumps({"msg_type": 13, "timestamp": msg["timestamp"]}))
        continue
    
    # Handle audio data
    if msg['msg_type'] == 14:
        audio_16k = base64.b64decode(msg['content'])
        audio_8k = resampler.resample(audio_16k)
        await telephony_service.send(audio_8k)
```

### Python - librosa (Best Quality)

```python
import librosa
import numpy as np

class LibrosaResampler:
    def __init__(self, input_rate, output_rate):
        self.input_rate = input_rate
        self.output_rate = output_rate
    
    def resample(self, pcm_data):
        """High-quality resampling with librosa"""
        # Convert to float
        audio = np.frombuffer(pcm_data, dtype=np.int16).astype(np.float32) / 32768
        
        # Resample
        resampled = librosa.resample(
            audio,
            orig_sr=self.input_rate,
            target_sr=self.output_rate,
            res_type='kaiser_best'  # Highest quality
        )
        
        # Convert back
        return (resampled * 32767).astype(np.int16).tobytes()
    
    def resample_fast(self, pcm_data):
        """Faster resampling with slightly lower quality"""
        audio = np.frombuffer(pcm_data, dtype=np.int16).astype(np.float32) / 32768
        
        resampled = librosa.resample(
            audio,
            orig_sr=self.input_rate,
            target_sr=self.output_rate,
            res_type='soxr_hq'  # Good balance
        )
        
        return (resampled * 32767).astype(np.int16).tobytes()

# Usage
resampler = LibrosaResampler(16000, 44100)
audio_cd = resampler.resample(audio_16k)
```

### Streaming Resampler

```python
import numpy as np
from scipy import signal

class StreamingResampler:
    def __init__(self, input_rate, output_rate):
        self.input_rate = input_rate
        self.output_rate = output_rate
        self.gcd = np.gcd(input_rate, output_rate)
        self.up = output_rate // self.gcd
        self.down = input_rate // self.gcd
        
        # State for continuity
        self.zi = None
    
    def process(self, pcm_data):
        """Process chunk with state preservation"""
        audio = np.frombuffer(pcm_data, dtype=np.int16).astype(np.float32)
        
        # Upsample
        upsampled = np.zeros(len(audio) * self.up)
        upsampled[::self.up] = audio
        
        # Design lowpass filter
        if self.zi is None:
            b, a = signal.butter(8, 0.5 / self.up)
            self.zi = signal.lfilter_zi(b, a)
        
        # Filter
        filtered, self.zi = signal.lfilter(b, a, upsampled, zi=self.zi * upsampled[0])
        
        # Downsample
        resampled = filtered[::self.down]
        
        return resampled.astype(np.int16).tobytes()
```

## Quality Comparison

| Method | Quality | Speed | Use Case |
|--------|---------|-------|----------|
| Linear interpolation | Fair | Fast | Real-time, low CPU |
| scipy.signal.resample | Good | Medium | General purpose |
| scipy.signal.resample_poly | Very Good | Medium | Ratio conversion |
| librosa kaiser_best | Excellent | Slow | High quality |
| Speex resampler | Excellent | Fast | Real-time, quality |

## Resources

- **librosa**: https://librosa.org/
- **scipy.signal**: https://docs.scipy.org/doc/scipy/reference/signal.html
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

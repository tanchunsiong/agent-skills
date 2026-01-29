# Decode PCM Audio

Decode and process PCM audio data from RTMS streams.

## Overview

RTMS delivers audio as PCM 16-bit signed integers. Decode for playback, analysis, or conversion.

## Skills Needed

- **zoom-rtms** - Primary

## PCM Format Details

```
PCM 16-bit Little-Endian:
┌────────┬────────┬────────┬────────┐
│ Sample │ Sample │ Sample │ Sample │
│   1    │   2    │   3    │   N    │
│ 2 bytes│ 2 bytes│ 2 bytes│ 2 bytes│
└────────┴────────┴────────┴────────┘
Value range: -32768 to 32767
```

## Implementation

### JavaScript

```javascript
class PCMDecoder {
  constructor(sampleRate = 16000, channels = 1) {
    this.sampleRate = sampleRate;
    this.channels = channels;
  }
  
  // Decode PCM to signed 16-bit integers
  decodeToInt16(buffer) {
    const samples = new Int16Array(buffer.length / 2);
    for (let i = 0; i < samples.length; i++) {
      samples[i] = buffer.readInt16LE(i * 2);
    }
    return samples;
  }
  
  // Decode PCM to normalized float (-1.0 to 1.0)
  decodeToFloat32(buffer) {
    const int16 = this.decodeToInt16(buffer);
    const float32 = new Float32Array(int16.length);
    for (let i = 0; i < int16.length; i++) {
      float32[i] = int16[i] / 32768;
    }
    return float32;
  }
  
  // Decode PCM to 8-bit unsigned (for simple playback)
  decodeToUint8(buffer) {
    const int16 = this.decodeToInt16(buffer);
    const uint8 = new Uint8Array(int16.length);
    for (let i = 0; i < int16.length; i++) {
      uint8[i] = Math.floor((int16[i] + 32768) / 256);
    }
    return uint8;
  }
  
  // Get duration in seconds
  getDuration(buffer) {
    const samples = buffer.length / 2 / this.channels;
    return samples / this.sampleRate;
  }
  
  // Calculate peak amplitude
  getPeakAmplitude(buffer) {
    const samples = this.decodeToInt16(buffer);
    let peak = 0;
    for (let i = 0; i < samples.length; i++) {
      const abs = Math.abs(samples[i]);
      if (abs > peak) peak = abs;
    }
    return peak / 32768;
  }
  
  // Calculate RMS (average loudness)
  getRMS(buffer) {
    const samples = this.decodeToFloat32(buffer);
    let sum = 0;
    for (let i = 0; i < samples.length; i++) {
      sum += samples[i] * samples[i];
    }
    return Math.sqrt(sum / samples.length);
  }
  
  // Convert to decibels
  toDecibels(linearValue) {
    return 20 * Math.log10(Math.max(linearValue, 0.0001));
  }
}

// Usage
const decoder = new PCMDecoder(16000, 1);

ws.on('message', (data) => {
  try {
    const msg = JSON.parse(data.toString());
    
    // Handle audio data (msg_type 14 = base64 encoded PCM)
    if (msg.msg_type === 14 && msg.content) {
      const pcmData = Buffer.from(msg.content, 'base64');
      
      const float32 = decoder.decodeToFloat32(pcmData);
      const duration = decoder.getDuration(pcmData);
      const rms = decoder.getRMS(pcmData);
      const db = decoder.toDecibels(rms);
      
      console.log(`Audio: ${duration.toFixed(2)}s, ${db.toFixed(1)} dB`);
      
      // Use float32 for Web Audio API, ML models, etc.
      audioProcessor.process(float32);
    }
    
    // Handle keep-alive (msg_type 13)
    if (msg.msg_type === 13) {
      console.log('Keep-alive received');
    }
  } catch (err) {
    console.error('Failed to parse message:', err);
  }
});
```

### Python

```python
import struct
import numpy as np

class PCMDecoder:
    def __init__(self, sample_rate=16000, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
    
    def decode_to_int16(self, buffer):
        """Decode PCM bytes to int16 numpy array"""
        return np.frombuffer(buffer, dtype='<i2')  # Little-endian int16
    
    def decode_to_float32(self, buffer):
        """Decode PCM bytes to normalized float32 (-1.0 to 1.0)"""
        int16 = self.decode_to_int16(buffer)
        return int16.astype(np.float32) / 32768
    
    def decode_to_float64(self, buffer):
        """Decode PCM bytes to float64 for high precision"""
        int16 = self.decode_to_int16(buffer)
        return int16.astype(np.float64) / 32768
    
    def get_duration(self, buffer):
        """Get duration in seconds"""
        samples = len(buffer) // 2 // self.channels
        return samples / self.sample_rate
    
    def get_peak_amplitude(self, buffer):
        """Get peak amplitude (0.0 to 1.0)"""
        samples = self.decode_to_int16(buffer)
        return np.abs(samples).max() / 32768
    
    def get_rms(self, buffer):
        """Calculate RMS (root mean square) loudness"""
        samples = self.decode_to_float32(buffer)
        return np.sqrt(np.mean(samples ** 2))
    
    def to_decibels(self, linear_value):
        """Convert linear amplitude to decibels"""
        return 20 * np.log10(max(linear_value, 0.0001))
    
    def encode_to_pcm(self, float_samples):
        """Encode float32 array back to PCM bytes"""
        int16 = (float_samples * 32767).astype(np.int16)
        return int16.tobytes()

# Usage
import json
import base64

decoder = PCMDecoder(16000, 1)

async for message in ws:
    try:
        msg = json.loads(message)
        
        # Handle audio data (msg_type 14 = base64 encoded PCM)
        if msg.get('msg_type') == 14 and msg.get('content'):
            pcm_data = base64.b64decode(msg['content'])
            
            float32 = decoder.decode_to_float32(pcm_data)
            duration = decoder.get_duration(pcm_data)
            rms = decoder.get_rms(pcm_data)
            db = decoder.to_decibels(rms)
            
            print(f"Audio: {duration:.2f}s, {db:.1f} dB")
            
            # Process with numpy/scipy/ML
            audio_processor.process(float32)
        
        # Handle keep-alive (msg_type 13)
        if msg.get('msg_type') == 13:
            print('Keep-alive received')
    except json.JSONDecodeError as err:
        print(f'Failed to parse message: {err}')
```

### Using struct for Manual Decoding

```python
import struct

def decode_pcm_manual(buffer):
    """Manually decode PCM using struct"""
    num_samples = len(buffer) // 2
    format_string = f'<{num_samples}h'  # Little-endian, signed short
    samples = struct.unpack(format_string, buffer)
    return samples

# Decode single sample
def decode_sample(two_bytes):
    return struct.unpack('<h', two_bytes)[0]
```

## Format Conversions

| From | To | Method |
|------|-----|--------|
| PCM 16-bit | Float32 | Divide by 32768 |
| PCM 16-bit | Uint8 | Add 32768, divide by 256 |
| Float32 | PCM 16-bit | Multiply by 32767, cast to int16 |

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/
- **PCM format**: https://en.wikipedia.org/wiki/Pulse-code_modulation

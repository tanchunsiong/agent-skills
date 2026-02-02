# Audio Level Monitoring

Monitor audio levels in real-time from RTMS streams.

## Overview

Track audio levels for visualization, silence detection, and quality monitoring.

## Skills Needed

- **zoom-rtms** - Primary

## Audio Metrics

| Metric | Description | Range |
|--------|-------------|-------|
| RMS | Root Mean Square (average loudness) | 0.0 - 1.0 |
| Peak | Maximum amplitude | 0.0 - 1.0 |
| dB | Decibels (logarithmic) | -∞ to 0 |
| dBFS | dB Full Scale | -∞ to 0 |

## Implementation

### JavaScript

```javascript
class AudioLevelMonitor {
  constructor(options = {}) {
    this.sampleRate = options.sampleRate || 16000;
    this.smoothingFactor = options.smoothingFactor || 0.8;
    this.silenceThreshold = options.silenceThreshold || -50; // dB
    
    this.currentRMS = 0;
    this.currentPeak = 0;
    this.isSilent = true;
    
    this.history = [];
    this.historySize = options.historySize || 100;
    
    this.onLevelChange = options.onLevelChange;
    this.onSilenceStart = options.onSilenceStart;
    this.onSilenceEnd = options.onSilenceEnd;
  }
  
  process(pcmBuffer) {
    const samples = pcmBuffer.length / 2;
    let sum = 0;
    let peak = 0;
    
    for (let i = 0; i < samples; i++) {
      const sample = Math.abs(pcmBuffer.readInt16LE(i * 2) / 32768);
      sum += sample * sample;
      if (sample > peak) peak = sample;
    }
    
    // Calculate RMS
    const rms = Math.sqrt(sum / samples);
    
    // Apply smoothing
    this.currentRMS = this.currentRMS * this.smoothingFactor + rms * (1 - this.smoothingFactor);
    this.currentPeak = Math.max(this.currentPeak * 0.95, peak); // Slow decay
    
    // Calculate dB
    const db = this.toDb(this.currentRMS);
    const peakDb = this.toDb(this.currentPeak);
    
    // Check silence
    const wasSilent = this.isSilent;
    this.isSilent = db < this.silenceThreshold;
    
    if (wasSilent && !this.isSilent) {
      this.onSilenceEnd?.();
    } else if (!wasSilent && this.isSilent) {
      this.onSilenceStart?.();
    }
    
    // Store history
    const level = {
      rms: this.currentRMS,
      peak: this.currentPeak,
      db,
      peakDb,
      isSilent: this.isSilent,
      timestamp: Date.now()
    };
    
    this.history.push(level);
    if (this.history.length > this.historySize) {
      this.history.shift();
    }
    
    this.onLevelChange?.(level);
    
    return level;
  }
  
  toDb(linear) {
    return 20 * Math.log10(Math.max(linear, 0.0001));
  }
  
  toLinear(db) {
    return Math.pow(10, db / 20);
  }
  
  getAverageLevel() {
    if (this.history.length === 0) return null;
    
    const sum = this.history.reduce((acc, h) => acc + h.rms, 0);
    return sum / this.history.length;
  }
  
  getSilencePercentage() {
    if (this.history.length === 0) return 0;
    
    const silentCount = this.history.filter(h => h.isSilent).length;
    return (silentCount / this.history.length) * 100;
  }
  
  reset() {
    this.currentRMS = 0;
    this.currentPeak = 0;
    this.history = [];
  }
}

// Usage
const monitor = new AudioLevelMonitor({
  silenceThreshold: -45,
  onLevelChange: (level) => {
    // Update UI
    updateVUMeter(level.db);
  },
  onSilenceStart: () => {
    console.log('Silence detected');
  },
  onSilenceEnd: () => {
    console.log('Audio activity resumed');
  }
});

ws.on('message', (data) => {
  const msg = JSON.parse(data.toString());
  
  // Handle keep-alive
  if (msg.msg_type === 12) {
    ws.send(JSON.stringify({ msg_type: 13, timestamp: msg.timestamp }));
    return;
  }
  
  // Process audio data (msg_type 14)
  if (msg.msg_type === 14) {
    const audioData = Buffer.from(msg.content, 'base64');
    const level = monitor.process(audioData);
    console.log(`Level: ${level.db.toFixed(1)} dB, Peak: ${level.peakDb.toFixed(1)} dB`);
  }
});

// VU Meter visualization
function updateVUMeter(db) {
  // Convert dB to percentage (0 dB = 100%, -60 dB = 0%)
  const percentage = Math.max(0, Math.min(100, (db + 60) / 60 * 100));
  
  // Update meter bar
  meterElement.style.width = `${percentage}%`;
  
  // Color coding
  if (db > -6) {
    meterElement.style.backgroundColor = 'red';    // Clipping
  } else if (db > -12) {
    meterElement.style.backgroundColor = 'yellow'; // Hot
  } else {
    meterElement.style.backgroundColor = 'green';  // Normal
  }
}
```

### Python

```python
import numpy as np
import json
import base64
from collections import deque
from dataclasses import dataclass
from typing import Optional, Callable

@dataclass
class AudioLevel:
    rms: float
    peak: float
    db: float
    peak_db: float
    is_silent: bool
    timestamp: float

class AudioLevelMonitor:
    def __init__(
        self,
        sample_rate: int = 16000,
        smoothing_factor: float = 0.8,
        silence_threshold: float = -50,
        history_size: int = 100
    ):
        self.sample_rate = sample_rate
        self.smoothing_factor = smoothing_factor
        self.silence_threshold = silence_threshold
        
        self.current_rms = 0.0
        self.current_peak = 0.0
        self.is_silent = True
        
        self.history = deque(maxlen=history_size)
        
        self.on_level_change: Optional[Callable] = None
        self.on_silence_start: Optional[Callable] = None
        self.on_silence_end: Optional[Callable] = None
    
    def process(self, pcm_data: bytes) -> AudioLevel:
        import time
        
        # Convert to numpy
        samples = np.frombuffer(pcm_data, dtype=np.int16).astype(np.float32) / 32768
        
        # Calculate RMS and peak
        rms = np.sqrt(np.mean(samples ** 2))
        peak = np.abs(samples).max()
        
        # Apply smoothing
        self.current_rms = (
            self.current_rms * self.smoothing_factor +
            rms * (1 - self.smoothing_factor)
        )
        self.current_peak = max(self.current_peak * 0.95, peak)
        
        # Calculate dB
        db = self.to_db(self.current_rms)
        peak_db = self.to_db(self.current_peak)
        
        # Check silence
        was_silent = self.is_silent
        self.is_silent = db < self.silence_threshold
        
        if was_silent and not self.is_silent:
            if self.on_silence_end:
                self.on_silence_end()
        elif not was_silent and self.is_silent:
            if self.on_silence_start:
                self.on_silence_start()
        
        # Create level object
        level = AudioLevel(
            rms=self.current_rms,
            peak=self.current_peak,
            db=db,
            peak_db=peak_db,
            is_silent=self.is_silent,
            timestamp=time.time()
        )
        
        self.history.append(level)
        
        if self.on_level_change:
            self.on_level_change(level)
        
        return level
    
    @staticmethod
    def to_db(linear: float) -> float:
        return 20 * np.log10(max(linear, 0.0001))
    
    @staticmethod
    def to_linear(db: float) -> float:
        return 10 ** (db / 20)
    
    def get_average_level(self) -> Optional[float]:
        if not self.history:
            return None
        return sum(h.rms for h in self.history) / len(self.history)
    
    def get_silence_percentage(self) -> float:
        if not self.history:
            return 0
        silent_count = sum(1 for h in self.history if h.is_silent)
        return (silent_count / len(self.history)) * 100
    
    def reset(self):
        self.current_rms = 0.0
        self.current_peak = 0.0
        self.history.clear()

# Usage
monitor = AudioLevelMonitor(silence_threshold=-45)

def on_level(level):
    print(f"Level: {level.db:.1f} dB, Peak: {level.peak_db:.1f} dB")

monitor.on_level_change = on_level
monitor.on_silence_start = lambda: print("Silence detected")
monitor.on_silence_end = lambda: print("Audio resumed")

async for message in ws:
    msg = json.loads(message)
    
    # Handle keep-alive
    if msg['msg_type'] == 12:
        await ws.send(json.dumps({"msg_type": 13, "timestamp": msg["timestamp"]}))
        continue
    
    # Process audio data (msg_type 14)
    if msg['msg_type'] == 14:
        audio_data = base64.b64decode(msg['content'])
        level = monitor.process(audio_data)
```

## Level Reference

| Level (dBFS) | Description |
|--------------|-------------|
| 0 dB | Maximum (clipping) |
| -6 dB | Very loud |
| -12 dB | Loud (target peak) |
| -20 dB | Normal speech |
| -40 dB | Quiet |
| -60 dB | Very quiet |
| < -60 dB | Essentially silent |

## Resources

- **Audio metering**: https://en.wikipedia.org/wiki/Audio_metering
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

# Voice Activity Detection (VAD)

Detect speech segments in RTMS audio streams.

## Overview

Use VAD to identify when someone is speaking, reducing processing costs and improving transcription quality.

## Skills Needed

- **zoom-rtms** - Primary

## VAD Benefits

- Reduce transcription API costs (only send speech)
- Improve transcript accuracy (skip silence/noise)
- Enable speaker turn detection
- Trigger recording on voice

## Implementation

### JavaScript - Energy-Based VAD

```javascript
class SimpleVAD {
  constructor(options = {}) {
    this.threshold = options.threshold || 0.01;
    this.minSpeechDuration = options.minSpeechDuration || 250; // ms
    this.minSilenceDuration = options.minSilenceDuration || 500; // ms
    this.sampleRate = options.sampleRate || 16000;
    
    this.isSpeaking = false;
    this.speechStart = null;
    this.silenceStart = null;
    this.onSpeechStart = options.onSpeechStart;
    this.onSpeechEnd = options.onSpeechEnd;
  }
  
  process(pcmBuffer) {
    const rms = this.calculateRMS(pcmBuffer);
    const isVoice = rms > this.threshold;
    const now = Date.now();
    
    if (isVoice) {
      this.silenceStart = null;
      
      if (!this.isSpeaking) {
        if (!this.speechStart) {
          this.speechStart = now;
        } else if (now - this.speechStart >= this.minSpeechDuration) {
          this.isSpeaking = true;
          this.onSpeechStart?.();
        }
      }
    } else {
      this.speechStart = null;
      
      if (this.isSpeaking) {
        if (!this.silenceStart) {
          this.silenceStart = now;
        } else if (now - this.silenceStart >= this.minSilenceDuration) {
          this.isSpeaking = false;
          this.onSpeechEnd?.();
        }
      }
    }
    
    return {
      isVoice,
      isSpeaking: this.isSpeaking,
      rms,
      db: 20 * Math.log10(Math.max(rms, 0.0001))
    };
  }
  
  calculateRMS(pcmBuffer) {
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
const vad = new SimpleVAD({
  threshold: 0.02,
  onSpeechStart: () => console.log('Speech started'),
  onSpeechEnd: () => console.log('Speech ended')
});

ws.on('message', (data) => {
  const msg = JSON.parse(data.toString());
  
  // Handle keep-alive
  if (msg.msg_type === 12) {
    ws.send(JSON.stringify({ msg_type: 13, timestamp: msg.timestamp }));
    return;
  }
  
  // Process audio
  if (msg.msg_type === 14) {
    const audioData = Buffer.from(msg.content, 'base64');
    const result = vad.process(audioData);
    
    if (result.isSpeaking) {
      transcriber.sendAudio(audioData);
    }
  }
});
```

### JavaScript - WebRTC VAD

```javascript
const vad = require('webrtc-vad');

class WebRTCVAD {
  constructor(mode = 3) {
    // Mode: 0=quality, 1=low bitrate, 2=aggressive, 3=very aggressive
    this.vad = new vad.VAD(mode);
    this.sampleRate = 16000;
    this.frameSize = 160; // 10ms at 16kHz
  }
  
  process(pcmBuffer) {
    const frames = [];
    const bytesPerFrame = this.frameSize * 2;
    
    for (let i = 0; i < pcmBuffer.length; i += bytesPerFrame) {
      if (i + bytesPerFrame <= pcmBuffer.length) {
        const frame = pcmBuffer.slice(i, i + bytesPerFrame);
        const isVoice = this.vad.is_speech(frame, this.sampleRate);
        frames.push({ frame, isVoice });
      }
    }
    
    return frames;
  }
  
  processAndFilter(pcmBuffer) {
    const frames = this.process(pcmBuffer);
    const voiceFrames = frames.filter(f => f.isVoice).map(f => f.frame);
    
    if (voiceFrames.length === 0) return null;
    return Buffer.concat(voiceFrames);
  }
}

// Usage
const webrtcVad = new WebRTCVAD(3); // Very aggressive

ws.on('message', (data) => {
  const msg = JSON.parse(data.toString());
  
  // Handle keep-alive
  if (msg.msg_type === 12) {
    ws.send(JSON.stringify({ msg_type: 13, timestamp: msg.timestamp }));
    return;
  }
  
  // Process audio
  if (msg.msg_type === 14) {
    const audioData = Buffer.from(msg.content, 'base64');
    const voiceAudio = webrtcVad.processAndFilter(audioData);
    if (voiceAudio) {
      transcriber.sendAudio(voiceAudio);
    }
  }
});
```

### Python - Silero VAD (Neural Network)

```python
import torch

class SileroVAD:
    def __init__(self, threshold=0.5):
        self.model, self.utils = torch.hub.load(
            repo_or_dir='snakers4/silero-vad',
            model='silero_vad',
            force_reload=False
        )
        
        self.get_speech_timestamps = self.utils[0]
        self.threshold = threshold
        self.sample_rate = 16000
    
    def process(self, pcm_data):
        """Process audio and detect speech"""
        # Convert to tensor
        audio = torch.frombuffer(pcm_data, dtype=torch.int16).float() / 32768
        
        # Get speech probability
        speech_prob = self.model(audio, self.sample_rate).item()
        
        return {
            'is_speech': speech_prob > self.threshold,
            'probability': speech_prob
        }
    
    def get_speech_segments(self, pcm_data):
        """Get speech timestamps from audio"""
        audio = torch.frombuffer(pcm_data, dtype=torch.int16).float() / 32768
        
        speech_timestamps = self.get_speech_timestamps(
            audio,
            self.model,
            sampling_rate=self.sample_rate,
            threshold=self.threshold,
            min_speech_duration_ms=250,
            min_silence_duration_ms=100
        )
        
        return speech_timestamps
    
    def filter_speech_only(self, pcm_data):
        """Return only speech portions"""
        audio = torch.frombuffer(pcm_data, dtype=torch.int16)
        timestamps = self.get_speech_segments(pcm_data)
        
        speech_segments = []
        for ts in timestamps:
            segment = audio[ts['start']:ts['end']]
            speech_segments.append(segment)
        
        if not speech_segments:
            return None
        
        return torch.cat(speech_segments).numpy().tobytes()

# Usage
import base64
import json

vad = SileroVAD(threshold=0.5)

async for message in ws:
    msg = json.loads(message)
    
    # Handle keep-alive
    if msg['msg_type'] == 12:
        await ws.send(json.dumps({"msg_type": 13, "timestamp": msg["timestamp"]}))
        continue
    
    # Process audio
    if msg['msg_type'] == 14:
        audio = base64.b64decode(msg['content'])
        result = vad.process(audio)
        
        if result['is_speech']:
            print(f"Speech detected (prob: {result['probability']:.2f})")
            await transcriber.send_audio(audio)
```

### Python - pyannote VAD

```python
from pyannote.audio import Model, Inference

class PyannoteVAD:
    def __init__(self, hf_token):
        self.model = Model.from_pretrained(
            "pyannote/segmentation-3.0",
            use_auth_token=hf_token
        )
        self.inference = Inference(self.model)
    
    def process_file(self, audio_path):
        """Process audio file"""
        output = self.inference(audio_path)
        
        segments = []
        for segment, _, label in output.itertracks(yield_label=True):
            if label == "SPEECH":
                segments.append({
                    'start': segment.start,
                    'end': segment.end
                })
        
        return segments
```

## VAD Comparison

| Method | Accuracy | Latency | CPU |
|--------|----------|---------|-----|
| Energy-based | 70% | <1ms | Very Low |
| WebRTC VAD | 85% | <5ms | Low |
| Silero VAD | 95% | ~10ms | Medium |
| pyannote | 98% | ~50ms | High |

## Resources

- **Silero VAD**: https://github.com/snakers4/silero-vad
- **WebRTC VAD**: https://github.com/nicepkg/webrtc-vad
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

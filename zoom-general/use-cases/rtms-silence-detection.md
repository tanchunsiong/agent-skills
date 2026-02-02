# Silence Detection

## Brief
Detect and measure silent periods in meetings using real-time media stream analysis.

## Overview
Silence detection identifies gaps in audio where no meaningful sound is being transmitted. This is useful for:
- Meeting engagement analysis
- Speaker turn detection
- Audio quality monitoring
- Automatic transcription segmentation
- Meeting summarization

## JavaScript Example

### Basic Silence Detection

```javascript
class SilenceDetector {
  constructor(options = {}) {
    this.silenceThreshold = options.silenceThreshold || -40; // dB
    this.minSilenceDuration = options.minSilenceDuration || 500; // ms
    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    this.analyser = this.audioContext.createAnalyser();
    this.analyser.fftSize = 2048;
    
    this.silenceGaps = [];
    this.currentSilenceStart = null;
    this.dataArray = new Uint8Array(this.analyser.frequencyBinCount);
  }

  async startMonitoring(stream) {
    const source = this.audioContext.createMediaStreamSource(stream);
    source.connect(this.analyser);
    
    this.monitoringInterval = setInterval(() => {
      this.detectSilence();
    }, 100); // Check every 100ms
  }

  detectSilence() {
    this.analyser.getByteFrequencyData(this.dataArray);
    
    // Calculate average frequency magnitude
    const average = this.dataArray.reduce((a, b) => a + b) / this.dataArray.length;
    const db = 20 * Math.log10(average / 255);
    
    const isSilent = db < this.silenceThreshold;
    const now = Date.now();
    
    if (isSilent) {
      if (this.currentSilenceStart === null) {
        this.currentSilenceStart = now;
      }
    } else {
      if (this.currentSilenceStart !== null) {
        const duration = now - this.currentSilenceStart;
        if (duration >= this.minSilenceDuration) {
          this.silenceGaps.push({
            startTime: this.currentSilenceStart,
            endTime: now,
            duration: duration,
            dB: db
          });
        }
        this.currentSilenceStart = null;
      }
    }
  }

  stopMonitoring() {
    clearInterval(this.monitoringInterval);
  }

  getSilenceReport() {
    const totalSilence = this.silenceGaps.reduce((sum, gap) => sum + gap.duration, 0);
    return {
      silenceGaps: this.silenceGaps,
      totalSilenceDuration: totalSilence,
      gapCount: this.silenceGaps.length,
      averageGapDuration: this.silenceGaps.length > 0 
        ? totalSilence / this.silenceGaps.length 
        : 0
    };
  }
}

// Usage
const detector = new SilenceDetector({
  silenceThreshold: -35,
  minSilenceDuration: 300
});

navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    detector.startMonitoring(stream);
    
    // After meeting
    setTimeout(() => {
      detector.stopMonitoring();
      console.log(detector.getSilenceReport());
    }, 60000); // 1 minute
  });
```

### Integration with Zoom RTMS

```javascript
class ZoomSilenceDetector {
  constructor(rtmsClient) {
    this.rtmsClient = rtmsClient;
    this.silenceDetector = new SilenceDetector();
    this.participantSilence = new Map();
  }

  async monitorParticipant(participantId, audioStream) {
    const detector = new SilenceDetector({
      silenceThreshold: -38,
      minSilenceDuration: 400
    });
    
    await detector.startMonitoring(audioStream);
    this.participantSilence.set(participantId, detector);
  }

  getParticipantSilenceMetrics(participantId) {
    const detector = this.participantSilence.get(participantId);
    if (!detector) return null;
    
    return {
      participantId,
      ...detector.getSilenceReport(),
      engagementScore: this.calculateEngagement(detector.getSilenceReport())
    };
  }

  calculateEngagement(report) {
    // Higher engagement = less silence
    const engagementScore = Math.max(0, 100 - (report.totalSilenceDuration / 60000) * 100);
    return Math.round(engagementScore);
  }

  getAllParticipantMetrics() {
    const metrics = [];
    for (const [participantId, detector] of this.participantSilence) {
      metrics.push(this.getParticipantSilenceMetrics(participantId));
    }
    return metrics;
  }
}
```

## Python Example

### Basic Silence Detection

```python
import numpy as np
from collections import deque
from datetime import datetime
import librosa

class SilenceDetector:
    def __init__(self, sample_rate=16000, silence_threshold=-40, min_duration=0.3):
        """
        Initialize silence detector.
        
        Args:
            sample_rate: Audio sample rate in Hz
            silence_threshold: dB threshold for silence detection
            min_duration: Minimum silence duration in seconds
        """
        self.sample_rate = sample_rate
        self.silence_threshold = silence_threshold
        self.min_duration = min_duration
        self.min_samples = int(min_duration * sample_rate)
        
        self.silence_gaps = []
        self.current_silence_start = None
        self.frame_count = 0
    
    def process_audio_frame(self, audio_frame):
        """
        Process a single audio frame and detect silence.
        
        Args:
            audio_frame: numpy array of audio samples
        """
        # Calculate RMS energy
        rms = np.sqrt(np.mean(audio_frame ** 2))
        db = 20 * np.log10(rms + 1e-10)  # Add small value to avoid log(0)
        
        is_silent = db < self.silence_threshold
        current_time = self.frame_count / self.sample_rate
        
        if is_silent:
            if self.current_silence_start is None:
                self.current_silence_start = current_time
        else:
            if self.current_silence_start is not None:
                duration = current_time - self.current_silence_start
                if duration >= self.min_duration:
                    self.silence_gaps.append({
                        'start_time': self.current_silence_start,
                        'end_time': current_time,
                        'duration': duration,
                        'db': db
                    })
                self.current_silence_start = None
        
        self.frame_count += len(audio_frame)
    
    def process_audio_file(self, audio_path):
        """
        Process entire audio file and detect all silence gaps.
        
        Args:
            audio_path: Path to audio file
        """
        # Load audio file
        y, sr = librosa.load(audio_path, sr=self.sample_rate)
        
        # Process in frames
        frame_length = self.sample_rate // 10  # 100ms frames
        for i in range(0, len(y), frame_length):
            frame = y[i:i + frame_length]
            if len(frame) > 0:
                self.process_audio_frame(frame)
        
        # Handle final silence if still ongoing
        if self.current_silence_start is not None:
            duration = (self.frame_count / self.sample_rate) - self.current_silence_start
            if duration >= self.min_duration:
                self.silence_gaps.append({
                    'start_time': self.current_silence_start,
                    'end_time': self.frame_count / self.sample_rate,
                    'duration': duration,
                    'db': -50
                })
    
    def get_silence_report(self):
        """
        Generate silence detection report.
        
        Returns:
            Dictionary with silence metrics
        """
        if not self.silence_gaps:
            return {
                'silence_gaps': [],
                'total_silence_duration': 0,
                'gap_count': 0,
                'average_gap_duration': 0,
                'max_gap_duration': 0
            }
        
        total_silence = sum(gap['duration'] for gap in self.silence_gaps)
        durations = [gap['duration'] for gap in self.silence_gaps]
        
        return {
            'silence_gaps': self.silence_gaps,
            'total_silence_duration': total_silence,
            'gap_count': len(self.silence_gaps),
            'average_gap_duration': total_silence / len(self.silence_gaps),
            'max_gap_duration': max(durations),
            'min_gap_duration': min(durations)
        }

# Usage
detector = SilenceDetector(
    sample_rate=16000,
    silence_threshold=-35,
    min_duration=0.3
)

detector.process_audio_file('meeting_recording.wav')
report = detector.get_silence_report()

print(f"Total silence: {report['total_silence_duration']:.2f}s")
print(f"Number of gaps: {report['gap_count']}")
print(f"Average gap: {report['average_gap_duration']:.2f}s")
```

### Integration with Zoom RTMS

```python
import asyncio
from typing import Dict, List
import json

class ZoomSilenceDetector:
    def __init__(self, rtms_client):
        """
        Initialize Zoom silence detector.
        
        Args:
            rtms_client: Zoom RTMS client instance
        """
        self.rtms_client = rtms_client
        self.participant_detectors: Dict[str, SilenceDetector] = {}
        self.meeting_start_time = datetime.now()
    
    async def monitor_participant(self, participant_id: str, audio_stream):
        """
        Monitor silence for a specific participant.
        
        Args:
            participant_id: Zoom participant ID
            audio_stream: Audio stream from participant
        """
        detector = SilenceDetector(
            sample_rate=16000,
            silence_threshold=-38,
            min_duration=0.4
        )
        self.participant_detectors[participant_id] = detector
        
        # Process audio frames as they arrive
        async for frame in audio_stream:
            detector.process_audio_frame(frame)
    
    def get_participant_metrics(self, participant_id: str) -> Dict:
        """
        Get silence metrics for a participant.
        
        Args:
            participant_id: Zoom participant ID
            
        Returns:
            Dictionary with silence metrics and engagement score
        """
        detector = self.participant_detectors.get(participant_id)
        if not detector:
            return None
        
        report = detector.get_silence_report()
        engagement_score = self._calculate_engagement(report)
        
        return {
            'participant_id': participant_id,
            **report,
            'engagement_score': engagement_score
        }
    
    def get_all_metrics(self) -> List[Dict]:
        """
        Get silence metrics for all participants.
        
        Returns:
            List of metrics for each participant
        """
        metrics = []
        for participant_id in self.participant_detectors:
            metric = self.get_participant_metrics(participant_id)
            if metric:
                metrics.append(metric)
        return metrics
    
    def _calculate_engagement(self, report: Dict) -> int:
        """
        Calculate engagement score based on silence.
        
        Args:
            report: Silence detection report
            
        Returns:
            Engagement score 0-100
        """
        meeting_duration = (datetime.now() - self.meeting_start_time).total_seconds()
        if meeting_duration == 0:
            return 100
        
        silence_ratio = report['total_silence_duration'] / meeting_duration
        engagement_score = max(0, int(100 * (1 - silence_ratio)))
        return engagement_score
    
    def export_report(self, output_path: str):
        """
        Export silence detection report to JSON.
        
        Args:
            output_path: Path to save report
        """
        report = {
            'meeting_start': self.meeting_start_time.isoformat(),
            'participants': self.get_all_metrics()
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

# Usage
async def main():
    detector = ZoomSilenceDetector(rtms_client)
    
    # Monitor participants
    await detector.monitor_participant('participant_1', audio_stream_1)
    await detector.monitor_participant('participant_2', audio_stream_2)
    
    # Get metrics
    metrics = detector.get_all_metrics()
    for metric in metrics:
        print(f"Participant {metric['participant_id']}: "
              f"Engagement {metric['engagement_score']}%")
    
    # Export report
    detector.export_report('silence_report.json')

asyncio.run(main())
```

## Key Metrics

- **Silence Gap**: Continuous period of silence exceeding threshold
- **Total Silence Duration**: Sum of all silence gaps
- **Gap Count**: Number of distinct silence periods
- **Average Gap Duration**: Mean duration of silence gaps
- **Engagement Score**: Inverse of silence ratio (100% = no silence)

## Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `silenceThreshold` | -40 dB | Audio level below which is considered silent |
| `minSilenceDuration` | 300-400 ms | Minimum duration to register as silence gap |
| `sampleRate` | 16000 Hz | Audio sample rate |
| `frameSize` | 2048 | FFT size for frequency analysis |

## Best Practices

1. **Calibrate threshold** based on meeting environment noise levels
2. **Set minimum duration** to avoid detecting brief pauses as silence
3. **Monitor per-participant** for individual engagement metrics
4. **Track trends** over multiple meetings for pattern analysis
5. **Consider context** - silence may indicate listening, not disengagement

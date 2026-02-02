# Interruption Detection

## Brief
Detect overlapping speech patterns and interruptions using real-time media stream (RTMS) timestamps and audio analysis.

## Overview
Interruption detection identifies moments when multiple speakers overlap or when one speaker interrupts another. This is useful for meeting analytics, conversation quality assessment, and speaker turn-taking analysis.

## Key Concepts

- **Overlapping Speech**: Two or more speakers speaking simultaneously
- **Interruption**: One speaker begins speaking before another finishes
- **Speech Segments**: Continuous periods of speech from a single speaker
- **Timestamp Correlation**: Matching audio timestamps across multiple streams

## JavaScript Example

```javascript
// Interruption detection using RTMS timestamps
class InterruptionDetector {
  constructor() {
    this.speakers = new Map(); // Map of speaker_id -> speech segments
  }

  // Add a speech segment for a speaker
  addSpeechSegment(speakerId, startTime, endTime) {
    if (!this.speakers.has(speakerId)) {
      this.speakers.set(speakerId, []);
    }
    this.speakers.get(speakerId).push({
      start: startTime,
      end: endTime,
      speakerId: speakerId
    });
  }

  // Detect overlapping speech periods
  detectOverlaps() {
    const overlaps = [];
    const allSegments = [];

    // Collect all segments with speaker info
    for (const [speakerId, segments] of this.speakers) {
      allSegments.push(...segments);
    }

    // Sort by start time
    allSegments.sort((a, b) => a.start - b.start);

    // Find overlaps
    for (let i = 0; i < allSegments.length; i++) {
      for (let j = i + 1; j < allSegments.length; j++) {
        const seg1 = allSegments[i];
        const seg2 = allSegments[j];

        // Check if segments overlap
        if (seg1.end > seg2.start && seg1.speakerId !== seg2.speakerId) {
          const overlapStart = Math.max(seg1.start, seg2.start);
          const overlapEnd = Math.min(seg1.end, seg2.end);

          overlaps.push({
            speaker1: seg1.speakerId,
            speaker2: seg2.speakerId,
            overlapStart: overlapStart,
            overlapEnd: overlapEnd,
            duration: overlapEnd - overlapStart,
            timestamp: new Date(overlapStart).toISOString()
          });
        }
      }
    }

    return overlaps;
  }

  // Detect interruptions (one speaker starts before another ends)
  detectInterruptions() {
    const interruptions = [];
    const allSegments = [];

    for (const [speakerId, segments] of this.speakers) {
      allSegments.push(...segments);
    }

    allSegments.sort((a, b) => a.start - b.start);

    for (let i = 0; i < allSegments.length - 1; i++) {
      const current = allSegments[i];
      const next = allSegments[i + 1];

      // Check if next speaker starts before current speaker ends
      if (next.start < current.end && current.speakerId !== next.speakerId) {
        interruptions.push({
          interrupter: next.speakerId,
          interrupted: current.speakerId,
          interruptionTime: next.start,
          interruptedSpeakerEndTime: current.end,
          overlapDuration: current.end - next.start,
          timestamp: new Date(next.start).toISOString()
        });
      }
    }

    return interruptions;
  }

  // Get statistics
  getStatistics() {
    const overlaps = this.detectOverlaps();
    const interruptions = this.detectInterruptions();

    return {
      totalSpeakers: this.speakers.size,
      totalOverlaps: overlaps.length,
      totalInterruptions: interruptions.length,
      totalOverlapDuration: overlaps.reduce((sum, o) => sum + o.duration, 0),
      averageOverlapDuration: overlaps.length > 0 
        ? overlaps.reduce((sum, o) => sum + o.duration, 0) / overlaps.length 
        : 0
    };
  }
}

// Usage Example
const detector = new InterruptionDetector();

// Add speech segments (timestamps in milliseconds)
detector.addSpeechSegment('speaker_1', 1000, 5000);  // Speaker 1: 1s to 5s
detector.addSpeechSegment('speaker_2', 4500, 8000);  // Speaker 2: 4.5s to 8s (overlaps)
detector.addSpeechSegment('speaker_1', 8500, 12000); // Speaker 1: 8.5s to 12s
detector.addSpeechSegment('speaker_2', 11000, 15000); // Speaker 2: 11s to 15s (interrupts)

console.log('Overlaps:', detector.detectOverlaps());
console.log('Interruptions:', detector.detectInterruptions());
console.log('Statistics:', detector.getStatistics());
```

## Python Example

```python
from dataclasses import dataclass
from typing import List, Dict, Tuple
from datetime import datetime

@dataclass
class SpeechSegment:
    speaker_id: str
    start_time: float  # milliseconds
    end_time: float    # milliseconds

class InterruptionDetector:
    def __init__(self):
        self.speakers: Dict[str, List[SpeechSegment]] = {}

    def add_speech_segment(self, speaker_id: str, start_time: float, end_time: float):
        """Add a speech segment for a speaker"""
        if speaker_id not in self.speakers:
            self.speakers[speaker_id] = []
        self.speakers[speaker_id].append(
            SpeechSegment(speaker_id, start_time, end_time)
        )

    def detect_overlaps(self) -> List[Dict]:
        """Detect overlapping speech periods"""
        overlaps = []
        all_segments = []

        # Collect all segments
        for speaker_id, segments in self.speakers.items():
            all_segments.extend(segments)

        # Sort by start time
        all_segments.sort(key=lambda s: s.start_time)

        # Find overlaps
        for i in range(len(all_segments)):
            for j in range(i + 1, len(all_segments)):
                seg1 = all_segments[i]
                seg2 = all_segments[j]

                # Check if segments overlap
                if seg1.end_time > seg2.start_time and seg1.speaker_id != seg2.speaker_id:
                    overlap_start = max(seg1.start_time, seg2.start_time)
                    overlap_end = min(seg1.end_time, seg2.end_time)

                    overlaps.append({
                        'speaker1': seg1.speaker_id,
                        'speaker2': seg2.speaker_id,
                        'overlap_start': overlap_start,
                        'overlap_end': overlap_end,
                        'duration': overlap_end - overlap_start,
                        'timestamp': datetime.fromtimestamp(overlap_start / 1000).isoformat()
                    })

        return overlaps

    def detect_interruptions(self) -> List[Dict]:
        """Detect interruptions (one speaker starts before another ends)"""
        interruptions = []
        all_segments = []

        for speaker_id, segments in self.speakers.items():
            all_segments.extend(segments)

        all_segments.sort(key=lambda s: s.start_time)

        for i in range(len(all_segments) - 1):
            current = all_segments[i]
            next_seg = all_segments[i + 1]

            # Check if next speaker starts before current speaker ends
            if next_seg.start_time < current.end_time and current.speaker_id != next_seg.speaker_id:
                interruptions.append({
                    'interrupter': next_seg.speaker_id,
                    'interrupted': current.speaker_id,
                    'interruption_time': next_seg.start_time,
                    'interrupted_speaker_end_time': current.end_time,
                    'overlap_duration': current.end_time - next_seg.start_time,
                    'timestamp': datetime.fromtimestamp(next_seg.start_time / 1000).isoformat()
                })

        return interruptions

    def get_statistics(self) -> Dict:
        """Get interruption statistics"""
        overlaps = self.detect_overlaps()
        interruptions = self.detect_interruptions()

        total_overlap_duration = sum(o['duration'] for o in overlaps)
        avg_overlap_duration = (
            total_overlap_duration / len(overlaps) if overlaps else 0
        )

        return {
            'total_speakers': len(self.speakers),
            'total_overlaps': len(overlaps),
            'total_interruptions': len(interruptions),
            'total_overlap_duration': total_overlap_duration,
            'average_overlap_duration': avg_overlap_duration
        }

# Usage Example
detector = InterruptionDetector()

# Add speech segments (timestamps in milliseconds)
detector.add_speech_segment('speaker_1', 1000, 5000)   # Speaker 1: 1s to 5s
detector.add_speech_segment('speaker_2', 4500, 8000)   # Speaker 2: 4.5s to 8s (overlaps)
detector.add_speech_segment('speaker_1', 8500, 12000)  # Speaker 1: 8.5s to 12s
detector.add_speech_segment('speaker_2', 11000, 15000) # Speaker 2: 11s to 15s (interrupts)

print('Overlaps:', detector.detect_overlaps())
print('Interruptions:', detector.detect_interruptions())
print('Statistics:', detector.get_statistics())
```

## Integration with Zoom RTMS

```javascript
// Example: Processing RTMS audio data for interruption detection
async function processRTMSForInterruptions(rtmsConnection) {
  const detector = new InterruptionDetector();
  const audioBuffer = {};

  rtmsConnection.on('audio_frame', (frame) => {
    const { participant_id, timestamp, audio_data } = frame;

    // Detect speech activity (simplified - use VAD in production)
    const hasSpeech = detectSpeechActivity(audio_data);

    if (hasSpeech) {
      if (!audioBuffer[participant_id]) {
        audioBuffer[participant_id] = {
          startTime: timestamp,
          lastUpdate: timestamp
        };
      }
      audioBuffer[participant_id].lastUpdate = timestamp;
    } else if (audioBuffer[participant_id]) {
      // Speech ended
      const segment = audioBuffer[participant_id];
      detector.addSpeechSegment(
        participant_id,
        segment.startTime,
        segment.lastUpdate
      );
      delete audioBuffer[participant_id];
    }
  });

  return detector;
}
```

## Use Cases

1. **Meeting Analytics**: Track speaker interruptions and overlapping speech
2. **Conversation Quality**: Identify turn-taking patterns and communication flow
3. **Accessibility**: Provide real-time alerts for overlapping speech
4. **Training**: Analyze communication patterns in training sessions
5. **Research**: Study conversation dynamics and interruption patterns

## Performance Considerations

- **Timestamp Precision**: Use millisecond precision for accurate overlap detection
- **Scalability**: For large meetings, use sliding window approach
- **Real-time Processing**: Process segments incrementally rather than batch
- **Memory**: Store only active segments to reduce memory footprint

## References

- [Zoom RTMS Documentation](https://developers.zoom.us/docs/meeting-sdk/real-time-media-stream/)
- [Voice Activity Detection (VAD)](https://en.wikipedia.org/wiki/Voice_activity_detection)
- [Conversation Analysis](https://en.wikipedia.org/wiki/Conversation_analysis)

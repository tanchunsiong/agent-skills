# Speaker Pace Analysis

## Brief
Analyze words per minute (WPM) for each speaker using Zoom Real-Time Messaging Service (RTMS) transcription data.

## Overview
This use case demonstrates how to calculate and track the speaking pace of individual speakers during a meeting. By analyzing the number of words spoken within specific time intervals, you can identify speaking patterns, detect rapid speech, and measure communication efficiency.

## Key Metrics
- **Words Per Minute (WPM)**: Total words spoken divided by duration in minutes
- **Average WPM**: Mean speaking pace across the entire meeting
- **Peak WPM**: Maximum speaking pace during any interval
- **Speaking Duration**: Total time a speaker was actively speaking

## JavaScript Example

```javascript
/**
 * Calculate Words Per Minute (WPM) for each speaker
 * @param {Array} transcripts - Array of transcript objects with speaker, text, and timestamp
 * @returns {Object} Speaker WPM statistics
 */
function calculateSpeakerWPM(transcripts) {
  const speakerStats = {};

  // Group transcripts by speaker
  transcripts.forEach((entry) => {
    const { speaker, text, timestamp } = entry;
    
    if (!speakerStats[speaker]) {
      speakerStats[speaker] = {
        totalWords: 0,
        startTime: timestamp,
        endTime: timestamp,
        segments: []
      };
    }

    const wordCount = text.trim().split(/\s+/).length;
    speakerStats[speaker].totalWords += wordCount;
    speakerStats[speaker].endTime = timestamp;
    speakerStats[speaker].segments.push({
      text,
      timestamp,
      wordCount
    });
  });

  // Calculate WPM for each speaker
  const results = {};
  Object.entries(speakerStats).forEach(([speaker, stats]) => {
    const durationMinutes = (stats.endTime - stats.startTime) / 60000; // Convert ms to minutes
    const wpm = durationMinutes > 0 ? stats.totalWords / durationMinutes : 0;
    
    results[speaker] = {
      totalWords: stats.totalWords,
      durationMinutes: Math.round(durationMinutes * 100) / 100,
      wpm: Math.round(wpm * 100) / 100,
      segmentCount: stats.segments.length
    };
  });

  return results;
}

/**
 * Calculate WPM for specific time intervals
 * @param {Array} transcripts - Array of transcript objects
 * @param {number} intervalSeconds - Interval size in seconds
 * @returns {Object} WPM by speaker and time interval
 */
function calculateIntervalWPM(transcripts, intervalSeconds = 60) {
  const intervalMs = intervalSeconds * 1000;
  const intervals = {};

  transcripts.forEach((entry) => {
    const { speaker, text, timestamp } = entry;
    const intervalKey = Math.floor(timestamp / intervalMs);
    const timeLabel = `${intervalKey * intervalSeconds}s - ${(intervalKey + 1) * intervalSeconds}s`;

    if (!intervals[timeLabel]) {
      intervals[timeLabel] = {};
    }

    if (!intervals[timeLabel][speaker]) {
      intervals[timeLabel][speaker] = 0;
    }

    const wordCount = text.trim().split(/\s+/).length;
    intervals[timeLabel][speaker] += wordCount;
  });

  // Convert word counts to WPM
  const wpmByInterval = {};
  Object.entries(intervals).forEach(([timeLabel, speakers]) => {
    wpmByInterval[timeLabel] = {};
    Object.entries(speakers).forEach(([speaker, wordCount]) => {
      const wpm = (wordCount / intervalSeconds) * 60;
      wpmByInterval[timeLabel][speaker] = Math.round(wpm * 100) / 100;
    });
  });

  return wpmByInterval;
}

// Example usage
const transcriptData = [
  { speaker: "Alice", text: "Hello everyone, welcome to the meeting", timestamp: 0 },
  { speaker: "Bob", text: "Thanks for joining us today", timestamp: 5000 },
  { speaker: "Alice", text: "Let's discuss the quarterly results and upcoming initiatives", timestamp: 10000 },
  { speaker: "Alice", text: "We've made significant progress on all fronts", timestamp: 15000 },
  { speaker: "Bob", text: "That's great to hear", timestamp: 20000 }
];

const overallWPM = calculateSpeakerWPM(transcriptData);
console.log("Overall WPM by Speaker:", overallWPM);

const intervalWPM = calculateIntervalWPM(transcriptData, 10);
console.log("WPM by 10-second Intervals:", intervalWPM);
```

## Python Example

```python
"""
Speaker Pace Analysis - Calculate WPM for each speaker
"""
from typing import Dict, List, Tuple
from collections import defaultdict
import statistics

class SpeakerPaceAnalyzer:
    """Analyze speaking pace (WPM) for meeting participants"""
    
    def __init__(self, transcripts: List[Dict]):
        """
        Initialize with transcript data
        
        Args:
            transcripts: List of dicts with keys: speaker, text, timestamp (ms)
        """
        self.transcripts = transcripts
        self.speaker_stats = defaultdict(lambda: {
            'total_words': 0,
            'start_time': float('inf'),
            'end_time': 0,
            'segments': []
        })
    
    def _count_words(self, text: str) -> int:
        """Count words in text"""
        return len(text.strip().split())
    
    def calculate_overall_wpm(self) -> Dict[str, Dict]:
        """
        Calculate overall WPM for each speaker
        
        Returns:
            Dictionary with speaker stats including WPM
        """
        # Group by speaker and aggregate
        for entry in self.transcripts:
            speaker = entry['speaker']
            text = entry['text']
            timestamp = entry['timestamp']
            
            word_count = self._count_words(text)
            self.speaker_stats[speaker]['total_words'] += word_count
            self.speaker_stats[speaker]['start_time'] = min(
                self.speaker_stats[speaker]['start_time'], 
                timestamp
            )
            self.speaker_stats[speaker]['end_time'] = max(
                self.speaker_stats[speaker]['end_time'], 
                timestamp
            )
            self.speaker_stats[speaker]['segments'].append({
                'text': text,
                'timestamp': timestamp,
                'word_count': word_count
            })
        
        # Calculate WPM
        results = {}
        for speaker, stats in self.speaker_stats.items():
            duration_minutes = (stats['end_time'] - stats['start_time']) / 60000
            wpm = stats['total_words'] / duration_minutes if duration_minutes > 0 else 0
            
            results[speaker] = {
                'total_words': stats['total_words'],
                'duration_minutes': round(duration_minutes, 2),
                'wpm': round(wpm, 2),
                'segment_count': len(stats['segments'])
            }
        
        return results
    
    def calculate_interval_wpm(self, interval_seconds: int = 60) -> Dict[str, Dict]:
        """
        Calculate WPM for specific time intervals
        
        Args:
            interval_seconds: Size of each interval in seconds
            
        Returns:
            Dictionary with WPM by interval and speaker
        """
        interval_ms = interval_seconds * 1000
        intervals = defaultdict(lambda: defaultdict(int))
        
        for entry in self.transcripts:
            speaker = entry['speaker']
            text = entry['text']
            timestamp = entry['timestamp']
            
            interval_key = int(timestamp // interval_ms)
            time_label = f"{interval_key * interval_seconds}s - {(interval_key + 1) * interval_seconds}s"
            
            word_count = self._count_words(text)
            intervals[time_label][speaker] += word_count
        
        # Convert to WPM
        wpm_by_interval = {}
        for time_label, speakers in intervals.items():
            wpm_by_interval[time_label] = {}
            for speaker, word_count in speakers.items():
                wpm = (word_count / interval_seconds) * 60
                wpm_by_interval[time_label][speaker] = round(wpm, 2)
        
        return wpm_by_interval
    
    def get_speaker_statistics(self, speaker: str) -> Dict:
        """
        Get detailed statistics for a specific speaker
        
        Args:
            speaker: Speaker name
            
        Returns:
            Dictionary with detailed statistics
        """
        if speaker not in self.speaker_stats:
            return {}
        
        stats = self.speaker_stats[speaker]
        wpm_values = [seg['word_count'] / ((seg['timestamp'] - stats['start_time']) / 60000 + 0.1) 
                      for seg in stats['segments']]
        
        return {
            'speaker': speaker,
            'total_words': stats['total_words'],
            'segment_count': len(stats['segments']),
            'average_wpm': round(statistics.mean(wpm_values), 2) if wpm_values else 0,
            'max_wpm': round(max(wpm_values), 2) if wpm_values else 0,
            'min_wpm': round(min(wpm_values), 2) if wpm_values else 0
        }


# Example usage
if __name__ == "__main__":
    transcript_data = [
        {"speaker": "Alice", "text": "Hello everyone, welcome to the meeting", "timestamp": 0},
        {"speaker": "Bob", "text": "Thanks for joining us today", "timestamp": 5000},
        {"speaker": "Alice", "text": "Let's discuss the quarterly results and upcoming initiatives", "timestamp": 10000},
        {"speaker": "Alice", "text": "We've made significant progress on all fronts", "timestamp": 15000},
        {"speaker": "Bob", "text": "That's great to hear", "timestamp": 20000}
    ]
    
    analyzer = SpeakerPaceAnalyzer(transcript_data)
    
    # Overall WPM
    overall_wpm = analyzer.calculate_overall_wpm()
    print("Overall WPM by Speaker:")
    for speaker, stats in overall_wpm.items():
        print(f"  {speaker}: {stats['wpm']} WPM ({stats['total_words']} words in {stats['duration_minutes']} min)")
    
    # Interval WPM
    interval_wpm = analyzer.calculate_interval_wpm(10)
    print("\nWPM by 10-second Intervals:")
    for interval, speakers in interval_wpm.items():
        print(f"  {interval}: {speakers}")
    
    # Detailed statistics
    print("\nDetailed Statistics:")
    for speaker in overall_wpm.keys():
        stats = analyzer.get_speaker_statistics(speaker)
        print(f"  {speaker}: Avg {stats['average_wpm']} WPM, Max {stats['max_wpm']} WPM")
```

## Use Cases
- **Meeting Quality Assessment**: Identify if speakers are rushing or speaking too slowly
- **Presentation Analysis**: Track speaker pace during presentations
- **Communication Efficiency**: Measure how effectively speakers convey information
- **Speaker Coaching**: Provide feedback on speaking pace and rhythm
- **Accessibility**: Ensure speaking pace is appropriate for audience comprehension

## Integration with Zoom RTMS
To use this with Zoom Real-Time Messaging Service:

1. Subscribe to transcript events from RTMS
2. Collect speaker, text, and timestamp data
3. Pass transcript data to the WPM calculation functions
4. Display results in real-time or post-meeting analytics

## References
- [Zoom Real-Time Messaging Service Documentation](https://developers.zoom.us/docs/rtms/)
- [Transcript Events](https://developers.zoom.us/docs/rtms/events/transcript/)

# Talk Time Analytics

## Brief
Track speaking duration per participant from RTMS transcripts. Analyze who spoke the most, identify participation patterns, and generate speaker engagement metrics.

## Overview
Real-Time Messaging Service (RTMS) transcripts contain speaker information and timestamps. By parsing these transcripts, you can calculate total talk time per participant, identify speaking patterns, and generate analytics reports.

## Use Case
- **Meeting Analytics**: Measure participant engagement by talk time
- **Presentation Tracking**: Monitor speaker duration in webinars
- **Participation Reports**: Identify who dominated the conversation
- **Engagement Metrics**: Calculate speaking time percentages

## JavaScript Example

```javascript
/**
 * Talk Time Analytics - JavaScript Implementation
 * Tracks speaking duration per participant from RTMS transcripts
 */

class TalkTimeAnalytics {
  constructor() {
    this.speakers = {};
    this.totalDuration = 0;
  }

  /**
   * Parse RTMS transcript and calculate talk time
   * @param {Array} transcript - Array of transcript objects with speaker, timestamp, and text
   * @returns {Object} Analytics results with speaker durations
   */
  analyzeTalkTime(transcript) {
    // Reset for new analysis
    this.speakers = {};
    this.totalDuration = 0;

    // Sort transcript by timestamp
    const sorted = transcript.sort((a, b) => 
      new Date(a.timestamp) - new Date(b.timestamp)
    );

    // Calculate duration for each speaker
    for (let i = 0; i < sorted.length; i++) {
      const current = sorted[i];
      const next = sorted[i + 1];
      
      // Calculate duration until next speaker or end
      const currentTime = new Date(current.timestamp).getTime();
      const nextTime = next ? new Date(next.timestamp).getTime() : currentTime + 5000;
      const duration = (nextTime - currentTime) / 1000; // Convert to seconds

      // Initialize speaker if not exists
      if (!this.speakers[current.speaker]) {
        this.speakers[current.speaker] = {
          name: current.speaker,
          totalSeconds: 0,
          messageCount: 0,
          messages: []
        };
      }

      // Add duration and message
      this.speakers[current.speaker].totalSeconds += duration;
      this.speakers[current.speaker].messageCount += 1;
      this.speakers[current.speaker].messages.push({
        text: current.text,
        timestamp: current.timestamp,
        duration: duration
      });

      this.totalDuration += duration;
    }

    return this.generateReport();
  }

  /**
   * Generate analytics report
   * @returns {Object} Formatted report with metrics
   */
  generateReport() {
    const report = {
      totalDuration: this.totalDuration,
      totalSeconds: Math.round(this.totalDuration),
      totalMinutes: Math.round(this.totalDuration / 60),
      speakers: [],
      topSpeaker: null,
      averageTalkTime: 0
    };

    // Calculate metrics for each speaker
    const speakerArray = Object.values(this.speakers).map(speaker => ({
      name: speaker.name,
      totalSeconds: Math.round(speaker.totalSeconds),
      totalMinutes: (speaker.totalSeconds / 60).toFixed(2),
      percentage: ((speaker.totalSeconds / this.totalDuration) * 100).toFixed(2),
      messageCount: speaker.messageCount,
      averageMessageDuration: (speaker.totalSeconds / speaker.messageCount).toFixed(2)
    }));

    // Sort by talk time descending
    speakerArray.sort((a, b) => b.totalSeconds - a.totalSeconds);

    report.speakers = speakerArray;
    report.topSpeaker = speakerArray[0] || null;
    report.averageTalkTime = speakerArray.length > 0 
      ? (this.totalDuration / speakerArray.length).toFixed(2)
      : 0;

    return report;
  }

  /**
   * Get speaker statistics
   * @param {string} speakerName - Name of speaker to analyze
   * @returns {Object} Speaker-specific metrics
   */
  getSpeakerStats(speakerName) {
    return this.speakers[speakerName] || null;
  }

  /**
   * Export report as JSON
   * @returns {string} JSON formatted report
   */
  exportJSON() {
    return JSON.stringify(this.generateReport(), null, 2);
  }
}

// Example usage
const transcript = [
  { speaker: "Alice", timestamp: "2024-01-15T10:00:00Z", text: "Good morning everyone" },
  { speaker: "Bob", timestamp: "2024-01-15T10:00:15Z", text: "Hi Alice, thanks for joining" },
  { speaker: "Alice", timestamp: "2024-01-15T10:00:30Z", text: "Let's discuss the project timeline" },
  { speaker: "Charlie", timestamp: "2024-01-15T10:01:00Z", text: "I have some concerns about the deadline" },
  { speaker: "Alice", timestamp: "2024-01-15T10:01:30Z", text: "What are your specific concerns?" },
  { speaker: "Bob", timestamp: "2024-01-15T10:02:00Z", text: "We should allocate more resources" }
];

const analytics = new TalkTimeAnalytics();
const report = analytics.analyzeTalkTime(transcript);

console.log("Talk Time Analytics Report:");
console.log(`Total Duration: ${report.totalMinutes} minutes`);
console.log(`Top Speaker: ${report.topSpeaker.name} (${report.topSpeaker.percentage}%)`);
console.log("\nSpeaker Breakdown:");
report.speakers.forEach(speaker => {
  console.log(`  ${speaker.name}: ${speaker.totalMinutes} min (${speaker.percentage}%)`);
});
```

## Python Example

```python
"""
Talk Time Analytics - Python Implementation
Tracks speaking duration per participant from RTMS transcripts
"""

from datetime import datetime
from typing import List, Dict, Any
import json

class TalkTimeAnalytics:
    def __init__(self):
        self.speakers = {}
        self.total_duration = 0

    def analyze_talk_time(self, transcript: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Parse RTMS transcript and calculate talk time per speaker.
        
        Args:
            transcript: List of transcript objects with speaker, timestamp, and text
            
        Returns:
            Dictionary containing analytics results with speaker durations
        """
        # Reset for new analysis
        self.speakers = {}
        self.total_duration = 0

        # Sort transcript by timestamp
        sorted_transcript = sorted(
            transcript,
            key=lambda x: datetime.fromisoformat(x['timestamp'].replace('Z', '+00:00'))
        )

        # Calculate duration for each speaker
        for i, current in enumerate(sorted_transcript):
            current_time = datetime.fromisoformat(
                current['timestamp'].replace('Z', '+00:00')
            )
            
            # Get next speaker's timestamp or add 5 seconds as default
            if i + 1 < len(sorted_transcript):
                next_time = datetime.fromisoformat(
                    sorted_transcript[i + 1]['timestamp'].replace('Z', '+00:00')
                )
            else:
                next_time = current_time.replace(second=current_time.second + 5)
            
            # Calculate duration in seconds
            duration = (next_time - current_time).total_seconds()

            # Initialize speaker if not exists
            speaker_name = current['speaker']
            if speaker_name not in self.speakers:
                self.speakers[speaker_name] = {
                    'name': speaker_name,
                    'total_seconds': 0,
                    'message_count': 0,
                    'messages': []
                }

            # Add duration and message
            self.speakers[speaker_name]['total_seconds'] += duration
            self.speakers[speaker_name]['message_count'] += 1
            self.speakers[speaker_name]['messages'].append({
                'text': current['text'],
                'timestamp': current['timestamp'],
                'duration': duration
            })

            self.total_duration += duration

        return self.generate_report()

    def generate_report(self) -> Dict[str, Any]:
        """
        Generate analytics report with metrics.
        
        Returns:
            Formatted report with speaker statistics
        """
        report = {
            'total_duration': self.total_duration,
            'total_seconds': round(self.total_duration),
            'total_minutes': round(self.total_duration / 60),
            'speakers': [],
            'top_speaker': None,
            'average_talk_time': 0
        }

        # Calculate metrics for each speaker
        speaker_list = []
        for speaker in self.speakers.values():
            speaker_metrics = {
                'name': speaker['name'],
                'total_seconds': round(speaker['total_seconds']),
                'total_minutes': round(speaker['total_seconds'] / 60, 2),
                'percentage': round((speaker['total_seconds'] / self.total_duration) * 100, 2),
                'message_count': speaker['message_count'],
                'average_message_duration': round(
                    speaker['total_seconds'] / speaker['message_count'], 2
                )
            }
            speaker_list.append(speaker_metrics)

        # Sort by talk time descending
        speaker_list.sort(key=lambda x: x['total_seconds'], reverse=True)

        report['speakers'] = speaker_list
        report['top_speaker'] = speaker_list[0] if speaker_list else None
        report['average_talk_time'] = round(
            self.total_duration / len(speaker_list), 2
        ) if speaker_list else 0

        return report

    def get_speaker_stats(self, speaker_name: str) -> Dict[str, Any]:
        """
        Get statistics for a specific speaker.
        
        Args:
            speaker_name: Name of the speaker to analyze
            
        Returns:
            Speaker-specific metrics or None if not found
        """
        return self.speakers.get(speaker_name)

    def export_json(self) -> str:
        """
        Export report as JSON string.
        
        Returns:
            JSON formatted report
        """
        return json.dumps(self.generate_report(), indent=2)


# Example usage
if __name__ == "__main__":
    transcript = [
        {"speaker": "Alice", "timestamp": "2024-01-15T10:00:00Z", "text": "Good morning everyone"},
        {"speaker": "Bob", "timestamp": "2024-01-15T10:00:15Z", "text": "Hi Alice, thanks for joining"},
        {"speaker": "Alice", "timestamp": "2024-01-15T10:00:30Z", "text": "Let's discuss the project timeline"},
        {"speaker": "Charlie", "timestamp": "2024-01-15T10:01:00Z", "text": "I have some concerns about the deadline"},
        {"speaker": "Alice", "timestamp": "2024-01-15T10:01:30Z", "text": "What are your specific concerns?"},
        {"speaker": "Bob", "timestamp": "2024-01-15T10:02:00Z", "text": "We should allocate more resources"}
    ]

    analytics = TalkTimeAnalytics()
    report = analytics.analyze_talk_time(transcript)

    print("Talk Time Analytics Report:")
    print(f"Total Duration: {report['total_minutes']} minutes")
    print(f"Top Speaker: {report['top_speaker']['name']} ({report['top_speaker']['percentage']}%)")
    print("\nSpeaker Breakdown:")
    for speaker in report['speakers']:
        print(f"  {speaker['name']}: {speaker['total_minutes']} min ({speaker['percentage']}%)")
```

## Key Features

- **Per-Speaker Duration Tracking**: Calculate total talk time for each participant
- **Engagement Metrics**: Percentage of total talk time per speaker
- **Message Analysis**: Count messages and average duration per message
- **Top Speaker Identification**: Automatically identify the most vocal participant
- **Timestamp Parsing**: Handle ISO 8601 timestamps from RTMS
- **Report Generation**: Export analytics in structured format

## Integration with RTMS

1. Fetch transcript data from RTMS API
2. Pass transcript array to `analyzeTalkTime()` method
3. Generate report with speaker metrics
4. Export results for further analysis

## Output Example

```json
{
  "total_duration": 120,
  "total_seconds": 120,
  "total_minutes": 2,
  "speakers": [
    {
      "name": "Alice",
      "total_seconds": 60,
      "total_minutes": 1.0,
      "percentage": 50.0,
      "message_count": 3,
      "average_message_duration": 20.0
    },
    {
      "name": "Bob",
      "total_seconds": 45,
      "total_minutes": 0.75,
      "percentage": 37.5,
      "message_count": 2,
      "average_message_duration": 22.5
    }
  ],
  "top_speaker": {
    "name": "Alice",
    "percentage": 50.0
  },
  "average_talk_time": 30.0
}
```

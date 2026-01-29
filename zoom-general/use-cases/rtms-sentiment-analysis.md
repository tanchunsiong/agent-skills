# Sentiment Analysis

Real-time sentiment analysis of RTMS transcripts to gauge meeting tone and participant emotions.

## Overview

Analyze the sentiment of meeting transcripts in real-time to understand the emotional tone of conversations. This helps identify positive, negative, or neutral sentiment trends throughout meetings, enabling better meeting facilitation and post-meeting analysis.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

```javascript
const Sentiment = require('sentiment');
const sentiment = new Sentiment();

class RTMSSentimentAnalyzer {
  constructor() {
    this.sentimentHistory = [];
  }
  
  analyzeSentiment(text, speaker, timestamp) {
    const result = sentiment.analyze(text);
    
    const analysis = {
      speaker,
      timestamp,
      text,
      score: result.score,
      comparative: result.comparative,
      sentiment: this.classifySentiment(result.score),
      positive: result.positive,
      negative: result.negative
    };
    
    this.sentimentHistory.push(analysis);
    return analysis;
  }
  
  classifySentiment(score) {
    if (score > 2) return 'very positive';
    if (score > 0) return 'positive';
    if (score === 0) return 'neutral';
    if (score > -2) return 'negative';
    return 'very negative';
  }
  
  getMeetingSentiment() {
    if (this.sentimentHistory.length === 0) return null;
    
    const avgScore = this.sentimentHistory.reduce((sum, item) => sum + item.score, 0) / this.sentimentHistory.length;
    
    return {
      averageScore: avgScore,
      overallSentiment: this.classifySentiment(avgScore),
      totalAnalyzed: this.sentimentHistory.length,
      distribution: this.getSentimentDistribution()
    };
  }
  
  getSentimentDistribution() {
    const dist = { 'very positive': 0, 'positive': 0, 'neutral': 0, 'negative': 0, 'very negative': 0 };
    this.sentimentHistory.forEach(item => dist[item.sentiment]++);
    return dist;
  }
}

// RTMS Integration
const analyzer = new RTMSSentimentAnalyzer();

receiver.onTranscript = (segment) => {
  if (segment.isFinal) {
    const analysis = analyzer.analyzeSentiment(
      segment.text,
      segment.speaker,
      segment.timestamp
    );
    
    console.log(`[${analysis.speaker}] ${analysis.sentiment} (${analysis.score}): ${segment.text}`);
  }
};

receiver.onMeetingEnd = () => {
  const summary = analyzer.getMeetingSentiment();
  console.log('Meeting Sentiment Summary:', summary);
};
```

### Python

```python
from textblob import TextBlob
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SentimentAnalysis:
    speaker: str
    timestamp: str
    text: str
    polarity: float
    subjectivity: float
    sentiment: str

class RTMSSentimentAnalyzer:
    def __init__(self):
        self.sentiment_history: List[SentimentAnalysis] = []
    
    def analyze_sentiment(self, text: str, speaker: str, timestamp: str) -> SentimentAnalysis:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        analysis = SentimentAnalysis(
            speaker=speaker,
            timestamp=timestamp,
            text=text,
            polarity=polarity,
            subjectivity=blob.sentiment.subjectivity,
            sentiment=self._classify_sentiment(polarity)
        )
        
        self.sentiment_history.append(analysis)
        return analysis
    
    def _classify_sentiment(self, polarity: float) -> str:
        if polarity > 0.5:
            return 'very positive'
        elif polarity > 0:
            return 'positive'
        elif polarity == 0:
            return 'neutral'
        elif polarity > -0.5:
            return 'negative'
        else:
            return 'very negative'
    
    def get_meeting_sentiment(self) -> Dict:
        if not self.sentiment_history:
            return None
        
        avg_polarity = sum(item.polarity for item in self.sentiment_history) / len(self.sentiment_history)
        
        return {
            'average_polarity': avg_polarity,
            'overall_sentiment': self._classify_sentiment(avg_polarity),
            'total_analyzed': len(self.sentiment_history),
            'distribution': self._get_sentiment_distribution()
        }
    
    def _get_sentiment_distribution(self) -> Dict[str, int]:
        dist = {'very positive': 0, 'positive': 0, 'neutral': 0, 'negative': 0, 'very negative': 0}
        for item in self.sentiment_history:
            dist[item.sentiment] += 1
        return dist

# RTMS Integration
analyzer = RTMSSentimentAnalyzer()

def on_transcript(segment):
    if segment['is_final']:
        analysis = analyzer.analyze_sentiment(
            segment['text'],
            segment['speaker'],
            segment['timestamp']
        )
        print(f"[{analysis.speaker}] {analysis.sentiment} ({analysis.polarity:.2f}): {segment['text']}")

def on_meeting_end():
    summary = analyzer.get_meeting_sentiment()
    print('Meeting Sentiment Summary:', summary)
```

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/
- **Sentiment library**: https://www.npmjs.com/package/sentiment
- **TextBlob**: https://textblob.readthedocs.io/

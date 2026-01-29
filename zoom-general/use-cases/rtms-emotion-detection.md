# Emotion Detection

Real-time emotion detection from RTMS transcripts using transformer models to identify and track emotional states throughout meetings.

## Overview

Detect and classify emotions in meeting transcripts in real-time to understand participant emotional states. This enables identification of emotional patterns (joy, sadness, anger, fear, surprise, disgust) across speakers and time, supporting better meeting insights and participant well-being monitoring.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

```javascript
const transformers = require('@xenova/transformers');

class RTMSEmotionDetector {
  constructor() {
    this.emotionHistory = [];
    this.classifier = null;
    this.emotions = ['joy', 'sadness', 'anger', 'fear', 'surprise', 'disgust'];
  }
  
  async initialize() {
    this.classifier = await transformers.pipeline(
      'text-classification',
      'Xenova/bert-base-multilingual-uncased-sentiment'
    );
  }
  
  async detectEmotion(text, speaker, timestamp) {
    const results = await this.classifier(text);
    
    const emotionScores = this.normalizeEmotionScores(results);
    const dominantEmotion = this.getDominantEmotion(emotionScores);
    
    const analysis = {
      speaker,
      timestamp,
      text,
      dominantEmotion,
      emotionScores,
      confidence: emotionScores[dominantEmotion]
    };
    
    this.emotionHistory.push(analysis);
    return analysis;
  }
  
  normalizeEmotionScores(results) {
    const scores = {};
    this.emotions.forEach(emotion => {
      scores[emotion] = Math.random(); // Placeholder for actual model scores
    });
    
    // Normalize to sum to 1
    const sum = Object.values(scores).reduce((a, b) => a + b, 0);
    Object.keys(scores).forEach(key => {
      scores[key] = scores[key] / sum;
    });
    
    return scores;
  }
  
  getDominantEmotion(emotionScores) {
    return Object.keys(emotionScores).reduce((a, b) =>
      emotionScores[a] > emotionScores[b] ? a : b
    );
  }
  
  getEmotionTimeline() {
    return this.emotionHistory.map(item => ({
      speaker: item.speaker,
      timestamp: item.timestamp,
      emotion: item.dominantEmotion,
      confidence: item.confidence
    }));
  }
  
  getEmotionDistribution() {
    const dist = {};
    this.emotions.forEach(e => dist[e] = 0);
    
    this.emotionHistory.forEach(item => {
      dist[item.dominantEmotion]++;
    });
    
    return dist;
  }
  
  getSpeakerEmotions(speaker) {
    return this.emotionHistory
      .filter(item => item.speaker === speaker)
      .map(item => ({
        timestamp: item.timestamp,
        emotion: item.dominantEmotion,
        confidence: item.confidence
      }));
  }
}

// RTMS Integration
const detector = new RTMSEmotionDetector();
await detector.initialize();

receiver.onTranscript = async (segment) => {
  if (segment.isFinal) {
    const analysis = await detector.detectEmotion(
      segment.text,
      segment.speaker,
      segment.timestamp
    );
    
    console.log(`[${analysis.speaker}] ${analysis.dominantEmotion} (${(analysis.confidence * 100).toFixed(1)}%): ${segment.text}`);
  }
};

receiver.onMeetingEnd = () => {
  const timeline = detector.getEmotionTimeline();
  const distribution = detector.getEmotionDistribution();
  console.log('Emotion Timeline:', timeline);
  console.log('Emotion Distribution:', distribution);
};
```

### Python

```python
from transformers import pipeline
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime

@dataclass
class EmotionAnalysis:
    speaker: str
    timestamp: str
    text: str
    dominant_emotion: str
    emotion_scores: Dict[str, float]
    confidence: float

class RTMSEmotionDetector:
    def __init__(self):
        self.emotion_history: List[EmotionAnalysis] = []
        self.emotions = ['joy', 'sadness', 'anger', 'fear', 'surprise', 'disgust']
        self.classifier = pipeline(
            'text-classification',
            model='Xenova/bert-base-multilingual-uncased-sentiment'
        )
    
    def detect_emotion(self, text: str, speaker: str, timestamp: str) -> EmotionAnalysis:
        results = self.classifier(text)
        
        emotion_scores = self._normalize_emotion_scores(results)
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        
        analysis = EmotionAnalysis(
            speaker=speaker,
            timestamp=timestamp,
            text=text,
            dominant_emotion=dominant_emotion,
            emotion_scores=emotion_scores,
            confidence=emotion_scores[dominant_emotion]
        )
        
        self.emotion_history.append(analysis)
        return analysis
    
    def _normalize_emotion_scores(self, results: List[Dict]) -> Dict[str, float]:
        scores = {emotion: 0.0 for emotion in self.emotions}
        
        for result in results:
            label = result['label'].lower()
            if label in scores:
                scores[label] = result['score']
        
        total = sum(scores.values())
        if total > 0:
            scores = {k: v / total for k, v in scores.items()}
        
        return scores
    
    def get_emotion_timeline(self) -> List[Dict]:
        return [
            {
                'speaker': item.speaker,
                'timestamp': item.timestamp,
                'emotion': item.dominant_emotion,
                'confidence': item.confidence
            }
            for item in self.emotion_history
        ]
    
    def get_emotion_distribution(self) -> Dict[str, int]:
        dist = {emotion: 0 for emotion in self.emotions}
        for item in self.emotion_history:
            dist[item.dominant_emotion] += 1
        return dist
    
    def get_speaker_emotions(self, speaker: str) -> List[Dict]:
        return [
            {
                'timestamp': item.timestamp,
                'emotion': item.dominant_emotion,
                'confidence': item.confidence
            }
            for item in self.emotion_history
            if item.speaker == speaker
        ]

# RTMS Integration
detector = RTMSEmotionDetector()

def on_transcript(segment):
    if segment['is_final']:
        analysis = detector.detect_emotion(
            segment['text'],
            segment['speaker'],
            segment['timestamp']
        )
        print(f"[{analysis.speaker}] {analysis.dominant_emotion} ({analysis.confidence * 100:.1f}%): {segment['text']}")

def on_meeting_end():
    timeline = detector.get_emotion_timeline()
    distribution = detector.get_emotion_distribution()
    print('Emotion Timeline:', timeline)
    print('Emotion Distribution:', distribution)
```

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/
- **Transformers.js**: https://xenova.github.io/transformers.js/
- **Hugging Face Transformers**: https://huggingface.co/transformers/

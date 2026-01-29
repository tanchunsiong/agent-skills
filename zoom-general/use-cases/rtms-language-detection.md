# Language Detection

Automatically detect the language of RTMS transcripts.

## Overview

Detect speaking language for automatic translation routing and multilingual support.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

```javascript
const { LanguageServiceClient } = require('@google-cloud/language');
const langdetect = require('langdetect');

class LanguageDetector {
  constructor(options = {}) {
    this.method = options.method || 'local'; // 'local', 'google', 'azure'
    
    if (this.method === 'google') {
      this.googleClient = new LanguageServiceClient();
    }
  }
  
  async detect(text) {
    switch (this.method) {
      case 'google':
        return await this.detectWithGoogle(text);
      case 'azure':
        return await this.detectWithAzure(text);
      default:
        return this.detectLocal(text);
    }
  }
  
  detectLocal(text) {
    try {
      const results = langdetect.detect(text);
      if (results.length > 0) {
        return {
          language: results[0].lang,
          confidence: results[0].prob
        };
      }
    } catch (e) {
      // Fallback for short text
    }
    
    return { language: 'en', confidence: 0.5 };
  }
  
  async detectWithGoogle(text) {
    const [result] = await this.googleClient.analyzeEntities({
      document: { content: text, type: 'PLAIN_TEXT' }
    });
    
    return {
      language: result.language,
      confidence: result.languageConfidence || 0.9
    };
  }
  
  async detectWithAzure(text) {
    const response = await axios.post(
      'https://api.cognitive.microsofttranslator.com/detect?api-version=3.0',
      [{ text }],
      {
        headers: {
          'Ocp-Apim-Subscription-Key': process.env.AZURE_TRANSLATOR_KEY,
          'Content-Type': 'application/json'
        }
      }
    );
    
    return {
      language: response.data[0].language,
      confidence: response.data[0].score
    };
  }
}

// Per-speaker language tracking
class SpeakerLanguageTracker {
  constructor(detector) {
    this.detector = detector;
    this.speakerLanguages = new Map();
    this.detectionHistory = new Map();
  }
  
  async trackSpeaker(speakerId, text) {
    const detection = await this.detector.detect(text);
    
    if (!this.detectionHistory.has(speakerId)) {
      this.detectionHistory.set(speakerId, []);
    }
    
    const history = this.detectionHistory.get(speakerId);
    history.push(detection);
    
    // Keep last 10 detections
    if (history.length > 10) {
      history.shift();
    }
    
    // Determine dominant language
    const langCounts = {};
    for (const d of history) {
      langCounts[d.language] = (langCounts[d.language] || 0) + d.confidence;
    }
    
    const dominantLang = Object.entries(langCounts)
      .sort((a, b) => b[1] - a[1])[0][0];
    
    this.speakerLanguages.set(speakerId, dominantLang);
    
    return dominantLang;
  }
  
  getSpeakerLanguage(speakerId) {
    return this.speakerLanguages.get(speakerId) || 'en';
  }
}

// Usage
const detector = new LanguageDetector({ method: 'local' });
const tracker = new SpeakerLanguageTracker(detector);

receiver.onTranscript = async (segment) => {
  const language = await tracker.trackSpeaker(segment.speakerId, segment.text);
  console.log(`${segment.speakerName} speaks: ${language}`);
  
  // Route to appropriate translator
  if (language !== 'en') {
    const translated = await translator.translate(segment.text, 'en', language);
    displayEnglishCaption(translated);
  }
};
```

### Python

```python
from langdetect import detect, detect_langs
from typing import Dict, List
from collections import Counter

class LanguageDetector:
    def detect(self, text: str) -> Dict:
        try:
            probs = detect_langs(text)
            if probs:
                return {
                    'language': probs[0].lang,
                    'confidence': probs[0].prob
                }
        except:
            pass
        
        return {'language': 'en', 'confidence': 0.5}

class SpeakerLanguageTracker:
    def __init__(self, detector: LanguageDetector):
        self.detector = detector
        self.speaker_history: Dict[str, List] = {}
    
    def track_speaker(self, speaker_id: str, text: str) -> str:
        detection = self.detector.detect(text)
        
        if speaker_id not in self.speaker_history:
            self.speaker_history[speaker_id] = []
        
        history = self.speaker_history[speaker_id]
        history.append(detection)
        
        if len(history) > 10:
            history.pop(0)
        
        # Find dominant language
        weighted = Counter()
        for d in history:
            weighted[d['language']] += d['confidence']
        
        return weighted.most_common(1)[0][0]

# Usage
detector = LanguageDetector()
tracker = SpeakerLanguageTracker(detector)

def on_transcript(segment):
    language = tracker.track_speaker(segment['speaker_id'], segment['text'])
    print(f"{segment['speaker_name']} speaks: {language}")
```

## Resources

- **langdetect**: https://github.com/Mimino666/langdetect
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

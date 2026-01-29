# Keyword Detection

Detect important keywords from RTMS transcripts using RAKE and YAKE algorithms.

## Overview

Keyword detection helps identify the most important terms and concepts from meeting transcripts. This use case demonstrates two popular algorithms:

- **RAKE** (Rapid Automatic Keyword Extraction): Identifies keywords by analyzing word frequency and co-occurrence
- **YAKE** (Yet Another Keyword Extractor): Language-independent algorithm that doesn't require training data

## JavaScript Example

### Using RAKE Algorithm

```javascript
// Install: npm install rake-js

const rake = require('rake-js');

const transcript = `
The quarterly earnings report shows strong growth in cloud services. 
Our AI-powered analytics platform has seen a 45% increase in adoption. 
We need to focus on customer retention and expand our enterprise solutions. 
The machine learning models are performing exceptionally well in production.
`;

// Extract keywords using RAKE
const keywords = rake.extract(transcript);

console.log('Top Keywords:');
keywords.slice(0, 10).forEach(([keyword, score]) => {
  console.log(`${keyword}: ${score.toFixed(2)}`);
});

// Output example:
// cloud services: 8.5
// AI-powered analytics platform: 7.2
// customer retention: 6.8
// machine learning models: 6.5
// enterprise solutions: 5.9
```

### Using YAKE Algorithm

```javascript
// Install: npm install yake

const yake = require('yake');

const transcript = `
The quarterly earnings report shows strong growth in cloud services. 
Our AI-powered analytics platform has seen a 45% increase in adoption. 
We need to focus on customer retention and expand our enterprise solutions. 
The machine learning models are performing exceptionally well in production.
`;

// Extract keywords using YAKE
const keywords = yake.extract(transcript, {
  top: 10,
  stopwords: 'english'
});

console.log('Top Keywords (YAKE):');
keywords.forEach(keyword => {
  console.log(`${keyword.text}: ${keyword.score.toFixed(4)}`);
});

// Output example:
// cloud services: 0.0234
// AI-powered analytics: 0.0312
// customer retention: 0.0289
// machine learning: 0.0267
```

### Processing RTMS Transcript Stream

```javascript
const WebSocket = require('ws');
const rake = require('rake-js');

class RTMSKeywordDetector {
  constructor(meetingId, accessToken) {
    this.meetingId = meetingId;
    this.accessToken = accessToken;
    this.transcript = '';
    this.keywords = [];
  }

  async connectToRTMS() {
    const wsUrl = `wss://rtms.zoom.us/v1/meetings/${this.meetingId}`;
    this.ws = new WebSocket(wsUrl, {
      headers: {
        'Authorization': `Bearer ${this.accessToken}`
      }
    });

    this.ws.on('message', (data) => {
      const message = JSON.parse(data);
      
      if (message.type === 'transcript') {
        this.transcript += ' ' + message.text;
        
        // Extract keywords every 500 words
        if (this.transcript.split(' ').length % 500 === 0) {
          this.updateKeywords();
        }
      }
    });
  }

  updateKeywords() {
    this.keywords = rake.extract(this.transcript).slice(0, 15);
    console.log('Updated Keywords:', this.keywords);
  }

  getTopKeywords(limit = 10) {
    return this.keywords.slice(0, limit);
  }
}

// Usage
const detector = new RTMSKeywordDetector('meeting-123', 'your-access-token');
detector.connectToRTMS();
```

## Python Example

### Using RAKE Algorithm

```python
# Install: pip install rake-nltk

from rake_nltk import Rake
import nltk

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

transcript = """
The quarterly earnings report shows strong growth in cloud services. 
Our AI-powered analytics platform has seen a 45% increase in adoption. 
We need to focus on customer retention and expand our enterprise solutions. 
The machine learning models are performing exceptionally well in production.
"""

# Initialize RAKE
rake = Rake(language='english')
rake.extract_keywords_from_text(transcript)

# Get ranked keywords
keywords = rake.get_ranked_phrases_with_scores()

print("Top Keywords (RAKE):")
for score, keyword in keywords[:10]:
    print(f"{keyword}: {score:.2f}")

# Output:
# cloud services: 8.50
# AI-powered analytics platform: 7.20
# customer retention: 6.80
# machine learning models: 6.50
# enterprise solutions: 5.90
```

### Using YAKE Algorithm

```python
# Install: pip install yake

import yake

transcript = """
The quarterly earnings report shows strong growth in cloud services. 
Our AI-powered analytics platform has seen a 45% increase in adoption. 
We need to focus on customer retention and expand our enterprise solutions. 
The machine learning models are performing exceptionally well in production.
"""

# Initialize YAKE
kw_extractor = yake.KeywordExtractor(
    lan="en",
    n=3,  # max n-gram size
    top=10,
    features=None
)

# Extract keywords
keywords = kw_extractor.extract_keywords(transcript)

print("Top Keywords (YAKE):")
for keyword, score in keywords:
    print(f"{keyword}: {score:.4f}")

# Output:
# cloud services: 0.0234
# AI-powered analytics: 0.0312
# customer retention: 0.0289
# machine learning: 0.0267
```

### Processing RTMS Transcript Stream

```python
import asyncio
import json
import websockets
from rake_nltk import Rake
import nltk

nltk.download('punkt')
nltk.download('stopwords')

class RTMSKeywordDetector:
    def __init__(self, meeting_id, access_token):
        self.meeting_id = meeting_id
        self.access_token = access_token
        self.transcript = ""
        self.keywords = []
        self.rake = Rake(language='english')
        self.word_count = 0

    async def connect_to_rtms(self):
        """Connect to RTMS WebSocket and process transcript"""
        ws_url = f"wss://rtms.zoom.us/v1/meetings/{self.meeting_id}"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        async with websockets.connect(ws_url, subprotocols=['rtms']) as websocket:
            async for message in websocket:
                data = json.loads(message)
                
                if data.get('type') == 'transcript':
                    self.transcript += ' ' + data.get('text', '')
                    self.word_count += len(data.get('text', '').split())
                    
                    # Update keywords every 500 words
                    if self.word_count % 500 == 0:
                        self.update_keywords()

    def update_keywords(self):
        """Extract and update keywords from transcript"""
        self.rake.extract_keywords_from_text(self.transcript)
        self.keywords = self.rake.get_ranked_phrases_with_scores()
        
        print("Updated Keywords:")
        for score, keyword in self.keywords[:15]:
            print(f"  {keyword}: {score:.2f}")

    def get_top_keywords(self, limit=10):
        """Get top N keywords"""
        return self.keywords[:limit]

    async def run(self):
        """Run the detector"""
        try:
            await self.connect_to_rtms()
        except Exception as e:
            print(f"Error: {e}")

# Usage
async def main():
    detector = RTMSKeywordDetector('meeting-123', 'your-access-token')
    await detector.run()

if __name__ == "__main__":
    asyncio.run(main())
```

## Comparison: RAKE vs YAKE

| Feature | RAKE | YAKE |
|---------|------|------|
| **Language Support** | Multiple languages | Language-independent |
| **Training Required** | No | No |
| **Speed** | Fast | Very fast |
| **Accuracy** | Good for English | Consistent across languages |
| **Dependencies** | NLTK stopwords | Minimal |
| **Best For** | English transcripts | Multilingual meetings |

## Best Practices

1. **Preprocessing**: Clean transcripts before keyword extraction
   - Remove filler words (um, uh, like)
   - Normalize speaker names and timestamps
   - Handle acronyms consistently

2. **Tuning Parameters**:
   - Adjust n-gram size based on keyword length preferences
   - Set appropriate top-K limits for your use case
   - Consider domain-specific stopwords

3. **Real-time Processing**:
   - Process in chunks to avoid memory issues
   - Update keywords periodically (every 500-1000 words)
   - Cache results for performance

4. **Post-processing**:
   - Filter out generic terms
   - Group related keywords
   - Rank by relevance to meeting context

## Integration with RTMS

```javascript
// Complete integration example
const RTMSClient = require('@zoom/rtms-sdk');
const rake = require('rake-js');

class MeetingAnalyzer {
  constructor(meetingId, accessToken) {
    this.client = new RTMSClient(accessToken);
    this.meetingId = meetingId;
    this.transcript = '';
  }

  async analyzeMeeting() {
    const stream = await this.client.getTranscriptStream(this.meetingId);
    
    stream.on('data', (chunk) => {
      this.transcript += chunk.text + ' ';
    });

    stream.on('end', () => {
      const keywords = rake.extract(this.transcript).slice(0, 20);
      return {
        meetingId: this.meetingId,
        keywords: keywords,
        summary: this.generateSummary(keywords)
      };
    });
  }

  generateSummary(keywords) {
    return keywords.map(([keyword]) => keyword).join(', ');
  }
}
```

## See Also

- [RTMS Transcription](./rtms-transcription.md)
- [Meeting Analytics](./meeting-analytics.md)
- [Real-time Messaging Service](../features/rtms.md)

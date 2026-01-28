# Filler Word Detection

## Brief
Detect filler words like "um", "uh", "like" in real-time meeting transcripts using the Zoom Real-Time Messaging Service (RTMS).

## Overview
Filler words are common speech patterns that don't add semantic value to communication. This use case demonstrates how to identify and track filler word usage during Zoom meetings using RTMS for real-time transcript analysis.

## JavaScript Example

```javascript
const WebSocket = require('ws');

// Filler words to detect
const FILLER_WORDS = ['um', 'uh', 'like', 'you know', 'basically', 'literally', 'actually'];

class FillerWordDetector {
  constructor(rtmsUrl, accessToken) {
    this.rtmsUrl = rtmsUrl;
    this.accessToken = accessToken;
    this.fillerWordCounts = {};
    this.initializeFillerCounts();
  }

  initializeFillerCounts() {
    FILLER_WORDS.forEach(word => {
      this.fillerWordCounts[word] = 0;
    });
  }

  connect() {
    this.ws = new WebSocket(this.rtmsUrl, {
      headers: {
        'Authorization': `Bearer ${this.accessToken}`
      }
    });

    this.ws.on('message', (data) => {
      this.processTranscript(data);
    });

    this.ws.on('error', (error) => {
      console.error('WebSocket error:', error);
    });
  }

  processTranscript(data) {
    const message = JSON.parse(data);
    
    if (message.type === 'caption') {
      const text = message.payload.text.toLowerCase();
      this.detectFillerWords(text);
    }
  }

  detectFillerWords(text) {
    FILLER_WORDS.forEach(word => {
      const regex = new RegExp(`\\b${word}\\b`, 'gi');
      const matches = text.match(regex);
      
      if (matches) {
        this.fillerWordCounts[word] += matches.length;
        console.log(`Detected "${word}": ${matches.length} occurrence(s)`);
      }
    });
  }

  getReport() {
    return {
      timestamp: new Date().toISOString(),
      fillerWords: this.fillerWordCounts,
      totalFillerWords: Object.values(this.fillerWordCounts).reduce((a, b) => a + b, 0)
    };
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
    }
  }
}

// Usage
const detector = new FillerWordDetector(
  'wss://rtms.zoom.us/v1',
  'YOUR_ACCESS_TOKEN'
);

detector.connect();

// Get report after meeting
setTimeout(() => {
  console.log(detector.getReport());
  detector.disconnect();
}, 3600000); // 1 hour
```

## Python Example

```python
import asyncio
import json
import re
import websockets
from datetime import datetime
from typing import Dict, List

FILLER_WORDS = ['um', 'uh', 'like', 'you know', 'basically', 'literally', 'actually']

class FillerWordDetector:
    def __init__(self, rtms_url: str, access_token: str):
        self.rtms_url = rtms_url
        self.access_token = access_token
        self.filler_word_counts: Dict[str, int] = {}
        self.initialize_filler_counts()
    
    def initialize_filler_counts(self):
        """Initialize counter for each filler word."""
        for word in FILLER_WORDS:
            self.filler_word_counts[word] = 0
    
    async def connect(self):
        """Connect to RTMS WebSocket."""
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        try:
            async with websockets.connect(self.rtms_url, subprotocols=['rtms']) as websocket:
                await self.listen(websocket)
        except Exception as e:
            print(f"Connection error: {e}")
    
    async def listen(self, websocket):
        """Listen for incoming transcript messages."""
        try:
            async for message in websocket:
                await self.process_transcript(message)
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
    
    async def process_transcript(self, data: str):
        """Process incoming transcript data."""
        try:
            message = json.loads(data)
            
            if message.get('type') == 'caption':
                text = message.get('payload', {}).get('text', '').lower()
                self.detect_filler_words(text)
        except json.JSONDecodeError:
            print("Failed to parse message")
    
    def detect_filler_words(self, text: str):
        """Detect and count filler words in text."""
        for word in FILLER_WORDS:
            # Use word boundaries to match whole words only
            pattern = rf'\b{re.escape(word)}\b'
            matches = re.findall(pattern, text, re.IGNORECASE)
            
            if matches:
                self.filler_word_counts[word] += len(matches)
                print(f'Detected "{word}": {len(matches)} occurrence(s)')
    
    def get_report(self) -> Dict:
        """Generate filler word detection report."""
        total_fillers = sum(self.filler_word_counts.values())
        
        return {
            'timestamp': datetime.now().isoformat(),
            'filler_words': self.filler_word_counts,
            'total_filler_words': total_fillers,
            'most_common': max(
                self.filler_word_counts.items(),
                key=lambda x: x[1]
            ) if total_fillers > 0 else None
        }

# Usage
async def main():
    detector = FillerWordDetector(
        'wss://rtms.zoom.us/v1',
        'YOUR_ACCESS_TOKEN'
    )
    
    # Run for 1 hour
    try:
        await asyncio.wait_for(detector.connect(), timeout=3600)
    except asyncio.TimeoutError:
        print("Session timeout")
    
    # Print report
    print(json.dumps(detector.get_report(), indent=2))

if __name__ == '__main__':
    asyncio.run(main())
```

## Key Features

- **Real-time Detection**: Processes captions as they arrive from RTMS
- **Word Boundary Matching**: Uses regex to match whole words only
- **Aggregated Reporting**: Tracks counts across the entire session
- **Extensible**: Easy to add more filler words to the detection list

## Integration Steps

1. Authenticate with Zoom OAuth to obtain access token
2. Connect to RTMS WebSocket endpoint
3. Subscribe to caption messages
4. Process incoming text for filler word patterns
5. Generate reports on demand

## Use Cases

- **Speaker Coaching**: Identify speakers who use excessive filler words
- **Meeting Quality Analysis**: Track communication patterns over time
- **Presentation Feedback**: Provide real-time feedback to presenters
- **Communication Training**: Measure improvement in speech clarity

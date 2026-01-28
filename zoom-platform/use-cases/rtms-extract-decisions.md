# Extract Decisions

## Brief

Extract key decisions from RTMS (Real-Time Messaging Service) transcripts. This use case demonstrates how to identify, parse, and structure decisions made during meetings using the Zoom platform APIs.

## Overview

Meeting transcripts often contain important decisions that need to be captured and tracked. This guide shows how to:
- Parse RTMS transcript data
- Identify decision statements using pattern matching
- Extract decision metadata (who, what, when, context)
- Structure decisions for downstream processing

## JavaScript Example

### Basic Decision Extraction

```javascript
const axios = require('axios');

class DecisionExtractor {
  constructor(accessToken) {
    this.accessToken = accessToken;
    this.client = axios.create({
      baseURL: 'https://api.zoom.us/v2',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      }
    });
  }

  /**
   * Fetch RTMS transcript for a meeting
   */
  async getTranscript(meetingId) {
    try {
      const response = await this.client.get(
        `/meetings/${meetingId}/recordings`
      );
      return response.data;
    } catch (error) {
      console.error('Error fetching transcript:', error.message);
      throw error;
    }
  }

  /**
   * Identify decision patterns in transcript text
   */
  identifyDecisions(transcript) {
    const decisionPatterns = [
      /we\s+(?:decided|will|agreed)\s+(?:to|that)\s+(.+?)(?:\.|,|$)/gi,
      /decision:\s*(.+?)(?:\.|,|$)/gi,
      /(?:let's|let us)\s+(.+?)(?:\.|,|$)/gi,
      /we\s+(?:should|must|need to)\s+(.+?)(?:\.|,|$)/gi,
      /action item:\s*(.+?)(?:\.|,|$)/gi
    ];

    const decisions = [];
    const lines = transcript.split('\n');

    lines.forEach((line, index) => {
      decisionPatterns.forEach(pattern => {
        let match;
        while ((match = pattern.exec(line)) !== null) {
          decisions.push({
            text: match[1].trim(),
            lineNumber: index + 1,
            context: line.trim(),
            confidence: this.calculateConfidence(match[0])
          });
        }
      });
    });

    return decisions;
  }

  /**
   * Calculate confidence score for decision match
   */
  calculateConfidence(matchText) {
    const strongIndicators = ['decided', 'agreed', 'will', 'must'];
    const weakIndicators = ['should', 'could', 'might'];

    let score = 0.5;
    strongIndicators.forEach(indicator => {
      if (matchText.toLowerCase().includes(indicator)) {
        score = Math.min(1.0, score + 0.25);
      }
    });

    return Math.round(score * 100) / 100;
  }

  /**
   * Extract structured decision data
   */
  extractDecisionMetadata(decisions, speakers) {
    return decisions.map(decision => ({
      id: `decision_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      statement: decision.text,
      context: decision.context,
      lineNumber: decision.lineNumber,
      confidence: decision.confidence,
      speaker: this.identifySpeaker(decision.lineNumber, speakers),
      timestamp: this.estimateTimestamp(decision.lineNumber),
      status: 'pending',
      tags: this.extractTags(decision.text)
    }));
  }

  /**
   * Identify speaker from line number
   */
  identifySpeaker(lineNumber, speakers) {
    // Match line number to speaker data
    return speakers.find(s => s.lineStart <= lineNumber && s.lineEnd >= lineNumber)?.name || 'Unknown';
  }

  /**
   * Estimate timestamp based on line position
   */
  estimateTimestamp(lineNumber) {
    // Rough estimation: assume ~10 lines per minute
    const minutes = Math.floor(lineNumber / 10);
    const seconds = (lineNumber % 10) * 6;
    return `${Math.floor(minutes / 60)}:${String(minutes % 60).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
  }

  /**
   * Extract relevant tags from decision text
   */
  extractTags(text) {
    const tags = [];
    const keywords = ['budget', 'timeline', 'resource', 'feature', 'bug', 'release', 'meeting', 'review'];
    
    keywords.forEach(keyword => {
      if (text.toLowerCase().includes(keyword)) {
        tags.push(keyword);
      }
    });

    return tags;
  }

  /**
   * Process full transcript and return structured decisions
   */
  async processTranscript(meetingId, transcriptText, speakers) {
    const decisions = this.identifyDecisions(transcriptText);
    const structured = this.extractDecisionMetadata(decisions, speakers);
    
    return {
      meetingId,
      totalDecisions: structured.length,
      decisions: structured,
      extractedAt: new Date().toISOString()
    };
  }
}

// Usage Example
async function main() {
  const extractor = new DecisionExtractor(process.env.ZOOM_ACCESS_TOKEN);
  
  const sampleTranscript = `
    John: We need to improve our API response time.
    Sarah: I agree. We decided to implement caching for frequently accessed endpoints.
    John: Good. Let's also add monitoring to track performance improvements.
    Sarah: Action item: I'll set up the monitoring dashboard by next Friday.
  `;

  const speakers = [
    { name: 'John', lineStart: 1, lineEnd: 3 },
    { name: 'Sarah', lineStart: 2, lineEnd: 4 }
  ];

  const result = await extractor.processTranscript(
    'meeting_123',
    sampleTranscript,
    speakers
  );

  console.log(JSON.stringify(result, null, 2));
}

main().catch(console.error);
```

## Python Example

### Decision Extraction with NLP

```python
import re
import json
from datetime import datetime
from typing import List, Dict, Tuple
import requests

class RTMSDecisionExtractor:
    """Extract decisions from RTMS meeting transcripts"""
    
    DECISION_PATTERNS = [
        r"we\s+(?:decided|will|agreed)\s+(?:to|that)\s+(.+?)(?:\.|,|$)",
        r"decision:\s*(.+?)(?:\.|,|$)",
        r"(?:let's|let us)\s+(.+?)(?:\.|,|$)",
        r"we\s+(?:should|must|need to)\s+(.+?)(?:\.|,|$)",
        r"action item:\s*(.+?)(?:\.|,|$)"
    ]
    
    STRONG_INDICATORS = {'decided', 'agreed', 'will', 'must', 'committed'}
    WEAK_INDICATORS = {'should', 'could', 'might', 'consider'}
    
    def __init__(self, access_token: str):
        """Initialize with Zoom API access token"""
        self.access_token = access_token
        self.base_url = "https://api.zoom.us/v2"
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    
    def fetch_transcript(self, meeting_id: str) -> Dict:
        """Fetch RTMS transcript from Zoom API"""
        try:
            response = requests.get(
                f"{self.base_url}/meetings/{meeting_id}/recordings",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching transcript: {e}")
            raise
    
    def identify_decisions(self, transcript: str) -> List[Dict]:
        """Identify decision statements in transcript"""
        decisions = []
        lines = transcript.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for pattern in self.DECISION_PATTERNS:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    decision_text = match.group(1).strip()
                    confidence = self._calculate_confidence(match.group(0))
                    
                    decisions.append({
                        'text': decision_text,
                        'line_number': line_num,
                        'context': line.strip(),
                        'confidence': confidence,
                        'match_text': match.group(0)
                    })
        
        return decisions
    
    def _calculate_confidence(self, match_text: str) -> float:
        """Calculate confidence score for decision match"""
        score = 0.5
        text_lower = match_text.lower()
        
        # Check for strong indicators
        for indicator in self.STRONG_INDICATORS:
            if indicator in text_lower:
                score = min(1.0, score + 0.25)
        
        # Check for weak indicators
        for indicator in self.WEAK_INDICATORS:
            if indicator in text_lower:
                score = max(0.3, score - 0.1)
        
        return round(score, 2)
    
    def extract_metadata(
        self, 
        decisions: List[Dict], 
        speakers: List[Dict]
    ) -> List[Dict]:
        """Extract structured metadata for each decision"""
        structured = []
        
        for decision in decisions:
            speaker = self._identify_speaker(decision['line_number'], speakers)
            timestamp = self._estimate_timestamp(decision['line_number'])
            tags = self._extract_tags(decision['text'])
            
            structured.append({
                'id': f"decision_{datetime.now().timestamp()}_{hash(decision['text']) % 10000}",
                'statement': decision['text'],
                'context': decision['context'],
                'line_number': decision['line_number'],
                'confidence': decision['confidence'],
                'speaker': speaker,
                'timestamp': timestamp,
                'status': 'pending',
                'tags': tags,
                'created_at': datetime.now().isoformat()
            })
        
        return structured
    
    def _identify_speaker(self, line_number: int, speakers: List[Dict]) -> str:
        """Identify speaker from line number"""
        for speaker in speakers:
            if speaker['line_start'] <= line_number <= speaker['line_end']:
                return speaker['name']
        return 'Unknown'
    
    def _estimate_timestamp(self, line_number: int) -> str:
        """Estimate timestamp based on line position"""
        # Assume ~10 lines per minute
        total_seconds = (line_number // 10) * 60 + (line_number % 10) * 6
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    
    def _extract_tags(self, text: str) -> List[str]:
        """Extract relevant tags from decision text"""
        keywords = [
            'budget', 'timeline', 'resource', 'feature', 'bug', 
            'release', 'meeting', 'review', 'deadline', 'priority'
        ]
        tags = []
        text_lower = text.lower()
        
        for keyword in keywords:
            if keyword in text_lower:
                tags.append(keyword)
        
        return tags
    
    def process_transcript(
        self, 
        meeting_id: str, 
        transcript_text: str, 
        speakers: List[Dict]
    ) -> Dict:
        """Process full transcript and return structured decisions"""
        decisions = self.identify_decisions(transcript_text)
        structured = self.extract_metadata(decisions, speakers)
        
        return {
            'meeting_id': meeting_id,
            'total_decisions': len(structured),
            'decisions': structured,
            'extracted_at': datetime.now().isoformat(),
            'summary': self._generate_summary(structured)
        }
    
    def _generate_summary(self, decisions: List[Dict]) -> Dict:
        """Generate summary statistics"""
        if not decisions:
            return {'total': 0, 'by_status': {}, 'by_tag': {}}
        
        by_tag = {}
        for decision in decisions:
            for tag in decision['tags']:
                by_tag[tag] = by_tag.get(tag, 0) + 1
        
        return {
            'total': len(decisions),
            'high_confidence': sum(1 for d in decisions if d['confidence'] >= 0.8),
            'by_tag': by_tag,
            'speakers': list(set(d['speaker'] for d in decisions))
        }


# Usage Example
if __name__ == "__main__":
    extractor = RTMSDecisionExtractor(access_token="your_zoom_token")
    
    sample_transcript = """
    John: We need to improve our API response time.
    Sarah: I agree. We decided to implement caching for frequently accessed endpoints.
    John: Good. Let's also add monitoring to track performance improvements.
    Sarah: Action item: I'll set up the monitoring dashboard by next Friday.
    John: Perfect. We must complete this by end of Q1.
    """
    
    speakers = [
        {'name': 'John', 'line_start': 1, 'line_end': 4},
        {'name': 'Sarah', 'line_start': 2, 'line_end': 5}
    ]
    
    result = extractor.process_transcript(
        meeting_id='meeting_123',
        transcript_text=sample_transcript,
        speakers=speakers
    )
    
    print(json.dumps(result, indent=2))
```

## Key Features

- **Pattern Matching**: Identifies decision statements using regex patterns
- **Confidence Scoring**: Rates decision confidence based on language indicators
- **Metadata Extraction**: Captures speaker, timestamp, and context
- **Tag Classification**: Automatically tags decisions by topic
- **Speaker Attribution**: Links decisions to meeting participants
- **Status Tracking**: Maintains decision status (pending, completed, etc.)

## Integration with Zoom APIs

Both examples integrate with Zoom's REST API to:
- Fetch meeting recordings and transcripts
- Access RTMS data streams
- Store extracted decisions for tracking

## Next Steps

- Implement decision tracking dashboard
- Add decision completion workflows
- Integrate with project management tools
- Set up automated decision notifications

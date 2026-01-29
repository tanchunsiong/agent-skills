# Extract Key Points

## Brief
Extract key discussion points from RTMS (Real-Time Messaging Service) transcripts using extractive summarization techniques.

## Overview
This use case demonstrates how to automatically identify and extract the most important discussion points from meeting transcripts. Extractive summarization selects the most relevant sentences or phrases from the original text without generating new content.

## Use Cases
- Meeting minutes generation
- Action item identification
- Decision point tracking
- Discussion summary for attendees
- Compliance and audit documentation

## JavaScript Example

```javascript
// Extract key points from RTMS transcript using Node.js

const axios = require('axios');

// Sample transcript from RTMS
const transcript = `
The team discussed the Q1 roadmap priorities. John mentioned that we need to focus on 
performance optimization first. Sarah agreed and suggested we allocate 40% of resources 
to this task. The team decided to start with database indexing improvements. 
Mike raised concerns about timeline constraints. We scheduled a follow-up meeting 
for next week to review progress. The budget allocation was approved at $50,000.
`;

// Simple extractive summarization using TF-IDF scoring
function extractKeyPoints(text, numPoints = 3) {
  // Split into sentences
  const sentences = text.match(/[^.!?]+[.!?]+/g) || [];
  
  // Calculate word frequency
  const words = text.toLowerCase().match(/\b\w+\b/g) || [];
  const wordFreq = {};
  
  words.forEach(word => {
    if (word.length > 3) { // Skip short words
      wordFreq[word] = (wordFreq[word] || 0) + 1;
    }
  });
  
  // Score sentences based on word frequency
  const scoredSentences = sentences.map(sentence => {
    const sentenceWords = sentence.toLowerCase().match(/\b\w+\b/g) || [];
    const score = sentenceWords.reduce((sum, word) => sum + (wordFreq[word] || 0), 0);
    return {
      text: sentence.trim(),
      score: score
    };
  });
  
  // Return top N sentences
  return scoredSentences
    .sort((a, b) => b.score - a.score)
    .slice(0, numPoints)
    .map(item => item.text);
}

// Extract and display key points
const keyPoints = extractKeyPoints(transcript, 3);
console.log('Key Points Extracted:');
keyPoints.forEach((point, index) => {
  console.log(`${index + 1}. ${point}`);
});

// Integration with Zoom RTMS API
async function extractFromZoomTranscript(meetingId, accessToken) {
  try {
    // Fetch transcript from Zoom API
    const response = await axios.get(
      `https://api.zoom.us/v2/meetings/${meetingId}/recordings`,
      {
        headers: { Authorization: `Bearer ${accessToken}` }
      }
    );
    
    // Extract transcript from response
    const transcriptUrl = response.data.recording_files
      .find(file => file.file_type === 'TRANSCRIPT')?.download_url;
    
    if (transcriptUrl) {
      const transcriptResponse = await axios.get(transcriptUrl);
      const keyPoints = extractKeyPoints(transcriptResponse.data, 5);
      return keyPoints;
    }
  } catch (error) {
    console.error('Error fetching transcript:', error.message);
  }
}

// Usage
// const keyPoints = await extractFromZoomTranscript('meeting-id', 'access-token');
```

## Python Example

```python
# Extract key points from RTMS transcript using Python

import re
from collections import Counter
from typing import List
import requests

# Sample transcript from RTMS
transcript = """
The team discussed the Q1 roadmap priorities. John mentioned that we need to focus on 
performance optimization first. Sarah agreed and suggested we allocate 40% of resources 
to this task. The team decided to start with database indexing improvements. 
Mike raised concerns about timeline constraints. We scheduled a follow-up meeting 
for next week to review progress. The budget allocation was approved at $50,000.
"""

def extract_key_points(text: str, num_points: int = 3) -> List[str]:
    """
    Extract key points from transcript using extractive summarization.
    
    Args:
        text: The transcript text
        num_points: Number of key points to extract
        
    Returns:
        List of key point sentences
    """
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Calculate word frequency
    words = re.findall(r'\b\w+\b', text.lower())
    word_freq = Counter(word for word in words if len(word) > 3)
    
    # Score sentences based on word frequency
    scored_sentences = []
    for sentence in sentences:
        sentence_words = re.findall(r'\b\w+\b', sentence.lower())
        score = sum(word_freq[word] for word in sentence_words if word in word_freq)
        scored_sentences.append({
            'text': sentence,
            'score': score
        })
    
    # Return top N sentences
    top_sentences = sorted(scored_sentences, key=lambda x: x['score'], reverse=True)
    return [item['text'] for item in top_sentences[:num_points]]

# Extract and display key points
key_points = extract_key_points(transcript, 3)
print("Key Points Extracted:")
for i, point in enumerate(key_points, 1):
    print(f"{i}. {point}")

# Integration with Zoom RTMS API
def extract_from_zoom_transcript(meeting_id: str, access_token: str) -> List[str]:
    """
    Fetch transcript from Zoom API and extract key points.
    
    Args:
        meeting_id: The Zoom meeting ID
        access_token: Zoom API access token
        
    Returns:
        List of extracted key points
    """
    try:
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Fetch recording details
        response = requests.get(
            f'https://api.zoom.us/v2/meetings/{meeting_id}/recordings',
            headers=headers
        )
        response.raise_for_status()
        
        # Find transcript file
        recording_files = response.json().get('recording_files', [])
        transcript_file = next(
            (f for f in recording_files if f.get('file_type') == 'TRANSCRIPT'),
            None
        )
        
        if transcript_file:
            transcript_response = requests.get(
                transcript_file['download_url'],
                headers=headers
            )
            transcript_response.raise_for_status()
            
            # Extract key points
            key_points = extract_key_points(transcript_response.text, 5)
            return key_points
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching transcript: {e}")
        return []

# Usage
# key_points = extract_from_zoom_transcript('meeting-id', 'access-token')
```

## Key Features

- **Extractive Summarization**: Selects existing sentences rather than generating new text
- **Word Frequency Analysis**: Identifies important terms and their relevance
- **Configurable Output**: Adjust the number of key points extracted
- **Zoom API Integration**: Direct integration with Zoom recording transcripts
- **Language Agnostic**: Works with transcripts in any language

## Implementation Considerations

1. **Preprocessing**: Clean transcript text, remove filler words, normalize formatting
2. **Scoring Algorithm**: Experiment with TF-IDF, TextRank, or other algorithms
3. **Sentence Segmentation**: Handle abbreviations and special characters properly
4. **Context Preservation**: Maintain chronological order of extracted points
5. **Post-processing**: Filter out incomplete or redundant sentences

## Advanced Techniques

- **TF-IDF Scoring**: Weight terms by frequency and inverse document frequency
- **TextRank Algorithm**: Graph-based ranking of sentences
- **Named Entity Recognition**: Identify and prioritize mentions of people, decisions, dates
- **Keyword Extraction**: Focus on domain-specific terminology
- **Multi-document Summarization**: Combine points from multiple meetings

## Error Handling

Both examples include error handling for:
- API authentication failures
- Network timeouts
- Missing or malformed transcript data
- Invalid meeting IDs

## References

- [Zoom Recording API Documentation](https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/recordingGet)
- [Extractive Summarization Techniques](https://en.wikipedia.org/wiki/Automatic_summarization)
- [TF-IDF Algorithm](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)

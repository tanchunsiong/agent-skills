# Profanity Filter

## Brief
Filter inappropriate language from transcripts using real-time meeting service (RTMS) data.

## Overview
This use case demonstrates how to implement profanity filtering on Zoom meeting transcripts. By integrating profanity detection libraries, you can automatically flag or remove inappropriate language from real-time transcripts or post-meeting records.

## Use Cases
- **Content Moderation**: Ensure meeting transcripts are appropriate for organizational records
- **Compliance**: Meet content standards for regulated industries
- **Family-Friendly Environments**: Filter transcripts for public-facing content
- **Accessibility**: Clean transcripts for accessibility platforms

## JavaScript Implementation

### Using `bad-words` Library

```javascript
const Filter = require('bad-words');
const filter = new Filter();

// Example transcript from Zoom RTMS
const transcript = "This is a great meeting, but that was a damn mistake.";

// Filter the text
const cleanedTranscript = filter.clean(transcript);
console.log(cleanedTranscript);
// Output: "This is a great meeting, but that was a **** mistake."

// Check if text contains profanity
const hasProfanity = filter.isProfane(transcript);
console.log(hasProfanity); // true

// Add custom words to filter
filter.addWords('customword', 'anotherword');

// Remove words from filter
filter.removeWords('word');
```

### Integration with Zoom RTMS

```javascript
const Filter = require('bad-words');
const filter = new Filter();

// Simulate receiving transcript from Zoom RTMS
function processTranscript(transcriptData) {
  const { text, speaker, timestamp } = transcriptData;
  
  // Check for profanity
  if (filter.isProfane(text)) {
    return {
      speaker,
      timestamp,
      original: text,
      cleaned: filter.clean(text),
      flagged: true
    };
  }
  
  return {
    speaker,
    timestamp,
    text,
    flagged: false
  };
}

// Example usage
const transcriptSegment = {
  text: "That's a hell of a good idea!",
  speaker: "John Doe",
  timestamp: "00:05:30"
};

const result = processTranscript(transcriptSegment);
console.log(result);
// Output: { speaker: 'John Doe', timestamp: '00:05:30', original: "That's a hell of a good idea!", cleaned: "That's a **** of a good idea!", flagged: true }
```

## Python Implementation

### Using `better-profanity` Library

```python
from better_profanity import profanity

# Load default profanity list
profanity.load_censor_words()

# Example transcript from Zoom RTMS
transcript = "This is a great meeting, but that was a damn mistake."

# Check if text contains profanity
contains_profanity = profanity.contains_profanity(transcript)
print(contains_profanity)  # True

# Censor the text
censored = profanity.censor(transcript)
print(censored)
# Output: "This is a great meeting, but that was a **** mistake."

# Get list of profanities found
profanities = profanity.find_profanities(transcript)
print(profanities)  # ['damn']
```

### Integration with Zoom RTMS

```python
from better_profanity import profanity
import json

# Load profanity filter
profanity.load_censor_words()

def process_transcript(transcript_data):
    """
    Process transcript segment and filter profanity
    
    Args:
        transcript_data: dict with 'text', 'speaker', 'timestamp'
    
    Returns:
        dict with processing results
    """
    text = transcript_data.get('text', '')
    speaker = transcript_data.get('speaker', '')
    timestamp = transcript_data.get('timestamp', '')
    
    # Check for profanity
    if profanity.contains_profanity(text):
        return {
            'speaker': speaker,
            'timestamp': timestamp,
            'original': text,
            'censored': profanity.censor(text),
            'profanities_found': profanity.find_profanities(text),
            'flagged': True
        }
    
    return {
        'speaker': speaker,
        'timestamp': timestamp,
        'text': text,
        'flagged': False
    }

# Example usage
transcript_segment = {
    'text': "That's a hell of a good idea!",
    'speaker': 'Jane Smith',
    'timestamp': '00:05:30'
}

result = process_transcript(transcript_segment)
print(json.dumps(result, indent=2))
# Output:
# {
#   "speaker": "Jane Smith",
#   "timestamp": "00:05:30",
#   "original": "That's a hell of a good idea!",
#   "censored": "That's a **** of a good idea!",
#   "profanities_found": ["hell"],
#   "flagged": true
# }
```

### Batch Processing Meeting Transcripts

```python
from better_profanity import profanity

profanity.load_censor_words()

def process_meeting_transcript(transcript_segments):
    """
    Process entire meeting transcript
    
    Args:
        transcript_segments: list of transcript dicts
    
    Returns:
        list of processed segments with profanity flags
    """
    results = []
    flagged_count = 0
    
    for segment in transcript_segments:
        processed = process_transcript(segment)
        results.append(processed)
        
        if processed.get('flagged'):
            flagged_count += 1
    
    return {
        'total_segments': len(transcript_segments),
        'flagged_segments': flagged_count,
        'transcript': results
    }

# Example meeting transcript
meeting_transcript = [
    {'text': 'Good morning everyone', 'speaker': 'Host', 'timestamp': '00:00:00'},
    {'text': 'This is damn important', 'speaker': 'Participant 1', 'timestamp': '00:01:15'},
    {'text': 'I agree completely', 'speaker': 'Participant 2', 'timestamp': '00:02:30'},
]

results = process_meeting_transcript(meeting_transcript)
print(f"Flagged {results['flagged_segments']} out of {results['total_segments']} segments")
```

## Best Practices

1. **Customize Word Lists**: Extend default profanity lists with industry-specific or organizational terms
2. **Context Awareness**: Consider false positives (e.g., "Scunthorpe" contains a profanity but is a place name)
3. **Logging**: Log flagged content for compliance and review purposes
4. **User Notification**: Inform users when content is filtered
5. **Storage**: Store both original and filtered versions for audit trails
6. **Performance**: Cache filter results for repeated phrases in long meetings

## Installation

### JavaScript
```bash
npm install bad-words
```

### Python
```bash
pip install better-profanity
```

## References
- [bad-words NPM Package](https://www.npmjs.com/package/bad-words)
- [better-profanity PyPI Package](https://pypi.org/project/better-profanity/)
- [Zoom RTMS Documentation](https://developers.zoom.us/docs/meeting-sdk/web/rtms/)

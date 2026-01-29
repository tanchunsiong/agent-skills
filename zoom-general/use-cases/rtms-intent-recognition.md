# Intent Recognition

## Brief

Recognize speaker intent from RTMS transcripts using zero-shot classification. This use case demonstrates how to classify speaker utterances into intent categories (question, statement, request, etc.) without requiring labeled training data.

## Overview

Intent recognition is crucial for understanding speaker goals in real-time meeting transcripts. Zero-shot classification allows you to classify text into custom intent categories without fine-tuning, making it flexible for different meeting contexts.

## Use Case Scenario

When processing RTMS (Real-Time Meeting Service) transcripts, you may need to:
- Identify questions from participants
- Detect action requests
- Recognize statements vs. inquiries
- Categorize speaker intent for meeting analytics

## Implementation

### JavaScript Example

```javascript
import { pipeline } from '@xenova/transformers';

async function recognizeIntent(transcript) {
  // Initialize zero-shot classification pipeline
  const classifier = await pipeline(
    'zero-shot-classification',
    'Xenova/mobilebert-uncased-mnli'
  );

  // Define intent categories
  const intents = ['question', 'statement', 'request', 'clarification', 'agreement'];

  // Process each speaker turn
  const results = [];
  for (const turn of transcript) {
    const classification = await classifier(turn.text, intents);
    
    results.push({
      speaker: turn.speaker,
      text: turn.text,
      intent: classification.labels[0],
      confidence: classification.scores[0],
      allScores: Object.fromEntries(
        classification.labels.map((label, idx) => [label, classification.scores[idx]])
      )
    });
  }

  return results;
}

// Example usage
const transcript = [
  { speaker: 'Alice', text: 'What is the project timeline?' },
  { speaker: 'Bob', text: 'We need to complete this by Friday.' },
  { speaker: 'Alice', text: 'Can you send me the requirements document?' },
  { speaker: 'Bob', text: 'Yes, I agree with that approach.' }
];

const intents = await recognizeIntent(transcript);
console.log(intents);
```

### Python Example

```python
from transformers import pipeline

def recognize_intent(transcript):
    """
    Classify speaker intent from RTMS transcript using zero-shot classification.
    
    Args:
        transcript: List of dicts with 'speaker' and 'text' keys
        
    Returns:
        List of dicts with intent classification results
    """
    # Initialize zero-shot classification pipeline
    classifier = pipeline(
        'zero-shot-classification',
        model='facebook/bart-large-mnli'
    )
    
    # Define intent categories
    intents = ['question', 'statement', 'request', 'clarification', 'agreement']
    
    # Process each speaker turn
    results = []
    for turn in transcript:
        classification = classifier(
            turn['text'],
            intents,
            multi_class=False
        )
        
        results.append({
            'speaker': turn['speaker'],
            'text': turn['text'],
            'intent': classification['labels'][0],
            'confidence': classification['scores'][0],
            'all_scores': dict(zip(classification['labels'], classification['scores']))
        })
    
    return results


# Example usage
transcript = [
    {'speaker': 'Alice', 'text': 'What is the project timeline?'},
    {'speaker': 'Bob', 'text': 'We need to complete this by Friday.'},
    {'speaker': 'Alice', 'text': 'Can you send me the requirements document?'},
    {'speaker': 'Bob', 'text': 'Yes, I agree with that approach.'}
]

intents = recognize_intent(transcript)
for result in intents:
    print(f"{result['speaker']}: {result['intent']} (confidence: {result['confidence']:.2f})")
```

## Integration with Zoom RTMS

To integrate with Zoom's Real-Time Meeting Service:

1. **Connect to RTMS**: Use Zoom's WebSocket connection to receive live transcripts
2. **Process Transcripts**: Feed transcript segments to the intent classifier
3. **Store Results**: Save intent classifications with timestamps for meeting analytics
4. **Real-time Feedback**: Use intent data for live meeting insights or bot responses

```python
import asyncio
from zoom_rtms import RTMSClient

async def process_meeting_intents(meeting_id, access_token):
    """Process intents from live RTMS stream."""
    client = RTMSClient(access_token)
    classifier = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')
    intents = ['question', 'statement', 'request', 'clarification', 'agreement']
    
    async for transcript_event in client.stream_transcripts(meeting_id):
        # Classify intent for each speaker turn
        result = classifier(
            transcript_event['text'],
            intents,
            multi_class=False
        )
        
        # Process result (store, analyze, respond, etc.)
        print(f"{transcript_event['speaker']}: {result['labels'][0]}")
```

## Customization

### Custom Intent Categories

Adapt intent categories to your use case:

```python
# Sales meeting intents
sales_intents = ['objection', 'question', 'agreement', 'request_demo', 'pricing_inquiry']

# Support meeting intents
support_intents = ['problem_report', 'question', 'request_help', 'feedback', 'resolution_confirmed']

# Project meeting intents
project_intents = ['status_update', 'blocker', 'question', 'action_item', 'decision']
```

### Confidence Thresholding

Filter results by confidence to ensure quality:

```python
def filter_by_confidence(results, threshold=0.7):
    """Keep only high-confidence classifications."""
    return [r for r in results if r['confidence'] >= threshold]
```

## Performance Considerations

- **Model Selection**: `facebook/bart-large-mnli` is more accurate but slower; `Xenova/mobilebert-uncased-mnli` is faster
- **Batch Processing**: Process multiple utterances together for efficiency
- **Caching**: Cache classifier instance to avoid reinitialization
- **Latency**: Zero-shot classification adds ~100-500ms per utterance depending on model

## Best Practices

1. **Define Clear Intent Categories**: Use 3-7 distinct, non-overlapping intents
2. **Test with Real Data**: Validate intent categories with actual meeting transcripts
3. **Monitor Confidence**: Track confidence scores to identify ambiguous utterances
4. **Iterate Categories**: Refine intents based on classification results
5. **Handle Edge Cases**: Plan for multi-intent utterances or unclear statements

## References

- [Hugging Face Zero-Shot Classification](https://huggingface.co/tasks/zero-shot-classification)
- [Transformers.js Documentation](https://xenova.github.io/transformers.js/)
- [Zoom RTMS API](https://developers.zoom.us/docs/meeting-sdk/real-time-transcription/)

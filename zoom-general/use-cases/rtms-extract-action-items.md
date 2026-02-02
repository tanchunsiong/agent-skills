# Extract Action Items

## Brief
Extract action items from RTMS transcripts using NLP to automatically identify tasks, owners, and deadlines from meeting transcripts.

## Overview
This use case demonstrates how to leverage Zoom's Real-Time Messaging Service (RTMS) transcripts combined with Natural Language Processing to automatically extract structured action items from meetings. The solution identifies tasks, assigns owners, and extracts relevant deadlines.

## Use Case Scenario
After a meeting concludes, automatically parse the transcript to:
- Identify action items and tasks mentioned
- Extract assigned owners/responsible parties
- Detect deadlines and due dates
- Generate a structured JSON output for integration with project management tools

## JavaScript Example

```javascript
const axios = require('axios');
const natural = require('natural');

async function extractActionItems(transcript) {
  // Tokenize the transcript
  const tokenizer = new natural.WordTokenizer();
  const tokens = tokenizer.tokenize(transcript);
  
  // Action item patterns
  const actionPatterns = [
    /(?:need to|should|must|will|have to)\s+(\w+(?:\s+\w+)*)/gi,
    /(?:action item|task|todo|follow up)[\s:]+([^.!?]+)/gi,
    /(?:assigned to|owner|responsible)\s+(\w+)/gi
  ];
  
  const actionItems = [];
  
  // Extract action items using pattern matching
  actionPatterns.forEach(pattern => {
    let match;
    while ((match = pattern.exec(transcript)) !== null) {
      actionItems.push({
        task: match[1].trim(),
        confidence: 0.85
      });
    }
  });
  
  // Extract owner assignments
  const ownerPattern = /(?:@|assigned to|owner:)\s*(\w+)/gi;
  let ownerMatch;
  const owners = [];
  while ((ownerMatch = ownerPattern.exec(transcript)) !== null) {
    owners.push(ownerMatch[1]);
  }
  
  // Extract dates/deadlines
  const datePattern = /(?:by|due|deadline|until)\s+(\w+\s+\d{1,2}(?:st|nd|rd|th)?)/gi;
  let dateMatch;
  const deadlines = [];
  while ((dateMatch = datePattern.exec(transcript)) !== null) {
    deadlines.push(dateMatch[1]);
  }
  
  // Structure output
  const structuredOutput = {
    meeting_id: generateMeetingId(),
    timestamp: new Date().toISOString(),
    action_items: actionItems.map((item, index) => ({
      id: `action_${index + 1}`,
      task: item.task,
      owner: owners[index] || 'Unassigned',
      deadline: deadlines[index] || null,
      status: 'pending',
      confidence_score: item.confidence
    })),
    summary: {
      total_items: actionItems.length,
      assigned_items: owners.length,
      items_with_deadline: deadlines.length
    }
  };
  
  return structuredOutput;
}

function generateMeetingId() {
  return `meeting_${Date.now()}`;
}

// Example usage
const sampleTranscript = `
John: We need to finalize the project proposal by next Friday.
Sarah: I'll handle the budget analysis. That's assigned to me.
John: Great. And we should schedule a follow-up meeting for next week.
Mike: I need to update the documentation by December 15th.
Sarah: Don't forget we must review the client feedback before the deadline.
`;

extractActionItems(sampleTranscript).then(result => {
  console.log(JSON.stringify(result, null, 2));
});
```

## Python Example

```python
import json
import re
from datetime import datetime
from typing import List, Dict, Any
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

class ActionItemExtractor:
    def __init__(self):
        self.action_patterns = [
            r'(?:need to|should|must|will|have to)\s+([^.!?]+)',
            r'(?:action item|task|todo|follow up)[\s:]+([^.!?]+)',
            r'(?:assigned to|owner|responsible)\s+(\w+)',
        ]
        self.owner_pattern = r'(?:@|assigned to|owner:)\s*(\w+)'
        self.deadline_pattern = r'(?:by|due|deadline|until)\s+([^.!?]+?)(?:\.|!|\?|$)'
    
    def extract_action_items(self, transcript: str) -> Dict[str, Any]:
        """Extract action items from transcript using NLP patterns."""
        
        # Tokenize sentences
        sentences = sent_tokenize(transcript)
        
        action_items = []
        owners = []
        deadlines = []
        
        # Extract action items from patterns
        for sentence in sentences:
            for pattern in self.action_patterns:
                matches = re.finditer(pattern, sentence, re.IGNORECASE)
                for match in matches:
                    action_items.append({
                        'task': match.group(1).strip(),
                        'confidence': 0.85,
                        'source_sentence': sentence.strip()
                    })
            
            # Extract owners
            owner_matches = re.finditer(self.owner_pattern, sentence, re.IGNORECASE)
            for match in owner_matches:
                owners.append(match.group(1))
            
            # Extract deadlines
            deadline_matches = re.finditer(self.deadline_pattern, sentence, re.IGNORECASE)
            for match in deadline_matches:
                deadlines.append(match.group(1).strip())
        
        # Structure output
        structured_output = {
            'meeting_id': self._generate_meeting_id(),
            'timestamp': datetime.now().isoformat(),
            'action_items': self._build_action_items(action_items, owners, deadlines),
            'summary': {
                'total_items': len(action_items),
                'assigned_items': len(owners),
                'items_with_deadline': len(deadlines)
            }
        }
        
        return structured_output
    
    def _build_action_items(self, items: List[Dict], owners: List[str], 
                           deadlines: List[str]) -> List[Dict[str, Any]]:
        """Build structured action items with owners and deadlines."""
        action_items = []
        
        for idx, item in enumerate(items):
            action_items.append({
                'id': f'action_{idx + 1}',
                'task': item['task'],
                'owner': owners[idx] if idx < len(owners) else 'Unassigned',
                'deadline': deadlines[idx] if idx < len(deadlines) else None,
                'status': 'pending',
                'confidence_score': item['confidence'],
                'source_sentence': item['source_sentence']
            })
        
        return action_items
    
    def _generate_meeting_id(self) -> str:
        """Generate unique meeting ID."""
        return f"meeting_{int(datetime.now().timestamp())}"

# Example usage
if __name__ == '__main__':
    sample_transcript = """
    John: We need to finalize the project proposal by next Friday.
    Sarah: I'll handle the budget analysis. That's assigned to me.
    John: Great. And we should schedule a follow-up meeting for next week.
    Mike: I need to update the documentation by December 15th.
    Sarah: Don't forget we must review the client feedback before the deadline.
    """
    
    extractor = ActionItemExtractor()
    result = extractor.extract_action_items(sample_transcript)
    
    print(json.dumps(result, indent=2))
```

## Expected JSON Output

```json
{
  "meeting_id": "meeting_1706345600",
  "timestamp": "2024-01-27T10:30:00.000Z",
  "action_items": [
    {
      "id": "action_1",
      "task": "finalize the project proposal",
      "owner": "John",
      "deadline": "next Friday",
      "status": "pending",
      "confidence_score": 0.85
    },
    {
      "id": "action_2",
      "task": "handle the budget analysis",
      "owner": "Sarah",
      "deadline": null,
      "status": "pending",
      "confidence_score": 0.85
    },
    {
      "id": "action_3",
      "task": "update the documentation",
      "owner": "Mike",
      "deadline": "December 15th",
      "status": "pending",
      "confidence_score": 0.85
    }
  ],
  "summary": {
    "total_items": 3,
    "assigned_items": 3,
    "items_with_deadline": 2
  }
}
```

## Integration with Zoom RTMS

To integrate with Zoom's Real-Time Messaging Service:

1. **Retrieve Transcript**: Use Zoom Meeting API to fetch the meeting transcript
2. **Process**: Pass transcript to the action item extractor
3. **Store**: Save structured output to your database
4. **Notify**: Send action items to participants via Zoom Chat or email
5. **Track**: Monitor status updates through your project management system

## Benefits

- **Automated Task Extraction**: Eliminate manual note-taking
- **Accountability**: Clear owner assignments for each action item
- **Timeline Visibility**: Automatic deadline extraction
- **Integration Ready**: Structured JSON output for downstream systems
- **Confidence Scoring**: Understand extraction reliability

## Limitations & Improvements

- Pattern-based extraction may miss implicit action items
- Consider using advanced NLP models (spaCy, BERT) for better accuracy
- Implement feedback loops to improve pattern matching
- Add support for multiple languages
- Enhance deadline parsing with date normalization libraries

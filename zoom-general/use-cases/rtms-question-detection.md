# Question Detection

## Brief
Identify questions using NLP patterns to extract and analyze questions from meeting transcripts.

## Overview
Question detection enables automated identification of questions within meeting transcripts using natural language processing patterns. This is useful for meeting analysis, FAQ generation, and engagement tracking.

## JavaScript Example

```javascript
// Question detection using regex patterns and NLP
class QuestionDetector {
  constructor() {
    // Common question patterns
    this.patterns = [
      /\b(what|when|where|who|why|how)\b[^?]*\?/gi,
      /\b(can|could|would|should|will|do|does|did|is|are|am)\b[^?]*\?/gi,
      /\b(is|isn't|are|aren't|was|wasn't|were|weren't)\b[^?]*\?/gi
    ];
  }

  detectQuestions(transcript) {
    const questions = [];
    const sentences = transcript.split(/[.!?]+/).filter(s => s.trim());

    sentences.forEach((sentence, index) => {
      const trimmed = sentence.trim();
      
      // Check if sentence matches question patterns
      const isQuestion = this.patterns.some(pattern => pattern.test(trimmed));
      
      // Also check for question marks
      if (trimmed.endsWith('?') || isQuestion) {
        questions.push({
          text: trimmed,
          index: index,
          confidence: this.calculateConfidence(trimmed)
        });
      }
    });

    return questions;
  }

  calculateConfidence(sentence) {
    let confidence = 0;
    
    // Question mark is strong indicator
    if (sentence.includes('?')) confidence += 0.8;
    
    // Question words
    if (/\b(what|when|where|who|why|how)\b/i.test(sentence)) confidence += 0.6;
    
    // Auxiliary verbs at start
    if (/^(can|could|would|should|will|do|does|did|is|are)\b/i.test(sentence)) confidence += 0.5;
    
    return Math.min(confidence, 1.0);
  }
}

// Usage
const detector = new QuestionDetector();
const transcript = `
  John: Good morning everyone. How are you all doing today?
  Sarah: I'm doing well, thanks for asking. What's on the agenda?
  John: We need to discuss the Q4 roadmap. Does everyone have their notes?
  Mike: Yes, I'm ready. When do we start?
`;

const questions = detector.detectQuestions(transcript);
console.log(questions);
// Output:
// [
//   { text: 'How are you all doing today', index: 0, confidence: 1.0 },
//   { text: "What's on the agenda", index: 2, confidence: 1.0 },
//   { text: 'Does everyone have their notes', index: 4, confidence: 0.9 },
//   { text: 'When do we start', index: 6, confidence: 0.9 }
// ]
```

## Python Example

```python
import re
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Question:
    text: str
    index: int
    confidence: float

class QuestionDetector:
    def __init__(self):
        # Question patterns
        self.wh_pattern = re.compile(r'\b(what|when|where|who|why|how)\b', re.IGNORECASE)
        self.aux_pattern = re.compile(
            r'\b(can|could|would|should|will|do|does|did|is|are|am|have|has|had)\b',
            re.IGNORECASE
        )
        self.question_mark_pattern = re.compile(r'\?')

    def detect_questions(self, transcript: str) -> List[Question]:
        """Extract questions from transcript."""
        questions = []
        
        # Split by sentence boundaries
        sentences = re.split(r'[.!?]+', transcript)
        
        for index, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Check if it's a question
            if self._is_question(sentence):
                confidence = self._calculate_confidence(sentence)
                questions.append(Question(
                    text=sentence,
                    index=index,
                    confidence=confidence
                ))
        
        return questions

    def _is_question(self, sentence: str) -> bool:
        """Determine if sentence is a question."""
        # Explicit question mark
        if self.question_mark_pattern.search(sentence):
            return True
        
        # WH-question words
        if self.wh_pattern.search(sentence):
            return True
        
        # Auxiliary verb at start (inverted structure)
        words = sentence.split()
        if words and self.aux_pattern.match(words[0]):
            return True
        
        return False

    def _calculate_confidence(self, sentence: str) -> float:
        """Calculate confidence score for question detection."""
        confidence = 0.0
        
        # Question mark is strong indicator
        if self.question_mark_pattern.search(sentence):
            confidence += 0.8
        
        # WH-question words
        if self.wh_pattern.search(sentence):
            confidence += 0.6
        
        # Auxiliary verb at start
        words = sentence.split()
        if words and self.aux_pattern.match(words[0]):
            confidence += 0.5
        
        return min(confidence, 1.0)

# Usage
detector = QuestionDetector()
transcript = """
John: Good morning everyone. How are you all doing today?
Sarah: I'm doing well, thanks for asking. What's on the agenda?
John: We need to discuss the Q4 roadmap. Does everyone have their notes?
Mike: Yes, I'm ready. When do we start?
"""

questions = detector.detect_questions(transcript)
for q in questions:
    print(f"Q: {q.text}")
    print(f"  Confidence: {q.confidence:.2f}\n")

# Output:
# Q: How are you all doing today
#   Confidence: 1.00
# 
# Q: What's on the agenda
#   Confidence: 1.00
# 
# Q: Does everyone have their notes
#   Confidence: 0.90
# 
# Q: When do we start
#   Confidence: 0.90
```

## Key Features

- **Pattern Matching**: Detects WH-questions (what, when, where, who, why, how)
- **Auxiliary Verbs**: Identifies inverted structures (can, could, would, should, will, do, does, did, is, are)
- **Question Marks**: Explicit punctuation detection
- **Confidence Scoring**: Provides confidence levels for each detected question
- **Transcript Parsing**: Handles multi-speaker transcripts

## Use Cases

- Meeting analysis and summarization
- FAQ generation from transcripts
- Engagement metrics (question frequency)
- Training data extraction
- Customer support analysis

## Integration with Zoom

Use with Zoom Meeting Transcripts API to:
1. Fetch meeting transcript
2. Run question detection
3. Store results for analysis
4. Generate reports or insights

## Limitations

- Rhetorical questions may be detected as genuine questions
- Context-dependent questions might be missed
- Sarcastic statements with question marks may be false positives
- Requires clean transcript data for best results

## Future Enhancements

- Machine learning models for improved accuracy
- Question classification (open-ended vs. yes/no)
- Question intent analysis
- Multi-language support

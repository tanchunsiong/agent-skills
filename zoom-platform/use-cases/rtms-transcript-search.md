# Search Transcripts

Search and query RTMS transcripts for keywords and phrases.

## Overview

Implement full-text search on meeting transcripts for finding specific content.

## Skills Needed

- **zoom-rtms** - Primary

## Search Features

| Feature | Description |
|---------|-------------|
| Keyword search | Find exact matches |
| Fuzzy search | Handle typos |
| Phrase search | Multi-word queries |
| Filter by speaker | Scope to participant |

## Implementation

### JavaScript

```javascript
class TranscriptSearch {
  constructor(transcripts = []) {
    this.transcripts = transcripts;
    this.index = this.buildIndex();
  }
  
  buildIndex() {
    const index = new Map();
    
    for (let i = 0; i < this.transcripts.length; i++) {
      const transcript = this.transcripts[i];
      const words = this.tokenize(transcript.text);
      
      for (const word of words) {
        if (!index.has(word)) {
          index.set(word, []);
        }
        index.get(word).push(i);
      }
    }
    
    return index;
  }
  
  tokenize(text) {
    return text
      .toLowerCase()
      .replace(/[^\w\s]/g, '')
      .split(/\s+/)
      .filter(w => w.length > 1);
  }
  
  search(query, options = {}) {
    const { speaker, limit = 10, fuzzy = false } = options;
    const queryWords = this.tokenize(query);
    
    if (queryWords.length === 0) {
      return [];
    }
    
    // Find matching transcript indices
    let matchingIndices;
    
    if (queryWords.length === 1) {
      if (fuzzy) {
        matchingIndices = this.fuzzySearch(queryWords[0]);
      } else {
        matchingIndices = this.index.get(queryWords[0]) || [];
      }
    } else {
      // Phrase search - find transcripts with all words
      matchingIndices = this.phraseSearch(queryWords);
    }
    
    // Get matching transcripts
    let results = matchingIndices
      .map(i => ({
        ...this.transcripts[i],
        index: i,
        highlights: this.highlight(this.transcripts[i].text, queryWords)
      }));
    
    // Filter by speaker
    if (speaker) {
      results = results.filter(r => 
        r.speakerName.toLowerCase().includes(speaker.toLowerCase())
      );
    }
    
    // Sort by relevance (more matches = higher)
    results.sort((a, b) => 
      b.highlights.length - a.highlights.length
    );
    
    return results.slice(0, limit);
  }
  
  phraseSearch(words) {
    // Get indices for each word
    const wordIndices = words.map(w => 
      new Set(this.index.get(w) || [])
    );
    
    if (wordIndices.some(s => s.size === 0)) {
      return [];
    }
    
    // Find intersection
    let result = wordIndices[0];
    for (let i = 1; i < wordIndices.length; i++) {
      result = new Set([...result].filter(x => wordIndices[i].has(x)));
    }
    
    return [...result];
  }
  
  fuzzySearch(word, maxDistance = 2) {
    const matches = [];
    
    for (const [indexWord, indices] of this.index) {
      if (this.levenshtein(word, indexWord) <= maxDistance) {
        matches.push(...indices);
      }
    }
    
    return [...new Set(matches)];
  }
  
  levenshtein(a, b) {
    const matrix = [];
    
    for (let i = 0; i <= b.length; i++) {
      matrix[i] = [i];
    }
    for (let j = 0; j <= a.length; j++) {
      matrix[0][j] = j;
    }
    
    for (let i = 1; i <= b.length; i++) {
      for (let j = 1; j <= a.length; j++) {
        if (b.charAt(i - 1) === a.charAt(j - 1)) {
          matrix[i][j] = matrix[i - 1][j - 1];
        } else {
          matrix[i][j] = Math.min(
            matrix[i - 1][j - 1] + 1,
            matrix[i][j - 1] + 1,
            matrix[i - 1][j] + 1
          );
        }
      }
    }
    
    return matrix[b.length][a.length];
  }
  
  highlight(text, words) {
    const highlights = [];
    const lowerText = text.toLowerCase();
    
    for (const word of words) {
      let pos = 0;
      while ((pos = lowerText.indexOf(word, pos)) !== -1) {
        highlights.push({
          word: text.substring(pos, pos + word.length),
          start: pos,
          end: pos + word.length
        });
        pos += word.length;
      }
    }
    
    return highlights.sort((a, b) => a.start - b.start);
  }
  
  searchByTimeRange(startTime, endTime) {
    return this.transcripts.filter(t =>
      t.timestamp >= startTime && t.timestamp <= endTime
    );
  }
  
  getSpeakerTranscripts(speakerName) {
    return this.transcripts.filter(t =>
      t.speakerName.toLowerCase() === speakerName.toLowerCase()
    );
  }
}

// Usage
const search = new TranscriptSearch(receiver.transcripts);

// Basic search
const results = search.search('project deadline');
console.log('Found:', results.length, 'matches');

// Fuzzy search
const fuzzyResults = search.search('projct', { fuzzy: true });

// Search specific speaker
const speakerResults = search.search('budget', { speaker: 'John' });

// Get highlighted context
for (const result of results) {
  console.log(`[${result.speakerName}]: ${result.text}`);
  console.log('Highlights:', result.highlights);
}
```

### Python

```python
from typing import List, Dict, Set, Optional
from dataclasses import dataclass
import re

@dataclass
class SearchResult:
    transcript: dict
    index: int
    highlights: List[dict]
    score: float

class TranscriptSearch:
    def __init__(self, transcripts: List[dict]):
        self.transcripts = transcripts
        self.index = self.build_index()
    
    def build_index(self) -> Dict[str, List[int]]:
        index = {}
        
        for i, transcript in enumerate(self.transcripts):
            words = self.tokenize(transcript['text'])
            
            for word in words:
                if word not in index:
                    index[word] = []
                index[word].append(i)
        
        return index
    
    def tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return [w for w in text.split() if len(w) > 1]
    
    def search(
        self,
        query: str,
        speaker: Optional[str] = None,
        limit: int = 10,
        fuzzy: bool = False
    ) -> List[SearchResult]:
        query_words = self.tokenize(query)
        
        if not query_words:
            return []
        
        # Find matching indices
        if len(query_words) == 1:
            if fuzzy:
                matching_indices = self.fuzzy_search(query_words[0])
            else:
                matching_indices = self.index.get(query_words[0], [])
        else:
            matching_indices = self.phrase_search(query_words)
        
        # Build results
        results = []
        for i in matching_indices:
            transcript = self.transcripts[i]
            highlights = self.highlight(transcript['text'], query_words)
            
            results.append(SearchResult(
                transcript=transcript,
                index=i,
                highlights=highlights,
                score=len(highlights)
            ))
        
        # Filter by speaker
        if speaker:
            results = [r for r in results 
                      if speaker.lower() in r.transcript['speaker_name'].lower()]
        
        # Sort by score
        results.sort(key=lambda r: r.score, reverse=True)
        
        return results[:limit]
    
    def phrase_search(self, words: List[str]) -> List[int]:
        word_indices = [set(self.index.get(w, [])) for w in words]
        
        if any(len(s) == 0 for s in word_indices):
            return []
        
        result = word_indices[0]
        for indices in word_indices[1:]:
            result = result.intersection(indices)
        
        return list(result)
    
    def fuzzy_search(self, word: str, max_distance: int = 2) -> List[int]:
        matches = []
        
        for index_word, indices in self.index.items():
            if self.levenshtein(word, index_word) <= max_distance:
                matches.extend(indices)
        
        return list(set(matches))
    
    @staticmethod
    def levenshtein(a: str, b: str) -> int:
        if len(a) < len(b):
            return TranscriptSearch.levenshtein(b, a)
        
        if len(b) == 0:
            return len(a)
        
        prev_row = range(len(b) + 1)
        
        for i, c1 in enumerate(a):
            curr_row = [i + 1]
            for j, c2 in enumerate(b):
                insertions = prev_row[j + 1] + 1
                deletions = curr_row[j] + 1
                substitutions = prev_row[j] + (c1 != c2)
                curr_row.append(min(insertions, deletions, substitutions))
            prev_row = curr_row
        
        return prev_row[-1]
    
    def highlight(self, text: str, words: List[str]) -> List[dict]:
        highlights = []
        lower_text = text.lower()
        
        for word in words:
            pos = 0
            while True:
                pos = lower_text.find(word, pos)
                if pos == -1:
                    break
                highlights.append({
                    'word': text[pos:pos + len(word)],
                    'start': pos,
                    'end': pos + len(word)
                })
                pos += len(word)
        
        return sorted(highlights, key=lambda h: h['start'])

# Usage
search = TranscriptSearch(receiver.transcripts)

# Basic search
results = search.search('project deadline')
print(f"Found {len(results)} matches")

# With fuzzy matching
fuzzy_results = search.search('projct', fuzzy=True)

# Filter by speaker
speaker_results = search.search('budget', speaker='John')
```

## Resources

- **Full-text search**: https://en.wikipedia.org/wiki/Full-text_search
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

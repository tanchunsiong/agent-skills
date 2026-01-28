# Generate Word Cloud

Create word cloud visualizations from RTMS transcripts.

## Overview

Generate word clouds to visualize meeting topics and frequently discussed terms.

## Skills Needed

- **zoom-rtms** - Primary

## Word Cloud Features

| Feature | Description |
|---------|-------------|
| Frequency-based sizing | Larger = more frequent |
| Stop word filtering | Remove common words |
| Speaker-specific | Per-participant clouds |
| Time-based | Track topic changes |

## Implementation

### JavaScript

```javascript
class WordCloudGenerator {
  constructor(options = {}) {
    this.stopWords = new Set(options.stopWords || [
      'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were',
      'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
      'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall',
      'can', 'need', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by',
      'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
      'above', 'below', 'between', 'under', 'again', 'further', 'then',
      'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'each',
      'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
      'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just', 'also',
      'now', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which',
      'who', 'this', 'that', 'these', 'those', 'am', 'as', 'if', 'because',
      'until', 'while', 'let', 'me', 'my', 'your', 'our', 'their', 'its',
      'him', 'her', 'them', 'us', 'yeah', 'okay', 'um', 'uh', 'like', 'know'
    ]);
    
    this.minWordLength = options.minWordLength || 3;
    this.maxWords = options.maxWords || 100;
  }
  
  generate(transcripts) {
    const wordCounts = new Map();
    
    for (const t of transcripts) {
      const words = this.tokenize(t.text);
      
      for (const word of words) {
        if (this.isValidWord(word)) {
          wordCounts.set(word, (wordCounts.get(word) || 0) + 1);
        }
      }
    }
    
    // Sort by frequency and limit
    const sorted = [...wordCounts.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, this.maxWords);
    
    // Normalize sizes
    const maxCount = sorted[0]?.[1] || 1;
    
    return sorted.map(([word, count]) => ({
      text: word,
      count: count,
      size: Math.round((count / maxCount) * 100),
      weight: count / maxCount
    }));
  }
  
  generateBySpeaker(transcripts) {
    const speakerWords = new Map();
    
    for (const t of transcripts) {
      if (!speakerWords.has(t.speakerId)) {
        speakerWords.set(t.speakerId, {
          name: t.speakerName,
          words: new Map()
        });
      }
      
      const speaker = speakerWords.get(t.speakerId);
      const words = this.tokenize(t.text);
      
      for (const word of words) {
        if (this.isValidWord(word)) {
          speaker.words.set(word, (speaker.words.get(word) || 0) + 1);
        }
      }
    }
    
    const result = {};
    for (const [id, data] of speakerWords) {
      result[id] = {
        name: data.name,
        cloud: this.normalizeCloud(data.words)
      };
    }
    
    return result;
  }
  
  generateByTimeWindow(transcripts, windowMs = 300000) {
    const windows = [];
    let currentWindow = { start: 0, words: new Map() };
    const startTime = transcripts[0]?.timestamp || 0;
    
    for (const t of transcripts) {
      const relativeTime = t.timestamp - startTime;
      const windowIndex = Math.floor(relativeTime / windowMs);
      
      if (windowIndex !== currentWindow.index) {
        if (currentWindow.words.size > 0) {
          windows.push({
            index: currentWindow.index,
            start: currentWindow.index * windowMs,
            cloud: this.normalizeCloud(currentWindow.words)
          });
        }
        currentWindow = { index: windowIndex, words: new Map() };
      }
      
      const words = this.tokenize(t.text);
      for (const word of words) {
        if (this.isValidWord(word)) {
          currentWindow.words.set(word, (currentWindow.words.get(word) || 0) + 1);
        }
      }
    }
    
    // Add last window
    if (currentWindow.words.size > 0) {
      windows.push({
        index: currentWindow.index,
        start: currentWindow.index * windowMs,
        cloud: this.normalizeCloud(currentWindow.words)
      });
    }
    
    return windows;
  }
  
  normalizeCloud(wordMap) {
    const sorted = [...wordMap.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, this.maxWords);
    
    const maxCount = sorted[0]?.[1] || 1;
    
    return sorted.map(([word, count]) => ({
      text: word,
      count: count,
      size: Math.round((count / maxCount) * 100)
    }));
  }
  
  tokenize(text) {
    return text
      .toLowerCase()
      .replace(/[^\w\s]/g, '')
      .split(/\s+/);
  }
  
  isValidWord(word) {
    return word.length >= this.minWordLength && !this.stopWords.has(word);
  }
  
  // Generate HTML/SVG visualization
  toSVG(cloud, width = 800, height = 400) {
    // Simple spiral placement
    const placed = [];
    let angle = 0;
    let radius = 0;
    const centerX = width / 2;
    const centerY = height / 2;
    
    const svg = [`<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">`];
    
    for (const word of cloud) {
      const fontSize = 12 + word.size * 0.4;
      const x = centerX + radius * Math.cos(angle);
      const y = centerY + radius * Math.sin(angle);
      
      svg.push(`<text x="${x}" y="${y}" font-size="${fontSize}" fill="hsl(${word.count * 20 % 360}, 70%, 50%)" text-anchor="middle">${word.text}</text>`);
      
      angle += 0.5;
      radius += 2;
    }
    
    svg.push('</svg>');
    return svg.join('\n');
  }
}

// Usage
const generator = new WordCloudGenerator({ maxWords: 50 });

// Generate overall cloud
const cloud = generator.generate(receiver.transcripts);
console.log('Top words:', cloud.slice(0, 10));

// Per-speaker clouds
const speakerClouds = generator.generateBySpeaker(receiver.transcripts);

// Time-based analysis (5 minute windows)
const timeClouds = generator.generateByTimeWindow(receiver.transcripts, 300000);

// Export as SVG
const svg = generator.toSVG(cloud);
fs.writeFileSync('wordcloud.svg', svg);
```

### Python

```python
from collections import Counter
from typing import List, Dict, Set
import math

class WordCloudGenerator:
    def __init__(self, stop_words: Set[str] = None, min_word_length: int = 3, max_words: int = 100):
        self.stop_words = stop_words or {
            'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were',
            'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'to', 'of', 'in', 'for', 'on',
            'with', 'at', 'by', 'from', 'i', 'you', 'he', 'she', 'it', 'we',
            'they', 'this', 'that', 'what', 'which', 'who', 'yeah', 'okay',
            'um', 'uh', 'like', 'know', 'just', 'so', 'really', 'think'
        }
        self.min_word_length = min_word_length
        self.max_words = max_words
    
    def generate(self, transcripts: List[dict]) -> List[dict]:
        word_counts = Counter()
        
        for t in transcripts:
            words = self.tokenize(t['text'])
            word_counts.update(w for w in words if self.is_valid(w))
        
        return self.normalize_cloud(word_counts)
    
    def generate_by_speaker(self, transcripts: List[dict]) -> Dict:
        speaker_words = {}
        
        for t in transcripts:
            speaker_id = t['speaker_id']
            if speaker_id not in speaker_words:
                speaker_words[speaker_id] = {
                    'name': t['speaker_name'],
                    'words': Counter()
                }
            
            words = self.tokenize(t['text'])
            speaker_words[speaker_id]['words'].update(
                w for w in words if self.is_valid(w)
            )
        
        return {
            sid: {
                'name': data['name'],
                'cloud': self.normalize_cloud(data['words'])
            }
            for sid, data in speaker_words.items()
        }
    
    def normalize_cloud(self, word_counts: Counter) -> List[dict]:
        most_common = word_counts.most_common(self.max_words)
        if not most_common:
            return []
        
        max_count = most_common[0][1]
        
        return [
            {
                'text': word,
                'count': count,
                'size': round((count / max_count) * 100)
            }
            for word, count in most_common
        ]
    
    def tokenize(self, text: str) -> List[str]:
        import re
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text.split()
    
    def is_valid(self, word: str) -> bool:
        return len(word) >= self.min_word_length and word not in self.stop_words

# Usage with wordcloud library
try:
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    
    def generate_image(transcripts, output_path='wordcloud.png'):
        generator = WordCloudGenerator()
        cloud = generator.generate(transcripts)
        
        # Convert to frequency dict
        freq = {w['text']: w['count'] for w in cloud}
        
        # Generate image
        wc = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='viridis'
        ).generate_from_frequencies(freq)
        
        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return output_path

except ImportError:
    pass

# Basic usage
generator = WordCloudGenerator()
cloud = generator.generate(receiver.transcripts)
print("Top words:", cloud[:10])
```

## Resources

- **wordcloud Python**: https://github.com/amueller/word_cloud
- **d3-cloud**: https://github.com/jasondavies/d3-cloud
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

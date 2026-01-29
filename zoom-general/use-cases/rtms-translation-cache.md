# Translation Caching

Cache translations to reduce API costs and latency.

## Overview

Implement caching for repeated phrases and common expressions.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

```javascript
const crypto = require('crypto');

class TranslationCache {
  constructor(options = {}) {
    this.cache = new Map();
    this.maxSize = options.maxSize || 10000;
    this.ttl = options.ttl || 3600000; // 1 hour
    this.stats = { hits: 0, misses: 0 };
  }
  
  getKey(text, targetLang, sourceLang = 'auto') {
    const hash = crypto.createHash('md5')
      .update(`${sourceLang}:${targetLang}:${text}`)
      .digest('hex');
    return hash;
  }
  
  get(text, targetLang, sourceLang = 'auto') {
    const key = this.getKey(text, targetLang, sourceLang);
    const entry = this.cache.get(key);
    
    if (entry && Date.now() - entry.timestamp < this.ttl) {
      this.stats.hits++;
      return entry.translation;
    }
    
    if (entry) {
      this.cache.delete(key); // Expired
    }
    
    this.stats.misses++;
    return null;
  }
  
  set(text, targetLang, translation, sourceLang = 'auto') {
    // Evict oldest if at capacity
    if (this.cache.size >= this.maxSize) {
      const oldest = this.cache.keys().next().value;
      this.cache.delete(oldest);
    }
    
    const key = this.getKey(text, targetLang, sourceLang);
    this.cache.set(key, {
      translation,
      timestamp: Date.now()
    });
  }
  
  getStats() {
    const total = this.stats.hits + this.stats.misses;
    return {
      hits: this.stats.hits,
      misses: this.stats.misses,
      hitRate: total > 0 ? (this.stats.hits / total) * 100 : 0,
      size: this.cache.size
    };
  }
  
  clear() {
    this.cache.clear();
    this.stats = { hits: 0, misses: 0 };
  }
}

class CachedTranslator {
  constructor(translator, cacheOptions = {}) {
    this.translator = translator;
    this.cache = new TranslationCache(cacheOptions);
  }
  
  async translate(text, targetLang, sourceLang = 'auto') {
    // Check cache first
    const cached = this.cache.get(text, targetLang, sourceLang);
    if (cached) {
      return cached;
    }
    
    // Call API
    const translation = await this.translator.translate(text, targetLang, sourceLang);
    
    // Cache result
    this.cache.set(text, targetLang, translation, sourceLang);
    
    return translation;
  }
  
  async translateToMultiple(text, targetLangs) {
    const results = {};
    const uncached = [];
    
    // Check cache for each language
    for (const lang of targetLangs) {
      const cached = this.cache.get(text, lang);
      if (cached) {
        results[lang] = cached;
      } else {
        uncached.push(lang);
      }
    }
    
    // Fetch uncached translations
    if (uncached.length > 0) {
      const translations = await this.translator.translateToMultiple(text, uncached);
      
      for (const [lang, translation] of Object.entries(translations)) {
        this.cache.set(text, lang, translation);
        results[lang] = translation;
      }
    }
    
    return results;
  }
  
  getStats() {
    return this.cache.getStats();
  }
}

// Usage
const cachedTranslator = new CachedTranslator(
  new GoogleTranslator('project-id'),
  { maxSize: 5000, ttl: 7200000 }
);

receiver.onTranscript = async (segment) => {
  const translations = await cachedTranslator.translateToMultiple(
    segment.text,
    ['es', 'fr', 'de']
  );
  
  displayTranslations(translations);
};

// Monitor cache performance
setInterval(() => {
  console.log('Cache stats:', cachedTranslator.getStats());
}, 60000);
```

### Python

```python
import hashlib
import time
from typing import Dict, Optional
from collections import OrderedDict

class TranslationCache:
    def __init__(self, max_size: int = 10000, ttl: int = 3600):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.ttl = ttl
        self.hits = 0
        self.misses = 0
    
    def _get_key(self, text: str, target_lang: str, source_lang: str = 'auto') -> str:
        content = f"{source_lang}:{target_lang}:{text}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, text: str, target_lang: str, source_lang: str = 'auto') -> Optional[str]:
        key = self._get_key(text, target_lang, source_lang)
        entry = self.cache.get(key)
        
        if entry and time.time() - entry['timestamp'] < self.ttl:
            self.hits += 1
            self.cache.move_to_end(key)  # LRU
            return entry['translation']
        
        if entry:
            del self.cache[key]
        
        self.misses += 1
        return None
    
    def set(self, text: str, target_lang: str, translation: str, source_lang: str = 'auto'):
        if len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)  # Remove oldest
        
        key = self._get_key(text, target_lang, source_lang)
        self.cache[key] = {
            'translation': translation,
            'timestamp': time.time()
        }
    
    def get_stats(self) -> Dict:
        total = self.hits + self.misses
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': (self.hits / total * 100) if total > 0 else 0,
            'size': len(self.cache)
        }

class CachedTranslator:
    def __init__(self, translator, max_size=10000, ttl=3600):
        self.translator = translator
        self.cache = TranslationCache(max_size, ttl)
    
    async def translate(self, text: str, target_lang: str) -> str:
        cached = self.cache.get(text, target_lang)
        if cached:
            return cached
        
        translation = await self.translator.translate(text, target_lang)
        self.cache.set(text, target_lang, translation)
        return translation

# Usage
cached_translator = CachedTranslator(GoogleTranslator('project-id'))
```

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/

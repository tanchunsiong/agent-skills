# Streaming Translation

Implement low-latency streaming translation for real-time captions.

## Overview

Translate incrementally as speech is transcribed for minimal caption delay.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

```javascript
class StreamingTranslator {
  constructor(translator, options = {}) {
    this.translator = translator;
    this.bufferTime = options.bufferTime || 500; // ms
    this.minChunkSize = options.minChunkSize || 5; // words
    
    this.buffer = '';
    this.timer = null;
    this.partialTranslation = '';
    
    this.onPartialTranslation = options.onPartialTranslation;
    this.onFinalTranslation = options.onFinalTranslation;
  }
  
  async processPartial(text, targetLang) {
    this.buffer = text;
    
    // Quick partial translation for responsiveness
    const words = text.split(/\s+/);
    
    if (words.length >= this.minChunkSize) {
      // Translate what we have so far
      const partial = await this.translator.translate(text, targetLang);
      this.partialTranslation = partial;
      this.onPartialTranslation?.(partial);
    }
    
    // Debounce for smoother updates
    if (this.timer) {
      clearTimeout(this.timer);
    }
    
    this.timer = setTimeout(async () => {
      if (this.buffer) {
        const updated = await this.translator.translate(this.buffer, targetLang);
        this.partialTranslation = updated;
        this.onPartialTranslation?.(updated);
      }
    }, this.bufferTime);
  }
  
  async processFinal(text, targetLang) {
    // Clear any pending updates
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }
    
    this.buffer = '';
    
    // Final, high-quality translation
    const translation = await this.translator.translate(text, targetLang);
    this.onFinalTranslation?.(translation);
    this.partialTranslation = '';
    
    return translation;
  }
}

class IncrementalTranslator {
  constructor(translator) {
    this.translator = translator;
    this.cache = new Map();
    this.lastTranslated = '';
  }
  
  async translateIncremental(text, targetLang) {
    // Find what's new
    const newPart = text.slice(this.lastTranslated.length).trim();
    
    if (!newPart) {
      return this.cache.get(this.lastTranslated) || '';
    }
    
    // Translate only the new part
    const newTranslation = await this.translator.translate(newPart, targetLang);
    
    // Combine with previous
    const previousTranslation = this.cache.get(this.lastTranslated) || '';
    const fullTranslation = previousTranslation + ' ' + newTranslation;
    
    // Cache
    this.cache.set(text, fullTranslation.trim());
    this.lastTranslated = text;
    
    return fullTranslation.trim();
  }
  
  reset() {
    this.cache.clear();
    this.lastTranslated = '';
  }
}

// Multi-language streaming
class MultiLangStreamingTranslator {
  constructor(translator, targetLangs) {
    this.translator = translator;
    this.targetLangs = targetLangs;
    this.streamers = new Map();
    
    for (const lang of targetLangs) {
      this.streamers.set(lang, new StreamingTranslator(translator, {
        onPartialTranslation: (text) => this.onPartial?.(lang, text),
        onFinalTranslation: (text) => this.onFinal?.(lang, text)
      }));
    }
    
    this.onPartial = null;
    this.onFinal = null;
  }
  
  async processPartial(text) {
    await Promise.all(
      this.targetLangs.map(lang => 
        this.streamers.get(lang).processPartial(text, lang)
      )
    );
  }
  
  async processFinal(text) {
    await Promise.all(
      this.targetLangs.map(lang => 
        this.streamers.get(lang).processFinal(text, lang)
      )
    );
  }
}

// Usage
const streamingTranslator = new MultiLangStreamingTranslator(
  new GoogleTranslator('project-id'),
  ['es', 'fr', 'de']
);

streamingTranslator.onPartial = (lang, text) => {
  updatePartialCaption(lang, text);
};

streamingTranslator.onFinal = (lang, text) => {
  displayFinalCaption(lang, text);
};

receiver.onTranscript = async (segment) => {
  if (segment.isFinal) {
    await streamingTranslator.processFinal(segment.text);
  } else {
    await streamingTranslator.processPartial(segment.text);
  }
};
```

### Python

```python
import asyncio
from typing import Callable, Optional, Dict

class StreamingTranslator:
    def __init__(
        self,
        translator,
        buffer_time: float = 0.5,
        min_chunk_size: int = 5
    ):
        self.translator = translator
        self.buffer_time = buffer_time
        self.min_chunk_size = min_chunk_size
        
        self.buffer = ''
        self.task: Optional[asyncio.Task] = None
        self.partial_translation = ''
        
        self.on_partial: Optional[Callable] = None
        self.on_final: Optional[Callable] = None
    
    async def process_partial(self, text: str, target_lang: str):
        self.buffer = text
        
        words = text.split()
        if len(words) >= self.min_chunk_size:
            partial = await self.translator.translate(text, target_lang)
            self.partial_translation = partial
            if self.on_partial:
                await self.on_partial(partial)
        
        # Cancel pending update
        if self.task:
            self.task.cancel()
        
        # Schedule debounced update
        async def delayed_update():
            await asyncio.sleep(self.buffer_time)
            if self.buffer:
                updated = await self.translator.translate(self.buffer, target_lang)
                self.partial_translation = updated
                if self.on_partial:
                    await self.on_partial(updated)
        
        self.task = asyncio.create_task(delayed_update())
    
    async def process_final(self, text: str, target_lang: str) -> str:
        if self.task:
            self.task.cancel()
            self.task = None
        
        self.buffer = ''
        translation = await self.translator.translate(text, target_lang)
        
        if self.on_final:
            await self.on_final(translation)
        
        self.partial_translation = ''
        return translation

# Usage
streaming = StreamingTranslator(GoogleTranslator('project-id'))

async def on_partial(text):
    update_caption(text)

streaming.on_partial = on_partial

async def on_transcript(segment):
    if segment['is_final']:
        await streaming.process_final(segment['text'], 'es')
    else:
        await streaming.process_partial(segment['text'], 'es')
```

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/

# Multilingual Captions Display

Display captions in multiple languages simultaneously.

## Overview

Show real-time captions in multiple languages for diverse meeting participants.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

```javascript
class MultilingualCaptionDisplay {
  constructor(container, options = {}) {
    this.container = container;
    this.languages = options.languages || ['en', 'es', 'fr'];
    this.translator = options.translator;
    this.displays = new Map();
    
    this.setupUI();
  }
  
  setupUI() {
    this.container.innerHTML = '';
    this.container.className = 'multilingual-captions';
    
    for (const lang of this.languages) {
      const langDiv = document.createElement('div');
      langDiv.className = 'language-track';
      langDiv.dataset.lang = lang;
      
      const label = document.createElement('div');
      label.className = 'language-label';
      label.textContent = this.getLanguageName(lang);
      
      const caption = document.createElement('div');
      caption.className = 'caption-text';
      
      langDiv.appendChild(label);
      langDiv.appendChild(caption);
      this.container.appendChild(langDiv);
      
      this.displays.set(lang, caption);
    }
  }
  
  async displayCaption(speaker, text, sourceLang = 'en') {
    // Display original
    if (this.displays.has(sourceLang)) {
      this.displays.get(sourceLang).textContent = `${speaker}: ${text}`;
    }
    
    // Translate to other languages
    const targetLangs = this.languages.filter(l => l !== sourceLang);
    
    if (this.translator && targetLangs.length > 0) {
      const translations = await this.translator.translateToMultiple(text, targetLangs);
      
      for (const [lang, translatedText] of Object.entries(translations)) {
        if (this.displays.has(lang)) {
          this.displays.get(lang).textContent = `${speaker}: ${translatedText}`;
        }
      }
    }
  }
  
  getLanguageName(code) {
    const names = {
      en: 'English',
      es: 'Español',
      fr: 'Français',
      de: 'Deutsch',
      ja: '日本語',
      zh: '中文',
      ko: '한국어',
      pt: 'Português'
    };
    return names[code] || code.toUpperCase();
  }
  
  setActiveLanguage(lang) {
    for (const [code, display] of this.displays) {
      display.parentElement.classList.toggle('active', code === lang);
    }
  }
}

// CSS
const style = `
.multilingual-captions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 8px;
}

.language-track {
  display: flex;
  align-items: center;
  gap: 12px;
  opacity: 0.7;
  transition: opacity 0.3s;
}

.language-track.active {
  opacity: 1;
}

.language-label {
  min-width: 80px;
  color: #888;
  font-size: 12px;
}

.caption-text {
  color: white;
  font-size: 16px;
  flex: 1;
}
`;

// Usage
const display = new MultilingualCaptionDisplay(
  document.getElementById('captions'),
  {
    languages: ['en', 'es', 'fr', 'de'],
    translator: new GoogleTranslator('project-id')
  }
);

receiver.onTranscript = async (segment) => {
  if (segment.isFinal) {
    await display.displayCaption(segment.speakerName, segment.text);
  }
};
```

### Python (Backend)

```python
from typing import Dict, List
import asyncio

class MultilingualProcessor:
    def __init__(self, translator, languages: List[str]):
        self.translator = translator
        self.languages = languages
    
    async def process_transcript(self, text: str, source_lang: str = 'en') -> Dict[str, str]:
        target_langs = [l for l in self.languages if l != source_lang]
        
        result = {source_lang: text}
        
        if target_langs:
            translations = await self.translator.translate_to_multiple(text, target_langs)
            result.update(translations)
        
        return result
    
    async def broadcast(self, speaker: str, translations: Dict[str, str], websockets: Dict):
        for lang, ws_list in websockets.items():
            if lang in translations:
                message = {
                    'speaker': speaker,
                    'text': translations[lang],
                    'language': lang
                }
                for ws in ws_list:
                    await ws.send_json(message)

# Usage
processor = MultilingualProcessor(
    translator=GoogleTranslator('project-id'),
    languages=['en', 'es', 'fr', 'de']
)

async def on_transcript(segment):
    translations = await processor.process_transcript(segment['text'])
    await processor.broadcast(segment['speaker_name'], translations, connected_clients)
```

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/

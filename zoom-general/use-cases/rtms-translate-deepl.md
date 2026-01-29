# Translate with DeepL

High-quality translation using DeepL API for RTMS transcripts.

## Overview

DeepL provides superior translation quality for European languages.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

```javascript
const axios = require('axios');

class DeepLTranslator {
  constructor(authKey) {
    this.authKey = authKey;
    this.baseUrl = authKey.endsWith(':fx')
      ? 'https://api-free.deepl.com/v2'
      : 'https://api.deepl.com/v2';
  }
  
  async translate(text, targetLang, sourceLang = null) {
    const params = {
      auth_key: this.authKey,
      text: text,
      target_lang: targetLang.toUpperCase()
    };
    
    if (sourceLang) {
      params.source_lang = sourceLang.toUpperCase();
    }
    
    const response = await axios.post(
      `${this.baseUrl}/translate`,
      new URLSearchParams(params)
    );
    
    return {
      text: response.data.translations[0].text,
      detectedSourceLang: response.data.translations[0].detected_source_language
    };
  }
  
  async translateBatch(texts, targetLang) {
    const params = new URLSearchParams();
    params.append('auth_key', this.authKey);
    params.append('target_lang', targetLang.toUpperCase());
    
    for (const text of texts) {
      params.append('text', text);
    }
    
    const response = await axios.post(`${this.baseUrl}/translate`, params);
    
    return response.data.translations.map(t => t.text);
  }
  
  async getUsage() {
    const response = await axios.get(`${this.baseUrl}/usage`, {
      params: { auth_key: this.authKey }
    });
    
    return {
      characterCount: response.data.character_count,
      characterLimit: response.data.character_limit
    };
  }
}

// Usage
const translator = new DeepLTranslator(process.env.DEEPL_AUTH_KEY);

receiver.onTranscript = async (segment) => {
  if (segment.isFinal) {
    // DeepL excels at European languages
    const german = await translator.translate(segment.text, 'DE');
    const french = await translator.translate(segment.text, 'FR');
    
    displayTranslation('de', german.text);
    displayTranslation('fr', french.text);
  }
};
```

### Python

```python
import deepl

class DeepLTranslator:
    def __init__(self, auth_key: str):
        self.translator = deepl.Translator(auth_key)
    
    def translate(self, text: str, target_lang: str, source_lang: str = None):
        result = self.translator.translate_text(
            text,
            target_lang=target_lang.upper(),
            source_lang=source_lang.upper() if source_lang else None
        )
        
        return {
            'text': result.text,
            'detected_source_lang': result.detected_source_lang
        }
    
    def translate_batch(self, texts: list, target_lang: str):
        results = self.translator.translate_text(texts, target_lang=target_lang.upper())
        return [r.text for r in results]
    
    def get_usage(self):
        usage = self.translator.get_usage()
        return {
            'character_count': usage.character.count,
            'character_limit': usage.character.limit
        }

# Usage
translator = DeepLTranslator(os.environ['DEEPL_AUTH_KEY'])

def on_transcript(segment):
    if segment['is_final']:
        result = translator.translate(segment['text'], 'DE')
        print(f"German: {result['text']}")
```

## Supported Languages

| Code | Language |
|------|----------|
| DE | German |
| FR | French |
| ES | Spanish |
| IT | Italian |
| NL | Dutch |
| PL | Polish |
| PT | Portuguese |
| JA | Japanese |
| ZH | Chinese |

## Resources

- **DeepL API**: https://www.deepl.com/docs-api
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

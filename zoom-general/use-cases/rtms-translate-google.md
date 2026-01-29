# Translate with Google Translate

Real-time translation of RTMS transcripts using Google Cloud Translation API.

## Overview

Translate meeting transcripts to multiple languages in real-time for multilingual meetings.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

```javascript
const { TranslationServiceClient } = require('@google-cloud/translate').v3;

class GoogleTranslator {
  constructor(projectId) {
    this.client = new TranslationServiceClient();
    this.projectId = projectId;
    this.location = 'global';
    this.parent = `projects/${projectId}/locations/${this.location}`;
  }
  
  async translate(text, targetLanguage, sourceLanguage = 'en') {
    const [response] = await this.client.translateText({
      parent: this.parent,
      contents: [text],
      mimeType: 'text/plain',
      sourceLanguageCode: sourceLanguage,
      targetLanguageCode: targetLanguage
    });
    
    return response.translations[0].translatedText;
  }
  
  async translateBatch(texts, targetLanguage) {
    const [response] = await this.client.translateText({
      parent: this.parent,
      contents: texts,
      mimeType: 'text/plain',
      targetLanguageCode: targetLanguage
    });
    
    return response.translations.map(t => t.translatedText);
  }
  
  async translateToMultiple(text, targetLanguages) {
    const results = {};
    
    await Promise.all(targetLanguages.map(async (lang) => {
      results[lang] = await this.translate(text, lang);
    }));
    
    return results;
  }
}

// Real-time translation with RTMS
const translator = new GoogleTranslator('your-project-id');
const targetLanguages = ['es', 'fr', 'de', 'ja', 'zh'];

receiver.onTranscript = async (segment) => {
  if (segment.isFinal) {
    const translations = await translator.translateToMultiple(
      segment.text,
      targetLanguages
    );
    
    console.log(`Original: ${segment.text}`);
    for (const [lang, text] of Object.entries(translations)) {
      console.log(`${lang}: ${text}`);
    }
  }
};
```

### Python

```python
from google.cloud import translate_v3 as translate
from typing import List, Dict
import asyncio

class GoogleTranslator:
    def __init__(self, project_id: str):
        self.client = translate.TranslationServiceClient()
        self.parent = f"projects/{project_id}/locations/global"
    
    def translate(self, text: str, target_language: str, source_language: str = 'en') -> str:
        response = self.client.translate_text(
            request={
                'parent': self.parent,
                'contents': [text],
                'mime_type': 'text/plain',
                'source_language_code': source_language,
                'target_language_code': target_language
            }
        )
        return response.translations[0].translated_text
    
    async def translate_to_multiple(self, text: str, target_languages: List[str]) -> Dict[str, str]:
        loop = asyncio.get_event_loop()
        
        async def translate_one(lang):
            return lang, await loop.run_in_executor(
                None, lambda: self.translate(text, lang)
            )
        
        results = await asyncio.gather(*[translate_one(lang) for lang in target_languages])
        return dict(results)

# Usage
translator = GoogleTranslator('your-project-id')

async def on_transcript(segment):
    if segment['is_final']:
        translations = await translator.translate_to_multiple(
            segment['text'],
            ['es', 'fr', 'de', 'ja']
        )
        print(f"Original: {segment['text']}")
        for lang, text in translations.items():
            print(f"{lang}: {text}")
```

## Supported Languages

| Code | Language |
|------|----------|
| es | Spanish |
| fr | French |
| de | German |
| ja | Japanese |
| zh | Chinese |
| ko | Korean |
| pt | Portuguese |
| ar | Arabic |

## Resources

- **Google Cloud Translation**: https://cloud.google.com/translate
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

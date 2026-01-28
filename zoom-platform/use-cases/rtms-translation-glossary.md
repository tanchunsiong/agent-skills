# Translation Glossary

Use custom glossaries for domain-specific translation accuracy.

## Overview

Define custom terminology for accurate translation of technical or business terms.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

```javascript
class TranslationGlossary {
  constructor() {
    this.terms = new Map(); // term -> { translations: {lang: translation} }
  }
  
  addTerm(term, translations) {
    this.terms.set(term.toLowerCase(), {
      original: term,
      translations: translations
    });
  }
  
  addTerms(termList) {
    for (const { term, translations } of termList) {
      this.addTerm(term, translations);
    }
  }
  
  getTranslation(term, targetLang) {
    const entry = this.terms.get(term.toLowerCase());
    return entry?.translations[targetLang];
  }
  
  applyToText(text, targetLang) {
    let result = text;
    const replacements = [];
    
    for (const [key, entry] of this.terms) {
      const translation = entry.translations[targetLang];
      if (translation) {
        const regex = new RegExp(`\\b${entry.original}\\b`, 'gi');
        const matches = text.match(regex);
        
        if (matches) {
          replacements.push({
            original: matches[0],
            translation: translation
          });
        }
      }
    }
    
    return { text, replacements };
  }
  
  preProcess(text) {
    // Replace glossary terms with placeholders
    let processed = text;
    const placeholders = [];
    let index = 0;
    
    for (const [key, entry] of this.terms) {
      const regex = new RegExp(`\\b${entry.original}\\b`, 'gi');
      processed = processed.replace(regex, (match) => {
        const placeholder = `__GLOSS_${index}__`;
        placeholders.push({ placeholder, original: match });
        index++;
        return placeholder;
      });
    }
    
    return { processed, placeholders };
  }
  
  postProcess(translatedText, placeholders, targetLang) {
    let result = translatedText;
    
    for (const { placeholder, original } of placeholders) {
      const translation = this.getTranslation(original, targetLang) || original;
      result = result.replace(placeholder, translation);
    }
    
    return result;
  }
  
  toJSON() {
    const obj = {};
    for (const [key, entry] of this.terms) {
      obj[entry.original] = entry.translations;
    }
    return obj;
  }
  
  fromJSON(json) {
    for (const [term, translations] of Object.entries(json)) {
      this.addTerm(term, translations);
    }
  }
}

class GlossaryAwareTranslator {
  constructor(translator, glossary) {
    this.translator = translator;
    this.glossary = glossary;
  }
  
  async translate(text, targetLang, sourceLang = 'en') {
    // Pre-process: protect glossary terms
    const { processed, placeholders } = this.glossary.preProcess(text);
    
    // Translate
    const translated = await this.translator.translate(processed, targetLang, sourceLang);
    
    // Post-process: restore with correct translations
    return this.glossary.postProcess(translated, placeholders, targetLang);
  }
}

// Example glossary for tech company
const glossary = new TranslationGlossary();
glossary.addTerms([
  {
    term: 'API',
    translations: { es: 'API', fr: 'API', de: 'API', ja: 'API' }
  },
  {
    term: 'Zoom Rooms',
    translations: { es: 'Zoom Rooms', fr: 'Zoom Rooms', de: 'Zoom Rooms' }
  },
  {
    term: 'breakout room',
    translations: { es: 'sala de grupos', fr: 'salle de répartition', de: 'Breakout-Raum' }
  },
  {
    term: 'webinar',
    translations: { es: 'seminario web', fr: 'webinaire', de: 'Webinar' }
  }
]);

const translator = new GlossaryAwareTranslator(
  new GoogleTranslator('project-id'),
  glossary
);

// Usage
const translated = await translator.translate(
  'The API for Zoom Rooms supports breakout rooms.',
  'es'
);
// Result: "La API para Zoom Rooms admite salas de grupos."
```

### Python

```python
import re
from typing import Dict, List, Tuple

class TranslationGlossary:
    def __init__(self):
        self.terms: Dict[str, Dict] = {}
    
    def add_term(self, term: str, translations: Dict[str, str]):
        self.terms[term.lower()] = {
            'original': term,
            'translations': translations
        }
    
    def get_translation(self, term: str, target_lang: str) -> str:
        entry = self.terms.get(term.lower())
        return entry['translations'].get(target_lang) if entry else None
    
    def pre_process(self, text: str) -> Tuple[str, List[Dict]]:
        processed = text
        placeholders = []
        index = 0
        
        for key, entry in self.terms.items():
            pattern = rf'\b{re.escape(entry["original"])}\b'
            
            def replacer(match):
                nonlocal index
                placeholder = f'__GLOSS_{index}__'
                placeholders.append({
                    'placeholder': placeholder,
                    'original': match.group()
                })
                index += 1
                return placeholder
            
            processed = re.sub(pattern, replacer, processed, flags=re.IGNORECASE)
        
        return processed, placeholders
    
    def post_process(self, translated: str, placeholders: List[Dict], target_lang: str) -> str:
        result = translated
        
        for item in placeholders:
            translation = self.get_translation(item['original'], target_lang) or item['original']
            result = result.replace(item['placeholder'], translation)
        
        return result

class GlossaryAwareTranslator:
    def __init__(self, translator, glossary: TranslationGlossary):
        self.translator = translator
        self.glossary = glossary
    
    async def translate(self, text: str, target_lang: str) -> str:
        processed, placeholders = self.glossary.pre_process(text)
        translated = await self.translator.translate(processed, target_lang)
        return self.glossary.post_process(translated, placeholders, target_lang)
```

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/

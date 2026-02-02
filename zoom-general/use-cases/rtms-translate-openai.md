# Translate with OpenAI

Use GPT-4 for context-aware translation of RTMS transcripts.

## Overview

Leverage LLMs for nuanced, context-aware translation that understands meeting context.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

```javascript
const OpenAI = require('openai');

class OpenAITranslator {
  constructor(apiKey) {
    this.openai = new OpenAI({ apiKey });
    this.context = [];
    this.maxContext = 10;
  }
  
  async translate(text, targetLang, options = {}) {
    const languageNames = {
      es: 'Spanish', fr: 'French', de: 'German',
      ja: 'Japanese', zh: 'Chinese', ko: 'Korean'
    };
    
    const targetName = languageNames[targetLang] || targetLang;
    
    const messages = [
      {
        role: 'system',
        content: `You are a professional translator. Translate the following text to ${targetName}. 
                  Maintain the speaker's tone and intent. Only output the translation, nothing else.
                  ${options.context ? `Context: This is from a business meeting about ${options.context}.` : ''}`
      }
    ];
    
    // Add recent context for consistency
    if (this.context.length > 0 && options.useContext !== false) {
      messages.push({
        role: 'user',
        content: `Previous translations for context:\n${this.context.slice(-3).map(c => 
          `Original: ${c.original}\n${targetName}: ${c.translation}`
        ).join('\n\n')}`
      });
      messages.push({
        role: 'assistant',
        content: 'I understand the context. I will maintain consistency with previous translations.'
      });
    }
    
    messages.push({
      role: 'user',
      content: text
    });
    
    const response = await this.openai.chat.completions.create({
      model: 'gpt-4',
      messages,
      temperature: 0.3,
      max_tokens: 1000
    });
    
    const translation = response.choices[0].message.content.trim();
    
    // Store for context
    this.context.push({ original: text, translation, lang: targetLang });
    if (this.context.length > this.maxContext) {
      this.context.shift();
    }
    
    return translation;
  }
  
  async translateWithExplanation(text, targetLang) {
    const response = await this.openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        {
          role: 'system',
          content: `Translate to ${targetLang}. Provide the translation and brief notes on any cultural adaptations made.`
        },
        { role: 'user', content: text }
      ],
      temperature: 0.3
    });
    
    return response.choices[0].message.content;
  }
  
  async translateToMultiple(text, targetLangs) {
    const results = {};
    
    // Parallel translation
    await Promise.all(targetLangs.map(async (lang) => {
      results[lang] = await this.translate(text, lang, { useContext: false });
    }));
    
    return results;
  }
  
  clearContext() {
    this.context = [];
  }
}

// Usage with meeting context
const translator = new OpenAITranslator(process.env.OPENAI_API_KEY);

let meetingContext = 'quarterly financial review';

receiver.onTranscript = async (segment) => {
  if (segment.isFinal) {
    const spanish = await translator.translate(
      segment.text,
      'es',
      { context: meetingContext }
    );
    
    displayCaption('es', spanish);
  }
};
```

### Python

```python
from openai import OpenAI
from typing import Dict, List, Optional

class OpenAITranslator:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.context: List[Dict] = []
        self.max_context = 10
    
    async def translate(
        self,
        text: str,
        target_lang: str,
        context: Optional[str] = None,
        use_context: bool = True
    ) -> str:
        language_names = {
            'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'ja': 'Japanese', 'zh': 'Chinese', 'ko': 'Korean'
        }
        
        target_name = language_names.get(target_lang, target_lang)
        
        system_prompt = f"""You are a professional translator. 
        Translate the following text to {target_name}. 
        Maintain the speaker's tone and intent. 
        Only output the translation, nothing else."""
        
        if context:
            system_prompt += f"\nContext: This is from a business meeting about {context}."
        
        messages = [{'role': 'system', 'content': system_prompt}]
        
        # Add context
        if use_context and self.context:
            context_text = "\n\n".join([
                f"Original: {c['original']}\n{target_name}: {c['translation']}"
                for c in self.context[-3:]
            ])
            messages.append({
                'role': 'user',
                'content': f"Previous translations for context:\n{context_text}"
            })
            messages.append({
                'role': 'assistant',
                'content': 'I understand the context.'
            })
        
        messages.append({'role': 'user', 'content': text})
        
        response = self.client.chat.completions.create(
            model='gpt-4',
            messages=messages,
            temperature=0.3,
            max_tokens=1000
        )
        
        translation = response.choices[0].message.content.strip()
        
        self.context.append({
            'original': text,
            'translation': translation,
            'lang': target_lang
        })
        
        if len(self.context) > self.max_context:
            self.context.pop(0)
        
        return translation

# Usage
translator = OpenAITranslator(os.environ['OPENAI_API_KEY'])

async def on_transcript(segment):
    if segment['is_final']:
        spanish = await translator.translate(
            segment['text'],
            'es',
            context='quarterly financial review'
        )
        display_caption('es', spanish)
```

## Resources

- **OpenAI API**: https://platform.openai.com/docs
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

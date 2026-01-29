# Translate with Azure Translator

Real-time translation using Azure Cognitive Services Translator.

## Overview

Use Azure Translator for accurate, real-time meeting translation with support for 100+ languages.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

```javascript
const axios = require('axios');
const { v4: uuidv4 } = require('uuid');

class AzureTranslator {
  constructor(subscriptionKey, region = 'eastus') {
    this.key = subscriptionKey;
    this.region = region;
    this.endpoint = 'https://api.cognitive.microsofttranslator.com';
  }
  
  async translate(text, targetLanguage, sourceLanguage = null) {
    const url = `${this.endpoint}/translate?api-version=3.0&to=${targetLanguage}`;
    const fullUrl = sourceLanguage ? `${url}&from=${sourceLanguage}` : url;
    
    const response = await axios.post(
      fullUrl,
      [{ text }],
      {
        headers: {
          'Ocp-Apim-Subscription-Key': this.key,
          'Ocp-Apim-Subscription-Region': this.region,
          'Content-Type': 'application/json',
          'X-ClientTraceId': uuidv4()
        }
      }
    );
    
    return {
      text: response.data[0].translations[0].text,
      detectedLanguage: response.data[0].detectedLanguage?.language
    };
  }
  
  async translateToMultiple(text, targetLanguages) {
    const toParam = targetLanguages.join('&to=');
    const url = `${this.endpoint}/translate?api-version=3.0&to=${toParam}`;
    
    const response = await axios.post(
      url,
      [{ text }],
      {
        headers: {
          'Ocp-Apim-Subscription-Key': this.key,
          'Ocp-Apim-Subscription-Region': this.region,
          'Content-Type': 'application/json'
        }
      }
    );
    
    const result = {};
    for (const translation of response.data[0].translations) {
      result[translation.to] = translation.text;
    }
    return result;
  }
  
  async detectLanguage(text) {
    const url = `${this.endpoint}/detect?api-version=3.0`;
    
    const response = await axios.post(
      url,
      [{ text }],
      {
        headers: {
          'Ocp-Apim-Subscription-Key': this.key,
          'Content-Type': 'application/json'
        }
      }
    );
    
    return response.data[0];
  }
}

// Usage with RTMS
const translator = new AzureTranslator(process.env.AZURE_TRANSLATOR_KEY, 'eastus');

receiver.onTranscript = async (segment) => {
  if (segment.isFinal) {
    const translations = await translator.translateToMultiple(
      segment.text,
      ['es', 'fr', 'de', 'zh-Hans']
    );
    
    displayMultilingualCaptions(segment.speakerName, translations);
  }
};
```

### Python

```python
import requests
import uuid
from typing import List, Dict

class AzureTranslator:
    def __init__(self, subscription_key: str, region: str = 'eastus'):
        self.key = subscription_key
        self.region = region
        self.endpoint = 'https://api.cognitive.microsofttranslator.com'
    
    def translate(self, text: str, target_language: str, source_language: str = None) -> Dict:
        url = f'{self.endpoint}/translate?api-version=3.0&to={target_language}'
        if source_language:
            url += f'&from={source_language}'
        
        headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-Type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }
        
        response = requests.post(url, headers=headers, json=[{'text': text}])
        result = response.json()[0]
        
        return {
            'text': result['translations'][0]['text'],
            'detected_language': result.get('detectedLanguage', {}).get('language')
        }
    
    def translate_to_multiple(self, text: str, target_languages: List[str]) -> Dict[str, str]:
        to_param = '&to='.join(target_languages)
        url = f'{self.endpoint}/translate?api-version=3.0&to={to_param}'
        
        headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, headers=headers, json=[{'text': text}])
        
        return {
            t['to']: t['text']
            for t in response.json()[0]['translations']
        }

# Usage
translator = AzureTranslator(os.environ['AZURE_TRANSLATOR_KEY'])

def on_transcript(segment):
    if segment['is_final']:
        translations = translator.translate_to_multiple(
            segment['text'],
            ['es', 'fr', 'de', 'zh-Hans']
        )
        print(translations)
```

## Resources

- **Azure Translator**: https://azure.microsoft.com/en-us/services/cognitive-services/translator/
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

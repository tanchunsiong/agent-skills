# OpenRouter Multi-Model Integration

Send RTMS transcripts to multiple AI models via OpenRouter and synthesize a unified response.

## Overview

This use case captures live transcript data from Zoom meetings via RTMS and sends each transcript segment to multiple AI models simultaneously through OpenRouter's unified API. It then synthesizes the responses from all models into a single, validated answer using a designated synthesis model. This multi-model approach cross-checks facts and generates more accurate, well-rounded responses.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

```javascript
import { RTMSManager } from './library/javascript/rtmsManager/RTMSManager.js';
import WebhookManager from './library/javascript/webhookManager/WebhookManager.js';
import { contextualSynthesisFromMultipleModels } from './chatWithOpenrouter.js';

const { MEDIA_PARAMS } = RTMSManager;

const rtmsConfig = {
  logging: { enabled: true, console: true },
  mediaSocketConnectionMode: process.env.MEDIA_SOCKET_CONNECTION_MODE || 'split',
  mediaTypesFlag: 32,
  credentials: {
    meeting: {
      clientId: process.env.ZOOM_CLIENT_ID,
      clientSecret: process.env.ZOOM_CLIENT_SECRET,
      zoomSecretToken: process.env.ZOOM_SECRET_TOKEN,
    }
  },
  mediaParams: {
    transcript: {
      contentType: MEDIA_PARAMS.MEDIA_CONTENT_TYPE_TEXT,
      language: MEDIA_PARAMS.LANGUAGE_ID_ENGLISH,
    }
  }
};

await RTMSManager.init(rtmsConfig);

const webhookManager = new WebhookManager({
  config: {
    webhookPath: process.env.WEBHOOK_PATH || '/webhook',
    zoomSecretToken: rtmsConfig.credentials.meeting.zoomSecretToken,
  },
  app: app
});

webhookManager.on('event', (event, payload) => {
  RTMSManager.handleEvent(event, payload);
});
webhookManager.setup();

// Send each transcript to multiple models and synthesize
RTMSManager.on('transcript', async ({ text, userName, timestamp }) => {
  console.log(`[TRANSCRIPT] ${userName}: ${text}`);
  await contextualSynthesisFromMultipleModels(text);
});

RTMSManager.on('meeting.rtms_started', (payload) => {
  console.log('RTMS Started:', payload.meeting_uuid);
});

await RTMSManager.start();
```

#### Multi-Model Synthesis Module

```javascript
// chatWithOpenrouter.js
const MODELS = (process.env.OPENROUTER_MODELS || 'x-ai/grok-4.1-fast').split(',');
const SYNTHESIS_MODEL = process.env.OPENROUTER_SYNTHESIS_MODEL || 'x-ai/grok-4.1-fast';

async function queryModel(model, prompt) {
  const res = await fetch('https://openrouter.ai/api/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.OPENROUTER_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model,
      messages: [{ role: 'user', content: prompt }],
    }),
  });
  const data = await res.json();
  return data.choices[0].message.content;
}

export async function contextualSynthesisFromMultipleModels(transcript) {
  // Query all models in parallel
  const responses = await Promise.allSettled(
    MODELS.map(model => queryModel(model, transcript))
  );

  const successfulResponses = responses
    .filter(r => r.status === 'fulfilled')
    .map(r => r.value);

  // Synthesize into a single unified answer
  const synthesisPrompt = `Multiple AI models responded to: "${transcript}"

Responses:
${successfulResponses.map((r, i) => `Model ${i + 1}: ${r}`).join('\n\n')}

Synthesize these into one accurate, well-validated answer:`;

  const finalAnswer = await queryModel(SYNTHESIS_MODEL, synthesisPrompt);
  console.log('[SYNTHESIS]', finalAnswer);
  return finalAnswer;
}
```

### Python

```python
import asyncio
import aiohttp
import os
from typing import List

OPENROUTER_API_KEY = os.environ['OPENROUTER_API_KEY']
MODELS = os.environ.get('OPENROUTER_MODELS', 'x-ai/grok-4.1-fast').split(',')

async def query_model(session, model: str, prompt: str) -> str:
    async with session.post(
        'https://openrouter.ai/api/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type': 'application/json',
        },
        json={
            'model': model,
            'messages': [{'role': 'user', 'content': prompt}],
        }
    ) as resp:
        data = await resp.json()
        return data['choices'][0]['message']['content']

async def synthesize_from_models(transcript: str) -> str:
    async with aiohttp.ClientSession() as session:
        tasks = [query_model(session, m, transcript) for m in MODELS]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    valid = [r for r in results if isinstance(r, str)]
    synthesis_prompt = f'Synthesize these model responses:\n'
    synthesis_prompt += '\n'.join(f'Model {i+1}: {r}' for i, r in enumerate(valid))

    async with aiohttp.ClientSession() as session:
        return await query_model(session, MODELS[0], synthesis_prompt)
```

## Resources

- **Sample repo**: https://github.com/zoom/rtms-samples/tree/main/transcript/send_transcript_to_openrouter_js
- **RTMS docs**: https://developers.zoom.us/docs/rtms/
- **OpenRouter API**: https://openrouter.ai/docs

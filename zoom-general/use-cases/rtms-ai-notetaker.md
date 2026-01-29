# AI Industry-Specific Notetaker

Build an AI-powered meeting notetaker with NER, action items, topic classification, and rolling summaries using RTMS transcripts.

## Overview

This use case demonstrates an intelligent meeting assistant that processes RTMS transcript streams through multiple NLP pipelines in real-time. As participants speak, each transcript segment is analyzed for Named Entity Recognition (NER), action item detection, topic classification, and periodic summarization. Results are broadcast to a web frontend via WebSocket for live display, providing comprehensive meeting intelligence.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

```javascript
import { RTMSManager } from './library/javascript/rtmsManager/RTMSManager.js';
import WebhookManager from './library/javascript/webhookManager/WebhookManager.js';
import { FrontendManager } from './library/javascript/rtmsManager/FrontendManager.js';
import { FrontendWssManager } from './library/javascript/rtmsManager/FrontendWssManager.js';
import detectEntities from './nlp/ner.js';
import detectActionItems from './nlp/actionItems.js';
import classifyTopic from './nlp/topicClassifier.js';
import summarize from './nlp/summarizer.js';

const { MEDIA_PARAMS } = RTMSManager;

let transcriptHistory = [];
let actionItems = [];
let summary = '';
let topics = new Set();

const rtmsConfig = {
  logging: 'info',
  credentials: {
    meeting: {
      clientId: process.env.ZOOM_CLIENT_ID,
      clientSecret: process.env.ZOOM_CLIENT_SECRET,
      zoomSecretToken: process.env.ZOOM_SECRET_TOKEN,
    },
  },
  mediaParams: {
    audio: {
      contentType: MEDIA_PARAMS.MEDIA_CONTENT_TYPE_RTP,
      sampleRate: MEDIA_PARAMS.AUDIO_SAMPLE_RATE_SR_16K,
      channel: MEDIA_PARAMS.AUDIO_CHANNEL_MONO,
      codec: MEDIA_PARAMS.MEDIA_PAYLOAD_TYPE_L16,
      dataOpt: MEDIA_PARAMS.MEDIA_DATA_OPTION_AUDIO_MIXED_STREAM,
      sendRate: 100,
    },
    transcript: {
      contentType: MEDIA_PARAMS.MEDIA_CONTENT_TYPE_TEXT,
      language: MEDIA_PARAMS.LANGUAGE_ID_ENGLISH,
    },
  }
};

await RTMSManager.init(rtmsConfig);

// Process transcripts through multiple NLP pipelines
RTMSManager.on('transcript', async ({ text, userName }) => {
  transcriptHistory.push(text);

  // Run NLP analysis
  const ner = await detectEntities(text);
  const actions = detectActionItems(text);
  const topic = await classifyTopic(text);

  if (actions.length) actionItems.push(...actions);
  if (topic) topics.add(topic);

  // Generate rolling summary every 5 segments
  if (transcriptHistory.length % 5 === 0) {
    try {
      summary = await summarize(transcriptHistory.join(' '));
    } catch (e) {
      console.error('Summary error:', e.message);
    }
  }

  // Broadcast results to frontend
  frontendWssManager.broadcastToFrontendClients({
    type: 'transcript',
    content: JSON.stringify({ transcript: text, summary, actionItems, topic, entities: ner }),
    user: userName,
    timestamp: Date.now()
  });
});

RTMSManager.on('meeting.rtms_started', (payload) => {
  transcriptHistory = [];
  actionItems = [];
  summary = '';
  topics = new Set();
});
```

#### Action Item Detection (Pattern-Based)

```javascript
// nlp/actionItems.js
export default function detectActionItems(text) {
  const actions = [];
  const regex = /\b(we need to|let's|assign|follow up|I'll|you should)\b.+?[.?!]/gi;
  let match;
  while ((match = regex.exec(text))) {
    actions.push(match[0]);
  }
  return actions;
}
```

#### NER via OpenRouter

```javascript
// nlp/ner.js
export default async function detectEntities(text) {
  const res = await fetch('https://openrouter.ai/api/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.OPENROUTER_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: process.env.NER_MODEL || 'mistralai/mistral-7b-instruct',
      messages: [
        { role: 'system', content: 'Extract named entities from text. Respond with JSON only.' },
        { role: 'user', content: `Text: ${text}\nOnly return valid JSON.` },
      ],
    }),
  });
  const data = await res.json();
  return JSON.parse(data.choices[0].message.content);
}
```

### Python

```python
import re
from typing import List, Dict, Set

class AINotetaker:
    def __init__(self):
        self.transcript_history: List[str] = []
        self.action_items: List[str] = []
        self.topics: Set[str] = set()
        self.summary: str = ''

    def detect_action_items(self, text: str) -> List[str]:
        pattern = r'\b(we need to|let\'s|assign|follow up|I\'ll|you should)\b.+?[.?!]'
        return re.findall(pattern, text, re.IGNORECASE)

    def process_transcript(self, text: str, user_name: str) -> Dict:
        self.transcript_history.append(text)
        actions = self.detect_action_items(text)
        if actions:
            self.action_items.extend(actions)

        # Generate rolling summary every 5 segments
        if len(self.transcript_history) % 5 == 0:
            self.summary = self._summarize(' '.join(self.transcript_history))

        return {
            'text': text,
            'user': user_name,
            'action_items': self.action_items,
            'summary': self.summary,
        }

    def reset(self):
        self.transcript_history = []
        self.action_items = []
        self.topics = set()
        self.summary = ''
```

## Resources

- **Sample repo**: https://github.com/zoom/rtms-samples/tree/main/zoom_apps/ai_industry_specific_notetaker_js
- **RTMS docs**: https://developers.zoom.us/docs/rtms/
- **OpenRouter**: https://openrouter.ai/docs

# AI Chat with Audio Playback

Build an AI chatbot that processes RTMS transcripts and responds with both text and neural audio playback in the browser.

## Overview

This use case creates an AI-powered assistant that listens to Zoom meeting transcripts via RTMS and responds with both text and synthesized speech. Transcripts are sent to OpenRouter for AI processing, and the response is delivered to a web frontend as text and played back as audio using Deepgram's text-to-speech API. The app supports both webhook and WebSocket event modes.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

```javascript
import { RTMSManager } from './library/javascript/rtmsManager/RTMSManager.js';
import WebhookManager from './library/javascript/webhookManager/WebhookManager.js';
import { setupFrontendWss, broadcastToFrontendClients, sharedServices } from './frontendWss.js';
import { textToSpeechBase64 } from './deepgramService.js';
import { chatWithOpenRouter } from './chatWithOpenrouter.js';
import express from 'express';
import http from 'http';

const { MEDIA_PARAMS } = RTMSManager;

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

const app = express();
const server = http.createServer(app);

await RTMSManager.init(rtmsConfig);

// Register Deepgram TTS service
sharedServices.textToSpeech = textToSpeechBase64;
setupFrontendWss(server);

// Set up webhook handler
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

// Process transcripts: AI response + text-to-speech
RTMSManager.on('transcript', async ({ text, userName, timestamp }) => {
  console.log('Transcript received:', text);

  try {
    // Get AI response from OpenRouter
    const aiResponse = await chatWithOpenRouter(text);

    // Broadcast text response to frontend
    broadcastToFrontendClients({
      type: 'text',
      data: aiResponse,
      metadata: {
        source: 'transcript_response',
        originalText: text,
        userName: userName,
        timestamp: Date.now()
      }
    });

    // Convert AI response to audio and broadcast
    if (sharedServices.textToSpeech) {
      const base64Audio = await sharedServices.textToSpeech(aiResponse);
      broadcastToFrontendClients({
        type: 'audio',
        data: base64Audio,
        metadata: {
          source: 'transcript_response',
          originalText: text,
          aiResponse: aiResponse,
          timestamp: Date.now()
        }
      });
    }
  } catch (error) {
    console.error('Error processing transcript:', error);
  }
});

await RTMSManager.start();

server.listen(process.env.PORT || 3000, () => {
  console.log(`Server running at http://localhost:${process.env.PORT || 3000}`);
});
```

#### Deepgram Text-to-Speech Service

```javascript
// deepgramService.js
import fetch from 'node-fetch';

export async function textToSpeechBase64(text) {
  const response = await fetch('https://api.deepgram.com/v1/speak?model=aura-asteria-en', {
    method: 'POST',
    headers: {
      'Authorization': `Token ${process.env.DEEPGRAM_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text }),
  });

  const buffer = await response.buffer();
  return buffer.toString('base64');
}
```

### Python

```python
import base64
import requests
import os

def text_to_speech(text: str) -> str:
    """Convert text to speech using Deepgram and return base64 audio."""
    response = requests.post(
        'https://api.deepgram.com/v1/speak?model=aura-asteria-en',
        headers={
            'Authorization': f'Token {os.environ["DEEPGRAM_API_KEY"]}',
            'Content-Type': 'application/json',
        },
        json={'text': text}
    )
    return base64.b64encode(response.content).decode()

def process_transcript(text: str, ai_client) -> dict:
    """Process transcript: get AI response and generate audio."""
    ai_response = ai_client.chat(text)
    audio_b64 = text_to_speech(ai_response)
    return {
        'text_response': ai_response,
        'audio_base64': audio_b64,
    }
```

## Resources

- **Sample repo**: https://github.com/zoom/rtms-samples/tree/main/zoom_apps/ai_chat_with_audio_playback_js
- **RTMS docs**: https://developers.zoom.us/docs/rtms/
- **OpenRouter**: https://openrouter.ai/docs
- **Deepgram TTS**: https://developers.deepgram.com/docs/text-to-speech

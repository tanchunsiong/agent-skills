# D&D Game with RTMS Voice Commands

Build a voice-controlled Dungeons & Dragons game during Zoom meetings with an AI Dungeon Master powered by RTMS transcripts.

## Overview

This use case transforms a Zoom meeting into an interactive D&D session. An AI Dungeon Master listens to participant speech via real-time RTMS transcripts and responds with narrative descriptions, NPC dialogue, and adventure choices. The game state persists throughout the meeting, creating a continuous roleplaying experience displayed in a web-based frontend via WebSocket.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

```javascript
import { RTMSManager } from './library/javascript/rtmsManager/RTMSManager.js';
import WebhookManager from './library/javascript/webhookManager/WebhookManager.js';
import { FrontendManager } from './library/javascript/rtmsManager/FrontendManager.js';
import { FrontendWssManager } from './library/javascript/rtmsManager/FrontendWssManager.js';
import { handleTranscript } from './dndGame.js';
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

// Set up frontend UI and WebSocket
const frontendManager = new FrontendManager({
  config: {
    port: 3000,
    serveStaticEnabled: true,
    viewsPath: './views',
    frontendWssUrl: process.env.FRONTEND_WSS_URL_TO_CONNECT_TO || '',
    frontendWssPath: '/ws'
  },
  app: app
});
frontendManager.setup();

const frontendWssManager = new FrontendWssManager({
  config: { frontendWssEnabled: true, frontendWssPath: '/ws' },
  server: server
});
frontendWssManager.setup();

const webhookManager = new WebhookManager({
  config: {
    webhookPath: process.env.WEBHOOK_PATH || '/',
    zoomSecretToken: rtmsConfig.credentials.meeting.zoomSecretToken,
  },
  app: app
});
webhookManager.on('event', (event, payload) => {
  RTMSManager.handleEvent(event, payload);
});
webhookManager.setup();

// Process transcripts as player commands
RTMSManager.on('transcript', async ({ text, userName }) => {
  console.log('Transcript received:', text);

  const dmResult = await handleTranscript(userName, text);

  if (dmResult) {
    console.log(`DM response for ${userName}:`, dmResult.narration);
    frontendWssManager.broadcastToFrontendClients({
      type: 'dm_response',
      content: text,
      user: userName,
      timestamp: Date.now(),
      gameresponse: dmResult,
    });
  }
});

RTMSManager.on('meeting.rtms_started', (payload) => {
  console.log(`RTMS started for meeting ${payload.meeting_uuid}`);
});

await RTMSManager.start();

server.listen(3000, () => {
  console.log('Server running at http://localhost:3000');
});
```

#### D&D Game Logic Module

```javascript
// dndGame.js - AI Dungeon Master with conversation history
import { chatWithOpenRouter } from './chatWithOpenrouter.js';

const history = [
  {
    role: 'system',
    content: `You are a Dungeon Master narrating a fantasy roleplaying game.
Be descriptive and interactive. Offer clear choices. Track player actions
and maintain continuity. Respond in character as the DM.`,
  },
];

export async function handleTranscript(playerName, text) {
  // Format player speech as in-game dialogue
  const playerMessage = `${playerName} says: "${text}"`;
  history.push({ role: 'user', content: playerMessage });

  try {
    const response = await chatWithOpenRouter(history);
    history.push({ role: 'assistant', content: response });

    return {
      narration: response,
      player: playerName,
      action: text,
    };
  } catch (error) {
    console.error('DM error:', error.message);
    return null;
  }
}
```

### Python

```python
from typing import Optional, Dict, List

class DungeonMaster:
    def __init__(self):
        self.history: List[Dict] = [{
            'role': 'system',
            'content': (
                'You are a Dungeon Master narrating a fantasy RPG. '
                'Be descriptive and interactive. Offer clear choices.'
            ),
        }]

    def process_player_action(self, player_name: str, text: str) -> Optional[Dict]:
        player_msg = f'{player_name} says: "{text}"'
        self.history.append({'role': 'user', 'content': player_msg})

        try:
            response = query_llm(self.history)
            self.history.append({'role': 'assistant', 'content': response})
            return {
                'narration': response,
                'player': player_name,
                'action': text,
            }
        except Exception as e:
            print(f'DM error: {e}')
            return None
```

## Resources

- **Sample repo**: https://github.com/zoom/rtms-samples/tree/main/zoom_apps/ai_dnd_game_js
- **RTMS docs**: https://developers.zoom.us/docs/rtms/
- **OpenRouter**: https://openrouter.ai/docs

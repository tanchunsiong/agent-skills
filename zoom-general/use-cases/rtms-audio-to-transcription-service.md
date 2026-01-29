# Send Audio to Transcription Service

Stream RTMS audio to external speech-to-text services.

## Overview

Send real-time audio from RTMS to services like Deepgram, AssemblyAI, or OpenAI Whisper for transcription.

## Skills Needed

- **zoom-rtms** - Primary

## Service Comparison

| Service | Latency | Accuracy | Cost |
|---------|---------|----------|------|
| Deepgram Nova-2 | ~300ms | 95%+ | $0.0043/min |
| AssemblyAI | ~500ms | 94%+ | $0.0037/min |
| OpenAI Whisper | ~1-2s | 95%+ | $0.006/min |
| Google Speech | ~300ms | 93%+ | $0.006/min |

## Implementation

### Deepgram (Recommended for Real-Time)

```javascript
const { createClient, LiveTranscriptionEvents } = require('@deepgram/sdk');

class DeepgramTranscriber {
  constructor(apiKey) {
    this.deepgram = createClient(apiKey);
    this.connection = null;
    this.onTranscript = null;
  }
  
  async connect() {
    this.connection = this.deepgram.listen.live({
      model: 'nova-2',
      language: 'en-US',
      smart_format: true,
      punctuate: true,
      interim_results: true,
      utterance_end_ms: 1000,
      vad_events: true,
      encoding: 'linear16',
      sample_rate: 16000,
      channels: 1
    });
    
    this.connection.on(LiveTranscriptionEvents.Open, () => {
      console.log('Deepgram connected');
    });
    
    this.connection.on(LiveTranscriptionEvents.Transcript, (data) => {
      const transcript = data.channel.alternatives[0];
      
      if (transcript.transcript) {
        this.onTranscript?.({
          text: transcript.transcript,
          confidence: transcript.confidence,
          isFinal: data.is_final,
          words: transcript.words
        });
      }
    });
    
    this.connection.on(LiveTranscriptionEvents.Error, (err) => {
      console.error('Deepgram error:', err);
    });
  }
  
  sendAudio(pcmData) {
    if (this.connection) {
      this.connection.send(pcmData);
    }
  }
  
  close() {
    if (this.connection) {
      this.connection.finish();
    }
  }
}

// Integration with RTMS
const transcriber = new DeepgramTranscriber(process.env.DEEPGRAM_API_KEY);

transcriber.onTranscript = (result) => {
  if (result.isFinal) {
    console.log(`Final: ${result.text}`);
    saveTranscript(result.text);
  } else {
    console.log(`Interim: ${result.text}`);
    updateLiveCaption(result.text);
  }
};

await transcriber.connect();

ws.on('message', (data) => {
  const msg = JSON.parse(data.toString());
  
  // Handle keep-alive
  if (msg.msg_type === 12) {
    ws.send(JSON.stringify({ msg_type: 13, timestamp: msg.timestamp }));
    return;
  }
  
  // Handle audio data
  if (msg.msg_type === 14) {
    const audioData = Buffer.from(msg.content, 'base64');
    transcriber.sendAudio(audioData);
  }
});
```

### AssemblyAI

```javascript
const { AssemblyAI } = require('assemblyai');

class AssemblyAITranscriber {
  constructor(apiKey) {
    this.client = new AssemblyAI({ apiKey });
    this.transcriber = null;
    this.onTranscript = null;
  }
  
  async connect() {
    this.transcriber = this.client.realtime.transcriber({
      sampleRate: 16000,
      encoding: 'pcm_s16le'
    });
    
    this.transcriber.on('open', ({ sessionId }) => {
      console.log(`AssemblyAI session: ${sessionId}`);
    });
    
    this.transcriber.on('transcript', (transcript) => {
      this.onTranscript?.({
        text: transcript.text,
        confidence: transcript.confidence,
        isFinal: transcript.message_type === 'FinalTranscript'
      });
    });
    
    this.transcriber.on('error', (err) => {
      console.error('AssemblyAI error:', err);
    });
    
    await this.transcriber.connect();
  }
  
  sendAudio(pcmData) {
    if (this.transcriber) {
      this.transcriber.sendAudio(pcmData);
    }
  }
  
   async close() {
     if (this.transcriber) {
       await this.transcriber.close();
     }
   }
}

// Integration with RTMS
const transcriber = new AssemblyAITranscriber(process.env.ASSEMBLYAI_API_KEY);

transcriber.onTranscript = (result) => {
  if (result.isFinal) {
    console.log(`Final: ${result.text}`);
    saveTranscript(result.text);
  } else {
    console.log(`Interim: ${result.text}`);
    updateLiveCaption(result.text);
  }
};

await transcriber.connect();

ws.on('message', (data) => {
  const msg = JSON.parse(data.toString());
  
  // Handle keep-alive
  if (msg.msg_type === 12) {
    ws.send(JSON.stringify({ msg_type: 13, timestamp: msg.timestamp }));
    return;
  }
  
  // Handle audio data
  if (msg.msg_type === 14) {
    const audioData = Buffer.from(msg.content, 'base64');
    transcriber.sendAudio(audioData);
  }
});
```

### OpenAI Whisper (Batch)

```javascript
const OpenAI = require('openai');
const fs = require('fs');

class WhisperTranscriber {
  constructor(apiKey) {
    this.openai = new OpenAI({ apiKey });
    this.audioBuffer = Buffer.alloc(0);
    this.chunkDuration = 30; // seconds
  }
  
  addAudio(pcmData) {
    this.audioBuffer = Buffer.concat([this.audioBuffer, pcmData]);
    
    // Process when we have enough audio
    const bytesPerSecond = 16000 * 2; // 16kHz, 16-bit
    if (this.audioBuffer.length >= this.chunkDuration * bytesPerSecond) {
      this.processChunk();
    }
  }
  
  async processChunk() {
    const chunk = this.audioBuffer;
    this.audioBuffer = Buffer.alloc(0);
    
    // Convert to WAV
    const wavBuffer = this.pcmToWav(chunk);
    
    // Write temp file (Whisper API requires file)
    const tempFile = `/tmp/audio_${Date.now()}.wav`;
    fs.writeFileSync(tempFile, wavBuffer);
    
    try {
      const transcription = await this.openai.audio.transcriptions.create({
        file: fs.createReadStream(tempFile),
        model: 'whisper-1',
        language: 'en',
        response_format: 'verbose_json'
      });
      
      return {
        text: transcription.text,
        segments: transcription.segments
      };
    } finally {
      fs.unlinkSync(tempFile);
    }
  }
  
   pcmToWav(pcmData) {
     // Create WAV header + data
     const header = Buffer.alloc(44);
     // ... (see WAV export use case)
     return Buffer.concat([header, pcmData]);
   }
}

// Integration with RTMS
const transcriber = new WhisperTranscriber(process.env.OPENAI_API_KEY);

ws.on('message', (data) => {
  const msg = JSON.parse(data.toString());
  
  // Handle keep-alive
  if (msg.msg_type === 12) {
    ws.send(JSON.stringify({ msg_type: 13, timestamp: msg.timestamp }));
    return;
  }
  
  // Handle audio data
  if (msg.msg_type === 14) {
    const audioData = Buffer.from(msg.content, 'base64');
    transcriber.addAudio(audioData);
  }
});
```

### Python - Deepgram

```python
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions

class DeepgramTranscriber:
    def __init__(self, api_key):
        self.client = DeepgramClient(api_key)
        self.connection = None
        self.on_transcript = None
    
    async def connect(self):
        self.connection = self.client.listen.live.v("1")
        
        options = LiveOptions(
            model="nova-2",
            language="en-US",
            smart_format=True,
            punctuate=True,
            interim_results=True,
            encoding="linear16",
            sample_rate=16000,
            channels=1
        )
        
        def on_message(self, result, **kwargs):
            transcript = result.channel.alternatives[0]
            if transcript.transcript:
                if self.on_transcript:
                    self.on_transcript({
                        'text': transcript.transcript,
                        'confidence': transcript.confidence,
                        'is_final': result.is_final
                    })
        
        self.connection.on(LiveTranscriptionEvents.Transcript, on_message)
        
        await self.connection.start(options)
    
    async def send_audio(self, pcm_data):
        if self.connection:
            await self.connection.send(pcm_data)
    
    async def close(self):
        if self.connection:
            await self.connection.finish()

# Usage
transcriber = DeepgramTranscriber(os.environ['DEEPGRAM_API_KEY'])

def handle_transcript(result):
    if result['is_final']:
        print(f"Final: {result['text']}")
    else:
        print(f"Interim: {result['text']}")

transcriber.on_transcript = handle_transcript
await transcriber.connect()

import json
import base64

async for data in rtms_ws:
    msg = json.loads(data)
    
    # Handle keep-alive
    if msg['msg_type'] == 12:
        await rtms_ws.send(json.dumps({"msg_type": 13, "timestamp": msg["timestamp"]}))
        continue
    
    # Handle audio data
    if msg['msg_type'] == 14:
        audio_data = base64.b64decode(msg['content'])
        await transcriber.send_audio(audio_data)
```

## Resources

- **Deepgram**: https://deepgram.com/
- **AssemblyAI**: https://www.assemblyai.com/
- **OpenAI Whisper**: https://platform.openai.com/docs/guides/speech-to-text
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

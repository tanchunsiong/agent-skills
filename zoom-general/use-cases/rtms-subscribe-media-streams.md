# Subscribe to Media Streams

Subscribe to specific media types (audio, video, transcript) from RTMS.

## Overview

After connecting, subscribe to the media streams you need. You can choose audio, video, transcript, or any combination.

## Skills Needed

- **zoom-rtms** - Primary

## Stream Types

| Type | Format | Use Case |
|------|--------|----------|
| Audio | PCM 16-bit | Transcription, voice analysis |
| Video | H.264 | Visual AI, recording |
| Transcript | JSON | Real-time captions, NLP |

## Implementation

### JavaScript

```javascript
class RTMSSubscriber {
  constructor(ws) {
    this.ws = ws;
    this.subscriptions = new Set();
  }
  
  subscribe(streamTypes) {
    // Valid types: 'audio', 'video', 'transcript'
    const validTypes = ['audio', 'video', 'transcript'];
    const types = streamTypes.filter(t => validTypes.includes(t));
    
    this.ws.send(JSON.stringify({
      msg_type: 'SUBSCRIBE',
      content: {
        stream_types: types
      }
    }));
    
    types.forEach(t => this.subscriptions.add(t));
    console.log(`Subscribed to: ${types.join(', ')}`);
  }
  
  unsubscribe(streamTypes) {
    this.ws.send(JSON.stringify({
      msg_type: 'UNSUBSCRIBE',
      content: {
        stream_types: streamTypes
      }
    }));
    
    streamTypes.forEach(t => this.subscriptions.delete(t));
  }
  
  // Subscribe to audio only (for transcription)
  subscribeAudioOnly() {
    this.subscribe(['audio']);
  }
  
  // Subscribe to transcript only (if Zoom transcription enabled)
  subscribeTranscriptOnly() {
    this.subscribe(['transcript']);
  }
  
  // Subscribe to all streams
  subscribeAll() {
    this.subscribe(['audio', 'video', 'transcript']);
  }
}

// Usage
const ws = new WebSocket(serverUrl, { headers });

ws.on('open', () => {
  const subscriber = new RTMSSubscriber(ws);
  
  // Choose what you need
  subscriber.subscribeAudioOnly();        // Just audio
  // subscriber.subscribeTranscriptOnly(); // Just transcript
  // subscriber.subscribeAll();            // Everything
});

ws.on('message', (data) => {
  const message = JSON.parse(data.toString());
  const msgType = message.msg_type;
  
  switch (msgType) {
    case 13:
      // Keep-alive message
      console.log('Keep-alive received');
      break;
    case 14:
      // Audio chunk (base64 encoded)
      console.log('Audio chunk received');
      const audioBuffer = Buffer.from(message.content.data, 'base64');
      processAudio(audioBuffer);
      break;
    case 15:
      // Video frame (base64 encoded)
      console.log('Video frame received');
      const videoBuffer = Buffer.from(message.content.data, 'base64');
      processVideo(videoBuffer);
      break;
    case 17:
      // Transcript (JSON)
      console.log('Transcript received');
      processTranscript(message.content);
      break;
  }
});
```

### Python

```python
import json

class RTMSSubscriber:
    def __init__(self, websocket):
        self.ws = websocket
        self.subscriptions = set()
    
    async def subscribe(self, stream_types):
        valid_types = {'audio', 'video', 'transcript'}
        types = [t for t in stream_types if t in valid_types]
        
        await self.ws.send(json.dumps({
            'msg_type': 'SUBSCRIBE',
            'content': {
                'stream_types': types
            }
        }))
        
        self.subscriptions.update(types)
        print(f"Subscribed to: {', '.join(types)}")
    
    async def unsubscribe(self, stream_types):
        await self.ws.send(json.dumps({
            'msg_type': 'UNSUBSCRIBE',
            'content': {
                'stream_types': stream_types
            }
        }))
        
        self.subscriptions -= set(stream_types)
    
    async def subscribe_audio_only(self):
        await self.subscribe(['audio'])
    
    async def subscribe_transcript_only(self):
        await self.subscribe(['transcript'])
    
    async def subscribe_all(self):
        await self.subscribe(['audio', 'video', 'transcript'])

# Usage
async def main():
    async with websockets.connect(url, extra_headers=headers) as ws:
        subscriber = RTMSSubscriber(ws)
        await subscriber.subscribe_audio_only()
        
        async for message in ws:
             msg = json.loads(message)
             msg_type = msg.get('msg_type')
             
             if msg_type == 13:
                 # Keep-alive message
                 print('Keep-alive received')
             elif msg_type == 14:
                 # Audio chunk (base64 encoded)
                 print('Audio chunk received')
                 import base64
                 audio_buffer = base64.b64decode(msg['content']['data'])
                 process_audio(audio_buffer)
             elif msg_type == 15:
                 # Video frame (base64 encoded)
                 print('Video frame received')
                 import base64
                 video_buffer = base64.b64decode(msg['content']['data'])
                 process_video(video_buffer)
             elif msg_type == 17:
                 # Transcript (JSON)
                 print('Transcript received')
                 process_transcript(msg['content'])
```

## Bandwidth Considerations

| Stream | Bandwidth | Recommendation |
|--------|-----------|----------------|
| Audio only | ~100 Kbps | Use for transcription |
| Transcript only | ~10 Kbps | Lowest bandwidth |
| Audio + Video | ~2-5 Mbps | Full recording |

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/

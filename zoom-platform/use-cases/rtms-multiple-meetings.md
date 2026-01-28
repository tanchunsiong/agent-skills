# Handle Multiple Concurrent Meetings

Manage RTMS connections for multiple simultaneous meetings.

## Overview

Scale your RTMS application to handle many concurrent meetings with proper connection management and resource allocation.

## Skills Needed

- **zoom-rtms** - Primary

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Connection Manager                        │
├─────────────────────────────────────────────────────────────┤
│  Meeting A ──▶ WebSocket A ──▶ Processor A                  │
│  Meeting B ──▶ WebSocket B ──▶ Processor B                  │
│  Meeting C ──▶ WebSocket C ──▶ Processor C                  │
└─────────────────────────────────────────────────────────────┘
```

## Implementation

### JavaScript

```javascript
const WebSocket = require('ws');
const EventEmitter = require('events');

class RTMSConnectionManager extends EventEmitter {
  constructor(options = {}) {
    super();
    this.connections = new Map();
    this.processors = new Map();
    this.maxConnections = options.maxConnections || 100;
  }
  
  handleWebhook(event, payload) {
    switch (event) {
      case 'meeting.rtms_started':
        this.addMeeting(payload);
        break;
      case 'meeting.rtms_stopped':
        this.removeMeeting(payload.object.meeting_uuid);
        break;
    }
  }
  
  addMeeting(payload) {
    const { meeting_uuid, rtms_stream_id, server_urls, signature } = payload.object;
    
    if (this.connections.size >= this.maxConnections) {
      console.error('Max connections reached, rejecting meeting:', meeting_uuid);
      this.emit('maxConnectionsReached', meeting_uuid);
      return;
    }
    
    if (this.connections.has(meeting_uuid)) {
      console.warn('Meeting already connected:', meeting_uuid);
      return;
    }
    
    const ws = new WebSocket(server_urls[0]);
    
    const processor = new MeetingProcessor(meeting_uuid);
    
    ws.on('open', () => {
      console.log(`Connected to meeting: ${meeting_uuid}`);
      
      // Send HMAC-SHA256 handshake
      const crypto = require('crypto');
      const sig = crypto.createHmac('sha256', process.env.ZOOM_CLIENT_SECRET)
        .update(`${process.env.ZOOM_CLIENT_ID},${meeting_uuid},${rtms_stream_id}`)
        .digest('hex');
      
      const handshake = {
        msg_type: 1,
        protocol_version: 1,
        meeting_uuid: meeting_uuid,
        rtms_stream_id: rtms_stream_id,
        sequence: Math.floor(Math.random() * 1000000),
        signature: sig
      };
      
      ws.send(JSON.stringify(handshake));
      
      this.connections.set(meeting_uuid, ws);
      this.processors.set(meeting_uuid, processor);
      this.emit('connected', meeting_uuid);
    });
    
    ws.on('message', (data) => {
      processor.process(data);
    });
    
    ws.on('close', () => {
      this.cleanup(meeting_uuid);
    });
    
    ws.on('error', (err) => {
      console.error(`Error in meeting ${meeting_uuid}:`, err.message);
    });
  }
  
  removeMeeting(meetingUuid) {
    const ws = this.connections.get(meetingUuid);
    if (ws) {
      ws.close(1000, 'Meeting ended');
    }
    this.cleanup(meetingUuid);
  }
  
  cleanup(meetingUuid) {
    const processor = this.processors.get(meetingUuid);
    if (processor) {
      processor.finalize();
    }
    
    this.connections.delete(meetingUuid);
    this.processors.delete(meetingUuid);
    
    console.log(`Cleaned up meeting: ${meetingUuid}`);
    console.log(`Active connections: ${this.connections.size}`);
    
    this.emit('disconnected', meetingUuid);
  }
  
  getStats() {
    return {
      activeConnections: this.connections.size,
      maxConnections: this.maxConnections,
      meetings: Array.from(this.connections.keys())
    };
  }
  
  closeAll() {
    for (const [meetingUuid, ws] of this.connections) {
      ws.close(1000, 'Server shutdown');
      this.cleanup(meetingUuid);
    }
  }
}

class MeetingProcessor {
  constructor(meetingUuid) {
    this.meetingUuid = meetingUuid;
    this.transcripts = [];
    this.audioChunks = [];
  }
  
  process(data) {
    try {
      const msg = JSON.parse(data);
      
      switch (msg.msg_type) {
        case 14:  // Audio data
          this.processAudio(Buffer.from(msg.content, 'base64'));
          break;
        case 15:  // Video data
          this.processVideo(Buffer.from(msg.content, 'base64'));
          break;
        case 17:  // Transcript data
          this.processTranscript(msg);
          break;
        case 12:  // Heartbeat request
          // Heartbeat handled at connection level
          break;
      }
    } catch (err) {
      console.error(`Error processing message for ${this.meetingUuid}:`, err);
    }
  }
  
  processAudio(payload) {
    // Process audio for this specific meeting
    this.audioChunks.push(payload);
  }
  
  processVideo(payload) {
    // Process video for this specific meeting
  }
  
  processTranscript(transcript) {
    this.transcripts.push(transcript);
  }
  
  finalize() {
    // Save transcripts, generate summary, etc.
    console.log(`Finalizing meeting ${this.meetingUuid}`);
    console.log(`Total transcript segments: ${this.transcripts.length}`);
  }
}

// Usage
const manager = new RTMSConnectionManager({ maxConnections: 50 });

manager.on('connected', (id) => console.log(`Meeting connected: ${id}`));
manager.on('disconnected', (id) => console.log(`Meeting disconnected: ${id}`));
manager.on('maxConnectionsReached', (id) => alertAdmin(id));

app.post('/webhook', (req, res) => {
  const { event, payload } = req.body;
  manager.handleWebhook(event, payload);
  res.status(200).send();
});

// Stats endpoint
app.get('/stats', (req, res) => {
  res.json(manager.getStats());
});

// Graceful shutdown
process.on('SIGTERM', () => {
  manager.closeAll();
  process.exit(0);
});
```

### Python

```python
import asyncio
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class MeetingConnection:
    meeting_uuid: str
    websocket: any
    processor: any

class MeetingProcessor:
    def __init__(self, meeting_uuid: str):
        self.meeting_uuid = meeting_uuid
        self.transcripts = []
        self.audio_chunks = []
    
    def process(self, data: str):
        try:
            import json
            msg = json.loads(data)
            
            if msg.get('msg_type') == 14:  # Audio data
                self.process_audio(bytes.fromhex(msg.get('content', '')))
            elif msg.get('msg_type') == 15:  # Video data
                self.process_video(bytes.fromhex(msg.get('content', '')))
            elif msg.get('msg_type') == 17:  # Transcript data
                self.process_transcript(msg)
            elif msg.get('msg_type') == 12:  # Heartbeat request
                pass  # Handled at connection level
        except Exception as e:
            print(f'Error processing message for {self.meeting_uuid}: {e}')
    
    def process_audio(self, payload: bytes):
        # Process audio for this specific meeting
        self.audio_chunks.append(payload)
    
    def process_video(self, payload: bytes):
        # Process video for this specific meeting
        pass
    
    def process_transcript(self, transcript: dict):
        self.transcripts.append(transcript)
    
    def finalize(self):
        # Save transcripts, generate summary, etc.
        print(f'Finalizing meeting {self.meeting_uuid}')
        print(f'Total transcript segments: {len(self.transcripts)}')

class RTMSConnectionManager:
    def __init__(self, max_connections: int = 100):
        self.connections: Dict[str, MeetingConnection] = {}
        self.max_connections = max_connections
    
    async def handle_webhook(self, event: str, payload: dict):
        if event == 'meeting.rtms_started':
            await self.add_meeting(payload)
        elif event == 'meeting.rtms_stopped':
            await self.remove_meeting(payload['object']['meeting_uuid'])
    
    async def add_meeting(self, payload: dict):
        obj = payload['object']
        meeting_uuid = obj['meeting_uuid']
        
        if len(self.connections) >= self.max_connections:
            print(f'Max connections reached, rejecting: {meeting_uuid}')
            return
        
        if meeting_uuid in self.connections:
            print(f'Meeting already connected: {meeting_uuid}')
            return
        
        try:
            # Send HMAC-SHA256 handshake
            import hmac
            import hashlib
            import json
            import os
            
            sig = hmac.new(
                os.environ['ZOOM_CLIENT_SECRET'].encode(),
                f"{os.environ['ZOOM_CLIENT_ID']},{meeting_uuid},{obj['rtms_stream_id']}".encode(),
                hashlib.sha256
            ).hexdigest()
            
            ws = await websockets.connect(obj['server_urls'][0])
            processor = MeetingProcessor(meeting_uuid)
            
            # Send handshake
            handshake = {
                "msg_type": 1,
                "protocol_version": 1,
                "meeting_uuid": meeting_uuid,
                "rtms_stream_id": obj['rtms_stream_id'],
                "sequence": __import__('random').randint(1, 1000000),
                "signature": sig
            }
            await ws.send(json.dumps(handshake))
            
            self.connections[meeting_uuid] = MeetingConnection(
                meeting_uuid=meeting_uuid,
                websocket=ws,
                processor=processor
            )
            
            # Start processing in background
            asyncio.create_task(self.process_meeting(meeting_uuid))
            print(f'Connected to meeting: {meeting_uuid}')
            
        except Exception as e:
            print(f'Failed to connect to {meeting_uuid}: {e}')
    
    async def process_meeting(self, meeting_uuid: str):
        conn = self.connections.get(meeting_uuid)
        if not conn:
            return
        
        try:
            async for message in conn.websocket:
                conn.processor.process(message)
        except Exception as e:
            print(f'Error processing {meeting_uuid}: {e}')
        finally:
            await self.cleanup(meeting_uuid)
    
    async def remove_meeting(self, meeting_uuid: str):
        conn = self.connections.get(meeting_uuid)
        if conn:
            await conn.websocket.close()
        await self.cleanup(meeting_uuid)
    
    async def cleanup(self, meeting_uuid: str):
        conn = self.connections.pop(meeting_uuid, None)
        if conn:
            conn.processor.finalize()
            print(f'Cleaned up: {meeting_uuid}')
        print(f'Active connections: {len(self.connections)}')
    
    def get_stats(self):
        return {
            'active_connections': len(self.connections),
            'max_connections': self.max_connections,
            'meetings': list(self.connections.keys())
        }
    
    async def close_all(self):
        for meeting_uuid in list(self.connections.keys()):
            await self.remove_meeting(meeting_uuid)
```

## Scaling Considerations

| Factor | Recommendation |
|--------|----------------|
| Max connections per instance | 50-100 |
| Memory per connection | ~50MB (with video) |
| CPU per connection | ~0.1 core |
| Horizontal scaling | Use load balancer |

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/

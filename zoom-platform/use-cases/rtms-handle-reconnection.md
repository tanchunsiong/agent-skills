# Handle RTMS Reconnection

Implement robust reconnection logic for dropped WebSocket connections.

## Overview

Network issues can cause WebSocket disconnections. Implement exponential backoff and state recovery.

## Skills Needed

- **zoom-rtms** - Primary

## Reconnection Strategy

```
Connection Lost
      ↓
Wait (exponential backoff)
      ↓
Check meeting still active
      ↓
Reconnect with same credentials
      ↓
Resume processing
```

## Implementation

### JavaScript

```javascript
class RTMSReconnector {
  constructor(config) {
    this.config = config;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxAttempts = 5;
    this.baseDelay = 1000;
    this.maxDelay = 30000;
    this.isIntentionallyClosed = false;
  }
  
  connect() {
    this.isIntentionallyClosed = false;
    this.ws = new WebSocket(this.config.url);
    
    this.ws.on('open', () => {
      console.log('Connected to RTMS');
      this.reconnectAttempts = 0;
      
      // Send HMAC-SHA256 handshake
      const crypto = require('crypto');
      const signature = crypto.createHmac('sha256', this.config.clientSecret)
        .update(`${this.config.clientId},${this.config.meetingUuid},${this.config.streamId}`)
        .digest('hex');
      
      const handshake = {
        msg_type: 1,
        protocol_version: 1,
        meeting_uuid: this.config.meetingUuid,
        rtms_stream_id: this.config.streamId,
        sequence: Math.floor(Math.random() * 1000000),
        signature: signature
      };
      
      this.ws.send(JSON.stringify(handshake));
    });
    
    this.ws.on('close', (code, reason) => {
      if (!this.isIntentionallyClosed) {
        this.handleDisconnect(code, reason);
      }
    });
    
    this.ws.on('error', (err) => {
      console.error('WebSocket error:', err.message);
    });
    
    this.ws.on('message', (data) => {
      this.config.onMessage(data);
    });
  }
  
  handleDisconnect(code, reason) {
    console.log(`Disconnected: ${code} - ${reason}`);
    
    if (this.reconnectAttempts >= this.maxAttempts) {
      console.error('Max reconnection attempts reached');
      this.config.onMaxRetriesExceeded?.();
      return;
    }
    
    const delay = Math.min(
      this.baseDelay * Math.pow(2, this.reconnectAttempts),
      this.maxDelay
    );
    
    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts + 1})`);
    
    setTimeout(() => {
      this.reconnectAttempts++;
      this.connect();
    }, delay);
  }
  
  disconnect() {
    this.isIntentionallyClosed = true;
    if (this.ws) {
      this.ws.close(1000, 'Client closing');
    }
  }
}

// Usage
const client = new RTMSReconnector({
  url: serverUrl,
  streamId: streamId,
  signature: signature,
  onMessage: (data) => processMedia(data),
  onMaxRetriesExceeded: () => alertAdmin()
});

client.connect();
```

### Python

```python
import asyncio
import websockets

class RTMSReconnector:
    def __init__(self, config):
        self.config = config
        self.reconnect_attempts = 0
        self.max_attempts = 5
        self.base_delay = 1
        self.max_delay = 30
        self.running = True
    
    async def connect(self):
        while self.running and self.reconnect_attempts < self.max_attempts:
            try:
                async with websockets.connect(self.config['url']) as ws:
                    print('Connected to RTMS')
                    self.reconnect_attempts = 0
                    
                    # Send HMAC-SHA256 handshake
                    import hmac
                    import hashlib
                    import json
                    
                    signature = hmac.new(
                        self.config['client_secret'].encode(),
                        f"{self.config['client_id']},{self.config['meeting_uuid']},{self.config['stream_id']}".encode(),
                        hashlib.sha256
                    ).hexdigest()
                    
                    handshake = {
                        "msg_type": 1,
                        "protocol_version": 1,
                        "meeting_uuid": self.config['meeting_uuid'],
                        "rtms_stream_id": self.config['stream_id'],
                        "sequence": __import__('random').randint(1, 1000000),
                        "signature": signature
                    }
                    
                    await ws.send(json.dumps(handshake))
                    
                    async for message in ws:
                        await self.config['on_message'](message)
                        
            except websockets.ConnectionClosed as e:
                await self.handle_disconnect(e.code, e.reason)
            except Exception as e:
                print(f'Connection error: {e}')
                await self.handle_disconnect(None, str(e))
    
    async def handle_disconnect(self, code, reason):
        if not self.running:
            return
            
        print(f'Disconnected: {code} - {reason}')
        
        delay = min(
            self.base_delay * (2 ** self.reconnect_attempts),
            self.max_delay
        )
        
        print(f'Reconnecting in {delay}s (attempt {self.reconnect_attempts + 1})')
        await asyncio.sleep(delay)
        self.reconnect_attempts += 1
    
    def stop(self):
        self.running = False
```

## Close Codes

| Code | Meaning | Action |
|------|---------|--------|
| 1000 | Normal close | Don't reconnect |
| 1001 | Going away | Reconnect |
| 1006 | Abnormal close | Reconnect |
| 4001 | Meeting ended | Don't reconnect |

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/

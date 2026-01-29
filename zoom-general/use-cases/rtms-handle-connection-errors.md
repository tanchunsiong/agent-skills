# Handle Connection Errors

Gracefully handle RTMS connection errors and edge cases.

## Overview

Implement comprehensive error handling for network issues, authentication failures, and unexpected disconnections.

## Skills Needed

- **zoom-rtms** - Primary

## Error Types

| Error | Cause | Recovery |
|-------|-------|----------|
| 401 Unauthorized | Invalid/expired signature | Request new credentials |
| 403 Forbidden | RTMS not enabled | Enable in Marketplace |
| 1006 Abnormal Close | Network issue | Reconnect with backoff |
| 4001 Meeting Ended | Meeting finished | Don't reconnect |
| Timeout | Server unresponsive | Retry connection |

## Implementation

### JavaScript

```javascript
class RTMSErrorHandler {
  constructor(config) {
    this.config = config;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
  }
  
  connect() {
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        reject(new Error('Connection timeout'));
      }, this.config.timeout || 15000);
      
      this.ws = new WebSocket(this.config.url);
      
      this.ws.on('open', () => {
        clearTimeout(timeout);
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
        resolve(this.ws);
      });
      
      this.ws.on('error', (err) => {
        clearTimeout(timeout);
        this.handleError(err);
        reject(err);
      });
      
      this.ws.on('close', (code, reason) => {
        this.handleClose(code, reason.toString());
      });
      
      // Handle upgrade errors (HTTP errors before WebSocket)
      this.ws.on('unexpected-response', (req, res) => {
        clearTimeout(timeout);
        this.handleHttpError(res.statusCode);
        reject(new Error(`HTTP ${res.statusCode}`));
      });
    });
  }
  
  handleError(err) {
    console.error('WebSocket error:', err.message);
    
    if (err.code === 'ECONNREFUSED') {
      console.error('Connection refused - server may be down');
    } else if (err.code === 'ETIMEDOUT') {
      console.error('Connection timed out');
    } else if (err.code === 'ENOTFOUND') {
      console.error('DNS lookup failed - check URL');
    }
    
    this.config.onError?.(err);
  }
  
  handleHttpError(statusCode) {
    switch (statusCode) {
      case 401:
        console.error('Authentication failed - signature invalid or expired');
        this.config.onAuthError?.();
        break;
      case 403:
        console.error('Forbidden - RTMS may not be enabled for this app');
        break;
      case 404:
        console.error('Stream not found - meeting may have ended');
        break;
      case 429:
        console.error('Rate limited - too many connection attempts');
        break;
      case 503:
        console.error('Service unavailable - try again later');
        this.scheduleReconnect();
        break;
      default:
        console.error(`Unexpected HTTP error: ${statusCode}`);
    }
  }
  
  handleClose(code, reason) {
    console.log(`Connection closed: ${code} - ${reason}`);
    
    switch (code) {
      case 1000:
        // Normal closure
        console.log('Clean disconnect');
        break;
      case 1001:
        // Going away
        console.log('Server going away - reconnecting');
        this.scheduleReconnect();
        break;
      case 1006:
        // Abnormal closure
        console.log('Abnormal closure - reconnecting');
        this.scheduleReconnect();
        break;
      case 4001:
        // Meeting ended (custom code)
        console.log('Meeting ended');
        this.config.onMeetingEnded?.();
        break;
      default:
        console.log(`Unknown close code: ${code}`);
        this.scheduleReconnect();
    }
  }
  
  scheduleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnect attempts reached');
      this.config.onMaxRetriesExceeded?.();
      return;
    }
    
    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
    console.log(`Reconnecting in ${delay}ms`);
    
    setTimeout(() => {
      this.reconnectAttempts++;
      this.connect().catch(() => {});
    }, delay);
  }
}

// Usage
const handler = new RTMSErrorHandler({
  url: serverUrl,
  streamId: streamId,
  signature: signature,
  timeout: 15000,
  onError: (err) => logError(err),
  onAuthError: () => requestNewCredentials(),
  onMeetingEnded: () => cleanup(),
  onMaxRetriesExceeded: () => alertAdmin()
});

handler.connect()
  .then(ws => console.log('Connected'))
  .catch(err => console.error('Failed to connect:', err));
```

### Python

```python
import asyncio
import websockets
from enum import IntEnum

class CloseCode(IntEnum):
    NORMAL = 1000
    GOING_AWAY = 1001
    ABNORMAL = 1006
    MEETING_ENDED = 4001

class RTMSErrorHandler:
    def __init__(self, config):
        self.config = config
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
    
    async def connect(self):
        try:
            ws = await asyncio.wait_for(
                websockets.connect(self.config['url']),
                timeout=self.config.get('timeout', 15)
            )
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
            return ws
            
        except asyncio.TimeoutError:
            print('Connection timeout')
            raise
        except websockets.InvalidStatusCode as e:
            self.handle_http_error(e.status_code)
            raise
        except Exception as e:
            self.handle_error(e)
            raise
    
    def handle_error(self, err):
        print(f'WebSocket error: {err}')
        if self.config.get('on_error'):
            self.config['on_error'](err)
    
    def handle_http_error(self, status_code):
        errors = {
            401: 'Authentication failed',
            403: 'Forbidden - RTMS not enabled',
            404: 'Stream not found',
            429: 'Rate limited',
            503: 'Service unavailable'
        }
        print(f'HTTP error: {errors.get(status_code, f"Unknown {status_code}")}')
    
    async def handle_close(self, code, reason):
        print(f'Connection closed: {code} - {reason}')
        
        if code == CloseCode.NORMAL:
            print('Clean disconnect')
        elif code == CloseCode.MEETING_ENDED:
            print('Meeting ended')
            if self.config.get('on_meeting_ended'):
                self.config['on_meeting_ended']()
        elif code in (CloseCode.GOING_AWAY, CloseCode.ABNORMAL):
            await self.schedule_reconnect()
    
    async def schedule_reconnect(self):
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            print('Max reconnect attempts reached')
            return
        
        delay = min(2 ** self.reconnect_attempts, 30)
        print(f'Reconnecting in {delay}s')
        
        await asyncio.sleep(delay)
        self.reconnect_attempts += 1
        
        try:
            await self.connect()
        except Exception:
            pass
```

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/

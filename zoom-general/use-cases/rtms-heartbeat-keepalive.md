# Implement Heartbeat/Keep-Alive

Maintain RTMS connection health with heartbeat messages.

## Overview

Send periodic heartbeats to keep the WebSocket connection alive and detect dead connections early.

## Skills Needed

- **zoom-rtms** - Primary

## Why Heartbeats?

- Detect dead connections before data loss
- Prevent NAT/firewall timeout disconnections
- Monitor connection health

## Implementation

### JavaScript

```javascript
class RTMSHeartbeat {
  constructor(ws, options = {}) {
    this.ws = ws;
    this.pingInterval = options.pingInterval || 30000; // 30 seconds
    this.pongTimeout = options.pongTimeout || 10000;   // 10 seconds
    this.pingTimer = null;
    this.pongTimer = null;
    this.missedPongs = 0;
    this.maxMissedPongs = 3;
    this.onConnectionDead = options.onConnectionDead;
  }
  
  start() {
    this.pingTimer = setInterval(() => {
      this.sendPing();
    }, this.pingInterval);
    
    // Listen for pong responses
    this.ws.on('pong', () => {
      this.handlePong();
    });
    
    console.log('Heartbeat started');
  }
  
  sendPing() {
    if (this.ws.readyState !== WebSocket.OPEN) {
      this.stop();
      return;
    }
    
    // Send WebSocket ping frame
    this.ws.ping();
    
    // Start pong timeout
    this.pongTimer = setTimeout(() => {
      this.handlePongTimeout();
    }, this.pongTimeout);
  }
  
  handlePong() {
    // Clear timeout and reset counter
    clearTimeout(this.pongTimer);
    this.missedPongs = 0;
  }
  
  handlePongTimeout() {
    this.missedPongs++;
    console.warn(`Pong timeout (${this.missedPongs}/${this.maxMissedPongs})`);
    
    if (this.missedPongs >= this.maxMissedPongs) {
      console.error('Connection appears dead - terminating');
      this.ws.terminate();
      this.onConnectionDead?.();
    }
  }
  
  stop() {
    clearInterval(this.pingTimer);
    clearTimeout(this.pongTimer);
    console.log('Heartbeat stopped');
  }
}

// Usage
const ws = new WebSocket(serverUrl, { headers });

ws.on('open', () => {
  const heartbeat = new RTMSHeartbeat(ws, {
    pingInterval: 30000,
    pongTimeout: 10000,
    onConnectionDead: () => {
      console.log('Initiating reconnection...');
      reconnect();
    }
  });
  
  heartbeat.start();
});

ws.on('close', () => {
  // Heartbeat will auto-stop when ws closes
});
```

### Application-Level Heartbeat

```javascript
// If WebSocket ping/pong not available, use application-level messages
class AppHeartbeat {
  constructor(ws, options = {}) {
    this.ws = ws;
    this.interval = options.interval || 30000;
    this.timeout = options.timeout || 10000;
    this.timer = null;
    this.pendingResponse = null;
  }
  
  start() {
    this.timer = setInterval(() => {
      this.sendHeartbeat();
    }, this.interval);
    
    console.log('Application heartbeat started');
  }
  
  sendHeartbeat() {
    const timestamp = Date.now();
    
    this.ws.send(JSON.stringify({
      msg_type: 'HEARTBEAT',
      timestamp: timestamp
    }));
    
    this.pendingResponse = setTimeout(() => {
      console.error('Heartbeat response timeout');
      this.ws.close(4000, 'Heartbeat timeout');
    }, this.timeout);
  }
  
  handleResponse(message) {
    if (message.msg_type === 'HEARTBEAT_ACK') {
      clearTimeout(this.pendingResponse);
      const latency = Date.now() - message.timestamp;
      console.log(`Heartbeat OK (latency: ${latency}ms)`);
    }
  }
  
  stop() {
    clearInterval(this.timer);
    clearTimeout(this.pendingResponse);
  }
}
```

### Python

```python
import asyncio
import time

class RTMSHeartbeat:
    def __init__(self, ws, ping_interval=30, pong_timeout=10):
        self.ws = ws
        self.ping_interval = ping_interval
        self.pong_timeout = pong_timeout
        self.running = False
        self.missed_pongs = 0
        self.max_missed_pongs = 3
        self.on_connection_dead = None
    
    async def start(self):
        self.running = True
        print('Heartbeat started')
        
        while self.running:
            await asyncio.sleep(self.ping_interval)
            if self.running:
                await self.send_ping()
    
    async def send_ping(self):
        try:
            # Send ping and wait for pong
            pong_waiter = await self.ws.ping()
            await asyncio.wait_for(pong_waiter, timeout=self.pong_timeout)
            self.missed_pongs = 0
            
        except asyncio.TimeoutError:
            self.missed_pongs += 1
            print(f'Pong timeout ({self.missed_pongs}/{self.max_missed_pongs})')
            
            if self.missed_pongs >= self.max_missed_pongs:
                print('Connection appears dead')
                await self.ws.close()
                if self.on_connection_dead:
                    await self.on_connection_dead()
    
    def stop(self):
        self.running = False
        print('Heartbeat stopped')

# Usage
async def main():
    async with websockets.connect(url, extra_headers=headers) as ws:
        heartbeat = RTMSHeartbeat(ws)
        heartbeat.on_connection_dead = reconnect
        
        # Run heartbeat in background
        heartbeat_task = asyncio.create_task(heartbeat.start())
        
        try:
            async for message in ws:
                process_message(message)
        finally:
            heartbeat.stop()
            heartbeat_task.cancel()
```

## Recommended Settings

| Setting | Value | Reason |
|---------|-------|--------|
| Ping interval | 30s | Balance between overhead and detection |
| Pong timeout | 10s | Allow for network latency |
| Max missed pongs | 3 | Tolerate transient issues |

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/
- **WebSocket RFC (Ping/Pong)**: https://tools.ietf.org/html/rfc6455#section-5.5.2

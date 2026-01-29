# Decode H.264 Video

Decode H.264 video frames from RTMS for processing.

## Overview

RTMS video is H.264 encoded. Decode to raw frames for visual AI, thumbnails, or recording.

## Skills Needed

- **zoom-rtms** - Primary

## Decoding Options

| Library | Language | GPU Support |
|---------|----------|-------------|
| FFmpeg | Any | Yes |
| OpenCV | Python/C++ | Yes (CUDA) |
| node-ffmpeg | Node.js | Yes |
| PyAV | Python | Yes |

## Implementation

### JavaScript - FFmpeg

```javascript
const { spawn } = require('child_process');

class H264Decoder {
  constructor(options = {}) {
    this.width = options.width || 1280;
    this.height = options.height || 720;
    this.onFrame = options.onFrame;
    this.ffmpeg = null;
  }
  
  start() {
    this.ffmpeg = spawn('ffmpeg', [
      '-f', 'h264',
      '-i', 'pipe:0',
      '-f', 'rawvideo',
      '-pix_fmt', 'rgb24',
      '-s', `${this.width}x${this.height}`,
      'pipe:1'
    ]);
    
    const frameSize = this.width * this.height * 3;
    let buffer = Buffer.alloc(0);
    
    this.ffmpeg.stdout.on('data', (data) => {
      buffer = Buffer.concat([buffer, data]);
      
      while (buffer.length >= frameSize) {
        const frame = buffer.slice(0, frameSize);
        buffer = buffer.slice(frameSize);
        
        this.onFrame?.({
          data: frame,
          width: this.width,
          height: this.height,
          format: 'rgb24',
          timestamp: Date.now()
        });
      }
    });
    
    this.ffmpeg.stderr.on('data', (data) => {
      // FFmpeg logs
    });
  }
  
  decode(h264Data) {
    if (this.ffmpeg && this.ffmpeg.stdin.writable) {
      this.ffmpeg.stdin.write(h264Data);
    }
  }
  
  stop() {
    if (this.ffmpeg) {
      this.ffmpeg.stdin.end();
      this.ffmpeg.kill();
    }
  }
}

// Usage
const decoder = new H264Decoder({
  width: 1280,
  height: 720,
  onFrame: (frame) => {
    console.log(`Decoded frame: ${frame.width}x${frame.height}`);
    // Process raw RGB frame
    processFrame(frame.data);
  }
});

decoder.start();

ws.on('message', (data) => {
  const msg = JSON.parse(data.toString());
  
  // Handle keep-alive
  if (msg.msg_type === 12) {
    ws.send(JSON.stringify({ msg_type: 13, timestamp: msg.timestamp }));
    return;
  }
  
  // Handle video frame (msg_type 15)
  if (msg.msg_type === 15) {
    const videoData = Buffer.from(msg.content, 'base64');
    decoder.decode(videoData);
  }
});

ws.on('close', () => {
  decoder.stop();
});
```

### Python - OpenCV

```python
import cv2
import numpy as np
from queue import Queue
from threading import Thread

class H264Decoder:
    def __init__(self):
        self.buffer = b''
        self.on_frame = None
        
    def decode_frame(self, h264_data):
        """Decode single H.264 NAL unit"""
        # Accumulate data
        self.buffer += h264_data
        
        # Try to decode
        nparr = np.frombuffer(self.buffer, np.uint8)
        
        # Use OpenCV's H.264 decoder
        # Note: Requires complete NAL units
        try:
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if frame is not None:
                self.buffer = b''  # Clear buffer on success
                if self.on_frame:
                    self.on_frame(frame)
                return frame
        except:
            pass
        
        return None

# Using PyAV (more reliable for streaming)
import av

class PyAVDecoder:
    def __init__(self):
        self.codec = av.CodecContext.create('h264', 'r')
        self.on_frame = None
    
    def decode(self, h264_data):
        """Decode H.264 data"""
        packet = av.Packet(h264_data)
        
        try:
            frames = self.codec.decode(packet)
            for frame in frames:
                # Convert to numpy array
                img = frame.to_ndarray(format='rgb24')
                
                if self.on_frame:
                    self.on_frame({
                        'data': img,
                        'width': frame.width,
                        'height': frame.height,
                        'pts': frame.pts
                    })
                
                return img
        except av.AVError as e:
            print(f"Decode error: {e}")
        
        return None

# Usage
decoder = PyAVDecoder()

def on_frame(frame):
    print(f"Decoded: {frame['width']}x{frame['height']}")
    # Process with OpenCV, PIL, etc.
    cv2.imshow('Video', cv2.cvtColor(frame['data'], cv2.COLOR_RGB2BGR))

decoder.on_frame = on_frame

import json
import base64

async for message in ws:
    msg = json.loads(message)
    
    # Handle keep-alive
    if msg['msg_type'] == 12:
        await ws.send(json.dumps({"msg_type": 13, "timestamp": msg["timestamp"]}))
        continue
    
    # Handle video frame (msg_type 15)
    if msg['msg_type'] == 15:
        video_data = base64.b64decode(msg['content'])
        decoder.decode(video_data)
```

### Python - FFmpeg subprocess

```python
import subprocess
import numpy as np

class FFmpegDecoder:
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height
        self.frame_size = width * height * 3
        self.process = None
        self.on_frame = None
    
    def start(self):
        self.process = subprocess.Popen([
            'ffmpeg',
            '-f', 'h264',
            '-i', 'pipe:0',
            '-f', 'rawvideo',
            '-pix_fmt', 'rgb24',
            '-s', f'{self.width}x{self.height}',
            'pipe:1'
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        
        # Start reader thread
        import threading
        self.reader = threading.Thread(target=self._read_frames)
        self.reader.daemon = True
        self.reader.start()
    
    def _read_frames(self):
        buffer = b''
        while self.process:
            data = self.process.stdout.read(4096)
            if not data:
                break
            
            buffer += data
            
            while len(buffer) >= self.frame_size:
                frame_data = buffer[:self.frame_size]
                buffer = buffer[self.frame_size:]
                
                frame = np.frombuffer(frame_data, dtype=np.uint8)
                frame = frame.reshape((self.height, self.width, 3))
                
                if self.on_frame:
                    self.on_frame(frame)
    
    def decode(self, h264_data):
        if self.process and self.process.stdin:
            self.process.stdin.write(h264_data)
    
    def stop(self):
        if self.process:
            self.process.stdin.close()
            self.process.terminate()
            self.process = None

# Usage
decoder = FFmpegDecoder(1280, 720)
decoder.on_frame = lambda f: print(f"Frame: {f.shape}")
decoder.start()

import json
import base64

async for message in ws:
    msg = json.loads(message)
    
    # Handle keep-alive
    if msg['msg_type'] == 12:
        await ws.send(json.dumps({"msg_type": 13, "timestamp": msg["timestamp"]}))
        continue
    
    # Handle video frame (msg_type 15)
    if msg['msg_type'] == 15:
        video_data = base64.b64decode(msg['content'])
        decoder.decode(video_data)
```

## Performance Tips

| Tip | Benefit |
|-----|---------|
| Use GPU decoding | 10x faster |
| Decode keyframes only | Lower CPU |
| Resize during decode | Less processing |
| Use hardware codec | NVENC/VAAPI |

## Resources

- **PyAV**: https://pyav.org/
- **FFmpeg**: https://ffmpeg.org/
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

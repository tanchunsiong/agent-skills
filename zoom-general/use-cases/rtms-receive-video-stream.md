# Receive Video Stream

Receive and process H.264 video frames from RTMS.

## Overview

RTMS delivers video as H.264 encoded frames. Decode for visual AI, recording, or analysis.

## Skills Needed

- **zoom-rtms** - Primary

## Video Format

| Property | Value |
|----------|-------|
| Codec | H.264 (AVC) |
| Container | Raw NAL units |
| Resolution | Up to 1080p |
| Frame rate | Variable (typically 15-30 fps) |

## Implementation

### JavaScript

```javascript
class RTMSVideoReceiver {
  constructor(options = {}) {
    this.frames = [];
    this.onFrame = options.onFrame;
    this.onKeyFrame = options.onKeyFrame;
  }
  
  handleMessage(data) {
     // Parse JSON protocol message
     const message = JSON.parse(data);
     
     // msg_type 15 = VIDEO
     if (message.msg_type === 15) {
       // Decode base64 video data
       const videoData = Buffer.from(message.data, 'base64');
       this.processVideoFrame(videoData);
     }
     
     // msg_type 13 = KEEP_ALIVE
     if (message.msg_type === 13) {
       // Handle keep-alive
     }
   }
  
  processVideoFrame(frameData) {
    // Parse NAL unit header
    const nalType = frameData[0] & 0x1F;
    
    const frame = {
      data: frameData,
      timestamp: Date.now(),
      isKeyFrame: nalType === 5 || nalType === 7, // IDR or SPS
      nalType: nalType,
      size: frameData.length
    };
    
    this.frames.push(frame);
    
    if (frame.isKeyFrame) {
      this.onKeyFrame?.(frame);
    }
    
    this.onFrame?.(frame);
    
    return frame;
  }
  
  getFrameCount() {
    return this.frames.length;
  }
  
  getKeyFrames() {
    return this.frames.filter(f => f.isKeyFrame);
  }
  
  clear() {
    this.frames = [];
  }
}

// Usage
const videoReceiver = new RTMSVideoReceiver({
  onFrame: (frame) => {
    console.log(`Frame: ${frame.size} bytes, keyframe: ${frame.isKeyFrame}`);
  },
  onKeyFrame: (frame) => {
    console.log('Keyframe received - can start decoding');
  }
});

ws.on('message', (data) => {
  videoReceiver.handleMessage(data);
});
```

### Python

```python
class RTMSVideoReceiver:
    def __init__(self):
        self.frames = []
        self.on_frame = None
        self.on_keyframe = None
    
    def handle_message(self, data):
         import json
         import base64
         
         # Parse JSON protocol message
         message = json.loads(data)
         
         # msg_type 15 = VIDEO
         if message.get('msg_type') == 15:
             # Decode base64 video data
             video_data = base64.b64decode(message.get('data', ''))
             self.process_video_frame(video_data)
         
         # msg_type 13 = KEEP_ALIVE
         if message.get('msg_type') == 13:
             # Handle keep-alive
             pass
    
    def process_video_frame(self, frame_data):
        import time
        
        # Parse NAL unit type
        nal_type = frame_data[0] & 0x1F
        
        frame = {
            'data': frame_data,
            'timestamp': time.time(),
            'is_keyframe': nal_type in (5, 7),  # IDR or SPS
            'nal_type': nal_type,
            'size': len(frame_data)
        }
        
        self.frames.append(frame)
        
        if frame['is_keyframe'] and self.on_keyframe:
            self.on_keyframe(frame)
        
        if self.on_frame:
            self.on_frame(frame)
        
        return frame
    
    def get_frame_count(self):
        return len(self.frames)
    
    def get_keyframes(self):
        return [f for f in self.frames if f['is_keyframe']]

# Usage
receiver = RTMSVideoReceiver()

def on_frame(frame):
    print(f"Frame: {frame['size']} bytes, keyframe: {frame['is_keyframe']}")

receiver.on_frame = on_frame

async for message in ws:
    receiver.handle_message(message)
```

## NAL Unit Types

| Type | Name | Description |
|------|------|-------------|
| 1 | Non-IDR | P/B frame |
| 5 | IDR | Keyframe |
| 7 | SPS | Sequence Parameter Set |
| 8 | PPS | Picture Parameter Set |

## Resources

- **H.264 spec**: https://www.itu.int/rec/T-REC-H.264
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

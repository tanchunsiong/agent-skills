# Video Frame Extraction

Extract individual frames from RTMS video streams.

## Overview

Extract frames for thumbnails, visual AI analysis, or image processing.

## Skills Needed

- **zoom-rtms** - Primary

## Extraction Strategies

| Strategy | Use Case | CPU |
|----------|----------|-----|
| Keyframes only | Thumbnails | Low |
| Every Nth frame | Sampling | Medium |
| All frames | Full analysis | High |

## Implementation

### JavaScript

```javascript
const sharp = require('sharp');

class FrameExtractor {
  constructor(options = {}) {
    this.strategy = options.strategy || 'keyframe'; // keyframe, interval, all
    this.interval = options.interval || 30; // frames
    this.outputDir = options.outputDir || './frames';
    this.format = options.format || 'jpeg';
    this.quality = options.quality || 80;
    
    this.frameCount = 0;
    this.extractedCount = 0;
    this.decoder = null;
  }
  
  shouldExtract(isKeyFrame) {
    this.frameCount++;
    
    switch (this.strategy) {
      case 'keyframe':
        return isKeyFrame;
      case 'interval':
        return this.frameCount % this.interval === 0;
      case 'all':
        return true;
      default:
        return false;
    }
  }
  
  async extractFrame(frameData, width, height) {
    const filename = `frame_${this.extractedCount.toString().padStart(6, '0')}.${this.format}`;
    const filepath = `${this.outputDir}/${filename}`;
    
    try {
      await sharp(frameData, {
        raw: {
          width: width,
          height: height,
          channels: 3
        }
      })
      .jpeg({ quality: this.quality })
      .toFile(filepath);
      
      this.extractedCount++;
      
      return {
        path: filepath,
        index: this.extractedCount - 1,
        timestamp: Date.now()
      };
    } catch (err) {
      console.error('Frame extraction error:', err);
      return null;
    }
  }
  
  async extractToBuffer(frameData, width, height) {
    return await sharp(frameData, {
      raw: {
        width: width,
        height: height,
        channels: 3
      }
    })
    .jpeg({ quality: this.quality })
    .toBuffer();
  }
  
  getStats() {
    return {
      totalFrames: this.frameCount,
      extractedFrames: this.extractedCount,
      ratio: this.extractedCount / this.frameCount
    };
  }
}

// Usage with RTMS video decoder
const extractor = new FrameExtractor({
  strategy: 'interval',
  interval: 30, // Every 30 frames (~1 per second at 30fps)
  outputDir: './meeting_frames',
  quality: 85
});

// RTMS WebSocket connection with JSON protocol
const ws = new WebSocket('wss://rtms.zoom.us/...');

ws.onmessage = async (event) => {
  try {
    const message = JSON.parse(event.data);
    
    // msg_type 15 = VIDEO frame
    if (message.msg_type === 15 && message.data) {
      // Decode base64 video data
      const frameBuffer = Buffer.from(message.data, 'base64');
      
      // Decode frame using video decoder
      const frame = decoder.decode(frameBuffer);
      
      if (frame && extractor.shouldExtract(frame.isKeyFrame)) {
        const result = await extractor.extractFrame(
          frame.data,
          frame.width,
          frame.height
        );
        
        if (result) {
          console.log(`Extracted: ${result.path}`);
          // Send to visual AI
          analyzeFrame(result.path);
        }
      }
    }
    
    // msg_type 13 = KEEP_ALIVE
    if (message.msg_type === 13) {
      console.log('Keep-alive received');
    }
  } catch (err) {
    console.error('Message parsing error:', err);
  }
};
```

### Python

```python
import cv2
import os
from pathlib import Path
from PIL import Image
import io

class FrameExtractor:
    def __init__(
        self,
        strategy='keyframe',
        interval=30,
        output_dir='./frames',
        format='jpeg',
        quality=80
    ):
        self.strategy = strategy
        self.interval = interval
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.format = format
        self.quality = quality
        
        self.frame_count = 0
        self.extracted_count = 0
    
    def should_extract(self, is_keyframe=False):
        self.frame_count += 1
        
        if self.strategy == 'keyframe':
            return is_keyframe
        elif self.strategy == 'interval':
            return self.frame_count % self.interval == 0
        elif self.strategy == 'all':
            return True
        return False
    
    def extract_frame(self, frame_array, filename=None):
        """Extract frame to file"""
        if filename is None:
            filename = f"frame_{self.extracted_count:06d}.{self.format}"
        
        filepath = self.output_dir / filename
        
        # Convert RGB to BGR for OpenCV
        if len(frame_array.shape) == 3 and frame_array.shape[2] == 3:
            frame_bgr = cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)
        else:
            frame_bgr = frame_array
        
        # Save with quality setting
        if self.format == 'jpeg':
            cv2.imwrite(str(filepath), frame_bgr, [cv2.IMWRITE_JPEG_QUALITY, self.quality])
        elif self.format == 'png':
            cv2.imwrite(str(filepath), frame_bgr, [cv2.IMWRITE_PNG_COMPRESSION, 9 - self.quality // 10])
        
        self.extracted_count += 1
        
        return {
            'path': str(filepath),
            'index': self.extracted_count - 1,
            'shape': frame_array.shape
        }
    
    def extract_to_buffer(self, frame_array):
        """Extract frame to bytes buffer"""
        img = Image.fromarray(frame_array)
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=self.quality)
        buffer.seek(0)
        return buffer.getvalue()
    
    def extract_thumbnail(self, frame_array, size=(320, 180)):
        """Extract resized thumbnail"""
        img = Image.fromarray(frame_array)
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=70)
        buffer.seek(0)
        return buffer.getvalue()
    
    def get_stats(self):
        return {
            'total_frames': self.frame_count,
            'extracted_frames': self.extracted_count,
            'ratio': self.extracted_count / max(self.frame_count, 1)
        }

# Usage
extractor = FrameExtractor(
    strategy='interval',
    interval=30,
    output_dir='./meeting_frames'
)

def on_decoded_frame(frame, is_keyframe):
    if extractor.should_extract(is_keyframe):
        result = extractor.extract_frame(frame)
        print(f"Extracted: {result['path']}")
        
        # Also get thumbnail for quick preview
        thumbnail = extractor.extract_thumbnail(frame)
        upload_thumbnail(thumbnail)

# With RTMS JSON protocol
import json
import base64
import asyncio
import websockets

async def process_rtms_stream():
    uri = "wss://rtms.zoom.us/..."
    async with websockets.connect(uri) as ws:
        async for message_str in ws:
            try:
                message = json.loads(message_str)
                
                # msg_type 15 = VIDEO frame
                if message.get('msg_type') == 15 and message.get('data'):
                    # Decode base64 video data
                    frame_bytes = base64.b64decode(message['data'])
                    
                    # Decode frame using video decoder
                    frame = decoder.decode(frame_bytes)
                    
                    if frame is not None:
                        is_keyframe = message.get('is_keyframe', False)
                        on_decoded_frame(frame, is_keyframe=is_keyframe)
                
                # msg_type 13 = KEEP_ALIVE
                if message.get('msg_type') == 13:
                    print('Keep-alive received')
                    
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
            except Exception as e:
                print(f"Frame processing error: {e}")

# Run the stream processor
asyncio.run(process_rtms_stream())
```

### Batch Extraction

```python
class BatchFrameExtractor:
    def __init__(self, output_dir, batch_size=10):
        self.output_dir = Path(output_dir)
        self.batch_size = batch_size
        self.pending_frames = []
        self.on_batch_ready = None
    
    def add_frame(self, frame_array, metadata=None):
        self.pending_frames.append({
            'frame': frame_array,
            'metadata': metadata or {},
            'timestamp': time.time()
        })
        
        if len(self.pending_frames) >= self.batch_size:
            self.process_batch()
    
    def process_batch(self):
        batch = self.pending_frames[:self.batch_size]
        self.pending_frames = self.pending_frames[self.batch_size:]
        
        results = []
        for i, item in enumerate(batch):
            filename = f"batch_{int(time.time())}_{i:03d}.jpg"
            filepath = self.output_dir / filename
            
            cv2.imwrite(str(filepath), cv2.cvtColor(item['frame'], cv2.COLOR_RGB2BGR))
            results.append({
                'path': str(filepath),
                'metadata': item['metadata']
            })
        
        if self.on_batch_ready:
            self.on_batch_ready(results)
    
    def flush(self):
        while self.pending_frames:
            self.process_batch()
```

## Resources

- **Pillow**: https://pillow.readthedocs.io/
- **sharp**: https://sharp.pixelplumbing.com/
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

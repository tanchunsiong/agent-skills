# Video Thumbnail Generation

Generate thumbnails from RTMS video streams.

## Overview

Create thumbnails for meeting previews, timeline scrubbing, or content indexing.

## Skills Needed

- **zoom-rtms** - Primary

## Thumbnail Strategies

| Strategy | Use Case | Storage |
|----------|----------|---------|
| Keyframe only | Preview | Low |
| Interval (1/min) | Timeline | Medium |
| Scene change | Smart index | Low |

## Implementation

### JavaScript

```javascript
const sharp = require('sharp');
const fs = require('fs');

class ThumbnailGenerator {
  constructor(options = {}) {
    this.outputDir = options.outputDir || './thumbnails';
    this.width = options.width || 320;
    this.height = options.height || 180;
    this.quality = options.quality || 80;
    this.interval = options.interval || 60000; // 1 minute
    this.strategy = options.strategy || 'interval'; // keyframe, interval, scene
    
    this.lastThumbnailTime = 0;
    this.lastFrame = null;
    this.thumbnails = [];
    
    fs.mkdirSync(this.outputDir, { recursive: true });
  }
  
  async processFrame(frameBuffer, width, height, isKeyframe = false) {
    const now = Date.now();
    let shouldGenerate = false;
    
    switch (this.strategy) {
      case 'keyframe':
        shouldGenerate = isKeyframe;
        break;
      case 'interval':
        shouldGenerate = now - this.lastThumbnailTime >= this.interval;
        break;
      case 'scene':
        shouldGenerate = await this.detectSceneChange(frameBuffer, width, height);
        break;
    }
    
    if (shouldGenerate) {
      return await this.generateThumbnail(frameBuffer, width, height);
    }
    
    return null;
  }
  
  async generateThumbnail(frameBuffer, width, height) {
    const timestamp = Date.now();
    const filename = `thumb_${timestamp}.jpg`;
    const filepath = `${this.outputDir}/${filename}`;
    
    try {
      // Add RGBA channel if needed (RGB -> RGBA)
      let channels = 3;
      if (frameBuffer.length === width * height * 4) {
        channels = 4;
      }
      
      await sharp(frameBuffer, {
        raw: { width, height, channels }
      })
      .resize(this.width, this.height, { fit: 'cover' })
      .jpeg({ quality: this.quality })
      .toFile(filepath);
      
      this.lastThumbnailTime = timestamp;
      
      const thumbnail = {
        path: filepath,
        filename: filename,
        timestamp: timestamp,
        index: this.thumbnails.length
      };
      
      this.thumbnails.push(thumbnail);
      
      return thumbnail;
    } catch (err) {
      console.error('Thumbnail generation error:', err);
      return null;
    }
  }
  
  async generateToBuffer(frameBuffer, width, height) {
    let channels = frameBuffer.length === width * height * 4 ? 4 : 3;
    
    return await sharp(frameBuffer, {
      raw: { width, height, channels }
    })
    .resize(this.width, this.height, { fit: 'cover' })
    .jpeg({ quality: this.quality })
    .toBuffer();
  }
  
  async detectSceneChange(frameBuffer, width, height) {
    if (!this.lastFrame) {
      this.lastFrame = frameBuffer;
      return true;
    }
    
    // Calculate difference
    const diff = await this.calculateDiff(this.lastFrame, frameBuffer, width, height);
    this.lastFrame = frameBuffer;
    
    return diff > 0.3; // 30% change threshold
  }
  
  async calculateDiff(frame1, frame2, width, height) {
    // Resize both frames for faster comparison
    const size = 50;
    
    const small1 = await sharp(frame1, { raw: { width, height, channels: 3 } })
      .resize(size, size)
      .raw()
      .toBuffer();
    
    const small2 = await sharp(frame2, { raw: { width, height, channels: 3 } })
      .resize(size, size)
      .raw()
      .toBuffer();
    
    let diff = 0;
    for (let i = 0; i < small1.length; i++) {
      diff += Math.abs(small1[i] - small2[i]);
    }
    
    return diff / (small1.length * 255);
  }
  
  getThumbnails() {
    return this.thumbnails;
  }
  
  async createSpriteSheet(columns = 10) {
    if (this.thumbnails.length === 0) return null;
    
    const rows = Math.ceil(this.thumbnails.length / columns);
    const spriteWidth = this.width * columns;
    const spriteHeight = this.height * rows;
    
    // Create composite
    const composites = this.thumbnails.map((thumb, i) => ({
      input: thumb.path,
      left: (i % columns) * this.width,
      top: Math.floor(i / columns) * this.height
    }));
    
    const spritePath = `${this.outputDir}/sprite.jpg`;
    
    await sharp({
      create: {
        width: spriteWidth,
        height: spriteHeight,
        channels: 3,
        background: { r: 0, g: 0, b: 0 }
      }
    })
    .composite(composites)
    .jpeg({ quality: 80 })
    .toFile(spritePath);
    
    return {
      path: spritePath,
      columns,
      rows,
      thumbWidth: this.width,
      thumbHeight: this.height
    };
  }
}

// Usage
const thumbGen = new ThumbnailGenerator({
  outputDir: './meeting_thumbnails',
  width: 320,
  height: 180,
  strategy: 'interval',
  interval: 30000 // Every 30 seconds
});

ws.on('message', async (message) => {
   try {
     const msgData = JSON.parse(message);
     const msgType = msgData.msg_type;
     
     // Handle keep-alive (msg_type 13)
     if (msgType === 13) {
       return;
     }
     
     // Process video frames (msg_type 15)
     if (msgType === 15) {
       const videoData = msgData.data || {};
       const frameb64 = videoData.frame;
       
       if (frameb64) {
         // Decode base64 frame data
         const frameBuffer = Buffer.from(frameb64, 'base64');
         const width = videoData.width;
         const height = videoData.height;
         const isKeyframe = videoData.is_keyframe || false;
         
         const thumb = await thumbGen.processFrame(
           frameBuffer,
           width,
           height,
           isKeyframe
         );
         
         if (thumb) {
           console.log(`Thumbnail: ${thumb.filename}`);
         }
       }
     }
   } catch (err) {
     console.error('Message parsing error:', err);
   }
});

// At end of meeting
const sprite = await thumbGen.createSpriteSheet(10);
console.log(`Sprite sheet: ${sprite.path}`);
```

### Python

```python
from PIL import Image
import numpy as np
from pathlib import Path
import time
import io
import json
import base64

class ThumbnailGenerator:
    def __init__(
        self,
        output_dir='./thumbnails',
        width=320,
        height=180,
        quality=80,
        interval=60,
        strategy='interval'
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.width = width
        self.height = height
        self.quality = quality
        self.interval = interval
        self.strategy = strategy
        
        self.last_thumbnail_time = 0
        self.last_frame = None
        self.thumbnails = []
    
    def process_frame(self, frame: np.ndarray, is_keyframe=False):
        now = time.time()
        should_generate = False
        
        if self.strategy == 'keyframe':
            should_generate = is_keyframe
        elif self.strategy == 'interval':
            should_generate = now - self.last_thumbnail_time >= self.interval
        elif self.strategy == 'scene':
            should_generate = self.detect_scene_change(frame)
        
        if should_generate:
            return self.generate_thumbnail(frame)
        
        return None
    
    def generate_thumbnail(self, frame: np.ndarray):
        timestamp = int(time.time() * 1000)
        filename = f"thumb_{timestamp}.jpg"
        filepath = self.output_dir / filename
        
        try:
            img = Image.fromarray(frame)
            img = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
            img.save(filepath, 'JPEG', quality=self.quality)
            
            self.last_thumbnail_time = time.time()
            
            thumbnail = {
                'path': str(filepath),
                'filename': filename,
                'timestamp': timestamp,
                'index': len(self.thumbnails)
            }
            
            self.thumbnails.append(thumbnail)
            return thumbnail
            
        except Exception as e:
            print(f"Thumbnail error: {e}")
            return None
    
    def generate_to_buffer(self, frame: np.ndarray) -> bytes:
        img = Image.fromarray(frame)
        img = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
        
        buffer = io.BytesIO()
        img.save(buffer, 'JPEG', quality=self.quality)
        buffer.seek(0)
        return buffer.getvalue()
    
    def detect_scene_change(self, frame: np.ndarray) -> bool:
        if self.last_frame is None:
            self.last_frame = frame.copy()
            return True
        
        # Calculate difference
        diff = self.calculate_diff(self.last_frame, frame)
        self.last_frame = frame.copy()
        
        return diff > 0.3
    
    def calculate_diff(self, frame1: np.ndarray, frame2: np.ndarray) -> float:
        # Resize for faster comparison
        size = (50, 50)
        small1 = np.array(Image.fromarray(frame1).resize(size))
        small2 = np.array(Image.fromarray(frame2).resize(size))
        
        diff = np.abs(small1.astype(float) - small2.astype(float))
        return np.mean(diff) / 255
    
    def create_sprite_sheet(self, columns=10):
        if not self.thumbnails:
            return None
        
        rows = (len(self.thumbnails) + columns - 1) // columns
        sprite_width = self.width * columns
        sprite_height = self.height * rows
        
        sprite = Image.new('RGB', (sprite_width, sprite_height), (0, 0, 0))
        
        for i, thumb in enumerate(self.thumbnails):
            img = Image.open(thumb['path'])
            x = (i % columns) * self.width
            y = (i // columns) * self.height
            sprite.paste(img, (x, y))
        
        sprite_path = self.output_dir / 'sprite.jpg'
        sprite.save(sprite_path, 'JPEG', quality=80)
        
        return {
            'path': str(sprite_path),
            'columns': columns,
            'rows': rows,
            'thumb_width': self.width,
            'thumb_height': self.height
        }

# Usage
generator = ThumbnailGenerator(
    output_dir='./meeting_thumbnails',
    strategy='interval',
    interval=30
)

async for message in ws:
     try:
         msg_data = json.loads(message)
         msg_type = msg_data.get('msg_type')
         
         # Handle keep-alive (msg_type 13)
         if msg_type == 13:
             continue
         
         # Process video frames (msg_type 15)
         if msg_type == 15:
             video_data = msg_data.get('data', {})
             frame_b64 = video_data.get('frame')
             
             if frame_b64:
                 # Decode base64 frame data
                 frame_bytes = base64.b64decode(frame_b64)
                 frame = np.frombuffer(frame_bytes, dtype=np.uint8)
                 frame = frame.reshape((video_data.get('height'), video_data.get('width'), 3))
                 
                 is_keyframe = video_data.get('is_keyframe', False)
                 thumb = generator.process_frame(frame, is_keyframe=is_keyframe)
                 
                 if thumb:
                     print(f"Thumbnail: {thumb['filename']}")
     except json.JSONDecodeError:
         continue

# Create sprite sheet at end
sprite = generator.create_sprite_sheet(10)
print(f"Sprite: {sprite['path']}")
```

## Resources

- **sharp**: https://sharp.pixelplumbing.com/
- **Pillow**: https://pillow.readthedocs.io/
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

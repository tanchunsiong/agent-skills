# Screen Share Video Processing

Process screen share content from RTMS video streams.

## Overview

Detect and process screen share content for OCR, slide extraction, or content analysis.

## Skills Needed

- **zoom-rtms** - Primary

## Screen Share Features

| Feature | Use Case |
|---------|----------|
| Detect start/stop | Trigger processing |
| OCR text extraction | Searchable content |
| Slide detection | Presentation index |
| Change detection | Only process new content |

## Implementation

### JavaScript

```javascript
const Tesseract = require('tesseract.js');
const sharp = require('sharp');

class ScreenShareProcessor {
  constructor(options = {}) {
    this.isScreenSharing = false;
    this.lastFrame = null;
    this.changeThreshold = options.changeThreshold || 0.1;
    this.ocrEnabled = options.ocrEnabled || true;
    
    this.slides = [];
    this.onSlideDetected = null;
    this.onTextExtracted = null;
  }
  
  handleRTMSMessage(message) {
    // Detect screen share events
    if (message.type === 'screen_share_started') {
      this.isScreenSharing = true;
      console.log('Screen share started');
      return;
    }
    
    if (message.type === 'screen_share_stopped') {
      this.isScreenSharing = false;
      console.log('Screen share stopped');
      return;
    }
    
    // Process screen share video
    if (message.type === 'video' && message.is_screen_share) {
      this.processFrame(message.data);
    }
  }
  
  async processFrame(frameData) {
    const hasChanged = await this.detectChange(frameData);
    
    if (hasChanged) {
      // New slide/content detected
      const slideIndex = this.slides.length;
      
      this.slides.push({
        index: slideIndex,
        timestamp: Date.now(),
        data: frameData
      });
      
      this.onSlideDetected?.({
        index: slideIndex,
        timestamp: Date.now()
      });
      
      // Extract text if enabled
      if (this.ocrEnabled) {
        const text = await this.extractText(frameData);
        this.onTextExtracted?.({
          slideIndex: slideIndex,
          text: text
        });
      }
    }
  }
  
  async detectChange(currentFrame) {
    if (!this.lastFrame) {
      this.lastFrame = currentFrame;
      return true;
    }
    
    const diff = await this.calculateDifference(this.lastFrame, currentFrame);
    this.lastFrame = currentFrame;
    
    return diff > this.changeThreshold;
  }
  
  async calculateDifference(frame1, frame2) {
    // Simple pixel difference
    const img1 = await sharp(frame1).resize(100, 100).raw().toBuffer();
    const img2 = await sharp(frame2).resize(100, 100).raw().toBuffer();
    
    let diff = 0;
    for (let i = 0; i < img1.length; i++) {
      diff += Math.abs(img1[i] - img2[i]);
    }
    
    return diff / (img1.length * 255);
  }
  
  async extractText(frameData) {
    try {
      const { data: { text } } = await Tesseract.recognize(frameData, 'eng');
      return text.trim();
    } catch (err) {
      console.error('OCR error:', err);
      return '';
    }
  }
  
  getSlides() {
    return this.slides;
  }
  
  async exportSlides(outputDir) {
    for (const slide of this.slides) {
      const filename = `slide_${slide.index.toString().padStart(3, '0')}.jpg`;
      await sharp(slide.data)
        .jpeg({ quality: 90 })
        .toFile(`${outputDir}/${filename}`);
    }
  }
}

// Usage
const processor = new ScreenShareProcessor({
  changeThreshold: 0.15,
  ocrEnabled: true
});

processor.onSlideDetected = (slide) => {
  console.log(`New slide detected: ${slide.index}`);
};

processor.onTextExtracted = (result) => {
  console.log(`Slide ${result.slideIndex} text:`, result.text.substring(0, 100));
};

ws.on('message', (data) => {
  const message = parseRTMSMessage(data);
  processor.handleRTMSMessage(message);
});
```

### Python

```python
import cv2
import numpy as np
from PIL import Image
import pytesseract
from dataclasses import dataclass
from typing import List, Optional, Callable
import time

@dataclass
class Slide:
    index: int
    timestamp: float
    frame: np.ndarray
    text: Optional[str] = None

class ScreenShareProcessor:
    def __init__(self, change_threshold=0.1, ocr_enabled=True):
        self.is_screen_sharing = False
        self.last_frame = None
        self.change_threshold = change_threshold
        self.ocr_enabled = ocr_enabled
        
        self.slides: List[Slide] = []
        self.on_slide_detected: Optional[Callable] = None
        self.on_text_extracted: Optional[Callable] = None
    
    def handle_message(self, message: dict):
        if message.get('type') == 'screen_share_started':
            self.is_screen_sharing = True
            print('Screen share started')
            return
        
        if message.get('type') == 'screen_share_stopped':
            self.is_screen_sharing = False
            print('Screen share stopped')
            return
        
        if message.get('type') == 'video' and message.get('is_screen_share'):
            self.process_frame(message['data'])
    
    def process_frame(self, frame_data: np.ndarray):
        has_changed = self.detect_change(frame_data)
        
        if has_changed:
            slide_index = len(self.slides)
            
            slide = Slide(
                index=slide_index,
                timestamp=time.time(),
                frame=frame_data.copy()
            )
            
            self.slides.append(slide)
            
            if self.on_slide_detected:
                self.on_slide_detected({
                    'index': slide_index,
                    'timestamp': slide.timestamp
                })
            
            if self.ocr_enabled:
                text = self.extract_text(frame_data)
                slide.text = text
                
                if self.on_text_extracted:
                    self.on_text_extracted({
                        'slide_index': slide_index,
                        'text': text
                    })
    
    def detect_change(self, current_frame: np.ndarray) -> bool:
        if self.last_frame is None:
            self.last_frame = current_frame.copy()
            return True
        
        diff = self.calculate_difference(self.last_frame, current_frame)
        self.last_frame = current_frame.copy()
        
        return diff > self.change_threshold
    
    def calculate_difference(self, frame1: np.ndarray, frame2: np.ndarray) -> float:
        # Resize for faster comparison
        small1 = cv2.resize(frame1, (100, 100))
        small2 = cv2.resize(frame2, (100, 100))
        
        # Calculate normalized difference
        diff = np.abs(small1.astype(float) - small2.astype(float))
        return np.mean(diff) / 255
    
    def extract_text(self, frame: np.ndarray) -> str:
        try:
            # Convert to grayscale for better OCR
            if len(frame.shape) == 3:
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            else:
                gray = frame
            
            # Apply preprocessing
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            
            # OCR
            text = pytesseract.image_to_string(gray)
            return text.strip()
        except Exception as e:
            print(f'OCR error: {e}')
            return ''
    
    def get_slides(self) -> List[Slide]:
        return self.slides
    
    def export_slides(self, output_dir: str):
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        for slide in self.slides:
            filename = f"slide_{slide.index:03d}.jpg"
            filepath = os.path.join(output_dir, filename)
            
            cv2.imwrite(filepath, cv2.cvtColor(slide.frame, cv2.COLOR_RGB2BGR))
            
            # Save text if available
            if slide.text:
                text_file = filepath.replace('.jpg', '.txt')
                with open(text_file, 'w') as f:
                    f.write(slide.text)

# Usage
processor = ScreenShareProcessor(change_threshold=0.15)

def on_slide(slide):
    print(f"New slide: {slide['index']}")

def on_text(result):
    print(f"Slide {result['slide_index']}: {result['text'][:100]}...")

processor.on_slide_detected = on_slide
processor.on_text_extracted = on_text

async for message in ws:
    parsed = parse_message(message)
    processor.handle_message(parsed)

# Export at end
processor.export_slides('./slides')
```

## OCR Tips

| Tip | Benefit |
|-----|---------|
| Preprocess image | Better accuracy |
| Use grayscale | Faster processing |
| Threshold binary | Clean text edges |
| Resize to 300+ DPI | Standard for OCR |

## Resources

- **Tesseract.js**: https://tesseract.projectnaptha.com/
- **pytesseract**: https://github.com/madmaze/pytesseract
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

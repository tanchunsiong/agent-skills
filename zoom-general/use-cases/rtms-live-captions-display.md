# Live Captions Display

Display real-time captions from RTMS transcripts.

## Overview

Show live captions with speaker attribution, styling, and smooth transitions.

## Skills Needed

- **zoom-rtms** - Primary

## Caption Features

| Feature | Description |
|---------|-------------|
| Speaker labels | Show who's speaking |
| Partial updates | Smooth text flow |
| Auto-scroll | Follow latest text |
| Fade animation | Clean transitions |

## Implementation

### JavaScript - Web Component

```javascript
class LiveCaptionDisplay {
  constructor(container, options = {}) {
    this.container = container;
    this.maxLines = options.maxLines || 3;
    this.fadeTime = options.fadeTime || 5000;
    this.showSpeaker = options.showSpeaker !== false;
    
    this.lines = [];
    this.currentPartial = null;
    
    this.setupStyles();
  }
  
  setupStyles() {
    const style = document.createElement('style');
    style.textContent = `
      .caption-container {
        position: fixed;
        bottom: 20%;
        left: 50%;
        transform: translateX(-50%);
        max-width: 80%;
        text-align: center;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
      }
      
      .caption-line {
        background: rgba(0, 0, 0, 0.75);
        color: white;
        padding: 8px 16px;
        margin: 4px 0;
        border-radius: 4px;
        font-size: 24px;
        line-height: 1.4;
        transition: opacity 0.3s ease;
      }
      
      .caption-speaker {
        color: #4fc3f7;
        font-weight: 600;
        margin-right: 8px;
      }
      
      .caption-partial {
        opacity: 0.7;
        font-style: italic;
      }
      
      .caption-fade {
        opacity: 0;
      }
    `;
    document.head.appendChild(style);
    
    this.container.className = 'caption-container';
  }
  
  addFinalCaption(speaker, text) {
    // Remove partial if from same speaker
    if (this.currentPartial) {
      this.currentPartial.remove();
      this.currentPartial = null;
    }
    
    const line = document.createElement('div');
    line.className = 'caption-line';
    
    if (this.showSpeaker) {
      const speakerSpan = document.createElement('span');
      speakerSpan.className = 'caption-speaker';
      speakerSpan.textContent = speaker + ':';
      line.appendChild(speakerSpan);
    }
    
    const textSpan = document.createElement('span');
    textSpan.textContent = text;
    line.appendChild(textSpan);
    
    this.container.appendChild(line);
    this.lines.push(line);
    
    // Remove old lines
    while (this.lines.length > this.maxLines) {
      const oldLine = this.lines.shift();
      oldLine.classList.add('caption-fade');
      setTimeout(() => oldLine.remove(), 300);
    }
    
    // Auto-fade after timeout
    setTimeout(() => {
      if (this.lines.includes(line)) {
        line.classList.add('caption-fade');
        setTimeout(() => {
          line.remove();
          this.lines = this.lines.filter(l => l !== line);
        }, 300);
      }
    }, this.fadeTime);
  }
  
  updatePartialCaption(speaker, text) {
    if (!this.currentPartial) {
      this.currentPartial = document.createElement('div');
      this.currentPartial.className = 'caption-line caption-partial';
      this.container.appendChild(this.currentPartial);
    }
    
    this.currentPartial.innerHTML = '';
    
    if (this.showSpeaker) {
      const speakerSpan = document.createElement('span');
      speakerSpan.className = 'caption-speaker';
      speakerSpan.textContent = speaker + ':';
      this.currentPartial.appendChild(speakerSpan);
    }
    
    const textSpan = document.createElement('span');
    textSpan.textContent = text;
    this.currentPartial.appendChild(textSpan);
  }
  
  clear() {
    this.container.innerHTML = '';
    this.lines = [];
    this.currentPartial = null;
  }
}

// Usage
const captionContainer = document.getElementById('captions');
const display = new LiveCaptionDisplay(captionContainer, {
  maxLines: 3,
  fadeTime: 5000,
  showSpeaker: true
});

// Connect to RTMS transcript
ws.on('message', (data) => {
  const message = JSON.parse(data.toString());
  
  // Handle keep-alive messages
  if (message.msg_type === 13) {
    return;
  }
  
  // Handle transcript messages
  if (message.msg_type === 17) {
    const { user_name, text, is_final } = message;
    
    if (is_final) {
      display.addFinalCaption(user_name, text);
    } else {
      display.updatePartialCaption(user_name, text);
    }
  }
});
```

### React Component

```jsx
import React, { useState, useEffect, useRef } from 'react';

const LiveCaptions = ({ maxLines = 3, fadeTime = 5000 }) => {
  const [captions, setCaptions] = useState([]);
  const [partial, setPartial] = useState(null);
  const containerRef = useRef(null);
  
  const addCaption = (speaker, text) => {
    const id = Date.now();
    
    setCaptions(prev => {
      const updated = [...prev, { id, speaker, text }];
      return updated.slice(-maxLines);
    });
    
    setPartial(null);
    
    // Auto-remove after fade time
    setTimeout(() => {
      setCaptions(prev => prev.filter(c => c.id !== id));
    }, fadeTime);
  };
  
  const updatePartial = (speaker, text) => {
    setPartial({ speaker, text });
  };
  
   // Expose methods via ref
   useEffect(() => {
     window.captionApi = { addCaption, updatePartial };
   }, []);
   
   // Listen to RTMS messages
   useEffect(() => {
     const handleMessage = (event) => {
       const message = JSON.parse(event.data);
       
       // Handle keep-alive messages
       if (message.msg_type === 13) {
         return;
       }
       
       // Handle transcript messages
       if (message.msg_type === 17) {
         const { user_name, text, is_final } = message;
         
         if (is_final) {
           addCaption(user_name, text);
         } else {
           updatePartial(user_name, text);
         }
       }
     };
     
     // Attach to global WebSocket if available
     if (window.ws) {
       window.ws.addEventListener('message', handleMessage);
       return () => window.ws.removeEventListener('message', handleMessage);
     }
   }, [addCaption, updatePartial]);
  
  return (
    <div ref={containerRef} style={styles.container}>
      {captions.map(caption => (
        <div key={caption.id} style={styles.line}>
          <span style={styles.speaker}>{caption.speaker}:</span>
          <span>{caption.text}</span>
        </div>
      ))}
      
      {partial && (
        <div style={{ ...styles.line, ...styles.partial }}>
          <span style={styles.speaker}>{partial.speaker}:</span>
          <span>{partial.text}</span>
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    position: 'fixed',
    bottom: '20%',
    left: '50%',
    transform: 'translateX(-50%)',
    maxWidth: '80%',
    textAlign: 'center',
  },
  line: {
    background: 'rgba(0, 0, 0, 0.75)',
    color: 'white',
    padding: '8px 16px',
    margin: '4px 0',
    borderRadius: '4px',
    fontSize: '24px',
    lineHeight: 1.4,
  },
  speaker: {
    color: '#4fc3f7',
    fontWeight: 600,
    marginRight: '8px',
  },
  partial: {
    opacity: 0.7,
    fontStyle: 'italic',
  },
};

export default LiveCaptions;
```

### Python - Terminal Display

```python
import sys
from collections import deque

class TerminalCaptionDisplay:
    def __init__(self, max_lines=5):
        self.max_lines = max_lines
        self.lines = deque(maxlen=max_lines)
        self.current_partial = None
    
    def add_final(self, speaker: str, text: str):
        self.current_partial = None
        self.lines.append(f"\033[94m{speaker}:\033[0m {text}")
        self.render()
    
    def update_partial(self, speaker: str, text: str):
        self.current_partial = f"\033[94m{speaker}:\033[0m \033[3m{text}\033[0m"
        self.render()
    
    def render(self):
        # Clear previous lines
        sys.stdout.write(f"\033[{self.max_lines + 1}A")  # Move up
        sys.stdout.write("\033[J")  # Clear to end
        
        # Print lines
        for line in self.lines:
            print(line)
        
        # Print partial
        if self.current_partial:
            print(self.current_partial)
        else:
            print()  # Empty line
        
        # Fill remaining lines
        remaining = self.max_lines - len(self.lines)
        for _ in range(remaining):
            print()
        
        sys.stdout.flush()

# Usage
display = TerminalCaptionDisplay(max_lines=5)

async for message in ws:
     data = json.loads(message)
     
     # Handle keep-alive messages
     if data.get('msg_type') == 13:
         continue
     
     # Handle transcript messages
     if data.get('msg_type') == 17:
         if data.get('is_final'):
             display.add_final(data['user_name'], data['text'])
         else:
             display.update_partial(data['user_name'], data['text'])
```

## Resources

- **Web Animations API**: https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API
- **RTMS docs**: https://developers.zoom.us/docs/rtms/

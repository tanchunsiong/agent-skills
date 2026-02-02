# Zoom Apps SDK - Layers API

Build immersive visual experiences in Zoom meetings.

## Overview

The Layers API allows you to render custom visuals that overlay on the meeting video feed.

## Getting Started

```javascript
// sdk = window.zoomSdk (see apis.md for initialization)
```

### 1. Request Capability

```javascript
await sdk.config({
  capabilities: ['runRenderingContext'],
  version: '0.16'
});
```

### 2. Start Rendering Context

```javascript
await sdk.runRenderingContext({
  view: 'immersive'
});
```

### 3. Draw on Canvas

```javascript
sdk.addEventListener('onRenderingContextChange', (event) => {
  const { canvas, context } = event;
  
  // Draw your content
  context.fillStyle = 'rgba(255, 0, 0, 0.5)';
  context.fillRect(0, 0, canvas.width, canvas.height);
});
```

## Use Cases

- Virtual backgrounds with custom elements
- Interactive annotations
- Gamification overlays
- Branding and watermarks
- Live reactions and effects

## Rendering Modes

| Mode | Description |
|------|-------------|
| `immersive` | Full-screen overlay |
| `camera` | Overlay on user's camera feed |

## Best Practices

1. Keep rendering performant (60fps target)
2. Test on various screen sizes
3. Provide controls to disable/enable effects
4. Consider accessibility

## Resources

- **Layers API docs**: https://developers.zoom.us/docs/zoom-apps/guides/layers/

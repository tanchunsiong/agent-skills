# RTMS - Media Types

Audio, video, and transcript data formats.

## Overview

RTMS delivers three types of media data over WebSocket.

## Audio

| Property | Value |
|----------|-------|
| Format | PCM |
| Bit depth | 16-bit |
| Sample rate | 16000 Hz or 32000 Hz |
| Channels | Mono or Stereo |

### Processing Audio

```javascript
function processAudio(audioBuffer) {
  // audioBuffer contains PCM 16-bit samples
  // Convert to your preferred format for processing
  
  // Example: Send to speech-to-text service
  transcriptionService.process(audioBuffer);
}
```

## Video

| Property | Value |
|----------|-------|
| Codec | H.264 |
| Container | Raw NAL units |
| Resolution | Variable (up to 1080p) |

### Processing Video

```javascript
function processVideo(videoFrame) {
  // videoFrame contains H.264 encoded data
  // Decode with FFmpeg or similar
  
  // Example: Extract frames for analysis
  videoDecoder.decode(videoFrame);
}
```

## Transcript

| Property | Value |
|----------|-------|
| Format | JSON |
| Content | Real-time speech-to-text |

### Transcript Structure

```json
{
  "type": "transcript",
  "data": {
    "user_id": "user_id",
    "user_name": "Speaker Name",
    "text": "Transcribed text content",
    "timestamp": 1234567890,
    "is_final": true
  }
}
```

### Processing Transcript

```javascript
function processTranscript(transcript) {
  const { user_name, text, is_final } = transcript.data;
  
  if (is_final) {
    // Final transcription for this segment
    saveTranscript(user_name, text);
  } else {
    // Interim result, may change
    updateLiveCaption(user_name, text);
  }
}
```

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/

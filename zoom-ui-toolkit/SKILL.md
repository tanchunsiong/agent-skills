---
name: zoom-ui-toolkit
description: |
  Zoom UI Toolkit guide for building video applications with pre-built UI components. Covers
  the React component library for Video SDK integrations including video tiles, controls,
  chat, and participant management. Use when building custom video experiences with less code.
---

# Zoom UI Toolkit

Pre-built React components for building video applications with Zoom Video SDK.

## Overview

Zoom UI Toolkit provides:
- Ready-to-use video conferencing components
- Consistent Zoom-like UI/UX
- React component library
- Customizable themes and styles
- Accessibility built-in
- Mobile-responsive design

## Key Features

| Feature | Description |
|---------|-------------|
| **Video Tiles** | Display participant video feeds |
| **Controls Bar** | Audio, video, screen share controls |
| **Participant List** | View and manage participants |
| **Chat Panel** | In-session messaging |
| **Screen Share** | View shared screens |
| **Settings** | Audio/video device selection |

## Installation

```bash
# Install UI Toolkit
npm install @zoom/videosdk-ui-toolkit

# Peer dependencies
npm install @zoom/videosdk react react-dom
```

## Quick Start

### Basic Video Session

```jsx
import { UIToolkit } from '@zoom/videosdk-ui-toolkit';
import '@zoom/videosdk-ui-toolkit/dist/videosdk-ui-toolkit.css';

function VideoApp() {
  const sessionConfig = {
    videoSDKJWT: 'your_jwt_token',
    sessionName: 'my-session',
    userName: 'User Name',
    features: ['video', 'audio', 'share', 'chat']
  };

  return (
    <UIToolkit
      config={sessionConfig}
      onSessionJoined={() => console.log('Joined!')}
      onSessionLeft={() => console.log('Left!')}
    />
  );
}
```

### Custom Layout

```jsx
import {
  VideoTile,
  ControlBar,
  ParticipantList,
  ChatPanel
} from '@zoom/videosdk-ui-toolkit';

function CustomVideoApp() {
  return (
    <div className="video-container">
      <div className="main-content">
        <VideoTile participantId="self" />
        <div className="gallery">
          <VideoTile participantId="participant-1" />
          <VideoTile participantId="participant-2" />
        </div>
      </div>
      
      <aside className="sidebar">
        <ParticipantList />
        <ChatPanel />
      </aside>
      
      <footer>
        <ControlBar />
      </footer>
    </div>
  );
}
```

## Core Components

### UIToolkit (All-in-One)

```jsx
<UIToolkit
  config={{
    videoSDKJWT: 'jwt_token',
    sessionName: 'session-123',
    userName: 'John Doe',
    features: ['video', 'audio', 'share', 'chat', 'users']
  }}
  onSessionJoined={handleJoin}
  onSessionLeft={handleLeave}
  onError={handleError}
/>
```

### VideoTile

```jsx
// Self video
<VideoTile participantId="self" mirrored={true} />

// Remote participant
<VideoTile 
  participantId={participant.id}
  showName={true}
  showAudioIndicator={true}
/>

// Active speaker highlight
<VideoTile 
  participantId={activeSpeaker.id}
  highlighted={true}
/>
```

### ControlBar

```jsx
<ControlBar
  buttons={[
    'audio',      // Mute/unmute
    'video',      // Camera on/off
    'share',      // Screen share
    'chat',       // Toggle chat
    'users',      // Participant list
    'settings',   // Device settings
    'leave'       // Leave session
  ]}
  position="bottom"  // 'top' | 'bottom'
  onLeave={handleLeave}
/>
```

### ParticipantList

```jsx
<ParticipantList
  showSearch={true}
  showRoles={true}
  onParticipantClick={(participant) => {
    console.log('Selected:', participant);
  }}
/>
```

### ChatPanel

```jsx
<ChatPanel
  showTimestamps={true}
  showSenderName={true}
  maxMessages={100}
  onSendMessage={(message) => {
    console.log('Sent:', message);
  }}
/>
```

## Customization

### Theming

```jsx
import { ThemeProvider } from '@zoom/videosdk-ui-toolkit';

const customTheme = {
  colors: {
    primary: '#0E72ED',
    secondary: '#2D8CFF',
    background: '#1A1A1A',
    surface: '#262626',
    text: '#FFFFFF',
    textSecondary: '#AAAAAA',
    error: '#E02828',
    success: '#2D8000'
  },
  borderRadius: '8px',
  fontFamily: 'Inter, sans-serif'
};

function App() {
  return (
    <ThemeProvider theme={customTheme}>
      <UIToolkit config={sessionConfig} />
    </ThemeProvider>
  );
}
```

### Custom Control Buttons

```jsx
<ControlBar
  buttons={['audio', 'video', 'share']}
  customButtons={[
    {
      id: 'record',
      icon: <RecordIcon />,
      label: 'Record',
      onClick: handleRecord
    },
    {
      id: 'reactions',
      icon: <ReactionIcon />,
      label: 'Reactions',
      onClick: showReactions
    }
  ]}
/>
```

### Layout Modes

```jsx
// Gallery view (grid)
<VideoGallery 
  layout="gallery"
  maxTilesPerPage={25}
/>

// Speaker view (active speaker large)
<VideoGallery 
  layout="speaker"
  showThumbnails={true}
/>

// Side-by-side
<VideoGallery 
  layout="side-by-side"
/>
```

## Event Handling

```jsx
<UIToolkit
  config={sessionConfig}
  // Session events
  onSessionJoined={(session) => {
    console.log('Joined session:', session.sessionName);
  }}
  onSessionLeft={() => {
    navigate('/');
  }}
  
  // Participant events
  onParticipantJoined={(participant) => {
    showNotification(`${participant.displayName} joined`);
  }}
  onParticipantLeft={(participant) => {
    showNotification(`${participant.displayName} left`);
  }}
  
  // Media events
  onAudioMuted={(muted) => {
    console.log('Audio muted:', muted);
  }}
  onVideoStarted={(started) => {
    console.log('Video started:', started);
  }}
  
  // Error handling
  onError={(error) => {
    console.error('Error:', error);
    showErrorModal(error.message);
  }}
/>
```

## Hooks

### useSession

```jsx
import { useSession } from '@zoom/videosdk-ui-toolkit';

function MyComponent() {
  const { 
    session,
    participants,
    localParticipant,
    isConnected 
  } = useSession();

  return (
    <div>
      <p>Session: {session?.sessionName}</p>
      <p>Participants: {participants.length}</p>
    </div>
  );
}
```

### useAudio

```jsx
import { useAudio } from '@zoom/videosdk-ui-toolkit';

function AudioControls() {
  const { 
    isMuted, 
    toggleMute, 
    audioDevices,
    selectAudioDevice 
  } = useAudio();

  return (
    <button onClick={toggleMute}>
      {isMuted ? 'Unmute' : 'Mute'}
    </button>
  );
}
```

### useVideo

```jsx
import { useVideo } from '@zoom/videosdk-ui-toolkit';

function VideoControls() {
  const { 
    isVideoOn, 
    toggleVideo, 
    videoDevices,
    selectVideoDevice 
  } = useVideo();

  return (
    <button onClick={toggleVideo}>
      {isVideoOn ? 'Stop Video' : 'Start Video'}
    </button>
  );
}
```

## Prerequisites

1. **Zoom Video SDK account** - Get credentials at [Zoom Marketplace](https://marketplace.zoom.us/)
2. **Video SDK JWT** - Generate session tokens server-side
3. **React 17+** - Component library requirement
4. **Modern browser** - WebRTC support required

## Common Use Cases

| Use Case | Components | Description |
|----------|------------|-------------|
| **Video Meeting** | UIToolkit | Full-featured video conferencing |
| **Telehealth** | Custom layout | HIPAA-compliant video visits |
| **Virtual Events** | Speaker view | Webinar-style presentations |
| **Education** | Gallery + Chat | Virtual classroom |
| **Customer Support** | Video + Chat | Video support sessions |

## Browser Support

| Browser | Version |
|---------|---------|
| Chrome | 78+ |
| Firefox | 76+ |
| Safari | 14.1+ |
| Edge | 79+ |

## Accessibility

UI Toolkit includes:
- Keyboard navigation
- Screen reader support
- High contrast mode
- Focus indicators
- ARIA labels

## Resources

- **UI Toolkit Guide**: https://developers.zoom.us/docs/video-sdk/web/ui-toolkit/
- **Video SDK Documentation**: https://developers.zoom.us/docs/video-sdk/
- **Component Reference**: https://developers.zoom.us/docs/video-sdk/web/ui-toolkit/components/
- **Sample App**: https://github.com/zoom/videosdk-ui-toolkit-react-sample
- **Marketplace**: https://marketplace.zoom.us/

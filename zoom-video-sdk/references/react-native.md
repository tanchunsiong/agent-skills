# Video SDK - React Native

Cross-platform video applications with React Native.

## Overview

React Native wrapper for building custom video applications on iOS and Android.

## Prerequisites

- React Native 0.60+
- iOS 12+ / Android API 21+
- Valid SDK credentials from [Marketplace](https://marketplace.zoom.us/) (sign-in required)

## Installation

```bash
npm install @zoom/react-native-videosdk
```

## Quick Start

```javascript
import { ZoomVideoSdkProvider, useZoom } from '@zoom/react-native-videosdk';

function App() {
  return (
    <ZoomVideoSdkProvider
      config={{
        domain: 'zoom.us',
      }}
    >
      <VideoSession />
    </ZoomVideoSdkProvider>
  );
}

function VideoSession() {
  const zoom = useZoom();
  
  const joinSession = async () => {
    await zoom.joinSession({
      sessionName: 'MySession',
      userName: 'User',
      token: signature,
    });
  };
  
  return (
    // Your UI
  );
}
```

## Event Handling

```javascript
useEffect(() => {
  const listener = zoom.addListener('onSessionJoin', () => {
    console.log('Joined session');
  });
  
  return () => listener.remove();
}, []);
```

## Common Tasks

### Component Integration

```javascript
import React, { useState, useEffect } from 'react';
import { View, StyleSheet } from 'react-native';
import {
  ZoomVideoSdkProvider,
  useZoom,
  ZoomView,
  VideoAspect,
} from '@zoom/react-native-videosdk';

function App() {
  return (
    <ZoomVideoSdkProvider config={{ domain: 'zoom.us' }}>
      <VideoSession />
    </ZoomVideoSdkProvider>
  );
}

function VideoSession() {
  const zoom = useZoom();
  const [participants, setParticipants] = useState([]);
  const [isJoined, setIsJoined] = useState(false);
  
  useEffect(() => {
    const listeners = [
      zoom.addListener('onSessionJoin', () => {
        setIsJoined(true);
      }),
      zoom.addListener('onUserJoin', ({ users }) => {
        setParticipants(prev => [...prev, ...users]);
      }),
      zoom.addListener('onUserLeave', ({ users }) => {
        setParticipants(prev => 
          prev.filter(p => !users.find(u => u.odId === p.userId))
        );
      }),
    ];
    
    return () => listeners.forEach(l => l.remove());
  }, [zoom]);
  
  const joinSession = async () => {
    try {
      await zoom.joinSession({
        sessionName: 'MySession',
        userName: 'React Native User',
        token: await getSignature(),
      });
    } catch (error) {
      console.error('Join failed:', error);
    }
  };
  
  return (
    <View style={styles.container}>
      {isJoined ? (
        <>
          <ZoomView
            style={styles.myVideo}
            userId={zoom.session.mySelf?.odId}
            videoAspect={VideoAspect.PanAndScan}
          />
          <View style={styles.participantStrip}>
            {participants.map(user => (
              <ZoomView
                key={user.odId}
                style={styles.thumbnail}
                userId={user.odId}
                videoAspect={VideoAspect.LetterBox}
              />
            ))}
          </View>
        </>
      ) : (
        <Button title="Join" onPress={joinSession} />
      )}
    </View>
  );
}
```

### Video Rendering Views

```javascript
import { ZoomView, VideoAspect } from '@zoom/react-native-videosdk';

// Full video view
function FullVideoView({ userId }) {
  return (
    <ZoomView
      style={{ flex: 1 }}
      userId={userId}
      videoAspect={VideoAspect.PanAndScan}
      resolution="720p"
    />
  );
}

// Gallery view with grid layout
function GalleryView({ participants, columns = 2 }) {
  return (
    <View style={styles.galleryContainer}>
      {participants.map((user, index) => (
        <ZoomView
          key={user.odId}
          style={[
            styles.galleryItem,
            { width: `${100 / columns}%` }
          ]}
          userId={user.odId}
          videoAspect={VideoAspect.LetterBox}
          resolution="360p"
        />
      ))}
    </View>
  );
}

// Screen share view
function ScreenShareView() {
  const zoom = useZoom();
  const [sharingUser, setSharingUser] = useState(null);
  
  useEffect(() => {
    const listener = zoom.addListener('onUserShareStatusChanged', ({ user, status }) => {
      if (status === 'started') {
        setSharingUser(user);
      } else {
        setSharingUser(null);
      }
    });
    return () => listener.remove();
  }, [zoom]);
  
  if (!sharingUser) return null;
  
  return (
    <ZoomView
      style={styles.screenShare}
      userId={sharingUser.odId}
      sharing={true}
      videoAspect={VideoAspect.LetterBox}
    />
  );
}
```

### Native Module Bridging

```javascript
// Access native functionality via zoom SDK
const zoom = useZoom();

// Audio controls
async function toggleAudio() {
  const audioHelper = zoom.audioHelper;
  const isMuted = await audioHelper.isMuted();
  
  if (isMuted) {
    await audioHelper.unmuteAudio();
  } else {
    await audioHelper.muteAudio();
  }
}

// Video controls
async function toggleVideo() {
  const videoHelper = zoom.videoHelper;
  const isOn = await videoHelper.isMyVideoOn();
  
  if (isOn) {
    await videoHelper.stopVideo();
  } else {
    await videoHelper.startVideo();
  }
}

// Camera switch
async function switchCamera() {
  const videoHelper = zoom.videoHelper;
  await videoHelper.switchCamera();
}

// Get device list
async function getDevices() {
  const cameras = await zoom.videoHelper.getCameraList();
  const mics = await zoom.audioHelper.getMicList();
  const speakers = await zoom.audioHelper.getSpeakerList();
  
  return { cameras, mics, speakers };
}
```

### Platform Setup

**iOS (ios/Podfile)**:
```ruby
platform :ios, '12.0'

post_install do |installer|
  installer.pods_project.targets.each do |target|
    target.build_configurations.each do |config|
      config.build_settings['ENABLE_BITCODE'] = 'NO'
    end
  end
end
```

**iOS (Info.plist)**:
```xml
<key>NSCameraUsageDescription</key>
<string>Camera for video calls</string>
<key>NSMicrophoneUsageDescription</key>
<string>Microphone for audio</string>
```

**Android (android/app/build.gradle)**:
```gradle
android {
    defaultConfig {
        minSdkVersion 21
    }
}
```

**Android (AndroidManifest.xml)**:
```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.INTERNET" />
```

## Resources

- **React Native SDK**: https://www.npmjs.com/package/@zoom/react-native-videosdk
- **Video SDK docs**: https://developers.zoom.us/docs/video-sdk/
- **Sample app**: https://github.com/nicholasyiu/zoom-videosdk-react-native-sample

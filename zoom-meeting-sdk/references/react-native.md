# Meeting SDK - React Native

Cross-platform meeting applications with React Native.

## Overview

React Native wrapper for embedding Zoom meetings on iOS and Android.

## Prerequisites

- React Native 0.60+
- iOS 12+ / Android API 21+
- Valid SDK credentials from [Marketplace](https://marketplace.zoom.us/) (sign-in required)

## Installation

```bash
npm install @zoom/react-native-meetingsdk
```

## Quick Start

```javascript
import { ZoomSDK } from '@zoom/react-native-meetingsdk';

// Initialize
await ZoomSDK.initialize({
  sdkKey: SDK_KEY,
  sdkSecret: SDK_SECRET,
});

// Join meeting
await ZoomSDK.joinMeeting({
  meetingNumber: meetingNumber,
  userName: 'User',
  password: password,
});
```

## Event Handling

```javascript
useEffect(() => {
  const listener = ZoomSDK.addListener('meetingStatusChanged', (status) => {
    console.log('Meeting status:', status);
  });
  
  return () => listener.remove();
}, []);
```

## Common Tasks

### Component Integration

```javascript
import React, { useEffect, useState } from 'react';
import { View, Button, StyleSheet } from 'react-native';
import { ZoomSDK } from '@zoom/react-native-meetingsdk';

function MeetingScreen({ meetingNumber, password }) {
  const [isInMeeting, setIsInMeeting] = useState(false);
  
  useEffect(() => {
    // Initialize SDK
    ZoomSDK.initialize({
      sdkKey: SDK_KEY,
      sdkSecret: SDK_SECRET,
    });
    
    // Listen for meeting status
    const listener = ZoomSDK.addListener('meetingStatusChanged', (status) => {
      switch (status) {
        case 'MEETING_STATUS_INMEETING':
          setIsInMeeting(true);
          break;
        case 'MEETING_STATUS_ENDED':
        case 'MEETING_STATUS_FAILED':
          setIsInMeeting(false);
          break;
      }
    });
    
    return () => listener.remove();
  }, []);
  
  const joinMeeting = async () => {
    try {
      await ZoomSDK.joinMeeting({
        meetingNumber: meetingNumber,
        userName: 'User',
        password: password,
      });
    } catch (error) {
      console.error('Join failed:', error);
    }
  };
  
  const leaveMeeting = async () => {
    await ZoomSDK.leaveMeeting();
  };
  
  return (
    <View style={styles.container}>
      {!isInMeeting ? (
        <Button title="Join Meeting" onPress={joinMeeting} />
      ) : (
        <Button title="Leave Meeting" onPress={leaveMeeting} />
      )}
    </View>
  );
}
```

### Navigation Handling

```javascript
import { useNavigation } from '@react-navigation/native';

function MeetingLauncher() {
  const navigation = useNavigation();
  
  useEffect(() => {
    const listener = ZoomSDK.addListener('meetingStatusChanged', (status) => {
      if (status === 'MEETING_STATUS_ENDED') {
        // Navigate back when meeting ends
        navigation.goBack();
      }
    });
    
    return () => listener.remove();
  }, [navigation]);
  
  const startMeeting = async () => {
    // Navigate to meeting screen
    navigation.navigate('Meeting');
    
    // Then join
    await ZoomSDK.joinMeeting({
      meetingNumber: '123456789',
      password: 'password',
      userName: 'User',
    });
  };
  
  return <Button title="Start Meeting" onPress={startMeeting} />;
}
```

### Platform-Specific Setup

**iOS Setup (ios/Podfile)**:
```ruby
platform :ios, '12.0'

target 'YourApp' do
  pod 'ZoomSDK', :path => '../node_modules/@zoom/react-native-meetingsdk'
end
```

**iOS Permissions (Info.plist)**:
```xml
<key>NSCameraUsageDescription</key>
<string>Camera for video meetings</string>
<key>NSMicrophoneUsageDescription</key>
<string>Microphone for audio</string>
```

**Android Setup (android/app/build.gradle)**:
```gradle
android {
    defaultConfig {
        minSdkVersion 21
    }
}
```

**Android Permissions (AndroidManifest.xml)**:
```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.INTERNET" />
```

### Audio/Video Controls

```javascript
// Mute/unmute audio
async function toggleAudio() {
  const isMuted = await ZoomSDK.isMyAudioMuted();
  if (isMuted) {
    await ZoomSDK.unmuteMyAudio();
  } else {
    await ZoomSDK.muteMyAudio();
  }
}

// Start/stop video
async function toggleVideo() {
  const isVideoOff = await ZoomSDK.isMyVideoMuted();
  if (isVideoOff) {
    await ZoomSDK.unmuteMyVideo();
  } else {
    await ZoomSDK.muteMyVideo();
  }
}

// Switch camera
async function switchCamera() {
  await ZoomSDK.switchCamera();
}
```

## Resources

- **React Native SDK**: https://developers.zoom.us/docs/meeting-sdk/react-native/
- **Sample app**: https://github.com/nicholasyiu/react-native-zoom-sdk-sample

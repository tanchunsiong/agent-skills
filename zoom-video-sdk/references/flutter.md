# Video SDK - Flutter

Cross-platform video applications with Flutter.

## Overview

Flutter plugin for building custom video applications on iOS and Android from a single codebase.

## Prerequisites

- Video SDK Flutter plugin
- Flutter 2.0+
- iOS 12+ / Android API 21+
- Valid SDK credentials from [Marketplace](https://marketplace.zoom.us/) (sign-in required)

## Installation

```yaml
dependencies:
  zoom_videosdk: ^1.0.0
```

## Quick Start

```dart
import 'package:zoom_videosdk/zoom_videosdk.dart';

// Initialize
await ZoomVideoSdk.initSdk(ZoomVideoSdkInitParams(
  domain: 'zoom.us',
));

// Join session
await ZoomVideoSdk.joinSession(ZoomVideoSdkSessionContext(
  sessionName: 'MySession',
  userName: 'User',
  token: signature,
));
```

## Event Handling

```dart
ZoomVideoSdk.onSessionJoin.listen((event) {
  print('Joined session');
});

ZoomVideoSdk.onUserJoin.listen((users) {
  print('Users joined: $users');
});

ZoomVideoSdk.onUserLeave.listen((users) {
  print('Users left: $users');
});
```

## Common Tasks

### Widget Integration

```dart
import 'package:flutter/material.dart';
import 'package:zoom_videosdk/zoom_videosdk.dart';

class VideoSessionScreen extends StatefulWidget {
  @override
  _VideoSessionScreenState createState() => _VideoSessionScreenState();
}

class _VideoSessionScreenState extends State<VideoSessionScreen> {
  List<ZoomVideoSdkUser> participants = [];
  
  @override
  void initState() {
    super.initState();
    _setupListeners();
    _joinSession();
  }
  
  void _setupListeners() {
    ZoomVideoSdk.onUserJoin.listen((users) {
      setState(() {
        participants.addAll(users);
      });
    });
    
    ZoomVideoSdk.onUserLeave.listen((users) {
      setState(() {
        participants.removeWhere((p) => users.contains(p));
      });
    });
  }
  
  Future<void> _joinSession() async {
    await ZoomVideoSdk.joinSession(ZoomVideoSdkSessionContext(
      sessionName: 'MySession',
      userName: 'Flutter User',
      token: await getSignature(),
    ));
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          // My video
          Expanded(
            flex: 2,
            child: ZoomVideoView(
              user: ZoomVideoSdk.session?.mySelf,
            ),
          ),
          // Participant videos
          Expanded(
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              itemCount: participants.length,
              itemBuilder: (context, index) {
                return SizedBox(
                  width: 160,
                  child: ZoomVideoView(
                    user: participants[index],
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
```

### Video Rendering

```dart
// Custom video view widget
class ZoomVideoView extends StatelessWidget {
  final ZoomVideoSdkUser? user;
  final ZoomVideoSdkResolution resolution;
  
  const ZoomVideoView({
    Key? key,
    required this.user,
    this.resolution = ZoomVideoSdkResolution.resolution_720P,
  }) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    if (user == null) {
      return Container(color: Colors.black);
    }
    
    return ZoomVideoSdkVideoView(
      user: user!,
      resolution: resolution,
      aspectMode: ZoomVideoSdkVideoAspect.letterBox,
    );
  }
}

// Toggle video
Future<void> toggleVideo() async {
  final videoHelper = ZoomVideoSdk.videoHelper;
  if (await videoHelper.isMyVideoOn()) {
    await videoHelper.stopVideo();
  } else {
    await videoHelper.startVideo();
  }
}

// Toggle audio
Future<void> toggleAudio() async {
  final audioHelper = ZoomVideoSdk.audioHelper;
  if (await audioHelper.isMuted()) {
    await audioHelper.unmuteAudio();
  } else {
    await audioHelper.muteAudio();
  }
}
```

### Cross-Platform Considerations

```dart
import 'dart:io';

class PlatformConfig {
  // Platform-specific initialization
  static ZoomVideoSdkInitParams getInitParams() {
    return ZoomVideoSdkInitParams(
      domain: 'zoom.us',
      enableLog: true,
      // iOS-specific
      logFilePrefix: Platform.isIOS ? 'zoom_ios' : 'zoom_android',
    );
  }
  
  // Handle platform differences
  static Future<void> requestPermissions() async {
    if (Platform.isAndroid) {
      // Android requires explicit permission request
      await Permission.camera.request();
      await Permission.microphone.request();
    }
    // iOS permissions are requested automatically via Info.plist
  }
  
  // Platform-specific UI adjustments
  static EdgeInsets getSafeAreaPadding(BuildContext context) {
    final padding = MediaQuery.of(context).padding;
    // iOS notch handling
    if (Platform.isIOS) {
      return EdgeInsets.only(top: padding.top, bottom: padding.bottom);
    }
    return EdgeInsets.zero;
  }
}

// iOS Info.plist additions required:
// NSCameraUsageDescription
// NSMicrophoneUsageDescription

// Android AndroidManifest.xml additions required:
// <uses-permission android:name="android.permission.CAMERA" />
// <uses-permission android:name="android.permission.RECORD_AUDIO" />
// <uses-permission android:name="android.permission.INTERNET" />
```

### State Management (with Provider)

```dart
class ZoomSessionProvider extends ChangeNotifier {
  bool _isConnected = false;
  List<ZoomVideoSdkUser> _participants = [];
  
  bool get isConnected => _isConnected;
  List<ZoomVideoSdkUser> get participants => _participants;
  
  ZoomSessionProvider() {
    _setupListeners();
  }
  
  void _setupListeners() {
    ZoomVideoSdk.onSessionJoin.listen((_) {
      _isConnected = true;
      notifyListeners();
    });
    
    ZoomVideoSdk.onSessionLeave.listen((_) {
      _isConnected = false;
      _participants.clear();
      notifyListeners();
    });
    
    ZoomVideoSdk.onUserJoin.listen((users) {
      _participants.addAll(users);
      notifyListeners();
    });
    
    ZoomVideoSdk.onUserLeave.listen((users) {
      _participants.removeWhere((p) => users.contains(p));
      notifyListeners();
    });
  }
}
```

## Resources

- **Flutter plugin**: https://pub.dev/packages/zoom_videosdk
- **Video SDK docs**: https://developers.zoom.us/docs/video-sdk/
- **Sample app**: https://github.com/nicholasyiu/zoom-videosdk-flutter-sample

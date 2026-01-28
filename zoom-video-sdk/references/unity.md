# Video SDK - Unity

Video experiences in Unity games and applications.

## Overview

Unity plugin for integrating Zoom Video SDK into games and interactive applications.

## Prerequisites

- Video SDK Unity plugin from [Marketplace](https://marketplace.zoom.us/) (sign-in required)
- Unity 2019.4+
- Valid SDK credentials

## Installation

1. Download Unity plugin from Marketplace (requires sign-in)
2. Import package into Unity project
3. Configure platform settings

## Quick Start

```csharp
using ZoomVideoSDK;

public class VideoManager : MonoBehaviour
{
    void Start()
    {
        // Initialize
        var initParams = new ZoomVideoSDKInitParams
        {
            domain = "zoom.us"
        };
        ZoomVideoSDK.Instance.Initialize(initParams);
    }
    
    public void JoinSession()
    {
        var context = new ZoomVideoSDKSessionContext
        {
            sessionName = "MySession",
            userName = "Player",
            token = signature
        };
        ZoomVideoSDK.Instance.JoinSession(context);
    }
}
```

## Event Handling

```csharp
void OnEnable()
{
    ZoomVideoSDK.Instance.OnSessionJoin += OnSessionJoin;
    ZoomVideoSDK.Instance.OnUserJoin += OnUserJoin;
}

void OnSessionJoin()
{
    Debug.Log("Joined session");
}

void OnUserJoin(ZoomVideoSDKUser[] users)
{
    Debug.Log($"Users joined: {users.Length}");
}
```

## Common Tasks

### Rendering to Textures

```csharp
using UnityEngine;
using ZoomVideoSDK;

public class VideoRenderer : MonoBehaviour
{
    public RawImage videoDisplay;
    private Texture2D videoTexture;
    private ZoomVideoSDKUser currentUser;
    
    void Start()
    {
        // Create texture for video rendering
        videoTexture = new Texture2D(1280, 720, TextureFormat.RGBA32, false);
        videoDisplay.texture = videoTexture;
    }
    
    public void AttachUser(ZoomVideoSDKUser user)
    {
        currentUser = user;
        // Subscribe to user's video
        var videoCanvas = user.GetVideoCanvas();
        videoCanvas.Subscribe(ZoomVideoSDKResolution._720P);
        videoCanvas.OnRawDataFrameReceived += OnVideoFrame;
    }
    
    void OnVideoFrame(YUVRawDataI420 rawData)
    {
        // Convert YUV to RGB
        byte[] rgbData = ConvertI420ToRGBA(
            rawData.GetBuffer(),
            rawData.GetStreamWidth(),
            rawData.GetStreamHeight()
        );
        
        // Update texture on main thread
        MainThreadDispatcher.Enqueue(() =>
        {
            videoTexture.Resize(rawData.GetStreamWidth(), rawData.GetStreamHeight());
            videoTexture.LoadRawTextureData(rgbData);
            videoTexture.Apply();
        });
    }
    
    private byte[] ConvertI420ToRGBA(byte[] yuv, int width, int height)
    {
        // YUV to RGBA conversion
        byte[] rgba = new byte[width * height * 4];
        // ... conversion logic
        return rgba;
    }
}
```

### Game Object Integration

```csharp
public class VideoGameObject : MonoBehaviour
{
    public Material videoMaterial;
    private Texture2D videoTexture;
    
    void Start()
    {
        // Create texture
        videoTexture = new Texture2D(640, 360, TextureFormat.RGBA32, false);
        
        // Apply to material
        videoMaterial.mainTexture = videoTexture;
        
        // Apply material to renderer
        GetComponent<Renderer>().material = videoMaterial;
    }
    
    public void SetUser(ZoomVideoSDKUser user)
    {
        var canvas = user.GetVideoCanvas();
        canvas.Subscribe(ZoomVideoSDKResolution._360P);
        canvas.OnRawDataFrameReceived += UpdateTexture;
    }
    
    void UpdateTexture(YUVRawDataI420 data)
    {
        // Update texture...
    }
}

// Usage: Attach video to a 3D object in your scene
public class VideoWall : MonoBehaviour
{
    public VideoGameObject[] videoScreens;
    private List<ZoomVideoSDKUser> participants = new List<ZoomVideoSDKUser>();
    
    void OnEnable()
    {
        ZoomVideoSDK.Instance.OnUserJoin += OnUserJoin;
        ZoomVideoSDK.Instance.OnUserLeave += OnUserLeave;
    }
    
    void OnUserJoin(ZoomVideoSDKUser[] users)
    {
        foreach (var user in users)
        {
            participants.Add(user);
            AssignToScreen(user);
        }
    }
    
    void AssignToScreen(ZoomVideoSDKUser user)
    {
        int index = participants.IndexOf(user);
        if (index < videoScreens.Length)
        {
            videoScreens[index].SetUser(user);
        }
    }
}
```

### Platform Builds (iOS, Android, Desktop)

```csharp
// Platform-specific configuration
public class PlatformConfig
{
    public static ZoomVideoSDKInitParams GetInitParams()
    {
        var initParams = new ZoomVideoSDKInitParams
        {
            domain = "zoom.us",
            enableLog = true
        };
        
        #if UNITY_IOS
        // iOS-specific settings
        initParams.appGroupId = "group.com.yourcompany.app";
        #endif
        
        #if UNITY_ANDROID
        // Android-specific settings
        initParams.logFilePrefix = "zoom_unity_android";
        #endif
        
        return initParams;
    }
    
    public static void RequestPermissions()
    {
        #if UNITY_ANDROID && !UNITY_EDITOR
        // Android runtime permissions
        if (!UnityEngine.Android.Permission.HasUserAuthorizedPermission(
            UnityEngine.Android.Permission.Camera))
        {
            UnityEngine.Android.Permission.RequestUserPermission(
                UnityEngine.Android.Permission.Camera);
        }
        if (!UnityEngine.Android.Permission.HasUserAuthorizedPermission(
            UnityEngine.Android.Permission.Microphone))
        {
            UnityEngine.Android.Permission.RequestUserPermission(
                UnityEngine.Android.Permission.Microphone);
        }
        #endif
    }
}

// Build settings in Unity:
// iOS: 
//   - Add NSCameraUsageDescription and NSMicrophoneUsageDescription to Info.plist
//   - Enable Background Modes > Audio if needed
// Android:
//   - Min API Level 21
//   - Add CAMERA, RECORD_AUDIO, INTERNET permissions to manifest
// Desktop:
//   - Include SDK DLLs in build
```

### Main Thread Dispatcher

```csharp
// Unity requires UI updates on main thread
public class MainThreadDispatcher : MonoBehaviour
{
    private static MainThreadDispatcher instance;
    private Queue<System.Action> actions = new Queue<System.Action>();
    
    void Awake()
    {
        if (instance == null)
        {
            instance = this;
            DontDestroyOnLoad(gameObject);
        }
    }
    
    public static void Enqueue(System.Action action)
    {
        lock (instance.actions)
        {
            instance.actions.Enqueue(action);
        }
    }
    
    void Update()
    {
        lock (actions)
        {
            while (actions.Count > 0)
            {
                actions.Dequeue().Invoke();
            }
        }
    }
}
```

## Resources

- **Video SDK docs**: https://developers.zoom.us/docs/video-sdk/
- **Unity integration guide**: https://developers.zoom.us/docs/video-sdk/unity/

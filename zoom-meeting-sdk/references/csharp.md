# Meeting SDK - C# / .NET

C# wrapper for Windows Meeting SDK integration in .NET applications.

## Overview

The C# wrapper provides managed .NET bindings over the native Windows SDK, enabling integration with WPF, WinForms, and other .NET applications.

## Prerequisites

- Meeting SDK C# Wrapper downloaded from [Marketplace](https://marketplace.zoom.us/) (sign-in required)
- Visual Studio 2019+ with .NET development workload
- .NET Framework 4.7.2+ or .NET 6.0+
- Windows 10+
- Valid SDK credentials

## Installation

1. Download the C# wrapper from Marketplace (requires sign-in)
2. Add the following references to your project:
   - `zoom_sdk_dotnet_wrap.dll`
   - Native SDK DLLs (copy to output directory)

```xml
<!-- In .csproj -->
<ItemGroup>
  <Reference Include="zoom_sdk_dotnet_wrap">
    <HintPath>lib\zoom_sdk_dotnet_wrap.dll</HintPath>
  </Reference>
</ItemGroup>

<!-- Copy native DLLs -->
<ItemGroup>
  <Content Include="lib\*.dll">
    <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
  </Content>
</ItemGroup>
```

## Quick Start

```csharp
using ZOOM_SDK_DOTNET_WRAP;

public class ZoomManager
{
    private CZoomSDKDotNetWrap _sdk;
    
    public void Initialize()
    {
        _sdk = CZoomSDKDotNetWrap.Instance;
        
        var initParam = new InitParam
        {
            web_domain = "zoom.us",
            enable_log = true,
            config_opts = new ConfigurableOptions
            {
                optionalFeatures = 0
            }
        };
        
        var result = _sdk.Initialize(initParam);
        if (result == SDKError.SDKERR_SUCCESS)
        {
            Console.WriteLine("SDK initialized successfully");
        }
    }
}
```

## Authentication

```csharp
public class AuthManager
{
    public void AuthenticateWithJWT(string jwtToken)
    {
        var authService = CZoomSDKDotNetWrap.Instance.GetAuthServiceWrap();
        
        // Set up auth event handler
        authService.Add_CB_onAuthenticationReturn(OnAuthResult);
        
        // Authenticate
        var authContext = new AuthContext
        {
            jwt_token = jwtToken
        };
        
        var result = authService.SDKAuth(authContext);
        if (result != SDKError.SDKERR_SUCCESS)
        {
            Console.WriteLine($"Auth failed: {result}");
        }
    }
    
    private void OnAuthResult(AuthResult result)
    {
        if (result == AuthResult.AUTHRET_SUCCESS)
        {
            Console.WriteLine("Authentication successful");
        }
        else
        {
            Console.WriteLine($"Authentication failed: {result}");
        }
    }
}
```

## Join Meeting

```csharp
public class MeetingManager
{
    public void JoinMeeting(string meetingNumber, string password, string displayName)
    {
        var meetingService = CZoomSDKDotNetWrap.Instance.GetMeetingServiceWrap();
        
        // Set up meeting event handlers
        meetingService.Add_CB_onMeetingStatusChanged(OnMeetingStatusChanged);
        
        var joinParam = new JoinParam
        {
            userType = SDKUserType.SDK_UT_WITHOUT_LOGIN,
            
        };
        
        var normalJoin = new JoinParam4WithoutLogin
        {
            meetingNumber = ulong.Parse(meetingNumber),
            userName = displayName,
            psw = password,
            isVideoOff = false,
            isAudioOff = false
        };
        
        joinParam.withoutloginJoin = normalJoin;
        
        var result = meetingService.Join(joinParam);
        Console.WriteLine($"Join result: {result}");
    }
    
    private void OnMeetingStatusChanged(MeetingStatus status, int result)
    {
        switch (status)
        {
            case MeetingStatus.MEETING_STATUS_CONNECTING:
                Console.WriteLine("Connecting...");
                break;
            case MeetingStatus.MEETING_STATUS_INMEETING:
                Console.WriteLine("In meeting");
                break;
            case MeetingStatus.MEETING_STATUS_ENDED:
                Console.WriteLine("Meeting ended");
                break;
        }
    }
}
```

## Audio/Video Controls

```csharp
public class AVControls
{
    public void ToggleAudio()
    {
        var audioCtrl = CZoomSDKDotNetWrap.Instance
            .GetMeetingServiceWrap()
            .GetMeetingAudioController();
        
        if (audioCtrl.IsMyAudioMuted())
        {
            audioCtrl.UnMuteAudio(0); // 0 = self
        }
        else
        {
            audioCtrl.MuteAudio(0, true);
        }
    }
    
    public void ToggleVideo()
    {
        var videoCtrl = CZoomSDKDotNetWrap.Instance
            .GetMeetingServiceWrap()
            .GetMeetingVideoController();
        
        if (videoCtrl.IsMyVideoOn())
        {
            videoCtrl.MuteVideo();
        }
        else
        {
            videoCtrl.UnmuteVideo();
        }
    }
}
```

## WPF Integration

### Embedding Meeting View

```csharp
// In XAML
<WindowsFormsHost x:Name="zoomHost" />

// In code-behind
public partial class MeetingWindow : Window
{
    public MeetingWindow()
    {
        InitializeComponent();
        
        // Create a panel for Zoom video
        var panel = new System.Windows.Forms.Panel();
        zoomHost.Child = panel;
        
        // Set the panel as video container after joining meeting
        var uiCtrl = CZoomSDKDotNetWrap.Instance
            .GetMeetingServiceWrap()
            .GetUIController();
        
        uiCtrl.SetMeetingUIPos(new WndPosition
        {
            hSelfWnd = panel.Handle,
            hParent = IntPtr.Zero
        });
    }
}
```

## Custom UI Mode

```csharp
public void EnableCustomUI()
{
    var uiCtrl = CZoomSDKDotNetWrap.Instance
        .GetMeetingServiceWrap()
        .GetUIController();
    
    // Get video canvas handle
    var customUI = CZoomSDKDotNetWrap.Instance
        .GetMeetingServiceWrap()
        .GetMeetingCustomizedUI();
    
    // Subscribe to video render events
    customUI.Add_CB_onVideoRenderElementActiveChange(OnActiveVideoChanged);
}

private void OnActiveVideoChanged(uint userId, VideoRenderElementType type)
{
    Console.WriteLine($"Active video changed: User {userId}");
}
```

## Event Handling Pattern

The C# wrapper uses callback delegates for events:

```csharp
public class EventManager
{
    public void SetupEvents()
    {
        var meetingService = CZoomSDKDotNetWrap.Instance.GetMeetingServiceWrap();
        
        // Meeting status
        meetingService.Add_CB_onMeetingStatusChanged(OnMeetingStatus);
        
        // Participants
        var participantCtrl = meetingService.GetMeetingParticipantsController();
        participantCtrl.Add_CB_onUserJoin(OnUserJoin);
        participantCtrl.Add_CB_onUserLeft(OnUserLeft);
        
        // Audio
        var audioCtrl = meetingService.GetMeetingAudioController();
        audioCtrl.Add_CB_onUserAudioStatusChange(OnAudioStatusChange);
        
        // Video
        var videoCtrl = meetingService.GetMeetingVideoController();
        videoCtrl.Add_CB_onUserVideoStatusChange(OnVideoStatusChange);
    }
    
    private void OnUserJoin(uint[] userIds)
    {
        foreach (var userId in userIds)
        {
            Console.WriteLine($"User joined: {userId}");
        }
    }
    
    private void OnUserLeft(uint[] userIds)
    {
        foreach (var userId in userIds)
        {
            Console.WriteLine($"User left: {userId}");
        }
    }
    
    private void OnAudioStatusChange(uint[] userIds)
    {
        // Handle audio status changes
    }
    
    private void OnVideoStatusChange(uint userId, VideoStatus status)
    {
        Console.WriteLine($"User {userId} video: {status}");
    }
}
```

## Common Gotchas

| Issue | Solution |
|-------|----------|
| DLL not found | Ensure all native DLLs are in output directory |
| Platform mismatch | Match x86/x64 with your .NET project platform |
| UI thread issues | Invoke callbacks on UI thread for WPF/WinForms |
| Memory leaks | Unsubscribe events when disposing |

### Thread Safety

```csharp
// For WPF - invoke on UI thread
Application.Current.Dispatcher.Invoke(() => 
{
    // Update UI here
});

// For WinForms
this.Invoke((MethodInvoker)delegate 
{
    // Update UI here
});
```

## Cleanup

```csharp
public void Cleanup()
{
    var meetingService = CZoomSDKDotNetWrap.Instance.GetMeetingServiceWrap();
    
    // Leave meeting
    meetingService.Leave(LeaveMeetingCmd.LEAVE_MEETING);
    
    // Clean up SDK
    CZoomSDKDotNetWrap.Instance.CleanUp();
}
```

## Resources

- **Windows SDK docs**: https://developers.zoom.us/docs/meeting-sdk/windows/
- **Sample app**: https://github.com/zoom/zoom-sdk-windows

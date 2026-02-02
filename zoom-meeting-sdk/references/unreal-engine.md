# Meeting SDK - Unreal Engine

Embed Zoom meetings in Unreal Engine games and applications.

## Overview

Unreal Engine plugin for integrating Zoom meetings into games and interactive experiences.

## Prerequisites

- Meeting SDK Unreal Engine plugin from [Marketplace](https://marketplace.zoom.us/) (sign-in required)
- Unreal Engine 5.0+
- Valid SDK credentials

## Installation

1. Download plugin from Marketplace (requires sign-in)
2. Copy to your project's Plugins folder
3. Enable plugin in Project Settings

## Quick Start

```cpp
#include "ZoomMeetingSDK.h"

// Initialize
UZoomMeetingSDK* ZoomSDK = NewObject<UZoomMeetingSDK>();
ZoomSDK->Initialize(SDKKey, SDKSecret, "zoom.us");

// Join meeting
FZoomJoinMeetingParams JoinParams;
JoinParams.MeetingNumber = MeetingNumber;
JoinParams.UserName = TEXT("Player");
JoinParams.Password = Password;
ZoomSDK->JoinMeeting(JoinParams);
```

## Blueprint Support

The plugin includes Blueprint nodes for:
- Initializing SDK
- Joining/leaving meetings
- Audio/video controls
- Meeting events

## Common Tasks

### Actor/Component Integration

```cpp
// ZoomMeetingActor.h
#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ZoomMeetingSDK.h"
#include "ZoomMeetingActor.generated.h"

UCLASS()
class AZoomMeetingActor : public AActor
{
    GENERATED_BODY()
    
public:
    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    UZoomMeetingSDK* ZoomSDK;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    UTextureRenderTarget2D* VideoRenderTarget;
    
    UFUNCTION(BlueprintCallable)
    void JoinMeeting(const FString& MeetingNumber, const FString& Password);
    
    UFUNCTION(BlueprintCallable)
    void LeaveMeeting();
    
protected:
    virtual void BeginPlay() override;
    
private:
    void OnMeetingStatusChanged(EZoomMeetingStatus Status);
};

// ZoomMeetingActor.cpp
void AZoomMeetingActor::BeginPlay()
{
    Super::BeginPlay();
    
    ZoomSDK = NewObject<UZoomMeetingSDK>(this);
    ZoomSDK->Initialize(SDKKey, SDKSecret, TEXT("zoom.us"));
    
    // Bind event delegate
    ZoomSDK->OnMeetingStatusChanged.AddDynamic(this, &AZoomMeetingActor::OnMeetingStatusChanged);
}

void AZoomMeetingActor::JoinMeeting(const FString& MeetingNumber, const FString& Password)
{
    FZoomJoinMeetingParams Params;
    Params.MeetingNumber = MeetingNumber;
    Params.Password = Password;
    Params.UserName = TEXT("Player");
    
    ZoomSDK->JoinMeeting(Params);
}

void AZoomMeetingActor::OnMeetingStatusChanged(EZoomMeetingStatus Status)
{
    switch (Status)
    {
        case EZoomMeetingStatus::InMeeting:
            UE_LOG(LogTemp, Log, TEXT("In meeting"));
            break;
        case EZoomMeetingStatus::Ended:
            UE_LOG(LogTemp, Log, TEXT("Meeting ended"));
            break;
    }
}
```

### Blueprint Event Handling

```cpp
// In your component header
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnMeetingJoined, const FString&, MeetingId);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnMeetingLeft);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnUserJoined, const FString&, UserName);

UPROPERTY(BlueprintAssignable)
FOnMeetingJoined OnMeetingJoined;

UPROPERTY(BlueprintAssignable)
FOnMeetingLeft OnMeetingLeft;

UPROPERTY(BlueprintAssignable)
FOnUserJoined OnUserJoined;

// Broadcast events from C++
void UZoomMeetingComponent::HandleMeetingJoined(const FString& MeetingId)
{
    OnMeetingJoined.Broadcast(MeetingId);
}
```

**Blueprint Usage:**
1. Add ZoomMeetingComponent to your Actor
2. In Event Graph, right-click and search for "OnMeetingJoined"
3. Connect to your game logic

### Rendering Meeting Video to Textures

```cpp
// Create render target for video
UTextureRenderTarget2D* CreateVideoRenderTarget(int32 Width, int32 Height)
{
    UTextureRenderTarget2D* RenderTarget = NewObject<UTextureRenderTarget2D>();
    RenderTarget->InitAutoFormat(Width, Height);
    RenderTarget->UpdateResourceImmediate(true);
    return RenderTarget;
}

// Update texture with video frame
void UZoomMeetingComponent::OnVideoFrameReceived(const FZoomVideoFrame& Frame)
{
    if (!VideoRenderTarget) return;
    
    // Copy frame data to render target
    FTextureRenderTargetResource* Resource = VideoRenderTarget->GameThread_GetRenderTargetResource();
    
    ENQUEUE_RENDER_COMMAND(UpdateVideoTexture)([Resource, Frame](FRHICommandListImmediate& RHICmdList)
    {
        FUpdateTextureRegion2D Region(0, 0, 0, 0, Frame.Width, Frame.Height);
        
        RHICmdList.UpdateTexture2D(
            Resource->GetRenderTargetTexture(),
            0,
            Region,
            Frame.Width * 4,  // RGBA stride
            Frame.Data
        );
    });
}

// Apply to material in world
void AVideoScreen::SetupVideoMaterial()
{
    // Create dynamic material instance
    UMaterialInstanceDynamic* DynamicMaterial = UMaterialInstanceDynamic::Create(BaseMaterial, this);
    
    // Set the render target as texture parameter
    DynamicMaterial->SetTextureParameterValue(TEXT("VideoTexture"), VideoRenderTarget);
    
    // Apply to mesh
    MeshComponent->SetMaterial(0, DynamicMaterial);
}
```

### Audio Controls

```cpp
// Mute/unmute
UFUNCTION(BlueprintCallable)
void ToggleAudio()
{
    if (ZoomSDK->IsMyAudioMuted())
    {
        ZoomSDK->UnmuteMyAudio();
    }
    else
    {
        ZoomSDK->MuteMyAudio();
    }
}

// Start/stop video
UFUNCTION(BlueprintCallable)
void ToggleVideo()
{
    if (ZoomSDK->IsMyVideoMuted())
    {
        ZoomSDK->UnmuteMyVideo();
    }
    else
    {
        ZoomSDK->MuteMyVideo();
    }
}
```

## Platform Build Notes

- **Windows**: Include SDK DLLs in build
- **Mac**: Include SDK frameworks, notarize for distribution
- **Shipping builds**: Ensure SDK binaries are packaged

## Resources

- **Meeting SDK docs**: https://developers.zoom.us/docs/meeting-sdk/
- **Unreal Engine Plugin docs**: https://developers.zoom.us/docs/meeting-sdk/unreal/

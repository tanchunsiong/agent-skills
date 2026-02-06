# Singleton Hierarchy: Navigation Guide

## Overview

The Zoom Windows Meeting SDK uses a **service locator pattern** - a tree of singletons where you navigate from root services down to specific features. You don't construct objects; you traverse to them.

```
You want to...              You navigate to...
─────────────────────────────────────────────────────
Mute audio                  IMeetingService → IMeetingAudioController
Create breakout rooms       IMeetingService → IMeetingBOController → IBOCreator
Control remote camera       IMeetingService → IMeetingVideoController → IMeetingCameraHelper
Batch invite contacts       IAuthService → INotificationServiceHelper → IPresenceHelper → IBatchRequestContactHelper
```

---

## Complete Hierarchy (4 Levels Deep)

```
Level 0: Global Factory Functions (zoom_sdk.h)
│
├─► Level 1: IAuthService
│   ├─► Level 2: IDirectShareServiceHelper                              [LEAF]
│   └─► Level 2: INotificationServiceHelper
│       └─► Level 3: IPresenceHelper
│           └─► Level 4: IBatchRequestContactHelper                     [LEAF - MAX DEPTH]
│
├─► Level 1: IMeetingService
│   │
│   ├─► Level 2: IMeetingVideoController
│   │   └─► Level 3: IMeetingCameraHelper                               [LEAF]
│   │
│   ├─► Level 2: IMeetingAudioController                                [LEAF]
│   ├─► Level 2: IMeetingShareController                                [LEAF]
│   ├─► Level 2: IMeetingChatController                                 [LEAF]
│   ├─► Level 2: IMeetingRecordingController                            [LEAF]
│   ├─► Level 2: IMeetingParticipantsController                         [LEAF]
│   ├─► Level 2: IMeetingWaitingRoomController                          [LEAF]
│   ├─► Level 2: IMeetingWebinarController                              [LEAF]
│   ├─► Level 2: IMeetingRawArchivingController                         [LEAF]
│   ├─► Level 2: IMeetingReminderController                             [LEAF]
│   ├─► Level 2: IMeetingEncryptionController                           [LEAF]
│   ├─► Level 2: IMeetingConfiguration                                  [LEAF]
│   │
│   ├─► Level 2: IMeetingBOController (Breakout Rooms)
│   │   ├─► Level 3: IBOCreator
│   │   │   └─► Level 4: IBatchCreateBOHelper                           [LEAF - MAX DEPTH]
│   │   ├─► Level 3: IBOAdmin                                           [LEAF]
│   │   ├─► Level 3: IBOAssistant                                       [LEAF]
│   │   ├─► Level 3: IBOAttendee                                        [LEAF]
│   │   └─► Level 3: IBOData                                            [LEAF]
│   │
│   ├─► Level 2: IMeetingAICompanionController
│   │   ├─► Level 3: IMeetingAICompanionSmartSummaryHelper              [LEAF]
│   │   └─► Level 3: IMeetingAICompanionQueryHelper                     [LEAF]
│   │
│   └─► Level 2: ICustomImmersiveController
│       └─► Level 3: ICustomImmersivePreLayoutHelper                    [LEAF]
│
├─► Level 1: ISettingService
│   ├─► Level 2: IGeneralSettingContext                                 [LEAF]
│   ├─► Level 2: IAudioSettingContext                                   [LEAF]
│   ├─► Level 2: IVideoSettingContext                                   [LEAF]
│   ├─► Level 2: IRecordingSettingContext                               [LEAF]
│   ├─► Level 2: IShareSettingContext                                   [LEAF]
│   ├─► Level 2: IStatisticSettingContext                               [LEAF]
│   └─► Level 2: IWallpaperSettingContext                               [LEAF]
│
├─► Level 1: INetworkConnectionHelper                                   [LEAF]
│
└─► Level 1: ICustomizedUIMgr (Custom UI Mode)
    ├─► Level 2: ICustomizedVideoContainer (factory-created)
    ├─► Level 2: ICustomizedShareRender (factory-created)
    └─► Level 2: ICustomizedImmersiveContainer (factory-created)
```

---

## When to Use Each Level

| Level | When | Example |
|-------|------|---------|
| **Level 1** | App startup, before joining | `CreateMeetingService()`, `CreateAuthService()` |
| **Level 2** | After joining meeting, for features | `meetingService->GetMeetingAudioController()` |
| **Level 3** | For specialized sub-features | `boController->GetBOCreatorHelper()` |
| **Level 4** | For batch/bulk operations | `boCreator->GetBatchCreateBOHelper()` |

---

## How to Use (Universal Pattern)

Every feature follows the **same 3-step pattern**:

```cpp
// Step 1: Navigate to the controller (singleton)
IMeetingAudioController* audioCtrl = meetingService->GetMeetingAudioController();

// Step 2: Register event listener (observer pattern)
audioCtrl->SetEvent(new MyAudioEventListener());

// Step 3: Call methods
audioCtrl->MuteAudio(userId, true);
```

---

## Examples by Depth

### Level 2 - Basic Feature (Audio)

```cpp
// Get controller
IMeetingAudioController* audioCtrl = meetingService->GetMeetingAudioController();

// Use it
audioCtrl->JoinVoip();
audioCtrl->MuteAudio(0, true);  // 0 = self
```

### Level 3 - Sub-Feature (Breakout Room Creation)

```cpp
// Navigate: Level 1 → Level 2 → Level 3
IMeetingBOController* boCtrl = meetingService->GetMeetingBOController();
IBOCreator* creator = boCtrl->GetBOCreatorHelper();

// Use it
creator->CreateBreakoutRoom(L"Room 1");
creator->AssignUserToBO(strUserID, strBOID);
```

### Level 4 - Batch Operations (Bulk Room Creation)

```cpp
// Navigate: Level 1 → Level 2 → Level 3 → Level 4
IMeetingBOController* boCtrl = meetingService->GetMeetingBOController();
IBOCreator* creator = boCtrl->GetBOCreatorHelper();
IBatchCreateBOHelper* batch = creator->GetBatchCreateBOHelper();

// Use it (transaction pattern)
batch->CreateBOTransactionBegin();
batch->AddNewBoToList(L"Room 1");
batch->AddNewBoToList(L"Room 2");
batch->AddNewBoToList(L"Room 3");
batch->CreateBoTransactionCommit();  // Creates all 3 at once
```

---

## Why the Hierarchy Exists

| Depth | Design Purpose |
|-------|----------------|
| **Level 1** (Services) | Lifecycle management - created once, destroyed at cleanup |
| **Level 2** (Controllers) | Feature grouping - one controller per domain |
| **Level 3** (Helpers) | Role-based access - different helpers for host vs attendee |
| **Level 4** (Batch) | Performance optimization - bulk ops instead of N individual calls |

---

## Practical Rules

### 1. Don't Cache Too Early

Controllers return `nullptr` if not in meeting:

```cpp
// WRONG - cached before meeting joined
IMeetingAudioController* audioCtrl = meetingService->GetMeetingAudioController();
meetingService->Join(joinParam);
audioCtrl->MuteAudio(0, true);  // audioCtrl might be nullptr!

// RIGHT - get after joining
meetingService->Join(joinParam);
// ... wait for MEETING_STATUS_INMEETING callback ...
IMeetingAudioController* audioCtrl = meetingService->GetMeetingAudioController();
if (audioCtrl) {
    audioCtrl->MuteAudio(0, true);
}
```

### 2. Re-get After State Changes

After joining/leaving meeting, get controllers again - previous pointers may be invalid.

### 3. Check for nullptr

Some helpers only available for hosts:

```cpp
IBOCreator* creator = boCtrl->GetBOCreatorHelper();
if (creator) {
    // Only hosts get a valid creator
    creator->CreateBreakoutRoom(L"Room 1");
}
```

### 4. Batch When Possible

Level 4 helpers exist specifically for performance:

```cpp
// SLOW - 10 individual calls
for (int i = 0; i < 10; i++) {
    creator->CreateBreakoutRoom(roomNames[i]);
}

// FAST - 1 batch call
IBatchCreateBOHelper* batch = creator->GetBatchCreateBOHelper();
batch->CreateBOTransactionBegin();
for (int i = 0; i < 10; i++) {
    batch->AddNewBoToList(roomNames[i]);
}
batch->CreateBoTransactionCommit();
```

---

## Deepest Paths (Maximum Depth = 4)

| Path | Use Case |
|------|----------|
| `IMeetingService` → `IMeetingBOController` → `IBOCreator` → `IBatchCreateBOHelper` | Bulk breakout room creation |
| `IAuthService` → `INotificationServiceHelper` → `IPresenceHelper` → `IBatchRequestContactHelper` | Bulk contact operations |

---

## Quick Reference: Common Navigation Paths

| Feature | Navigation Path |
|---------|-----------------|
| Audio control | `IMeetingService` → `GetMeetingAudioController()` |
| Video control | `IMeetingService` → `GetMeetingVideoController()` |
| Screen sharing | `IMeetingService` → `GetMeetingShareController()` |
| Chat | `IMeetingService` → `GetMeetingChatController()` |
| Recording | `IMeetingService` → `GetMeetingRecordingController()` |
| Participants | `IMeetingService` → `GetMeetingParticipantsController()` |
| Waiting room | `IMeetingService` → `GetMeetingWaitingRoomController()` |
| Breakout rooms | `IMeetingService` → `GetMeetingBOController()` → `GetBO*Helper()` |
| AI Companion | `IMeetingService` → `GetMeetingAICompanionController()` |
| Remote camera | `IMeetingService` → `GetMeetingVideoController()` → `GetMeetingCameraHelper()` |
| Audio settings | `ISettingService` → `GetAudioSettings()` |
| Video settings | `ISettingService` → `GetVideoSettings()` |
| Presence/contacts | `IAuthService` → `GetNotificationServiceHelper()` → `GetPresenceHelper()` |

---

## Related Documentation

- [SDK Architecture Pattern](sdk-architecture-pattern.md) - The universal 3-step pattern
- [Custom UI Architecture](custom-ui-architecture.md) - Custom UI specific hierarchy
- [Breakout Rooms Example](../examples/breakout-rooms.md) - Level 3 helpers in action

---

**TL;DR**: The hierarchy is your navigation map. Start at a service, drill down to the feature you need, then call methods. Deeper levels = more specialized operations.

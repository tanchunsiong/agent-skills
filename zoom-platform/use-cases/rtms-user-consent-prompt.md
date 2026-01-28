# User Consent Prompt for RTMS

Prompt meeting participants for explicit consent before starting RTMS recording/streaming, with automatic pause/resume for new joiners.

## Overview

This use case demonstrates an enterprise consent-based approach to RTMS transcript access. The Zoom in-meeting app ensures RTMS streaming only begins when all participants have provided explicit consent. When new participants join, RTMS automatically pauses until they also consent. Features include a host dashboard with color-coded consent status, guest consent UI, live WebSocket synchronization, and automatic app invitations for new joiners.

## Skills Needed

- **zoom-rtms** - Primary

## Implementation

### JavaScript

The consent app uses a multi-service architecture with React frontend, Node.js backend, Redis for state management, and the Zoom Apps SDK for in-meeting control.

#### Backend: Consent State Management

```javascript
// Consent state stored in Redis with encryption
const consentState = {
  meetingId: null,
  participants: new Map(), // userId -> { name, consent: null | true | false }
  rtmsActive: false,
};

// Check if all participants have consented
function allConsented() {
  for (const [, p] of consentState.participants) {
    if (p.consent !== true) return false;
  }
  return consentState.participants.size > 0;
}

// Handle consent submission
app.post('/api/consent', async (req, res) => {
  const { userId, consent } = req.body;
  const participant = consentState.participants.get(userId);
  if (participant) {
    participant.consent = consent;
    broadcastStateUpdate();

    if (consent === false) {
      // Any decline stops RTMS permanently
      await stopRTMS();
    } else if (allConsented()) {
      // All consented — start or resume RTMS
      await startOrResumeRTMS();
    }
  }
  res.json({ success: true });
});
```

#### Frontend: Zoom Apps SDK Integration

```javascript
// Configure Zoom Apps SDK with RTMS capabilities
const configResponse = await zoomSdk.config({
  capabilities: [
    'getMeetingContext',
    'getMeetingUUID',
    'getUserContext',
    'getMeetingParticipants',
    'onParticipantChange',
    'sendAppInvitationToAllParticipants',
    'startRTMS',
    'stopRTMS',
  ],
});

// Auto-invite new participants to open the consent app
zoomSdk.on('onParticipantChange', async (event) => {
  if (event.changeType === 'join') {
    // Pause RTMS until new participant consents
    await zoomSdk.stopRTMS();
    // Send app invitation to new participant
    await zoomSdk.sendAppInvitationToAllParticipants();
  }
});

// Host: Start RTMS when all participants consent
async function startRTMSIfAllConsented() {
  const response = await fetch('/api/consent-status');
  const status = await response.json();
  if (status.allConsented) {
    await zoomSdk.startRTMS();
  }
}
```

#### RTMS Lifecycle

```
All Participants Consent → RTMS Starts
    ↓
New Participant Joins → RTMS Pauses
    ↓
New Participant Consents → RTMS Resumes
    ↓
Any Participant Declines → RTMS Stops Permanently
```

### Python

```python
from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class ConsentManager:
    participants: Dict[str, dict] = field(default_factory=dict)
    rtms_active: bool = False

    def add_participant(self, user_id: str, name: str):
        self.participants[user_id] = {'name': name, 'consent': None}

    def set_consent(self, user_id: str, consent: bool) -> Optional[str]:
        if user_id in self.participants:
            self.participants[user_id]['consent'] = consent
            if not consent:
                return 'stop'  # Any decline stops RTMS
            if self.all_consented():
                return 'start'  # All consented
        return 'waiting'

    def all_consented(self) -> bool:
        return (len(self.participants) > 0 and
                all(p['consent'] is True for p in self.participants.values()))

    def needs_reconsent(self) -> bool:
        return any(p['consent'] is None for p in self.participants.values())
```

## Resources

- **Sample repo**: https://github.com/zoom/rtms-samples/tree/main/zoom_apps/prompt_for_user_consent_js
- **RTMS docs**: https://developers.zoom.us/docs/rtms/
- **Zoom Apps SDK**: https://developers.zoom.us/docs/zoom-apps/

# Contact Center Integration

Build customer engagement solutions with Zoom Contact Center.

## Overview

Integrate Zoom Contact Center capabilities into your application for video-enabled customer support, sales engagements, and service interactions.

## Skills Needed

- **zoom-contact-center** - Primary

## Integration Options

| Option | Use Case |
|--------|----------|
| Web SDK | Browser-based contact center |
| iOS SDK | Mobile customer app |
| Android SDK | Mobile customer app |
| APIs | Backend integration |

## Key Concepts

| Concept | Description |
|---------|-------------|
| Engagement | Customer-agent interaction |
| Queue | Routing destination |
| Agent | Contact center representative |
| Flow | Call/chat routing logic |

## Quick Start (Web)

```javascript
import { ZoomContactCenter } from '@zoom/contact-center-sdk';

const client = new ZoomContactCenter();

await client.init({
  clientId: 'YOUR_CLIENT_ID',
  domain: 'your-domain.zoom.us'
});

await client.startVideoEngagement({
  queueId: 'QUEUE_ID',
  customerInfo: {
    name: 'Customer Name',
    email: 'customer@example.com'
  }
});
```

## Common Tasks

### Customer-Initiated Video Calls

```javascript
import { ZoomContactCenter } from '@zoom/contact-center-sdk';

const client = new ZoomContactCenter();

// Initialize
await client.init({
  clientId: 'YOUR_CLIENT_ID',
  domain: 'your-domain.zoom.us'
});

// Start video engagement
async function startVideoCall(customerInfo, queueId) {
  try {
    const engagement = await client.startVideoEngagement({
      queueId: queueId,
      customerInfo: {
        name: customerInfo.name,
        email: customerInfo.email,
        phone: customerInfo.phone,
        // Custom data for agent context
        customFields: {
          accountId: customerInfo.accountId,
          orderNumber: customerInfo.orderNumber,
          issue: customerInfo.issue
        }
      }
    });
    
    return engagement;
  } catch (error) {
    if (error.code === 'QUEUE_CLOSED') {
      showOfflineMessage();
    } else if (error.code === 'NO_AGENTS_AVAILABLE') {
      showWaitMessage();
    }
    throw error;
  }
}

// Handle engagement events
client.on('engagementStarted', (engagement) => {
  console.log('Connected with agent:', engagement.agentName);
  showVideoUI();
});

client.on('engagementEnded', (engagement) => {
  console.log('Call ended:', engagement.endReason);
  showSurvey();
});

client.on('agentJoined', (agent) => {
  console.log('Agent joined:', agent.displayName);
});

// End call
function endCall() {
  client.endEngagement();
}
```

### Agent Dashboard Integration

```javascript
// For building custom agent dashboards
const axios = require('axios');

// Get agent status
async function getAgentStatus(agentId) {
  const response = await axios.get(
    `https://api.zoom.us/v2/contact_center/agents/${agentId}/status`,
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
  
  return response.data;
}

// Set agent status
async function setAgentStatus(agentId, status) {
  // status: 'available', 'busy', 'offline', 'break'
  await axios.put(
    `https://api.zoom.us/v2/contact_center/agents/${agentId}/status`,
    { status: status },
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
}

// Get active engagements for agent
async function getActiveEngagements(agentId) {
  const response = await axios.get(
    `https://api.zoom.us/v2/contact_center/agents/${agentId}/engagements?status=active`,
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
  
  return response.data.engagements;
}

// Transfer engagement to another queue/agent
async function transferEngagement(engagementId, targetQueueId) {
  await axios.post(
    `https://api.zoom.us/v2/contact_center/engagements/${engagementId}/transfer`,
    {
      type: 'queue',
      target_id: targetQueueId
    },
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
}
```

### Queue Management

```javascript
// Get queue statistics
async function getQueueStats(queueId) {
  const response = await axios.get(
    `https://api.zoom.us/v2/contact_center/queues/${queueId}/statistics`,
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
  
  return {
    waitingCount: response.data.waiting_count,
    averageWaitTime: response.data.avg_wait_time,
    activeEngagements: response.data.active_count,
    availableAgents: response.data.available_agents
  };
}

// List all queues
async function listQueues() {
  const response = await axios.get(
    'https://api.zoom.us/v2/contact_center/queues',
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
  
  return response.data.queues;
}

// Check queue hours
function isQueueOpen(queue) {
  const now = new Date();
  const day = now.getDay();
  const time = now.getHours() * 100 + now.getMinutes();
  
  const schedule = queue.schedule[day];
  if (!schedule.enabled) return false;
  
  const start = parseInt(schedule.start.replace(':', ''));
  const end = parseInt(schedule.end.replace(':', ''));
  
  return time >= start && time <= end;
}
```

### Engagement Analytics

```javascript
// Get engagement history
async function getEngagementHistory(filters) {
  const response = await axios.get(
    'https://api.zoom.us/v2/contact_center/engagements',
    {
      params: {
        from: filters.from,
        to: filters.to,
        queue_id: filters.queueId,
        status: filters.status  // 'completed', 'abandoned', 'transferred'
      },
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
  
  return response.data.engagements;
}

// Calculate metrics
function calculateMetrics(engagements) {
  const completed = engagements.filter(e => e.status === 'completed');
  const abandoned = engagements.filter(e => e.status === 'abandoned');
  
  return {
    totalEngagements: engagements.length,
    completedCount: completed.length,
    abandonedCount: abandoned.length,
    abandonRate: (abandoned.length / engagements.length * 100).toFixed(1),
    averageWaitTime: average(engagements.map(e => e.wait_time)),
    averageHandleTime: average(completed.map(e => e.handle_time)),
    // CSAT from post-call surveys
    averageSatisfaction: average(completed.filter(e => e.csat).map(e => e.csat))
  };
}

// Webhook for real-time updates
app.post('/webhook/contact-center', (req, res) => {
  const { event, payload } = req.body;
  
  switch (event) {
    case 'engagement.started':
      trackEngagementStart(payload);
      break;
    case 'engagement.ended':
      trackEngagementEnd(payload);
      break;
    case 'queue.status_changed':
      updateQueueStatus(payload);
      break;
  }
  
  res.status(200).send();
});
```

## Resources

- **Contact Center docs**: https://developers.zoom.us/docs/contact-center/
- **Contact Center API**: https://developers.zoom.us/docs/api/rest/reference/contact-center/

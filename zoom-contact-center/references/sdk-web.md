# Contact Center - Web SDK

Browser-based Contact Center integration.

## Overview

Embed Zoom Contact Center video/chat capabilities into your web application.

## Prerequisites

- Zoom Contact Center license
- SDK credentials from [Marketplace](https://marketplace.zoom.us/) (sign-in required)

## Installation

```bash
npm install @zoom/contact-center-sdk
```

## Quick Start

```javascript
import { ZoomContactCenter } from '@zoom/contact-center-sdk';

const client = new ZoomContactCenter();

await client.init({
  clientId: 'YOUR_CLIENT_ID',
  domain: 'your-domain.zoom.us'
});

// Start video engagement
await client.startVideoEngagement({
  queueId: 'QUEUE_ID',
  customerInfo: {
    name: 'Customer Name',
    email: 'customer@example.com'
  }
});
```

## Event Handling

```javascript
client.on('engagementStarted', (engagement) => {
  console.log('Engagement started:', engagement);
});

client.on('engagementEnded', (engagement) => {
  console.log('Engagement ended:', engagement);
});

client.on('agentJoined', (agent) => {
  console.log('Agent joined:', agent);
});
```

## Common Tasks

### Starting Video Engagement

```javascript
import { ZoomContactCenter } from '@zoom/contact-center-sdk';

const client = new ZoomContactCenter();

async function initContactCenter() {
  await client.init({
    clientId: 'YOUR_CLIENT_ID',
    domain: 'your-domain.zoom.us'
  });
}

async function startVideoCall(customerInfo, queueId) {
  try {
    const engagement = await client.startVideoEngagement({
      queueId: queueId,
      customerInfo: {
        name: customerInfo.name,
        email: customerInfo.email,
        phone: customerInfo.phone
      },
      // Optional custom data for agent context
      metadata: {
        accountId: customerInfo.accountId,
        orderNumber: customerInfo.orderNumber
      }
    });
    
    console.log('Engagement started:', engagement.id);
    return engagement;
  } catch (error) {
    handleEngagementError(error);
  }
}

function handleEngagementError(error) {
  switch (error.code) {
    case 'QUEUE_CLOSED':
      showMessage('Support is currently closed. Please try again during business hours.');
      break;
    case 'NO_AGENTS_AVAILABLE':
      showMessage('All agents are busy. Please wait or try again later.');
      break;
    case 'QUEUE_FULL':
      showMessage('The queue is full. Please try again later.');
      break;
    default:
      showMessage('Unable to connect. Please try again.');
  }
}
```

### Chat Integration

```javascript
// Start chat engagement
async function startChat(customerInfo, queueId) {
  const engagement = await client.startChatEngagement({
    queueId: queueId,
    customerInfo: customerInfo
  });
  
  return engagement;
}

// Send message
async function sendMessage(text) {
  await client.sendChatMessage({
    text: text,
    type: 'text'
  });
}

// Send file
async function sendFile(file) {
  await client.sendChatMessage({
    file: file,
    type: 'file'
  });
}

// Listen for messages
client.on('chatMessageReceived', (message) => {
  displayMessage({
    sender: message.senderName,
    text: message.text,
    timestamp: message.timestamp,
    isAgent: message.isFromAgent
  });
});

// Typing indicator
client.on('agentTyping', (isTyping) => {
  if (isTyping) {
    showTypingIndicator();
  } else {
    hideTypingIndicator();
  }
});
```

### Queue Management

```javascript
// Check queue status before initiating
async function checkQueueStatus(queueId) {
  const status = await client.getQueueStatus(queueId);
  
  return {
    isOpen: status.isOpen,
    waitTime: status.estimatedWaitTime,
    position: status.queuePosition,
    agentsAvailable: status.availableAgents > 0
  };
}

// Display queue info to customer
async function showQueueInfo(queueId) {
  const status = await checkQueueStatus(queueId);
  
  if (!status.isOpen) {
    displayOfflineMessage();
    return false;
  }
  
  if (!status.agentsAvailable) {
    displayWaitTime(status.waitTime);
  }
  
  return true;
}

// Listen for queue position updates
client.on('queuePositionChanged', (position) => {
  updateQueueDisplay(position.current, position.total);
});
```

### Custom UI Integration

```javascript
// Embed in custom container
const container = document.getElementById('contact-center-container');

await client.init({
  clientId: 'YOUR_CLIENT_ID',
  domain: 'your-domain.zoom.us',
  container: container,  // Custom container element
  theme: {
    primaryColor: '#007bff',
    fontFamily: 'Arial, sans-serif'
  }
});

// Handle UI events
client.on('engagementStarted', () => {
  showVideoUI();
  hideWaitingUI();
});

client.on('engagementEnded', (reason) => {
  hideVideoUI();
  showSurvey();
});

client.on('agentJoined', (agent) => {
  displayAgentInfo(agent.displayName, agent.avatarUrl);
});

// Control video/audio
function toggleVideo() {
  client.toggleVideo();
}

function toggleMute() {
  client.toggleMute();
}

function endEngagement() {
  client.endEngagement();
}
```

## Resources

- **Contact Center docs**: https://developers.zoom.us/docs/contact-center/
- **Web SDK reference**: https://developers.zoom.us/docs/contact-center/web/

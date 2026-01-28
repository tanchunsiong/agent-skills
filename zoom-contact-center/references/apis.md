# Contact Center - APIs

REST APIs for Contact Center management.

## Overview

Server-side APIs for managing Contact Center resources, engagements, and analytics.

## Base URL

```
https://api.zoom.us/v2/contact_center
```

## Endpoints

### Queues

```bash
# List queues
GET /contact_center/queues

# Get queue details
GET /contact_center/queues/{queueId}
```

### Engagements

```bash
# List engagements
GET /contact_center/engagements

# Get engagement details
GET /contact_center/engagements/{engagementId}
```

### Agents

```bash
# List agents
GET /contact_center/agents

# Get agent status
GET /contact_center/agents/{agentId}/status
```

## Authentication

Use Server-to-Server OAuth or OAuth tokens:

```bash
curl -X GET "https://api.zoom.us/v2/contact_center/queues" \
  -H "Authorization: Bearer {accessToken}"
```

## Required Scopes

- `contact_center:read` - View Contact Center data
- `contact_center:write` - Manage Contact Center resources

## Common Tasks

### Queue Management

```javascript
const axios = require('axios');

// List all queues
async function listQueues() {
  const response = await axios.get(
    'https://api.zoom.us/v2/contact_center/queues',
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
  return response.data.queues;
}

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
    availableAgents: response.data.available_agents,
    serviceLevel: response.data.service_level
  };
}

// Update queue settings
async function updateQueue(queueId, settings) {
  await axios.patch(
    `https://api.zoom.us/v2/contact_center/queues/${queueId}`,
    {
      name: settings.name,
      max_wait_time: settings.maxWaitTime,
      wrap_up_time: settings.wrapUpTime,
      overflow_queue_id: settings.overflowQueueId
    },
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
}
```

### Agent Status Monitoring

```javascript
// Get all agents
async function listAgents() {
  const response = await axios.get(
    'https://api.zoom.us/v2/contact_center/agents',
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
  return response.data.agents;
}

// Get agent status
async function getAgentStatus(agentId) {
  const response = await axios.get(
    `https://api.zoom.us/v2/contact_center/agents/${agentId}/status`,
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
  
  return {
    status: response.data.status,  // 'available', 'busy', 'away', 'offline'
    activeEngagements: response.data.active_engagements,
    lastStatusChange: response.data.last_status_change
  };
}

// Set agent status (admin only)
async function setAgentStatus(agentId, status) {
  await axios.put(
    `https://api.zoom.us/v2/contact_center/agents/${agentId}/status`,
    { status: status },  // 'available', 'away', 'offline'
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
}

// Monitor all agents in real-time
async function monitorAgents() {
  const agents = await listAgents();
  
  const statuses = await Promise.all(
    agents.map(async (agent) => ({
      id: agent.id,
      name: agent.display_name,
      ...(await getAgentStatus(agent.id))
    }))
  );
  
  return {
    total: agents.length,
    available: statuses.filter(a => a.status === 'available').length,
    busy: statuses.filter(a => a.status === 'busy').length,
    away: statuses.filter(a => a.status === 'away').length,
    offline: statuses.filter(a => a.status === 'offline').length,
    agents: statuses
  };
}
```

### Engagement Analytics

```javascript
// List engagements with filters
async function listEngagements(filters) {
  const response = await axios.get(
    'https://api.zoom.us/v2/contact_center/engagements',
    {
      params: {
        from: filters.from,
        to: filters.to,
        status: filters.status,  // 'active', 'completed', 'abandoned'
        queue_id: filters.queueId,
        page_size: 100
      },
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
  
  return response.data.engagements;
}

// Calculate engagement metrics
async function getEngagementMetrics(from, to) {
  const engagements = await listEngagements({ from, to });
  
  const completed = engagements.filter(e => e.status === 'completed');
  const abandoned = engagements.filter(e => e.status === 'abandoned');
  
  const waitTimes = engagements.map(e => e.wait_time);
  const handleTimes = completed.map(e => e.handle_time);
  
  return {
    totalEngagements: engagements.length,
    completedCount: completed.length,
    abandonedCount: abandoned.length,
    abandonRate: (abandoned.length / engagements.length * 100).toFixed(1),
    averageWaitTime: average(waitTimes),
    averageHandleTime: average(handleTimes),
    firstCallResolution: calculateFCR(completed)
  };
}
```

### Reporting

```javascript
// Daily report
async function getDailyReport(date) {
  const response = await axios.get(
    'https://api.zoom.us/v2/contact_center/reports/daily',
    {
      params: { date: date },
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
  
  return response.data;
}

// Queue performance report
async function getQueueReport(queueId, from, to) {
  const response = await axios.get(
    `https://api.zoom.us/v2/contact_center/reports/queues/${queueId}`,
    {
      params: { from, to },
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
  
  return {
    totalEngagements: response.data.total_engagements,
    answeredEngagements: response.data.answered,
    abandonedEngagements: response.data.abandoned,
    avgWaitTime: response.data.avg_wait_time,
    avgHandleTime: response.data.avg_handle_time,
    serviceLevel: response.data.service_level
  };
}

// Agent performance report
async function getAgentReport(agentId, from, to) {
  const response = await axios.get(
    `https://api.zoom.us/v2/contact_center/reports/agents/${agentId}`,
    {
      params: { from, to },
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
  
  return {
    totalEngagements: response.data.total_engagements,
    avgHandleTime: response.data.avg_handle_time,
    avgAfterCallWork: response.data.avg_after_call_work,
    utilizationRate: response.data.utilization_rate,
    customerSatisfaction: response.data.csat
  };
}

// Export report to CSV
async function exportReport(reportType, from, to) {
  const report = await getReport(reportType, from, to);
  
  const csv = convertToCSV(report);
  fs.writeFileSync(`report_${reportType}_${from}_${to}.csv`, csv);
}
```

### Webhooks

```javascript
// Handle Contact Center webhooks
app.post('/webhook/contact-center', (req, res) => {
  const { event, payload } = req.body;
  
  switch (event) {
    case 'engagement.started':
      logEngagementStart(payload);
      break;
    case 'engagement.ended':
      logEngagementEnd(payload);
      calculateMetrics(payload);
      break;
    case 'agent.status_changed':
      updateAgentDashboard(payload);
      break;
    case 'queue.threshold_exceeded':
      alertSupervisor(payload);
      break;
  }
  
  res.status(200).send();
});
```

## Resources

- **Contact Center API**: https://developers.zoom.us/docs/api/rest/reference/contact-center/methods/

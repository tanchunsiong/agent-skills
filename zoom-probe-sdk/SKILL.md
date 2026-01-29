---
name: zoom-probe-sdk
description: |
  Zoom Probe SDK guide for monitoring and debugging Zoom Apps. Covers the diagnostic toolkit
  for tracking app performance, debugging issues, and monitoring user experience in production.
  Use when building observability into Zoom Apps or troubleshooting app behavior.
---

# Zoom Probe SDK

Monitor, debug, and optimize your Zoom Apps with the Probe SDK diagnostic toolkit.

## Overview

Zoom Probe SDK provides:
- Real-time performance monitoring
- Error tracking and reporting
- User experience metrics
- Network diagnostics
- Debug logging
- Production observability

## Key Features

| Feature | Description |
|---------|-------------|
| **Performance Metrics** | Track load times, render performance |
| **Error Tracking** | Capture and report JavaScript errors |
| **Network Monitoring** | Monitor API calls and latency |
| **User Actions** | Track user interactions and flows |
| **Session Recording** | Replay user sessions for debugging |
| **Custom Events** | Log application-specific events |

## Installation

```bash
# Install Probe SDK
npm install @zoom/probe-sdk

# Or via CDN
<script src="https://static.zoom.us/probe-sdk/v1/probe.min.js"></script>
```

## Quick Start

### Initialize Probe SDK

```javascript
import { ProbeSDK } from '@zoom/probe-sdk';

const probe = new ProbeSDK({
  appId: 'your_app_id',
  environment: 'production', // 'development' | 'staging' | 'production'
  version: '1.0.0',
  enableAutoCapture: true
});

// Initialize
await probe.init();
```

### Basic Error Tracking

```javascript
// Automatic error capture (if enableAutoCapture: true)
// Or manual error reporting
try {
  await riskyOperation();
} catch (error) {
  probe.captureError(error, {
    context: 'riskyOperation',
    userId: currentUser.id
  });
}
```

### Performance Monitoring

```javascript
// Track a timed operation
const transaction = probe.startTransaction('loadDashboard');

await loadUserData();
transaction.setTag('dataLoaded', true);

await renderComponents();
transaction.finish(); // Automatically calculates duration
```

## Configuration Options

```javascript
const probe = new ProbeSDK({
  // Required
  appId: 'your_app_id',
  
  // Environment
  environment: 'production',
  version: '1.0.0',
  
  // Auto-capture settings
  enableAutoCapture: true,
  captureUnhandledErrors: true,
  captureUnhandledRejections: true,
  captureConsoleErrors: true,
  
  // Performance
  enablePerformanceMonitoring: true,
  tracesSampleRate: 0.1, // 10% of transactions
  
  // Network
  enableNetworkMonitoring: true,
  tracePropagationTargets: ['api.zoom.us', 'your-api.com'],
  
  // Privacy
  beforeSend: (event) => {
    // Scrub sensitive data
    delete event.user.email;
    return event;
  },
  
  // Debug
  debug: false
});
```

## Error Tracking

### Capture Exceptions

```javascript
// Capture with context
probe.captureError(error, {
  level: 'error', // 'fatal' | 'error' | 'warning' | 'info'
  tags: {
    feature: 'video-upload',
    userId: user.id
  },
  extra: {
    fileSize: file.size,
    fileType: file.type
  }
});
```

### Capture Messages

```javascript
// Log important events
probe.captureMessage('User exceeded storage limit', {
  level: 'warning',
  tags: { userId: user.id },
  extra: { currentUsage: usage, limit: limit }
});
```

### Error Boundaries (React)

```jsx
import { ProbeErrorBoundary } from '@zoom/probe-sdk/react';

function App() {
  return (
    <ProbeErrorBoundary
      fallback={<ErrorPage />}
      onError={(error, componentStack) => {
        console.log('Component error:', componentStack);
      }}
    >
      <MainContent />
    </ProbeErrorBoundary>
  );
}
```

## Performance Monitoring

### Transactions

```javascript
// Start a transaction
const transaction = probe.startTransaction({
  name: 'pageLoad',
  op: 'navigation'
});

// Add spans for sub-operations
const apiSpan = transaction.startSpan({
  op: 'http.request',
  description: 'GET /api/users'
});

const users = await fetchUsers();
apiSpan.finish();

const renderSpan = transaction.startSpan({
  op: 'render',
  description: 'renderUserList'
});

renderUserList(users);
renderSpan.finish();

// Finish transaction
transaction.finish();
```

### Web Vitals

```javascript
// Automatically captured when enablePerformanceMonitoring: true
// - LCP (Largest Contentful Paint)
// - FID (First Input Delay)
// - CLS (Cumulative Layout Shift)
// - TTFB (Time to First Byte)
// - FCP (First Contentful Paint)

// Access metrics
probe.onWebVitals((metric) => {
  console.log(`${metric.name}: ${metric.value}`);
});
```

### Custom Metrics

```javascript
// Track custom performance metrics
probe.trackMetric('videoLoadTime', loadTimeMs, {
  unit: 'milliseconds',
  tags: { resolution: '1080p' }
});

probe.trackMetric('participantCount', count, {
  unit: 'count',
  tags: { sessionId: session.id }
});
```

## Network Monitoring

### API Call Tracking

```javascript
// Automatic tracking for fetch/XHR
// Or manual tracking
const networkSpan = probe.startSpan({
  op: 'http.request',
  description: 'POST /api/meetings'
});

try {
  const response = await fetch('/api/meetings', {
    method: 'POST',
    body: JSON.stringify(meetingData)
  });
  
  networkSpan.setStatus(response.ok ? 'ok' : 'error');
  networkSpan.setData('statusCode', response.status);
} catch (error) {
  networkSpan.setStatus('error');
  throw error;
} finally {
  networkSpan.finish();
}
```

### Network Breadcrumbs

```javascript
// View network activity leading to an error
probe.captureError(error);
// Breadcrumbs automatically include recent network calls:
// - GET /api/user (200) - 150ms
// - POST /api/meeting (500) - 2300ms  <-- Error here
```

## User Context

### Set User Information

```javascript
// Set current user (for error/event attribution)
probe.setUser({
  id: user.id,
  email: user.email, // Optional, consider privacy
  username: user.displayName,
  subscription: user.plan
});

// Clear on logout
probe.clearUser();
```

### Add Tags and Context

```javascript
// Global tags (included in all events)
probe.setTag('appVersion', '2.1.0');
probe.setTag('accountType', 'enterprise');

// Add context for debugging
probe.setContext('meeting', {
  meetingId: meeting.id,
  participantCount: participants.length,
  hasRecording: meeting.recordingEnabled
});
```

## Breadcrumbs

```javascript
// Manual breadcrumbs
probe.addBreadcrumb({
  category: 'user-action',
  message: 'User clicked Start Meeting',
  level: 'info',
  data: { meetingId: '123' }
});

probe.addBreadcrumb({
  category: 'navigation',
  message: 'Navigated to /dashboard',
  level: 'info'
});

// Breadcrumbs provide context when errors occur
```

## Session Replay (Optional)

```javascript
const probe = new ProbeSDK({
  appId: 'your_app_id',
  enableSessionReplay: true,
  sessionReplayOptions: {
    maskAllText: false,
    maskAllInputs: true,
    blockSelector: '.sensitive-data'
  }
});

// Sessions are recorded and can be replayed in dashboard
```

## Dashboard Integration

### View in Zoom Developer Portal

1. Go to [Zoom App Marketplace](https://marketplace.zoom.us/)
2. Navigate to your app -> **Monitoring**
3. View:
   - Error rates and trends
   - Performance metrics
   - User sessions
   - Network performance

### Alerts

```javascript
// Configure alerts in dashboard for:
// - Error rate exceeds threshold
// - Performance degradation
// - Specific error types
```

## Privacy and Data Handling

```javascript
const probe = new ProbeSDK({
  appId: 'your_app_id',
  
  // Scrub sensitive data
  beforeSend: (event) => {
    // Remove PII
    if (event.user) {
      delete event.user.email;
      delete event.user.ip_address;
    }
    
    // Scrub request bodies
    if (event.request?.data) {
      event.request.data = '[Filtered]';
    }
    
    return event;
  },
  
  // Opt-out certain errors
  ignoreErrors: [
    'ResizeObserver loop limit exceeded',
    /^NetworkError/
  ]
});
```

## Prerequisites

1. **Zoom App** - Registered in Marketplace
2. **Probe SDK credentials** - Available in app settings
3. **Modern browser** - ES6+ support

## Common Use Cases

| Use Case | Feature | Description |
|----------|---------|-------------|
| **Error Monitoring** | captureError | Track production errors |
| **Performance** | Transactions | Monitor load times |
| **Debugging** | Session Replay | Reproduce user issues |
| **Analytics** | Custom Events | Track feature usage |
| **Alerting** | Dashboard | Get notified of issues |

## Resources

- **Probe SDK Guide**: https://developers.zoom.us/docs/zoom-apps/probe-sdk/
- **Zoom Apps Documentation**: https://developers.zoom.us/docs/zoom-apps/
- **Developer Dashboard**: https://marketplace.zoom.us/
- **Best Practices**: https://developers.zoom.us/docs/zoom-apps/best-practices/

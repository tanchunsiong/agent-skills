---
name: zoom-rivet
description: |
  Zoom Rivet development toolkit guide. Covers the CLI tool for creating, developing, testing,
  and deploying Zoom Apps. Use when scaffolding new Zoom Apps, running local development
  servers, or managing app deployment workflows.
---

# Zoom Rivet Toolkit

The official CLI and development toolkit for building Zoom Apps faster.

## Overview

Zoom Rivet provides:
- Project scaffolding with templates
- Local development server with hot reload
- OAuth and authentication helpers
- Testing and debugging tools
- Deployment automation
- SDK integration setup

## Key Features

| Feature | Description |
|---------|-------------|
| **Project Templates** | Scaffold React, Next.js, or vanilla JS apps |
| **Dev Server** | Local server with Zoom SDK integration |
| **Auth Flow** | Built-in OAuth handling |
| **Hot Reload** | Live updates during development |
| **Tunnel** | Public URL for local development |
| **Deploy** | One-command deployment |

## Installation

```bash
# Install globally
npm install -g @zoom/rivet

# Or use npx
npx @zoom/rivet <command>
```

## Quick Start

### Create a New Zoom App

```bash
# Interactive project creation
rivet create my-zoom-app

# Or specify template
rivet create my-zoom-app --template react
rivet create my-zoom-app --template nextjs
rivet create my-zoom-app --template vanilla
```

### Start Development Server

```bash
cd my-zoom-app

# Start dev server with tunnel
rivet dev

# Output:
# > Development server started at http://localhost:3000
# > Tunnel URL: https://abc123.rivet.zoom.us
# > Configure this URL in your Zoom App settings
```

### Configure Your App

1. Go to [Zoom App Marketplace](https://marketplace.zoom.us/)
2. Create or select your app
3. Set redirect URLs to your Rivet tunnel URL
4. Copy Client ID and Secret to `.env`

## CLI Commands

| Command | Description |
|---------|-------------|
| `rivet create <name>` | Create new Zoom App project |
| `rivet dev` | Start development server |
| `rivet build` | Build for production |
| `rivet deploy` | Deploy to hosting |
| `rivet auth` | Test OAuth flow |
| `rivet tunnel` | Start tunnel only |
| `rivet logs` | View app logs |

## Project Templates

### React Template

```bash
rivet create my-app --template react
```

Includes:
- React 18 with hooks
- Zoom Apps SDK configured
- TypeScript support
- Tailwind CSS
- Example components

### Next.js Template

```bash
rivet create my-app --template nextjs
```

Includes:
- Next.js 14 App Router
- Server-side OAuth handling
- API routes for Zoom APIs
- TypeScript
- Tailwind CSS

### Vanilla JavaScript

```bash
rivet create my-app --template vanilla
```

Includes:
- Plain HTML/CSS/JS
- Zoom Apps SDK
- Minimal setup

## Configuration

### rivet.config.js

```javascript
module.exports = {
  // App settings
  name: 'My Zoom App',
  clientId: process.env.ZOOM_CLIENT_ID,
  clientSecret: process.env.ZOOM_CLIENT_SECRET,
  
  // Development
  dev: {
    port: 3000,
    tunnel: true,
    hot: true
  },
  
  // Build
  build: {
    outDir: 'dist',
    minify: true
  },
  
  // Deploy
  deploy: {
    provider: 'vercel', // or 'netlify', 'aws'
    env: ['ZOOM_CLIENT_ID', 'ZOOM_CLIENT_SECRET']
  }
};
```

### Environment Variables

```bash
# .env
ZOOM_CLIENT_ID=your_client_id
ZOOM_CLIENT_SECRET=your_client_secret
ZOOM_REDIRECT_URI=https://abc123.rivet.zoom.us/auth/callback
```

## Development Workflow

### 1. Initialize Project

```bash
rivet create my-zoom-app --template nextjs
cd my-zoom-app
```

### 2. Configure Credentials

```bash
# Copy example env file
cp .env.example .env

# Edit with your Zoom App credentials
```

### 3. Start Development

```bash
rivet dev
```

### 4. Test in Zoom

1. Open Zoom Desktop Client
2. Go to Apps -> Add Apps
3. Search for your development app
4. Click to open and test

### 5. Deploy

```bash
rivet build
rivet deploy
```

## SDK Integration

Rivet automatically configures the Zoom Apps SDK:

```javascript
// The SDK is pre-configured in Rivet projects
import zoomSdk from '@zoom/appssdk';

// Initialize (Rivet handles this)
await zoomSdk.config({
  capabilities: ['shareApp', 'getMeetingContext']
});

// Use SDK methods
const context = await zoomSdk.getMeetingContext();
console.log('Meeting ID:', context.meetingID);
```

## OAuth Helpers

Rivet provides built-in OAuth utilities:

```javascript
// Rivet handles OAuth token exchange
import { getAccessToken, refreshToken } from '@zoom/rivet/auth';

// Get current access token
const token = await getAccessToken(userId);

// Refresh expired token
const newToken = await refreshToken(userId);

// Make authenticated API call
const response = await fetch('https://api.zoom.us/v2/users/me', {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

## Debugging

### View Logs

```bash
# Real-time logs
rivet logs --follow

# Filter by level
rivet logs --level error
```

### Debug OAuth

```bash
# Test OAuth flow
rivet auth --test

# Output:
# > Authorization URL: https://zoom.us/oauth/authorize?...
# > Waiting for callback...
# > Token received successfully
# > Access token: eyJ...
```

### Inspect Requests

```bash
# Enable request logging
rivet dev --verbose
```

## Prerequisites

1. **Node.js 18+** - Required runtime
2. **Zoom Account** - Developer account
3. **Zoom App** - Created in Marketplace
4. **ngrok or Rivet tunnel** - For HTTPS development

## Common Use Cases

| Use Case | Command | Description |
|----------|---------|-------------|
| **New Project** | `rivet create` | Start a new Zoom App |
| **Local Testing** | `rivet dev` | Test with live Zoom |
| **Production Build** | `rivet build` | Optimize for deployment |
| **Quick Deploy** | `rivet deploy` | Ship to hosting |
| **Auth Testing** | `rivet auth --test` | Verify OAuth setup |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tunnel not connecting | Check firewall, try `rivet tunnel --debug` |
| OAuth failing | Verify redirect URIs match exactly |
| SDK not loading | Check CSP headers, use HTTPS |
| Hot reload broken | Restart dev server |

## Resources

- **Rivet Documentation**: https://developers.zoom.us/docs/zoom-apps/zoom-rivet/
- **Zoom Apps Guide**: https://developers.zoom.us/docs/zoom-apps/
- **GitHub Repository**: https://github.com/zoom/rivet
- **Zoom Apps SDK**: https://developers.zoom.us/docs/zoom-apps/js-sdk/

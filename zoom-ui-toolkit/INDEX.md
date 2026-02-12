# Zoom Video SDK UI Toolkit - Documentation Index

Complete navigation for all UI Toolkit documentation.

## 📚 Start Here

New to the UI Toolkit? Follow this learning path:

1. **[SKILL.md](SKILL.md)** - Main overview and quick start
2. **Quick Start Guide** - Working code in 5 minutes (see skill.md)
3. **JWT Authentication** - Server-side token generation (see skill.md)
4. **Choose Your Mode** - Composite vs Components (see skill.md)

## 🎯 Core Concepts

Understanding how UI Toolkit works:

- **Composite vs Components** - Two ways to use UI Toolkit (see skill.md)
- **UI Toolkit Architecture** - How it wraps Video SDK internally
- **Feature Configuration** - Understanding featuresOptions structure
- **Session Lifecycle** - Join → Active → Leave/Close → Destroy flow

## 📖 Complete Guides

### Getting Started
- **Installation** - NPM install and React 18 setup (see skill.md)
- **Quick Start - Composite** - Full UI in one container (see skill.md)
- **Quick Start - Components** - Individual UI pieces (see skill.md)
- **JWT Authentication** - Server-side token generation (see skill.md)

### Framework Integration
- **React Integration** - Hooks, useEffect patterns (see skill.md)
- **Vue.js Integration** - Composition API and Options API (see skill.md)
- **Angular Integration** - Component lifecycle (see skill.md)
- **Next.js Integration** - App Router, Server Components (see skill.md)
- **Vanilla JavaScript** - No framework usage (see skill.md)

### Advanced Topics
- **Component Lifecycle** - Mount, unmount, cleanup patterns
- **Event Listeners** - React to session events
- **Session Management** - Programmatic control
- **Quality Statistics** - Monitor connection quality
- **Custom Themes** - Theme customization
- **Virtual Backgrounds** - Custom background images

## 📚 API Reference

Complete API documentation:

- **Core Methods** (see skill.md)
  - `joinSession()` - Start a video session
  - `closeSession()` - End session and remove UI
  - `destroy()` - Clean up UI Toolkit instance
  - `leaveSession()` - Leave without destroying UI

- **Component Methods** (see skill.md)
  - `showControlsComponent()` - Display control bar
  - `showChatComponent()` - Display chat panel
  - `showUsersComponent()` - Display participants list
  - `showSettingsComponent()` - Display settings panel
  - `hideAllComponents()` - Hide all components

- **Event Listeners** (see skill.md)
  - `onSessionJoined()` - Session joined successfully
  - `onSessionClosed()` - Session ended
  - `onSessionDestroyed()` - UI Toolkit destroyed
  - `onViewTypeChange()` - View mode changed
  - `on()` - Subscribe to Video SDK events
  - `off()` - Unsubscribe from events

- **Information Methods** (see skill.md)
  - `getSessionInfo()` - Get session details
  - `getCurrentUserInfo()` - Get current user
  - `getAllUser()` - Get all participants
  - `getClient()` - Get underlying Video SDK client
  - `version()` - Get version info

- **Control Methods** (see skill.md)
  - `changeViewType()` - Switch view mode
  - `mirrorVideo()` - Mirror self video
  - `isSupportCustomLayout()` - Check device support

- **Statistics Methods** (see skill.md)
  - `subscribeAudioStatisticData()` - Audio quality stats
  - `subscribeVideoStatisticData()` - Video quality stats
  - `subscribeShareStatisticData()` - Share quality stats

## 🔧 Configuration

- **Feature Configuration** (see skill.md)
  - `featuresOptions` structure
  - Audio/Video options
  - Chat, Users, Settings
  - Virtual Background
  - Recording, Captions (paid features)
  - Theme customization
  - View modes

- **Session Configuration** (see skill.md)
  - Required: `videoSDKJWT`, `sessionName`, `userName`
  - Optional: `sessionPasscode`, `sessionIdleTimeoutMins`
  - Debug mode
  - Web endpoint
  - Language settings

## ⚠️ Troubleshooting

### Common Issues
- React 18 peer dependency error
- JWT token invalid
- CSS not loading
- Components not showing
- Session join failures

See: **[troubleshooting/common-issues.md](troubleshooting/common-issues.md)**

### Framework-Specific Issues
- React: SSR, hydration, cleanup
- Vue: Reactivity, lifecycle
- Angular: Module imports, AOT
- Next.js: App Router, basePath

### Session Issues
- Authentication failures
- Connection problems
- Video/audio not working
- Screen share issues

## 📦 Sample Applications

**Official Repositories**:

| Framework | Repository | Key Features |
|-----------|------------|--------------|
| React | [videosdk-zoom-ui-toolkit-react-sample](https://github.com/zoom/videosdk-zoom-ui-toolkit-react-sample) | Hooks, TypeScript |
| Vue.js | [videosdk-zoom-ui-toolkit-vuejs-sample](https://github.com/zoom/videosdk-zoom-ui-toolkit-vuejs-sample) | Composition API |
| Angular | [videosdk-zoom-ui-toolkit-angular-sample](https://github.com/zoom/videosdk-zoom-ui-toolkit-angular-sample) | Services, Guards |
| JavaScript | [videosdk-zoom-ui-toolkit-javascript-sample](https://github.com/zoom/videosdk-zoom-ui-toolkit-javascript-sample) | Vanilla JS |
| Auth Endpoint | [videosdk-auth-endpoint-sample](https://github.com/zoom/videosdk-auth-endpoint-sample) | Node.js JWT |

## 🌐 External Resources

- **Official Documentation**: https://developers.zoom.us/docs/zoom-video-sdk/web/zoom-ui-toolkit/
- **API Reference**: https://marketplacefront.zoom.us/sdk/uitoolkit/web/
- **NPM Package**: https://www.npmjs.com/package/@zoom/videosdk-zoom-ui-toolkit
- **Marketplace**: https://marketplace.zoom.us/
- **Developer Forum**: https://devforum.zoom.us/
- **Live Demo**: https://sdk.zoom.com/videosdk-uitoolkit
- **Changelog**: https://developers.zoom.us/changelog/zoom-ui-toolkit/web/

## 🎓 Learning Path

### Beginner
1. Read [SKILL.md](SKILL.md) overview
2. Follow Quick Start - Composite
3. Generate JWT on server
4. Join your first session
5. Explore available features

### Intermediate
1. Try Component Mode
2. Add event listeners
3. Customize theme
4. Add virtual backgrounds
5. Integrate with your framework

### Advanced
1. Access underlying Video SDK
2. Subscribe to quality statistics
3. Handle all edge cases
4. Implement custom layouts
5. Build production-ready app

## 📋 Quick Reference Card

### Minimal Working Example

```javascript
import uitoolkit from "@zoom/videosdk-zoom-ui-toolkit";
import "@zoom/videosdk-zoom-ui-toolkit/dist/videosdk-zoom-ui-toolkit.css";

const config = {
  videoSDKJWT: "YOUR_JWT",
  sessionName: "test-session",
  userName: "User",
  featuresOptions: {
    video: { enable: true },
    audio: { enable: true }
  }
};

uitoolkit.joinSession(document.getElementById("container"), config);
uitoolkit.onSessionJoined(() => console.log("Joined"));
uitoolkit.onSessionClosed(() => uitoolkit.destroy());
```

### Must-Remember Rules

1. ✅ **Always** generate JWT server-side
2. ✅ **Always** call `destroy()` on cleanup
3. ✅ **Always** use React 18 (not 17/19)
4. ✅ **Always** import CSS file
5. ❌ **Never** expose SDK secret client-side
6. ❌ **Never** skip `onSessionClosed` cleanup
7. ❌ **Never** call components before `joinSession`

## 📞 Support

- **Developer Forum**: https://devforum.zoom.us/
- **Developer Support**: https://developers.zoom.us/support/
- **Premier Support**: https://explore.zoom.us/en/support-plans/developer/

---

**Navigation**: [← Back to SKILL.md](SKILL.md)

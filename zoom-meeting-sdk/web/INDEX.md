# Zoom Meeting SDK (Web) - Documentation Index

Quick navigation guide for all Web SDK documentation.

## Start Here

| Document | Description |
|----------|-------------|
| **[SKILL.md](SKILL.md)** | Main entry point - Quick starts for both Client View and Component View |

## By View Type

### Client View (Full-Page)
| Document | Description |
|----------|-------------|
| **[client-view/SKILL.md](client-view/SKILL.md)** | Complete Client View reference |
| [client-view/references/](client-view/references/) | API method documentation |

### Component View (Embeddable)
| Document | Description |
|----------|-------------|
| **[component-view/SKILL.md](component-view/SKILL.md)** | Complete Component View reference |
| [component-view/references/](component-view/references/) | API method documentation |

## Concepts

| Document | Description |
|----------|-------------|
| **[concepts/sharedarraybuffer.md](concepts/sharedarraybuffer.md)** | HD video requirements, COOP/COEP headers |
| **[concepts/browser-support.md](concepts/browser-support.md)** | Feature matrix by browser |

## Examples

| Document | Description |
|----------|-------------|
| [examples/client-view-basic.md](examples/client-view-basic.md) | Basic Client View integration |
| [examples/component-view-react.md](examples/component-view-react.md) | React integration with Component View |

## Troubleshooting

| Document | Description |
|----------|-------------|
| **[troubleshooting/error-codes.md](troubleshooting/error-codes.md)** | All SDK error codes (3000-10000 range) |
| **[troubleshooting/common-issues.md](troubleshooting/common-issues.md)** | Quick diagnostics and fixes |

## By Topic

### Authentication
- [SKILL.md#authentication-endpoint](SKILL.md#authentication-endpoint-required) - Signature generation
- [SKILL.md#authorization-requirements-2026-update](SKILL.md#authorization-requirements-2026-update) - OBF tokens

### HD Video & Performance
- [concepts/sharedarraybuffer.md](concepts/sharedarraybuffer.md) - Enable 720p/1080p

### Events & Callbacks
- [SKILL.md#event-listeners-client-view](SKILL.md#event-listeners-client-view) - Client View events
- [SKILL.md#event-listeners-component-view](SKILL.md#event-listeners-component-view) - Component View events

### Government (ZFG)
- [SKILL.md#zoom-for-government-zfg](SKILL.md#zoom-for-government-zfg) - ZFG configuration

### China CDN
- [SKILL.md#china-cdn](SKILL.md#china-cdn) - China-specific CDN

## Quick Reference

### Client View vs Component View

| Aspect | Client View | Component View |
|--------|-------------|----------------|
| **Object** | `ZoomMtg` | `ZoomMtgEmbedded.createClient()` |
| **API Style** | Callbacks | Promises |
| **Password param** | `passWord` (capital W) | `password` (lowercase) |
| **Events** | `inMeetingServiceListener()` | `on()`/`off()` |

### Key Gotchas

1. **Password spelling differs between views!**
   - Client View: `passWord` (capital W)
   - Component View: `password` (lowercase)

2. **SharedArrayBuffer required for HD features**
   - 720p/1080p video
   - Gallery view (25 videos)
   - Virtual backgrounds

3. **March 2026 Authorization Change**
   - Apps joining external meetings need OBF or ZAK tokens

## External Resources

- **Official docs**: https://developers.zoom.us/docs/zoom-meeting-sdk/web/
- **Client View API**: https://marketplacefront.zoom.us/sdk/meeting/web/index.html
- **Component View API**: https://marketplacefront.zoom.us/sdk/meeting/web/components/index.html
- **GitHub samples**: https://github.com/zoom/meetingsdk-web-sample

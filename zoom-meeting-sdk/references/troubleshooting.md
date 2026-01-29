# Meeting SDK - Troubleshooting

Common issues and solutions for Meeting SDK.

## Overview

Troubleshooting guide for Meeting SDK across all platforms.

## Common Issues

### Join Meeting Failed

| Error | Possible Cause | Solution |
|-------|----------------|----------|
| Invalid signature | JWT malformed or expired | Regenerate signature server-side |
| Meeting not found | Invalid meeting number | Verify meeting exists |
| Wrong password | Password mismatch | Check meeting password |
| Meeting locked | Host locked meeting | Contact host |

**Note:** Error code 0 often means success - check the SDK enum values (e.g., `SDKERR_SUCCESS = 0`).

### Authentication Issues

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| Auth failed | Invalid credentials | Check SDK Key/Secret |
| Token expired | JWT too old | Generate fresh signature |
| Signature invalid | Wrong secret used | Verify SDK Secret |

### No Video

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| Black screen | Permission denied | Request camera permission |
| Video not starting | Camera in use | Close other camera apps |
| Poor quality | Low bandwidth | Check network |

### No Audio

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| Can't hear | Audio not connected | Join audio |
| Muted | User is muted | Check mute state |
| Echo | No echo cancellation | Use headphones |

### Web-Specific Issues

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| SharedArrayBuffer error | Missing headers | Add COOP/COEP headers |
| Component not rendering | Wrong container | Check `zoomAppRoot` element |

## Collecting Logs

See [SDK Logs & Troubleshooting](../../zoom-general/references/sdk-logs-troubleshooting.md) for log collection.

## Getting Support

1. Collect SDK logs
2. Note SDK version and platform
3. Document steps to reproduce
4. Contact [Developer Support](https://devsupport.zoom.us/)

## Resources

- **Developer forum**: https://devforum.zoom.us/
- **Support**: https://devsupport.zoom.us/

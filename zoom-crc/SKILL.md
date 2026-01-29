---
name: zoom-crc
description: |
  Zoom Cloud Room Connector (CRC) API integration guide. Enables SIP/H.323 conference room systems 
  (Cisco, Polycom, etc.) to join Zoom meetings. Covers device registration, dial-in configuration, 
  port management, and room system integration. Use when connecting traditional video conferencing 
  systems to Zoom or managing room connector infrastructure.
---

# Zoom Cloud Room Connector (CRC) API

Connect SIP/H.323 conference room systems to Zoom meetings with Cloud Room Connector.

## Overview

Cloud Room Connector (CRC) enables traditional video conferencing systems (Cisco, Polycom, etc.) to join Zoom meetings via SIP or H.323 protocols. The API manages CRC configurations, dial-in settings, and room system integrations.

## Key Features

| Feature | Description |
|---------|-------------|
| **SIP Device Registration** | Register and manage SIP endpoints |
| **H.323 Device Support** | Connect H.323 conference systems |
| **Dial-In Configuration** | Generate meeting-specific dial strings |
| **Port Management** | Monitor and allocate CRC ports |
| **Room Connector Integration** | Manage room system connections |
| **Multi-Protocol Support** | UDP, TCP, TLS, AUTO transport options |

## Choose Your Integration

| I want to... | Use this |
|--------------|----------|
| Register a SIP conference room | **SIP Devices API** |
| Connect H.323 system to Zoom | **H.323 Devices API** |
| Get meeting dial-in info | **Dial-In Information API** |
| Manage CRC account settings | **CRC Settings API** |
| Monitor port usage | **Port Management API** |
| List all room connectors | **Room Connectors API** |

## CRC Settings

Manage account-level CRC configuration and port allocation.

### Get CRC Settings

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/accounts/{accountId}/crc',
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const settings = await response.json();
// {
//   "enabled": true,
//   "sip_uri": "meeting_id@zoomcrc.com",
//   "h323_ip_addresses": ["162.255.37.11", "162.255.36.11"],
//   "ports_allocated": 10,
//   "ports_in_use": 3
// }
```

### Update CRC Settings

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/accounts/{accountId}/crc',
  {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      enabled: true,
      sip_uri: 'meeting_id@zoomcrc.com'
    })
  }
);
```

## SIP Device Management

Register and manage SIP conference room endpoints.

### Register SIP Device

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/sip_phones',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      authorization_name: 'conf-room-1',
      domain: 'sip.company.com',
      user_name: 'conference_room_1',
      password: 'secure_password',
      voice_mail: 'Conference Room 1',
      transport_protocol: 'TLS',
      registration_expire_time: 60
    })
  }
);

const device = await response.json();
// Returns device ID and registration details
```

### List SIP Devices

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/sip_phones',
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const devices = await response.json();
// devices.sip_phones contains array of registered devices
```

### Get SIP Device Details

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/sip_phones/{deviceId}',
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const device = await response.json();
```

### Update SIP Device

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/sip_phones/{deviceId}',
  {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      password: 'new_secure_password',
      registration_expire_time: 120
    })
  }
);
```

### Delete SIP Device

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/sip_phones/{deviceId}',
  {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);
```

## H.323 Device Management

Connect H.323 conference systems to Zoom.

### Register H.323 Device

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/h323/devices',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: 'Cisco Telepresence Room',
      h323_device_type: 'cisco',
      device_ip: '192.168.1.100',
      device_port: 1719,
      registration_expire_time: 60
    })
  }
);

const device = await response.json();
```

### List H.323 Devices

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/h323/devices',
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const devices = await response.json();
// devices.h323_devices contains array of registered devices
```

## Meeting Dial-In Information

Get SIP/H.323 dial-in details for specific meetings.

### Get SIP Dial-In Info

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/meetings/{meetingId}/sip_dialing',
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const dialInfo = await response.json();
// {
//   "sip_dialing": {
//     "uri": "12345678910@zoomcrc.com",
//     "password": "abc123",
//     "ip_addresses": ["162.255.37.11", "162.255.36.11"]
//   }
// }
```

### Get H.323 Dial-In Info

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/meetings/{meetingId}/h323_dialing',
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const dialInfo = await response.json();
// {
//   "h323_dialing": {
//     "ip_addresses": ["162.255.37.11", "162.255.36.11"],
//     "meeting_id": "12345678910",
//     "passcode": "abc123"
//   }
// }
```

## Dial String Formats

### SIP URI Format

```
{meeting_id}.{passcode}@zoomcrc.com
```

**Example**: `12345678910.123456@zoomcrc.com`

### H.323 Format

```
IP: 162.255.37.11
Meeting ID: {meeting_id}
Passcode: {passcode}
```

**Example**:
- IP: 162.255.37.11
- Meeting ID: 12345678910
- Passcode: 123456

## Device Registration Fields

| Field | Type | Description |
|-------|------|-------------|
| `authorization_name` | string | Unique device identifier |
| `domain` | string | SIP domain |
| `user_name` | string | Registration username |
| `password` | string | Registration password |
| `transport_protocol` | string | UDP, TCP, TLS, AUTO |
| `registration_expire_time` | integer | Expiration in seconds |
| `voice_mail` | string | Voicemail display name |

## Port Management

Monitor CRC port allocation and usage.

### Get Port Usage

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/accounts/{accountId}/crc/ports',
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const portInfo = await response.json();
// {
//   "ports_allocated": 10,
//   "ports_in_use": 3,
//   "ports_available": 7
// }
```

## Room Connectors

List and manage room connector infrastructure.

### List Room Connectors

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/rooms/connectors',
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const connectors = await response.json();
// connectors.connectors contains array of room connectors
```

### Get Room Connector Details

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/rooms/connectors/{connectorId}',
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const connector = await response.json();
```

## API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/accounts/{accountId}/crc` | Get CRC settings |
| PATCH | `/accounts/{accountId}/crc` | Update CRC settings |
| GET | `/accounts/{accountId}/crc/ports` | Get port usage |
| GET | `/sip_phones` | List SIP devices |
| POST | `/sip_phones` | Register SIP device |
| GET | `/sip_phones/{deviceId}` | Get SIP device |
| PATCH | `/sip_phones/{deviceId}` | Update SIP device |
| DELETE | `/sip_phones/{deviceId}` | Delete SIP device |
| GET | `/h323/devices` | List H.323 devices |
| POST | `/h323/devices` | Register H.323 device |
| GET | `/h323/devices/{deviceId}` | Get H.323 device |
| PATCH | `/h323/devices/{deviceId}` | Update H.323 device |
| DELETE | `/h323/devices/{deviceId}` | Delete H.323 device |
| GET | `/rooms/connectors` | List room connectors |
| GET | `/rooms/connectors/{connectorId}` | Get connector details |
| GET | `/meetings/{meetingId}/sip_dialing` | Get SIP dial-in info |
| GET | `/meetings/{meetingId}/h323_dialing` | Get H.323 dial-in info |

## Authentication

Requires OAuth 2.0 with CRC scopes:

| Scope | Description |
|-------|-------------|
| `crc:read` | Read CRC configurations |
| `crc:write` | Manage CRC settings |
| `crc:read:admin` | Admin read access |
| `crc:write:admin` | Admin write access |

See **zoom-oauth** skill for authentication setup.

## Prerequisites

1. **CRC License** - Account must have CRC enabled
2. **OAuth app** - Create in [Zoom App Marketplace](https://marketplace.zoom.us/)
3. **Scopes** - See [references/scopes.md](references/scopes.md) for required permissions
4. **Room Systems** - Cisco, Polycom, or compatible SIP/H.323 devices

## Common Use Cases

| Use Case | Description | Integration |
|----------|-------------|-------------|
| **Conference Room Integration** | Connect room systems to Zoom | SIP/H.323 Device APIs |
| **Multi-Site Meetings** | Enable remote sites to join | CRC Settings + Dial-In APIs |
| **Device Provisioning** | Automate room system setup | Device Registration APIs |
| **Port Monitoring** | Track CRC resource usage | Port Management API |
| **Meeting Dial-In** | Generate dial strings for rooms | Dial-In Information API |
| **Room Connector Management** | Manage infrastructure | Room Connectors API |

## Detailed References

- **[references/crc.md](references/crc.md)** - CRC API reference
- **[references/sip-devices.md](references/sip-devices.md)** - SIP device integration
- **[references/h323-devices.md](references/h323-devices.md)** - H.323 device integration
- **[references/dial-strings.md](references/dial-strings.md)** - Dial string formats
- **[references/scopes.md](references/scopes.md)** - Required OAuth scopes

## Resources

- **Official docs**: https://developers.zoom.us/docs/crc/
- **API Reference**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Cloud-Room-Connector
- **SIP/H.323 Guide**: https://support.zoom.us/hc/en-us/articles/201363273
- **Room Connector Setup**: https://support.zoom.us/hc/en-us/articles/202175286
- **Marketplace**: https://marketplace.zoom.us/

# Compliance & Security

HIPAA, GDPR, and security considerations for Zoom integrations.

## Overview

When building Zoom integrations, you must consider regulatory requirements like HIPAA (healthcare), GDPR (EU privacy), and general security best practices.

---

## HIPAA Compliance

### Zoom's HIPAA Support

Zoom offers HIPAA-compliant plans for healthcare:
- Business Associate Agreement (BAA) required
- Available on Healthcare plan
- Specific features must be enabled

### Your Application's Responsibility

Even with Zoom's HIPAA compliance, your app must also be compliant:

| Requirement | Your Responsibility |
|-------------|---------------------|
| BAA with Zoom | Request from Zoom sales |
| Encryption at rest | Encrypt stored recordings/data |
| Access controls | Implement role-based access |
| Audit logs | Log all PHI access |
| Data retention | Follow retention policies |
| Breach notification | Have incident response plan |

### Recording Handling

```javascript
// Encrypt recordings before storage
const crypto = require('crypto');

async function storeRecordingEncrypted(recordingBuffer, meetingId) {
  // Generate encryption key (store securely, e.g., AWS KMS)
  const key = await getEncryptionKey(meetingId);
  
  // Encrypt
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  const encrypted = Buffer.concat([
    cipher.update(recordingBuffer),
    cipher.final()
  ]);
  const authTag = cipher.getAuthTag();
  
  // Store encrypted data
  await storage.put(`recordings/${meetingId}`, {
    iv: iv.toString('base64'),
    authTag: authTag.toString('base64'),
    data: encrypted.toString('base64')
  });
  
  // Log access
  await auditLog.write({
    action: 'RECORDING_STORED',
    meetingId,
    timestamp: new Date(),
    encrypted: true
  });
}
```

### Audit Logging

```javascript
// Comprehensive audit logging
class AuditLogger {
  async log(event) {
    const entry = {
      timestamp: new Date().toISOString(),
      eventType: event.type,
      userId: event.userId,
      resourceType: event.resourceType,
      resourceId: event.resourceId,
      action: event.action,
      ipAddress: event.ipAddress,
      userAgent: event.userAgent,
      success: event.success,
      details: event.details
    };
    
    // Write to immutable log store
    await this.writeToAuditLog(entry);
    
    // Alert on sensitive actions
    if (this.isSensitiveAction(event.action)) {
      await this.alertSecurityTeam(entry);
    }
  }
  
  isSensitiveAction(action) {
    return [
      'PHI_ACCESSED',
      'RECORDING_DOWNLOADED',
      'PATIENT_DATA_EXPORTED',
      'ADMIN_ACTION'
    ].includes(action);
  }
}
```

---

## GDPR Compliance

### Key Requirements

| Requirement | Implementation |
|-------------|----------------|
| **Consent** | Get explicit consent before processing |
| **Right to Access** | Provide data export feature |
| **Right to Deletion** | Implement data deletion |
| **Data Portability** | Export in machine-readable format |
| **Breach Notification** | 72-hour notification requirement |
| **Privacy by Design** | Minimize data collection |

### Data Subject Requests

```javascript
// Handle GDPR data subject requests
class GDPRController {
  
  // Right to Access - Export user's data
  async exportUserData(userId) {
    const data = {
      profile: await this.getUserProfile(userId),
      meetings: await this.getUserMeetings(userId),
      recordings: await this.getUserRecordings(userId),
      chatHistory: await this.getUserChats(userId),
      webhookEvents: await this.getUserEvents(userId)
    };
    
    await this.auditLog.log({
      action: 'GDPR_DATA_EXPORT',
      userId,
      timestamp: new Date()
    });
    
    return data;
  }
  
  // Right to Deletion - Delete user's data
  async deleteUserData(userId) {
    // Delete from all tables
    await this.db.query('DELETE FROM user_profiles WHERE user_id = $1', [userId]);
    await this.db.query('DELETE FROM meeting_data WHERE user_id = $1', [userId]);
    await this.db.query('DELETE FROM recordings WHERE user_id = $1', [userId]);
    
    // Delete from object storage
    await this.storage.deletePrefix(`users/${userId}/`);
    
    // Log deletion (keep minimal audit record)
    await this.auditLog.log({
      action: 'GDPR_DATA_DELETION',
      userId,
      timestamp: new Date()
    });
    
    return { success: true, deletedAt: new Date() };
  }
  
  // Data Portability - Export in standard format
  async exportPortableData(userId) {
    const data = await this.exportUserData(userId);
    
    // Return in JSON format (machine-readable)
    return {
      format: 'application/json',
      schema: 'https://yourapp.com/schemas/user-data-v1',
      exportedAt: new Date().toISOString(),
      data
    };
  }
}
```

### Consent Management

```javascript
// Track consent for processing
async function recordConsent(userId, consentType, granted) {
  await db.query(`
    INSERT INTO user_consents (user_id, consent_type, granted, timestamp, ip_address)
    VALUES ($1, $2, $3, $4, $5)
  `, [userId, consentType, granted, new Date(), ipAddress]);
}

// Check consent before processing
async function hasConsent(userId, consentType) {
  const result = await db.query(`
    SELECT granted FROM user_consents 
    WHERE user_id = $1 AND consent_type = $2
    ORDER BY timestamp DESC LIMIT 1
  `, [userId, consentType]);
  
  return result.rows[0]?.granted === true;
}

// Example: Check before storing recording
async function handleRecording(userId, recording) {
  if (!await hasConsent(userId, 'recording_storage')) {
    throw new Error('User has not consented to recording storage');
  }
  
  await storeRecording(recording);
}
```

---

## Security Best Practices

### Token Security

```javascript
// Never log tokens
const sanitizeForLogging = (obj) => {
  const sanitized = { ...obj };
  const sensitiveKeys = ['access_token', 'refresh_token', 'password', 'secret'];
  
  sensitiveKeys.forEach(key => {
    if (sanitized[key]) {
      sanitized[key] = '[REDACTED]';
    }
  });
  
  return sanitized;
};

// Store tokens encrypted
const encryptToken = (token) => {
  const cipher = crypto.createCipheriv('aes-256-gcm', encryptionKey, iv);
  return Buffer.concat([cipher.update(token, 'utf8'), cipher.final()]).toString('base64');
};
```

### Webhook Security

```javascript
// Always verify webhook signatures
function verifyWebhookSignature(req) {
  const signature = req.headers['x-zm-signature'];
  const timestamp = req.headers['x-zm-request-timestamp'];
  
  // Prevent replay attacks
  const now = Math.floor(Date.now() / 1000);
  if (Math.abs(now - parseInt(timestamp)) > 300) {
    return false;
  }
  
  const payload = `v0:${timestamp}:${JSON.stringify(req.body)}`;
  const expectedSig = 'v0=' + crypto
    .createHmac('sha256', WEBHOOK_SECRET)
    .update(payload)
    .digest('hex');
  
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expectedSig)
  );
}
```

### Input Validation

```javascript
const Joi = require('joi');

// Validate meeting creation input
const meetingSchema = Joi.object({
  topic: Joi.string().max(200).required(),
  type: Joi.number().valid(1, 2, 3, 8).required(),
  duration: Joi.number().min(1).max(1440),
  password: Joi.string().max(10).pattern(/^[a-zA-Z0-9@\-_*]+$/),
  start_time: Joi.date().iso().greater('now')
});

async function createMeeting(req, res) {
  const { error, value } = meetingSchema.validate(req.body);
  
  if (error) {
    return res.status(400).json({ error: error.details[0].message });
  }
  
  // Proceed with validated data
  const meeting = await zoomClient.createMeeting(value);
  res.json(meeting);
}
```

### API Key Management

```javascript
// Use environment variables, never hardcode
const config = {
  clientId: process.env.ZOOM_CLIENT_ID,
  clientSecret: process.env.ZOOM_CLIENT_SECRET,
  webhookSecret: process.env.ZOOM_WEBHOOK_SECRET
};

// Validate config on startup
function validateConfig() {
  const required = ['ZOOM_CLIENT_ID', 'ZOOM_CLIENT_SECRET', 'ZOOM_WEBHOOK_SECRET'];
  
  const missing = required.filter(key => !process.env[key]);
  
  if (missing.length > 0) {
    throw new Error(`Missing environment variables: ${missing.join(', ')}`);
  }
}
```

---

## Data Residency

### Handle Regional Requirements

```javascript
// Determine storage region based on user location
async function getStorageRegion(accountId) {
  const accountInfo = await zoomClient.getAccountInfo(accountId);
  
  // Map Zoom data center to storage region
  const regionMap = {
    'US': 'us-east-1',
    'EU': 'eu-west-1',
    'AU': 'ap-southeast-2',
    'IN': 'ap-south-1'
  };
  
  return regionMap[accountInfo.data_residency_region] || 'us-east-1';
}

// Store data in correct region
async function storeData(accountId, data) {
  const region = await getStorageRegion(accountId);
  const regionalStorage = getStorageClient(region);
  
  await regionalStorage.put(data);
}
```

---

## Security Checklist

### Before Going Live

- [ ] OAuth tokens encrypted at rest
- [ ] Webhook signatures verified
- [ ] Input validation on all endpoints
- [ ] Rate limiting implemented
- [ ] Audit logging enabled
- [ ] Error messages don't leak sensitive info
- [ ] HTTPS enforced everywhere
- [ ] Dependencies updated (no known vulnerabilities)
- [ ] Penetration testing completed
- [ ] Incident response plan documented

### Ongoing

- [ ] Regular security audits
- [ ] Dependency vulnerability scanning
- [ ] Log monitoring for anomalies
- [ ] Token rotation procedures
- [ ] Backup and recovery tested

## Resources

- **Zoom Security**: https://zoom.us/security
- **HIPAA Compliance**: https://zoom.us/healthcare
- **GDPR**: https://zoom.us/gdpr
- **Trust Center**: https://trust.zoom.us/

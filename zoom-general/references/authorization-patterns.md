# Authorization Patterns

Permission validation middleware and role-based access control for Zoom API integrations.

## Overview

When chaining multiple Zoom API calls, each step may require different scopes and permissions. This document provides patterns for validating authorization at each step before proceeding.

## Authorization Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     AUTHORIZATION VALIDATION FLOW                        │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ 1. Check Token Validity                                                 │
│    └── Is token expired? → Refresh or re-authenticate                  │
│    └── Is token revoked? → Re-authenticate                             │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. Validate Required Scopes                                             │
│    └── Does token have scopes for this operation?                       │
│    └── If missing → Return 403 with required scopes                     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. Check Resource Permissions                                           │
│    └── Does user have access to this resource?                          │
│    └── Is user admin/owner/member?                                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4. Execute Operation                                                    │
│    └── Call Zoom API                                                    │
│    └── Handle API-level authorization errors                            │
└─────────────────────────────────────────────────────────────────────────┘
```

## Scope Validation Middleware

### Express.js Middleware

```javascript
const axios = require('axios');

/**
 * Middleware to validate OAuth token has required scopes
 * @param {string[]} requiredScopes - Scopes required for this route
 */
function requireScopes(requiredScopes) {
  return async (req, res, next) => {
    const token = req.headers.authorization?.replace('Bearer ', '');
    
    if (!token) {
      return res.status(401).json({
        error: 'unauthorized',
        message: 'No access token provided'
      });
    }
    
    try {
      // Get token info to check scopes
      const tokenInfo = await getTokenInfo(token);
      
      // Check if token has all required scopes
      const tokenScopes = tokenInfo.scope.split(' ');
      const missingScopes = requiredScopes.filter(
        scope => !tokenScopes.includes(scope)
      );
      
      if (missingScopes.length > 0) {
        return res.status(403).json({
          error: 'insufficient_scope',
          message: 'Token missing required scopes',
          required_scopes: requiredScopes,
          missing_scopes: missingScopes,
          your_scopes: tokenScopes
        });
      }
      
      // Attach token info to request for downstream use
      req.zoomToken = tokenInfo;
      req.zoomScopes = tokenScopes;
      next();
      
    } catch (error) {
      if (error.response?.status === 401) {
        return res.status(401).json({
          error: 'invalid_token',
          message: 'Token is invalid or expired'
        });
      }
      next(error);
    }
  };
}

/**
 * Get token information including scopes
 */
async function getTokenInfo(accessToken) {
  // Decode JWT to get scopes (for Server-to-Server OAuth)
  // Or call token introspection endpoint
  const parts = accessToken.split('.');
  if (parts.length === 3) {
    const payload = JSON.parse(Buffer.from(parts[1], 'base64').toString());
    return {
      scope: payload.scope || '',
      exp: payload.exp,
      aud: payload.aud
    };
  }
  
  // For user OAuth tokens, call the /users/me endpoint to verify
  const response = await axios.get('https://api.zoom.us/v2/users/me', {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  });
  
  return {
    scope: response.headers['x-zm-scopes'] || '',
    user_id: response.data.id
  };
}

// Usage
const express = require('express');
const app = express();

// Route requiring meeting:read scope
app.get('/api/meetings/:id',
  requireScopes(['meeting:read']),
  async (req, res) => {
    // Token already validated, proceed with API call
    const meeting = await getMeeting(req.params.id, req.headers.authorization);
    res.json(meeting);
  }
);

// Route requiring multiple scopes
app.post('/api/users/:id/meetings',
  requireScopes(['user:read', 'meeting:write']),
  async (req, res) => {
    const meeting = await createMeeting(req.params.id, req.body, req.headers.authorization);
    res.json(meeting);
  }
);
```

### Scope Requirements by Operation

| Operation | Required Scopes |
|-----------|-----------------|
| List users | `user:read:admin` |
| Create user | `user:write:admin` |
| Get meeting | `meeting:read` or `meeting:read:admin` |
| Create meeting | `meeting:write` or `meeting:write:admin` |
| List recordings | `recording:read` or `recording:read:admin` |
| Delete recording | `recording:write` or `recording:write:admin` |
| Access phone | `phone:read`, `phone:write` |

## Role-Based Access Control

### Define Roles

```javascript
/**
 * Role definitions with allowed scopes
 */
const ROLES = {
  admin: {
    scopes: [
      'user:read:admin', 'user:write:admin',
      'meeting:read:admin', 'meeting:write:admin',
      'recording:read:admin', 'recording:write:admin',
      'account:read:admin', 'account:write:admin'
    ],
    description: 'Full administrative access'
  },
  
  manager: {
    scopes: [
      'user:read:admin',
      'meeting:read:admin', 'meeting:write:admin',
      'recording:read:admin'
    ],
    description: 'Manage meetings and view users'
  },
  
  user: {
    scopes: [
      'user:read',
      'meeting:read', 'meeting:write',
      'recording:read'
    ],
    description: 'Manage own meetings and recordings'
  },
  
  viewer: {
    scopes: [
      'meeting:read',
      'recording:read'
    ],
    description: 'View-only access'
  }
};

/**
 * Check if user role has required scope
 */
function roleHasScope(role, requiredScope) {
  const roleConfig = ROLES[role];
  if (!roleConfig) return false;
  
  return roleConfig.scopes.some(scope => {
    // Exact match
    if (scope === requiredScope) return true;
    
    // Admin scope covers non-admin version
    // e.g., meeting:read:admin covers meeting:read
    if (scope.endsWith(':admin')) {
      const baseScope = scope.replace(':admin', '');
      if (baseScope === requiredScope) return true;
    }
    
    return false;
  });
}

/**
 * Middleware to require a specific role
 */
function requireRole(allowedRoles) {
  return (req, res, next) => {
    const userRole = req.user?.role; // From your auth system
    
    if (!userRole || !allowedRoles.includes(userRole)) {
      return res.status(403).json({
        error: 'forbidden',
        message: 'Insufficient role permissions',
        required_roles: allowedRoles,
        your_role: userRole || 'none'
      });
    }
    
    next();
  };
}

// Usage
app.delete('/api/users/:id',
  requireRole(['admin']),
  requireScopes(['user:write:admin']),
  async (req, res) => {
    // Only admins can delete users
    await deleteUser(req.params.id);
    res.json({ success: true });
  }
);
```

## Permission Checking Between Chained Operations

### Chain Validation Pattern

```javascript
/**
 * Validate permissions for a multi-step operation
 * before executing any steps
 */
async function validateChainPermissions(operations, tokenScopes) {
  const allRequiredScopes = new Set();
  
  for (const op of operations) {
    for (const scope of op.requiredScopes) {
      allRequiredScopes.add(scope);
    }
  }
  
  const missingScopes = [...allRequiredScopes].filter(
    scope => !tokenScopes.includes(scope)
  );
  
  if (missingScopes.length > 0) {
    return {
      valid: false,
      missingScopes,
      message: `Cannot complete operation chain. Missing scopes: ${missingScopes.join(', ')}`
    };
  }
  
  return { valid: true };
}

/**
 * Execute a chain of operations with permission validation
 */
async function executeAuthorizedChain(operations, accessToken) {
  // Get token scopes
  const tokenInfo = await getTokenInfo(accessToken);
  const tokenScopes = tokenInfo.scope.split(' ');
  
  // Validate all permissions upfront
  const validation = await validateChainPermissions(operations, tokenScopes);
  if (!validation.valid) {
    throw new Error(validation.message);
  }
  
  // Execute operations in sequence
  const results = [];
  for (const op of operations) {
    console.log(`Executing: ${op.name}`);
    
    try {
      const result = await op.execute(accessToken, results);
      results.push({ name: op.name, success: true, data: result });
    } catch (error) {
      // Check if it's an authorization error
      if (error.response?.status === 403) {
        throw new Error(`Authorization failed at step "${op.name}": ${error.response.data.message}`);
      }
      throw error;
    }
  }
  
  return results;
}

// Example: User + Meeting creation chain
const userMeetingChain = [
  {
    name: 'createUser',
    requiredScopes: ['user:write:admin'],
    execute: async (token, previousResults) => {
      return await createUser({
        email: 'new@example.com',
        firstName: 'New',
        lastName: 'User'
      }, token);
    }
  },
  {
    name: 'createMeeting',
    requiredScopes: ['meeting:write:admin'],
    execute: async (token, previousResults) => {
      const user = previousResults.find(r => r.name === 'createUser').data;
      return await createMeeting(user.id, {
        topic: 'Onboarding Meeting'
      }, token);
    }
  }
];

// Usage
try {
  const results = await executeAuthorizedChain(userMeetingChain, accessToken);
  console.log('Chain completed:', results);
} catch (error) {
  console.error('Chain failed:', error.message);
}
```

## Graceful Degradation

### Handle Partial Permissions

```javascript
/**
 * Execute with graceful degradation when permissions are partial
 */
async function executeWithDegradation(operations, accessToken) {
  const tokenInfo = await getTokenInfo(accessToken);
  const tokenScopes = tokenInfo.scope.split(' ');
  
  const results = [];
  
  for (const op of operations) {
    // Check if we have permission for this operation
    const hasPermission = op.requiredScopes.every(
      scope => tokenScopes.includes(scope)
    );
    
    if (!hasPermission) {
      if (op.required) {
        // Required operation - fail the chain
        throw new Error(`Missing required scopes for ${op.name}: ${op.requiredScopes.join(', ')}`);
      } else {
        // Optional operation - skip with warning
        console.warn(`Skipping ${op.name}: insufficient permissions`);
        results.push({
          name: op.name,
          skipped: true,
          reason: 'insufficient_permissions',
          required_scopes: op.requiredScopes
        });
        continue;
      }
    }
    
    // Execute operation
    const result = await op.execute(accessToken, results);
    results.push({ name: op.name, success: true, data: result });
  }
  
  return results;
}

// Example with optional operations
const meetingWithOptionalRecording = [
  {
    name: 'getMeeting',
    required: true,
    requiredScopes: ['meeting:read'],
    execute: async (token) => getMeetingDetails(meetingId, token)
  },
  {
    name: 'getRecordings',
    required: false, // Optional - won't fail chain
    requiredScopes: ['recording:read'],
    execute: async (token, prev) => {
      const meeting = prev.find(r => r.name === 'getMeeting').data;
      return getRecordings(meeting.uuid, token);
    }
  }
];
```

## Authorization Decision Flowchart

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      AUTHORIZATION DECISION FLOW                          │
└──────────────────────────────────────────────────────────────────────────┘

                        ┌─────────────────┐
                        │  Receive Request │
                        └────────┬────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │  Is token present?     │
                    └───────────┬────────────┘
                                │
                    ┌───────────┴───────────┐
                    │ NO                    │ YES
                    ▼                       ▼
            ┌───────────────┐     ┌────────────────────┐
            │ Return 401    │     │ Is token valid?    │
            │ Unauthorized  │     └─────────┬──────────┘
            └───────────────┘               │
                                ┌───────────┴───────────┐
                                │ NO                    │ YES
                                ▼                       ▼
                        ┌───────────────┐     ┌────────────────────┐
                        │ Return 401    │     │ Has required       │
                        │ Invalid Token │     │ scopes?            │
                        └───────────────┘     └─────────┬──────────┘
                                                        │
                                            ┌───────────┴───────────┐
                                            │ NO                    │ YES
                                            ▼                       ▼
                                    ┌───────────────┐     ┌────────────────────┐
                                    │ Return 403    │     │ Has resource       │
                                    │ Insufficient  │     │ access?            │
                                    │ Scope         │     └─────────┬──────────┘
                                    └───────────────┘               │
                                                        ┌───────────┴───────────┐
                                                        │ NO                    │ YES
                                                        ▼                       ▼
                                                ┌───────────────┐     ┌────────────────┐
                                                │ Return 403    │     │ Execute        │
                                                │ Forbidden     │     │ Operation      │
                                                └───────────────┘     └────────────────┘
```

## Common Authorization Errors

| Status | Error | Cause | Solution |
|--------|-------|-------|----------|
| 401 | `invalid_token` | Token expired or revoked | Refresh token or re-authenticate |
| 401 | `unauthorized` | No token provided | Include Authorization header |
| 403 | `insufficient_scope` | Token missing required scope | Request additional scopes |
| 403 | `forbidden` | User lacks resource access | Check user permissions |
| 403 | `access_denied` | Admin-only operation | Use admin account |

## Best Practices

1. **Validate upfront** - Check all permissions before starting a chain
2. **Fail fast** - Return clear error messages with required scopes
3. **Graceful degradation** - Skip optional steps rather than fail entirely
4. **Audit logging** - Log all authorization decisions
5. **Principle of least privilege** - Request only needed scopes
6. **Token caching** - Cache token info to avoid repeated validation calls

## Resources

- **OAuth Scopes Reference**: https://developers.zoom.us/docs/integrations/oauth-scopes/
- **API Error Codes**: https://developers.zoom.us/docs/api/rest/error-handling/
- **Authentication Guide**: [authentication.md](authentication.md)
- **Scopes Reference**: [scopes.md](scopes.md)

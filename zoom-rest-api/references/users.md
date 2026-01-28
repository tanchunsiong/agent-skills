# REST API - Users

User management endpoints.

## Overview

Manage Zoom users - list, create, update, and delete users.

## Endpoints

### List Users

```bash
GET /users
```

Query parameters:
- `status` - active, inactive, pending
- `page_size` - Results per page (max 300)
- `page_number` - Page number

### Get User

```bash
GET /users/{userId}
```

### Create User

```bash
POST /users
```

```json
{
  "action": "create",
  "user_info": {
    "email": "user@example.com",
    "type": 1,
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### Update User

```bash
PATCH /users/{userId}
```

### Delete User

```bash
DELETE /users/{userId}
```

## User Types

| Type | Value | Description |
|------|-------|-------------|
| Basic | 1 | Free user |
| Licensed | 2 | Paid license |
| On-prem | 3 | On-premise user |

## Required Scopes

- `user:read` - View users
- `user:write` - Create/update/delete users

## Resources

- **API Reference**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Users

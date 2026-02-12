# Two Roles Pattern

Zoom Cobrowse uses two roles:

- `role_type=1`: customer session
- `role_type=2`: agent session

Use separate JWTs for each role and keep token generation on the server.

See:
- [Get Started](../get-started.md)
- [Authorization (official)](../references/authorization-official.md)

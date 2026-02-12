# Common Issues

Quick diagnostics for Zoom CoBrowse SDK issues.

- Ensure SDK script/package is loaded.
- Verify role-specific JWT generation on server.
- Validate token expiry and clock skew.
- Confirm session PIN flow between customer and agent.

## Docs Links / 404s

**Symptom**: Official doc links you found are stale or return 404.

**Fix**:
- Prefer the curated references under `references/` (these are meant to stay stable even if external URLs drift).
- If you need working code, start from official sample repos referenced by the skill, then adapt to your stack.

## Confusing "Who Creates the Session?"

**Symptom**: You built an "agent creates session" endpoint, but the customer flow seems to actually start the share / generate the PIN.

**Fix**:
- Treat **customer start/share** as the action that creates the shareable context (PIN/session), then the **agent joins** using that PIN/session info.
- Keep your server responsibilities narrow: token minting, optional auditing, and routing; avoid inventing "session creation" semantics that the SDK already owns.

## Plain HTML / Express Integration Friction

**Symptom**: Quickstarts assume Vite/modern build pipeline; your plain HTML/Express adaptation breaks.

**Fix**:
- Load the SDK exactly as the official snippet expects (script order matters).
- Avoid bundler-only patterns in plain HTML (ESM imports, `import.meta`, etc.) unless you add a bundler.

See:
- [Get Started](../get-started.md)
- [Get Started (official)](../references/get-started-official.md)

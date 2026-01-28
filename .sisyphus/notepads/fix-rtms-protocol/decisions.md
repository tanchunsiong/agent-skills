# Decisions - RTMS Protocol Fixes

## [2026-01-28] Execution Strategy
- Process files ONE AT A TIME (subagents refuse batches per their directive)
- Use category="quick" for single-file surgical fixes
- Verify each file after fix with grep

# Shared Report Format for Review Skills

## Severity Levels

All review skills use the same three severity levels:

- **BLOCKING** — Must be fixed before merge. The issue will cause a test failure, production bug, security vulnerability, or data loss.
- **WARNING** — Likely unintended or fragile. Needs human review before merging.
- **SUGGESTION** — Not a rule violation, but a safer or cleaner alternative exists.

## Report Structure

Every review report must include:

1. **Section per check area** — each with findings or "No violations"
2. **Per-finding details** — file path, line number (if applicable), issue description, and a concrete fix
3. **Summary line** — `[BLOCKING count] [WARNING count] [SUGGESTION count]`

## Summary Line Format

```
### Summary
[N] BLOCKING  [N] WARNING  [N] SUGGESTION
```

## Domain-Specific Severity Guidance

Each review skill defines what constitutes BLOCKING vs WARNING for its domain.
Refer to the individual skill's `references/checks.md` for the detailed mapping.

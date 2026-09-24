@../AGENTS.md

## Skills

Skills for this project live in `.github/skills/` as SKILL.md files. They are
**not** registered in Claude Code's built-in skill registry and must never be
invoked via the Skill tool.

**Invocation:** When a task matches a skill listed in the skills table in
AGENTS.md (Section 6), read `.github/skills/<skill>/SKILL.md` and follow its
instructions. When the user names a skill directly, do the same.

Do **not** scan all skill directories to discover skills — use the table in
AGENTS.md as the lookup index.

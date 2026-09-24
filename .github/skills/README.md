# GitHub Skills

Skills are reusable prompt-driven automations for AI coding agents. Agents
discover skills via the lookup table in `AGENTS.md` (Section 6) and invoke
them by reading the corresponding `SKILL.md` file.

This README is for **human contributors**. Agents do not read this file.

## What is a skill?

A skill is a directory containing a `SKILL.md` file with YAML frontmatter and
markdown instructions. Skills follow the [agentskills.io specification](https://agentskills.io/specification).

## How agents discover skills

Agents use the **skills lookup table** in `AGENTS.md` (Section 6) to match
tasks to skills. They do **not** scan skill directories at startup.

Once a skill is selected, its content loads progressively:

1. **Instructions (<5000 tokens)** — the full `SKILL.md` body is loaded when
   the skill is activated.
2. **Resources (on demand)** — files in `scripts/`, `references/`, or `assets/`
   are loaded only when the instructions reference them.

## Directory layout

```
.github/skills/
  README.md              # This file (human-facing)
  <skill-name>/          # One directory per skill
    SKILL.md             # Required — skill definition with frontmatter
    scripts/             # Optional — executable code
    references/          # Optional — additional documentation
    assets/              # Optional — templates, schemas, static resources
```

## SKILL.md format

Each `SKILL.md` file **must** start with YAML frontmatter containing at least
`name` and `description`:

```markdown
---
name: my-skill-name
description: "A clear description of what this skill does and when to use it. Include keywords that help agents match user requests to this skill."
---

## Instructions

Step-by-step instructions for the agent to follow.

## Validation

(Optional) How to verify the skill executed successfully.

## Examples

(Optional) Example scenarios or edge cases.
```

### Required frontmatter fields

| Field         | Constraints                                                                                                                |
| ------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `name`        | 1-64 chars. Lowercase alphanumeric + hyphens only. Must match the directory name. No leading/trailing/consecutive hyphens. |
| `description` | 1-1024 chars. Describes what the skill does **and** when to use it. Include specific keywords for semantic matching.       |

### Optional frontmatter fields

| Field           | Purpose                                                    |
| --------------- | ---------------------------------------------------------- |
| `license`       | License name or reference to a bundled license file.       |
| `compatibility` | Environment requirements (tools, network access, etc.).    |
| `metadata`      | Arbitrary key-value pairs (author, version, etc.).         |
| `allowed-tools` | Space-delimited list of pre-approved tools. (Experimental) |

### Body guidelines

- Keep `SKILL.md` under **500 lines**.
- Move detailed reference material to `references/` files.
- Use relative paths when referencing other files in the skill directory.
- Keep file references one level deep from `SKILL.md`.

## Current skills

The catalog with "use when…" triggers is the skills table in [`AGENTS.md`](../../AGENTS.md#skills); add new skills there.

## When to add a skill

Add a skill when you find yourself giving the same multi-step instructions to
an AI agent more than once. Good candidates:

- Aligning the SDKs with a new External API spec
- Commit-message formatting and PR creation
- Running a specific test suite with pre/post steps
- Regenerating clients or preparing release notes

## Adding a new skill

1. Create a new subdirectory: `.github/skills/<skill-name>/`
    - Use kebab-case for the directory name (e.g., `sdk-run-integration-tests`); prefix `sdk-` for SDK code and review, `ci-` for workflows and release scripts
    - The directory name **must** match the `name` field in frontmatter

2. Create `SKILL.md` inside the directory
    - **Must** be named `SKILL.md` (case-sensitive)
    - **Must** include YAML frontmatter with `name` and `description`
    - Write clear, actionable instructions in the body
    - Include keywords in the `description` for semantic matching

3. Test the skill
    - Ask an AI agent to perform a task that should trigger the skill
    - Verify the agent discovers and uses the skill correctly
    - Refine the `description` if the skill isn't being matched properly

4. Open a pull request
    - Skills require code review like any other change
    - Include a test scenario in the PR description
    - Explain why this skill is needed and what problem it solves

## Review constraints

All skill files **must** pass code review before merging. Reviewers should
verify:

- **No secrets or credentials** — skills must never contain tokens, passwords,
  API keys, connection strings, or any other secret material. Use environment
  variables or vault references instead.
- **No production side-effects** — skills must not deploy to production, modify
  production data, or interact with production services directly.
- **Scripts reviewed** — if a skill invokes shell commands or scripts, those
  commands must be reviewed for safety (no destructive operations without
  explicit confirmation, no unchecked `rm -rf`, no force-pushes to shared
  branches).
- **Scoped permissions** — skills should request the minimum permissions
  needed. Avoid broad filesystem or network access when a narrow scope suffices.
- **Idempotent where possible** — prefer skills that can be re-run safely
  without unintended duplication or side-effects.

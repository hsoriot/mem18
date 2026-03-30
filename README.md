# Project Memory

`project-memory` is a reusable skill for Claude Code, Codex, and other CLI agents.

It provides a shared project-memory workflow built around:

- project background
- current status
- key decisions
- handoff summaries

The shared memory root is:

```text
~/.agent-memory/project-memory/
```

## Installation

```bash
npx skills add hsoriot/mem18 --skill project-memory -g
```

This installs the skill globally for all supported agents (Claude Code, Codex, GitHub Copilot, etc.).

To install for the current project only, omit `-g`:

```bash
npx skills add hsoriot/mem18 --skill project-memory
```

## Repository Layout

```
skills/project-memory/
  SKILL.md              # skill definition
  references/
    actions.md          # available actions
    schema.md           # memory file schema
    usage.md            # usage guide
```

## What The Skill Does

The daily workflow is intentionally minimal:

1. `read_project_memory`
2. `update_current_status`
3. `append_decision`
4. `generate_handoff_summary`

The default entry is:

```text
Use project-memory for project <project-name>.
```

or:

```text
Use project-memory to continue project <project-name>.
```

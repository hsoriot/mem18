# Project Memory

`project-memory` is a reusable skill for Codex, Claude Code, and other CLI agents.

It provides a shared project-memory workflow built around:

- project background
- current status
- key decisions
- handoff summaries

The shared memory root is:

```text
~/.agent-memory/project-memory/
```

## Repository Layout

- [project-memory](/Users/riot/mem18/project-memory): the real skill project
- [project-memory](/Users/riot/mem18/plugins/project-memory): Claude Code plugin wrapper
- [skills-project-memory](/Users/riot/mem18/ai_coding/skills-project-memory): development notes, requirements, and design history
- [.skills/project-memory](/Users/riot/mem18/.skills/project-memory): local skill entry for this repo

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

## Installation Paths

Two installation paths are supported:

1. Claude Code plugin installation through the local plugin wrapper in `plugins/project-memory`
2. Direct skill installation by copying `project-memory/` into an agent's skills directory

See the full install and usage guide in [README.md](/Users/riot/mem18/project-memory/README.md).

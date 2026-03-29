# Project Memory

`project-memory` is a shared working-memory skill for Codex, Claude Code, and other CLI agents.

It is designed to help an agent:

- recover project purpose quickly
- understand current progress
- preserve important decisions
- hand work to another agent without re-explaining everything

All agents share the same memory root:

```text
~/.agent-memory/project-memory/
```

## Core Model

Each project uses one directory:

```text
~/.agent-memory/project-memory/projects/<project-slug>/
```

with these files:

- `project.md`: stable project background
- `current.md`: current task, status, blockers, next step
- `decisions.md`: important decisions
- `meta.yaml`: metadata

Global discovery uses:

- `~/.agent-memory/project-memory/registry.yaml`

## Default Entry

The preferred invocation is:

```text
Use project-memory for project <project-name>.
```

or:

```text
Use project-memory to continue project <project-name>.
```

Default behavior:

1. resolve the project from `registry.yaml`
2. read `project.md`, `current.md`, and `decisions.md`
3. return `Project`, `Current`, `Decisions`, `Next`
4. continue work from that recovered context

## Daily Workflow

The skill keeps the daily path small:

1. `read_project_memory`
2. `update_current_status`
3. `append_decision`
4. `generate_handoff_summary`

Default checkpoints:

1. At task start or when context feels incomplete, read project memory.
2. After meaningful progress, scope change, blocker discovery, or task completion, update current status.
3. After an important decision, append a decision.
4. Before pausing work or switching agents, generate a handoff summary.

## Installation

Two installation styles are supported.

### 1. Claude Code Plugin

This repo includes a Claude-style local plugin wrapper:

```text
plugins/project-memory
```

with marketplace metadata at:

```text
.agents/plugins/marketplace.json
```

After `git clone`, the user should:

1. load the local marketplace in Claude Code
2. install the `project-memory` plugin
3. create the shared memory root:

```bash
mkdir -p ~/.agent-memory/project-memory/projects
```

### 2. Direct Skill Install

The skill project itself is this directory:

```text
project-memory
```

After `git clone`, the user should:

1. copy `project-memory/` into the target agent's skills directory
2. create the shared memory root:

```bash
mkdir -p ~/.agent-memory/project-memory/projects
```

## Example Triggers

```text
Use project-memory for project skills-project-memory.
Use project-memory to continue project skills-project-memory.
Use project-memory to update current status for project skills-project-memory.
Use project-memory to append a decision for project skills-project-memory.
Use project-memory to generate a handoff summary for project skills-project-memory.
```

## Repository Boundary

- `project-memory/` is the real skill project
- `plugins/project-memory/` is the Claude plugin wrapper
- `ai_coding/` is the development workspace and design history

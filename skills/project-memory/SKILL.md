---
name: project-memory
description: Maintain structured per-project working memory for Claude Code or Codex. Use when Codex needs to read project context, update the current task state, record an important decision, or produce a clean handoff summary for a new agent. Best for multi-step software projects that need stable background, current status, and decision history stored in a global shared location outside the repo.
---

# Project Memory

Use this skill to keep a project's working memory consistent across agents and sessions.

Store memory in the shared global root:

- `~/.agent-memory/project-memory/projects/<project-slug>/`
- `~/.agent-memory/project-memory/registry.yaml`

This root is intentionally agent-neutral so Codex, Claude Code, and other CLI agents can share the same memory store.

## Default Entry

If the user says either of these:

- `Use project-memory for project <project-name>.`
- `Use project-memory to continue project <project-name>.`

then treat that as the default entry point.

Default behavior:

1. resolve the project from `registry.yaml`
2. read `project.md`, `current.md`, and `decisions.md`
3. return a compact summary with `Project`, `Current`, `Decisions`, and `Next`
4. continue the task from that recovered context unless the user asks to stop after the summary

Treat the user-provided project name as the source of truth. Normalize it to a safe lowercase slug using hyphens. Reuse the same slug for every future read and update.

## Core Files

Every project memory directory contains:

- `project.md`: stable project background
- `current.md`: current task, progress, blockers, and next step
- `decisions.md`: key decisions and reversals
- `meta.yaml`: project metadata and timestamps

The global root may also contain:

- `registry.yaml`: project name to slug lookup for reliable discovery

Read the exact file structures in:

- `references/schema.md` for file schemas
- `references/actions.md` for the minimal action set and output format
- `references/usage.md` for the day-to-day calling convention

When creating new memory files, follow the schemas defined in `references/schema.md`.

## Required Workflow

### 1. Resolve Project Identity

Before any operation:

1. Ask for or locate the user-defined project name.
2. Normalize it into `project-slug`.
3. Check `registry.yaml` first when it exists.
4. Use `~/.agent-memory/project-memory/projects/<project-slug>/` as the only storage location.
5. If memory exists, reuse it. Do not create a second directory for the same project unless the user explicitly renames the project.

### 2. Choose the Action

Default to this minimal action set:

1. `read_project_memory`
2. `update_current_status`
3. `append_decision`
4. `generate_handoff_summary`

If the user request is ambiguous, infer the closest action from context and say which action you are performing.

If the user only provides the project name and asks to continue, default to `read_project_memory` followed by normal task continuation.

### 3. Read Before Writing

Before changing memory:

1. Read the existing relevant files.
2. Preserve useful context.
3. Update only the sections needed for the current action.
4. Refresh `updated_at` in `meta.yaml`.

Never overwrite `project.md`, `current.md`, or `decisions.md` blindly without first reading them.

## Action Rules

### `read_project_memory`

Read `project.md`, `current.md`, and `decisions.md`, then return a concise structured summary with:

- project background
- current task and status
- active blockers or risks
- latest important decisions
- immediate next step

Optimize this output for rapid handoff to a new agent.

### `update_current_status`

Use for frequent updates:

- what is being worked on now
- what changed recently
- current status
- blockers
- next step

This file is expected to change often and may be rewritten to reflect the latest truth.

### `append_decision`

Add a new dated entry to `decisions.md` when a meaningful project choice is made.

Include:

- decision
- reason
- rejected alternatives
- impact

### `generate_handoff_summary`

Produce a short agent-to-agent handoff using current memory. Include:

1. project purpose
2. current task
3. what is already done
4. important decisions and warnings
5. next recommended action

## Operating Rules

- Keep memory project-specific. Do not mix projects.
- Prefer concise, high-signal writing over long notes.
- Write facts and decisions, not chat transcripts.
- If information is uncertain, mark it explicitly.
- If the user gives a better project name later, rename the slug only with explicit confirmation.
- If the repo path changes, keep the same project identity unless the user says it is a different project.
- Keep the storage root vendor-neutral. Do not move it under a tool-specific directory such as `.codex`.

## Output Style

When reading or summarizing memory, use a compact structure with these headings:

1. `Project`
2. `Current`
3. `Decisions`
4. `Next`

When updating memory, state:

- which action you performed
- which project slug you used
- which files changed
- whether `registry.yaml` changed

## Minimal Example Triggers

- "Use project-memory for project skills-project-memory."
- "Use project-memory to continue project skills-project-memory."
- "Read project memory for my billing refactor project."
- "Update current status for project Alpha."
- "Record this architectural decision in project memory."
- "Generate a handoff summary from project memory."

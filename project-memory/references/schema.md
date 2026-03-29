# Project Memory Schema

Use one directory per project:

```text
~/.agent-memory/project-memory/
  registry.yaml
  projects/
    <project-slug>/
      project.md
      current.md
      decisions.md
      meta.yaml
```

## `registry.yaml`

```yaml
version: "v1"
projects:
  - project_name: "<user-defined project name>"
    project_slug: "<normalized-project-slug>"
    repo_path: "<optional current repo path>"
    git_remote: "<optional current git remote>"
    last_updated: "<ISO-8601 timestamp>"
```

Use this file as the first lookup layer when resolving a project from a user-supplied name.
Keep one entry per project slug.

## `project.md`

```md
# Project Background

## Project Name
<user-defined project name>

## Goal
<overall objective>

## Scope
<what is included>

## Constraints
<technical, product, timeline, or environment constraints>

## Non-Goals
<what this project is not trying to do>
```

Use this file for relatively stable context only.

## `current.md`

```md
# Current Status

## Current Task
<the task in progress now>

## Status
<not started | in progress | blocked | done>

## Recent Progress
<short bullet list of recent meaningful changes>

## Blockers
<known blockers, dependencies, or risks>

## Next Step
<most immediate next action>
```

Rewrite this file freely as the task changes.

## `decisions.md`

```md
# Key Decisions

## Active Decisions

### <YYYY-MM-DD> <short title>
- Decision: <what was chosen>
- Reason: <why>
- Rejected alternatives: <what was not chosen>
- Impact: <what this changes>
- Status: <active | superseded | reverted>

## Revisions

### <YYYY-MM-DD> <short title>
- Change: <what was corrected or rewritten>
- Reason: <why the history needed revision>
- Notes: <what older entries are now less relevant>
```

Use `Active Decisions` for the current truth.
Use `Revisions` when cleaning up, correcting, or replacing earlier decisions.

## `meta.yaml`

```yaml
project_name: "<user-defined project name>"
project_slug: "<normalized-project-slug>"
memory_version: "v1"
storage_root: "~/.agent-memory/project-memory"
repo_path: "<optional current repo path>"
git_remote: "<optional current git remote>"
created_at: "<ISO-8601 timestamp>"
updated_at: "<ISO-8601 timestamp>"
```

Keep fields simple and machine-readable.
Use this shared root so multiple CLI agents can read and update the same project memory.

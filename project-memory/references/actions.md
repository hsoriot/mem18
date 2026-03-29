# Minimal Actions

Use only these four day-to-day actions:

- `read_project_memory`: read all core files and summarize them
- `update_current_status`: refresh in-flight status
- `append_decision`: add a new important decision
- `generate_handoff_summary`: produce a new-agent handoff from current memory

Treat all other operations as maintenance work, not the default workflow.

## Read Sequence

When reading project memory:

1. Check `registry.yaml` if the project name or slug needs to be resolved.
2. Load `meta.yaml` to confirm project identity.
3. Read `project.md`.
4. Read `current.md`.
5. Read `decisions.md`.
6. Return a compact summary optimized for a new agent taking over.

## Write Sequence

When updating project memory:

1. Confirm the project name and slug.
2. Read `registry.yaml` when it exists and keep the project entry aligned.
3. Read the relevant existing file.
4. Preserve still-valid information.
5. Update only the target file unless metadata must change.
6. Refresh `updated_at` in `meta.yaml`.
7. Refresh the matching `registry.yaml` entry.
8. Report the action, slug, and modified files.

Use the shared root `~/.agent-memory/project-memory` unless the user explicitly overrides it with another cross-agent shared location.

## Maintenance Boundary

Avoid adding more routine actions unless repeated real usage proves they are necessary.
Do not treat project initialization, background rewrites, or decision-log rewrites as the default operating path.

## Handoff Output

Use this shape when returning a handoff summary:

```md
## Project
<goal, scope, constraints>

## Current
<task, status, recent progress, blockers>

## Decisions
<active decisions and reversals that matter now>

## Next
<the immediate next action for the next agent>
```

Keep the summary short and operational.

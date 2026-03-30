# Calling Convention

Use this minimal operating rule:

## Default Entry Prompt

The shortest expected invocation is:

1. `Use project-memory for project <project-name>.`
2. `Use project-memory to continue project <project-name>.`

When invoked this way, the skill should:

1. resolve the project in `registry.yaml`
2. read the project memory files
3. return `Project`, `Current`, `Decisions`, `Next`
4. continue work from that context

## Default Checkpoints

Apply these checkpoints by default:

1. At task start or when context is incomplete, read project memory.
2. After meaningful progress, scope change, blocker discovery, or task completion, update `current.md`.
3. After an important decision, append to `decisions.md`.
4. Before pausing work or switching agents, generate a handoff summary.

## When To Read

Read project memory at the start of a task or when context feels incomplete.

## When To Update `current.md`

Update `current.md` after meaningful progress, scope change, or task completion.

## When To Append `decisions.md`

Append a decision only when a choice changes implementation direction, constraints, or a path that should not be retried blindly.

## When To Generate Handoff

Generate a handoff summary when pausing work, switching agents, or ending a meaningful task block.

## Daily Default

For normal work, the sequence should be:

1. `read_project_memory`
2. do the task
3. `update_current_status`
4. `append_decision` only if needed
5. `generate_handoff_summary` only if handing off

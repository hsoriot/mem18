# Calling Convention

## Default Entry Prompts

The shortest expected invocations are:

1. `Use req-decompose for <requirement description>.`
2. `Help me decompose this requirement: <requirement description>.`
3. `Continue decomposing requirement for project <project-name>.`

When invoked with a new requirement, the skill should:

1. Acknowledge the initial requirement
2. Normalize the project name into a slug
3. Check `registry.yaml` for existing sessions
4. If new: create project directory and start Phase 1
5. If resuming: read `session.yaml`, show current draft status, continue from last phase

When invoked to continue, the skill should:

1. Resolve the project from `registry.yaml`
2. Read `session.yaml` and `requirement.md` (if exists)
3. Show a summary of what has been captured so far
4. Continue questioning from the current phase

## Interaction Pattern

Each round of interaction follows this pattern:

1. **Agent asks** 1-3 focused questions (propose concrete answers when possible)
2. **User answers** (may be brief or detailed)
3. **Agent summarizes** what was captured in 2-3 bullet points
4. **Agent transitions** to the next question or phase

The agent should never ask more than 3 questions at once. If a phase has many aspects to cover, spread them across multiple rounds.

## Progress Indicator

After each round, show a brief progress line:

```
[Phase 3/9: Core Features] — captured 4 features, 2 more to clarify
```

This helps the user understand where they are in the process and how much is left.

## Draft Preview

The user can ask to see the current draft at any time. When they do:

1. Generate a requirement document from all information gathered so far
2. Mark incomplete sections with `[TBD]`
3. List remaining phases and open questions
4. Ask if the user wants to continue questioning or finalize

## Finalization

When all phases are covered (or the user says "that's enough"):

1. Generate the complete `requirement.md`
2. List any remaining `[TBD]` items and open questions
3. Ask the user for final review
4. Save to the project directory
5. Update `registry.yaml` with status `complete`

## Minimal Example Triggers

- "Use req-decompose for a user authentication system."
- "Help me decompose this requirement: I want users to be able to export their data."
- "Continue decomposing requirement for project user-auth."
- "Show me the current draft for project data-export."
- "I think the requirement is complete, generate the final document."

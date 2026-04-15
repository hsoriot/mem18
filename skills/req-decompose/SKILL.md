---
name: req-decompose
description: Help users decompose vague requirements into complete, implementable requirement documents through structured iterative questioning. Use when a user has a rough idea, feature request, or project concept that needs to be clarified and formalized into an actionable specification.
---

# Requirement Decompose

Use this skill to turn a vague idea or one-sentence requirement into a complete, implementable requirement document through iterative questioning.

Store session data in the shared global root:

- `~/.agent-memory/req-decompose/projects/<project-slug>/`
- `~/.agent-memory/req-decompose/registry.yaml`

This root is intentionally agent-neutral so multiple CLI agents can share the same data.

## Default Entry

If the user says any of these:

- `Use req-decompose for <requirement description>.`
- `Help me decompose this requirement: <requirement description>.`
- `Continue decomposing requirement for project <project-name>.`

then treat that as the default entry point.

Default behavior:

1. Check if the project already has an in-progress session
2. If resuming: read existing drafts and session state, show the current draft, then continue questioning from where it left off
3. If new: acknowledge the initial requirement, then begin the structured questioning workflow

## Core Principle

**The user cannot describe requirements accurately in one shot.** The agent's job is to ask the right questions in the right order to progressively extract a complete specification. Never attempt to generate a full requirement document from the first input alone.

## Questioning Workflow

The agent works through requirement dimensions in phases. Each phase focuses on one aspect. Within each phase:

1. Ask 1-3 focused questions (never more, to avoid overwhelming the user)
2. Wait for the user's answers
3. Update the internal understanding
4. Show a brief summary of what was captured
5. Move to the next phase or dig deeper if answers reveal ambiguity

Read the detailed questioning framework in `references/workflow.md`.

## Questioning Phases

Work through these phases in order. Skip phases that are clearly not applicable. Return to earlier phases if new information invalidates previous assumptions.

### Phase 1: Goal & Background

Why does this requirement exist? What problem does it solve? What is the expected outcome?

### Phase 2: Users & Roles

Who are the target users? What are their goals? Are there different user types with different permissions or workflows?

### Phase 3: Core Features

What are the must-have capabilities? Break each feature into specific, testable behaviors.

### Phase 4: User Flows

How does the user interact with each feature? What is the step-by-step flow? What happens on edge cases or errors?

### Phase 5: Data & State

What data is involved? What is created, read, updated, or deleted? What are the relationships between data entities?

### Phase 6: Non-functional Requirements

Performance, security, accessibility, internationalization, compatibility — which of these matter and what are the specific targets?

### Phase 7: Constraints & Dependencies

Technical constraints, third-party integrations, timeline, budget, existing system limitations.

### Phase 8: Boundaries & Non-Goals

What is explicitly NOT included in this requirement? What might users assume is included but should not be?

### Phase 9: Acceptance Criteria

For each core feature, what are the specific conditions that must be met for it to be considered done?

## During the Conversation

While questioning the user:

- **Summarize frequently.** After every 2-3 rounds of Q&A, show a brief summary of the current understanding. This helps the user correct misunderstandings early.
- **Propose, don't just ask.** When possible, propose a concrete answer and ask the user to confirm or correct. This is faster than open-ended questions. For example, instead of "What should happen when the user clicks submit?", ask "When the user clicks submit, I assume we validate the form and show an error toast if validation fails — is that right?"
- **Flag assumptions.** When you make an assumption to move forward, mark it explicitly as `[Assumption]` so the user can review it later.
- **Detect completeness.** When all phases have been covered and no major open questions remain, propose generating the final document. Do not force more questions when the requirement is already clear.

## Output Actions

### `generate_draft`

At any point during or after questioning, the user can ask to see the current draft. Generate a structured requirement document from all information gathered so far, marking incomplete sections with `[TBD]`.

### `generate_final`

When the user confirms the requirement is complete, generate the final requirement document following the schema in `references/schema.md`. Save it to the project directory.

### `save_session`

Save the current session state (questions asked, answers received, current phase, draft) so it can be resumed in a future session.

### `read_requirement`

Read and display a previously saved requirement document.

## Operating Rules

- Keep questions focused and concrete. Avoid abstract or theoretical questions.
- Respect the user's domain expertise. Do not over-explain obvious concepts.
- If the user gives a short answer, accept it and move on. Do not repeatedly push for more detail on aspects the user considers unimportant.
- If the user wants to skip a phase, skip it. Note it as `[Skipped by user]` in the document.
- When the user provides information that spans multiple phases, capture it all — do not force a strict linear order.
- Prefer concise, high-signal writing in the final document. Do not pad with boilerplate.
- The final document should be implementable — a developer should be able to start coding from it without needing to ask more questions.

## File Structure

Read the exact file schemas in:

- `references/schema.md` for the requirement document template and session file format
- `references/workflow.md` for the detailed questioning framework and phase transitions
- `references/usage.md` for the calling convention and example triggers

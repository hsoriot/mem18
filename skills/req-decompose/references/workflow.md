# Questioning Workflow

This document defines how the agent guides the user through iterative requirement decomposition.

## Core Principle

**Propose, then confirm.** Instead of asking open-ended questions, propose a concrete answer based on context and ask the user to confirm, correct, or expand. This reduces the user's cognitive load and speeds up the process.

Bad: "What are the user roles in your system?"
Good: "Based on what you described, I see two user roles: admin and regular user. Admin can manage all content, regular user can only manage their own. Is that right, or are there other roles?"

## Phase Transition Rules

1. Start with Phase 1 (Goal & Background) unless the user's initial input already covers it clearly.
2. Move to the next phase when the current phase has enough information to write its section in the requirement document.
3. If the user's answer touches on a later phase, capture that information immediately but still finish the current phase first.
4. If the user explicitly asks to skip a phase, mark it as `skipped` and move on.
5. If new information from a later phase invalidates earlier assumptions, go back and update.

## Phase Details

### Phase 1: Goal & Background

**Purpose**: Understand why this requirement exists and what success looks like.

**Key questions to explore**:
- What problem is being solved?
- Who requested this? What triggered this need?
- What does the world look like after this is implemented?
- Is this a new system, a feature addition, or a modification of existing behavior?

**Move on when**: You can write a clear 2-3 sentence summary of the project goal.

### Phase 2: Users & Roles

**Purpose**: Identify who will use this and how their needs differ.

**Key questions to explore**:
- Who are the primary users?
- Are there different user types with different permissions?
- Are there admin/back-office users?
- Are there external integrations that act as "users"?

**Move on when**: You have a clear list of user roles with their primary goals.

### Phase 3: Core Features

**Purpose**: Define the must-have capabilities.

**Key questions to explore**:
- What are the main things users need to do?
- For each capability: what specifically should happen?
- What is MVP vs nice-to-have?
- Are there existing features this interacts with?

**Strategy**: List features first at a high level, then drill into each one. Use the pattern:
1. "Here are the features I've identified so far: [list]. What's missing?"
2. For each feature: "Let me clarify [feature X]. When the user does [action], I assume [behavior]. Correct?"

**Move on when**: Each feature can be described in 2-3 concrete sentences.

### Phase 4: User Flows

**Purpose**: Map the step-by-step interaction for key scenarios.

**Key questions to explore**:
- What is the happy path for each major feature?
- What happens when something goes wrong?
- Are there multi-step processes (wizards, approvals, etc.)?
- What triggers notifications or state changes?

**Strategy**: Walk through flows verbally: "So the user opens the page, sees [X], clicks [Y], then [Z] happens. Is that right?"

**Move on when**: The main flows are clear enough to draw a diagram from.

### Phase 5: Data & State

**Purpose**: Understand what information the system manages.

**Key questions to explore**:
- What data does the user create or input?
- What data is displayed or exported?
- How do different data entities relate to each other?
- What is the lifecycle of key data objects?

**Strategy**: Propose a simple data model based on the features discussed, then ask the user to validate.

**Move on when**: Core entities and their relationships are identified.

### Phase 6: Non-functional Requirements

**Purpose**: Capture quality attributes that affect architecture.

**Key questions to explore**:
- Expected scale (users, data volume, request rate)?
- Security requirements (authentication, authorization, data protection)?
- Performance targets (response time, throughput)?
- Accessibility or internationalization needs?
- Compliance requirements?

**Strategy**: Only ask about categories that are relevant to the project type. A small internal tool does not need the same questions as a public-facing SaaS.

**Move on when**: Relevant non-functional requirements are captured with specific targets, or the user confirms none are critical.

### Phase 7: Constraints & Dependencies

**Purpose**: Identify what limits the solution space.

**Key questions to explore**:
- Technology stack constraints?
- Third-party services or APIs to integrate with?
- Existing system limitations?
- Timeline or resource constraints?
- Deployment environment constraints?

**Move on when**: Known constraints are listed.

### Phase 8: Boundaries & Non-Goals

**Purpose**: Explicitly define what is NOT part of this requirement.

**Key questions to explore**:
- What might someone assume is included but should not be?
- Are there related features that are out of scope?
- What will be handled in a future phase?

**Strategy**: Propose boundaries based on the scope discussed: "Based on what we discussed, I think [X] and [Y] are out of scope for now. Agree?"

**Move on when**: Non-goals are clearly stated.

### Phase 9: Acceptance Criteria

**Purpose**: Define testable conditions for each feature.

**Key questions to explore**:
- For each feature: what specific conditions must be met?
- Are there measurable success criteria?
- What would a QA engineer test?

**Strategy**: Propose acceptance criteria for each feature and ask the user to confirm: "For [feature], I'd say it's done when: [criteria list]. Anything to add?"

**Move on when**: Each core feature has at least one testable acceptance criterion.

## Completeness Check

Before generating the final document, verify:

1. Every core feature has a description, user flow (if applicable), and acceptance criteria.
2. Assumptions are explicitly listed.
3. Open questions are captured (it is OK to have some — mark them as `[TBD]`).
4. Non-goals are stated to prevent scope creep.
5. The document is written at a level where a developer can start implementation.

If any of these are missing, ask the user if they want to address them or leave them as `[TBD]`.

## Session Persistence

After each round of Q&A:

1. Update `session.yaml` with the new information.
2. If the user asks to pause, save the session and confirm it can be resumed later.
3. When resuming, read `session.yaml` and pick up from `current_phase`.

# Requirement Decompose Schema

Use one directory per project:

```text
~/.agent-memory/req-decompose/
  registry.yaml
  projects/
    <project-slug>/
      requirement.md
      session.yaml
      meta.yaml
```

## `registry.yaml`

```yaml
version: "v1"
projects:
  - project_name: "<user-defined project name>"
    project_slug: "<normalized-project-slug>"
    status: "<drafting | complete>"
    last_updated: "<ISO-8601 timestamp>"
```

Use this file as the first lookup layer when resolving a project.
Keep one entry per project slug.

## `requirement.md`

This is the final output — a structured, implementable requirement document.

```md
# Requirement: <project name>

## 1. Overview

### 1.1 Background
<Why does this requirement exist? What problem does it solve?>

### 1.2 Goal
<What is the expected outcome? What does success look like?>

### 1.3 Target Users
<Who are the users? List user roles if applicable.>

## 2. Functional Requirements

### 2.1 <Feature Module Name>

**Description**: <what this module does>

**User Stories**:
- As a <role>, I want to <action>, so that <benefit>.

**Detailed Behavior**:
- <specific behavior 1>
- <specific behavior 2>

**Acceptance Criteria**:
- [ ] <testable condition 1>
- [ ] <testable condition 2>

### 2.2 <Feature Module Name>
<same structure as above>

## 3. User Flows

### 3.1 <Flow Name>
1. <step 1>
2. <step 2>
3. <step 3>

**Error / Edge Cases**:
- <case>: <handling>

## 4. Data Model

### 4.1 Core Entities
- **<Entity>**: <description, key fields>

### 4.2 Relationships
- <Entity A> → <Entity B>: <relationship description>

## 5. Non-functional Requirements

| Category | Requirement |
|----------|-------------|
| Performance | <specific target> |
| Security | <specific requirement> |
| Compatibility | <specific requirement> |
| Other | <specific requirement> |

## 6. Constraints

- <technical, timeline, budget, or environment constraint>

## 7. Non-Goals

- <what is explicitly excluded>

## 8. Open Questions

- [ ] <unresolved question 1>
- [ ] <unresolved question 2>

## 9. Assumptions

- [Assumption] <assumption made during decomposition>
```

Notes:
- Sections that were skipped by the user should be omitted entirely, not left empty.
- Sections that are incomplete should use `[TBD]` markers.
- The document language should match the user's language.
- Keep writing concise and implementable. A developer should be able to code from this document.

## `session.yaml`

Tracks the state of the iterative questioning process for resumption.

```yaml
project_name: "<user-defined project name>"
project_slug: "<normalized-project-slug>"
status: "<in_progress | paused | complete>"
current_phase: "<phase name, e.g. goal_background>"
initial_requirement: "<the user's original one-sentence requirement>"
phases:
  goal_background:
    status: "<not_started | in_progress | done | skipped>"
    findings: "<captured information>"
  users_roles:
    status: "<not_started | in_progress | done | skipped>"
    findings: "<captured information>"
  core_features:
    status: "<not_started | in_progress | done | skipped>"
    findings: "<captured information>"
  user_flows:
    status: "<not_started | in_progress | done | skipped>"
    findings: "<captured information>"
  data_state:
    status: "<not_started | in_progress | done | skipped>"
    findings: "<captured information>"
  non_functional:
    status: "<not_started | in_progress | done | skipped>"
    findings: "<captured information>"
  constraints_dependencies:
    status: "<not_started | in_progress | done | skipped>"
    findings: "<captured information>"
  boundaries_non_goals:
    status: "<not_started | in_progress | done | skipped>"
    findings: "<captured information>"
  acceptance_criteria:
    status: "<not_started | in_progress | done | skipped>"
    findings: "<captured information>"
assumptions:
  - "<assumption 1>"
  - "<assumption 2>"
open_questions:
  - "<question 1>"
  - "<question 2>"
created_at: "<ISO-8601 timestamp>"
updated_at: "<ISO-8601 timestamp>"
```

## `meta.yaml`

```yaml
project_name: "<user-defined project name>"
project_slug: "<normalized-project-slug>"
memory_version: "v1"
storage_root: "~/.agent-memory/req-decompose"
created_at: "<ISO-8601 timestamp>"
updated_at: "<ISO-8601 timestamp>"
```

Keep fields simple and machine-readable.

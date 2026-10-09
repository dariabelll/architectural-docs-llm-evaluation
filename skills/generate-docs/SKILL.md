---
name: generate-docs
description: Generate architectural documentation from source code. Use when the user asks to generate docs, an overview, or architecture documentation for a local project.
---

# Generate Docs

Generate architectural documentation for a local project by analyzing source code only.

## Rules

Do not use existing documentation as a source. Ignore README files, docs/, doc/, AGENTS.md, CLAUDE.md, CHANGELOG, CONTRIBUTING, architecture/design documents, and similar files during analysis.

Use source code, build and dependency files, configuration files, entry points, and directory structure as evidence.

Do not rely on external websites or prior knowledge about the project. Every factual claim must be supported by files you actually inspected.

Write the result to generated-architecture.md unless the user specifies another path.

## Size

Keep the documentation proportional to the architectural size and complexity of the project.

Small project: a short overview, roughly 1 page.

Medium project: 2–3 pages with a section for each major component.

Large project: an overview plus concise sections for the major architectural components and subsystems.

Do not produce a file-by-file description. Increase detail only when the project contains additional meaningful architectural components, interactions, or execution flows.

## Structure

```markdown
# <Project Name>

## Overview
2–4 sentences describing what the project does, its language/stack, and whether it is primarily a server, CLI, library, application, etc.

## Components
For each major architectural component:
- **Purpose** — its main responsibility.
- **Key source locations** — 2–5 relevant paths.
- **Interactions** — the important internal components it calls, imports, creates, or communicates with.

## Data / Control Flow
Describe one or more representative execution or data flows through the main components. Use a short numbered list or a Mermaid diagram when a diagram makes the relationships clearer.

## Key Decisions & Gotchas
3–7 important implementation details visible from the code that are useful for understanding the architecture, such as concurrency, configuration loading, error handling, external service boundaries, or non-obvious constraints.
```

## Analysis Steps

Map the project structure and identify likely entry points.

Identify major architectural components from the code rather than assuming that every top-level directory is a component.

Inspect the key implementation files for each component.

Trace dependencies and interactions between components.

Identify important cross-cutting concerns when they affect the architecture.

Trace representative execution or data flows.

Write the documentation only after the architecture has been investigated.

## Output Quality

Every factual claim must come from code or configuration you actually inspected.

Prefer concrete paths, functions, types, and component names over abstract descriptions.

Do not guess when evidence is insufficient.

If two components interact, explain how they interact.

Avoid unnecessary repetition and file-by-file summaries.

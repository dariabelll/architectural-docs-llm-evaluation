---
name: evaluate-docs
description: Evaluate generated architectural documentation against source code using precision and recall.
---

# Evaluate Docs

Evaluate generated architectural documentation against the actual source code of the current project.

## Rules

**Do not use existing project documentation as a source.** Ignore README files, `docs/`, `doc/`, `AGENTS.md`, `CLAUDE.md`, CHANGELOG, CONTRIBUTING, architecture/design documents, and similar files.
Use source code, build and dependency files, configuration files, entry points, directory structure, and source-code comments as evidence.
Do not use external websites or prior knowledge about the project.
Every judgment must be supported by code or configuration you actually inspected.

The candidate document and `reference-facts.md` are evaluation inputs: read them for claims and coverage, never as evidence that a claim is true. Confirm source evidence against the same repository revision used for generation. Ask for the candidate path if it is ambiguous; do not overwrite the candidate.

## Precision

Split the candidate documentation into independently verifiable factual claims.

For every claim:
- mark it as **Supported** if it is confirmed by the source code;
- otherwise mark it as **Unsupported**;
- record relevant source paths and symbols or line numbers as evidence.

Include all independently verifiable factual claims, including diagram relationships. Split compound claims rather than marking a whole paragraph correct. For Unsupported claims, state whether evidence contradicts the claim or is insufficient; both count as unsupported under this binary metric.

Precision measures how much of the generated documentation is correct:

`precision = supported claims / all claims`

## Recall

Use `reference-facts.md` as the reference set of important architectural facts.

If `reference-facts.md` does not exist, create it from the source code before evaluating the candidate documentation. Include:
- major components and their responsibilities;
- important interactions between components;
- important entry points;
- representative execution or data flows.

Keep the reference set proportional to the architectural size and complexity of the project. Do not include trivial file-level facts.

If `reference-facts.md` already exists, use it unchanged. Use one frozen reference set per project and source revision for all candidate models. Record the source commit in the reference file. When creating a new reference set, inspect the code and save the reference set before reading the candidate to avoid tailoring the denominator to its contents.

For every reference fact, determine whether it is correctly covered by the candidate documentation. Cite the candidate section or claim ID as well as source evidence. A mention of a component name alone does not establish coverage of its responsibility or interaction.

Recall measures how much of the important architecture is covered:

`recall = covered reference facts / all reference facts`

## Output

Write the result to `evaluation.md` unless a separate output path is specified. Record the candidate path and SHA-256, source commit, reference path and SHA-256, and evaluator identity if known. Do not guess the generating model from writing style. For multiple candidates, use separate output files.

Use the following report format:

```markdown
# Documentation Evaluation

## Precision

| Claim | Verdict | Evidence |
|---|---|---|
| ... | Supported / Unsupported | path/to/file |

Supported claims: <N>
Total claims: <N>

## Recall

| Reference fact | Covered | Evidence |
|---|---|---|
| ... | Yes / No | path/to/file |

Covered reference facts: <N>
Total reference facts: <N>

## Metrics

Precision: ...
Recall: ...
F1: ...
```

Use the metrics.py file bundled with this skill to calculate Precision, Recall, and F1 from the four counts. Do not calculate the final metrics yourself.
## Quality
- Keep claims independently verifiable.
- Do not guess when evidence is insufficient.
- Do not treat similar names as proof of a relationship.
- Prefer concrete paths, functions, types, and component names as evidence.

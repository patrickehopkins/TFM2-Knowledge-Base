# Agent instructions — TFM2 Knowledge Base

## Purpose and scope

Maintain a public, independently useful reference for **Teamfight Manager 2** modding. Curate findings that are reusable across mods; do not mirror whole repositories, raw probe logs, private source code, or project-specific roadmaps. This repository is documentation, not an authoritative replacement for the game's SDK or for individual mods' implementations.

Before editing, read `README.md`, `CONTRIBUTING.md`, and the relevant topic page. Check for an existing finding before adding a duplicate.

## Research and evidence requirements

- Label each conclusion **runtime verified**, **static evidence**, **hypothesis/untested**, or **rejected/unsafe**. Never promote a source-only or build-only check into a physical test pass.
- Include the specific game version, test date, source project/probe identifier, observed result, limits, and follow-up verification where relevant. Native addresses and signatures additionally require the executable fingerprint (hash, PE timestamp/image size as available). Record SDK/host ABI and mod build when relevant.
- Distinguish watched *simulation computation* from visible *replay/presentation* timing. Do not use simulation-tick observations as playback event timestamps without separate proof.
- Distinguish observation-only native hooks from deterministic gameplay-authority surfaces. Document concurrency, cross-mod detour conflicts, fail-closed signature checks, and rollback for native instrumentation.
- Preserve negative evidence and superseded claims. If a new test corrects an older finding, update its status and explain the correction; do not quietly erase its history.
- Cite original public reports, commits, or stable API documentation where possible. If a source repo is private, describe the evidence and its provenance without embedding inaccessible deep links or copying private contents.
- Prefer reproducible, concise explanations to speculative architecture prescriptions. If evidence is insufficient, record an open question rather than inventing a definitive answer.

## Cross-repository workflow

1. Document new experimental detail in the **originating mod repository** first, where full runbooks and probe traces belong.
2. Evaluate whether the result applies to other TFM2 mods. A project-specific design choice alone is not a shared finding.
3. For a reusable result, update an existing knowledge-base topic or create a focused new page. Update the source index, compatibility matrix, and README navigation *only if needed*.
4. If the update changes a previously published conclusion, explain the conflicting evidence and exact build scope.
5. If editing this knowledge base from another mod project is authorized and available, update it as part of the discovery workflow. Otherwise produce a specific proposed change/link and report that the knowledge base was **not** updated. Never claim a cross-repo write succeeded without verifying it.
6. Keep mod and knowledge-base Git histories independently useful. Do not copy a full source report merely to synchronize the repositories.

## Public-data precautions

Before publishing, inspect added files and diffs for credentials, email addresses, personal paths, account or machine identifiers, sensitive logs, third-party recordings, and proprietary game assets. Use sanitized excerpts and synthetic examples. Do not introduce private repository deep links or publish private documents wholesale. Check the public Git commit identity when relevant: privacy can be lost through commit metadata even when Markdown is clean.

## Completion checklist for agents

- Links and relative paths resolve; no duplicated or dangling navigation entries.
- Claims and status labels are consistent across changed pages.
- Versions and exact-build constraints remain visible.
- No unsupported claims of compatibility, gameplay authority, safety, or successful testing.
- Report the changed files, evidence used, and any unverified questions or blocked cross-repo updates.

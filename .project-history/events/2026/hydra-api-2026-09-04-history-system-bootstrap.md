---
id: hydra-api-2026-09-04-history-system-bootstrap
title: Bootstrap of the project-history system (reconstruction and maintenance mechanism)
kind: bootstrap
scope: [project, docs/history, .project-history, scripts/project_history.py]
paths: [docs/history/**, .project-history/**, scripts/project_history.py, tests/test_project_history.py, AGENTS.md, .github/**]
significance: medium
summary: >-
  On 2026-09-04 the complete history of this repository was reconstructed from Git, related repositories and the owner's
  dated records, and a deterministic, dependency-free maintenance tool (assess/context/validate/render/audit) with tests,
  an agent continuity contract, a PR template and a CI workflow was installed. Everything is backfilled: recorded_at is
  the reconstruction date, occurred_at values are the underlying events' dates.
occurred_at: 2026-09-04
decided_at: 2026-09-04
merged_at: null
released_at: null
recorded_at: 2026-09-04
last_verified_at: 2026-09-04
backfilled: false
anchors:
  - 0106964e92fa29d6a9cde46fa652839cb282b302
rewrite_resistant_locators:
  - ".project-history/state.yml (full_audit_anchor)"
claim_ids: [ha-c01, ha-c10, ha-c12, ha-c18]
source_ids: [src-git-hydra-api, src-leaf-brief-2026-09-04, src-worktree-2026-09-04]
related_events: [hydra-api-2026-09-02-credential-purge-untouched]
amends: []
supersedes: []
reverses: []
amendments: []
status: closed
confidence: confirmed
observed_outcome: validate, render (byte-stable), audit, assess, context and the unit tests pass on the audit date
secrets_reviewed: true
---

## Before-state and pressure

The repository had a 31-line README, no changelog, no licence, no tests and no record of why it existed or what became of
it; every account of it lived in the owner's private control-plane documents. The pressure was an explicit owner request
to reconstruct and permanently maintain the history of four project families, of which this is one of three "API projects".

## Intended beneficiaries

Future humans and coding agents working here, who need orientation, goals, principles and prior decisions before touching
the code, and a low-friction way to leave a trace afterwards.

## Goal, non-goal and definition of success

Goal: a complete, evidence-linked, unabridged history plus a living mechanism. Non-goals: changing runtime code, adding
dependencies, committing, pushing, contacting anyone, or reproducing any secret. Success: the independent verifier passes;
render is byte-stable; every cited SHA resolves; claims carry status and confidence; the agent contract and PR template carry
the three declarations.

## Principles affected

Introduces the history system's own rules (recorded in policy.yml): materiality tests, no naked skips, deferrals that expire,
backfilled records that never masquerade as contemporaneous, and no auto-authored ideological prose.

## Alternatives and rejected paths

A commit-by-commit changelog (rejected by the assignment); a shared cross-repository history (rejected — each repository
gets its own complete record, cross-citing the others by absolute path); a YAML dependency for the tool (rejected — a strict
subset parser is embedded so no dependency is added).

## Decision and rationale

Install the record in the project's native language (Python, stdlib only) with the layout fixed by the shared contract.

## Implementation and evidence

PROJECT_HISTORY.md, docs/history/*, .project-history/*, scripts/project_history.py, tests/test_project_history.py,
AGENTS.md, .github/PULL_REQUEST_TEMPLATE.md, .github/workflows/project-history.yml. Anchored to HEAD 0106964e….

## Expected versus observed outcome

Expected: all commands exit 0 and the verifier passes. Observed: recorded in the reconstruction report delivered with this
work; re-verify with `python3 scripts/project_history.py validate`.

## Tradeoffs, debt and consequences

The CI workflow can only run once the repository is pushed to GitHub with these files; until then it is documentation of an
intended mechanism. The history adds files to a public repository — they contain no secrets and no personal data beyond
the owner's already-public business identity.

## Related events

hydra-api-2026-09-02-credential-purge-untouched.

## Unresolved questions

Whether the owner will adopt the declaration discipline for a repository that has not changed since March; if not, the
gardener audit will still report drift monthly once CI is active.

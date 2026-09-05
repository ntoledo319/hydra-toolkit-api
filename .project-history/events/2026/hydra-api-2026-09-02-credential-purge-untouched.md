---
id: hydra-api-2026-09-02-credential-purge-untouched
title: September 2026 credential purge classifies the history as clean and leaves it unrewritten
kind: security
scope: [project]
paths: []
significance: medium
summary: >-
  The workspace-wide September 2026 credential purge scanned this history, matched only public-configuration pattern
  classes, confirmed no secret, and neither rewrote nor force-pushed it; origin/master still equals local master. Recorded
  as a first-class event because it fixes the reliability of every anchor cited here.
occurred_at: 2026-09-02
decided_at: 2026-09-02
merged_at: null
released_at: null
recorded_at: 2026-09-04
last_verified_at: 2026-09-04
backfilled: true
anchors:
  - 0106964e92fa29d6a9cde46fa652839cb282b302
rewrite_resistant_locators:
  - "/home/nick/Development/SECURITY_CLEANUP_REPORT.md (2026-09-02)"
  - "/home/nick/Development/.unlazy/credential-cleanup/verification/history-pattern-final-classification.json"
claim_ids: [ha-c12, ha-c10, ha-c18]
source_ids: [src-purge-2026-09, src-gh-metadata, src-worktree-2026-09-04, src-leaf-brief-2026-09-04]
related_events: [hydra-api-2026-08-06-audits-park-fix, hydra-api-2026-09-04-history-system-bootstrap]
amends: []
supersedes: []
reverses: []
amendments: []
status: closed
confidence: confirmed
observed_outcome: history unchanged; anchors remain valid; sibling NoHustle received a fast-forward security commit instead
secrets_reviewed: true
---

## Before-state and pressure

A workspace-wide credential exposure review in early September 2026 rewrote eighteen owned remotes and pushed dedicated
security commits to twenty-two others. Any history that was rewritten loses its commit anchors; a history that was not
keeps them. This repository had to be checked either way.

## Intended beneficiaries

Future readers of this history, whose citations depend on the anchors; and the owner, whose exposure the purge reduced.

## Goal, non-goal and definition of success

Goal: know whether the reachable graph is the original one. Success: the classification records and the remote ref agree
that nothing changed.

## Principles affected

None of the project's own principles. The history system's rule — cite full SHAs while reachable and record rewrites as
events rather than silently rebinding — is exercised here for the first time.

## Alternatives and rejected paths

Not applicable; the purge's routing decisions were made outside this project.

## Decision and rationale

The purge classified every pattern match in this history as RETAINED_PUBLIC_CLASS ("public configuration, identifier,
endpoint, environment reference, or placeholder with no embedded credential"), so no rewrite was warranted (ha-c12).

## Implementation and evidence

No commit here. Evidence is external: the classification JSON (values omitted), the cleanup report's rewritten-repository
table (this repository absent), and `git ls-remote` on 2026-09-04 showing origin/master at 0106964e…. The working tree's
three pre-existing changes (modified bytecode, untracked agent settings, untracked manifest) predate the purge and were
preserved.

## Expected versus observed outcome

Expected: no change. Observed: no change. The NoHustle sibling, by contrast, received a fast-forward security commit on its
remote that its local clone had not fetched when this audit began (the reconstruction fetched it read-only on 2026-09-04,
leaving local main one commit behind); that is recorded in NoHustle's history.

## Tradeoffs, debt and consequences

None for the code. For the reconstruction: the lead's dispatch brief mis-assigned dirty baselines between the two HYDRA
repositories (ha-c18); this event records the measured truth so the discrepancy is attributable.

## Related events

hydra-api-2026-09-04-history-system-bootstrap.

## Unresolved questions

None.

---
id: <repo-slug>-<YYYY-MM-DD>-<slug>            # must equal the file name (without .md)
title: <one line>
kind: decision                                  # origin|decision|release|deployment|migration|reversal|abandonment|consolidation|governance|incident|security|licence|experiment|bootstrap
scope: [project]                                # components / path globs this event constrains
paths: []                                       # optional path globs used by `context`
significance: medium                            # high|medium|low
summary: <two sentences an agent can act on>
occurred_at: <YYYY-MM-DD or null>               # when the underlying project event happened
decided_at: null
merged_at: null
released_at: null
recorded_at: <YYYY-MM-DD>                       # when this capsule was written; later than occurred_at when backfilled
last_verified_at: null
backfilled: false
anchors: []                                     # 40-hex commit shas (reachable here or in a related repo listed in sources.yml)
rewrite_resistant_locators: []                  # tags, release ids, archived URLs, checksums
claim_ids: []                                   # from .project-history/claims.yml
source_ids: []                                  # from .project-history/sources.yml
related_events: []
amends: []
supersedes: []
reverses: []
amendments: []                                  # - {date, reason, evidence, confidence_moved}
status: closed                                  # open|closed|amended|superseded
confidence: plausible                           # confirmed|strongly_supported|plausible|speculative|unknown
observed_outcome: <short phrase or "unknown">
secrets_reviewed: true
---

## Before-state and pressure

What was true before, and what need, failure, opportunity or pressure opened this arc.

## Intended beneficiaries

Who this was for.

## Goal, non-goal and definition of success

What was sought, what was explicitly out of scope, and how success was defined at the time.

## Principles affected

Principles affirmed, introduced, weakened or challenged (cite doctrine ids and versions).

## Alternatives and rejected paths

What else was available, attempted, postponed or explicitly rejected — with evidence, or marked as inferred.

## Decision and rationale

What was decided and why. Mark uncertainty exactly where it occurs.

## Implementation and evidence

How it landed in code, config, defaults, docs, process — with anchors and claim ids.

## Expected versus observed outcome

What was expected; what actually happened (or "unknown — no evidence found").

## Tradeoffs, debt and consequences

What it cost, what it constrained, what follow-ups it created.

## Related events

Links to related, amended, reversed or superseding capsules.

## Unresolved questions

What remains unknown and what evidence would settle it.

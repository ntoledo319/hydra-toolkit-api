---
id: hydra-api-2026-05-05-backburner-and-revenue-label
title: Workspace migration files the repository under backburner/ and labels it a revenue asset
kind: governance
scope: [project, .toledo.yaml]
paths: [.toledo.yaml]
significance: medium
summary: >-
  On 2026-05-05 the owner's workspace migration moved the checkout out of the macOS CascadeProjects folder into backburner/
  and generated an untracked .toledo.yaml (status backburner, type revenue, platform render, url null); portfolio documents
  in June then framed it as "a parallel Python/FastAPI variant for a possible RapidAPI listing".
occurred_at: 2026-05-05
decided_at: 2026-05-05
merged_at: null
released_at: null
recorded_at: 2026-09-04
last_verified_at: 2026-09-04
backfilled: true
anchors:
  - 73e342abef33abc9161838c868d5f3939d92e721
rewrite_resistant_locators:
  - "toledo-command/archive/_meta-inventory-2026-05/migration-log.txt lines 162-164, 229"
claim_ids: [ha-c07, ha-c08, ha-c13, ha-c22]
source_ids: [src-tc-meta-inventory-2026-05, src-tc-master-portfolio, src-worktree-2026-09-04, src-marketing-arm, src-business-ops]
related_events: [hydra-api-2026-03-26-render-blueprint-and-worker-port, hydra-api-2026-08-06-audits-park-fix]
amends: []
supersedes: []
reverses: []
amendments: []
status: closed
confidence: confirmed
observed_outcome: label recorded; no code, listing or price followed
secrets_reviewed: true
---

## Before-state and pressure

Between 2026-03-26 and 2026-05-05 nothing happened in this repository. The pressure came from outside it: the owner
consolidated dozens of scattered checkouts into one `Development/` layout with lifecycle folders, and every project received
a generated manifest. This one landed in `backburner/` with `type: revenue` (ha-c07), the same classification given to its
Worker sibling.

## Intended beneficiaries

The owner and the agents that operate the portfolio: the manifest exists so tooling can answer "what is this, is it live,
does it make money" without opening the code.

## Goal, non-goal and definition of success

Goal g-revenue-classification (introduced here): be a revenue asset. Goal g-rapidapi-listing gained its clearest statement
in the June portfolio: "intended top-of-funnel dev surface + a freemium RapidAPI candidate" (ha-c08). Success was never
defined in measurable terms; the marketing-machine documents later supplied one — a decided price — and failed the product
on it ("no price set").

## Principles affected

p-keyless-free v1 moved to *challenged*: the label asserts revenue while the code gives everything away. No principle was
rewritten; the tension was simply recorded on both sides.

## Alternatives and rejected paths

The marketing documents name the alternatives explicitly for "hydra" (meaning the Worker): set a freemium tier, or
designate HYDRA a backlink/lead asset for another product. Neither was chosen. This Python repository is not named in those
documents at all (ha-c22); its fate was decided by omission.

## Decision and rationale

A classification, not a decision: the migration tooling wrote the manifest from a plan the owner approved. The "revenue"
type most plausibly encodes the marketplace ambition; the "backburner" status records the truth that no one was working on it.

## Implementation and evidence

Untracked .toledo.yaml in the working tree (present tense); migration-log.txt entries; MASTER-PORTFOLIO.md section HYDRA in
toledo-command commit 73e342ab…; business-ops asset-sale kit (2026-06-05) valuing HYDRA as a template or RapidAPI freemium
with "no canonical price".

## Expected versus observed outcome

Expected by the label: eventual revenue. Observed: none; every subsequent auditor calls the label aspirational
(contradiction hydra-api-x3).

## Tradeoffs, debt and consequences

The manifest also captured the original macOS path under the owner's home directory. Because the file is untracked here it
never reached GitHub; in the Worker sibling the equivalent file *was* committed on 2026-09-01. That asymmetry is noted in the
Worker's history.

## Related events

hydra-api-2026-03-26-render-blueprint-and-worker-port; hydra-api-2026-08-06-audits-park-fix.

## Unresolved questions

Did the owner ever intend this Python copy, rather than the Worker, to be the RapidAPI artifact? The June portfolio implies
so ("for a possible RapidAPI listing"); no later document repeats it.

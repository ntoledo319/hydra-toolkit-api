---
id: hydra-api-2026-03-26-render-blueprint-and-worker-port
title: Render blueprint added, then overtaken by the Cloudflare Worker port 17 minutes later
kind: abandonment
scope: [project, render.yaml, deployment]
paths: [render.yaml, .gitignore]
significance: high
summary: >-
  A free-plan Render blueprint with auto-deploy was committed at 02:11 EDT; at 02:28 the same code was reborn as a Hono
  Worker in a new repository, which became the deployed HYDRA. This service was never observed running anywhere.
occurred_at: 2026-03-26
decided_at: 2026-03-26
merged_at: 2026-03-26
released_at: null
recorded_at: 2026-09-04
last_verified_at: 2026-09-04
backfilled: true
anchors:
  - 0106964e92fa29d6a9cde46fa652839cb282b302
  - 2a804e67b5eb84bb52ddd4950fa41b0aa533959b
rewrite_resistant_locators:
  - "GitHub repository ntoledo319/hydra-worker created 2026-03-26T06:28:30Z"
  - "https://hydra-worker.toledonick98.workers.dev (live surface; HTTP 200 on 2026-09-04)"
claim_ids: [ha-c03, ha-c04, ha-c05, ha-c17, ha-c20]
source_ids: [src-git-hydra-api, src-git-hydra-worker, src-gh-metadata, src-live-probe, src-tc-root-reports-2026-07]
related_events: [hydra-api-2026-03-26-fastapi-toolkit-v1, hydra-api-2026-08-06-audits-park-fix]
amends: []
supersedes: []
reverses: []
amendments: []
status: closed
confidence: strongly_supported
observed_outcome: no Render service ever observed; the Worker became the live HYDRA within eight days
secrets_reviewed: true
---

## Before-state and pressure

Fifty-eight minutes after the root commit the code was complete and unhosted. The blueprint (free plan, Oregon, uvicorn on
$PORT, PYTHON_VERSION 3.11.0, autoDeploy true) is the conventional next step for this author — NoHustle had used the same
file seven months earlier — and the .gitignore added in the same commit ignores `__pycache__/` a minute after the bytecode
had already been tracked (ha-c03).

## Intended beneficiaries

The same public developers; and, if the marketing framing is taken at face value, RapidAPI browsers who would find a free
Python-hosted API (ha-c08).

## Goal, non-goal and definition of success

Goal g-render-free-deploy: a live onrender.com URL. It was abandoned by outcome rather than by decision: on 2026-07-20 the
owner's ship queue still listed "hydra-api (Render) — Render → Blueprint → connect — 20m" as undone work, and probes in
August and September found no service (ha-c05).

## Principles affected

Introduced and immediately superseded: p-render-first-hosting v1. The edge-first principle that replaced it is recorded in
the hydra-worker doctrine, not here, because the decision was enacted by creating a different repository.

## Alternatives and rejected paths

The alternative actually taken: rewrite the same 24 routes on Hono for Cloudflare Workers (ha-c04). What Render offered
that the edge did not — generated Swagger/ReDoc pages — was lost in the port and back-filled eight days later with a
hand-written openapi.json and an HTML playground (ha-c17). What the edge offered — no cold starts, "~50ms worldwide", "$0
on Workers free tier (100K req/day)" per the Worker README — is the only stated rationale, and it is marketing copy, not a
decision record. Keeping both alive as "parallel variants" was the framing chosen afterwards (contradiction hydra-api-x1).

## Decision and rationale

Recorded nowhere. The sequence of commits is the decision: blueprint at 06:11Z, push at 06:11Z, Worker repository created
at 06:28Z with an already-working port. The Worker's `/` banner still points its `docs` at this repository, which is the
one contemporaneous acknowledgement of the parentage.

## Implementation and evidence

render.yaml and .gitignore (commit 0106964e…); the Worker's root commit 2a804e67… in the related repository; Worker README
of 2026-04-03 with the live URL (commit 465f2847… there).

## Expected versus observed outcome

Expected (blueprint): a running Render service. Observed: none, ever (strongly supported; the Render dashboard was not
consulted). The Worker answered HTTP 200 in 0.13 s on 2026-09-04 (ha-c20).

## Tradeoffs, debt and consequences

The repository was left in a permanently "ready to deploy" posture — autoDeploy true on a public repo — that every later
auditor flagged as a dormant but live-looking configuration. The consequence for the family: two public repositories
describe the same product, with counts and links that drifted (hydra-api-x4).

## Related events

hydra-api-2026-03-26-fastapi-toolkit-v1; hydra-api-2026-08-06-audits-park-fix; in hydra-worker:
hydra-worker-2026-03-26-worker-port-and-first-deploy.

## Unresolved questions

Was the blueprint ever connected to a Render service that was later deleted? Was Render rejected for cost, cold starts, the
Python-version friction NoHustle had suffered, or simply because the Worker port worked first? Only the Render account and
the session logs can say.

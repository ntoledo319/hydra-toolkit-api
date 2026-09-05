# AGENTS.md — HYDRA Developer Toolkit API (`backburner/hydra-api`)

This repository is the Python/FastAPI sibling of the deployed HYDRA Worker (`/home/nick/Development/active/hydra-worker`). It has not changed since 2026-03-26 and is not deployed anywhere. Do not change runtime behaviour, add dependencies, commit, push or deploy unless the task explicitly authorises it.

## Project-history continuity contract

At task start, read `docs/history/ORIENTATION.md`, the relevant current goals and principles (`.project-history/doctrine/goals.yml`, `.project-history/doctrine/principles.yml`), and the history surfaced for the paths or component you will touch:

```
python3 scripts/project_history.py context [paths...]
```

At task completion, run the history-impact assessment and declare **exactly one** of:

- `history:recorded <event-id>` — you added or amended an event capsule under `.project-history/events/YYYY/`, updated affected goal/principle lifecycle records, patched the relevant curated chapter(s) in `docs/history/`, ran `python3 scripts/project_history.py render`, and `python3 scripts/project_history.py validate` passes.
- `history:none — <specific reason>` — the work is immaterial (typos, formatting, generated refreshes, lockfile churn, fixups, mechanical renames, behaviour-preserving refactors, tests that only confirm existing behaviour). Say why; a bare `history:none` is not accepted.
- `history:defer — <tracking item, owner, deadline>` — emergency rollback, incident containment or a security hotfix may defer the prose, but the deferral must be attributable and must expire: add it to `deferrals:` in `.project-history/policy.yml` with an `id`, `owner`, `deadline` (YYYY-MM-DD) and `tracking` reference. `validate` fails on expired open deferrals.

Materiality (see `.project-history/policy.yml`): record an event when purpose, audience, value, principle, success metric, goal or non-goal changed; when a durable API, data-model, architecture, security, privacy, reliability, governance or deployment choice constrains future work; on a meaningful release, migration, deprecation, incident, rollback or reversal; when an experiment or discovery changed what the project believes; when a feature or removal changed the user promise or identity. Do not create history noise for anything else.

Rules: closed events are append-mostly — correct them with an `amendments:` entry (date, reason, evidence, confidence_moved), never by silent rewrite; backfilled capsules carry `recorded_at` later than `occurred_at`; cite full 40-hex commit SHAs while they are reachable plus a rewrite-resistant locator where one exists; never reproduce secrets, tokens, env values or personal data in any history artifact (validate secret-scans them); automation may index and assemble curated prose but must never author or wholesale rewrite ideological or causal narrative.

Commands: `assess`, `context`, `validate`, `render`, `audit --full`, `audit --since <anchor>` in `scripts/project_history.py`; tests in `tests/test_project_history.py` (`python3 -B -m unittest -q tests/test_project_history.py`).

## Repository facts agents keep getting wrong

- The live HYDRA is the Worker, not this service; `hydra-toolkit-api.onrender.com` has never been observed serving.
- The code has 24 utility routes plus `/` and `/health`. "20+", "22" and the live banner's "20" are all approximations; do not propagate them.
- `.toledo.yaml`, `.claude/settings.local.json` and the modified tracked bytecode are present-tense working-tree state, not history. Leave them alone.

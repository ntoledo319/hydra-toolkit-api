# Orientation — HYDRA Developer Toolkit API (`backburner/hydra-api`)

_Present-tense briefing as of the audit date 2026-09-04. Everything here is what is true **now**; the history that produced it lives in the chapters that follow. Read this file first; then read `NARRATIVE.md`._

## What this repository is

A single 437-line FastAPI module (`main.py`) exposing 24 stateless developer-utility routes plus `/` and `/health`: text analysis, hashing, Base64, UUIDs, JSON validate/diff, regex testing, password scoring, URL/e-mail/JWT parsing, colour conversion, Markdown-to-HTML, time helpers and fake-data generation. No authentication, no storage, no outbound calls, wildcard CORS, three pinned dependencies (`fastapi`, `uvicorn`, `pydantic`). It is the Python **sibling** of the Cloudflare Worker at `active/hydra-worker`, which is the deployed and canonical HYDRA.

## What is true today (verified 2026-09-04)

- **Not deployed.** `render.yaml` describes a free Render service with `autoDeploy: true`, but `https://hydra-toolkit-api.onrender.com/health` answers `404` with `x-render-routing: no-server` (claim `ha-c05`). No dated record after the blueprint shows a service ever ran.
- **Frozen since 2026-03-26.** Three commits, all inside one night; `origin/master` equals local `master` at `0106964e92fa29d6a9cde46fa652839cb282b302`; GitHub shows no push since `2026-03-26T06:11:05Z` (`ha-c10`).
- **Public and unlicensed.** The GitHub repository `ntoledo319/hydra-toolkit-api` is public with no licence file; the Worker sibling chose MIT. GitHub secret scanning and push protection are enabled on it.
- **Still cited as documentation by the live product.** The Worker's `/` banner links its `docs` field to this repository (`ha-c04`). A caller following the live API's own metadata lands here.
- **Labelled `revenue`, earns nothing.** The untracked `.toledo.yaml` says `status: backburner`, `type: revenue`, `url: null`; the code has no key, metering or billing (`ha-c07`, contradiction `hydra-api-x3`).
- **Working tree (present tense, not history):** `M __pycache__/main.cpython-312.pyc`, `?? .claude/settings.local.json`, `?? .toledo.yaml`. These predate the history work and are preserved untouched.

## Who should care, and what for

- **A reader of the Worker's code** who prefers Python or wants the generated Swagger (`/docs`) and ReDoc (`/redoc`) pages this implementation gets for free (`ha-c17`).
- **Anyone deciding this repository's fate.** Three August-2026 reviews reached three verdicts — PARK/FIX, KILL-by-rule, "superseded/shelved" — and none has been acted on (`ha-c09`, contradiction `hydra-api-x6`).
- **Agents touching HYDRA at all.** Endpoint counts (20, "20+", 22, 24) disagree across the family (`ha-c16`, `hydra-api-x4`); do not propagate any of them without checking `main.py`.

## How to read the history

- `NARRATIVE.md` — prehistory, the eras and the causal story; the lineage NoHustle → this repository → the Worker is argued there with evidence, not assumed.
- `IDEOLOGY.md` — the worldview the code reveals, its non-goals and the tensions that were never resolved.
- `GOALS.md` — every goal, when it was proposed, and what became of it.
- `DECISION_MAP.md` — decision genealogies plus the generated index of events, principles and goals.
- `TIMELINE.md` — deterministic, evidence-linked index.
- `OPEN_QUESTIONS.md` — gaps, contradictions and low-confidence claims, ranked.

**Evidence conventions.** Every material statement cites a claim id (`ha-cNN`) from `.project-history/claims.yml`; each claim carries an evidence type (`direct`, `contemporaneous`, `retrospective`, `behavioral`, `inferred`), a status and a confidence. Four things are kept apart throughout: what participants said, what the system did, what outcome followed, and what the historian infers. Where the record says "inferred" or "plausible", treat it as an argument, not a fact. Git authorship is not intellectual authorship: several dated records here were written by AI agents on the owner's behalf and are labelled as such.

## Maintaining this history

Commands (run from the repository root; all exit 0 when healthy):

```
python3 scripts/project_history.py context [paths...]   # smallest relevant history for an area
python3 scripts/project_history.py assess [range]       # advisory materiality check on new work
python3 scripts/project_history.py validate             # schemas, ids, dates, anchors, secrets, render drift
python3 scripts/project_history.py render               # rebuild TIMELINE, DECISION_MAP index, PROJECT_HISTORY.md
python3 scripts/project_history.py audit --full         # compare git evidence with recorded history
python3 scripts/project_history.py audit --since HEAD~1 # incremental audit
python3 -B -m unittest -q tests/test_project_history.py # the tool's tests
```

At task end every agent declares exactly one of `history:recorded <event-id>`, `history:none — <specific reason>` or `history:defer — <tracking item, owner, deadline>` (see `AGENTS.md` and `.github/PULL_REQUEST_TEMPLATE.md`). Material changes get an event capsule under `.project-history/events/`; noise does not.

**CI status.** `.github/workflows/project-history.yml` runs validate, render-drift, tests, an incremental audit, a secret scan and the declaration check on pull requests, and a monthly "history gardener" audit. The repository has never had GitHub Actions and the workflow file exists only in this uncommitted working tree: **it activates only once these files are committed and pushed to GitHub.** Nothing here claims it is running today.

## Related repositories (absolute paths; cited SHAs resolve against them)

- `/home/nick/Development/active/hydra-worker` — the canonical, deployed HYDRA (Cloudflare Worker). Its own history lives there.
- `/home/nick/Development/archive/NoHustle API` — the August-2025 paid utility API; thematic predecessor, no shared code.
- `/home/nick/Development/archive/duplicates/hydra-site` — retired static mirror of the Worker's landing page.
- `/home/nick/Development/experiments/thing` — the NoHustle growth kit of August 2025.

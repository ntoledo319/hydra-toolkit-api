# HYDRA Developer Toolkit API (hydra-api) — Project History

_Canonical, unabridged reading path. Assembled deterministically by `scripts/project_history` `render` from the curated chapters in `docs/history/` and the evidence ledgers in `.project-history/`. Edit the chapters, not this file._

## Contents

- [ORIENTATION.md](#chapter-orientationmd)
- [NARRATIVE.md](#chapter-narrativemd)
- [IDEOLOGY.md](#chapter-ideologymd)
- [GOALS.md](#chapter-goalsmd)
- [DECISION_MAP.md](#chapter-decision_mapmd)
- [TIMELINE.md](#chapter-timelinemd)
- [OPEN_QUESTIONS.md](#chapter-open_questionsmd)
- [Appendix A — Claims ledger](#appendix-a-claims-ledger)
- [Appendix B — Contradiction register](#appendix-b-contradiction-register)
- [Appendix C — Source inventory](#appendix-c-source-inventory)
- [Appendix D — Coverage and reproducibility](#appendix-d-coverage-and-reproducibility)

## Chapter: ORIENTATION.md

## Orientation — HYDRA Developer Toolkit API (`backburner/hydra-api`)

_Present-tense briefing as of the audit date 2026-09-04. Everything here is what is true **now**; the history that produced it lives in the chapters that follow. Read this file first; then read `NARRATIVE.md`._

### What this repository is

A single 437-line FastAPI module (`main.py`) exposing 24 stateless developer-utility routes plus `/` and `/health`: text analysis, hashing, Base64, UUIDs, JSON validate/diff, regex testing, password scoring, URL/e-mail/JWT parsing, colour conversion, Markdown-to-HTML, time helpers and fake-data generation. No authentication, no storage, no outbound calls, wildcard CORS, three pinned dependencies (`fastapi`, `uvicorn`, `pydantic`). It is the Python **sibling** of the Cloudflare Worker at `active/hydra-worker`, which is the deployed and canonical HYDRA.

### What is true today (verified 2026-09-04)

- **Not deployed.** `render.yaml` describes a free Render service with `autoDeploy: true`, but `https://hydra-toolkit-api.onrender.com/health` answers `404` with `x-render-routing: no-server` (claim `ha-c05`). No dated record after the blueprint shows a service ever ran.
- **Frozen since 2026-03-26.** Three commits, all inside one night; `origin/master` equals local `master` at `0106964e92fa29d6a9cde46fa652839cb282b302`; GitHub shows no push since `2026-03-26T06:11:05Z` (`ha-c10`).
- **Public and unlicensed.** The GitHub repository `ntoledo319/hydra-toolkit-api` is public with no licence file; the Worker sibling chose MIT. GitHub secret scanning and push protection are enabled on it.
- **Still cited as documentation by the live product.** The Worker's `/` banner links its `docs` field to this repository (`ha-c04`). A caller following the live API's own metadata lands here.
- **Labelled `revenue`, earns nothing.** The untracked `.toledo.yaml` says `status: backburner`, `type: revenue`, `url: null`; the code has no key, metering or billing (`ha-c07`, contradiction `hydra-api-x3`).
- **Working tree (present tense, not history):** `M __pycache__/main.cpython-312.pyc`, `?? .claude/settings.local.json`, `?? .toledo.yaml`. These predate the history work and are preserved untouched.

### Who should care, and what for

- **A reader of the Worker's code** who prefers Python or wants the generated Swagger (`/docs`) and ReDoc (`/redoc`) pages this implementation gets for free (`ha-c17`).
- **Anyone deciding this repository's fate.** Three August-2026 reviews reached three verdicts — PARK/FIX, KILL-by-rule, "superseded/shelved" — and none has been acted on (`ha-c09`, contradiction `hydra-api-x6`).
- **Agents touching HYDRA at all.** Endpoint counts (20, "20+", 22, 24) disagree across the family (`ha-c16`, `hydra-api-x4`); do not propagate any of them without checking `main.py`.

### How to read the history

- `NARRATIVE.md` — prehistory, the eras and the causal story; the lineage NoHustle → this repository → the Worker is argued there with evidence, not assumed.
- `IDEOLOGY.md` — the worldview the code reveals, its non-goals and the tensions that were never resolved.
- `GOALS.md` — every goal, when it was proposed, and what became of it.
- `DECISION_MAP.md` — decision genealogies plus the generated index of events, principles and goals.
- `TIMELINE.md` — deterministic, evidence-linked index.
- `OPEN_QUESTIONS.md` — gaps, contradictions and low-confidence claims, ranked.

**Evidence conventions.** Every material statement cites a claim id (`ha-cNN`) from `.project-history/claims.yml`; each claim carries an evidence type (`direct`, `contemporaneous`, `retrospective`, `behavioral`, `inferred`), a status and a confidence. Four things are kept apart throughout: what participants said, what the system did, what outcome followed, and what the historian infers. Where the record says "inferred" or "plausible", treat it as an argument, not a fact. Git authorship is not intellectual authorship: several dated records here were written by AI agents on the owner's behalf and are labelled as such.

### Maintaining this history

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

### Related repositories (absolute paths; cited SHAs resolve against them)

- `/home/nick/Development/active/hydra-worker` — the canonical, deployed HYDRA (Cloudflare Worker). Its own history lives there.
- `/home/nick/Development/archive/NoHustle API` — the August-2025 paid utility API; thematic predecessor, no shared code.
- `/home/nick/Development/archive/duplicates/hydra-site` — retired static mirror of the Worker's landing page.
- `/home/nick/Development/experiments/thing` — the NoHustle growth kit of August 2025.

## Chapter: NARRATIVE.md

## Narrative — how a one-night Python draft became the shadow of a live product

_Curated era-and-causal synthesis. Claim ids (`ha-cNN`) point into `.project-history/claims.yml`; event ids point into `.project-history/events/`. Statements marked **inferred** are the historian's reading, not the record's._

### How to read this

This repository has three commits, all made inside seventy-five minutes of one night in March 2026. A commit-by-commit account would be four sentences long and would explain nothing. The history worth having is the history of a **choice that was never written down**: the same developer-utility toolkit was implemented twice, in two languages, in one sitting — and the second implementation went live while this one stayed a blueprint. Everything after that night is other people (mostly the owner's AI agents, in dated records) reinterpreting a repository that never changed. The eras below are defined by those reinterpretations, because they are the only events there were.

### Prehistory — the marketplace-utility thesis before HYDRA (2025-08 to 2026-03)

The idea this repository executes — small, useful developer endpoints bundled behind one HTTP surface and discovered through an API marketplace — has a documented ancestor in the same portfolio. **NoHustle API** (`ntoledo319/NoHustle-API`, 2025-08-18 to 2025-08-21) was a Flask "Utility Pack" of seven heavy file-processing endpoints (background removal, smart crop, PDF tables, Excel→CSV, URL→Markdown, e-mail verification, text dedupe), sold behind an API key, metered into SQLite, licensed under the Business Source License 1.1, deployed to Render and prepared for a RapidAPI listing with a four-tier price sheet. Its four days of commits are a fight with Render's Python version, a 1.5 GB ML dependency and RapidAPI's health checker; a separate "growth kit" repository then published dev.to posts, Hugging Face demos, a Postman collection and a GitHub Action around it (2025-08-22 to 2025-08-29). After that, silence. Its history is reconstructed in full in `/home/nick/Development/archive/NoHustle API`.

What matters for this repository is what the record does **not** contain. A mechanical comparison on 2026-09-04 found no shared route beyond `/` and `/health`, no shared distinctive literal, an identifier overlap of 0.28, and no textual reference in either direction; no portfolio document names NoHustle and HYDRA in the same breath (`ha-c14`, confirmed). As late as 2026-01-17 the owner's own codebase audit still rated NoHustle "Production-Ready", proposed folding it into a shared backend and priced it at "$5–50/mo per user" (`ha-c23`). Nine weeks later a utility API was started again from a blank file, in FastAPI, with no key, no storage, no ML and no price. The inversion is exact and systematic — heavy dependencies → three pins and the standard library; SQLite analytics → statelessness; keys and paid tiers → keyless and free; BSL → (in the Worker) MIT; Render → the edge (`ha-c15`). Whether this was a *lesson learned* from NoHustle or simply the shape of an easier product is the central inference of this history and is marked **plausible**, not confirmed: no source states the intent, and the authoring session that would have is inaccessible.

The idea's birth is therefore earlier than the first commit and unrecorded. The original checkout lived in a macOS `CascadeProjects` directory (`ha-c07`), which suggests an AI-assisted editor session; the commit messages ("HYDRA Developer Toolkit API v1.0 - 20+ utility endpoints") read like a product name that already existed. Nothing in the owner's synced documents from before March 2026 mentions HYDRA.

### Era 1 — The one-night build (2026-03-26, 01:13–02:28 EDT)

**Situation.** Spring 2026 in this portfolio was a triage toward things that could be live at zero cost (the July ship queue and June asset kit make that explicit in retrospect). A utility API that needs no models, no disk and no keys is the cheapest possible "live" product. That framing is **inferred**; the only contemporaneous witnesses are the code and four timestamps.

**What it believed the problem was.** Developers reach for the same small helpers over and over — hash this, slugify that, decode this JWT, give me five UUIDs — and each is a search, a library install or a throwaway script. One HTTP surface with typed inputs and generated documentation answers all of them. The README's own words: "A comprehensive developer utility API with 20+ endpoints for text analysis, hashing, encoding, data generation, and more."

**Whom it was for.** Any developer, anonymously: wildcard CORS, no key, no sign-up (`ha-c06`). Secondarily the owner's studio — the file is signed "Built by Toledo Technologies LLC" — as a demonstrable, cheap, public artifact.

**Goals, non-goals, success.** Goal `g-ship-toolkit-v1`: a working "20+ endpoint" toolkit in one sitting with self-generated docs. Success evidently meant "it runs and the docs page lists everything": the only fix in the repository's life — a tuple-unpacking bug in `json/validate` — landed eighty-nine seconds after the root commit, together with the CPython bytecode cache (`ha-c02`), proving the code was exercised locally. Non-goals, revealed by absence rather than statement: authentication, metering, rate limiting, persistence, tests. None was stubbed or mentioned.

**Principles introduced** (all visible in the first commit, none revised since): one file, stateless, pure handlers (`p-one-file-stateless`); keyless and free (`p-keyless-free`); three dependencies and the standard library (`p-minimal-deps`, `ha-c21`); the API documents itself through typed models and FastAPI's Swagger/ReDoc (`p-self-documenting`, `ha-c17`).

**The second act.** Fifty-eight minutes after the root commit a Render blueprint was added — free plan, Oregon, `uvicorn` on `$PORT`, `PYTHON_VERSION 3.11.0`, `autoDeploy: true` — together with a `.gitignore` that ignores the bytecode already tracked (`ha-c03`, event `hydra-api-2026-03-26-render-blueprint-and-worker-port`). Render is the author's habitual first host; NoHustle used the same file seven months earlier. The blueprint was pushed at 06:11Z. At 06:28Z a new GitHub repository, `hydra-worker`, was created with an already-working Hono port of this file for Cloudflare Workers: all 26 routes match, identifier overlap 0.82, the same stop-word list, the same fake-company names, the same password heuristics — and the Worker's `/` banner points its `docs` field at *this* repository (`ha-c04`, confirmed).

**Alternatives and the decision nobody recorded.** Two implementations of one product in one night is the event of this history, and there is no sentence anywhere explaining it. The candidates, weighed only by later evidence: Python was the comfortable draft language and the Worker was always the target (consistent with the Worker's `docs` link back here); Render was tried and rejected for cold starts or cost (the Worker README's "~50ms worldwide", "$0 on Workers free tier (100K req/day)" is marketing copy, not a decision record); the Python-version friction NoHustle had suffered on Render was fresh (**inferred**, plausible); or the port simply worked first. What the record does show is that the *documentation* advantage of this implementation — generated Swagger and ReDoc — was lost in the port and back-filled eight days later with a hand-written `openapi.json` and an HTML playground (`ha-c17`).

**Outcome.** This code never ran anywhere public. The Worker did, and still does (`ha-c20`). Goal `g-render-free-deploy` is recorded as abandoned by outcome, not by decision.

**Synthesis at the end of the night.** The project believed small stateless utilities were worth publishing, for free, to anyone; that a single readable file was the right unit; that documentation should come from types rather than prose. It could ship a complete surface in an hour and port it in another. It could not — or did not — write down why it chose the edge. It refused to become a metered product, a keyed product or a stateful one, and it refused to become a second NoHustle. It inherited, from the first ninety seconds, a tracked bytecode file, no licence and a "20+" count that never matched the code.

### Era 2 — The eight-day afterlife as "the Python version" (2026-03-27 to 2026-04-03)

Nothing changed here. In the sibling, on 2026-04-03, a full README appeared with the live `workers.dev` URL, "All 22 Endpoints", "$0", "MIT", and an "Also Available" section listing this repository as the "Python/FastAPI version" alongside "RapidAPI: Listed for marketplace discovery" (`ha-c08`). Two hours later the Worker gained `openapi.json` and a playground. From this point the family's public framing is fixed: the Worker is the product; this is a parallel variant kept for Python readers and, possibly, a marketplace listing. Whether any RapidAPI listing ever existed is **unknown** (`ha-c13`): the README asserts it, every later reviewer marks it unverified, and the provider dashboard was not consulted.

The chronology contradiction is preserved rather than resolved (`hydra-api-x1`): by commit order this repository is the Worker's predecessor by seventy-five minutes and the source of its code; by the author's framing eight days later it is a sibling; by the August registry it is the "earlier ... predecessor ... superseded/shelved". All three are true of different things — origin, framing, deployment outcome.

### Era 3 — Reclassified from outside (2026-05-05 to 2026-07-22)

The repository did not move for the next four months; the portfolio around it did. On 2026-05-05 a workspace migration moved the checkout out of `CascadeProjects` into `backburner/` and generated an untracked manifest: `status: backburner`, `type: revenue`, `platform: render`, `url: null` (`ha-c07`, event `hydra-api-2026-05-05-backburner-and-revenue-label`). The migration filed the Worker in `backburner/` too, with `platform: none`; only later (by 2026-06-16) was the Worker promoted to `active/` — for several weeks the owner's own trackers listed a one-file static landing page (`hydra-site`) as the active HYDRA and the live engine as backburner. That mis-filing is why a 2026-07-22 research note concluded "hydra is NOT actually live (static backup repo, no deploy pipeline)" while the Worker was answering `200` (`ha-c05`, `ha-c20`; the sibling's history records it in detail).

In June the framing hardened in three documents written weeks apart. The asset-sale kit (2026-06-05) valued "HYDRA" — meaning the Worker — as "a deployable template ... or RapidAPI freemium", "no canonical price", and never named this repository (`ha-c22`). The marketing-machine gate (2026-06-17) failed "hydra" on G1, "no price set", and told the owner to either set a freemium tier or designate HYDRA a backlink asset for another product. The master portfolio (2026-06-23) called this repository "a parallel Python/FastAPI variant for a possible RapidAPI listing" (`ha-c08`) — the clearest statement of what it was *for* that anyone wrote, and it is a statement of possibility. A business-ops action list of 2026-06-22 was blunter: "Archive dead `hydra-api` (Render 404); list `hydra-worker` on RapidAPI".

July produced the only physical trace of anyone touching the code after March. The 2026-07-20 ship queue scheduled "hydra-api (Render) — Render → Blueprint → connect — 20m" for week three, and on the same day the tracked bytecode was regenerated (`ha-c11`, **inferred** that the module was imported or run locally; whether that was a deploy attempt is not known). No service appeared. The value audit of the same day flagged "MIT claimed with no LICENSE file" in the Worker — a debt this repository shares in a worse form, since it claims no licence at all.

**What the project believed by now** is best described as what others believed about it: a reference copy with an unexercised deployment path and an aspirational revenue label. The tension that propels the next era is simple — a public repository with a live-looking `autoDeploy: true` blueprint, a dead URL and a "revenue" tag is a credibility problem for a portfolio being audited for exactly that.

### Era 4 — Verdicts without a decision (2026-07-25 to 2026-08-16)

On 2026-07-25 the family got a source-of-truth boundary: the Worker "owns the Worker code, OpenAPI description, operator documentation, and editable `docs/index.html`"; the static site was archived byte-identical. This repository is not mentioned in that boundary — it was neither absorbed nor retired, simply left outside.

Three reviews then measured it within four days. The 2026-08-03 registry note calls it the "earlier Python/FastAPI predecessor, same feature set, targeting Render, never deployed ... Superseded/shelved". The 2026-08-06 dossier (agent-written) finds it public, `404` on Render, "labeled revenue but has no billing/auth and gives everything away free", and issues **PARK / FIX**: point the README at the live Worker and delete the stale `render.yaml`/`.pyc`, or make the repository private; drop the revenue label or add metering. The rule-based estate audit of the same day says **KILL** — "trivial: under 500 logical lines and under 10 commits" — a rule that also condemns the live Worker (`ha-c09`, contradiction `hydra-api-x6`). All three verdicts are opinions written by agents on the owner's behalf; none was adopted. An assistant session was opened in this directory on 2026-08-16 (a permissions file appeared, `ha-c19`) and produced no commit. Event `hydra-api-2026-08-06-audits-park-fix` is left **open** for that reason: the finding is that no decision was taken.

### Era 5 — The purge that did not touch it, and the record it now has (2026-09-02 to 2026-09-04)

The workspace-wide credential purge of early September 2026 rewrote eighteen owned remotes and pushed security commits to twenty-two others. This history was scanned, matched only "public configuration / placeholder" pattern classes, and was neither rewritten nor force-pushed; `origin/master` still equals local `master` (`ha-c12`, event `hydra-api-2026-09-02-credential-purge-untouched`). That matters more than it sounds: every commit anchor cited here remains valid, and the reconstruction did not have to rebind anything. The NoHustle sibling, by contrast, received a security commit its local clone had not fetched.

On 2026-09-04 this history system was installed (event `hydra-api-2026-09-04-history-system-bootstrap`): ledgers, capsules, doctrine, a deterministic renderer, tests, an agent contract, a PR template and a CI workflow that will run once pushed. The dispatch brief for that work mis-assigned dirty baselines between the two HYDRA repositories; the measured state was used and the discrepancy recorded (`ha-c18`, `hydra-api-x5`).

### The lineage question, answered with evidence

**NoHustle (Aug 2025) → HYDRA API (Mar 2026) → HYDRA Worker (Mar 2026).** The chain is real as a sequence of the same author's attempts at the same thesis; it is not a code lineage at any link but the last.

- *NoHustle → this repository:* no shared code, routes or literals (`ha-c14`, confirmed). What carried over is the thesis (small utilities via an API marketplace), the Render habit, and — by inversion — every choice NoHustle stalled on (`ha-c15`, plausible). The January-2026 audit shows the owner still valued NoHustle as reusable code (`ha-c23`); the rebuild ignored it.
- *This repository → the Worker:* a route-for-route port made seventeen minutes after the blueprint, with the Worker still pointing its `docs` here (`ha-c04`, confirmed). Rejected in the port: Render and a Python runtime; lost in the port: generated Swagger/ReDoc, later replaced by hand-written OpenAPI (`ha-c17`).
- *What was rejected across the whole chain* (paid → free, keyed → keyless, Flask → FastAPI → Workers, BSL → none → MIT, seven ML-heavy file endpoints → twenty-four stdlib text/crypto utilities) is established by the code. *Why* is established nowhere.

### Inheritance — what the present carries

- A public, unlicensed repository whose `autoDeploy: true` blueprint points at a host that has never served it (`ha-c03`, `ha-c05`).
- A committed bytecode file that has been the repository's only "dirty" line for five months (`ha-c02`, `ha-c11`).
- The role of *documentation target* for a live API it does not describe accurately: the Worker banner still says `docs: hydra-toolkit-api` and `endpoints: 20` (`ha-c04`, `ha-c16`).
- A `revenue` label with no mechanism, and a marketplace listing that may not exist (`ha-c07`, `ha-c13`).
- Three unadopted verdicts and one open event awaiting an owner decision (`ha-c09`).
- One genuine, unique asset: readable Python with generated Swagger/ReDoc that the Worker never had (`ha-c17`).

## Chapter: IDEOLOGY.md

## Ideology — the worldview this code reveals

_"Ideology" here means the project's governing assumptions, priorities, non-negotiables, theory of the problem, intended beneficiaries, definition of success, acceptable trade-offs and revealed non-goals. Nothing below is manufactured from motive; where the code is the only witness, that is said._

### Theory of the problem

Developers spend small, repeated units of attention on utilities that are individually trivial and collectively tedious. The remedy is not a library — libraries must be installed, versioned and learned — but a **public HTTP surface** that answers a typed request with a JSON answer and documents itself. The unit of value is the endpoint; the unit of trust is the readable source. Both are visible in the first commit and nowhere restated (`ha-c01`, `ha-c06`).

### Theory of change

Publish everything, charge nothing, require nothing. Adoption, if it comes, comes from discovery (a marketplace listing, a README, a playground) rather than from sales. This is stated only later and only for the Worker — "intended top-of-funnel dev surface + a freemium RapidAPI candidate" (2026-06-23, `ha-c08`) — and the "freemium" half was never built anywhere in the family.

### Intended beneficiaries over time

1. **2026-03-26:** anonymous developers (wildcard CORS, no key) and the studio's own portfolio ("Built by Toledo Technologies LLC").
2. **2026-04-03:** readers who prefer Python — the Worker README lists this as the "Python/FastAPI version" (`ha-c08`).
3. **2026-05 to 2026-08:** the owner and the agents that operate the portfolio; the repository exists in their records as an inventory row, a ship-queue item, a dossier (`ha-c07`, `ha-c09`, `ha-c22`).

The beneficiary drifted from users to bookkeeping without a single change to the code.

### Principles (versioned in `.project-history/doctrine/principles.yml`)

| Principle | Status | Revealed by |
|---|---|---|
| `p-one-file-stateless` v1 — one file, no database, no state, no outbound calls; every handler a pure function of its request | active | `main.py` structure; absence of storage or HTTP clients |
| `p-keyless-free` v1 — no API key, no billing, open CORS | **challenged** since 2026-05-05 by the `type: revenue` label and the June "freemium candidate" framing, neither of which changed the code | `CORSMiddleware(allow_origins=["*"])`; no auth dependency |
| `p-minimal-deps` v1 — three pinned framework dependencies and the standard library | active | `requirements.txt`; `hashlib`/`re`/`json`/`difflib`/`urllib` in `main.py` (`ha-c21`) |
| `p-self-documenting` v1 — typed models with field descriptions feed generated Swagger and ReDoc | active | `FastAPI(docs_url="/docs", redoc_url="/redoc")`, pydantic `Field(description=…)` (`ha-c17`) |
| `p-render-first-hosting` v1 — host on Render's free plan from a blueprint with auto-deploy | **superseded** the same night by the edge-first principle enacted in `hydra-worker` | `render.yaml` (`ha-c03`) |

No principle has a version 2. That is itself the finding: the doctrine froze at 02:11 EDT on 2026-03-26.

### Non-goals and negative space

Revealed by absence — none is written anywhere:

- **No authentication, metering or rate limiting.** Not stubbed, not commented, not in the README's future tense. The only later mention of metering is by auditors recommending it (`ha-c09`).
- **No persistence.** No database, no file writes, no cache. NoHustle's SQLite usage analytics have no descendant here.
- **No heavy processing.** Nothing that needs a model, a binary or more memory than a request; NoHustle's `rembg`/`pdfplumber`/`pandas` stack has no descendant here.
- **No tests.** The Worker at least kept a template test; this repository has none.
- **No licence.** The Worker chose MIT in text and, from 2026-09-01, in a file; this repository never chose.

### Recurring tensions

1. **Free versus revenue.** The code gives everything away; the manifest and every strategy document call it a revenue asset or a freemium candidate; the marketing gate fails it for having no price. The tension was recorded on both sides and resolved on neither (`hydra-api-x3`).
2. **Readability versus reach.** The Python file is the more readable and better-documented implementation; the Worker is the one that runs everywhere for free. Readability lost the deployment and kept the `docs` link.
3. **Intent versus decision.** A blueprint with `autoDeploy: true` is an intent to run. Nothing turned it into a service, and nothing turned it off; it sits in a public repository as a live-looking configuration for a dead URL (`ha-c05`).
4. **Public versus dormant.** The repository is one of the estate's few public ones. Every reviewer asks whether that is wanted; nobody answered.
5. **Rule versus judgement.** The estate audit's KILL rule ("under 500 lines and under 10 commits") condemns this repository and the live Worker alike; the judgement-based dossier says PARK; the registry says shelved (`hydra-api-x6`).

### Stated ideals versus revealed behaviour

- *Stated:* "20+ endpoints" (README, commit message, FastAPI title). *Revealed:* 24 utility routes plus two meta routes; the family later published 22 and 20 for the same code (`ha-c16`). The number was never counted — it was a slogan.
- *Stated (by the Worker):* "Python/FastAPI version — also available". *Revealed:* never available at any URL (`ha-c05`).
- *Stated (by the manifest):* `type: revenue`. *Revealed:* no mechanism; no price; no listing evidenced (`ha-c07`, `ha-c13`).
- *Stated (by the blueprint):* deploy on push. *Revealed:* no push after the blueprint (`ha-c10`).

### What the project refused to become

A second NoHustle. Every axis on which NoHustle was heavy — dependencies, state, keys, tiers, licence restrictions, host-specific fixes — is light or absent here. The refusal is visible in the code with **confirmed** confidence; that it was a *conscious* refusal is **plausible** and unproven (`ha-c15`).

### Evolution

There was none inside the repository. Outside it, the ideology of the *family* moved from "free edge utility" (April) to "freemium candidate" (June) to "set a price or shelve it" (June, marketing gate) to "park, fix or kill" (August). This repository's doctrine is a snapshot of the first position; the pressure to change it has been recorded four times and answered zero times.

## Chapter: GOALS.md

## Goals — every goal, its lifecycle and what "success" meant

_Versioned lifecycle records live in `.project-history/doctrine/goals.yml`. Status vocabulary: proposed → active → narrowed / expanded / blocked → achieved / abandoned / superseded. Dates are decision or observation dates, not commit dates, unless stated._

### `g-ship-toolkit-v1` — ship a working "20+ endpoint" developer utility API in one sitting

- **Proposed / activated:** 2026-03-26, revealed by the root commit's subject line and the FastAPI title (`ha-c01`).
- **Definition of success at the time:** every route answers locally; the generated docs page lists them all. The only bug fix (89 seconds later) and the committed bytecode show the code was run (`ha-c02`).
- **Status: achieved** the same night. The measure that would have exposed the count problem — actually counting — was never applied (`ha-c16`).
- **Consequence:** the goal's completeness made the code portable, and portability made this copy expendable.

### `g-render-free-deploy` — run the service on Render's free plan from the blueprint

- **Proposed / activated:** 2026-03-26 02:11 EDT with `render.yaml` (`ha-c03`).
- **Definition of success:** a live `onrender.com` URL answering `/health`.
- **Blocked / overtaken:** seventeen minutes later by the Worker port (`ha-c04`).
- **Still listed as work:** the 2026-07-20 ship queue scheduled "Render → Blueprint → connect — 20m" for week three; the 2026-07-22 research note listed it under "ready-but-unshipped (need your accounts)"; the bytecode was regenerated the same day (`ha-c05`, `ha-c11`).
- **Status: abandoned** — by outcome, not by any written decision. Every probe (2026-08-06, 2026-09-04) found no service.
- **What could revive it:** connecting the blueprint takes minutes; what is missing is a reason, since the Worker already serves the same routes for free.

### `g-python-reference` — remain the Python/FastAPI reference for readers who prefer Python or want generated Swagger/ReDoc

- **Proposed:** 2026-04-03, when the Worker README listed this repository under "Also Available" (`ha-c08`).
- **Definition of success:** the repository stays readable, public and linked from the Worker as the Python version.
- **Status: active** (review by 2026-12-31). It is met in the weakest sense: the link exists and the code is unchanged. It is undermined by the same facts every auditor lists — a dead blueprint, committed bytecode, no licence, no tests.
- **Tension:** this is the only goal that argues for keeping the repository at all, and it was never stated by the owner; it is inferred from the README link and from the Worker's lack of generated docs (`ha-c17`).

### `g-rapidapi-listing` — offer HYDRA on RapidAPI for marketplace discovery, possibly as a freemium tier

- **Proposed:** 2026-04-03 ("RapidAPI: Listed for marketplace discovery", Worker README) and 2026-06-23 ("a possible RapidAPI listing", master portfolio) (`ha-c08`).
- **Definition of success (supplied later by the marketing-machine documents):** a published listing with at least a free tier and a decided price.
- **Status: blocked** since 2026-06-17 on gate G1, "no price set"; a business-model decision the documents explicitly refuse to treat as a one-click fix. Whether any listing was ever created is unknown (`ha-c13`).
- **Which repository was meant:** the June portfolio ties the listing to *this* Python variant; every later document ties "hydra" to the Worker. The ambiguity is preserved in `hydra-api-x1`.

### `g-revenue-classification` — be a revenue asset (the manifest's `type`)

- **Proposed:** 2026-05-05 by the migration tooling's generated `.toledo.yaml` (`ha-c07`).
- **Definition of success:** any paid usage or a listed price.
- **Status: blocked.** No auth, metering or billing exists in code; the 2026-08-06 dossier calls the label "aspirational, not real revenue" (`ha-c09`, `hydra-api-x3`).
- **Alternative named by the documents:** drop the label and treat HYDRA as a lead/backlink asset. Not chosen either.

### Goals that were never proposed

Worth recording because their absence is a choice: a test suite; a licence; a versioning or release scheme (the FastAPI `version="1.0.0"` never changed and there are no tags); reconciling the endpoint count; a custom domain; rate limiting or abuse protection for a public no-key API. The Worker's history shows several of these surfacing as audit findings in July–August 2026; none surfaced here.

### How the definition of success moved

| When | Success meant | Who said so |
|---|---|---|
| 2026-03-26 | it runs, the docs list everything | the code (`ha-c01`, `ha-c02`) |
| 2026-03-26 02:11 | a live Render URL | `render.yaml` (`ha-c03`) |
| 2026-04-03 | "also available" next to a live Worker | Worker README (`ha-c08`) |
| 2026-06-17 | a decided price | marketing gate G1 (`ha-c13`) |
| 2026-06-23 | a possible RapidAPI listing | master portfolio (`ha-c08`) |
| 2026-08-06 | a credibility fix: README → Worker, delete blueprint/bytecode, or go private | dossier (`ha-c09`) |

The repository met the first and none of the rest.

## Chapter: DECISION_MAP.md

## Decision map — genealogies and cross-links

_Each genealogy follows `pressure → belief → alternatives → decision → implementation → result → consequence → later revision`. The index at the end is generated by `scripts/project_history.py render` from the event capsules and doctrine files; edit those, not the table._

### D1 — Build the whole surface as one FastAPI file (2026-03-26 01:13 EDT)

- **Pressure:** ship a complete, demonstrable developer API at zero cost (**inferred**).
- **Belief:** typed inputs plus generated docs are the product; statelessness is a feature.
- **Alternatives (revealed by contrast with NoHustle, not by any note):** a keyed, metered, ML-heavy file-processing API; a multi-module package; a licence-restricted release. None taken (`ha-c14`, `ha-c15`).
- **Decision and implementation:** commit `ff404c6030c6529b28dbc50ff7b80f1031eb7916` — 437 lines, 26 routes, three pins (`ha-c01`). Fix `58f61160f054a28da6573e37adadd943fd188e12` eighty-nine seconds later (`ha-c02`).
- **Result:** complete and runnable in an hour.
- **Consequence:** trivially portable; the committed bytecode and the missing licence become permanent debts.
- **Later revision:** none. Event `hydra-api-2026-03-26-fastapi-toolkit-v1`.

### D2 — Host on Render from a blueprint (2026-03-26 02:11 EDT)

- **Pressure:** the code is finished and unhosted.
- **Belief:** Render's free plan with auto-deploy is the fastest route to a URL — the author's habit since NoHustle.
- **Decision and implementation:** commit `0106964e92fa29d6a9cde46fa652839cb282b302` (`render.yaml`, `.gitignore`) (`ha-c03`).
- **Result:** never observed serving; `x-render-routing: no-server` on every probe (`ha-c05`).
- **Consequence:** a live-looking `autoDeploy: true` configuration on a public repository for a dead URL; flagged by every auditor.
- **Later revision:** superseded within seventeen minutes by D3; principle `p-render-first-hosting` marked superseded; goal `g-render-free-deploy` abandoned by outcome. Event `hydra-api-2026-03-26-render-blueprint-and-worker-port`.

### D3 — Re-express the same routes as a Cloudflare Worker (2026-03-26 02:28 EDT, enacted in another repository)

- **Pressure:** unrecorded. Candidates: edge latency and cost (the Worker's later marketing), Render friction (**inferred** from NoHustle), or Python as draft language with the edge always the target.
- **Decision and implementation:** new repository `hydra-worker`, root `2a804e67b5eb84bb52ddd4950fa41b0aa533959b`, route-for-route port; `/` banner keeps `docs` pointing here (`ha-c04`).
- **Result:** the Worker went live and is still live (`ha-c20`); this repository went silent.
- **Consequence:** two public repositories describe one product with drifting counts and links (`ha-c16`); generated Swagger/ReDoc lost, replaced by hand-written OpenAPI eight days later (`ha-c17`).
- **Cross-link:** the Worker's own capsule `hydra-worker-2026-03-26-worker-port-and-first-deploy` in `/home/nick/Development/active/hydra-worker`.

### D4 — Keep this repository as "the Python/FastAPI version" (2026-04-03, by framing rather than decision)

- **Belief:** a Python reader or a marketplace listing might want it.
- **Implementation:** one line in the Worker README (`465f28476f262c580f8e9a10638851209cafe88c`) (`ha-c08`).
- **Result:** the repository stayed public and unchanged.
- **Consequence:** goal `g-python-reference` (active, inferred); the June portfolio's "parallel variant for a possible RapidAPI listing" framing; contradiction `hydra-api-x1` about predecessor versus sibling.

### D5 — File it under `backburner/` and label it `revenue` (2026-05-05, tooling on an owner-approved plan)

- **Implementation:** migration log entries and the untracked `.toledo.yaml` (`ha-c07`); the master-portfolio commit `73e342abef33abc9161838c868d5f3939d92e721` framed the family in June.
- **Result:** the label contradicts the code; the marketing gate fails "hydra" on price (`ha-c13`); the asset kit and registry treat "hydra" as the Worker only (`ha-c22`).
- **Consequence:** principle `p-keyless-free` marked *challenged*; goals `g-revenue-classification` and `g-rapidapi-listing` blocked. Event `hydra-api-2026-05-05-backburner-and-revenue-label`.

### D6 — Three verdicts, no decision (2026-08-03 to 2026-08-06)

- **Accounts:** registry "superseded/shelved"; dossier PARK/FIX; estate audit KILL by rule (`ha-c09`).
- **Result:** nothing changed; an assistant session on 2026-08-16 produced no commit (`ha-c19`).
- **Consequence:** contradiction `hydra-api-x6`; event `hydra-api-2026-08-06-audits-park-fix` left **open** until an owner decision is recorded.

### D7 — Do not rewrite (2026-09-02, decided by the credential purge's classification)

- **Implementation:** pattern classes RETAINED_PUBLIC_CLASS only; no force-push; `origin/master` unchanged (`ha-c12`).
- **Consequence:** every anchor in this record remains valid. Event `hydra-api-2026-09-02-credential-purge-untouched`.

### D8 — Install the history system (2026-09-04)

- Event `hydra-api-2026-09-04-history-system-bootstrap`; anchored to `0106964e92fa29d6a9cde46fa652839cb282b302`; the dispatch baseline discrepancy is recorded rather than smoothed (`ha-c18`, `hydra-api-x5`).

### Generated index

<!-- BEGIN GENERATED: decision-index -->
| Event | Kind | Significance | Occurred | Status | Related | Amends / supersedes |
|---|---|---|---|---|---|---|
| `hydra-api-2026-03-26-fastapi-toolkit-v1` | origin | high | 2026-03-26 | closed | `hydra-api-2026-03-26-render-blueprint-and-worker-port` | — |
| `hydra-api-2026-03-26-render-blueprint-and-worker-port` | abandonment | high | 2026-03-26 | closed | `hydra-api-2026-03-26-fastapi-toolkit-v1`, `hydra-api-2026-08-06-audits-park-fix` | — |
| `hydra-api-2026-05-05-backburner-and-revenue-label` | governance | medium | 2026-05-05 | closed | `hydra-api-2026-03-26-render-blueprint-and-worker-port`, `hydra-api-2026-08-06-audits-park-fix` | — |
| `hydra-api-2026-08-06-audits-park-fix` | governance | medium | 2026-08-06 | open | `hydra-api-2026-05-05-backburner-and-revenue-label`, `hydra-api-2026-09-02-credential-purge-untouched` | — |
| `hydra-api-2026-09-02-credential-purge-untouched` | security | medium | 2026-09-02 | closed | `hydra-api-2026-08-06-audits-park-fix`, `hydra-api-2026-09-04-history-system-bootstrap` | — |
| `hydra-api-2026-09-04-history-system-bootstrap` | bootstrap | medium | 2026-09-04 | closed | `hydra-api-2026-09-02-credential-purge-untouched` | — |

##### Principles (versioned)

| Id | v | Status | Introduced | Supersedes | Statement |
|---|---|---|---|---|---|
| `p-one-file-stateless` | 1 | active | 2026-03-26 | — | One file, no database, no persistent state, no outbound calls: every endpoint is a pure function of its request, so the service can be read in one sitting and hosted anywhere. |
| `p-keyless-free` | 1 | challenged | 2026-03-26 | — | No API key, no billing and open CORS; anyone may call any endpoint. |
| `p-minimal-deps` | 1 | active | 2026-03-26 | — | Three pinned framework dependencies and the standard library for everything else; no ML, no parsers, no clients. |
| `p-self-documenting` | 1 | active | 2026-03-26 | — | The API documents itself; typed request models with field descriptions feed generated Swagger and ReDoc pages. |
| `p-render-first-hosting` | 1 | superseded | 2026-03-26 | — | Host on Render's free plan from a blueprint with auto-deploy on push. |

##### Goals (lifecycle)

| Id | v | Status | Introduced | Review by | Supersedes | Statement |
|---|---|---|---|---|---|---|
| `g-ship-toolkit-v1` | 1 | achieved | 2026-03-26 | — | — | Ship a working "20+ endpoint" developer utility API in a single sitting. |
| `g-render-free-deploy` | 1 | abandoned | 2026-03-26 | — | — | Run the service on Render's free plan from the blueprint. |
| `g-python-reference` | 1 | active | 2026-04-03 | 2026-12-31 | — | Remain the Python/FastAPI reference for readers who prefer Python or want generated Swagger/ReDoc documentation. |
| `g-rapidapi-listing` | 1 | blocked | 2026-04-03 | 2026-12-31 | — | Offer HYDRA on RapidAPI for marketplace discovery, possibly as a freemium tier. |
| `g-revenue-classification` | 1 | blocked | 2026-05-05 | 2026-12-31 | — | Be a revenue asset (the .toledo.yaml type). |
<!-- END GENERATED: decision-index -->

## Chapter: TIMELINE.md

## Timeline — deterministic, evidence-linked index

_Generated by `scripts/project_history.py render` from event front matter and claim dates. Rows are sorted by date, then kind, then id; identical inputs produce identical output. Times inside claim locators are UTC unless marked EDT. This index is a lookup aid, not the story — read `NARRATIVE.md` for causality._

Reading the rows: `occurred` / `decided` / `merged` / `released` are the distinct dates carried by each event capsule (null dates are omitted); `claim` rows carry the claim's own date or the start of its date range. Events whose `released` date is null were never released or deployed — for this repository that is all of them.

<!-- BEGIN GENERATED: timeline -->
| Date | Kind | Id | Summary | Record |
|---|---|---|---|---|
| 2025-08-18 | claim | `ha-c14` | NoHustle API (2025-08-18..21) shares this project's author, its RapidAPI-marketplace thesis and its Render-fir | `.project-history/claims.yml` |
| 2026-01-17 | claim | `ha-c23` | Nine weeks before this repository existed, the owner's 2026-01-17 codebase audit still rated NoHustle API "Pro | `.project-history/claims.yml` |
| 2026-03-26 | claim | `ha-c01` | The repository began on 2026-03-26 at 05:13:09Z (01:13 EDT) with a single 437-line FastAPI file exposing 26 ro | `.project-history/claims.yml` |
| 2026-03-26 | claim | `ha-c02` | Eighty-nine seconds after the root commit, a tuple-unpacking bug in the json/validate key counter was fixed, a | `.project-history/claims.yml` |
| 2026-03-26 | claim | `ha-c03` | At 06:11:04Z (02:11 EDT) a Render blueprint was added (free plan, Oregon, uvicorn start command, autoDeploy tr | `.project-history/claims.yml` |
| 2026-03-26 | claim | `ha-c04` | Seventeen minutes later (06:28:23Z, 02:28 EDT) the sibling repository hydra-worker was born with a Hono/Cloudf | `.project-history/claims.yml` |
| 2026-03-26 | claim | `ha-c05` | No evidence of this service ever being deployed exists: .toledo.yaml records deployment url null (2026-05-05), | `.project-history/claims.yml` |
| 2026-03-26 | claim | `ha-c06` | The code has no authentication, no rate limiting, no billing hook and wildcard CORS; every handler is a pure f | `.project-history/claims.yml` |
| 2026-03-26 | claim | `ha-c15` | HYDRA's design inverts every point where NoHustle stalled — heavy ML dependencies became zero dependencies, SQ | `.project-history/claims.yml` |
| 2026-03-26 | claim | `ha-c16` | The endpoint count is stated inconsistently across the family: this README says "20+", the Worker README and G | `.project-history/claims.yml` |
| 2026-03-26 | claim | `ha-c17` | FastAPI's generated Swagger (/docs) and ReDoc (/redoc) pages were part of this design; the Worker port has no | `.project-history/claims.yml` |
| 2026-03-26 | claim | `ha-c21` | The three-dependency posture (fastapi 0.115.6, uvicorn 0.34.0, pydantic 2.10.4) and standard-library-only util | `.project-history/claims.yml` |
| 2026-03-26 | decided | `hydra-api-2026-03-26-fastapi-toolkit-v1` | One-file FastAPI developer toolkit built and committed in a single sitting | `.project-history/events/2026/hydra-api-2026-03-26-fastapi-toolkit-v1.md` |
| 2026-03-26 | decided | `hydra-api-2026-03-26-render-blueprint-and-worker-port` | Render blueprint added, then overtaken by the Cloudflare Worker port 17 minutes later | `.project-history/events/2026/hydra-api-2026-03-26-render-blueprint-and-worker-port.md` |
| 2026-03-26 | merged | `hydra-api-2026-03-26-fastapi-toolkit-v1` | One-file FastAPI developer toolkit built and committed in a single sitting | `.project-history/events/2026/hydra-api-2026-03-26-fastapi-toolkit-v1.md` |
| 2026-03-26 | merged | `hydra-api-2026-03-26-render-blueprint-and-worker-port` | Render blueprint added, then overtaken by the Cloudflare Worker port 17 minutes later | `.project-history/events/2026/hydra-api-2026-03-26-render-blueprint-and-worker-port.md` |
| 2026-03-26 | occurred | `hydra-api-2026-03-26-fastapi-toolkit-v1` | One-file FastAPI developer toolkit built and committed in a single sitting | `.project-history/events/2026/hydra-api-2026-03-26-fastapi-toolkit-v1.md` |
| 2026-03-26 | occurred | `hydra-api-2026-03-26-render-blueprint-and-worker-port` | Render blueprint added, then overtaken by the Cloudflare Worker port 17 minutes later | `.project-history/events/2026/hydra-api-2026-03-26-render-blueprint-and-worker-port.md` |
| 2026-04-03 | claim | `ha-c08` | The Worker README (2026-04-03) lists this repository under "Also Available" as the "Python/FastAPI version", a | `.project-history/claims.yml` |
| 2026-04-03 | claim | `ha-c13` | Whether a RapidAPI listing for HYDRA (in any form) was ever created is unknown: the Worker README asserts "Lis | `.project-history/claims.yml` |
| 2026-04-03 | claim | `ha-c20` | The Worker, not this service, became the deployed HYDRA surface: the Worker README of 2026-04-03 already publi | `.project-history/claims.yml` |
| 2026-05-05 | claim | `ha-c07` | On 2026-05-05 the workspace migration moved the checkout from the macOS CascadeProjects directory into backbur | `.project-history/claims.yml` |
| 2026-05-05 | decided | `hydra-api-2026-05-05-backburner-and-revenue-label` | Workspace migration files the repository under backburner/ and labels it a revenue asset | `.project-history/events/2026/hydra-api-2026-05-05-backburner-and-revenue-label.md` |
| 2026-05-05 | occurred | `hydra-api-2026-05-05-backburner-and-revenue-label` | Workspace migration files the repository under backburner/ and labels it a revenue asset | `.project-history/events/2026/hydra-api-2026-05-05-backburner-and-revenue-label.md` |
| 2026-06-05 | claim | `ha-c22` | The workspace registry, marketing-machine documents and asset-sale kit treat "hydra" as one product (the Worke | `.project-history/claims.yml` |
| 2026-07-20 | claim | `ha-c11` | The tracked bytecode file was regenerated locally on 2026-07-20 (file mtime 19:49 local), the same day the own | `.project-history/claims.yml` |
| 2026-08-03 | claim | `ha-c09` | Later owner records reinterpret the repository: the 2026-08-03 registry note calls it the "earlier Python/Fast | `.project-history/claims.yml` |
| 2026-08-06 | occurred | `hydra-api-2026-08-06-audits-park-fix` | August 2026 audits reinterpret the repository as a shelved predecessor and recommend PARK or KILL | `.project-history/events/2026/hydra-api-2026-08-06-audits-park-fix.md` |
| 2026-08-16 | claim | `ha-c19` | An agent permissions file (.claude/settings.local.json allowing two Gmail MCP tools) appeared in the checkout | `.project-history/claims.yml` |
| 2026-09-02 | claim | `ha-c12` | The September 2026 credential purge examined this history, matched only "public configuration / placeholder" p | `.project-history/claims.yml` |
| 2026-09-02 | decided | `hydra-api-2026-09-02-credential-purge-untouched` | September 2026 credential purge classifies the history as clean and leaves it unrewritten | `.project-history/events/2026/hydra-api-2026-09-02-credential-purge-untouched.md` |
| 2026-09-02 | occurred | `hydra-api-2026-09-02-credential-purge-untouched` | September 2026 credential purge classifies the history as clean and leaves it unrewritten | `.project-history/events/2026/hydra-api-2026-09-02-credential-purge-untouched.md` |
| 2026-09-04 | claim | `ha-c10` | The GitHub repository is public, has no licence file, no topics, no issues, pull requests, releases or tags, a | `.project-history/claims.yml` |
| 2026-09-04 | claim | `ha-c18` | The lead's dispatch brief recorded this repository's dirty baseline as ".env.example" and hydra-worker's as th | `.project-history/claims.yml` |
| 2026-09-04 | decided | `hydra-api-2026-09-04-history-system-bootstrap` | Bootstrap of the project-history system (reconstruction and maintenance mechanism) | `.project-history/events/2026/hydra-api-2026-09-04-history-system-bootstrap.md` |
| 2026-09-04 | occurred | `hydra-api-2026-09-04-history-system-bootstrap` | Bootstrap of the project-history system (reconstruction and maintenance mechanism) | `.project-history/events/2026/hydra-api-2026-09-04-history-system-bootstrap.md` |

#### Git anchors cited by events

- `0106964e92fa29d6a9cde46fa652839cb282b302`
- `2a804e67b5eb84bb52ddd4950fa41b0aa533959b`
- `58f61160f054a28da6573e37adadd943fd188e12`
- `73e342abef33abc9161838c868d5f3939d92e721`
- `ff404c6030c6529b28dbc50ff7b80f1031eb7916`
<!-- END GENERATED: timeline -->

## Chapter: OPEN_QUESTIONS.md

## Open questions, gaps and low-confidence claims

_Ranked by how much an answer would change the record. "No evidence found" is never treated as "did not happen"; each entry names what was searched and what would settle it._

### Ranked questions

1. **Why were two implementations made the same night, and why did the edge win?** The only witnesses are commit timestamps and the Worker's later marketing copy. Searched: both repositories' full histories, every owner document naming HYDRA, the migration logs. Would settle it: the AI-assisted authoring session of 2026-03-26 (former `CascadeProjects` directory; inaccessible) or one sentence from the owner. Affects `ha-c15` (plausible), contradiction `hydra-api-x1`, principle `p-render-first-hosting`'s supersession note.
2. **Was a Render service ever created from the blueprint, then deleted?** Every probe says `no-server`; the ship queue and research note of July 2026 treat it as undone. Searched: probes on 2026-08-06 and 2026-09-04, all dated owner records. Would settle it: the Render dashboard's service list and event history (a business-ops note of 2026-06-22 records that the Render workspace could not be enumerated by tooling). Affects `ha-c05` (strongly supported, not confirmed), `hydra-api-x2`.
3. **Does any RapidAPI listing for HYDRA exist, and for which implementation?** The Worker README asserts one; no document, listing copy or traffic corroborates it; the June portfolio attaches the possibility to this Python variant. Would settle it: the RapidAPI provider account. Affects `ha-c13` (unknown), goal `g-rapidapi-listing`.
4. **Which verdict does the owner accept — park, fix, kill, or keep as reference?** Three agent-written opinions, zero recorded decisions. Would settle it: an event capsule recording the choice. Affects event `hydra-api-2026-08-06-audits-park-fix` (open), `hydra-api-x6`, goal `g-python-reference`.
5. **Was the 2026-07-20 bytecode regeneration a deploy attempt?** A file mtime coinciding with the ship-queue date. Would settle it: shell history or Render build logs. Affects `ha-c11` (plausible).
6. **What was the 2026-08-16 assistant session for?** A permissions file appeared; no commit followed. Would settle it: the session transcript. Affects `ha-c19` (plausible).
7. **Where did the endpoint list come from?** A prompt, a competitor's feature list, or NoHustle's leftovers? Nothing in the tree or the owner's documents says. Affects the prehistory paragraph of `NARRATIVE.md` only.
8. **Did the owner ever intend this repository, rather than the Worker, to be the RapidAPI artifact?** One document implies it (2026-06-23); none repeats it. Affects `hydra-api-x1`.

### Contradictions carried in the register (`.project-history/contradictions.yml`)

- `hydra-api-x1` — predecessor or parallel variant (chronology; strongly supported reading: both, of different things).
- `hydra-api-x2` — ever deployed to Render (outcome; strongly supported: never).
- `hydra-api-x3` — revenue asset (interpretation; confirmed: label only).
- `hydra-api-x4` — endpoint count 20 / 20+ / 22 / 24 (fact; confirmed: 24 utility + 2 meta).
- `hydra-api-x5` — the dispatch brief's dirty baseline versus the measured one (fact; confirmed: measured state used).
- `hydra-api-x6` — what should become of the repository (interpretation; plausible: dormant reference copy).

### Low-confidence claims to keep visible

- `ha-c11` (plausible, inferred) — bytecode regeneration as a deploy attempt.
- `ha-c13` (unknown) — existence of a RapidAPI listing.
- `ha-c15` (plausible, inferred) — HYDRA as a deliberate inversion of NoHustle.
- `ha-c19` (plausible, inferred) — purpose of the 2026-08-16 session.

### Evidence gaps and lost or inaccessible sources

- The 2026-03-26 authoring session (former macOS `CascadeProjects` path, unlinked 2026-05-05).
- Render dashboard and deploy logs for `hydra-toolkit-api`.
- RapidAPI provider account state.
- Any pre-repository design note; none exists in the owner's synced documents (searched only for the project's names).
- The committed `__pycache__/main.cpython-312.pyc` binary was not disassembled; its content is assumed to match `main.py` at `58f61160f054a28da6573e37adadd943fd188e12`.

### Biases audited

- **Main-branch bias:** there is one branch; no never-merged work exists to be missed (`refs_examined` in `state.yml`).
- **Survivor bias:** the live Worker's account of the family was not allowed to define this repository; the June portfolio's "parallel variant" framing and the August "predecessor" framing are both preserved.
- **Recency and hindsight bias:** the August verdicts are labelled as opinions written five months after the event, by agents, and are not used to infer March intent.
- **Most-articulate-source bias:** the longest documents about HYDRA (dossiers, marketing blueprints) are retrospective and agent-written; the terse contemporaneous record (four commits, one README line) is given priority for what happened, and the long documents only for what was later believed.

### Coverage statement

All three reachable commits were deep-read (the binary `.pyc` excepted); both tracking refs examined; the related repositories (`hydra-worker`, `NoHustle API`, `hydra-site`, `experiments/thing`) read in full; every dated owner document naming HYDRA or NoHustle read for the relevant lines only. That is complete coverage of the available record and is not the same as knowing the project's full history: the design happened inside a session whose transcript is unavailable, and the only account of intent is the code plus later retrospectives. See Appendix D of `PROJECT_HISTORY.md` and `state.yml` for counts, exclusions and the coverage matrix.

## Appendix A — Claims ledger

| Claim | Date | Type | Status | Confidence | Statement |
|---|---|---|---|---|---|
| `ha-c01` | 2026-03-26 | direct | verified | confirmed | The repository began on 2026-03-26 at 05:13:09Z (01:13 EDT) with a single 437-line FastAPI file exposing 26 routes (24 utilities plus / and /health), a 31-line README and three pinned dependencies; the GitHub repository was created two seconds later. |
| `ha-c02` | 2026-03-26 | direct | verified | confirmed | Eighty-nine seconds after the root commit, a tuple-unpacking bug in the json/validate key counter was fixed, and the CPython 3.12 bytecode cache was committed alongside the fix. |
| `ha-c03` | 2026-03-26 | direct | verified | confirmed | At 06:11:04Z (02:11 EDT) a Render blueprint was added (free plan, Oregon, uvicorn start command, autoDeploy true, PYTHON_VERSION 3.11.0) together with a .gitignore that ignores the already-tracked bytecode. |
| `ha-c04` | 2026-03-26 | behavioral | verified | confirmed | Seventeen minutes later (06:28:23Z, 02:28 EDT) the sibling repository hydra-worker was born with a Hono/Cloudflare Workers implementation that is a route-for-route port of this file: all 26 routes match, identifier overlap is 0.82, the stop-word list, name/company tables and password heuristics are the same, and the Worker's `/` banner links its `docs` to this repository. |
| `ha-c05` | 2026-03-26..2026-09-04 | behavioral | verified | strongly_supported | No evidence of this service ever being deployed exists: .toledo.yaml records deployment url null (2026-05-05), the 2026-07-20 ship queue still lists "Render -> Blueprint -> connect" as a 20-minute to-do, and hydra-toolkit-api.onrender.com returned 404 with x-render-routing no-server on 2026-08-06 and again on 2026-09-04. |
| `ha-c06` | 2026-03-26 | direct | verified | confirmed | The code has no authentication, no rate limiting, no billing hook and wildcard CORS; every handler is a pure function of the request, and the README signs the work "Built by Toledo Technologies LLC". |
| `ha-c07` | 2026-05-05 | contemporaneous | verified | confirmed | On 2026-05-05 the workspace migration moved the checkout from the macOS CascadeProjects directory into backburner/ and generated an untracked .toledo.yaml marking status backburner, type revenue, platform render, url null. |
| `ha-c08` | 2026-04-03..2026-06-23 | contemporaneous | verified | confirmed | The Worker README (2026-04-03) lists this repository under "Also Available" as the "Python/FastAPI version", and the owner's 2026-06-23 portfolio calls it "a parallel Python/FastAPI variant for a possible RapidAPI listing". |
| `ha-c09` | 2026-08-03..2026-08-06 | retrospective | reported | confirmed | Later owner records reinterpret the repository: the 2026-08-03 registry note calls it the "earlier Python/FastAPI predecessor ... never deployed ... superseded/shelved"; the 2026-08-06 dossier verdict is PARK / FIX; the rule-based estate audit says KILL ("under 500 logical lines and under 10 commits"). |
| `ha-c10` | 2026-09-04 | behavioral | verified | confirmed | The GitHub repository is public, has no licence file, no topics, no issues, pull requests, releases or tags, and has not been pushed since 2026-03-26T06:11:05Z; local master equals origin/master. |
| `ha-c11` | 2026-07-20 | behavioral | inferred | plausible | The tracked bytecode file was regenerated locally on 2026-07-20 (file mtime 19:49 local), the same day the owner's ship queue scheduled "hydra-api (Render)"; main.py was therefore imported or run locally that day under CPython 3.12. |
| `ha-c12` | 2026-09-02 | contemporaneous | verified | confirmed | The September 2026 credential purge examined this history, matched only "public configuration / placeholder" pattern classes (RETAINED_PUBLIC_CLASS), confirmed no secret, and did not rewrite or force-push it. |
| `ha-c13` | 2026-04-03..2026-09-04 | inferred | unknown | unknown | Whether a RapidAPI listing for HYDRA (in any form) was ever created is unknown: the Worker README asserts "Listed for marketplace discovery", no repository, portfolio, audit or marketing document evidences a listing, and the RapidAPI dashboard was not consulted. |
| `ha-c14` | 2025-08-18..2026-03-26 | behavioral | verified | confirmed | NoHustle API (2025-08-18..21) shares this project's author, its RapidAPI-marketplace thesis and its Render-first hosting habit, but shares no route, no distinctive literal, no dependency beyond the language, and neither repository, nor any portfolio document, references the other. |
| `ha-c15` | 2026-03-26 | inferred | inferred | plausible | HYDRA's design inverts every point where NoHustle stalled — heavy ML dependencies became zero dependencies, SQLite usage analytics became statelessness, API keys and paid tiers became keyless and free, BSL 1.1 became MIT, and Render became the edge — which reads as a lesson learned, but no source states that intent. |
| `ha-c16` | 2026-03-26..2026-09-04 | direct | verified | confirmed | The endpoint count is stated inconsistently across the family: this README says "20+", the Worker README and GitHub description say 22, the live Worker banner hard-codes 20, and the code in both repositories has 24 utility routes. |
| `ha-c17` | 2026-03-26..2026-04-03 | direct | verified | confirmed | FastAPI's generated Swagger (/docs) and ReDoc (/redoc) pages were part of this design; the Worker port has no equivalent and compensated eight days later with a hand-written openapi.json and an HTML playground. |
| `ha-c18` | 2026-09-04 | behavioral | verified | confirmed | The lead's dispatch brief recorded this repository's dirty baseline as ".env.example" and hydra-worker's as the bytecode/.claude/.toledo.yaml set; the working trees show the reverse — this repository carries the modified bytecode, the untracked .claude/settings.local.json and the untracked .toledo.yaml, while hydra-worker is clean. |
| `ha-c19` | 2026-08-16 | behavioral | inferred | plausible | An agent permissions file (.claude/settings.local.json allowing two Gmail MCP tools) appeared in the checkout on 2026-08-16, showing an AI-assistant session was opened in this directory that day; no commit followed. |
| `ha-c20` | 2026-04-03..2026-09-04 | behavioral | verified | confirmed | The Worker, not this service, became the deployed HYDRA surface: the Worker README of 2026-04-03 already publishes a live workers.dev URL and "$0 on Workers free tier", and it still answers 200 on 2026-09-04. |
| `ha-c21` | 2026-03-26 | direct | verified | strongly_supported | The three-dependency posture (fastapi 0.115.6, uvicorn 0.34.0, pydantic 2.10.4) and standard-library-only utilities were deliberate design, matching the "zero dependencies beyond Hono" line the Worker later advertised. |
| `ha-c22` | 2026-06-05..2026-08-06 | retrospective | verified | confirmed | The workspace registry, marketing-machine documents and asset-sale kit treat "hydra" as one product (the Worker) and never name this repository; its only independent mentions after April are inventory rows and audit dossiers. |
| `ha-c23` | 2026-01-17 | retrospective | verified | confirmed | Nine weeks before this repository existed, the owner's 2026-01-17 codebase audit still rated NoHustle API "Production-Ready", proposed merging it with TallySec and ComplyCrawl into one backend, and priced it as a "$5-50/mo per user" SaaS utility API; HYDRA was nonetheless started from zero with none of that code, in a different framework, free and keyless. |

## Appendix B — Contradiction register

### `hydra-api-x1` — Is this repository HYDRA's predecessor or a parallel variant of the Worker?

- Disagreement kind: chronology
- Account (src-git-hydra-api, src-git-hydra-worker; 2026-03-26; contemporaneous machine record): The FastAPI root commit precedes the Worker root commit by 75 minutes and the Worker's own banner links back here as its docs.
- Account (src-git-hydra-worker, src-tc-master-portfolio; 2026-04-03; author, eight days after the event): 'Also Available: Python/FastAPI version' and, in June, 'a parallel Python/FastAPI variant for a possible RapidAPI listing' — a sibling, not an ancestor.
- Account (src-tc-registry-hydra; 2026-08-03; agent-written, four months later): 'earlier Python/FastAPI predecessor, same feature set, targeting Render, never deployed ... Superseded/shelved.'
- Best-supported reading (strongly_supported): Chronologically the predecessor by 75 minutes and functionally the origin of the Worker's code; strategically a parallel variant kept for Python readers and a marketplace listing that never materialised. "Superseded" describes the deployment outcome, not a decision anyone recorded.
- Resolving evidence: The authoring session logs of 2026-03-26 or an owner statement about why two implementations were made the same night.

### `hydra-api-x2` — Was this service deployed to Render?

- Disagreement kind: outcome
- Account (src-git-hydra-api; 2026-03-26; contemporaneous): render.yaml declares a free web service with autoDeploy true, which reads as an intention to run it.
- Account (src-tc-root-reports-2026-07; 2026-07-20; owner-side planning, four months later): 'hydra-api ... ship_now ... Render -> Blueprint -> connect ... 20m' — still a to-do.
- Account (src-tc-audit-2026-08, src-live-probe; 2026-08-06; measurement): hydra-toolkit-api.onrender.com returns 404 with x-render-routing no-server (also on 2026-09-04).
- Best-supported reading (strongly_supported): Never deployed. Every dated record after the blueprint treats deployment as future work, and no probe ever found a service.
- Resolving evidence: The Render dashboard's service list and event history for the owner's account.

### `hydra-api-x3` — Is this a revenue asset?

- Disagreement kind: interpretation
- Account (src-tc-meta-inventory-2026-05; 2026-05-05; owner tooling): .toledo.yaml: type revenue.
- Account (src-git-hydra-api, src-tc-audit-2026-08; 2026-08-06; code and measurement): No auth, no billing, no key; "labeled revenue but has no billing/auth and gives everything away free."
- Best-supported reading (confirmed): The label records an aspiration (a possible RapidAPI freemium listing) that the code never implemented; as built it is a free reference implementation.
- Resolving evidence: A RapidAPI listing with a paid tier, or a code change adding metering.

### `hydra-api-x4` — How many endpoints does HYDRA have?

- Disagreement kind: fact
- Account (src-git-hydra-api; 2026-03-26; contemporaneous): README: '20+ endpoints'; code: 24 utility routes.
- Account (src-git-hydra-worker; 2026-04-03; contemporaneous): README badge and GitHub description: 22; live banner hard-codes 20.
- Best-supported reading (confirmed): 24 utility routes plus two meta routes in both implementations; the published numbers are marketing approximations that were never reconciled.
- Resolving evidence: none needed; a README correction would close it.

### `hydra-api-x5` — What was this repository's uncommitted baseline when the history reconstruction began?

- Disagreement kind: fact
- Account (src-leaf-brief-2026-09-04; 2026-09-04; lead agent's dispatch record): backburner/hydra-api: ' M .env.example'; active/hydra-worker: the bytecode/.claude/.toledo.yaml set.
- Account (src-worktree-2026-09-04; 2026-09-04; direct measurement): hydra-api: ' M __pycache__/main.cpython-312.pyc', '?? .claude/', '?? .toledo.yaml'; hydra-worker clean; there is no .env.example in this repository.
- Best-supported reading (confirmed): The brief cross-wired the two HYDRA repositories' baselines; the measured state is authoritative and was preserved untouched.
- Resolving evidence: none needed; recorded so an automated verifier run with the brief's baseline is explicable.

### `hydra-api-x6` — What should become of this repository?

- Disagreement kind: interpretation
- Account (src-tc-estate-audit-2026-08; 2026-08-06; rule-generated verdict): KILL — trivial: under 500 logical lines and under 10 commits.
- Account (src-tc-audit-2026-08; 2026-08-06; agent judgement): PARK / FIX — point the public README at the live Worker and delete the stale render.yaml/.pyc, or make it private; drop the revenue label or add metering.
- Account (src-tc-registry-hydra; 2026-08-03; agent judgement): Superseded/shelved.
- Best-supported reading (plausible): A dormant reference copy whose only distinctive value is the generated Swagger/ReDoc documentation and Python readability; none of the verdicts has been acted on.
- Resolving evidence: An owner decision recorded as a history event.

## Appendix C — Source inventory

| Source | Kind | Class | Access | Retrieved | Locator |
|---|---|---|---|---|---|
| `src-git-hydra-api` | git repository (this project) | direct | accessible | 2026-09-04 | https://github.com/ntoledo319/hydra-toolkit-api.git |
| `src-git-hydra-worker` | git repository (related; canonical HYDRA implementation) | direct | accessible | 2026-09-04 | https://github.com/ntoledo319/hydra-worker.git |
| `src-git-nohustle` | git repository (related; thematic predecessor) | direct | accessible | 2026-09-04 | https://github.com/ntoledo319/NoHustle-API.git |
| `src-git-hydra-site` | git repository (related; retired static mirror) | direct | accessible | 2026-09-04 | https://github.com/ntoledo319/hydra-site.git |
| `src-git-thing` | git repository (related; NoHustle growth kit, 2025-08-22..29) | direct | accessible | 2026-09-04 | https://github.com/ntoledo319/spidermind-omega.git |
| `src-git-toledo-command` | git repository (owner's private control-plane / portfolio index) | retrospective | accessible | 2026-09-04 | /home/nick/Development/toledo-command |
| `src-gh-metadata` | GitHub REST metadata via authenticated gh (read-only) | external | accessible | 2026-09-04 | gh api repos/ntoledo319/{hydra-toolkit-api,hydra-worker,NoHustle-API,hydra-site} |
| `src-live-probe` | read-only HTTP GET probes of public URLs | behavioral | accessible | 2026-09-04 | https://hydra-toolkit-api.onrender.com/health ; https://hydra-worker.toledonick98.workers.dev/ ; https://nohustle-api.onrender.com/health |
| `src-worktree-2026-09-04` | uncommitted working-tree state at audit time | behavioral | accessible | 2026-09-04 | git status --porcelain -uall (M __pycache__/main.cpython-312.pyc; ?? .claude/settings.local.json; ?? .toledo.yaml) |
| `src-tc-master-portfolio` | owner portfolio document (toledo-command/MASTER-PORTFOLIO.md, section HYDRA) | retrospective | accessible | 2026-09-04 | /home/nick/Development/toledo-command/MASTER-PORTFOLIO.md |
| `src-tc-registry-hydra` | owner asset registry note (toledo-command/registry/assets/hydra.md) | retrospective | accessible | 2026-09-04 | /home/nick/Development/toledo-command/registry/assets/hydra.md |
| `src-tc-audit-2026-08` | owner asset audit dossiers (toledo-command/audit-2026-08/assets/*.md, 03-TRUTH-VS-CLAIMS.md) | retrospective | accessible | 2026-09-04 | /home/nick/Development/toledo-command/audit-2026-08/assets/backburner-hydra-api.md |
| `src-tc-estate-audit-2026-08` | owner estate audit (toledo-command/estate-audit-2026-08/**) | retrospective | accessible | 2026-09-04 | /home/nick/Development/toledo-command/estate-audit-2026-08/assets/backburner-hydra-api.md |
| `src-tc-root-reports-2026-07` | owner root reports (SHIP-QUEUE-2026-07-20, VALUE-AUDIT-GROUND-TRUTH-2026-07-20, DEEP-RESEARCH-2026-07-22) | retrospective | accessible | 2026-09-04 | /home/nick/Development/toledo-command/archive/root-reports-2026-07/ |
| `src-tc-meta-inventory-2026-05` | workspace migration records (migration-log.txt, migration-plan.md, inventory-summary.md) | contemporaneous | accessible | 2026-09-04 | /home/nick/Development/toledo-command/archive/_meta-inventory-2026-05/ |
| `src-tc-workspace-registry` | workspace registry and overrides (registry.json, project-overrides.json, ROOT-LAYOUT.md, registry/REPOS.md) | retrospective | accessible | 2026-09-04 | /home/nick/Development/toledo-command/workspace/ |
| `src-marketing-arm` | marketing-machine strategy docs (marketing-arm/portfolio.yml, KILL-LIST.md; toledo-command/strategy/marketing-machine/*) | retrospective | accessible | 2026-09-04 | /home/nick/Development/marketing-arm/portfolio.yml |
| `src-business-ops` | business-ops strategy hub (EXECUTIVE-SUMMARY.md, TOLEDO-CAPABILITIES.md, assets-for-sale/*) | retrospective | accessible | 2026-09-04 | /home/nick/Development/business-ops/assets-for-sale/MASTER-ASSET-INVENTORY.md |
| `src-icloud-ttllc-status` | owner status trackers synced from iCloud (DECISION_LOG, ASSETS_TRACKER, PRODUCT_CATALOG, MASTER_PORTFOLIO_TRACKER) | retrospective | accessible | 2026-09-04 | /home/nick/Development/active/Mind/60 Sources/iCloud/Documents — TTLLC Status docs — * |
| `src-icloud-mycodemine-reports` | owner codebase-audit reports synced from iCloud (MyCodeMine REPORTS 00_EXEC_SUMMARY, 01_REPO_CATALOG, 07_APP_IDEAS_RANKED, 08_TOP_3_EXECUTION_PLANS) | retrospective | accessible | 2026-09-04 | /home/nick/Development/active/Mind/60 Sources/iCloud/App — MyCodeMine — REPORTS — 00_EXEC_SUMMARY.md |
| `src-purge-2026-09` | credential-purge records (SECURITY_CLEANUP_REPORT.md; .unlazy/credential-cleanup/verification/*.json) | contemporaneous | accessible | 2026-09-04 | /home/nick/Development/SECURITY_CLEANUP_REPORT.md |
| `src-leaf-brief-2026-09-04` | lead agent's dispatch brief and PLAN.md baseline record for this reconstruction | contemporaneous | accessible | 2026-09-04 | /home/nick/Development/.unlazy/project-history/PLAN.md |
| `src-inaccessible-render-dashboard` | Render dashboard / deploy logs for hydra-toolkit-api | external | inaccessible | — | https://dashboard.render.com (owner account; not opened) |
| `src-inaccessible-rapidapi` | RapidAPI provider dashboard / listing state | external | inaccessible | — | https://rapidapi.com (owner account; not opened) |
| `src-inaccessible-authoring-sessions` | local AI-assistant session logs from the 2026-03-26 build (CascadeProjects directory suggests Windsurf/Cascade) | external | inaccessible | — | /Users/nicholastoledo/CascadeProjects (former macOS path; directory unlinked 2026-05-05 per migration log) |

## Appendix D — Coverage and reproducibility

- **repository:** ntoledo319/hydra-toolkit-api
- **audit_date:** 2026-09-04
- **full_audit_anchor:** 0106964e92fa29d6a9cde46fa652839cb282b302
- **incremental_anchor:** 0106964e92fa29d6a9cde46fa652839cb282b302
- **reachable_commit_count:** 3
- **refs_examined:**
  - refs/heads/master
  - refs/remotes/origin/master
- **exclusion_counts:**
  - commits_total: 3
  - commits_deep_read: 3
  - binary_diffs_not_inspected: 1
  - generated_or_vendored_files_skipped: 0
  - history_only_commits: 0
  - uncommitted_paths_treated_as_present_tense: 3
- **source_classes:**
  - direct: 5
  - contemporaneous: 3
  - retrospective: 11
  - behavioral: 2
  - external: 4
  - inferred: 0
- **inaccessible_sources:**
  - Render dashboard and deploy logs for hydra-toolkit-api (would settle whether a service was ever created)
  - RapidAPI provider account (would settle whether any HYDRA listing exists)
  - AI-assistant authoring session of 2026-03-26 in the former CascadeProjects directory (would reveal intent behind the same-night port)
  - Any pre-repository design notes; none were found in the owner's synced documents
- **evidence_gaps:**
  - Why two implementations were made the same night is inferred from timing and code identity, never stated.
  - The reason the Worker won as the deployed surface is inferred from the Worker's marketing copy (cost, latency), not from a decision record.
  - Whether the 2026-07-20 local bytecode regeneration was a deploy attempt is inferred from a file mtime.
  - The purpose of the 2026-08-16 assistant session in this directory is unknown.
  - Whether a RapidAPI listing ever existed is unknown.
- **rewritten_history:** no — the September 2026 credential purge classified this history as containing only public-configuration pattern matches, performed no rewrite, and origin/master still equals local master; nothing in the reachable graph shows force-push or rebase evidence
- **coverage_matrix:**
  - eras:
    - era: prehistory (SPECTRUM-lite/NoHustle 2025-08 and the unrecorded idea before 2026-03-26)
    - git: related repositories fully read
    - docs: owner reports read
    - external: GitHub metadata read
    - gaps: origin of the idea and the authoring prompt unrecorded
    - era: the one-night build (2026-03-26)
    - git: 3 of 3 commits deep-read
    - docs: README read
    - external: GitHub creation and push timestamps read
    - gaps: intent behind the port inferred
    - era: dormancy and reinterpretation (2026-04..2026-09)
    - git: no commits; working tree read
    - docs: portfolio, audit, ship-queue, marketing and registry records read
    - external: live probes and GitHub metadata
    - gaps: no Render/RapidAPI account evidence
- **completeness_statement:** All reachable Git objects and every dated owner document mentioning this project were reviewed. That is not the same as knowing the project's full history: the design was made inside an AI-assisted session whose transcript is unavailable, the deployment platforms were not consulted, and the only account of intent is the code itself plus later, agent-written retrospectives.

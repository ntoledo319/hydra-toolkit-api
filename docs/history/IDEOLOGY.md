# Ideology — the worldview this code reveals

_"Ideology" here means the project's governing assumptions, priorities, non-negotiables, theory of the problem, intended beneficiaries, definition of success, acceptable trade-offs and revealed non-goals. Nothing below is manufactured from motive; where the code is the only witness, that is said._

## Theory of the problem

Developers spend small, repeated units of attention on utilities that are individually trivial and collectively tedious. The remedy is not a library — libraries must be installed, versioned and learned — but a **public HTTP surface** that answers a typed request with a JSON answer and documents itself. The unit of value is the endpoint; the unit of trust is the readable source. Both are visible in the first commit and nowhere restated (`ha-c01`, `ha-c06`).

## Theory of change

Publish everything, charge nothing, require nothing. Adoption, if it comes, comes from discovery (a marketplace listing, a README, a playground) rather than from sales. This is stated only later and only for the Worker — "intended top-of-funnel dev surface + a freemium RapidAPI candidate" (2026-06-23, `ha-c08`) — and the "freemium" half was never built anywhere in the family.

## Intended beneficiaries over time

1. **2026-03-26:** anonymous developers (wildcard CORS, no key) and the studio's own portfolio ("Built by Toledo Technologies LLC").
2. **2026-04-03:** readers who prefer Python — the Worker README lists this as the "Python/FastAPI version" (`ha-c08`).
3. **2026-05 to 2026-08:** the owner and the agents that operate the portfolio; the repository exists in their records as an inventory row, a ship-queue item, a dossier (`ha-c07`, `ha-c09`, `ha-c22`).

The beneficiary drifted from users to bookkeeping without a single change to the code.

## Principles (versioned in `.project-history/doctrine/principles.yml`)

| Principle | Status | Revealed by |
|---|---|---|
| `p-one-file-stateless` v1 — one file, no database, no state, no outbound calls; every handler a pure function of its request | active | `main.py` structure; absence of storage or HTTP clients |
| `p-keyless-free` v1 — no API key, no billing, open CORS | **challenged** since 2026-05-05 by the `type: revenue` label and the June "freemium candidate" framing, neither of which changed the code | `CORSMiddleware(allow_origins=["*"])`; no auth dependency |
| `p-minimal-deps` v1 — three pinned framework dependencies and the standard library | active | `requirements.txt`; `hashlib`/`re`/`json`/`difflib`/`urllib` in `main.py` (`ha-c21`) |
| `p-self-documenting` v1 — typed models with field descriptions feed generated Swagger and ReDoc | active | `FastAPI(docs_url="/docs", redoc_url="/redoc")`, pydantic `Field(description=…)` (`ha-c17`) |
| `p-render-first-hosting` v1 — host on Render's free plan from a blueprint with auto-deploy | **superseded** the same night by the edge-first principle enacted in `hydra-worker` | `render.yaml` (`ha-c03`) |

No principle has a version 2. That is itself the finding: the doctrine froze at 02:11 EDT on 2026-03-26.

## Non-goals and negative space

Revealed by absence — none is written anywhere:

- **No authentication, metering or rate limiting.** Not stubbed, not commented, not in the README's future tense. The only later mention of metering is by auditors recommending it (`ha-c09`).
- **No persistence.** No database, no file writes, no cache. NoHustle's SQLite usage analytics have no descendant here.
- **No heavy processing.** Nothing that needs a model, a binary or more memory than a request; NoHustle's `rembg`/`pdfplumber`/`pandas` stack has no descendant here.
- **No tests.** The Worker at least kept a template test; this repository has none.
- **No licence.** The Worker chose MIT in text and, from 2026-09-01, in a file; this repository never chose.

## Recurring tensions

1. **Free versus revenue.** The code gives everything away; the manifest and every strategy document call it a revenue asset or a freemium candidate; the marketing gate fails it for having no price. The tension was recorded on both sides and resolved on neither (`hydra-api-x3`).
2. **Readability versus reach.** The Python file is the more readable and better-documented implementation; the Worker is the one that runs everywhere for free. Readability lost the deployment and kept the `docs` link.
3. **Intent versus decision.** A blueprint with `autoDeploy: true` is an intent to run. Nothing turned it into a service, and nothing turned it off; it sits in a public repository as a live-looking configuration for a dead URL (`ha-c05`).
4. **Public versus dormant.** The repository is one of the estate's few public ones. Every reviewer asks whether that is wanted; nobody answered.
5. **Rule versus judgement.** The estate audit's KILL rule ("under 500 lines and under 10 commits") condemns this repository and the live Worker alike; the judgement-based dossier says PARK; the registry says shelved (`hydra-api-x6`).

## Stated ideals versus revealed behaviour

- *Stated:* "20+ endpoints" (README, commit message, FastAPI title). *Revealed:* 24 utility routes plus two meta routes; the family later published 22 and 20 for the same code (`ha-c16`). The number was never counted — it was a slogan.
- *Stated (by the Worker):* "Python/FastAPI version — also available". *Revealed:* never available at any URL (`ha-c05`).
- *Stated (by the manifest):* `type: revenue`. *Revealed:* no mechanism; no price; no listing evidenced (`ha-c07`, `ha-c13`).
- *Stated (by the blueprint):* deploy on push. *Revealed:* no push after the blueprint (`ha-c10`).

## What the project refused to become

A second NoHustle. Every axis on which NoHustle was heavy — dependencies, state, keys, tiers, licence restrictions, host-specific fixes — is light or absent here. The refusal is visible in the code with **confirmed** confidence; that it was a *conscious* refusal is **plausible** and unproven (`ha-c15`).

## Evolution

There was none inside the repository. Outside it, the ideology of the *family* moved from "free edge utility" (April) to "freemium candidate" (June) to "set a price or shelve it" (June, marketing gate) to "park, fix or kill" (August). This repository's doctrine is a snapshot of the first position; the pressure to change it has been recorded four times and answered zero times.

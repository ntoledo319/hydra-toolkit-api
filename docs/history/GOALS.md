# Goals — every goal, its lifecycle and what "success" meant

_Versioned lifecycle records live in `.project-history/doctrine/goals.yml`. Status vocabulary: proposed → active → narrowed / expanded / blocked → achieved / abandoned / superseded. Dates are decision or observation dates, not commit dates, unless stated._

## `g-ship-toolkit-v1` — ship a working "20+ endpoint" developer utility API in one sitting

- **Proposed / activated:** 2026-03-26, revealed by the root commit's subject line and the FastAPI title (`ha-c01`).
- **Definition of success at the time:** every route answers locally; the generated docs page lists them all. The only bug fix (89 seconds later) and the committed bytecode show the code was run (`ha-c02`).
- **Status: achieved** the same night. The measure that would have exposed the count problem — actually counting — was never applied (`ha-c16`).
- **Consequence:** the goal's completeness made the code portable, and portability made this copy expendable.

## `g-render-free-deploy` — run the service on Render's free plan from the blueprint

- **Proposed / activated:** 2026-03-26 02:11 EDT with `render.yaml` (`ha-c03`).
- **Definition of success:** a live `onrender.com` URL answering `/health`.
- **Blocked / overtaken:** seventeen minutes later by the Worker port (`ha-c04`).
- **Still listed as work:** the 2026-07-20 ship queue scheduled "Render → Blueprint → connect — 20m" for week three; the 2026-07-22 research note listed it under "ready-but-unshipped (need your accounts)"; the bytecode was regenerated the same day (`ha-c05`, `ha-c11`).
- **Status: abandoned** — by outcome, not by any written decision. Every probe (2026-08-06, 2026-09-04) found no service.
- **What could revive it:** connecting the blueprint takes minutes; what is missing is a reason, since the Worker already serves the same routes for free.

## `g-python-reference` — remain the Python/FastAPI reference for readers who prefer Python or want generated Swagger/ReDoc

- **Proposed:** 2026-04-03, when the Worker README listed this repository under "Also Available" (`ha-c08`).
- **Definition of success:** the repository stays readable, public and linked from the Worker as the Python version.
- **Status: active** (review by 2026-12-31). It is met in the weakest sense: the link exists and the code is unchanged. It is undermined by the same facts every auditor lists — a dead blueprint, committed bytecode, no licence, no tests.
- **Tension:** this is the only goal that argues for keeping the repository at all, and it was never stated by the owner; it is inferred from the README link and from the Worker's lack of generated docs (`ha-c17`).

## `g-rapidapi-listing` — offer HYDRA on RapidAPI for marketplace discovery, possibly as a freemium tier

- **Proposed:** 2026-04-03 ("RapidAPI: Listed for marketplace discovery", Worker README) and 2026-06-23 ("a possible RapidAPI listing", master portfolio) (`ha-c08`).
- **Definition of success (supplied later by the marketing-machine documents):** a published listing with at least a free tier and a decided price.
- **Status: blocked** since 2026-06-17 on gate G1, "no price set"; a business-model decision the documents explicitly refuse to treat as a one-click fix. Whether any listing was ever created is unknown (`ha-c13`).
- **Which repository was meant:** the June portfolio ties the listing to *this* Python variant; every later document ties "hydra" to the Worker. The ambiguity is preserved in `hydra-api-x1`.

## `g-revenue-classification` — be a revenue asset (the manifest's `type`)

- **Proposed:** 2026-05-05 by the migration tooling's generated `.toledo.yaml` (`ha-c07`).
- **Definition of success:** any paid usage or a listed price.
- **Status: blocked.** No auth, metering or billing exists in code; the 2026-08-06 dossier calls the label "aspirational, not real revenue" (`ha-c09`, `hydra-api-x3`).
- **Alternative named by the documents:** drop the label and treat HYDRA as a lead/backlink asset. Not chosen either.

## Goals that were never proposed

Worth recording because their absence is a choice: a test suite; a licence; a versioning or release scheme (the FastAPI `version="1.0.0"` never changed and there are no tags); reconciling the endpoint count; a custom domain; rate limiting or abuse protection for a public no-key API. The Worker's history shows several of these surfacing as audit findings in July–August 2026; none surfaced here.

## How the definition of success moved

| When | Success meant | Who said so |
|---|---|---|
| 2026-03-26 | it runs, the docs list everything | the code (`ha-c01`, `ha-c02`) |
| 2026-03-26 02:11 | a live Render URL | `render.yaml` (`ha-c03`) |
| 2026-04-03 | "also available" next to a live Worker | Worker README (`ha-c08`) |
| 2026-06-17 | a decided price | marketing gate G1 (`ha-c13`) |
| 2026-06-23 | a possible RapidAPI listing | master portfolio (`ha-c08`) |
| 2026-08-06 | a credibility fix: README → Worker, delete blueprint/bytecode, or go private | dossier (`ha-c09`) |

The repository met the first and none of the rest.

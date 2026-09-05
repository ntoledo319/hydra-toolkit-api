# Open questions, gaps and low-confidence claims

_Ranked by how much an answer would change the record. "No evidence found" is never treated as "did not happen"; each entry names what was searched and what would settle it._

## Ranked questions

1. **Why were two implementations made the same night, and why did the edge win?** The only witnesses are commit timestamps and the Worker's later marketing copy. Searched: both repositories' full histories, every owner document naming HYDRA, the migration logs. Would settle it: the AI-assisted authoring session of 2026-03-26 (former `CascadeProjects` directory; inaccessible) or one sentence from the owner. Affects `ha-c15` (plausible), contradiction `hydra-api-x1`, principle `p-render-first-hosting`'s supersession note.
2. **Was a Render service ever created from the blueprint, then deleted?** Every probe says `no-server`; the ship queue and research note of July 2026 treat it as undone. Searched: probes on 2026-08-06 and 2026-09-04, all dated owner records. Would settle it: the Render dashboard's service list and event history (a business-ops note of 2026-06-22 records that the Render workspace could not be enumerated by tooling). Affects `ha-c05` (strongly supported, not confirmed), `hydra-api-x2`.
3. **Does any RapidAPI listing for HYDRA exist, and for which implementation?** The Worker README asserts one; no document, listing copy or traffic corroborates it; the June portfolio attaches the possibility to this Python variant. Would settle it: the RapidAPI provider account. Affects `ha-c13` (unknown), goal `g-rapidapi-listing`.
4. **Which verdict does the owner accept — park, fix, kill, or keep as reference?** Three agent-written opinions, zero recorded decisions. Would settle it: an event capsule recording the choice. Affects event `hydra-api-2026-08-06-audits-park-fix` (open), `hydra-api-x6`, goal `g-python-reference`.
5. **Was the 2026-07-20 bytecode regeneration a deploy attempt?** A file mtime coinciding with the ship-queue date. Would settle it: shell history or Render build logs. Affects `ha-c11` (plausible).
6. **What was the 2026-08-16 assistant session for?** A permissions file appeared; no commit followed. Would settle it: the session transcript. Affects `ha-c19` (plausible).
7. **Where did the endpoint list come from?** A prompt, a competitor's feature list, or NoHustle's leftovers? Nothing in the tree or the owner's documents says. Affects the prehistory paragraph of `NARRATIVE.md` only.
8. **Did the owner ever intend this repository, rather than the Worker, to be the RapidAPI artifact?** One document implies it (2026-06-23); none repeats it. Affects `hydra-api-x1`.

## Contradictions carried in the register (`.project-history/contradictions.yml`)

- `hydra-api-x1` — predecessor or parallel variant (chronology; strongly supported reading: both, of different things).
- `hydra-api-x2` — ever deployed to Render (outcome; strongly supported: never).
- `hydra-api-x3` — revenue asset (interpretation; confirmed: label only).
- `hydra-api-x4` — endpoint count 20 / 20+ / 22 / 24 (fact; confirmed: 24 utility + 2 meta).
- `hydra-api-x5` — the dispatch brief's dirty baseline versus the measured one (fact; confirmed: measured state used).
- `hydra-api-x6` — what should become of the repository (interpretation; plausible: dormant reference copy).

## Low-confidence claims to keep visible

- `ha-c11` (plausible, inferred) — bytecode regeneration as a deploy attempt.
- `ha-c13` (unknown) — existence of a RapidAPI listing.
- `ha-c15` (plausible, inferred) — HYDRA as a deliberate inversion of NoHustle.
- `ha-c19` (plausible, inferred) — purpose of the 2026-08-16 session.

## Evidence gaps and lost or inaccessible sources

- The 2026-03-26 authoring session (former macOS `CascadeProjects` path, unlinked 2026-05-05).
- Render dashboard and deploy logs for `hydra-toolkit-api`.
- RapidAPI provider account state.
- Any pre-repository design note; none exists in the owner's synced documents (searched only for the project's names).
- The committed `__pycache__/main.cpython-312.pyc` binary was not disassembled; its content is assumed to match `main.py` at `58f61160f054a28da6573e37adadd943fd188e12`.

## Biases audited

- **Main-branch bias:** there is one branch; no never-merged work exists to be missed (`refs_examined` in `state.yml`).
- **Survivor bias:** the live Worker's account of the family was not allowed to define this repository; the June portfolio's "parallel variant" framing and the August "predecessor" framing are both preserved.
- **Recency and hindsight bias:** the August verdicts are labelled as opinions written five months after the event, by agents, and are not used to infer March intent.
- **Most-articulate-source bias:** the longest documents about HYDRA (dossiers, marketing blueprints) are retrospective and agent-written; the terse contemporaneous record (four commits, one README line) is given priority for what happened, and the long documents only for what was later believed.

## Coverage statement

All three reachable commits were deep-read (the binary `.pyc` excepted); both tracking refs examined; the related repositories (`hydra-worker`, `NoHustle API`, `hydra-site`, `experiments/thing`) read in full; every dated owner document naming HYDRA or NoHustle read for the relevant lines only. That is complete coverage of the available record and is not the same as knowing the project's full history: the design happened inside a session whose transcript is unavailable, and the only account of intent is the code plus later retrospectives. See Appendix D of `PROJECT_HISTORY.md` and `state.yml` for counts, exclusions and the coverage matrix.

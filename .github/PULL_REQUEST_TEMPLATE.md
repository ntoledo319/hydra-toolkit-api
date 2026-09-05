## Summary

<!-- What changed and why. -->

## History-impact declaration (required — exactly one)

Run `python3 scripts/project_history.py assess` and pick one:

- [ ] `history:recorded <event-id>` — event capsule added/amended under `.project-history/events/`, doctrine and `docs/history/` updated, `render` run, `validate` passes
- [ ] `history:none — <specific reason>` — immaterial change (say why; a bare skip is rejected by CI)
- [ ] `history:defer — <tracking item, owner, deadline YYYY-MM-DD>` — emergency/security work; deferral registered in `.project-history/policy.yml`

Declaration line (CI parses this):

```
history:
```

## Checks

- [ ] `python3 scripts/project_history.py validate`
- [ ] `python3 scripts/project_history.py render --check`
- [ ] `python3 -B -m unittest -q tests/test_project_history.py`
- [ ] No secrets, tokens, env values or personal data in any changed file

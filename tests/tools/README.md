# Claude's testing tools for the Mirror (test-only, never part of the site)

These are the scripts Claude uses to check each build before Karl sees it. They never run on aurasense.app.
Invented test words only; no one's real conversation, no keys. The self-test's private token is not here
(only its fingerprint is in the helper).

- `t_helper.mjs` — the listener helper with a pretend Claude (run with the token in `SELFTEST_TOKEN` for the self-test checks).
- `t_heavy.js` — the heavy-words list, tested both ways.
- `harness.py` + `t158.py`, `t163.py`, `t164.py` — the Mirror page walked in a real browser with a pretend helper.
- `chk.py` — page scripts checked, and stray invisible characters.
- `edit*.py` — each build's changes, always applied from the previous live files (re-runnable).

Kept here on 23 October 2026 because the project's document space was full.

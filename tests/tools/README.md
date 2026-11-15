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

## The Alphasense study (28 Oct 2026)

- `alphasense-study/`: the study "Alphasense One by One" (every chapter as a circle of dusk, one symbol at a time,
  sensed before it is named). `build_study.py` joins `template.html`, the site's own symbols, words and bonds
  (`alpha-data.json`, read from the live map page) and the site's two drawing functions (copied from
  `index-mapbox.html` at build time) into one page. It is a study, not part of the site.
- `t_alpha_study.py`: walks it at phone, small-phone and laptop sizes and with motion reduced (48 checks).
- When it moves into the map page: keep every sense id as it is (saved auras use them); show the three doubled
  senses once; turn the aura by turning its colours (a spinning square box widens a phone page).

## Build 171 · the open pages (14 November 2026)

- `open-pages/build_pages.py <site folder>`: writes `ledger.html` (drawn from `ledger.json`), `sense-before-you-sign.html`,
  `ambas.html`, `pledge.html` and `mutual-benefit.txt`. The four pages share one look and have no scripts at all.
  **To add a payment to the ledger:** add a row to `ledger.json` (`in` or `out`, with `date`, `kind`, exact `amount`,
  and optionally `note` or `named`), set `updated`, run the builder, copy `mutual-benefit.txt` to `.well-known/`, run `t171.py`.
  The builder refuses a ledger with more out than in, or an unknown kind.
- `open-pages/checklist-source.html` + `open-pages/make_pdf.py <source> <out.pdf>`: the six-page checklist (Lora and Inter;
  Letter size). The script also reports any page whose words run into the footer.
- `t171.py [site folder] [shots folder]`: walks `/`, `/ledger`, `/sense-before-you-sign`, `/ambas`, `/pledge` the way
  Cloudflare serves them (`/name` answers with `name.html`) at phone, small phone and laptop sizes and with motion reduced;
  checks links, tap sizes, sideways overflow, smallest words, colours, the ledger's sums on invented rows, the pledge file
  and the PDF. 454 checks.

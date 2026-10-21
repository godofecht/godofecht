# How this page is built

`README.md` contains a hand-maintained expanded Flow section. The original `gen_readme.py` generator does not yet reproduce that section; avoid regenerating the README without preserving its current content.

```
python3 gen_graph.py      # rebuild assets/graph-light.svg and assets/graph-dark.svg
python3 gen_readme.py     # rebuild README.md
```

The constellation graph reads live repository data through `gh` and Flow project/file totals from `FLOW_SOURCES.md`. The README generator reads live repository data through `gh`. The hand-written part is `spine.py`:
section titles, the blurb under each, and the one-line fact next to each repo.
A repo with no fact falls back to its GitHub description, so a repo with a bad
description shows up here as a bad line.

`gen_readme.py` refuses to write output containing an em dash, an en dash or a
curly quote.

A repo listed in `spine.py` that is not public is reported on stderr and left
out of the page.

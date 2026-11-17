# Locked Introduction v2 installation

Status: **INTRO_V2_INSTALLED**

Placement: **PAGE2_TOP_VERIFIED**

Date: 2026-11-17

The supplied Introduction was installed in the already imported
`sections/01_introduction.tex`, byte for byte. The supplied figure block was
installed as `fig/fig1_page2.tex`, with only the expressly allowed image-path
substitution to `figures/fig1.pdf`. No scientific prose or caption was rewritten.

There is exactly one active Introduction heading, `sec:intro` label,
`fig:teaser` label, and Figure 1 import. Counts exclude literal examples in
comments. No active page-one strip/teaser import existed in `main.tex`.
No page break, strip, captionof, margin change, spacing hack, or forced height
was added.

## Figure identity and author confirmation

The task initially specified Figure 1 SHA256
`e43de84978336f1f8c564c397c6d60f5c1a4902cf5eecd40acd52f63d8b0b895`.
The author explicitly approved using the repository's `clip_fig1.pdf` instead.
Its SHA256 is
`73662d384bba2851e9a6cef37bed4c359e52319cc4c6e4db99ec84aa31a63429`.
The stable tracked `figures/fig1.pdf` has identical bytes and is reused.

Figure 2 retains SHA256
`43898365c3584fcfa231c03cb6f4678011ac21db03541a728c723cdde38daa1f`.
Both PDFs, the official CVPR style/preamble/bibliography style, and all unrelated
tracked files are unchanged. The pre-existing Section 5 Figure 2 block was
preserved; this task did not insert another Figure 2 or invent its future label.

## Bibliography

The supplied `zhou2022coop` entry was appended exactly once to `main.bib`.
Its authors, title, venue, volume, issue, pages, year, and DOI were verified
against [Springer](https://doi.org/10.1007/s11263-022-01653-1) and Crossref.
The existing bibliography switch in `main.tex` was enabled so this verified
entry is actually used. No other bibliography entry was fabricated.

Seven distinct citation keys remain absent:
`chao2016gzsl`, `li2022ordinalclip`, `mai2024fine`,
`radford2021clip`, `wang2023l2rclip`, `wortsman2022robust`,
`zhou2022cocoop`. The final log has eight unresolved citation occurrences.

Expected pending references are `prop:cal` and `fig:matched_strength`.
They were not replaced with fake labels or prose.

## Compilation and visual inspection

With the author's installation authorization, TinyTeX v2026.11 / TeX Live 2026
and PyMuPDF 1.26.7 were installed in the ignored project tool directory.
The TinyTeX archive matched its official release SHA256. No research environment,
system package installation, shell profile, or credential configuration was changed.
The new isolated TeX manager needed its own update before installing the missing
`silence` package. A rebuild cleared the cached earlier dependency failure.

The prescribed command then returned exit code 0:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Build versions: latexmk 4.88, pdfTeX 1.40.29, BibTeX 0.99e.
The actual review PDF has **3 pages**. Pages 1 and 2 were rendered and visually
inspected: page 1 has no Figure 1; Figure 1 and its supplied caption appear at
the top of page 2 below the standard review header, with no body text above.
No clipping was observed. Anonymous review appearance and empty PDF Author
metadata were confirmed.

The final log has no fatal error, missing input, or overfull/underfull box warning.
The missing citations and two pending labels above remain visible as expected.
The final full-paper eight-page check is deferred until the other sections exist.

## Scope and preservation

Changed source paths are the imported Introduction, `fig/fig1_page2.tex`,
`main.bib`, and the bibliography-switch line in `main.tex`; this report is the
only additional published file.

Default `git diff --check` flags the literal blocks' trailing blank separator
lines. They are retained to preserve exact supplied bytes. The additional check
excluding only `blank-at-eof` passes; no whitespace normalization was applied.

Old Introduction/main/bibliography copies, literal comparison sources, full
build logs, rendered previews, source hashes, and final commit/push receipts
are retained under ignored local audit directories and are not committed.
No abstract, LLM statement, other chapter, experiment, plot, or source data was
written or changed. No GPU work was run. Stop after this installation.

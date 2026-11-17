# CVPR 2027 paper source

**Fixing the Score Is Not Fixing the Order:
Ordinal Transfer to Unseen Grades in Adapted CLIP**

This repository contains the P0 LaTeX initialization only: the frozen title,
six main sections, subsection skeletons, and a provisional administrative LLM
disclosure. The title/outline follow the author's subsequently supplied locked
writing blueprint. Scientific body text and captions remain unwritten.
The two author-supplied final PDFs are included unchanged; no results table or
unverified citation is initialized.

The official template is pinned to **CVPR2027-v1**, commit
`a2369342011145be8c85e5ad21a9b61f9fa53473`. The style, preamble, and bibliography
style are unchanged upstream copies; see `docs/TEMPLATE_PROVENANCE.json` and
`docs/TEMPLATE_SHA256SUMS.txt`.

The root `main.tex` uses anonymous review mode. Local compilation is
**READY_FOR_OVERLEAF_COMPILE_NOT_LOCALLY_VERIFIED** because the local TeX
toolchain is unavailable. This is not a completed or submission-ready paper.

```text
main.tex
preamble.tex
cvpr.sty
ieeenat_fullname.bst
main.bib
sections/
  00_abstract.tex
  01_introduction.tex
  02_related_work.tex
  03_calibration_ranking.tex
  04_tie.tex
  05_experiments.tex
  06_conclusion.tex
  90_llm_usage_statement.tex
figures/README.md
figures/fig1.pdf
figures/fig2.pdf
tables/README.md
supplementary/supplementary.tex
docs/
  CVPR2027_FORMAT_CHECKLIST.md
  PAPER_STRUCTURE.md
  FIGURE_ASSET_STATUS.md
  FIGURE_ASSET_PROVENANCE.json
  OVERLEAF_SYNC.md
  TEMPLATE_PROVENANCE.json
  TEMPLATE_SHA256SUMS.txt
  UPSTREAM_SHA256SUMS.txt
```

With an existing TeX installation, compile from the repository root:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

For Overleaf, import tracked sources and select root `main.tex` with pdfLaTeX;
see `docs/OVERLEAF_SYNC.md`. Figure 1 and Figure 2 are enabled at full text
width, with empty captions pending author text. Their original hashes,
source-level PDF checks, and rendering limitations are recorded in
`docs/FIGURE_ASSET_PROVENANCE.json`. The separate frozen terminology file
remains unavailable; the received narrative blueprint does not replace it.

Bibliography is disabled until actual verified citations exist. Supplementary
material is disabled by default. Neither switch changes the six-section outline.
The LLM disclosure must be completed and verified by the authors before submission.

Only manuscript source, necessary official template files, approved final figure
assets, and sanitized project documentation belong here. Local initialization
receipts, server paths, datasets, checkpoints, raw predictions, and internal
research handoffs are excluded from Git.

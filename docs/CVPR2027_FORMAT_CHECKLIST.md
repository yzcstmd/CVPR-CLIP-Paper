# CVPR 2027 format checklist

Sources checked:

- [Official Author Guidelines](https://cvpr.thecvf.com/Conferences/2027/AuthorGuidelines),
  especially Paper formatting and LLM Policy.
- [Official author-kit CVPR2027-v1](https://github.com/cvpr-org/author-kit/tree/CVPR2027-v1),
  commit `a2369342011145be8c85e5ad21a9b61f9fa53473`.
- Pinned `main.tex`, `preamble.tex`, `cvpr.sty`, `sec/1_intro.tex`,
  `sec/2_formatting.tex`, `sec/X_suppl.tex`, bibliography style, and build workflow.

`STATIC_PASS` means source inspection only. It does not certify a compiled PDF.

| Check | Official requirement / implementation | P0 outcome |
|---|---|---|
| 1. Class and paper | `article`, `10pt,twocolumn,letterpaper`; native style dimensions | STATIC_PASS |
| 2. Review mode | `\usepackage[review]{cvpr}`; anonymous title block and review rulers | STATIC_PASS; PDF not verified |
| 3. Main length | At most eight pages including figures/tables | Rule recorded; page count unknown |
| 4. Reference pages | Cited references excluded from the main-page limit | Conditional bibliography prepared; no entries fabricated |
| 5. LLM statement | Required after main text and before references; excluded from limit | Section present; truthful P0 disclosure, author completion required |
| 6. Captions | 9pt Roman; figures below, tables above; native caption setup | No overrides; assets pending |
| 7. Headings | Native numbered section/subsection commands and template fonts | Six sections and frozen subsections present |
| 8. Images | PDF/PNG/JPEG supported by the recommended pdfLaTeX route; vector PDF preferred for final plots | No active missing image inputs; final PDFs deferred |
| 9. Anonymity | No identifying authors, affiliations, acknowledgments, or identifying material in review PDF | Anonymous source; blank PDF author metadata |
| 10. Supplement | Official page break, page reset and `\maketitlesupplementary` | Optional input fragment disabled in the main review build |
| 11. Compiler/packages | pdfLaTeX through `latexmk -pdf`; BibTeX when real citations exist | Tools absent locally; no system installation performed |
| 12. Citations | Numeric `natbib` with sorting/compression; `ieeenat_fullname.bst`; `hyperref` after preamble; native `cleveref` | Sources wired; runtime/BibTeX unverified |

## Source differences and implementation decisions

The tagged example has sample authors and fictional bibliography entries.
They are not paper content: the skeleton uses Anonymous Authors and an empty,
comment-only `main.bib`. The bibliography switch remains off until real citations
exist, avoiding an empty BibTeX run. No citation correctness is asserted.

The tagged example does not contain the mandatory LLM Usage Statement described
by the current conference website. The skeleton adds the required unnumbered
section in that position, without modifying `cvpr.sty`. Its unfinished status
must be resolved by the authors before submission.

The exact author-frozen title and heading wording are preserved. The template
prose recommends sentence-case headings, while the supplied outline uses title
case; this copyediting difference is recorded for author review, not silently
resolved by changing the frozen outline.

Only `main.tex` is a root document. The official optional supplement mechanism
is retained without importing sample scientific prose. The main review PDF must
exclude supplementary pages. If enabled for an extended build, separate those
pages before submission as directed by the official kit.

`cvpr.sty`, `preamble.tex`, and `ieeenat_fullname.bst` are byte-identical upstream
copies. No margin, spacing, font-size, caption-size, or page-limit workaround is
enabled. The pinned preamble's optional layout tweaks remain commented.

The full staged `git diff --check` reports two upstream trailing-space lines:
`preamble.tex:11` and `ieeenat_fullname.bst:2`. They are preserved to keep the
official files byte-identical. A separate check excluding only the three
hash-verified upstream files passes for the authored project files.

## Dependencies inspected in the source

Direct style/preamble dependencies include Times/Helvetica fonts, xspace, xcolor,
graphicx, amsmath, amssymb, booktabs, natbib, silence, etoolbox, caption,
subcaption, url, keyval, lineno, enumitem, cleveref, cuted, currfile, and hyperref,
plus their TeX-distribution dependencies. Their local presence is unverified.
The official workflow uses a TeX Live-based latex-action; no workflow or package
installer is executed in P0. Use a normal complete Overleaf TeX environment.

## Compile outcome

**READY_FOR_OVERLEAF_COMPILE_NOT_LOCALLY_VERIFIED**

`latexmk`, `pdflatex`, `bibtex`, `tectonic`, `xelatex`, `lualatex`, and
`kpsewhich` were not found. PDF page count, runtime references, font embedding,
missing-package errors, and overfull boxes cannot be assessed. There is no claim
of successful compilation, a valid eight-page manuscript, or completed Overleaf
testing.

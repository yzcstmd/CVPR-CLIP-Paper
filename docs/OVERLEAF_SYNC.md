# Overleaf import and synchronization

The repository is a flat LaTeX project with `main.tex` at its root. No external
server path is needed by an active LaTeX input.

1. Import the GitHub repository through Overleaf's available GitHub integration,
   or upload a ZIP containing the tracked project files.
2. Set **Main document** to root `main.tex` and **Compiler** to pdfLaTeX.
   Use a current complete TeX Live environment.
3. Recompile. The bibliography and supplementary switches are intentionally off.
   Review the log, rendered anonymity, page count, fonts, and box warnings.
4. Add only verified bibliography entries and real citations, then change
   `\paperhasreferencesfalse` to `\paperhasreferencestrue`. Recompile through
   the normal BibTeX cycle; retain `ieeenat_fullname`.
5. When author-final figures arrive, follow `FIGURE_ASSET_STATUS.md`. Do not
   replace them with historical plots or enable nonexistent image paths.
6. Complete and author-review the LLM Usage Statement. Keep review mode and
   exclude supplement pages from the main review submission.

For ZIP import, use only version-controlled source files. Do not package `.git`,
`.local`, the ignored local P0 report, logs, credentials, data, predictions,
checkpoints, or internal handoffs. A snapshot can be exported after commit with:

```sh
git archive --format=zip --output=/tmp/cvpr-clip-paper-overleaf.zip HEAD
```

This task prepares source layout only. It does not connect to an Overleaf account,
test an Overleaf build, or certify account/plan-specific synchronization features.
Pull before editing and integrate ordinary changes; do not force-push or overwrite
concurrent work.

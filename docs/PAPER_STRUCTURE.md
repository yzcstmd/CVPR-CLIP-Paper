# Frozen paper structure

This is an engineering skeleton. Scientific prose, results, citations, and final
captions remain author work.

Title: **Fixing the Score Is Not Fixing the Order:
Ordinal Transfer for Unseen Grades in CLIP**

The P0 instruction freezes this title; do not restore a historical title
automatically.

| Number | Heading | Source |
|---|---|---|
| — | Abstract | `sections/00_abstract.tex` |
| 1 | Introduction | `sections/01_introduction.tex` |
| 2 | Related Work | `sections/02_related_work.tex` |
| 3 | Calibration–Ranking Separation | `sections/03_calibration_ranking.tex` |
| 3.1 | Ordinal Classification with Missing Grades | same file |
| 3.2 | What Class-Bias Calibration Can and Cannot Change | same file |
| 3.3 | Reference–Displacement Analysis | same file |
| 4 | TIE: Ordinal Displacement Transfer | `sections/04_tie.tex` |
| 4.1 | Neighbor Displacement Inheritance | same file |
| 4.2 | Structural Properties and Inheritance Error | same file |
| 4.3 | Calibration and Inference | same file |
| 5 | Experiments | `sections/05_experiments.tex` |
| 5.1 | Experimental Setup | same file |
| 5.2 | Main Results under Matched Calibration | same file |
| 5.3 | Matched-Strength Ranking Analysis | same file |
| 5.4 | Structural and Supervision Analyses | same file |
| 5.5 | Extensions and Scope | same file |
| 6 | Conclusion | `sections/06_conclusion.tex` |
| unnumbered | LLM Usage Statement | `sections/90_llm_usage_statement.tex` |
| — | References, when populated | `main.bib` |

`--` in LaTeX renders the en dash in the two frozen headings.
The administrative LLM statement follows Conclusion and precedes References;
it is not a seventh numbered main section. Its current disclosure covers P0
initialization only and explicitly requires author completion.

There is one root `main.tex`. Supplementary material is an input fragment,
disabled by default, using the official `\maketitlesupplementary` mechanism.

## Terminology

`CLIP_PAPER_TERMINOLOGY_FINAL_FROZEN_20261117.md` was not found in the
accessible project/attachment search. The author deferred providing its path.
Do not claim this file has been reviewed.

Until it arrives, retain only the explicitly supplied terms:
CLIP-based ordinal classification; missing grades / seen grades;
Reference–Displacement Analysis; TIE; ordinal displacement transfer;
post-hoc class-bias calibration; global score blending; MS-AUC;
adapter-averaged results.

TIE has no invented expansion. Reference–Displacement Analysis is not renamed
as another acronym method. The task is single-image, fixed-class ordinal
classification with CLIP, not MLLM ordinal classification.

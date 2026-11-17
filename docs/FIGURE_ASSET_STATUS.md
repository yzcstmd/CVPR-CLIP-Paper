# Figure asset status

| Asset | Status | Repository destination | Source / SHA256 |
|---|---|---|---|
| Figure 1, author-final layout | PENDING_AUTHOR_DELIVERY | `figures/fig1.pdf` | Not provided; no hash asserted |
| Figure 2, final matched-strength ranking plot | PENDING_AUTHOR_DELIVERY | `figures/fig2.pdf` | Not provided; no hash asserted |

The author explicitly deferred both final PDFs and the terminology-file path
during P0. The accessible task attachment contained only the initialization
instruction. Historical figure exports were found but were not substituted.
No figure, photograph, original prediction, or experimental CSV is copied.

Both LaTeX figure slots are comments, so absent assets are not active file
dependencies. This is an asset hold, not permission to reconstruct a figure.
Full-width rendering, aspect ratio, fonts, PDF metadata, page occupancy, and
caption appearance cannot be verified before final assets and a compiler exist.

On delivery, verify author-final identity and SHA256, copy only approved PDFs,
preserve scientific content and appearance, insert approved captions, enable
the slots, and compile at CVPR double-column full width. Keep internal source
paths in the ignored local initialization report, not in the public repository.

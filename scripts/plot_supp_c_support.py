import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from pathlib import Path

DATA = [
    ("Adience", "fixed-total", "CoOp", .0475, -.0095, -.0177),
    ("Adience", "fixed-total", "OrdinalCLIP", .1618, .0500, .0314),
    ("Adience", "fixed-total", "Tip-F", .0847, .0497, .0315),

    ("Adience", "fixed-seen", "CoOp", .0389, -.0220, -.0224),
    ("Adience", "fixed-seen", "OrdinalCLIP", .1102, .0376, .0255),
    ("Adience", "fixed-seen", "Tip-F", .0722, .0380, .0258),

    ("HCI", "fixed-total", "CoOp", .0515, -.0571, -.0766),
    ("HCI", "fixed-total", "OrdinalCLIP", .0750, -.0307, -.0560),
    ("HCI", "fixed-total", "Tip-F", .0554, -.0313, -.0593),

    ("HCI", "fixed-seen", "CoOp", .0913, -.0524, -.0830),
    ("HCI", "fixed-seen", "OrdinalCLIP", .0655, -.0258, -.0466),
    ("HCI", "fixed-seen", "Tip-F", .0565, -.0205, -.0569),

    ("FairFace", "fixed-total", "CoOp", .0367, .0150, .0084),
    ("FairFace", "fixed-total", "OrdinalCLIP", .1051, .0151, .0014),
    ("FairFace", "fixed-total", "Tip-F", .1051, .0715, .0402),

    ("KonIQ", "fixed-total", "CoOp", .0814, .0321, .0172),
    ("KonIQ", "fixed-total", "OrdinalCLIP", .0552, .0116, -.0051),
    ("KonIQ", "fixed-total", "Tip-F", .0722, .0616, .0535),
]

assert len(DATA) == 18

keys = [(r[0], r[1], r[2]) for r in DATA]
assert len(set(keys)) == 18

for row in DATA:
    a = np.array(row[3:], dtype=float)
    assert np.isfinite(a).all()
    assert a[0] > a[1] > a[2]

COLORS = {
    "CoOp": "#345c86",
    "OrdinalCLIP": "#14876a",
    "Tip-F": "#a16f34",
}

plt.rcParams.update({
    "font.family": "STIXGeneral",
    "mathtext.fontset": "stix",
    "font.size": 8,
    "axes.labelsize": 8,
    "axes.titlesize": 9,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

fig, axs = plt.subplots(
    2, 2, figsize=(6.875, 3.15)
)

fig.subplots_adjust(
    left=.10, right=.985,
    top=.94, bottom=.19,
    wspace=.25, hspace=.68
)

datasets = ["Adience", "HCI", "FairFace", "KonIQ"]

for ax, dataset in zip(axs.flat, datasets):
    subset = [r for r in DATA if r[0] == dataset]
    values = np.concatenate([
        np.asarray(r[3:], dtype=float)
        for r in subset
    ])

    spread = values.max() - values.min()
    pad = max(spread * .10, .01)

    for _, protocol, method, *scores in subset:
        ax.plot(
            [0, 10, 20],
            scores,
            color=COLORS[method],
            marker="o",
            markersize=3,
            linewidth=1.05,
            linestyle=(
                "-" if protocol == "fixed-total"
                else "--"
            ),
            markerfacecolor=(
                COLORS[method]
                if protocol == "fixed-total"
                else "white"
            ),
        )

    ax.axhline(
        0,
        color="#777777",
        linewidth=.55
    )

    ax.set_title(dataset, pad=4)
    ax.set_xlim(-1.3, 21.3)
    ax.set_ylim(
        values.min() - pad,
        values.max() + pad
    )
    ax.set_xticks([0, 10, 20])
    ax.set_xlabel("Target-grade support (%)")
    ax.tick_params(labelsize=7)

    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=.2)

axs[0, 0].set_ylabel(
    "TIE − Adapted MS-AUC"
)
axs[1, 0].set_ylabel(
    "TIE − Adapted MS-AUC"
)

handles = [
    Line2D(
        [0], [0],
        color=color,
        marker="o",
        lw=1.1,
        label=method
    )
    for method, color in COLORS.items()
]

handles += [
    Line2D(
        [0], [0],
        color="#555555",
        lw=1.1,
        label="Fixed total"
    ),
    Line2D(
        [0], [0],
        color="#555555",
        linestyle="--",
        lw=1.1,
        label="Fixed seen"
    ),
]

fig.legend(
    handles=handles,
    loc="lower center",
    bbox_to_anchor=(.51, .010),
    ncol=5,
    fontsize=7.3,
    frameon=False,
    columnspacing=1.0,
    handlelength=1.8
)

out = Path(
    "figures/supp/supp_c_support_levels.pdf"
)
out.parent.mkdir(parents=True, exist_ok=True)

fig.savefig(
    out,
    metadata={
        "Title": "Grade-specific support sensitivity",
        "Author": ""
    }
)

fig.savefig(
    out.with_suffix(".png"),
    dpi=220
)

plt.close(fig)

print("PASS: 18 monotone trajectories.")
print("Figure:", out)

import argparse
import csv
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FormatStrFormatter


DATASETS = ["adience", "hci", "fairface", "koniq"]
TITLES = ["Adience", "HCI", "FairFace", "KonIQ"]
METHODS = [
    ("COOP_STYLE", "CoOp-style"),
    ("ORD_FROZEN", "OrdinalCLIP-style"),
    ("KGCOOP_STYLE", "KgCoOp-style"),
    ("TASKRES_STYLE", "TaskRes-style\n(CE)"),
    ("TASKRES_SORD", "TaskRes-style\n(SORD)"),
    ("TIP_ADAPTER_F", "Tip-Adapter-F\n(CE)"),
    ("TIPF_SORD", "Tip-Adapter-F\n(SORD)"),
    ("M3", "M3"),
    ("TEXT_ONLY", "TEXT_ONLY"),
]
GRID = np.array([i / 10 for i in range(16)] + [2.0])
GREEN = "#176B59"
BROWN = "#B47D48"

plt.rcParams.update({
    "font.family": "STIXGeneral",
    "mathtext.fontset": "stix",
    "font.size": 8,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.linewidth": 0.55,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.facecolor": "white",
})


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError(f"Empty source: {path}")
    for row in rows:
        if "lambda_" not in row and "lambda" in row:
            row["lambda_"] = row["lambda"]
    return rows


def number(row, key):
    try:
        return float(row[key])
    except (ValueError, TypeError):
        return float("nan")


def ordered(rows):
    rows = sorted(rows, key=lambda r: number(r, "lambda_"))
    x = np.array([number(r, "lambda_") for r in rows])
    if x.shape != GRID.shape or not np.allclose(x, GRID, atol=1e-12):
        raise ValueError(
            "Each curve must contain the original 17-point grid exactly once."
        )
    return rows


def save_figure(fig, out, stem):
    fig.savefig(
        out / (stem + ".pdf"),
        metadata={"Title": stem, "Author": ""},
    )
    fig.savefig(out / (stem + ".png"), dpi=220)
    plt.close(fig)


def curve_matrix(curves, family, out):
    cells = {}

    for ds in DATASETS:
        for method, _ in METHODS:
            rows = ordered([
                r for r in curves
                if r["dataset"].lower() == ds
                and r["layer"] == "INTERNAL"
                and r["method"] == method
            ])
            b = np.array([number(r, "Blend_AUC") for r in rows])
            t = np.array([number(r, "TIE_AUC") for r in rows])
            d = np.array([number(r, "delta") for r in rows])

            if not np.isfinite(np.stack([b, t, d])).all():
                raise ValueError(f"Missing point estimate: {ds}/{method}")
            if not np.allclose(t - b, d, rtol=0, atol=1e-12):
                raise ValueError(f"Paired difference mismatch: {ds}/{method}")
            if abs(d[0]) > 1e-12:
                raise ValueError(
                    f"Nonzero difference at zero strength: {ds}/{method}"
                )

            lo = np.array([number(r, "CI_low") for r in rows])
            hi = np.array([number(r, "CI_high") for r in rows])

            for j, r in enumerate(rows):
                if r.get("CI_valid", "True").lower() not in ("true", "1"):
                    lo[j] = hi[j] = np.nan
                if r.get("point_conditions"):
                    if int(float(r["point_conditions"])) != 9:
                        raise ValueError(f"Wrong population: {ds}/{method}")

            cells[ds, method] = (b, t, d, lo, hi)

        fam = ordered([
            r for r in family
            if r["dataset"].lower() == ds
            and r["layer"] == "INTERNAL"
            and r["method"] == "NINE_METHOD_FAMILY"
        ])

        for field, pos in [
            ("Blend_AUC", 0),
            ("TIE_AUC", 1),
            ("delta", 2),
        ]:
            mean = np.mean(
                [cells[ds, m][pos] for m, _ in METHODS], axis=0
            )
            expected = [number(r, field) for r in fam]
            if not np.allclose(mean, expected, rtol=0, atol=1e-10):
                raise ValueError(
                    f"Configuration mean disagrees with Fig. 2: {ds}/{field}"
                )

    positive = sum(
        cells[ds, m][2][10] > 1e-12
        for ds in DATASETS for m, _ in METHODS
    )
    if positive != 35:
        raise ValueError(
            f"Expected 35 positive interior settings at lambda=1; found {positive}."
        )

    fig, axs = plt.subplots(
        9, 4, figsize=(6.875, 7.1), sharex=True, sharey="col"
    )
    fig.subplots_adjust(
        left=0.19, right=0.985, bottom=0.065, top=0.955,
        wspace=0.27, hspace=0.20,
    )

    for c, ds in enumerate(DATASETS):
        values = np.concatenate([
            np.concatenate(cells[ds, m][2:])
            for m, _ in METHODS
        ])
        finite = values[np.isfinite(values)]
        lo = min(0.0, finite.min())
        hi = max(0.0, finite.max())
        pad = max((hi - lo) * 0.08, 0.003)

        for r, (method, _) in enumerate(METHODS):
            ax = axs[r, c]
            _, _, d, lower, upper = cells[ds, method]

            ax.fill_between(
                GRID, lower, upper,
                color=GREEN, alpha=0.16, linewidth=0,
            )
            ax.axhline(0, color="#777777", lw=0.55)
            ax.axvline(
                1, color="#999999", lw=0.55, ls=(0, (3, 3))
            )
            ax.plot(
                GRID, d,
                color=GREEN, lw=0.9, marker="o", ms=2.1,
            )

            ax.set_xlim(-0.04, 2.04)
            ax.set_ylim(lo - pad, hi + pad)
            ax.set_xticks([0, 0.5, 1, 1.5, 2])
            ax.yaxis.set_major_locator(MaxNLocator(3))
            ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
            ax.tick_params(
                labelsize=7, length=2, width=0.5, pad=1.5,
                labelleft=True, labelbottom=(r == 8),
            )

            if r == 0:
                ax.set_title(TITLES[c], fontsize=9, pad=5)
            if r == 8:
                ax.set_xlabel(r"$\lambda$", fontsize=8, labelpad=1)

    for r, (_, label) in enumerate(METHODS):
        box = axs[r, 0].get_position()
        fig.text(
            0.008, (box.y0 + box.y1) / 2,
            label, ha="left", va="center", fontsize=7.4,
        )

    fig.text(
        0.19, 0.995,
        r"$\Delta$MS-AUC = TIE $-$ Blend",
        ha="left", va="top", fontsize=8,
    )
    save_figure(fig, out, "supp_a_configuration_curves")


def tradeoff_plot(table, out):
    styles = [
        ("T0", "Zero-shot", "*", "#777777", True, 8),
        ("RAW", "Adapted", "x", "#999999", True, 5.8),
        ("RAW_CAL", "Adapted+C", "s", "#55718D", True, 5),
        ("BLEND_CAL", "Blend-S+C", "^", BROWN, False, 6),
        ("BLEND_CAL_AWARE", "Blend-A+C", "D", BROWN, False, 5.3),
        ("TIE_CAL", "TIE+C", "o", GREEN, True, 6.5),
    ]

    def value(ds, method, metric):
        rows = [
            r for r in table
            if r["dataset"].lower() == ds
            and r["row"] == method
            and r["metric"] == metric
        ]
        if len(rows) != 1:
            raise ValueError(
                f"Expected one original Table 1 point: {ds}/{method}/{metric}"
            )
        row = rows[0]
        if (
            int(float(row["conditions"])) != 162
            or int(float(row["methods"])) != 9
        ):
            raise ValueError(f"Wrong Table 1 population: {ds}/{method}")
        v = number(row, "point")
        if not np.isfinite(v):
            raise ValueError(f"Missing Table 1 value: {ds}/{method}/{metric}")
        return v

    fig, axs = plt.subplots(2, 2, figsize=(6.875, 3.9))
    fig.subplots_adjust(
        left=0.09, right=0.985, bottom=0.21, top=0.93,
        wspace=0.26, hspace=0.53,
    )
    handles = []

    for idx, (ds, ax) in enumerate(zip(DATASETS, axs.flat)):
        for method, label, marker, color, filled, size in styles:
            x = value(ds, method, "seen_MAE")
            y = value(ds, method, "missing_MAE")
            h, = ax.plot(
                x, y, ls="none", marker=marker, ms=size,
                markeredgecolor=color,
                markerfacecolor=color if filled else "white",
                markeredgewidth=1.0,
                label=label,
                zorder=4 if method == "TIE_CAL" else 3,
            )
            if idx == 0:
                handles.append(h)

        start = (
            value(ds, "RAW_CAL", "seen_MAE"),
            value(ds, "RAW_CAL", "missing_MAE"),
        )
        end = (
            value(ds, "TIE_CAL", "seen_MAE"),
            value(ds, "TIE_CAL", "missing_MAE"),
        )
        ax.annotate(
            "", xy=end, xytext=start,
            arrowprops={
                "arrowstyle": "->",
                "color": GREEN,
                "lw": 0.7,
                "shrinkA": 4,
                "shrinkB": 5,
            },
            zorder=2,
        )
        ax.set_title(TITLES[idx], fontsize=9, pad=4)
        ax.set_xlabel(
            r"Seen MAE $\downarrow$", fontsize=8.5, labelpad=1.5
        )
        ax.set_ylabel(
            r"Missing MAE $\downarrow$", fontsize=8.5, labelpad=2
        )
        ax.xaxis.set_major_locator(MaxNLocator(4))
        ax.yaxis.set_major_locator(MaxNLocator(4))
        ax.tick_params(labelsize=8, length=2.5, pad=2)
        ax.margins(x=0.13, y=0.15)
        ax.grid(lw=0.35, color="#E5E5E5", zorder=0)

    fig.legend(
        handles, [s[1] for s in styles],
        loc="lower center", bbox_to_anchor=(0.5, 0.005),
        ncol=3, frameon=False, fontsize=8.2,
        handletextpad=0.4, columnspacing=1.6,
    )
    save_figure(fig, out, "supp_a_error_tradeoff")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--curves", required=True)
    parser.add_argument("--family", required=True)
    parser.add_argument("--table", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    curve_matrix(
        read_csv(args.curves),
        read_csv(args.family),
        out,
    )
    tradeoff_plot(read_csv(args.table), out)


if __name__ == "__main__":
    main()

import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("csv_path", type=Path)
parser.add_argument("pdf_path", type=Path)
args = parser.parse_args()

names = ["Adience", "HCI", "FairFace", "KonIQ"]

with args.csv_path.open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))

assert len(rows) == 4
by_name = {r["dataset"].strip().casefold(): r for r in rows}
assert set(by_name) == {x.casefold() for x in names}
rows = [by_name[name.casefold()] for name in names]

kappa = np.array([float(r["kappa_median"]) for r in rows])
inheritance = np.array([float(r["I_mean"]) for r in rows])
model_change = np.array([float(r["A_mean"]) for r in rows])

assert np.isfinite(np.r_[kappa, inheritance, model_change]).all()
assert ((kappa >= 0) & (kappa <= 1)).all()

plt.rcParams.update({
    "font.family": "STIXGeneral",
    "mathtext.fontset": "stix",
    "font.size": 8.5,
    "axes.titlesize": 9.5,
    "axes.labelsize": 8.5,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8.5,
    "legend.fontsize": 8,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.linewidth": 0.6
})

fig, axes = plt.subplots(1, 2, figsize=(6.875, 2.3))
fig.subplots_adjust(
    left=0.10, right=0.985, bottom=0.22, top=0.73, wspace=0.38
)

y = np.arange(4)
gray, teal, brown = "#CBD1D5", "#397D79", "#B4773C"

ax = axes[0]
ax.barh(
    y, kappa, height=0.55, color=gray,
    label="Constant", zorder=3
)
ax.barh(
    y, 1-kappa, left=kappa, height=0.55, color=teal,
    label="Image-dependent", zorder=3
)

for row, value in enumerate(kappa):
    ax.text(
        value/2, row, f"{100*value:.1f}%",
        ha="center", va="center", fontsize=8, color="#252A2E"
    )

ax.set(
    xlim=(0, 1), ylim=(3.6, -0.6),
    yticks=y, yticklabels=names,
    xticks=[0, 0.5, 1], xticklabels=["0", "0.5", "1.0"],
    xlabel="Median energy share"
)
ax.set_title("(a) Error components", loc="left", pad=30)
ax.legend(
    loc="lower left", bbox_to_anchor=(-0.02, 1.02), ncol=2,
    frameon=False, handlelength=1.0, columnspacing=0.9,
    borderaxespad=0
)

ax = axes[1]
ax.axvline(0, color="#687278", lw=0.7, zorder=1)

for values, offset, color, marker, label in [
    (inheritance, -0.14, teal, "o", r"$I$: inheritance"),
    (model_change, 0.14, brown, "s", r"$A$: model change")
]:
    yy = y + offset
    ax.hlines(yy, 0, values, color=color, lw=1.4, zorder=2)
    ax.scatter(
        values, yy, s=22, color=color, marker=marker,
        label=label, zorder=3
    )
    for value, row in zip(values, yy):
        text = (
            f"{value:+.4f}"
            if value == 0 or abs(value) >= 5e-5
            else f"{value:+.1e}"
        )
        text = text.replace("-", "−")
        ax.annotate(
            text, (value, row), xytext=(8 if offset < 0 else 4, 6 if offset < 0 else -6),
            textcoords="offset points", va="center",
            ha="left", fontsize=7.5, color=color
        )

all_gaps = np.r_[inheritance, model_change]
ax.set(
    xlim=(
        min(-0.015, float(all_gaps.min())-0.008),
        max(0.15, float(all_gaps.max())+0.035)
    ),
    ylim=(3.6, -0.6),
    yticks=y, yticklabels=names,
    xlabel="MS-AUC difference"
)
ax.set_title("(b) Signed ranking gap", loc="left", pad=30)
ax.legend(
    loc="lower left", bbox_to_anchor=(-0.02, 1.02), ncol=2,
    frameon=False, handlelength=1, columnspacing=0.8,
    borderaxespad=0
)

for ax in axes:
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", length=3, width=0.6)
    ax.grid(axis="x", color="#E7EAEB", lw=0.5, zorder=0)

args.pdf_path.parent.mkdir(parents=True, exist_ok=True)
# Crop only exterior vertical whitespace; retain the full-width drawing scale.
fig.canvas.draw()
crop = fig.get_tightbbox(fig.canvas.get_renderer())
crop = matplotlib.transforms.Bbox.from_extents(
    0, crop.y0 - 0.025, fig.get_figwidth(), crop.y1 + 0.05
)
fig.savefig(
    args.pdf_path,
    bbox_inches=crop,
    metadata={
        "Title": "Inheritance error diagnostic",
        "Author": "",
        "Creator": "Matplotlib"
    }
)
fig.savefig(args.pdf_path.with_suffix(".png"), dpi=200, bbox_inches=crop)
plt.close(fig)

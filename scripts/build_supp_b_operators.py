import argparse
import csv
import itertools
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score

DATASETS = ["adience", "hci", "fairface", "koniq"]
DISPLAY = ["Adience", "HCI", "FairFace", "KonIQ"]
VARIANTS = ["adapted", "reference", "tie", "score", "left", "right", "distance"]
LABELS = [
    "Adapted", "Reference-only", r"\textbf{TIE}",
    "Direct score interpolation", "Left-anchor inheritance",
    "Right-anchor inheritance", "Distance-weighted inheritance"
]


def score_variants(T, S, missing):
    D = S - T
    seen = np.flatnonzero(~missing)
    outputs = {name: S.copy() for name in VARIANTS}
    outputs["reference"][:, missing] = T[:, missing]

    for m in np.flatnonzero(missing):
        lower, upper = seen[seen < m], seen[seen > m]

        if len(lower) and len(upper):
            lo, hi = int(lower[-1]), int(upper[0])
            mean = 0.5 * (D[:, lo] + D[:, hi])
            alpha = (m - lo) / (hi - lo)

            outputs["tie"][:, m] = T[:, m] + mean
            outputs["score"][:, m] = 0.5 * (S[:, lo] + S[:, hi])
            outputs["left"][:, m] = T[:, m] + D[:, lo]
            outputs["right"][:, m] = T[:, m] + D[:, hi]
            outputs["distance"][:, m] = (
                T[:, m] + (1 - alpha) * D[:, lo] + alpha * D[:, hi]
            )
        else:
            n = int(lower[-1] if len(lower) else upper[0])

            for name in ["tie", "left", "right", "distance"]:
                outputs[name][:, m] = T[:, m] + D[:, n]

            outputs["score"][:, m] = S[:, n]

            assert np.allclose(
                outputs["tie"][:, m] - S[:, n],
                T[:, m] - T[:, n], rtol=0, atol=1e-10
            )
            assert np.array_equal(outputs["score"][:, m], S[:, n])

    for Z in outputs.values():
        assert np.array_equal(Z[:, ~missing], S[:, ~missing])

    return outputs


def metrics(Z, y, missing, pairs, weights):
    aucs = []
    for m, n in pairs:
        keep = (y == m) | (y == n)
        positive = y[keep] == m
        assert positive.any() and (~positive).any()
        aucs.append(
            roc_auc_score(positive, Z[keep, m] - Z[keep, n])
        )

    prediction = np.argmax(Z, axis=1)
    errors = [
        np.abs(prediction[y == m] - m).mean()
        for m in np.flatnonzero(missing)
    ]

    return float(np.dot(weights, aucs)), float(np.mean(errors))


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("baseline_reference", type=Path)
    parser.add_argument("data_dir", type=Path)
    parser.add_argument("table_tex", type=Path)
    args = parser.parse_args()

    with args.manifest.open(newline="", encoding="utf-8") as handle:
        manifest = list(csv.DictReader(handle))

    assert len(manifest) == 648, "Use the complete main-paper population."

    for row in manifest:
        row["dataset"] = row["dataset"].strip().casefold()
        row["seed"] = int(row["seed"])

    assert {r["dataset"] for r in manifest} == set(DATASETS)

    configs = sorted({r["configuration"] for r in manifest})
    masks = sorted({r["mask"] for r in manifest})
    assert len(configs) == 9 and len(masks) == 6

    keys = [
        (r["dataset"], r["configuration"], r["mask"], r["seed"])
        for r in manifest
    ]
    expected = set(
        itertools.product(DATASETS, configs, masks, [101, 202, 303])
    )
    assert len(set(keys)) == len(keys) and set(keys) == expected

    points = []

    for row in manifest:
        path = Path(row["npz"])
        if not path.is_absolute():
            path = args.manifest.parent / path

        with np.load(path, allow_pickle=False) as source:
            T = np.asarray(source["T"], dtype=np.float64)
            S = np.asarray(source["S"], dtype=np.float64)
            y = np.asarray(source["y"], dtype=np.int64)
            missing = np.asarray(source["missing"])
            pairs = np.asarray(source["pairs"], dtype=np.int64)
            weights = np.asarray(source["pair_weights"], dtype=np.float64)
            image_ids = source["image_ids"].astype(str)

        assert S.ndim == 2 and T.shape == S.shape
        N, K = S.shape
        assert np.isfinite(S).all() and np.isfinite(T).all()
        assert y.shape == image_ids.shape == (N,)
        assert len(np.unique(image_ids)) == N
        assert y.min() >= 0 and y.max() < K
        assert missing.dtype == np.bool_ and missing.shape == (K,)
        assert 0 < missing.sum() < K
        assert pairs.ndim == 2 and pairs.shape[1] == 2 and len(pairs) > 0
        assert (pairs >= 0).all() and (pairs < K).all()
        assert missing[pairs[:, 0]].all()
        assert (~missing[pairs[:, 1]]).all()
        assert weights.shape == (len(pairs),) and (weights >= 0).all()
        assert np.isclose(weights.sum(), 1, rtol=0, atol=1e-12)
        assert all((y == m).any() for m in np.flatnonzero(missing))

        for variant, Z in score_variants(T, S, missing).items():
            auc, mae = metrics(Z, y, missing, pairs, weights)
            points.append({
                "dataset": row["dataset"],
                "configuration": row["configuration"],
                "mask": row["mask"],
                "seed": row["seed"],
                "variant": variant,
                "MS_AUC": auc,
                "Missing_MAE": mae
            })

    configuration_rows = []

    for dataset, config, variant in itertools.product(
        DATASETS, configs, VARIANTS
    ):
        group = [
            r for r in points
            if (r["dataset"], r["configuration"], r["variant"])
            == (dataset, config, variant)
        ]
        assert len(group) == 18
        configuration_rows.append({
            "dataset": dataset,
            "configuration": config,
            "variant": variant,
            **{
                metric: float(np.mean([r[metric] for r in group]))
                for metric in ["MS_AUC", "Missing_MAE"]
            }
        })

    family = {}

    for dataset, variant in itertools.product(DATASETS, VARIANTS):
        group = [
            r for r in configuration_rows
            if (r["dataset"], r["variant"]) == (dataset, variant)
        ]
        assert len(group) == 9
        family[dataset, variant] = {
            metric: float(np.mean([r[metric] for r in group]))
            for metric in ["MS_AUC", "Missing_MAE"]
        }

    # References must come from previously saved primary results.
    with args.baseline_reference.open(
        newline="", encoding="utf-8"
    ) as handle:
        references = list(csv.DictReader(handle))

    reference_keys = {
        (r["dataset"].strip().casefold(), r["variant"])
        for r in references
    }

    assert len(references) == 8
    assert reference_keys == set(
        itertools.product(DATASETS, ["adapted", "tie"])
    )

    for row in references:
        key = (row["dataset"].strip().casefold(), row["variant"])
        for metric in ["MS_AUC", "Missing_MAE"]:
            assert np.isclose(
                family[key][metric], float(row[metric]),
                rtol=0, atol=1e-9
            ), (key, metric)

    write_csv(
        args.data_dir / "supp_b_operator_points.csv",
        ["dataset", "configuration", "mask", "seed", "variant",
         "MS_AUC", "Missing_MAE"],
        points
    )
    write_csv(
        args.data_dir / "supp_b_operator_configurations.csv",
        ["dataset", "configuration", "variant", "MS_AUC", "Missing_MAE"],
        configuration_rows
    )
    write_csv(
        args.data_dir / "supp_b_operator_summary.csv",
        ["dataset", "variant", "MS_AUC", "Missing_MAE"],
        [
            {"dataset": d, "variant": v, **family[d, v]}
            for d, v in family
        ]
    )

    lines = [
        r"\begin{tabular*}{\textwidth}{@{}l@{\extracolsep{\fill}}*{8}{r}@{}}",
        r"\toprule",
        " & " + " & ".join(
            r"\multicolumn{2}{c}{" + n + "}" for n in DISPLAY
        ) + r" \\",
        r"\cmidrule(lr){2-3}\cmidrule(lr){4-5}"
        r"\cmidrule(lr){6-7}\cmidrule(lr){8-9}",
        "Construction & " + " & ".join(
            [r"MS-AUC $\uparrow$ & MAE $\downarrow$"] * 4
        ) + r" \\",
        r"\midrule"
    ]

    for variant, label in zip(VARIANTS, LABELS):
        cells = [
            f"{family[d, variant][m]:.3f}"
            for d in DATASETS for m in ["MS_AUC", "Missing_MAE"]
        ]
        lines.append(label + " & " + " & ".join(cells) + r" \\")

    lines += [r"\bottomrule", r"\end{tabular*}"]
    args.table_tex.parent.mkdir(parents=True, exist_ok=True)
    args.table_tex.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(
        "648 conditions; seven fixed operators; "
        "primary baselines reproduced."
    )


if __name__ == "__main__":
    main()

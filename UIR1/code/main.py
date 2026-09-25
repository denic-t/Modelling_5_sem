import json
from pathlib import Path

import numpy as np

from uir1 import plots
from uir1.distribution import hypoexp_generate, hypoexp_params
from uir1.stats import autocorrelation, characteristics, pearson
from uir1.tables import form_acf, form_deviations, form_values

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / "210_variant.txt"
REPORT = ROOT.parent / "report"
OUTPUT = ROOT / "output"
SIZES = [10, 20, 50, 100, 200, 300]
N_BINS = 10
SEED = 42


def load(path):
    return np.array([float(s.replace(",", ".")) for s in path.read_text(encoding="utf-8").split()])


def main():
    figs, tabs = REPORT / "figures", REPORT / "tables"
    for d in (figs, tabs, OUTPUT):
        d.mkdir(parents=True, exist_ok=True)

    x = load(DATA)
    given = {n: characteristics(x[:n]) for n in SIZES}
    ref = given[SIZES[-1]]
    t, cv = ref["mean"], ref["cv"]

    t1, t2 = hypoexp_params(t, cv)
    y = hypoexp_generate(t1, t2, len(x), np.random.default_rng(SEED))
    np.savetxt(OUTPUT / "generated.txt", y, fmt="%.3f")
    gen = {n: characteristics(y[:n]) for n in SIZES}

    acf_x, acf_y = autocorrelation(x), autocorrelation(y)
    r_xy = pearson(x, y)

    tables = {
        "form1": form_values(SIZES, given),
        "form1_dev": form_deviations(SIZES, given, {n: ref for n in SIZES}),
        "form2": form_values(SIZES, gen),
        "form2_dev": form_deviations(SIZES, gen, given),
        "form3": form_acf(acf_x, acf_y),
    }
    for name, tex in tables.items():
        (tabs / f"{name}.tex").write_text(tex, encoding="utf-8")

    bins = np.linspace(x.min(), x.max(), N_BINS + 1)
    plots.sequence(x, figs / "sequence.png")
    plots.acf({"Исходная": acf_x}, "Автокорреляция исходной последовательности", figs / "acf_given.png")
    plots.histogram(x, bins, figs / "histogram.png")
    plots.density(x, bins, t1, t2, figs / "density.png")
    plots.compare_sequences(x, y, figs / "compare_sequence.png")
    plots.compare_histograms(x, y, np.linspace(0, max(x.max(), y.max()), N_BINS + 1), figs / "compare_histogram.png")
    plots.acf({"Исходная": acf_x, "Сгенерированная": acf_y}, "Сравнение автокорреляций", figs / "acf_compare.png")

    results = {
        "t": t, "cv": cv, "t1": t1, "t2": t2,
        "acf_given": acf_x.tolist(), "acf_gen": acf_y.tolist(), "r_xy": r_xy,
        "freq": np.histogram(x, bins)[0].tolist(), "bins": bins.tolist(),
        "given": {n: {**c, "ci": {str(p): v for p, v in c["ci"].items()}} for n, c in given.items()},
        "gen": {n: {**c, "ci": {str(p): v for p, v in c["ci"].items()}} for n, c in gen.items()},
    }
    (OUTPUT / "results.json").write_text(json.dumps(results, indent=2, default=float), encoding="utf-8")

    print(f"Mean t: {t:.4f}, cv: {cv:.4f}")
    print(f"Hypoexponential params: t1 = {t1:.4f}, t2 = {t2:.4f}")
    print(f"Generated (n=300): mean = {gen[300]['mean']:.4f}, cv = {gen[300]['cv']:.4f}")
    print(f"Correlation given vs generated: r = {r_xy:.4f}")


if __name__ == "__main__":
    main()

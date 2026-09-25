import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .distribution import hypoexp_pdf


def _save(fig, ax, title, path):
    ax.set_title(title)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def sequence(x, path):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(np.arange(1, len(x) + 1), x, lw=1)
    ax.set_xlabel("Номер наблюдения")
    ax.set_ylabel("Значение")
    _save(fig, ax, "Исходная числовая последовательность", path)


def acf(series, title, path):
    fig, ax = plt.subplots(figsize=(8, 4))
    for (label, values), marker in zip(series.items(), "os"):
        ax.plot(range(1, len(values) + 1), values, marker=marker, label=label)
    ax.axhline(0, lw=0.8)
    ax.set_xticks(range(1, len(next(iter(series.values()))) + 1))
    ax.set_xlabel("Сдвиг")
    ax.set_ylabel("Коэффициент автокорреляции")
    if len(series) > 1:
        ax.legend()
    _save(fig, ax, title, path)


def histogram(x, bins, path):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(x, bins=bins, edgecolor="black", alpha=0.75)
    ax.set_xlabel("Значение")
    ax.set_ylabel("Частота")
    _save(fig, ax, f"Гистограмма исходной ЧП ({len(bins) - 1} интервалов)", path)


def density(x, bins, t1, t2, path):
    grid = np.linspace(0, bins[-1], 1000)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(x, bins=bins, density=True, edgecolor="black", alpha=0.6, label="Исходная ЧП")
    ax.plot(grid, hypoexp_pdf(grid, t1, t2), lw=2, label="Гипоэкспоненциальная плотность")
    ax.set_xlabel("x")
    ax.set_ylabel("Плотность")
    ax.legend()
    _save(fig, ax, "Аппроксимация закона распределения", path)


def compare_sequences(x, y, path):
    idx = np.arange(1, len(x) + 1)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(idx, x, lw=1, label="Исходная")
    ax.plot(idx, y, lw=1, alpha=0.8, label="Сгенерированная")
    ax.set_xlabel("Номер наблюдения")
    ax.set_ylabel("Значение")
    ax.legend()
    _save(fig, ax, "Сравнение последовательностей", path)


def compare_histograms(x, y, bins, path):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(x, bins=bins, density=True, alpha=0.5, label="Исходная")
    ax.hist(y, bins=bins, density=True, alpha=0.5, label="Сгенерированная")
    ax.set_xlabel("Значение")
    ax.set_ylabel("Плотность")
    ax.legend()
    _save(fig, ax, "Сравнение гистограмм", path)

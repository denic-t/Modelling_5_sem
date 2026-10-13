import numpy as np


def hypoexp_params(mean, cv):
    """Средние фаз t1, t2 двухфазного гипоэкспоненциального закона с заданными мат. ожиданием и коэффициентом вариации."""
    if not 1 / np.sqrt(2) <= cv < 1:
        raise ValueError(f"hypoexponential requires 0.707 <= cv < 1, got {cv:.4f}")
    s = np.sqrt(2 * cv ** 2 - 1)
    return mean * (1 + s) / 2, mean * (1 - s) / 2


def hypoexp_pdf(x, t1, t2):
    """Плотность гипоэкспоненциального закона: свёртка двух экспоненциальных плотностей."""
    return (np.exp(-x / t1) - np.exp(-x / t2)) / (t1 - t2)


def hypoexp_generate(t1, t2, size, rng):
    """Сумма двух экспоненциальных фаз, каждая получена методом обратной функции."""
    r1, r2 = rng.random(size), rng.random(size)
    # r из [0; 1), поэтому 1 - r > 0 и логарифм всегда определён
    return -t1 * np.log(1 - r1) - t2 * np.log(1 - r2)

import numpy as np

# t_p = Ф^-1((1 + p) / 2), значения из таблицы методички
T_P = {0.9: 1.643, 0.95: 1.960, 0.99: 2.576}


def characteristics(x):
    """Мат. ожидание, несмещённая дисперсия, с.к.о., коэффициент вариации и полуинтервалы доверительных интервалов."""
    n = len(x)
    mean = x.mean()
    var = x.var(ddof=1)  # несмещённая оценка: деление на n - 1
    std = np.sqrt(var)
    ci = {p: t * std / np.sqrt(n) for p, t in T_P.items()}
    return {"mean": mean, "ci": ci, "var": var, "std": std, "cv": std / mean}


def rel_dev(value, reference):
    """Относительное отклонение от эталона в процентах, со знаком."""
    return (value - reference) / reference * 100


def pearson(x, y):
    """Коэффициент корреляции Пирсона двух массивов одинаковой длины."""
    dx, dy = x - x.mean(), y - y.mean()
    return (dx * dy).sum() / np.sqrt((dx ** 2).sum() * (dy ** 2).sum())


def autocorrelation(x, max_lag=10):
    """Коэффициенты автокорреляции для сдвигов 1..max_lag: корреляция Пирсона x[:-k] и x[k:]."""
    return np.array([pearson(x[:-k], x[k:]) for k in range(1, max_lag + 1)])

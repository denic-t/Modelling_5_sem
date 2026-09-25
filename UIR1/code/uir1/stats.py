import numpy as np

T_P = {0.9: 1.643, 0.95: 1.960, 0.99: 2.576}


def characteristics(x):
    n = len(x)
    mean = x.mean()
    var = x.var(ddof=1)
    std = np.sqrt(var)
    ci = {p: t * std / np.sqrt(n) for p, t in T_P.items()}
    return {"mean": mean, "ci": ci, "var": var, "std": std, "cv": std / mean}


def rel_dev(value, reference):
    return (value - reference) / reference * 100


def pearson(x, y):
    dx, dy = x - x.mean(), y - y.mean()
    return (dx * dy).sum() / np.sqrt((dx ** 2).sum() * (dy ** 2).sum())


def autocorrelation(x, max_lag=10):
    return np.array([pearson(x[:-k], x[k:]) for k in range(1, max_lag + 1)])

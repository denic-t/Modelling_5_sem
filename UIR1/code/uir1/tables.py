from .stats import rel_dev

ROWS = [
    ("Мат. ожидание", "mean", 3),
    ("Дисперсия", "var", 3),
    ("С.к.о.", "std", 3),
    ("Коэффициент вариации", "cv", 4),
    ("Дов. полуинтервал 0,90", ("ci", 0.9), 3),
    ("Дов. полуинтервал 0,95", ("ci", 0.95), 3),
    ("Дов. полуинтервал 0,99", ("ci", 0.99), 3),
]


def num(v, d):
    """Число с d знаками после десятичной запятой и минусом в формате LaTeX."""
    s = f"{abs(v):.{d}f}".replace(".", ",")
    return ("$-$" if v < 0 and s.strip("0,") else "") + s


def _get(ch, key):
    """Характеристика по ключу, ключ ("ci", p) - полуинтервал для вероятности p."""
    return ch[key[0]][key[1]] if isinstance(key, tuple) else ch[key]


def _table(sizes, cell):
    """Таблица LaTeX: строка на характеристику, столбец на объём выборки."""
    lines = [
        f"\\begin{{tabular}}{{|l|{'c|' * len(sizes)}}}", "\\hline",
        "\\textbf{Характеристика} & " + " & ".join(str(n) for n in sizes) + " \\\\ \\hline",
    ]
    for title, key, d in ROWS:
        lines.append(f"{title} & " + " & ".join(cell(n, key, d) for n in sizes) + " \\\\ \\hline")
    lines.append("\\end{tabular}")
    return "\n".join(lines)


def form_values(sizes, chars):
    """Формы 1 и 2: значения характеристик."""
    return _table(sizes, lambda n, key, d: num(_get(chars[n], key), d))


def form_deviations(sizes, chars, refs):
    """Модули относительных отклонений от эталона refs в процентах."""
    return _table(sizes, lambda n, key, d: num(abs(rel_dev(_get(chars[n], key), _get(refs[n], key))), 2) + "\\%")


def form_acf_given(acf):
    """Форма 3 для заданной ЧП: коэффициенты автокорреляции по сдвигам."""
    lines = ["\\begin{tabular}{|c|c|}", "\\hline", "\\textbf{Сдвиг} & \\textbf{К-т АК} \\\\ \\hline"]
    lines += [f"{k} & {num(a, 4)} \\\\ \\hline" for k, a in enumerate(acf, 1)]
    lines.append("\\end{tabular}")
    return "\n".join(lines)


def form_acf(acf_given, acf_gen):
    """Форма 3: коэффициенты автокорреляции исходной и сгенерированной ЧП."""
    lines = [
        "\\begin{tabular}{|c|c|c|c|}", "\\hline",
        "\\textbf{Сдвиг} & \\textbf{Исходная ЧП} & \\textbf{Сгенерированная ЧП} & \\textbf{Различие, \\%} \\\\ \\hline",
    ]
    for k, (a, g) in enumerate(zip(acf_given, acf_gen), 1):
        lines.append(f"{k} & {num(a, 4)} & {num(g, 4)} & {num(abs(rel_dev(g, a)), 1)}\\% \\\\ \\hline")
    lines.append("\\end{tabular}")
    return "\n".join(lines)

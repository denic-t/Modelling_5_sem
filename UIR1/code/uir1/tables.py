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
    s = f"{abs(v):.{d}f}".replace(".", ",")
    return ("$-$" if v < 0 and s.strip("0,") else "") + s


def _get(ch, key):
    return ch[key[0]][key[1]] if isinstance(key, tuple) else ch[key]


def _table(sizes, cell):
    lines = [
        f"\\begin{{tabular}}{{|l|{'c|' * len(sizes)}}}", "\\hline",
        "\\textbf{Характеристика} & " + " & ".join(str(n) for n in sizes) + " \\\\ \\hline",
    ]
    for title, key, d in ROWS:
        lines.append(f"{title} & " + " & ".join(cell(n, key, d) for n in sizes) + " \\\\ \\hline")
    lines.append("\\end{tabular}")
    return "\n".join(lines)


def form_values(sizes, chars):
    return _table(sizes, lambda n, key, d: num(_get(chars[n], key), d))


def form_deviations(sizes, chars, refs):
    return _table(sizes, lambda n, key, d: num(abs(rel_dev(_get(chars[n], key), _get(refs[n], key))), 2) + "\\%")


def form_acf(acf_given, acf_gen):
    lines = [
        "\\begin{tabular}{|c|c|c|c|}", "\\hline",
        "\\textbf{Сдвиг} & \\textbf{Исходная ЧП} & \\textbf{Сгенерированная ЧП} & \\textbf{Различие, \\%} \\\\ \\hline",
    ]
    for k, (a, g) in enumerate(zip(acf_given, acf_gen), 1):
        lines.append(f"{k} & {num(a, 4)} & {num(g, 4)} & {num(abs(rel_dev(g, a)), 1)}\\% \\\\ \\hline")
    lines.append("\\end{tabular}")
    return "\n".join(lines)

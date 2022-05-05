from copy import deepcopy

from printers.printer import Printer
from solvers.simplex_table import SimplexTable


# Решает задачу максимизации в канонической форме с начальным базисом, найденным вручную
def simplex_basic(problem: SimplexTable, printer: Printer):
    s = deepcopy(problem)

    while not simplex_is_optimal(s):
        simplex_iterate(s, printer)
    printer.print_table(s)

    return s


# Упорядочивание плана
def simplex_reorder_plan(s: SimplexTable):
    for j in range(s.n):
        if (j + 1) in s.basis:
            s.x[j] = s.b[s.basis.index(j + 1)]
        else:
            s.x[j] = 0


# Подсчёт целевой функции
def simplex_calc_w(s: SimplexTable):
    s.w = 0

    for j in range(s.n):
        s.w += s.c[j] * s.x[j]


# Критерий оптимальности. Подсчёт оценок
def simplex_is_optimal(s: SimplexTable):
    for j in range(s.n):
        z = 0
        for i in range(s.m):
            z += s.a[i][j] * s.c[s.basis[i] - 1]
        s.d[j] = z - s.c[j]

    # Оптимально, если отрицательных оценок нет
    return not has_negatives(s.d)


# Итерация симплекс-метода (переразрешение)
def simplex_iterate(s: SimplexTable, printer):
    # Поиск разрешающих столбца и строки
    # Проверка на условие неотрицательности столбца b
    if has_negatives(s.b):
        s.flag_bfs = True

        # Базисное решение не опорно - поиск разрешающих столбца и строки по алгоритму спуска на область
        p_j = simplex_bfs_pivot_j(s)
        p_i = simplex_bfs_pivot_i(s, p_j)
    else:
        s.flag_bfs = False

        p_j = simplex_pivot_j(s)
        p_i = simplex_pivot_i(s, p_j)

    printer.print_table(s)

    # Включение в базис переменной на место исключаемой
    s.basis[p_i] = p_j + 1
    simplex_gauss(s, p_i, p_j)

    simplex_reorder_plan(s)
    simplex_calc_w(s)

    s.iter += 1


# Алгоритм спуска на область. Поиск разрешающего столбца
def simplex_bfs_pivot_j(s: SimplexTable):
    # Выбор в столбце b минимального отрицательного элемента
    b_min = 0
    b_min_i = None
    for i in range(s.m):
        if s.b[i] < b_min:
            b_min = s.b[i]
            b_min_i = i

    # Выбор минимального отрицательного элемента в соответствующей строке
    a_min = 0
    a_min_j = None
    for j in range(s.m):
        if s.a[b_min_i][j] < a_min:
            a_min = s.a[b_min_i][j]
            a_min_j = j
    if a_min_j is None:
        raise ValueError('Нет решения ЗЛП')

    return a_min_j


# Алгоритм спуска на область. Поиск разрешающей строки
def simplex_bfs_pivot_i(s: SimplexTable, p_j):
    # Выбор в разрешающем столбце элементов, имеющих одинаковый знак с соответствующим b
    # Поиск отношений. Выбор минимального отношения
    theta_min = 100_000_000
    theta_min_i = None

    for i in range(s.m):
        if same_sign(s.a[i][p_j], s.b[i]) and s.a[i][p_j] != 0:
            s.theta[i] = s.b[i] / s.a[i][p_j]

            if s.theta[i] < theta_min:
                theta_min = s.theta[i]
                theta_min_i = i
        else:
            s.theta[i] = None

    return theta_min_i


# Определение включаемой в базис переменной. Поиск разрешающего столбца
def simplex_pivot_j(s: SimplexTable):
    # Выбор наибольшей по модулю отрицательной оценки
    d_min = 0
    d_min_j = None

    for j in range(s.n):
        if s.d[j] < d_min:
            d_min = s.d[j]
            d_min_j = j

    return d_min_j


# Определение исключаемой из базиса переменной (условие допустимости). Поиск разрешающей строки
def simplex_pivot_i(s: SimplexTable, p_j):
    # Выбор неотрицательных элементов в разрешающем столбце
    # Поиск отношений. Выбор минимального положительного отношения

    theta_min = 100_000_000
    theta_min_i = None

    for i in range(s.m):
        if s.a[i][p_j] > 0:
            s.theta[i] = s.b[i] / s.a[i][p_j]

            if s.theta[i] < theta_min:
                theta_min = s.theta[i]
                theta_min_i = i
        else:
            s.theta[i] = None

    return theta_min_i


# Процедура однократного замещения по методу Гаусса-Жордана
def simplex_gauss(s: SimplexTable, p_i, p_j):
    p_e = s.a[p_i][p_j]

    # Преобразование разрешающей строки
    for j in range(s.n):
        s.a[p_i][j] /= p_e
    s.b[p_i] /= p_e

    # Преобразование прочих строк
    for i in range(s.m):
        if i == p_i:
            continue
        p_a = s.a[i][p_j]
        for j in range(s.n):
            s.a[i][j] -= p_a * s.a[p_i][j]
        s.b[i] -= p_a * s.b[p_i]


def has_negatives(x):
    return min(x) < 0


def same_sign(x, y):
    return x >= 0 and y >= 0 or x < 0 and y < 0

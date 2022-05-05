import math
from copy import deepcopy

from printers.printer import Printer
from solvers.simplex_table import SimplexTable
from solvers.simplex_basic import simplex_iterate


# Решает целочисленную ЗЛП на основе предварительно полученной симплекс-таблицы
def simplex_gomory(problem: SimplexTable, printer: Printer):
    if gomory_is_integer_plan(problem):
        return problem

    s = deepcopy(problem)
    s.iter += 1

    while not gomory_is_integer_plan(s):
        s.flag_gomory = True
        gomory_add_constraint(s)
        simplex_iterate(s, printer)

    s.flag_bfs = False
    s.flag_gomory = False
    printer.print_table(s)
    return s


# Проверка плана на целочисленность
def gomory_is_integer_plan(s: SimplexTable):
    for j in range(s.n):
        if not is_integer(s.x[j]):
            return False

    return True


# Добавление нового ограничения
def gomory_add_constraint(s: SimplexTable):
    # Поиск наибольшей дробной части в столбце b
    bfrac_max = 0
    bfrac_max_i = None

    for i in range(s.m):
        bfrac = modf(s.b[i])

        if bfrac >= bfrac_max:
            bfrac_max = bfrac
            bfrac_max_i = i

    # Конструирование нового ограничения
    constraint = [0] * (s.n + 1)
    for j in range(s.n):
        constraint[j] = -modf(s.a[bfrac_max_i][j])
    constraint[s.n] = 1

    # Внесение нового ограничения. Расширение симплекс-таблицы
    for i in range(s.m):
        s.a[i].append(0)

    s.c.append(0)
    s.a.append(constraint)
    s.b.append(-bfrac_max)
    s.basis.append(s.n + 1)

    s.m += 1
    s.n += 1

    s.d.append(None)
    s.theta.append(None)
    s.x.append(None)


def modf(x):
    return x - math.floor(x)


def is_integer(x):
    return "{0:.3f}".format(float(x)).split('.')[1] == '000'

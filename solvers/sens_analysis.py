from copy import deepcopy

from printers.printer import Printer
from solvers.simplex_table import SimplexTable
from solvers.simplex_basic import simplex_basic


def sens_analysis(solution: SimplexTable, problem: SimplexTable, b_constraints, printer: Printer):
    db = [0] * len(b_constraints)
    dw = [0] * len(b_constraints)
    y = [0] * len(b_constraints)

    for i in b_constraints:
        # Увеличить запас i-го ресурса в оригинальной задаче и решить её
        new_solution = deepcopy(problem)
        new_solution.b[i] += 1_000_000
        new_solution = simplex_basic(new_solution, printer=Printer())

        new_b = 0
        for j in range(problem.n - problem.m):
            new_b += problem.a[i][j] * new_solution.x[j]

        db[i] = new_b - problem.b[i]
        dw[i] = new_solution.w - solution.w
        y[i] = dw[i] / db[i] if db[i] != 0 else 0

    printer.print_analysis(db, dw, y)

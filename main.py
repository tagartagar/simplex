from printers.text_printer import TextPrinter
from solvers.simplex_basic import simplex_basic
from solvers.simplex_gomory import simplex_gomory
from solvers.sens_analysis import sens_analysis
from printers.printer import *
from printers.html_printer import HtmlPrinter

testproblem = SimplexTable(
    c=[2, 3, 4, 5, 0, 0, 0, 0, 0, 0, 0],
    a=[
        [0.5, 2, 1, 4,  1, 0, 0, 0, 0, 0, 0],
        [3, 4, 2, 1,    0, 1, 0, 0, 0, 0, 0],
        [1, 5, 3, 2,    0, 0, 1, 0, 0, 0, 0],
        [-1, 0, 0, 0,   0, 0, 0, 1, 0, 0, 0],
        [0, -1, 0, 0,   0, 0, 0, 0, 1, 0, 0],
        [0, 0, -1, 0,   0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, -1,   0, 0, 0, 0, 0, 0, 1]
    ],
    b=[10000, 90000, 110000, -2000, -1300, -1500, -1000],
    basis=[5, 6, 7, 8, 9, 10, 11]
)

problem = SimplexTable(
    c=[60, 25, 140, 160, 0, 0, 0, 0, 0, 0, 0],
    a=[
        [5, 1, 12, 15, 1, 0, 0, 0, 0, 0, 0],
        [3, 2, 6, 5, 0, 1, 0, 0, 0, 0, 0],
        [7, 5, 10, 12, 0, 0, 1, 0, 0, 0, 0],
        [-1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, -1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, -1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]
    ],
    b=[1500, 1000, 3200, -40, 120, -20, 20],
    basis=[5, 6, 7, 8, 9, 10, 11]
)

printer = HtmlPrinter(filename='Report.html')

solution = simplex_basic(problem, printer=printer)
simplex_gomory(solution, printer=printer)
sens_analysis(solution=solution, problem=problem, b_constraints=[0, 1, 2], printer=printer)

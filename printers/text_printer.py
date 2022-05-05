from printers.printer import Printer
from solvers.simplex_table import SimplexTable

COL_LEN = 11


def column(s, col_count=1):
    print(str(s).ljust(COL_LEN * col_count, ' '), end='')


def delimiter(n):
    print('\n' + '-' * COL_LEN * (3 + n + 2))


def number(num):
    return "{0:.2f}".format(num) if num is not None else ''


class TextPrinter(Printer):
    def print_table(self, s: SimplexTable):
        print()

        if s.iter != 0:
            column('ИТЕРАЦИЯ')
            column(s.iter)
        else:
            column('ИСХОДНЫЙ ВИД', 2)
        column("Cj ->")
        for c in s.c:
            column(c)
        if s.flag_bfs:
            column('+ПоискБОР')
        if s.flag_gomory:
            column('+Гомори')
        delimiter(s.n)

        column('Nогр')
        column('Nбаз')
        column('Cбаз')
        for j in range(s.n):
            column('A' + str(j + 1))
        column('B')
        column('Theta')
        delimiter(s.n)

        for i in range(s.m):
            column(i + 1)
            column(s.basis[i])
            column(s.c[s.basis[i] - 1])

            for j in range(s.n):
                column(number(s.a[i][j]))

            column(number(s.b[i]))
            column(number(s.theta[i]))

            if i != s.m - 1:
                print()
        delimiter(s.n)

        column(' ', 2)
        column('D ->')
        for j in range(s.n):
            column(number(s.d[j]))
        column(number(s.w))
        delimiter(s.n)

        column(' ', 2)
        column('X ->')
        for j in range(s.n):
            column(number(s.x[j]))
        print()

    def print_analysis(self, db, dw, y):
        print('\nАНАЛИЗ НА ЧУВСТВИТЕЛЬНОСТЬ')

        print('-' * COL_LEN * (2 * 3 + 2 + 2))
        column('Ресурс')
        column('Статус')
        column('Макс. изм-е запаса (dB)', 3)
        column('Макс. изм-е прибыли (dW)', 3)
        column('Теневая цена (y)', 2)
        print('\n' + '-' * COL_LEN * (2 * 3 + 2 + 2))

        for i in range(len(db)):
            column(i + 1)
            column('деф.' if y[i] != 0 else 'н/д')
            column(number(db[i]), 3)
            column(number(dw[i]), 3)
            column(number(y[i]), 2)
            print()

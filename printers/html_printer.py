from solvers.simplex_table import SimplexTable
from printers.text_printer import number


class HtmlPrinter:
    def __init__(self, filename):
        self.f = open(filename, 'w', encoding='utf-8')
        self.header()

    def __del__(self):
        self.footer()
        self.f.close()

    def print_table(self, s: SimplexTable):
        self.tag_open('table', hclass='simplex-table')

        self.row_open()
        self.cell('ИТЕРАЦИЯ %i' % s.iter if s.iter != 0 else 'ИСХОДНЫЙ ВИД', colspan=2, hclass='simplex-table-iter')
        self.cell('Cj &rarr;', hclass='simplex-table-text')
        for c in s.c:
            self.cell(c)
        flags = ''
        if s.flag_bfs:
            flags += 'Поиск БОР<br>'
        if s.flag_gomory:
            flags += 'Гомори<br>'
        self.cell(flags, colspan=2, hclass='simplex-table-flags')
        self.row_close()

        self.row_open(hclass='simplex-table-header')
        self.cell('№ огр')
        self.cell('№ баз')
        self.cell('C баз')
        for j in range(s.n):
            self.cell('A' + str(j + 1))
        self.cell('B')
        self.cell('&Theta;')
        self.row_close()

        for i in range(s.m):
            self.row_open()
            self.cell(i + 1)
            self.cell(s.basis[i])
            self.cell(s.c[s.basis[i] - 1])

            for j in range(s.n):
                self.cell(number(s.a[i][j]))

            self.cell(number(s.b[i]))
            self.cell(number(s.theta[i]))
            self.row_close()

        self.row_open()
        self.cell('D &rarr;', colspan=3, hclass='simplex-table-stub')
        for j in range(s.n):
            self.cell(number(s.d[j]))
        self.cell(number(s.w), colspan=2, rowspan=2, hclass='simplex-table-w')
        self.row_close()

        self.row_open()
        self.cell('X &rarr;', colspan=3, hclass='simplex-table-stub')
        for j in range(s.n):
            self.cell(number(s.x[j]))
        self.row_close()

        self.tag_close('table')

    def print_analysis(self, db, dw, y):
        self.f.write('<h2>Анализ на чувствительность</h2>')

        self.tag_open('table', hclass='analysis-table')

        self.row_open(hclass='analysis-table-header')
        self.cell('Ресурс')
        self.cell('Статус')
        self.cell('Максимальное изменение запаса (&Delta;B)')
        self.cell('Максимальное изменение прибыли (&Delta;W)')
        self.cell('Теневая цена')
        self.row_close()

        for i in range(len(db)):
            self.row_open()
            self.cell(i + 1)
            self.cell('дефицитный' if y[i] != 0 else 'недефицитный')
            self.cell(number(db[i]))
            self.cell(number(dw[i]))
            self.cell(number(y[i]))
            self.row_close()

        self.tag_close('table')

    def header(self):
        self.tag_open('html')
        self.tag_open('head')
        self.tag_open('style')
        with open('printers/stylesheet.css', 'r') as stylesheet:
            self.f.write(stylesheet.read())
        self.tag_close('style')
        self.f.write('<title>Приложение А - Симплекс-таблицы</title>')
        self.tag_close('head')
        self.tag_open('body')
        self.tag_open('main')
        self.f.write('<h2>Приложение А</h2>')
        self.tag_open('h2')
        self.f.write('<h1>Симплекс-таблицы</h1>')
        self.tag_close('h2')

    def footer(self):
        self.tag_close('main')
        self.tag_close('body')
        self.tag_close('html')

    def tag_open(self, tag, **kwargs):
        html = '<%s' % tag

        for k, v in kwargs.items():
            if k == 'hclass':
                k = 'class'

            html += ' %s="%s"' % (k, v)

        html += '>'

        self.f.write(html)

    def tag_close(self, tag):
        self.f.write('</%s>' % tag)

    def row_open(self, **kwargs):
        self.tag_open('tr', **kwargs)

    def row_close(self):
        self.tag_close('tr')

    def cell(self, value, **kwargs):
        self.tag_open('td', **kwargs)
        self.f.write(str(value))
        self.tag_close('td')

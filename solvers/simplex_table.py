class SimplexTable:
    def __init__(self, c, a, b, basis):
        n = len(c)
        m = len(b)

        if len(a) != m:
            raise ValueError('Число строк a не равна длине b (m)')
        for i in range(m):
            if len(a[i]) != n:
                raise ValueError('Длина строки a[{0}] не равна длине строки c (n)'.format(i))
        if len(basis) != m:
            raise ValueError('Длина начального базиса не равна длине b (m)')

        self.c = c
        self.a = a
        self.b = b
        self.basis = basis

        self.n = n
        self.m = m

        self.d = [None] * n
        self.theta = [None] * m
        self.x = [None] * n
        self.w = None

        self.iter = 0
        self.flag_bfs = False
        self.flag_gomory = False

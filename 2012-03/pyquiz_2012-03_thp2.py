
# http://www.pyug.at/PythonQuiz/2012-03
# <m@thp.io>'s solution, variant 2

import fileinput
import functools
import operator

a = [((1+4*(i%2))*10**(i//2), c) for i, c in enumerate('IVXLCDM')]
s = [(a[x+1][0]-a[x//2*2][0], a[x//2*2][1]+a[x+1][1]) for x in range(6)]

def convert(x):
    n = x.isdigit()
    if n: x = int(x)
    for av, rv in sorted(a+s, reverse=True):
        while (n and x >= av) or (not n and x.startswith(rv)):
            yield (rv if n else av)
            x = ((x - av) if n else x[len(rv):])

for line in filter(None, map(lambda x: x.strip(), fileinput.input())):
    print(functools.reduce(operator.add, convert(line)))


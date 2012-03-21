# pyquiz_2012-03_thp9_cute.py
# Thomas Perl <m@thp.io>; 2012-03-21

from functools import reduce


PAIRS = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
    (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
    (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
]

def step(state, pair):
    remainder, result = state
    arabic, roman = pair

    while remainder >= arabic:
        remainder -= arabic
        result += roman

    return remainder, result

print 'const char data[][] = {'
for arabic in range(1, 4000):
    remainder, result = reduce(step, PAIRS, (arabic, ''))
    print '    "%s",' % result
    #TRANSLATE.update({str(arabic): result, result: arabic})
print '};'


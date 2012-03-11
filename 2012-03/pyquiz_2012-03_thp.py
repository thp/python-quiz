
# http://www.pyug.at/PythonQuiz/2012-03
# <m@thp.io>'s solution

import sys

alpha = [
    (1, 'I'),
    (5, 'V'),
    (10, 'X'),
    (50, 'L'),
    (100, 'C'),
    (500, 'D'),
    (1000, 'M'),
]

# [(4, 'IV'), (9, 'IX'), (40, 'XL'), ...]
specials = [(alpha[x+1][0] - alpha[x//2*2][0],
             alpha[x//2*2][1] + alpha[x+1][1])
             for x in range(len(alpha)-1)]

alpha = sorted(alpha + specials, reverse=True)

def to_roman(arabic):
    for avalue, rvalue in alpha:
        while arabic >= avalue:
            yield rvalue
            arabic -= avalue

def to_arabic(roman):
    for avalue, rvalue in alpha:
        while roman.startswith(rvalue):
            yield avalue
            roman = roman[len(rvalue):]

for line in sys.stdin:
    try:
        print(''.join(to_roman(int(line))))
    except ValueError:
        print(sum(to_arabic(line)))


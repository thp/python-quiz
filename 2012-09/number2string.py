#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# number2string - Pretty-print numbers as string
# 2012-09-15 Thomas Perl <m@thp.io>
#

import fileinput

# '12341231.123123' -> split it at the '.'
# ['12341231', '123123'] -> the first part needs padding
# [pad('12341231'), '123123']
# ^^^^               ^^^
# '12.341.231'      '123123' -> ','.join()
# 12.341.231,123123


# '1234.123'
# [(0, '1234'), (1, '123')]
# '1234'
# pad([(0, '1'), (1, '2'), (2, '3'), (3, '4')], 4) -> '1.234'
# [(4, '1'), (3, '2'), (2, '3'), (1, '4')]
# [(1, '1'), (0, '2'), (2, '3'), (1, '4')]
#     1       .2        3            4

# msep * False + c -> msep * 0 + c -> c
# msep * True + c -> msep * 1 + c -> msep + c -> ".c"
# the "i and" takes care of avoiding '123' -> '.123'

# ['1.234', '123'] -> '1.234,123'

def number2string(number, msep='.', sep=','):
    # Support for "negative" numbers
    if number.startswith('-'):
        return '-' + number2string(number[1:], msep, sep)

    pad = lambda x, l: ''.join(msep*(i and (l-i)%3 == 0) + c for i, c in x)
    convert = lambda txt, pos: txt if pos else pad(enumerate(txt), len(txt))
    return sep.join(convert(a, i) for i, a in enumerate(number.split('.')))

def process(n):
    print '-> %s or %s' % (number2string(n), number2string(n, ',', '.'))

if __name__ == '__main__':
    for line in fileinput.input():
        process(line.strip())


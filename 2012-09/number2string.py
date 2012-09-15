#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# number2string - Pretty-print numbers as string
# 2012-09-15 Thomas Perl <m@thp.io>
#

import fileinput

def number2string(number, msep='.', sep=','):
    pad = lambda x, l: ''.join(msep*(i and (l-i)%3 == 0) + c for i, c in x)
    convert = lambda txt, pos: txt if pos else pad(enumerate(txt), len(txt))
    return sep.join(convert(a, i) for i, a in enumerate(number.split('.')))

def process(n):
    print '-> %s or %s' % (number2string(n), number2string(n, ',', '.'))

if __name__ == '__main__':
    for line in fileinput.input():
        process(line.strip())


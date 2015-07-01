import functools
import itertools
import pprint
import math
import time
import random

from pyug_20150618 import run as pyug_20150618_run


def cmp(a, b):
    return (a > b) - (a < b)


def bruteforce_best_number(l):
    return max(int(''.join(str(part) for part in permutation))
               for permutation in itertools.permutations(l))


def ziffernkette_pyugat_str(l):
    def cmpv(a, b):
        ab = str(a) + str(b)
        ba = str(b) + str(a)
        return cmp(ab, ba)
    return int(''.join(sorted([str(x) for x in l], key=functools.cmp_to_key(cmpv), reverse=True)))


def ziffernkette_pyugat_str_fast(l):
    def cmpv(a, b):
        ab = a + b
        ba = b + a
        return (ab > ba) - (ab < ba)
    return int(''.join(sorted([str(x) for x in l], key=functools.cmp_to_key(cmpv), reverse=True)))


def ziffernkette_pyugat_str_slow(l):
    def cmpv(a, b):
        ab = a + b
        ba = b + a
        return int(ab) - int(ba)
        if ab > ba:
            return 1
        elif ab < ba:
            return -1
        return 0
    return int(''.join(sorted([str(x) for x in l], key=functools.cmp_to_key(cmpv), reverse=True)))


def ziffernkette_pyugat_int(l):
    def cmpv(a, b):
        pow_a = 10 ** int(1 + math.log10(max(1, a)))
        pow_b = 10 ** int(1 + math.log10(max(1, b)))
        ab = a * pow_b + b
        ba = b * pow_a + a
        return cmp(ab, ba)
    return int(''.join(str(x) for x in sorted(l, key=functools.cmp_to_key(cmpv), reverse=True)))


def ziffernkette_pyugat_int_fast(l):
    def cmpv(a, b):
        pow_a = 10 ** int(1 + math.log10(max(1, a)))
        pow_b = 10 ** int(1 + math.log10(max(1, b)))
        ab = a * pow_b + b
        ba = b * pow_a + a
        return (ab > ba) - (ab < ba)
    return int(''.join(str(x) for x in sorted(l, key=functools.cmp_to_key(cmpv), reverse=True)))


funcs_to_test = [
    ziffernkette_pyugat_str,
    ziffernkette_pyugat_str_fast,
    ziffernkette_pyugat_str_slow,
    ziffernkette_pyugat_int,
    ziffernkette_pyugat_int_fast,
    pyug_20150618_run,
    bruteforce_best_number,
]

def test_correctness(l, expected=None):
    #print('l =', l)
    res = [(f, f(l)) for f in funcs_to_test]
    #pprint.pprint(res)
    vals = [value for func, value in res]
    #print('vals = ', vals)
    assert len(set(vals)) == 1, 'Different results'
    if expected is not None:
        assert vals[0] == expected, 'Unexpected value'
        return vals[0]
    else:
        return None

test_l = [
    ([5, 50], 550),
    ([5, 56], 565),
    ([50, 2, 1, 9], 95021),
    ([5, 50, 56], 56550),
    ([420, 42, 423], 42423420),
]

test_l.extend(([x, y], bruteforce_best_number([x, y]))
              for x in range(1, 101) for y in range(1, 101))

for x in range(1000):
    l = [random.randint(1, 10000) for y in range(5)]
    print(l)
    test_l.append((l, None))#bruteforce_best_number(l)))

print('Testing for correctness first')
for l, expected in test_l:
    assert test_correctness(l, expected) == expected
print('Correctness tests done')

def test_func(func):
    start = time.time()
    for i in range(100):
        for l, expected in test_l:
            func(l)
    end = time.time()
    return end - start

print('Testing performance')
for func in funcs_to_test:
    print(func, 'duration:', test_func(func))
print('Performance tests done')

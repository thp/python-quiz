# pyug.at/PythonQuiz/2012-03, m@thp.io

import sys

# Generate list, alternate between 1 and 5 and multiply by 10**(i/2)
a = [((1+4*(i%2))*10**(i/2), 'IVXLCDM'[i]) for i in range(7)]
# a = [(1, 'I'), (5, 'V'), (10, 'X'), (50, 'L'), (100, 'C'), ...]

# Add "special cases": 5-1, 10-1, 50-10, 100-10, 500-100, 1000-100
a += [(a[x+1][0]-a[x/2*2][0], a[x/2*2][1]+a[x+1][1]) for x in range(6)]
# a = [..., (4, 'IV'), (9, 'IX'), (40, 'XL'), (90, 'XC'), ...]

def c(x, n):
    # Convert the argument to an int (for arabic->roman)
    if n: x = int(x)

    # Iterate over all (arabic, roman) pairs, biggest values first
    for y, z in reversed(sorted(a)):
        # As long as we can "eat" the current value from the input value..
        while (n and x >= y) or (not n and x.startswith(z)):
            # ..yield the corresponding value of the current pair..
            yield (n and z or y)
            # ..and decrease the input value by the yielded value.
            x = ((x-y) if n else x[len(z):])

# Read lines from stdin, strip whitespace + filter empty lines
for x in filter(None, map(str.strip, sys.stdin)):
    # convert (using "c") the input line, then reduce the result via "+"
    # this works both for int (1000+10+1+1) and for str ('M'+'X'+'I'+'I')
    print reduce(lambda d, e: d+e, c(x, x.isdigit()))


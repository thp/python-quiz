def a(lines, e=enumerate, r=range):
    w = [[(x, y, v == '*') for x, v in e(row)] for y, row in e(lines)]
    return '\n'.join(''.join('*' if c[2] else str(sum(x[2] for x in [w[y][x]
        for y in r(max(0, c[1]-1), min(len(w), c[1]+2)) for x in r(max(0,
            c[0]-1), min(len(w[y]), c[0]+2))])) for c in row) for row in w)
def minisweeper(f, y=True):
    while y:
        y = [int(n) for n in (f.readline() or '0 0').split()][0]
        print(a(list(f.readline().strip()) for _ in range(y)))
minisweeper(open((__import__('sys').argv[1:] + ['input.txt'])[0]))

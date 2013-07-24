class Cell:
    def __init__(self, area, x, y, value):
        self.area, self.x, self.y, self.mine = area, x, y, (value == '*')

    def ch(self):
        return '*' if self.mine else str(sum(c.mine for c in
            self.area.adjacent(self.x, self.y)))

class Area:
    def __init__(self, lines):
        self.c = [[Cell(self, x, y, v) for x, v in enumerate(row)]
                for y, row in enumerate(lines)]

    def solve(self):
        return '\n'.join(''.join(c.ch() for c in row) for row in self.c)

    def adjacent(self, cx, cy):
        return [self.c[y][x] for y in range(max(0, cy-1), min(len(self.c),
            cy+2)) for x in range(max(0, cx-1), min(len(self.c[y]), cx+2))]

def area_factory(fileobj, rows=True):
    while rows:
        header = fileobj.readline() or '0 0'
        rows, columns = (int(x) for x in header.split())
        yield Area([list(fileobj.readline().strip()) for _ in range(rows)])

print('\n\n'.join(area.solve() for area in area_factory(open('input.txt'))))

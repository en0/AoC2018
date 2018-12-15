from multiprocessing import cpu_count, Pool
from sys import maxsize


def main():
    sn = get_serial("input")
    t = SummedAreaTable(300, sn)
    print("Part 1:", part1(t))
    print("Part 2:", part2(t))


def part1(table):
    _, _, point = find_max_with_size(table, 3)
    return "{},{}".format(*point)


def part2(table):
    _, size, point = find_max(table)
    return "{},{},{}".format(*point, size)


def find_max(table):
    with Pool(cpu_count()) as p:
        args = [(table, x) for x in range(1, 300)]
        result = p.starmap(find_max_with_size, args)
    return max(result)


def find_max_with_size(table, size):
    m, p = -maxsize, None
    for x in range(1, (table.size + 1) - size):
        for y in range(1, (table.size + 1) - size):
            v = table.get_value((x, y), size)
            m, p = max([(m, p), (v, (x, y))])
    return m, size, p


def get_serial(path):
    with open(path, 'r') as fd:
        return int(fd.read())


class SummedAreaTable():
    """Computed Summed Area Table

    Computes a Summed Area Table for a square matrix whos values are defined by
    a given Serial Number.

    NOTE:
        Externally x and y are expected to be 1 based.
        Internally they are 0 based.
    """

    def __init__(self, size, sn):
        self.sn = sn
        self.size = size
        self.table = []
        for i in range(self.size):
            self.table.append([None] * self.size)
        self._compile()

    def dumps(self):
        """Dumpt the integral table to a string"""
        ret = []
        for y in range(self.size):
            for x in range(self.size):
                ret.append("{0: >4} ".format(self._get((x, y))))
            ret.append("\n")
        return "".join(ret)

    def get_value(self, p, s):
        """Get the sum of values in a rectangled defined by size s at point p.

        IMPORTANT: It is assumed that p references a 1 based index.

        Example:

        In the given table below:
        - (1, 1) has a value of 0.
        - (3, 3) has a value of 8

        0 1 2
        3 4 5
        6 7 8
        """
        x, y = p[0] - 2, p[1] - 2
        a = self._get((x, y))
        b = self._get((x + s, y + s))
        c = self._get((x, y + s))
        d = self._get((x + s, y))
        return a + b - c - d

    def _compile(self):
        for _x in range(self.size):
            for _y in range(self.size):
                s = self._power_at((_x, _y))
                s += self._get((_x - 1, _y)) if _x > 0 else 0
                s += self._get((_x, _y - 1)) if _y > 0 else 0
                s -= self._get((_x - 1, _y - 1)) if _y > 0 < _x else 0
                self._set((_x, _y), s)

    def _power_at(self, p):
        x, y = p
        rack_id = x + 1 + 10
        power_level = (rack_id * (y + 1) + self.sn) * rack_id // 100 % 10
        return power_level - 5

    def _set(self, p, val):
        x, y = p
        self.table[y][x] = val

    def _get(self, p):
        x, y = p
        if x < 0 or y < 0:
            return 0
        return self.table[y][x]


if __name__ == "__main__":
    main()

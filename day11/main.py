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
    m, s, p = -maxsize, None, None
    args = [(table, x) for x in range(1, 300)]
    with Pool(cpu_count() * 2) as p:
        result = p.starmap(find_max_with_size, args)
    for _m, _s, _p in result:
        if _m > m:
            m, s, p = _m, _s, _p
    return m, s, p


def find_max_with_size(table, size):
    m, p = -maxsize, None
    for x in range(1, (table.size + 1) - size):
        for y in range(1, (table.size + 1) - size):
            v = table.get_value((x, y), size)
            if v > m:
                p, m = (x, y), v
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
        self.table = [None] * self.size
        for i in range(len(self.table)):
            self.table[i] = [None] * self.size
        self._compile()

    def dumps(self):
        """Dumpt the integral table to a string"""
        ret = []
        for y in range(self.size):
            for x in range(self.size):
                ret.append("{0: >4} ".format(self._get_value_at((x, y))))
            ret.append("\n")
        return "".join(ret)

    def get_value(self, p, s):
        """It is assumed that p references a 1 based index"""
        x, y = p[0] - 1, p[1] - 1
        x1, y1 = x - 1, y - 1
        x2, y2 = x1 + s, y1 + s
        a = self._get_value_at((x1, y1))
        b = self._get_value_at((x2, y2))
        c = self._get_value_at((x1, y2))
        d = self._get_value_at((x2, y1))
        return a + b - c - d

    def _compile(self):
        for _x in range(self.size):
            for _y in range(self.size):
                s = self._power_at((_x, _y))
                if _x > 0:
                    s += self._get_value_at((_x - 1, _y))
                if _y > 0:
                    s += self._get_value_at((_x, _y - 1))
                if _x > 0 and _y > 0:
                    s -= self._get_value_at((_x - 1, _y - 1))
                self._set_value_at((_x, _y), s)

    def _power_at(self, p):
        x, y = p
        rack_id = x + 1 + 10
        power_level = (rack_id * (y + 1) + self.sn) * rack_id // 100 % 10
        return power_level - 5

    def _set_value_at(self, p, val):
        x, y = p
        self.table[y][x] = val

    def _get_value_at(self, p):
        x, y = p
        if x < 0 or y < 0:
            return 0
        return self.table[y][x]


if __name__ == "__main__":
    main()

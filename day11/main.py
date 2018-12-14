from sys import maxsize
from multiprocessing import Pool


def get_serial(path):
    with open(path, 'r') as fd:
        return int(fd.read())


SERIAL = get_serial("input")


def main():
    print("Part 1:", brute_part1())
    print("Part 2:", brute_part2())


def brute_part1():
    _, _, p = brute_value(3)
    return p


def brute_part2():
    """This is most definatly a bad idea"""

    m, s, p = -maxsize, None, None
    with Pool(8) as p:
        result = p.map(brute_value, range(1, 301))
    for _m, _s, _p in result:
        if _m > m:
            m = _m
            s = _s
            p = _p

    x, y = p
    return x, y, s


def brute_value(size):
    """I think this is the nature of the issue.
    This needs to be O(1) to solve the puzzle in a reasonable time.
    """
    m = -maxsize
    p = None
    for y in range(1, 301 - size):
        for x in range(1, 301 - size):
            s = 0
            for _y in range(y, y + size):
                for _x in range(x, x + size):
                    s += power_at((_x, _y), SERIAL)
            if s > m:
                m = s
                p = (x, y)
    return m, size, p


def power_at(p, sn):
    x, y = p
    rack_id = x + 10
    power_level = (rack_id * y + sn) * rack_id // 100 % 10
    return power_level - 5


if __name__ == "__main__":
    main()

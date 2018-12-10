import re
from sys import stdout, maxsize


class Vector():
    def __init__(self, location, velocity):
        self.loc = location
        self.vel = velocity

    def __repr__(self):
        return "({}, {}) -> ({}, {})".format(*self.loc, *self.vel)

    def get_position(self, t):
        x = (self.vel[0] * t) + self.loc[0]
        y = (self.vel[1] * t) + self.loc[1]
        return x, y

    def get_position_as_vector(self, t):
        x = (self.vel[0] * t) + self.loc[0]
        y = (self.vel[1] * t) + self.loc[1]
        return Vector((x, y), self.vel)


def part1(vectors):
    for i in range(1, 5):
        vector_set = set()
        left_top = (maxsize, maxsize)
        right_bottom = (-1*maxsize, -1*maxsize)
        for vec in vectors:
            vec = vec.get_position_as_vector(i)
            left_top = pmin(vec.loc, left_top)
            right_bottom = pmax(vec.loc, right_bottom)
            vector_set.add(vec.loc)
        show(vector_set, left_top, right_bottom, stdout)


def main():
    path = "sample"
    vectors = [x for x in get_data(path)]
    print("Part 1", part1(vectors))


def get_data(path):
    with open(path, "r") as fd:
        for line in fd:
            loc, vel = re.findall(r"<[0-9,\ -]*>", line)
            yield Vector(
                tuple([int(x) for x in loc[1:-1].split(",")]),
                tuple([int(x) for x in vel[1:-1].split(",")]))


def pmin(a, b):
    return min(a[0], b[0]), min(a[1], b[1])


def pmax(a, b):
    return max(a[0], b[0]), max(a[1], b[1])


def show(vectors, min_point, max_point, fd):
    (min_x, min_y), (max_x, max_y) = min_point, max_point
    for y in range(min_y-1, max_y+2):
        for x in range(min_x-1, max_x+2):
            if (x, y) in vectors:
                fd.write("█")
            else:
                fd.write("░")
        fd.write("\n")
    fd.write("\n")


if __name__ == "__main__":
    main()

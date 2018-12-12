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

    last_area = 0
    is_shrinking = False
    last_vector_set = None
    last_left_top = None
    last_right_bottom = None

    stdout.write("Working: [")
    stdout.flush()

    for i in range(0, 50000):

        if i % 1000 == 0:
            stdout.write("=")
            stdout.flush()

        left_top = (maxsize, maxsize)
        right_bottom = (-1*maxsize, -1*maxsize)
        vector_set = set()
        for vec in vectors:
            vec = vec.get_position_as_vector(i)
            left_top = pmin(vec.loc, left_top)
            right_bottom = pmax(vec.loc, right_bottom)
            vector_set.add(vec.loc)

        (lx, ly), (rx, ry) = left_top, right_bottom
        area = (rx - lx) * (ry - ly)

        if last_area > area:
            is_shrinking = True
        elif is_shrinking:
            stdout.write("] DONE\n")
            return draw(last_vector_set, last_left_top, last_right_bottom), i-1

        last_vector_set = vector_set
        last_left_top, last_right_bottom = left_top, right_bottom
        last_area = area


def main():
    path = "input"
    vectors = [x for x in get_data(path)]
    disp, t = part1(vectors)
    print("Part 1:\n{}".format(disp))
    print("Part 2:", t)


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


def draw(vectors, min_point, max_point):
    (min_x, min_y), (max_x, max_y) = min_point, max_point
    ret = []
    for y in range(min_y-1, max_y+2):
        ret.append("")
        for x in range(min_x-1, max_x+2):
            if (x, y) in vectors:
                ret[-1] += "█"
            else:
                ret[-1] += "░"
    return "\n".join(ret)


if __name__ == "__main__":
    main()

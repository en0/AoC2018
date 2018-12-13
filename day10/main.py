import re
from sys import maxsize


def main():
    path = "input"
    vectors = [x for x in get_data(path)]
    disp, t = get_message(vectors, 1000, 50000)
    print("Part 1:\n{}".format(disp))
    print("Part 2:", t)


def get_message(vectors, start, end):
    """Locate the message.

    Use a modifed binary search to find a local minimium - The nature
    of the data should have only one local minium so we will assume that
    is the point at which the message exists.

    Arguments:
        vectors: A list of Vector objects.
        start: The point in time to start searching for the message.
        end: The last point in time worth searching for the message.

    Returns:
        tuple:
            0: The rendered field.
            1: The offset that was used to render the field.
    """

    _start = start
    _end = end

    while _start < _end:

        mp = _start + (_end - _start) // 2

        vs_left = transform_vectors(vectors, mp - 1)
        vs = transform_vectors(vectors, mp)
        vs_right = transform_vectors(vectors, mp + 1)

        if vs_left["area"] < vs["area"]:
            _end = mp
        elif vs_right["area"] < vs["area"]:
            _start = mp
        else:
            return draw(vs), mp


def transform_vectors(vectors, offset):
    """Create a set of vector locations at the given time offset.

    Returns:
        area: The number of elements in the containing rectangle
        left_top: Left, top most corner of the containing rectangle
        bottom_right: Bottom, right most corner of the containing rectangle
        vector_set: A set() with all the point location for the given offset
    """
    left_top = (maxsize, maxsize)
    right_bottom = (-1*maxsize, -1*maxsize)
    vector_set = set()
    for vec in vectors:
        vec = vec.get_position_as_vector(offset)
        left_top = pmin(vec.loc, left_top)
        right_bottom = pmax(vec.loc, right_bottom)
        vector_set.add(vec.loc)
    (lx, ly), (rx, ry) = left_top, right_bottom
    return {
        "area": (rx - lx) * (ry - ly),
        "left_top": left_top,
        "right_bottom": right_bottom,
        "vector_set": vector_set}


def get_data(path):
    """Read in datafile load vector objects."""
    with open(path, "r") as fd:
        for line in fd:
            loc, vel = re.findall(r"<[0-9,\ -]*>", line)
            yield Vector(
                tuple([int(x) for x in loc[1:-1].split(",")]),
                tuple([int(x) for x in vel[1:-1].split(",")]))


def pmin(a, b):
    """Return top, left corner of the rect containing the given points."""
    return min(a[0], b[0]), min(a[1], b[1])


def pmax(a, b):
    """Return bottom, right corner of the rect containing the given points."""
    return max(a[0], b[0]), max(a[1], b[1])


def draw(field):
    """Render the given field as a string.

    Arguments:
        Field:
            left_top: A tuple representing the left top most point in the field
            right_bottom: A tuple representing the right bottom most point
            vector_set: A set() of points, one for each vector
    """

    vectors = field["vector_set"]
    min_point = field["left_top"]
    max_point = field["right_bottom"]

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


class Vector():
    """Represents a moving point"""

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


if __name__ == "__main__":
    main()

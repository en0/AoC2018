from sys import maxsize


def main():

    limit, path = 10000, "input"
    # limit, path = 32, "sample"

    points = [p for p in lines(path)]
    print("PART 1:", part1(points))
    print("PART 2:", part2(points, limit))


def part1(points):
    """Find the largest non-infinite area"""

    (min_x, min_y), (max_x, max_y) = find_board(points)

    vals = dict()
    exclude = set()

    # Find the nearest location for each point in the known board
    for y in range(min_y - 1, max_y + 2):
        for x in range(min_x - 1, max_x + 2):
            n = find_nearest((x, y), points)

            if n is None:
                continue

            vals.setdefault(n, []).append((x, y))

            nx, ny = n
            if nx == min_x or nx == max_x:
                exclude.add(n)

            elif ny == min_y or ny == max_y:
                exclude.add(n)

    # Find the point with the largest area
    largest_area = -1
    for candidate, value in vals.items():
        if candidate in exclude:
            continue
        largest_area = max(largest_area, len(value))

    return largest_area


def part2(points, limit):
    """Find points who is less then n from all other locations."""

    r = 0
    (min_x, min_y), (max_x, max_y) = find_board(points)

    # Find the nearest location for each point in the known board
    for y in range(min_y - 1, max_y + 2):
        for x in range(min_x - 1, max_x + 2):
            n = sum_distance((x, y), points)
            if n < limit:
                r += 1
    return r


def sum_distance(point, points):
    c = 0
    for p in points:
        c += taxi_distance(p, point)
    return c


def find_nearest(point, points):
    m = maxsize
    d = -1
    r = None
    for p in points:
        c = taxi_distance(p, point)
        if m == c:
            d = m
        elif m > c:
            m = c
            r = p
    return None if d == m else r


def find_board(points):
    # Assumed that all points are positive
    x_min, x_max = maxsize, -1
    y_min, y_max = maxsize, -1

    for x, y in points:
        x_min = min(x_min, x)
        x_max = max(x_max, x)
        y_min = min(y_min, y)
        y_max = max(y_max, y)

    return (x_min, y_min), (x_max, y_max)


def taxi_distance(a, b):
    (ax, ay), (bx, by) = a, b
    return abs(ax - bx) + abs(ay - by)


def lines(path):
    with open(path, "r") as fd:
        for line in fd.readlines():
            x, y = line[:-1].split(", ")
            yield (int(x), int(y))


if __name__ == "__main__":
    main()


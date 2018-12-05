def main():
    print("Part One:", find_overlap())
    print("Part Two:", find_not_overlap())


def find_not_overlap():
    """Find the claim that has no overlaps"""
    is_claimed_ids = set()
    has_conflict_ids = set()
    is_claimed = dict()

    for c in claims():
        _id, (offset_x, offset_y), (w, h) = c
        for x in range(offset_x, offset_x + w):
            for y in range(offset_y, offset_y + h):
                point = (x, y)
                if point in is_claimed:
                    has_conflict_ids.add(_id)
                    has_conflict_ids.add(is_claimed[point])
                else:
                    is_claimed[point] = _id
                    is_claimed_ids.add(_id)

    return is_claimed_ids.difference(has_conflict_ids).pop()


def find_overlap():
    """Find the units that overlap"""
    is_claimed = set()
    has_conflict = set()

    for c in claims():
        _id, (offset_x, offset_y), (w, h) = c
        for x in range(offset_x, offset_x + w):
            for y in range(offset_y, offset_y + h):
                point = (x, y)
                if point in is_claimed:
                    has_conflict.add(point)
                else:
                    is_claimed.add(point)

    return len(has_conflict)


def claims():
    with open("./input", "r") as fd:
        for claim in fd.readlines():
            yield decode_claim(claim)


def decode_claim(claim):
    _id, _, _offset, _size = claim.split(" ")
    offset_x, offset_y = [int(_) for _ in _offset[:-1].split(",")]
    w, h = [int(_) for _ in _size[:-1].split("x")]
    return _id[1:], (offset_x, offset_y), (w, h)


if __name__ == "__main__":
    main()


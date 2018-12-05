def main():
    print("Part One:", checksum())
    print("Part Two:", find_subset())


def find_subset():
    _max = -1
    _ret = None
    items = dict()
    for s in lines():
        for i in range(len(s)):
            key = s[:i] + s[i+1:]
            items.setdefault(key, set()).add(s)
            if len(items[key]) > _max:
                _max = len(items[key])
                _ret = key
    return _ret


def checksum():
    with2 = set()
    with3 = set()

    for s in lines():
        for c in set(s):
            if count_of(c, s) == 3:
                with3.add(s)
            if count_of(c, s) == 2:
                with2.add(s)

    return len(with2) * len(with3)


def count_of(c, s):
    return len([_ for _ in s if _ == c])


def lines():
    with open("./input", "r") as fd:
        for line in fd.readlines():
            yield decode_line(line)


def decode_line(line):
    return line[:-1]


if __name__ == "__main__":
    main()


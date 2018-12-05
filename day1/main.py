def main():
    print("Part One:", sum(lines()))
    print("Part Two:", search_for_duplicate())


def search_for_duplicate():
    state = 0
    state_seen = set([state])
    while True:
        for f in lines():
            state = state + f
            if state in state_seen:
                return state
            state_seen.add(state)


def lines():
    with open("./input", "r") as fd:
        for line in fd.readlines():
            yield decode_line(line)


def decode_line(line):
    val = int(line[1:-1])
    return val if line[0] == "+" else val * -1


if __name__ == "__main__":
    main()


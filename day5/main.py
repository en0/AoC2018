from multiprocessing import Pool
from os import cpu_count


def main():
    print("Part One:", react())
    with Pool(cpu_count() * 2) as p:
        print("Part Two:", min(p.map(react, "abcdefghijklmnopqrstuvwxyz")))


def react(extract=""):
    a = line()
    i = 0
    while i < len(a) - 1:
        if extract == a[i].lower():
            a = a[:i] + a[i+1:]
            i = max(i - 1, 0)
        if should_destruct(a[i], a[i+1]):
            a = a[:i] + a[i+2:]
            i = max(i - 1, 0)
        else:
            i += 1
    return len(a)


def should_destruct(a, b):
    return a.lower() == b.lower() and not a == b


def line():
    with open("input", "r") as fd:
        return fd.read()[:-1]


if __name__ == "__main__":
    main()

import re
from datetime import datetime, timedelta


class Nap():
    def __init__(self, start):
        self.start = start
        self.end = start
        self.duration = 0

    def wake_up(self, end):
        self.end = end
        span = self.end - self.start
        self.duration = int(span.total_seconds() / 60)

    def minutes(self):
        s = self.start
        while s < self.start + timedelta(minutes=self.duration):
            yield s
            s += timedelta(minutes=1)


class Guard():
    def __init__(self, ident):
        self.ident = ident
        self.sleep_time = 0
        self._nap = None
        self._minute_map = dict()
        self._minute_map_max = -1
        self._minute_map_max_key = None

    @property
    def score(self):
        if self._strategy == 1:
            return self.sleep_time
        elif self._strategy == 2:
            return self._minute_map_max

    def set_strategy(self, value):
        self._strategy = value

    def sleep(self, when):
        self._nap = Nap(when)

    def wake(self, when):
        self._nap.wake_up(when)
        self.sleep_time += self._nap.duration
        for m in self._nap.minutes():
            m = m.minute
            self._minute_map[m] = self._minute_map.get(m, 0) + 1
            if self._minute_map[m] > self._minute_map_max:
                self._minute_map_max = self._minute_map[m]
                self._minute_map_max_key = m

    def product(self):
        return self.ident * self._minute_map_max_key

    def __repr__(self):
        return "<Guard(ident={},sleep_time={})>".format(
            self.ident, self.sleep_time)


def main():
    print("Part One:", strategy(1))
    print("Part Two:", strategy(2))


def strategy(strat):
    dat = dict()
    guard = None
    laziest_guard = None
    for line in sorted(lines()):

        d, e = re.findall(r"\[(.*)\] (.*)", line)[0]
        day, time = d.split(" ")
        date = datetime.strptime(d, "%Y-%m-%d %H:%M")

        if e.startswith("Guard"):
            ident = int(re.findall(r"#[0-9]*", e)[0][1:])
            guard = dat.setdefault(ident, Guard(ident))
            guard.set_strategy(strat)
        elif e.startswith("falls"):
            guard.sleep(date)
        elif e.startswith("wakes"):
            guard.wake(date)

        if laziest_guard is None:
            laziest_guard = guard
        elif laziest_guard.score < guard.score:
            laziest_guard = guard

    return laziest_guard.product()


def get_minute_part(t):
    return int(t.split(":")[1])


def lines():
    with open("./input", "r") as fd:
        for line in fd.readlines():
            yield line[:-1]


if __name__ == "__main__":
    main()


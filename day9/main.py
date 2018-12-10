"""

I know this challenge can be solved with a single formula.
I just cannot figure out what that formula would be.

the player that recieve points for a marble is defined as:
    [marble mod player_count] where `marble` is divisible by 23

example:
    f(23, 9) = 23 mod 9 = 5
    f(46, 9) = 46 mod 9 = 1
    f(69, 9) = 69 mod 9 = 6

How to determin the points given to each player?
It should be a function of the marble value only.
"""
import re
from collections import deque


class LListItem():
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

    def __repr__(self):
        return "<{}>".format(self.value)

    def insert_after(self, item):
        if self.next:
            self.next.prev = item
            item.next = self.next
        item.prev = self
        self.next = item

    def remove(self):
        if self.prev:
            self.prev.next = self.next
        if self.next:
            self.next.prev = self.prev
        self.prev, self.next = None, None

    def get_prev(self, n=1):
        m = self
        for _ in range(n):
            if not m or not m.prev:
                return None
            m = m.prev
        return m

    def get_next(self, n=1):
        m = self
        for _ in range(n):
            if not m or not m.next:
                return None
            m = m.next
        return m


class Player():
    def __init__(self, name):
        self.name = name
        self.score = 0

    def __repr__(self):
        return "<{}:{}>".format(self.name, self.score)


class GameBoard():
    def __init__(self, marble_limit):
        gen = self._generate_marbles(marble_limit)
        self.marble_0 = next(gen)
        self.marble_0.insert_after(self.marble_0)
        self.current_marble = self.marble_0
        self._marble_generator = gen

    def play_next_marble(self):
        marble = next(self._marble_generator)
        if marble.value % 23 == 0:
            r = self.current_marble.get_prev(7)
            self.current_marble = r.next
            r.remove()
            return marble.value + r.value
        else:
            self.current_marble.next.insert_after(marble)
            self.current_marble = marble
            return 0

    def dump_board(self):

        def _format_marble(_m):
            if _m is self.current_marble:
                return "[{}]".format(_m.value)
            else:
                return _m.__repr__()

        ret = [_format_marble(self.marble_0)]
        m = self.marble_0.next

        while m is not self.marble_0:
            ret.append(_format_marble(m))
            m = m.next
        return ", ".join(ret)

    def _generate_marbles(self, limit):
        for m in range(limit + 1):
            yield LListItem(m)

def main():
    players, marble = get_specs("input")
    print("Player Count:", players)
    print("Largest Marble:", marble)
    print("Part 1:", part1(players, marble))
    print("Part 2:", part1(players, marble*100))


def part1(player_num, marble):
    players = deque([
        Player("Player{}".format(i + 1))
        for i in range(player_num)])
    max_score = -1
    board = GameBoard(marble)
    i = -1 
    while True:
        p = players.popleft()
        i += 1

        try:
            p.score += board.play_next_marble()
            max_score = max(max_score, p.score)
        except StopIteration as e:
            return max(max_score, p.score)

        players.append(p)


def get_specs(path):
    with open(path, "r") as fd:
        p, m = re.findall(r"\d+", fd.read())
        return int(p), int(m)


if __name__ == "__main__":
    main()

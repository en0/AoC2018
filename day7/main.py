import heapq
# from collections import deque


class Task():
    def __init__(self, name):
        self.name = name
        self.dependents = []
        self.depends_on = []
        self.value = ord(name)
        self.effort = 60 + ord(name) - ord("A") + 1

    @property
    def can_start(self):
        return len(self.depends_on) == 0

    def dump(self, level=0, st=None):
        st = set() if st is None else st
        if self not in st:
            st.add(self)
            print(" - " * level, self. name)
            for dep in self.dependents:
                dep.dump(level+1, st)
        else:
            print(" - " * level, self. name)

    def __repr__(self):
        return "<{}>".format(self.name)


class HeapQueue():
    def __init__(self, init=[]):
        self._dat = []
        self._members = set()
        for node in init:
            self.push(node)

    def __bool__(self):
        return self._dat.__bool__()

    def push(self, node):
        if node not in self._members:
            value = node.value
            heapq.heappush(self._dat, (value, node))
            self._members.add(node)

    def pop(self):
        if not self._dat:
            return None
        _, node = heapq.heappop(self._dat)
        self._members.remove(node)
        return node


class Tasker():
    def __init__(self):
        self.queue = HeapQueue()
        self.pending_tasks = dict()
        self.hold = []

    def load_instruction(self, path):
        """load instructions from file and compile task graph"""

        with open(path, "r") as fd:
            for line in fd.readlines():
                words = line.split(" ")
                p, c = (words[1], words[7])
                _c = self.pending_tasks.setdefault(c, Task(c))
                _p = self.pending_tasks.setdefault(p, Task(p))
                _c.depends_on.append(_p)
                _p.dependents.append(_c)

        for n in self.pending_tasks.values():
            if n.can_start:
                self.queue.push(n)

    def tasks(self):
        """Get the next available task"""

        while len(self.pending_tasks) > 0:
            while True:
                task = self.queue.pop()
                if not task:
                    yield None
                    break

                elif self._can_start_task(task):
                    yield task
                    break

                else:
                    self.hold.append(task)

    def complete(self, task):
        """Mark a task complete

        This will enqueue it's dependents"""

        if self.hold:
            [self.queue.push(x) for x in self.hold]
            self.hold = []

        if task is None:
            return

        elif task.name in self.pending_tasks:
            del self.pending_tasks[task.name]
            if task.dependents:
                [self.queue.push(x) for x in task.dependents]

    def _can_start_task(self, task):
        for t in task.depends_on:
            if t.name in self.pending_tasks:
                return False
        return True


def main():
    tasker = Tasker()
    tasker.load_instruction("input")
    print("Part 1:", part1(tasker))

    tasker = Tasker()
    tasker.load_instruction("input")
    print("Part 2:", part2(tasker))


def part1(tasker):
    steps = []
    for task in tasker.tasks():
        tasker.complete(task)
        steps.append(task.name)
    return "".join(steps)


def part2(tasker):
    pass


if __name__ == "__main__":
    main()

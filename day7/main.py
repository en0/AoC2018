import heapq


# PATH, WORKER_COUNT, EFFORT_WEIGHT = "sample", 2, 0
PATH, WORKER_COUNT, EFFORT_WEIGHT = "input", 10, 60


class Task():
    def __init__(self, name):
        self.name = name
        self.dependents = []
        self.depends_on = []
        self.value = ord(name)
        self.effort = EFFORT_WEIGHT + self.value - ord("A") + 1

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
        return "<{}:{}>".format(self.name, self.effort)


class HeapQueue():
    def __init__(self, init=[]):
        self._dat = []
        self._members = set()
        for node in init:
            self.push(node)

    def __bool__(self):
        return len(self._dat) > 0

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


class SimpleHeapQueue():
    def __init__(self, dat):
        self.dat = dat
        heapq.heapify(self.dat)

    def __bool__(self):
        return len(self.dat) > 0

    def push(self, value):
        heapq.heappush(self.dat, value)

    def pop(self):
        if not self.dat:
            return None
        return heapq.heappop(self.dat)


class Tasker():
    def __init__(self):
        self.queue = HeapQueue()
        self.pending_tasks = dict()
        self.hold = []

    def __bool__(self):
        return len(self.pending_tasks) > 0

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
    tasker.load_instruction(PATH)
    print("Part 1:", part1(tasker))

    tasker = Tasker()
    tasker.load_instruction(PATH)
    print("Part 2:", part2(tasker, WORKER_COUNT))


def part1(tasker):
    steps = []
    for task in tasker.tasks():
        tasker.complete(task)
        steps.append(task.name)
    return "".join(steps)


def part2(tasker, worker_count):
    current_time = 0
    workers = {}
    worker_queue = SimpleHeapQueue([x for x in range(worker_count)])
    task_generator = tasker.tasks()

    while tasker:
        while worker_queue:
            task = next(task_generator)
            if not task:
                break
            worker = worker_queue.pop()
            workers[worker] = task
        m = min_effort(workers)
        current_time += m
        for idel_worker, complete_task in subtract_effort(m, workers):
            worker_queue.push(idel_worker)
            tasker.complete(complete_task)

    return current_time


def min_effort(workers):
    return min([x.effort for x in workers.values()])


def subtract_effort(value, workers):
    keys_to_remove = []
    for worker, task in workers.items():
        task.effort -= value
        if task.effort == 0:
            keys_to_remove.append(worker)
            yield (worker, task)

    for key in keys_to_remove:
        del workers[key]


if __name__ == "__main__":
    main()

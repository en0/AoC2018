class Node():
    def __init__(self):
        self.child_nodes = []
        self.metadata_entries = []

    def add_child(self, node):
        self.child_nodes.append(node)

    def add_metadata_entry(self, metadata):
        self.metadata_entries.append(metadata)

    def sum_metadata(self):
        return sum(self.metadata_entries) + sum([
            c.sum_metadata() for c in self.child_nodes])

    @property
    def value(self):
        if not self.child_nodes:
            return self.sum_metadata()
        return sum([
            self.child_nodes[i-1].value
            for i in self.metadata_entries
            if 0 < i < len(self.child_nodes) + 1])


def build_node(data, index):
    """Recursivly read the data to build the terr"""
    node = Node()
    number_of_children, number_of_meta = data[index:index+2]
    index += 2

    for _ in range(number_of_children):
        index, child_node = build_node(data, index)
        node.add_child(child_node)

    for _ in range(number_of_meta):
        node.add_metadata_entry(data[index])
        index += 1

    return index, node


def load_tree(path):
    with open(path, "r") as fd:
        data = [int(x) for x in fd.read().split(" ")]
    _, root = build_node(data, 0)
    return root


def main():
    path = "sample"
    # path = "input"

    root = load_tree(path)
    print("Part 1:", root.sum_metadata())
    print("Part 2:", root.value)


if __name__ == "__main__":
    main()

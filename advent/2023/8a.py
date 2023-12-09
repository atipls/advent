from dataclasses import dataclass
from advent.aoc import get_input


data = get_input(8)
if False:
    data = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

lines = data.splitlines()
sequence = lines[0]

TARGET = "ZZZ"

@dataclass
class Node:
    name: str
    left: str
    right: str


@dataclass
class NodeList:
    nodes: list[Node]

    def get(self, name: str) -> Node:
        for node in self.nodes:
            if node.name == name:
                return node
        raise KeyError(f"Node {name} not found")

    @staticmethod
    def parse_nodes():
        nodes = []
        for line in lines[2:]:
            left, right = line.split(" = ")
            nodes.append(Node(left, *right[1:-1].split(", ")))
        return NodeList(nodes)

nodes = NodeList.parse_nodes()
num_steps = 0

current = nodes.get("AAA")
while current.name != TARGET:
    print(current)
    next_node = nodes.get(current.left if sequence[num_steps % len(sequence)] == "L" else current.right)
    num_steps += 1
    current = next_node

print(num_steps)
from dataclasses import dataclass
from advent.aoc import get_input
from math import lcm

data = get_input(8)
if False:
    data = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

lines = data.splitlines()
sequence = lines[0]

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

currents = [
    node for node in nodes.nodes if node.name.endswith("A")
]

print(currents)

steps_taken = []
for current in currents:
    num_steps = 1
    found_target = False
    while not found_target:
        if num_steps == 1:
            next_node = current

        for current_sequence in sequence:
            next_node = nodes.get(next_node.left if current_sequence == "L" else next_node.right)
            if next_node.name.endswith("Z"):
                found_target = True
                break
            else:
                num_steps += 1

    steps_taken.append(num_steps)

print(lcm(*steps_taken))


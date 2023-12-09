from dataclasses import dataclass
from advent.aoc import get_input
from math import comb

data = get_input(9)
if False:
    data = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

lines = data.splitlines()


def pascal(n: int) -> list[int]:
    for i in range(n + 1):
        yield comb(n, i) * (-1) ** (i + n)


@dataclass
class Value:
    values: list[int]

    def diff(self):
        new_values = []
        for i in range(len(self.values) - 1):
            new_values.append(self.values[i + 1] - self.values[i])

        return Value(new_values)

    def predicted(self):
        pascal_values = list(pascal(len(self.values)))
        first_pascal = -pascal_values[0]
        total_sum = 0
        for pnum, vnum in zip(pascal_values[1:], self.values):
            total_sum += pnum * vnum

        return total_sum * first_pascal

    def __repr__(self) -> str:
        return f"Value({self.values})"


def parse_values() -> list[Value]:
    for line in lines:
        yield Value([int(x) for x in line.split(" ")])


values = list(parse_values())

print(sum(value.predicted() for value in values))

print(list(pascal(5)))
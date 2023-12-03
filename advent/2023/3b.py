from collections import defaultdict
from dataclasses import dataclass
from advent.aoc import get_input

data = get_input(3)
if False:
    data = """467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598.."""
lines = data.splitlines()


@dataclass
class EngineSymbol:
    symbol: str
    x: int
    y: int

    def __repr__(self):
        return f"EngineSymbol({self.symbol}, {self.x}, {self.y})"


def maybe_get_valid_symbol(x: int, y: int) -> EngineSymbol:
    if x < 0 or y < 0:
        return None

    if x >= len(lines[0]) or y >= len(lines):
        return None

    maybe_symbol = lines[y][x]
    if maybe_symbol.isdigit() or maybe_symbol == ".":
        return None

    return EngineSymbol(maybe_symbol, x, y)


def gear_ratios() -> dict[tuple[int, int], list[int]]:
    ratios = defaultdict(list)
    for y, line in enumerate(lines):
        x = 0
        while x < len(line):
            if not line[x].isdigit():
                x += 1
                continue

            start = x - 1
            end = x
            while end < len(line) and line[end].isdigit():
                end += 1

            valid_symbol = maybe_get_valid_symbol(start, y)
            valid_symbol = valid_symbol or maybe_get_valid_symbol(end, y)

            for xcheck in range(start, end + 1):
                valid_symbol = valid_symbol or maybe_get_valid_symbol(xcheck, y - 1)
                valid_symbol = valid_symbol or maybe_get_valid_symbol(xcheck, y + 1)

            if valid_symbol and valid_symbol.symbol == "*":
                ratios[(valid_symbol.x, valid_symbol.y)].append(
                    int(line[start + 1 : end])
                )

            x = end

    return ratios


print(sum([ratio[0] * ratio[1] for ratio in gear_ratios().values() if len(ratio) == 2]))

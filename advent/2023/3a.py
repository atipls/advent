from advent.aoc import get_input

data = get_input(3)
lines = data.splitlines()

def is_valid_symbol(x: int, y: int) -> bool:
    if x < 0 or y < 0:
        return False

    if x >= len(lines[0]) or y >= len(lines):
        return False

    maybe_symbol = lines[y][x]
    if maybe_symbol.isdigit() or maybe_symbol == ".":
        return False

    return True

def numbers_with_adjacent_symbols() -> list[int]:
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

            valid_symbol = is_valid_symbol(start, y)
            valid_symbol = valid_symbol or is_valid_symbol(end, y)
            
            for xcheck in range(start, end + 1):
                valid_symbol = valid_symbol or is_valid_symbol(xcheck, y-1)
                valid_symbol = valid_symbol or is_valid_symbol(xcheck, y+1)

            if valid_symbol:
                yield int(line[start+1:end])
            
            x = end

print(sum(numbers_with_adjacent_symbols()))

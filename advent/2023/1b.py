from advent.aoc import get_input
import re

data = get_input(1).splitlines()

MAPPING = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

def build_number(line: str) -> str:
    for index, char in enumerate(line):
        if char in "0123456789":
            yield char

        mapping = (
            str(MAPPING[word]) for word in MAPPING 
            if line[index:index+len(word)] == word
        )

        if found_mapping := next(mapping, None):
            yield found_mapping
 

def map_line(line: str) -> int:
    line = "".join(build_number(line))
    line = re.sub(r"[^0-9]", "", line)

    calib = line[0] + line[-1]
    return int(calib)

data = [map_line(line) for line in data]

print(sum(data))
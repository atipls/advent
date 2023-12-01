from advent.aoc import get_input
import re

data = get_input(1).splitlines()

def map_line(line):
    line = re.sub(r"[^0-9]", "", line)
    calib = line[0] + line[-1]
    return int(calib)

data = [map_line(line) for line in data]
print(sum(data))
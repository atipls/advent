from collections import defaultdict
from dataclasses import dataclass
from advent.aoc import get_input
from math import prod, floor, ceil
data = get_input(6)
if False: 
    data = """Time:      7  15   30
Distance:  9  40  200"""

lines = data.splitlines()

@dataclass
class BoatRaceRecord:
    time_ms: int
    record_distance: int

    def __repr__(self):
        return f"BoatRaceRecord({self.time_ms}, {self.record_distance})"

    def number_of_accels_that_beat_the_record(self) -> int:
        minimum = (self.time_ms - (self.time_ms ** 2 - 4 * self.record_distance) ** 0.5) / 2
        maximum = (self.time_ms + (self.time_ms ** 2 - 4 * self.record_distance) ** 0.5) / 2

        minimum = floor(minimum + 1)
        maximum = ceil(maximum - 1)

        return maximum - minimum + 1

def get_record() -> BoatRaceRecord:
    time = lines[0].strip("Time: ")
    time = time.replace(" ", "")

    distance = lines[1].strip("Distance: ")
    distance = distance.replace(" ", "")

    return BoatRaceRecord(int(time), int(distance))

record = get_record()
print(record.number_of_accels_that_beat_the_record())
from collections import defaultdict
from dataclasses import dataclass
from advent.aoc import get_input
from math import prod
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
    
    def get_final_distance(self, accel_time_ms: int) -> int:
        remaining = self.time_ms - accel_time_ms
        if remaining < 0:
            return 0
        return remaining * accel_time_ms

    def accelerations_that_beat_the_record(self) -> list[int]:
        for accel_time_ms in range(1, self.time_ms):
            if self.get_final_distance(accel_time_ms) > self.record_distance:
                yield accel_time_ms

def get_records() -> list[BoatRaceRecord]:
    time = lines[0].strip("Time: ")
    time = time.replace(" ", "")

    distance = lines[1].strip("Distance: ")
    distance = distance.replace(" ", "")

    yield BoatRaceRecord(int(time), int(distance))


for record in get_records():
    print(record, "can be beaten by accelerations of", list(record.accelerations_that_beat_the_record()), "ms")

print(prod(len(list(accels)) for accels in (record.accelerations_that_beat_the_record() for record in get_records())))
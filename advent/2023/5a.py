from collections import defaultdict
from dataclasses import dataclass
from advent.aoc import get_input

data = get_input(5)
if False:
    data = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""
lines = data.splitlines()

@dataclass
class Mapping:
    dst_start: int
    src_start: int
    range_len: int

    def __repr__(self):
        return f"Mapping({self.dst_start}, {self.src_start}, {self.range_len})"
    
    def __str__(self):
        return f"Mapping: {self.src_start} - {self.src_start + self.range_len} -> {self.dst_start} - {self.dst_start + self.range_len}"

    def to_destination_category(self, src: int) -> int:
        if src < self.src_start or src >= self.src_start + self.range_len:
            return None

        return self.dst_start + (src - self.src_start)


@dataclass
class Parcel:
    seeds: list[int]
    seed_to_soil: list[Mapping]
    soil_to_fertilizer: list[Mapping]
    fertilizer_to_water: list[Mapping]
    water_to_light: list[Mapping]
    light_to_temperature: list[Mapping]
    temperature_to_humidity: list[Mapping]
    humidity_to_location: list[Mapping]

    def _map(self, src: int, mappings: list[Mapping]) -> int:
        for mapping in mappings:
            if category := mapping.to_destination_category(src):
                return category

        # Any source numbers that aren't mapped correspond to the same destination number.
        return src

    def map_seed_to_soil(self, seed: int) -> int:
        return self._map(seed, self.seed_to_soil)
    
    def map_soil_to_fertilizer(self, soil: int) -> int:
        return self._map(soil, self.soil_to_fertilizer)
    
    def map_fertilizer_to_water(self, fertilizer: int) -> int:
        return self._map(fertilizer, self.fertilizer_to_water)
    
    def map_water_to_light(self, water: int) -> int:
        return self._map(water, self.water_to_light)
    
    def map_light_to_temperature(self, light: int) -> int:
        return self._map(light, self.light_to_temperature)
    
    def map_temperature_to_humidity(self, temperature: int) -> int:
        return self._map(temperature, self.temperature_to_humidity)
    
    def map_humidity_to_location(self, humidity: int) -> int:
        return self._map(humidity, self.humidity_to_location)
    
    def map_seed_to_location(self, seed: int) -> int:
        soil = self.map_seed_to_soil(seed)
        fertilizer = self.map_soil_to_fertilizer(soil)
        water = self.map_fertilizer_to_water(fertilizer)
        light = self.map_water_to_light(water)
        temperature = self.map_light_to_temperature(light)
        humidity = self.map_temperature_to_humidity(temperature)
        location = self.map_humidity_to_location(humidity)
        return location

    @staticmethod
    def parse_mapping(index: int) -> tuple[list[Mapping], int]:
        current = index
        mappings = []
        current += 1 # skip the header
        while current < len(lines):
            line = lines[current]
            current += 1
            if len(line) == 0:
                break

            dst_start, src_start, range_len = map(int, line.split(" "))
            mappings.append(Mapping(dst_start, src_start, range_len))

        return mappings, current

    @staticmethod
    def parse():
        current = 0
        _, seeds = lines[current].split(":")
        seeds = seeds.strip()
        seeds = [int(n.strip()) for n in seeds.split(" ")]
        current += 2 # skip empty line

        seed_to_soil, current = Parcel.parse_mapping(current)
        soil_to_fertilizer, current = Parcel.parse_mapping(current)
        fertilizer_to_water, current = Parcel.parse_mapping(current)
        water_to_light, current = Parcel.parse_mapping(current)
        light_to_temperature, current = Parcel.parse_mapping(current)
        temperature_to_humidity, current = Parcel.parse_mapping(current)
        humidity_to_location, current = Parcel.parse_mapping(current)

        return Parcel(
            seeds,
            seed_to_soil,
            soil_to_fertilizer,
            fertilizer_to_water,
            water_to_light,
            light_to_temperature,
            temperature_to_humidity,
            humidity_to_location
        )   


parcel = Parcel.parse()
locations = [parcel.map_seed_to_location(seed) for seed in parcel.seeds]

print(min(locations))
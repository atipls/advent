struct Mapping {
    dst_start: u64,
    src_start: u64,
    range_len: u64,
}

impl Mapping {
    fn new(dst_start: u64, src_start: u64, range_len: u64) -> Self {
        Self {
            dst_start,
            src_start,
            range_len,
        }
    }

    pub fn to_destination_category(&self, src: u64) -> Option<u64> {
        if src < self.src_start || src >= self.src_start + self.range_len {
            None
        } else {
            Some(self.dst_start + src - self.src_start)
        }
    }
}

struct Parcel {
    seeds: Vec<(u64, u64)>,
    total_seeds: u64,
    seed_to_soil: Vec<Mapping>,
    soil_to_fertilizer: Vec<Mapping>,
    fertilizer_to_water: Vec<Mapping>,
    water_to_light: Vec<Mapping>,
    light_to_temperature: Vec<Mapping>,
    temperature_to_humidity: Vec<Mapping>,
    humidity_to_location: Vec<Mapping>,
}

impl Parcel {
    fn parse_mappings(lines: &Vec<String>, index: usize) -> (Vec<Mapping>, usize) {
        let mut mappings = Vec::new();
        let mut i = index + 1; // Skip the header line
        while i < lines.len() {
            let line = &lines[i];
            i += 1;
            if line.len() == 0 {
                break;
            }
            let mut parts = line.split_whitespace();
            let dst_start = parts.next().unwrap().parse::<u64>().unwrap();
            let src_start = parts.next().unwrap().parse::<u64>().unwrap();
            let range_len = parts.next().unwrap().parse::<u64>().unwrap();
            mappings.push(Mapping::new(dst_start, src_start, range_len));
        }
        (mappings, i)
    }

    pub fn parse(lines: &Vec<String>) -> Self {
        let mut current = 0;
        let seeds = lines[current]
            .split(":")
            .nth(1)
            .unwrap()
            .trim()
            .split(" ")
            .collect::<Vec<&str>>();
        let mut seed_ranges = Vec::new();
        for i in (0..seeds.len()).step_by(2) {
            seed_ranges.push((
                seeds[i].trim().parse::<u64>().unwrap(),
                seeds[i + 1].trim().parse::<u64>().unwrap(),
            ));
        }
        let mut total_seeds = 0u64;
        for (start, length) in &seed_ranges {
            total_seeds += length;
        }

        println!("A total of {} seeds", total_seeds);
        current += 2; // skip empty line

        let (seed_to_soil, current) = Parcel::parse_mappings(lines, current);
        let (soil_to_fertilizer, current) = Parcel::parse_mappings(lines, current);
        let (fertilizer_to_water, current) = Parcel::parse_mappings(lines, current);
        let (water_to_light, current) = Parcel::parse_mappings(lines, current);
        let (light_to_temperature, current) = Parcel::parse_mappings(lines, current);
        let (temperature_to_humidity, current) = Parcel::parse_mappings(lines, current);
        let (humidity_to_location, _) = Parcel::parse_mappings(lines, current);
        Self {
            seeds: seed_ranges,
            total_seeds,
            seed_to_soil,
            soil_to_fertilizer,
            fertilizer_to_water,
            water_to_light,
            light_to_temperature,
            temperature_to_humidity,
            humidity_to_location,
        }
    }


    fn map(&self, src: u64, mappings: &Vec<Mapping>) -> u64 {
        for mapping in mappings {
            if let Some(category) = mapping.to_destination_category(src) {
                return category;
            }
        }

        src
    }

    pub fn map_seed_to_soil(&self, seed: u64) -> u64 {
        self.map(seed, &self.seed_to_soil)
    }

    pub fn map_soil_to_fertilizer(&self, soil: u64) -> u64 {
        self.map(soil, &self.soil_to_fertilizer)
    }

    pub fn map_fertilizer_to_water(&self, fertilizer: u64) -> u64 {
        self.map(fertilizer, &self.fertilizer_to_water)
    }

    pub fn map_water_to_light(&self, water: u64) -> u64 {
        self.map(water, &self.water_to_light)
    }

    pub fn map_light_to_temperature(&self, light: u64) -> u64 {
        self.map(light, &self.light_to_temperature)
    }

    pub fn map_temperature_to_humidity(&self, temperature: u64) -> u64 {
        self.map(temperature, &self.temperature_to_humidity)
    }

    pub fn map_humidity_to_location(&self, humidity: u64) -> u64 {
        self.map(humidity, &self.humidity_to_location)
    }

    pub fn map_seed_to_location(&self, seed: u64) -> u64 {
        let soil = self.map_seed_to_soil(seed);
        let fertilizer = self.map_soil_to_fertilizer(soil);
        let water = self.map_fertilizer_to_water(fertilizer);
        let light = self.map_water_to_light(water);
        let temperature = self.map_light_to_temperature(light);
        let humidity = self.map_temperature_to_humidity(temperature);
        self.map_humidity_to_location(humidity)
    }
}

fn main() {
    let input = std::fs::read_to_string("/Users/atipls/Work/advent/data/2023_5.txt").unwrap();
    let lines = input
        .lines()
        .map(|x| x.to_string())
        .collect::<Vec<String>>();

    let parcel = Parcel::parse(&lines);
    let mut current_minimum = vec![u64::MAX; parcel.seeds.len()];
    let mut seeds_checked = 0u64;
    let mut start_time = std::time::Instant::now();

    for (index, (seed_start, length)) in parcel.seeds.iter().enumerate() {
        println!(
            "Checking seeds {} to {} ({})",
            seed_start,
            seed_start + length,
            length
        );
        for seed_index in 0..*length {
            let location = parcel
                .map_seed_to_location(*seed_start + seed_index);
            seeds_checked += 1;
            let elapsed = start_time.elapsed().as_secs_f64();
            if elapsed > 10.0 {
                println!(
                    "Progress: {:.2}%",
                    seeds_checked as f64 / parcel.total_seeds as f64 * 100.0
                );
                start_time = std::time::Instant::now();
            }
            if location < current_minimum[index] {
                current_minimum[index] = location;
            }
        }
        println!("Minimum: {}", current_minimum[index]);
    }

    println!("All seeds checked");

    let mut actual_minimum = u64::MAX;
    for location in current_minimum {
        if location < actual_minimum {
            actual_minimum = location;
        }
    }

    println!("The minimum location is {}", actual_minimum);
}

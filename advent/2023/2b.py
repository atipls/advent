from dataclasses import dataclass
from advent.aoc import get_input

data = get_input(2).splitlines()

@dataclass
class RevealedCube:
    count: int
    color: str

@dataclass
class CubeSet:
    cubes: list[RevealedCube]

    def get_count(self, color: str) -> int:
        return next((cube.count for cube in self.cubes if cube.color == color), 0)

    def possible(self, red: int, green: int, blue: int):
        return self.get_count("red") <= red and self.get_count("green") <= green and self.get_count("blue") <= blue
    

@dataclass
class Game:
    id: int
    cubes: list[CubeSet]

    def possible(self, red: int, green: int, blue: int):
        return all(cube.possible(red, green, blue) for cube in self.cubes)

    def smallest_red(self):
        return max(cube.get_count("red") for cube in self.cubes)
    
    def smallest_green(self):
        return max(cube.get_count("green") for cube in self.cubes)
    
    def smallest_blue(self):
        return max(cube.get_count("blue") for cube in self.cubes)
    
    def smallest(self):
        return (
            self.smallest_red(),
            self.smallest_green(),
            self.smallest_blue()
        )

def parse_game_data(line):
    game_tag, game_data = line.split(":")
    _, gameid = game_tag.split(" ")
    gameid = int(gameid)

    cubesets = []

    for cubeset in game_data.split(";"):
        cubes = []
        for cube in cubeset.split(","):
            cube = cube.strip()

            count, color = cube.split(" ")
            cubes.append(RevealedCube(int(count), color))
        cubesets.append(CubeSet(cubes))        

    return Game(gameid, cubesets)

games = [
    parse_game_data(line)
    for line in data
]

fewest_cubes_per_game = [
    game.smallest()
    for game in games
]

for index, game in enumerate(fewest_cubes_per_game):
    print(games[index], game)

powers = [
    red * green * blue
    for red, green, blue in fewest_cubes_per_game
]

print(sum(powers))
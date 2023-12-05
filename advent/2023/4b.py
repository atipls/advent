from collections import defaultdict
from dataclasses import dataclass
from advent.aoc import get_input

data = get_input(4)

if False:
    data = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

lines = data.splitlines()


@dataclass
class Scratchcard:
    card: int
    winning: list[int]
    actual: list[int]

    def __repr__(self):
        return f"Scratchcard({self.card}, {self.winning}, {self.actual})"

    def points(self) -> int:
        points = 0
        for number in self.winning:
            if number in self.actual:
                if points == 0:
                    points = 1
                else:
                    points *= 2

        return points

    def number_of_matches(self) -> int:
        return len([n for n in self.winning if n in self.actual])

    def __str__(self) -> str:
        return f"Scratchcard {self.card} has {self.points()} points"


def parse_scratchcards() -> list[Scratchcard]:
    scratchcards = []
    for line in lines:
        card, numbers = line.split(":")
        card = card.split(" ")[-1]

        winning, actual = numbers.split("|")
        winning = [int(n) for n in winning.split()]
        actual = [int(n) for n in actual.split()]

        scratchcards.append(Scratchcard(int(card), winning, actual))

    return scratchcards


scratchcards = parse_scratchcards()


def process_scratches() -> int:
    num_scratchcards_processed = 0
    num_scratchcards = [1] * len(scratchcards)

    # Process while we still have scratchcards
    while all(n > 0 for n in num_scratchcards):
        for index, scratchcard in enumerate(scratchcards):
            for _ in range(
                num_scratchcards[index]
            ):  # Process however many scratchcards we have of this type
                num_scratchcards_processed += 1  # Mark this as processed
                num_scratchcards[
                    index
                ] -= 1  # Remove this scratchcard from the pile, we are processing it

                matches = scratchcard.number_of_matches()
                if matches == 0:  # We didn't win any new scratchcards
                    continue

                for extra in range(matches):
                    # We won a new scratchcard
                    num_scratchcards[index + extra + 1] += 1

    return num_scratchcards_processed


processed = process_scratches()
print("Processed", processed, "scratchcards")

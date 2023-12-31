from collections import Counter, defaultdict
from dataclasses import dataclass
import enum
from advent.aoc import get_input
from functools import cmp_to_key

data = get_input(7)
if True:
    data = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
lines = data.splitlines()

STRENGTHS = "23456789TJQKA"

class DeckType(enum.IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    FULL_HOUSE = 3
    THREE_OF_A_KIND = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6
   
    def to_str(self) -> str:
        match self:
            case DeckType.HIGH_CARD:
                return "High Card"
            case DeckType.ONE_PAIR:
                return "One Pair"
            case DeckType.TWO_PAIR:
                return "Two Pair"
            case DeckType.FULL_HOUSE:
                return "Full House"
            case DeckType.THREE_OF_A_KIND:
                return "Three of a Kind"
            case DeckType.FOUR_OF_A_KIND:
                return "Four of a Kind"
            case DeckType.FIVE_OF_A_KIND:
                return "Five of a Kind"
            case _:
                return "Unknown"

@dataclass
class CamelCard:
    cards: list[str]
    bid: int
    rank: int = None
    
    def classification(self) -> DeckType:
        counter = Counter(self.cards)

        if len(counter) == 1:
            return DeckType.FIVE_OF_A_KIND
        
        if 3 in counter.values():
            return DeckType.FULL_HOUSE
        
        if len(counter) == 2:
            if 4 in counter.values():
                return DeckType.FOUR_OF_A_KIND
            else:
                return DeckType.THREE_OF_A_KIND
            
        if 2 in counter.values():
            pair_count = 0
            for count in counter.values():
                if count == 2:
                    pair_count += 1

            if pair_count == 2:
                return DeckType.TWO_PAIR
            else:
                return DeckType.ONE_PAIR
            
        return DeckType.HIGH_CARD

    def __repr__(self):
        return f"CamelCard('{"".join(self.cards)}', {self.bid}, rank={self.rank}, classification={self.classification().to_str()})"
    

def parse_camel_cards() -> list[CamelCard]:
    return [
        CamelCard(
            cards=[*line.split(" ")[0]],
            bid=int(line.split(" ")[1])
        )
        for line in lines
    ]

def compare_cards(card1: CamelCard, card2: CamelCard) -> int:
    classification1 = card1.classification()
    classification2 = card2.classification()

    if classification1 > classification2:
        return 1
    elif classification1 < classification2:
        return -1
    
    # Same classification, compare the cards
    for card1, card2 in zip(card1.cards, card2.cards):
        if STRENGTHS.index(card1) > STRENGTHS.index(card2):
            return 1
        elif STRENGTHS.index(card1) < STRENGTHS.index(card2):
            return -1
        
    # Same cards, doesn't matter
    return 0
    

# Order the cards by classification and then by rank/strength
def order_cards(cards: list[CamelCard]) -> list[CamelCard]:
    return sorted(
        cards,
        key=cmp_to_key(compare_cards),
        reverse=False
    )

ordered_cards = order_cards(parse_camel_cards())

rank = 1
for card in ordered_cards:
    card.rank = rank
    rank += 1

    print(card)

for card in ordered_cards:
    print(f"{card.bid}*{card.rank}", end="")
    if card != ordered_cards[-1]:
        print("+", end="")

print(f"={sum(card.rank * card.bid for card in ordered_cards)}")
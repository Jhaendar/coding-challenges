# Advent of code, day 7
from __future__ import annotations

from collections import Counter
from functools import total_ordering
from typing import NamedTuple


@total_ordering
class Hand:
    class HandStrength(NamedTuple):
        hand_type: int
        card_strengths: list[int]

    HandTypes: dict[str, int] = {
        "Five of a kind": 6,
        "Four of a kind": 5,
        "Full house": 4,
        "Three of a kind": 3,
        "Two pair": 2,
        "One pair": 1,
        "High card": 0,
    }

    HandTypeMapping: dict[tuple[tuple[int, ...], int], int] = {
        ((5,), 0): HandTypes["Five of a kind"],
        ((), 5): HandTypes["Five of a kind"],
        ((1, 4), 0): HandTypes["Four of a kind"],
        ((1,), 4): HandTypes["Five of a kind"],
        ((4,), 1): HandTypes["Five of a kind"],
        ((2, 3), 0): HandTypes["Full house"],
        ((3,), 2): HandTypes["Five of a kind"],
        ((2,), 3): HandTypes["Five of a kind"],
        ((1, 1, 3), 0): HandTypes["Three of a kind"],
        ((1, 1), 3): HandTypes["Four of a kind"],
        ((1, 3), 1): HandTypes["Four of a kind"],
        ((1, 2, 2), 0): HandTypes["Two pair"],
        ((1, 2), 2): HandTypes["Four of a kind"],
        ((2, 2), 1): HandTypes["Full house"],
        ((1, 1, 1, 2), 0): HandTypes["One pair"],
        ((1, 1, 1), 2): HandTypes["Three of a kind"],
        ((1, 1, 2), 1): HandTypes["Three of a kind"],
        ((1, 1, 1, 1, 1), 0): HandTypes["High card"],
        ((1, 1, 1, 1), 1): HandTypes["One pair"],
    }

    CardStrength = {
        "J": 0,
        "2": 1,
        "3": 2,
        "4": 3,
        "5": 4,
        "6": 5,
        "7": 6,
        "8": 7,
        "9": 8,
        "T": 9,
        "Q": 10,
        "K": 11,
        "A": 12,
    }

    def __init__(self, hand: str, bid: int):
        self.hand = hand
        self.bid = bid
        self.hand_strength = self.get_hand_strength()

    def get_hand_strength(self) -> HandStrength:
        hand_freqs = Counter(self.hand)

        J_freq = hand_freqs.pop("J", 0)
        hand_freq_values = sorted(hand_freqs.values())

        hand_map = (tuple(hand_freq_values), J_freq)
        hand_type = Hand.HandTypeMapping.get(hand_map, None)

        if hand_type is None:
            raise ValueError(f"No HandType found for {self.hand}")

        card_strengths: list[int] = [Hand.CardStrength[x] for x in self.hand]

        return Hand.HandStrength(hand_type, card_strengths)

    def __eq__(self, other) -> bool:
        return self.hand_strength == other.hand_strength

    def __lt__(self, other) -> bool:
        return self.hand_strength < other.hand_strength

    def __repr__(self):
        return f"{self.hand}, {self.bid}, {self.hand_strength}"


def parse_file(filename: str):
    hands: list[Hand] = list()
    with open(filename, "r") as file:
        for line in file:
            hand, bid = line.split()
            new_hand = Hand(hand, int(bid))
            hands.append(new_hand)

    return hands


def rank_hands(hands: list[Hand]):
    return sorted(hands)


def get_winning(hand: Hand, rank: int) -> int:
    return hand.bid * rank


def get_total_winnings(hands: list[Hand]) -> int:
    ranked_hands = rank_hands(hands)

    total_winnings = 0
    for i, hand in enumerate(ranked_hands, start=1):
        hand_winning = get_winning(hand, i)
        total_winnings += hand_winning

    return total_winnings


if __name__ == "__main__":
    input_file = "./advent-of-code/2023/7/day7_input"
    input_example = "./advent-of-code/2023/7/day7_input_example"

    hands = parse_file(input_file)
    # hands = parse_file(input_example)

    # Part 2
    total_winnings = get_total_winnings(hands)
    print(total_winnings)  # 249138943

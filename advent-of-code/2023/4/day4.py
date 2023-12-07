import re

Card = dict[str, list[int]]


def get_card_name(card_part: str) -> int:
    card_match = re.search(r"(\d+)", card_part)

    if card_match:
        return int(card_match.group(1))
    else:
        raise ValueError(f"No card number found: {card_part}")


def parse_file(filename: str) -> dict[int, Card]:
    cards: dict[int, Card] = dict()

    with open(filename, "r") as file:
        for line in file:
            cards.update(parse_card(line))
    return cards


def parse_card(line: str) -> dict[int, Card]:
    card: dict[int, Card] = dict()
    pattern = r":|\|"
    card_part, winner, draw = re.split(pattern, line)
    card_number = get_card_name(card_part)

    winner = {int(x) for x in winner.split()}
    draw = {int(x) for x in draw.split()}

    intersection = winner & draw
    wins = len(intersection)
    if wins == 0:
        points = 0
    else:
        points = 2 ** (wins - 1)

    card_info: Card = {
        "winner": list(winner),
        "draw": list(draw),
        "info": [points, wins, 1],  # points, wins, number of cards
    }

    card[card_number] = card_info

    return card


def get_total_points(cards: list[Card]) -> int:
    total = 0

    for card in cards:
        total += card["info"][0]

    return total


# PART 2
def count_total_cards(cards: dict[int, Card]) -> int:
    total = 0

    for number, card in cards.items():
        wins = card["info"][1]
        amount = card["info"][2]
        total += amount

        for i in range(wins):
            # Add current amount to `wins` successive cards:
            cards[i + number + 1]["info"][2] += amount

    return total


if __name__ == "__main__":
    input_file = "./advent-of-code/2023/4/day4_input"
    input_example = "./advent-of-code/2023/4/day4_example"

    cards = parse_file(input_file)
    # cards = parse_file(input_example)
    points = get_total_points(list(cards.values()))
    print(f"{points=}")

    # PART 2
    amount = count_total_cards(cards)
    print(f"{amount=}")

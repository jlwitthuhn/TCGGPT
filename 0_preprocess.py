# This script takes a scryfall bulk data json file as input
# These files can be downloaded at https://scryfall.com/docs/api/bulk-data
# I recommend the 'Oracle Cards' set which has been deduplicated by card name

import json
import random
import sys

from cardgen.clean import clean_card
from cardgen.tokenizer import CardTokenizer


def print_help():
    print("Usage: python3 0_preprocess.py [input file path] [test percent]")
    print(
        "The file must contain an array of json objects, each with the following shape:"
    )
    print(
        json.dumps(
            {
                "id": "Some sort of guid goes here",
                "name": "Card Name",
                "layout": "normal",
                "mana_cost": "{W}{U}{B}{R}{G}",
                "cmc": 5,
                "type_line": "Creature — Dinosaur",
                "oracle_text": "Rules text goes here.",
                "set_type": "expansion",
                "oversized": False,
                "border_color": "black",
            },
            indent=2,
        )
    )
    print(
        "Cards with a layout other than 'normal' and ones that are silver-bordered or otherwise not playable under normal rules will not be included"
    )
    print()

# Cards with unique mechanics and words. Anything listed here is subjectively
# 'too far' from a standard magic card to be useful in training.
FORBIDDEN_NAMES = {
    "Chaos Orb",
    "Falling Star",
    "Fiery Gambit",
    "Goblin Game",
}

def is_card_valid(maybe_card):
    return (
        "id" in maybe_card
        and isinstance(maybe_card["id"], str)
        and "name" in maybe_card
        and maybe_card["name"] not in FORBIDDEN_NAMES
        and isinstance(maybe_card["name"], str)
        and "layout" in maybe_card
        and isinstance(maybe_card["layout"], str)
        and "mana_cost" in maybe_card
        and isinstance(maybe_card["mana_cost"], str)
        and "cmc" in maybe_card
        and isinstance(maybe_card["cmc"], float)
        and "type_line" in maybe_card
        and isinstance(maybe_card["type_line"], str)
        and "oracle_text" in maybe_card
        and isinstance(maybe_card["oracle_text"], str)
        and "set_type" in maybe_card
        and isinstance(maybe_card["set_type"], str)
    )


def is_card_eligible(maybe_card):
    result = True
    result = result and maybe_card["layout"] == "normal"
    result = result and maybe_card["oversized"] != True
    result = result and maybe_card["set_type"] != "alchemy"
    result = result and maybe_card["set_type"] != "funny"
    result = result and maybe_card["set_type"] != "memorabilia"
    result = result and maybe_card["set_type"] != "token"
    result = result and maybe_card["border_color"] != "silver"
    result = result and maybe_card["set"] != "past"
    result = result and maybe_card["set"] != "pcel"
    if "promo_types" in maybe_card:
        result = result and "playtest" not in maybe_card["promo_types"]
    if "watermark" in maybe_card:
        result = result and maybe_card["watermark"] != "conspiracy"
    return result


def write_full(out_file, the_card):
    out_file.write("<NewCard> ")
    out_file.write("<Type> " + the_card["type_line"] + " ")
    out_file.write("<ManaCost> " + the_card["mana_cost"] + " ")
    if "power" in the_card and "toughness" in the_card:
        out_file.write(
            "<Stats> " + the_card["power"] + " / " + the_card["toughness"] + " "
        )
    out_file.write("<Text> " + the_card["oracle_text"] + "\n")


def write_name(out_file, the_card):
    out_file.write(the_card["name"].lower() + "\n")


def format_data(in_path, train_fraction):
    print("Loading input file: " + in_path)
    in_file = open(in_path, "r")
    card_list = json.loads(in_file.read())
    print("Found " + str(len(card_list)) + " cards")
    # Full file is used to simplify making the tokenizer later
    out_file_full = open("./data/full.txt", "w")
    cards_train = []
    cards_test = []
    count = 0
    random.seed(123456)
    random.shuffle(card_list)

    for this_card in card_list:
        if is_card_valid(this_card) and is_card_eligible(this_card):
            clean_card(this_card)
            write_full(out_file_full, this_card)
            count = count + 1
            # Append to either train or test set
            if len(cards_test) / (len(cards_train) + 1) < train_fraction:
                cards_test.append(this_card)
            else:
                cards_train.append(this_card)
    out_file_full.close()
    print("Wrote out " + str(count) + " valid cards")
    out_file_train = open("./data/train.txt", "w")
    for this_card in cards_train:
        write_full(out_file_train, this_card)
    print(f"Training set: {len(cards_train)}")
    out_file_test = open("./data/test.txt", "w")
    for this_card in cards_test:
        write_full(out_file_test, this_card)
    print(f"Test set: {len(cards_test)}")
    tokenizer = CardTokenizer("./data/full.txt")
    tokenizer.write_stats("./data/token_frequency.txt")
    print("Wrote token_frequency.txt")


if __name__ == "__main__":

    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print_help()
        sys.exit(0)

    train_fraction: float = 0.10
    if len(sys.argv) == 3:
        try:
            train_fraction = float(sys.argv[2]) / 100.0
        except ValueError:
            print_help()
            sys.exit(0)

    format_data(sys.argv[1], train_fraction)

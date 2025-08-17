# This script takes a scryfall bulk data json file as input
# These files can be downloaded at https://scryfall.com/docs/api/bulk-data
# I recommend the 'Oracle Cards' set which has been deduplicated by card name

import argparse
import json
import random
import sys

from cardgen.clean import clean_card
from cardgen.tokenizer import CardTokenizer

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


ALLOWED_LAYOUTS = {
    "mutate",
    "normal",
    "saga",
}


def is_card_eligible(maybe_card):
    result = True
    result = result and maybe_card["layout"] in ALLOWED_LAYOUTS
    result = result and maybe_card["oversized"] != True
    result = result and maybe_card["set_type"] != "alchemy"
    result = result and maybe_card["set_type"] != "funny"
    result = result and maybe_card["set_type"] != "memorabilia"
    result = result and maybe_card["set_type"] != "token"
    result = result and maybe_card["border_color"] != "silver"
    result = result and maybe_card["set"] != "past"
    result = result and maybe_card["set"] != "pcel"
    result = result and "stickers" not in maybe_card["type_line"].lower()
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


TYPES_EXCLUDED: list[str] = ["control", "the", "will"]


def get_plural_type_mapping(card_list: list) -> dict[str, str]:
    potential_types: set[str] = set()
    for this_card in card_list:
        if "—" not in this_card["type_line"]:
            continue
        dash_index = this_card["type_line"].find("—")
        before_dash = this_card["type_line"][:dash_index].lower().strip()
        if before_dash == "planeswalker":
            continue
        after_dash = this_card["type_line"][dash_index + 1 :].lower().strip()
        type_list = after_dash.split()
        potential_types.update(type_list)
    for to_exclude in TYPES_EXCLUDED:
        potential_types.remove(to_exclude)
    result: dict[str, str] = {}
    for this_card in card_list:
        if is_card_valid(this_card) == False or is_card_eligible(this_card) == False:
            continue
        to_remove: set[str] = set()
        for this_type in potential_types:
            if len(this_type) < 3:
                to_remove.add(this_type)
                continue
            this_type_plural = this_type + "s"
            if this_type_plural in this_card["oracle_text"].lower():
                result[this_type_plural] = this_type + " *s"
                to_remove.add(this_type)
        for this_remove in to_remove:
            potential_types.remove(this_remove)
    return result


def format_data(
    in_path: str, test_fraction: float, lite_clean: bool, omit_valid_words: bool
):
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

    print("Preprocessing types...")
    plural_type_map = get_plural_type_mapping(card_list)

    print("Processing...")
    for this_card in card_list:
        if is_card_valid(this_card) and is_card_eligible(this_card):
            clean_card(this_card, lite_clean, plural_type_map)
            write_full(out_file_full, this_card)
            count = count + 1
            # Append to either train or test set
            len_test = len(cards_test)
            len_all = len(cards_train) + len_test
            if len_test / (len_all + 1) < test_fraction:
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
    tokenizer.write_stats("./data/token_frequency.txt", omit_valid_words)
    print("Wrote token_frequency.txt")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Transform data from scryfall json format to text ready for training",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    arg_parser.add_argument("json_path", help="Path to the scryfall json file")
    arg_parser.add_argument(
        "--test",
        default=0.1,
        type=float,
        help="Fraction of data to use as the test split",
    )
    arg_parser.add_argument(
        "--lite-clean",
        action="store_true",
        help="Only do basic data cleaning. See the function clean_card in cardgen/clean.py for details",
    )
    arg_parser.add_argument(
        "--omit-valid-words",
        action="store_true",
        help="Do not include valid words in token_frequency.txt",
    )
    args = arg_parser.parse_args()

    format_data(args.json_path, args.test, args.lite_clean, args.omit_valid_words)

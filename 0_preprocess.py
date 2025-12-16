# This script takes a scryfall bulk data json file as input
# These files can be downloaded at https://scryfall.com/docs/api/bulk-data
# I recommend the 'Oracle Cards' set which has been deduplicated by card name

import argparse
import json
import os
import random
import time

from cardgen.clean import clean_advanced, clean_basic
from cardgen.clean.mtg_keywords import KEYWORD_ABILITIES, KEYWORD_ACTIONS
from cardgen.tokenizer import CardTokenizer
from cardgen.trie import Trie

# Cards with unique mechanics and words. Anything listed here is subjectively
# 'too far' from a standard magic card to be useful in training.
FORBIDDEN_NAMES = {
    "Chaos Orb",
    "Falling Star",
    "Fiery Gambit",
    "Goblin Game",
    "Steamflogger Boss",
    "Truth or Consequences",  # I just don't want to deal with cleaning this one
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
    result = result and "paper" in maybe_card["games"]
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
        result = result and "alchemy" not in maybe_card["promo_types"]
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
        if "--" not in this_card["type_line"]:
            continue
        dash_index = this_card["type_line"].find("--")
        before_dash = this_card["type_line"][:dash_index].strip()
        if before_dash == "planeswalker":
            continue
        after_dash = this_card["type_line"][dash_index + 2 :].strip()
        type_list = after_dash.split()
        potential_types.update(type_list)
    for to_exclude in TYPES_EXCLUDED:
        if to_exclude in potential_types:
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
            if this_type_plural in this_card["oracle_text"]:
                result[this_type_plural] = this_type + " *s"
                to_remove.add(this_type)
        for this_remove in to_remove:
            potential_types.remove(this_remove)
    return result


def get_type_set(card_list: list) -> set[str]:
    result = set()
    for this_card in card_list:
        if "type_line" in this_card:
            full_type = this_card["type_line"]
            dash_index = full_type.find("--")
            before_dash_type: str = full_type[:dash_index]
            after_dash_types: list[str] = full_type[dash_index + 3 :].split(" ")
            result.add(before_dash_type)
            for this_type in after_dash_types:
                result.add(this_type)
    return result


NAME_FILTER_LENGTH_MIN: int = 8

NAME_FILTER_EXCLUDE = {
    "blessing",  # Part of "the city's blessing"
    "black dragon",  # Token color+type
    "blue dragon",  # Token color+type
    "cast out",  # Use in the phrase "cast outlaw"
    "join forces",  # Ability Word (207)
    "goblin wizard",  # Token types
    "greed dragon",  # Token color+type
    "red dragon",  # Token color+type
    "start your engines",  # "start your engines" is a card and "start your engines!" is a keyword
    "white knight",  # Token color+type
}


def get_long_card_name_trie(card_list: list, exclude_set: set[str]) -> Trie:
    trie = Trie()
    for this_card in card_list:
        if (
            this_card["name"] not in exclude_set
            and this_card["name"] not in KEYWORD_ABILITIES
            and this_card["name"] not in KEYWORD_ACTIONS
            and this_card["name"] not in NAME_FILTER_EXCLUDE
            and len(this_card["name"]) >= NAME_FILTER_LENGTH_MIN
        ):
            trie.add(this_card["name"])
    return trie


def get_rare_planeswalker_set(card_list: list) -> set[str]:
    counts = {}

    def add_count(key: str):
        if key in counts:
            counts[key] = counts[key] + 1
        else:
            counts[key] = 1

    for this_card in card_list:
        PW_LINE: str = "legendary planeswalker -- "
        if this_card["type_line"].startswith(PW_LINE):
            end_index = len(PW_LINE)
            add_count(this_card["type_line"][end_index:])
    result = set()
    for type, count in counts.items():
        if count <= 2:
            result.add(type)
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

    print("Filtering to eligible cards...")
    card_list = [
        the_card
        for the_card in card_list
        if is_card_valid(the_card) and is_card_eligible(the_card)
    ]
    print(f"Remaining: {len(card_list)} cards")

    print("Performing basic clean...")
    for this_card in card_list:
        if is_card_valid(this_card) and is_card_eligible(this_card):
            clean_basic(this_card)

    print("Processing types...")
    plural_type_map = get_plural_type_mapping(card_list)
    type_set = get_type_set(card_list)

    print("Processing names...")
    name_trie = get_long_card_name_trie(card_list, type_set)

    print("Processing planeswalkers...")
    rare_planeswalker_set = get_rare_planeswalker_set(card_list)

    print("Doing final clean...")
    for this_card in card_list:
        if not lite_clean:
            clean_advanced(this_card, plural_type_map, name_trie, rare_planeswalker_set)
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
    print(f"Vocab size: {tokenizer.get_vocab_size()}")
    os.makedirs("./data/meta", exist_ok=True)
    tokenizer.write_stats("./data/meta/token_frequency.txt", omit_valid_words)
    print("Wrote data/meta/token_frequency.txt")
    with open("./data/meta/filtered_names.txt", "w") as filtered_log:
        for this_word in name_trie.to_set():
            filtered_log.write(f"{this_word}\n")
    print("Wrote data/meta/filtered_names.txt")


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

    start_time = time.time()
    format_data(args.json_path, args.test, args.lite_clean, args.omit_valid_words)
    end_time = time.time()
    duration = end_time - start_time
    print(f"Finished after {duration:.2f} seconds")

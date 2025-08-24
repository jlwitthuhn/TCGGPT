# Simple cleaning algorithms that do not depend on any hand-made data

import re

from unidecode import unidecode

from .strings import NAMED_CARD

_PARTNER_REGEX = re.compile(r"partner with ([a-zA-Z0-9,\-\s]+?)\s+[\|$]")


def clean_basic(the_card: dict):
    # Alchemy versions of cards start with 'A-', remove it
    if the_card["name"].startswith("A-"):
        the_card["name"] = the_card["name"][2:]

    # Replace names first before further cleaning up strings
    if "oracle_text" in the_card:
        the_card["oracle_text"] = the_card["oracle_text"].replace(the_card["name"], "~")

    # Sometimes we can automatically determine short name
    if "oracle_text" in the_card and (
        "Artifact" in the_card["type_line"]
        or "Creature" in the_card["type_line"]
        or "Land" in the_card["type_line"]
        or "Planeswalker" in the_card["type_line"]
    ):
        # Some cards have a name of the form "Name, Title"
        if "," in the_card["name"]:
            comma_index = the_card["name"].find(",")
            short_name = the_card["name"][:comma_index]
            the_card["oracle_text"] = the_card["oracle_text"].replace(short_name, "~")
        # Other cards have a name like "Name of the Thing"
        elif " of the " in the_card["name"]:
            of_index = the_card["name"].find(" of the ")
            short_name = the_card["name"][:of_index]
            the_card["oracle_text"] = the_card["oracle_text"].replace(short_name, "~")
        # Or "Name the Title"
        elif " the " in the_card["name"]:
            the_index = the_card["name"].find(" the ")
            short_name = the_card["name"][:the_index]
            the_card["oracle_text"] = the_card["oracle_text"].replace(short_name, "~")
        # "Firstname Lastname"
        elif "Legendary Creature" in the_card["type_line"] and " " in the_card["name"]:
            name_list = the_card["name"].split()
            if len(name_list) == 2 and name_list[0] not in the_card["type_line"]:
                short_name = name_list[0]
                the_card["oracle_text"] = the_card["oracle_text"].replace(
                    short_name, "~"
                )

    # Standard cleanup
    if "mana_cost" in the_card:
        the_card["mana_cost"] = the_card["mana_cost"].lower()
    the_card["type_line"] = unidecode(the_card["type_line"]).lower()
    the_card["name"] = unidecode(the_card["name"]).lower()
    if "oracle_text" in the_card:
        # Replace newlines
        the_card["oracle_text"] = (
            unidecode(the_card["oracle_text"]).lower().replace("\n", " | ")
        )
        # Remove reminder text
        the_card["oracle_text"] = re.sub(r"\(.*?\)", "", the_card["oracle_text"])
        # Replace partner name with generic token
        maybe_swap_words = _PARTNER_REGEX.findall(the_card["oracle_text"])
        for this_word in maybe_swap_words:
            the_card["oracle_text"] = the_card["oracle_text"].replace(
                this_word, NAMED_CARD
            )
    return the_card

# Cleaning algorithms that depend on data dynamically gathered from the dataset

from .strings import NAMED_CARD


def clean_named_cards(the_card, name_set: set[str]):
    # In reverse order of length so we always replace the longer strings first
    name_list: list[str] = list(name_set)
    name_list.sort(key=len, reverse=True)
    for this_name in name_set:
        if this_name in the_card["oracle_text"]:
            the_card["oracle_text"] = the_card["oracle_text"].replace(
                this_name, NAMED_CARD
            )


def clean_plural_types(the_card, plural_type_map: dict[str, str]):
    for word in plural_type_map:
        if word in the_card["oracle_text"]:
            # Do not clean this word if it is immediately followed by a letter
            # This is needed to stop the keyword 'demonstrate' from being treated like 'demons' and similar
            next_index = the_card["oracle_text"].find(word) + len(word)
            if (
                next_index < len(the_card["oracle_text"])
                and the_card["oracle_text"][next_index].isalpha()
            ):
                continue
            the_card["oracle_text"] = the_card["oracle_text"].replace(
                word, plural_type_map[word]
            )

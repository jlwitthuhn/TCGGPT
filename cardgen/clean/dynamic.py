# Cleaning algorithms that depend on data dynamically gathered from the dataset

from cardgen.trie import Trie

from .strings import NAMED_CARD, UNIQUE_PLANESWALKER_TYPE


def clean_named_cards(the_card, name_trie: Trie):
    current_text = the_card["oracle_text"]
    text_changed = True
    while text_changed:
        current_text, text_changed = name_trie.replace_longest_match(
            current_text, NAMED_CARD
        )
    the_card["oracle_text"] = current_text
    return the_card


def clean_planeswalker_type(the_card, rare_planeswalker_set: set[str]):
    PW_LINE: str = "legendary planeswalker -- "
    if the_card["type_line"].startswith(PW_LINE):
        type_end = the_card["type_line"][len(PW_LINE) :]
        if type_end in rare_planeswalker_set:
            the_card["type_line"] = PW_LINE + UNIQUE_PLANESWALKER_TYPE
    return the_card


def clean_plural_types(the_card, plural_type_map: dict[str, str]):
    words_list = list(plural_type_map.keys())
    words_list.sort(key=len, reverse=True)
    for word in words_list:
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

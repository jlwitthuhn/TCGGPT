# Cleaning algorithms that depend on data dynamically gathered from the dataset


def clean_named_cards(the_card, name_set: set[str]):
    # In reverse order of length so we always replace the longer strings first
    name_list: list[str] = list(name_set)
    name_list.sort(key=len, reverse=True)
    for this_name in name_set:
        if this_name in the_card["oracle_text"]:
            the_card["oracle_text"] = the_card["oracle_text"].replace(
                this_name, NAMED_CARD
            )

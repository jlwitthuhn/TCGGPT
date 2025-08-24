from .strings import UNIQUE_PLANESWALKER_TYPE

_SPECIAL_TYPES = {}
_SPECIAL_TYPES["aminatou, the fateshifter"] = ("aminatou", UNIQUE_PLANESWALKER_TYPE)
_SPECIAL_TYPES["arlinn, voice of the pack"] = ("arlinn", UNIQUE_PLANESWALKER_TYPE)
_SPECIAL_TYPES["dakkon, shadow slayer"] = ("dakkon", UNIQUE_PLANESWALKER_TYPE)
_SPECIAL_TYPES["estrid, the masked"] = ("estrid", UNIQUE_PLANESWALKER_TYPE)
_SPECIAL_TYPES["grist, the hunger tide"] = ("grist", UNIQUE_PLANESWALKER_TYPE)
_SPECIAL_TYPES["jeska, thrice reborn"] = ("jeska", UNIQUE_PLANESWALKER_TYPE)
_SPECIAL_TYPES["mordenkainen"] = ("mordenkainen", UNIQUE_PLANESWALKER_TYPE)
_SPECIAL_TYPES["quintorius kand"] = ("quintorius", UNIQUE_PLANESWALKER_TYPE)
_SPECIAL_TYPES["vronos, masked inquisitor"] = ("vronos", UNIQUE_PLANESWALKER_TYPE)
_SPECIAL_TYPES["xenagos, the reveler"] = ("xenagos", UNIQUE_PLANESWALKER_TYPE)
_SPECIAL_TYPES["zariel, archduke of avernus"] = ("zariel", UNIQUE_PLANESWALKER_TYPE)


def clean_special_type(the_card: dict):
    if the_card["name"] in _SPECIAL_TYPES:
        find, replace = _SPECIAL_TYPES[the_card["name"]]
        the_card["type_line"] = the_card["type_line"].replace(find, replace)

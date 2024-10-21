import re

from unidecode import unidecode

SELF = "~"
FLAVOR_ABILITY_WORD = "$flavor_ability_word$"
NAMED_CARD = "$named_card$"
UNIQUE_COUNTER = "$unique_counter$"
UNIQUE_PLANESWALKER = "$unique_planeswalker$"
UNIQUE_TOKEN = "$unique_token$"

SPECIAL_CASES = {}
SPECIAL_CASES["agency outfitter"] = [
    ("magnifying glass", NAMED_CARD),
    ("thinking cap", NAMED_CARD),
]
SPECIAL_CASES["angel's herald"] = [
    ("empyrial archangel", NAMED_CARD),
]
SPECIAL_CASES["arbiter of the ideal"] = [
    ("manifestation", UNIQUE_COUNTER),
]
SPECIAL_CASES["auditore ambush"] = [
    ("ezio, blade of vengeance", NAMED_CARD),
]
SPECIAL_CASES["axelrod gunnarson"] = [
    ("axelrod", SELF),
]
SPECIAL_CASES["catti-brie of mithral hall"] = [
    ("catti-brie", SELF),
]
SPECIAL_CASES["denry klin, editor in chief"] = [
    ("denry", SELF),
]
SPECIAL_CASES["drizzt do'urden"] = [
    ("drizzt", SELF),
    ("guenhwyvar", UNIQUE_TOKEN),
]
SPECIAL_CASES["durnan of the yawning portal"] = [
    ("durnan", SELF),
]
SPECIAL_CASES["ellivere of the wild court"] = [
    ("virtuous", UNIQUE_TOKEN),
]
SPECIAL_CASES["festering newt"] = [
    ("bogbrew witch", NAMED_CARD),
]
SPECIAL_CASES["freyalise, skyshroud partisan"] = [
    ("regal force", NAMED_CARD),
]
SPECIAL_CASES["gandalf the grey"] = [
    ("gandalf", SELF),
]
SPECIAL_CASES["garruk's warsteed"] = [
    ("garruk, savage herald", NAMED_CARD),
]
SPECIAL_CASES["gate to the afterlife"] = [
    ("god-pharaoh's gift", NAMED_CARD),
]
SPECIAL_CASES["giant caterpillar"] = [
    ("butterfly", UNIQUE_TOKEN),
]
SPECIAL_CASES["gideon's resolve"] = [
    ("gideon, martial paragon", NAMED_CARD),
]
SPECIAL_CASES["hazoret the fervent"] = [
    ("hazoret", SELF),
]
SPECIAL_CASES["kassandra, eagle bearer"] = [
    ("the spear of leonidas", NAMED_CARD),
]
SPECIAL_CASES["kaya the inexorable"] = [
    ("ghostform", UNIQUE_COUNTER),
]
SPECIAL_CASES["kjeldoran home guard"] = [
    ("deserter", UNIQUE_TOKEN),
]
SPECIAL_CASES["lita, mechanical engineer"] = [
    ("zeppelin", UNIQUE_TOKEN),
]
SPECIAL_CASES["nissa's encouragement"] = [
    ("brambleweft behemoth", NAMED_CARD),
    ("nissa, genesis mage", NAMED_CARD),
]
SPECIAL_CASES["phantasmal sphere"] = [
    ("orb", UNIQUE_TOKEN),
]
SPECIAL_CASES["rashka the slayer"] = [
    ("rashka", SELF),
]
SPECIAL_CASES["ral's dispersal"] = [
    ("ral, caller of storms", NAMED_CARD),
]
SPECIAL_CASES["raven clan war-axe"] = [
    ("eivor, battle-ready", NAMED_CARD),
]
SPECIAL_CASES["replicating ring"] = [
    ("replicated ring", UNIQUE_TOKEN),
]
SPECIAL_CASES["rowan's stalwarts"] = [
    ("rowan, fearless sparkmage", NAMED_CARD),
]
SPECIAL_CASES["skophos maze-warden"] = [
    ("labyrinth of skophos", NAMED_CARD),
]
SPECIAL_CASES["sol'kanar the tainted"] = [
    ("sol'kanar", SELF),
]
SPECIAL_CASES["tomb of urami"] = [
    ("urami", UNIQUE_TOKEN),
]
SPECIAL_CASES["teferi's wavecaster"] = [
    ("teferi, timeless voyager", NAMED_CARD),
]
SPECIAL_CASES["tetravus"] = [
    ("tetravite", UNIQUE_TOKEN),
]
SPECIAL_CASES["tezzeret's betrayal"] = [
    ("tezzeret, master of metal", NAMED_CARD),
]
SPECIAL_CASES["the rani"] = [
    ("mark of the rani", UNIQUE_TOKEN),
]
SPECIAL_CASES["tooth and claw"] = [
    ("carnivore", UNIQUE_TOKEN),
]
SPECIAL_CASES["vraska's stoneglare"] = [
    ("vraska, regal gorgon", NAMED_CARD),
]
SPECIAL_CASES["witness protection"] = [
    ("legitimate businessperson", UNIQUE_TOKEN),
]
SPECIAL_CASES["yanling's harbinger"] = [
    ("mu yanling, celestial wind", NAMED_CARD),
]

SPECIAL_TYPES = {}
SPECIAL_TYPES["dakkon, shadow slayer"] = ("dakkon", UNIQUE_PLANESWALKER)
SPECIAL_TYPES["mordenkainen"] = ("mordenkainen", UNIQUE_PLANESWALKER)
SPECIAL_TYPES["vronos, masked inquisitor"] = ("vronos", UNIQUE_PLANESWALKER)
SPECIAL_TYPES["zariel, archduke of avernus"] = ("zariel", UNIQUE_PLANESWALKER)

PLURALS = {}
PLURALS["artifacts"] = "artifact ~s"
PLURALS["artificers"] = "artificer ~s"
PLURALS["battles"] = "battle ~s"
PLURALS["cards"] = "card ~s"
PLURALS["creatures"] = "creature ~s"
PLURALS["enchantments"] = "enchantment ~s"
PLURALS["goats"] = "goat ~s"
PLURALS["goblins"] = "goblin ~s"
PLURALS["permanents"] = "permanent ~s"
PLURALS["planeswalkers"] = "planeswalker ~s"
PLURALS["robots"] = "robot ~s"
PLURALS["salamanders"] = "salamander ~s"
PLURALS["slivers"] = "sliver ~s"

PREFIXES = {}
PREFIXES["unchanged"] = "un~ changed"

VERBS = {}
VERBS["caused"] = "cause ~ed"
VERBS["causes"] = "cause ~s"
VERBS["changed"] = "change ~ed"
VERBS["changing"] = "change ~ing"
VERBS["cloaks"] = "cloak ~s"
VERBS["drawing"] = "draw ~ing"
VERBS["draws"] = "draw ~s"
VERBS["foraging"] = "forage ~ing"
VERBS["discovered"] = "discover ~ed"
VERBS["explores"] = "explore ~s"
VERBS["passed"] = "pass ~ed"
VERBS["plotting"] = "plot ~ing"
VERBS["turning"] = "turn ~ing"


def _clean_special_words(the_card):
    for word in PLURALS:
        if word in the_card["oracle_text"]:
            the_card["oracle_text"] = the_card["oracle_text"].replace(
                word, PLURALS[word]
            )

    for word in PREFIXES:
        if word in the_card["oracle_text"]:
            the_card["oracle_text"] = the_card["oracle_text"].replace(
                word, PREFIXES[word]
            )

    for word in VERBS:
        if word in the_card["oracle_text"]:
            the_card["oracle_text"] = the_card["oracle_text"].replace(word, VERBS[word])

    if the_card["name"] in SPECIAL_CASES:
        for find, replace in SPECIAL_CASES[the_card["name"]]:
            the_card["oracle_text"] = the_card["oracle_text"].replace(find, replace)

    if the_card["name"] in SPECIAL_TYPES:
        find, replace = SPECIAL_TYPES[the_card["name"]]
        the_card["type_line"] = the_card["type_line"].replace(find, replace)

    return the_card


#                                  Prefix                 Keyword             ' -- '
FLAVOR_ABILITY_REGEX = re.compile("(?:^|(?:\|\s(?:\*\s)?))([a-zA-Z\s\.!\?\-]+)\s\-\-\s")

# Defined in comprehensive rules 207.2c
# Last updated 2024-08-02
ABILITY_WORDS = {
    "battalion",
    "bloodrush",
    "channel",
    "chroma",
    "domain",
    "fateful hour",
    "grandeur",
    "hellbent",
    "heroic",
    "imprint",
    "join forces",
    "kinship",
    "landfall",
    "metalcraft",
    "morbid",
    "radiance",
    "sweep",
    "tempting offer",
    "threshold",
}


def _clean_flavor_ability(the_card):
    maybe_swap_words = FLAVOR_ABILITY_REGEX.findall(the_card["oracle_text"])
    for this_word in maybe_swap_words:
        if this_word in ABILITY_WORDS:
            # Do not swap out words defined by the rules
            continue
        if "choose one" in this_word:
            continue
        the_card["oracle_text"] = the_card["oracle_text"].replace(
            this_word, FLAVOR_ABILITY_WORD
        )
    return the_card


PARTNER_REGEX = re.compile("partner with ([a-zA-Z0-9,\-\s]+?)\s+[\|$]")


def _clean_partner(the_card):
    maybe_swap_words = PARTNER_REGEX.findall(the_card["oracle_text"])
    for this_word in maybe_swap_words:
        the_card["oracle_text"] = the_card["oracle_text"].replace(this_word, NAMED_CARD)
    return the_card


def clean_card(the_card):
    # Alchemy versions of cards start with 'A-', remove it
    if the_card["name"].startswith("A-"):
        the_card["name"] = the_card["name"][2:]

    # Replace names first before further cleaning up strings
    the_card["oracle_text"] = the_card["oracle_text"].replace(the_card["name"], "~")

    # Some cards have a name of the form "Name, Title"
    # Also replace any instance of 'Name' in the card in this case
    if "," in the_card["name"]:
        comma_index = the_card["name"].find(",")
        short_name = the_card["name"][:comma_index]
        the_card["oracle_text"] = the_card["oracle_text"].replace(short_name, "~")

    # Standard cleanup
    the_card["mana_cost"] = the_card["mana_cost"].lower()
    the_card["type_line"] = unidecode(the_card["type_line"]).lower()
    the_card["name"] = unidecode(the_card["name"]).lower()
    the_card["oracle_text"] = (
        unidecode(the_card["oracle_text"]).lower().replace("\n", " | ")
    )

    # Remove reminder text
    the_card["oracle_text"] = re.sub("\(.*?\)", "", the_card["oracle_text"])

    the_card = _clean_partner(the_card)
    the_card = _clean_flavor_ability(the_card)
    the_card = _clean_special_words(the_card)
    return the_card

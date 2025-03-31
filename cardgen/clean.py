import re

from unidecode import unidecode

SELF = "~"
FLAVOR_ABILITY_WORD = "$flavor_ability_word$"
NAMED_CARD = "$named_card$"
NAMED_PERMANENT = "$named_permanent$"
UNIQUE_COUNTER = "$unique_counter$"
UNIQUE_PLANESWALKER_TYPE = "$unique_planeswalker_type$"

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
SPECIAL_CASES["awakening of vitu-ghazi"] = [
    ("vitu-ghazi", NAMED_PERMANENT),
]
SPECIAL_CASES["axelrod gunnarson"] = [
    ("axelrod", SELF),
]
SPECIAL_CASES["basri's aegis"] = [
    ("basri, devoted paladin", NAMED_CARD),
]
SPECIAL_CASES["catti-brie of mithral hall"] = [
    ("catti-brie", SELF),
]
SPECIAL_CASES["denry klin, editor in chief"] = [
    ("denry", SELF),
]
SPECIAL_CASES["drizzt do'urden"] = [
    ("drizzt", SELF),
    ("guenhwyvar", NAMED_PERMANENT),
]
SPECIAL_CASES["ellivere of the wild court"] = [
    ("virtuous", NAMED_PERMANENT),
]
SPECIAL_CASES["estrid, the masked"] = [
    ("mask", NAMED_PERMANENT),
]
SPECIAL_CASES["farid, enterprising salvager"] = [
    ("scrap", NAMED_PERMANENT),
]
SPECIAL_CASES["festering newt"] = [
    ("bogbrew witch", NAMED_CARD),
]
SPECIAL_CASES["freyalise, skyshroud partisan"] = [
    ("regal force", NAMED_CARD),
]
SPECIAL_CASES["garruk's warsteed"] = [
    ("garruk, savage herald", NAMED_CARD),
]
SPECIAL_CASES["garth one-eye"] = [
    ("disenchant", NAMED_CARD),
    ("braingeyser", NAMED_CARD),
    ("terror", NAMED_CARD),
    ("shivan dragon", NAMED_CARD),
    ("regrowth", NAMED_CARD),
    ("black lotus", NAMED_CARD),
]
SPECIAL_CASES["gate to the afterlife"] = [
    ("god-pharaoh's gift", NAMED_CARD),
]
SPECIAL_CASES["giant caterpillar"] = [
    ("butterfly", NAMED_PERMANENT),
]
SPECIAL_CASES["gideon's resolve"] = [
    ("gideon, martial paragon", NAMED_CARD),
]
SPECIAL_CASES["goldmeadow lookout"] = [
    ("goldmeadow harrier", NAMED_PERMANENT),
]
SPECIAL_CASES["inquisitor eisenhorn"] = [
    ("cherubael", NAMED_PERMANENT),
]
SPECIAL_CASES["jace's ruse"] = [
    ("jace, arcane strategist", NAMED_CARD),
]
SPECIAL_CASES["kassandra, eagle bearer"] = [
    ("the spear of leonidas", NAMED_CARD),
]
SPECIAL_CASES["kaya the inexorable"] = [
    ("ghostform", UNIQUE_COUNTER),
]
SPECIAL_CASES["kibo, uktabi prince"] = [
    ("banana", NAMED_PERMANENT),
]
SPECIAL_CASES["kjeldoran home guard"] = [
    ("deserter", NAMED_PERMANENT),
]
SPECIAL_CASES["koma, cosmos serpent"] = [
    # Actually named "koma's coil" but the name has already been replaced
    ("~'s coil", NAMED_PERMANENT),
]
SPECIAL_CASES["koma, world-eater"] = [
    # Actually named "koma's coil" but the name has already been replaced
    ("~'s coil", NAMED_PERMANENT),
]
SPECIAL_CASES["kyscu drake"] = [
    ("spitting drake", NAMED_PERMANENT),
    ("viashivan dragon", NAMED_CARD),
]
SPECIAL_CASES["lita, mechanical engineer"] = [
    ("zeppelin", NAMED_PERMANENT),
]
SPECIAL_CASES["llanowar mentor"] = [
    ("llanowar elves", NAMED_PERMANENT),
]
SPECIAL_CASES["marauding maulhorn"] = [
    ("advocate of the beast", NAMED_CARD),
]
SPECIAL_CASES["murmuration"] = [
    ("storm crow", NAMED_PERMANENT),
]
SPECIAL_CASES["moira brown, guide author"] = [
    ("wasteland survival guide", NAMED_PERMANENT),
]
SPECIAL_CASES["nissa's encouragement"] = [
    ("brambleweft behemoth", NAMED_CARD),
    ("nissa, genesis mage", NAMED_CARD),
]
SPECIAL_CASES["oko's hospitality"] = [
    ("oko, the trickster", NAMED_CARD),
]
SPECIAL_CASES["overlord of the hauntwoods"] = [
    ("everywhere", NAMED_PERMANENT),
]
SPECIAL_CASES["phantasmal sphere"] = [
    ("orb", NAMED_PERMANENT),
]
SPECIAL_CASES["ral's dispersal"] = [
    ("ral, caller of storms", NAMED_CARD),
]
SPECIAL_CASES["raven clan war-axe"] = [
    ("eivor, battle-ready", NAMED_CARD),
]
SPECIAL_CASES["renowned weaponsmith"] = [
    ("heart-piercer bow", NAMED_CARD),
    ("vial of dragonfire", NAMED_CARD),
]
SPECIAL_CASES["replicating ring"] = [
    ("replicated ring", NAMED_PERMANENT),
]
SPECIAL_CASES["rowan's stalwarts"] = [
    ("rowan, fearless sparkmage", NAMED_CARD),
]
SPECIAL_CASES["shaun & rebecca, agents"] = [
    ("the animus", NAMED_CARD),
]
SPECIAL_CASES["shoreline scout"] = [
    ("tropical island", NAMED_CARD),
]
SPECIAL_CASES["smoke spirits' aid"] = [
    ("smoke blessing", NAMED_PERMANENT),
]
SPECIAL_CASES["sophia, dogged detective"] = [
    ("tiny", NAMED_PERMANENT),
]
SPECIAL_CASES["sphinx's herald"] = [
    ("sphinx sovereign", NAMED_CARD),
]
SPECIAL_CASES["splintering wind"] = [
    ("splinter", NAMED_PERMANENT),
]
SPECIAL_CASES["skophos maze-warden"] = [
    ("labyrinth of skophos", NAMED_CARD),
]
SPECIAL_CASES["teferi's wavecaster"] = [
    ("teferi, timeless voyager", NAMED_CARD),
]
SPECIAL_CASES["tetravus"] = [
    ("tetravite", NAMED_PERMANENT),
]
SPECIAL_CASES["teyo, aegis adept"] = [
    ("lumbering lightshield", NAMED_CARD),
]
SPECIAL_CASES["tezzeret the schemer"] = [
    ("etherium cell", NAMED_PERMANENT),
]
SPECIAL_CASES["tezzeret's betrayal"] = [
    ("tezzeret, master of metal", NAMED_CARD),
]
SPECIAL_CASES["the rani"] = [
    ("mark of the rani", NAMED_PERMANENT),
]
SPECIAL_CASES["tomb of urami"] = [
    ("urami", NAMED_PERMANENT),
]
SPECIAL_CASES["tooth and claw"] = [
    ("carnivore", NAMED_PERMANENT),
]
SPECIAL_CASES["toralf's disciple"] = [
    ("lightning bolt", NAMED_CARD),
]
SPECIAL_CASES["tuktuk the explorer"] = [
    ("tuktuk the returned", NAMED_PERMANENT),
]
SPECIAL_CASES["verix bladewing"] = [
    ("karox bladewing", NAMED_PERMANENT),
]
SPECIAL_CASES["vraska's stoneglare"] = [
    ("vraska, regal gorgon", NAMED_CARD),
]
SPECIAL_CASES["wall of kelp"] = [
    ("kelp", NAMED_PERMANENT),
]
SPECIAL_CASES["witness protection"] = [
    ("legitimate businessperson", NAMED_PERMANENT),
]
SPECIAL_CASES["xathrid gorgon"] = [
    ("petrification", UNIQUE_COUNTER),
]
SPECIAL_CASES["yanling's harbinger"] = [
    ("mu yanling, celestial wind", NAMED_CARD),
]
SPECIAL_CASES["zimone, all-questioning"] = [
    ("primo, the indivisible", NAMED_PERMANENT),
]

SPECIAL_TYPES = {}
SPECIAL_TYPES["arlinn, voice of the pack"] = ("arlinn", UNIQUE_PLANESWALKER_TYPE)
SPECIAL_TYPES["dakkon, shadow slayer"] = ("dakkon", UNIQUE_PLANESWALKER_TYPE)
SPECIAL_TYPES["estrid, the masked"] = ("estrid", UNIQUE_PLANESWALKER_TYPE)
SPECIAL_TYPES["grist, the hunger tide"] = ("grist", UNIQUE_PLANESWALKER_TYPE)
SPECIAL_TYPES["jeska, thrice reborn"] = ("jeska", UNIQUE_PLANESWALKER_TYPE)
SPECIAL_TYPES["mordenkainen"] = ("mordenkainen", UNIQUE_PLANESWALKER_TYPE)
SPECIAL_TYPES["quintorius kand"] = ("quintorius", UNIQUE_PLANESWALKER_TYPE)
SPECIAL_TYPES["vronos, masked inquisitor"] = ("vronos", UNIQUE_PLANESWALKER_TYPE)
SPECIAL_TYPES["zariel, archduke of avernus"] = ("zariel", UNIQUE_PLANESWALKER_TYPE)

PLURALS = {}
PLURALS["artifacts"] = "artifact *s"
PLURALS["artificers"] = "artificer *s"
PLURALS["battles"] = "battle *s"
PLURALS["cards"] = "card *s"
PLURALS["creatures"] = "creature *s"
PLURALS["deck"] = "deck *s"
PLURALS["demons"] = "demon *s"
PLURALS["devils"] = "devil *s"
PLURALS["doors"] = "door *s"
PLURALS["enchantments"] = "enchantment *s"
PLURALS["goats"] = "goat *s"
PLURALS["goblins"] = "goblin *s"
PLURALS["gorgons"] = "gorgon *s"
PLURALS["imps"] = "imp *s"
PLURALS["permanents"] = "permanent *s"
PLURALS["planeswalkers"] = "planeswalker *s"
PLURALS["rebels"] = "rebel *s"
PLURALS["robots"] = "robot *s"
PLURALS["rooms"] = "room *s"
PLURALS["salamanders"] = "salamander *s"
PLURALS["snakes"] = "snake *s"
PLURALS["shards"] = "shard *s"
PLURALS["slivers"] = "sliver *s"
PLURALS["tieflings"] = "tiefling *s"

PREFIXES = {}
PREFIXES["nonattacking"] = "non` attacking"
PREFIXES["nonblocking"] = "non` blocking"
PREFIXES["redistribute"] = "re` distribute"
PREFIXES["unchanged"] = "un` changed"
PREFIXES["untapped"] = "un` tapped"
PREFIXES["untap"] = "un` tap"

VERBS = {}
VERBS["antes"] = "ante `s"
VERBS["attacking"] = "attack `ing"
VERBS["blocking"] = "block `ing"
VERBS["caused"] = "cause `ed"
VERBS["causes"] = "cause `s"
VERBS["changed"] = "change `ed"
VERBS["changing"] = "change `ing"
VERBS["circled"] = "circle `ed"
VERBS["cloaks"] = "cloak `s"
VERBS["connives"] = "connive `s"
VERBS["dealing"] = "deal `ing"
VERBS["discovered"] = "discover `ed"
VERBS["drawing"] = "draw `ing"
VERBS["draws"] = "draw `s"
VERBS["enchanting"] = "enchant `ing"
VERBS["enlisted"] = "enlist `ed"
VERBS["explores"] = "explore `s"
VERBS["faced"] = "face `ed"
VERBS["foraging"] = "forage `ing"
VERBS["found"] = "find `ed"
VERBS["loses"] = "lose `s"
VERBS["losing"] = "lose `ing"
VERBS["lost"] = "lose `ed"
VERBS["passed"] = "pass `ed"
VERBS["plotting"] = "plot `ing"
VERBS["revealed"] = "reveal `ed"
VERBS["reveals"] = "reveal `s"
VERBS["rolls"] = "roll `s"
VERBS["spliced"] = "splice `ed"
VERBS["tapped"] = "tap `ed"
VERBS["turning"] = "turn `ing"
VERBS["unlocked"] = "unlock `ed"


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


FLAVOR_ABILITY_REGEX = re.compile(
    # Prefix                Keyword                ' -- '
    "(?:^|(?:\|\s(?:\*\s)?))([a-zA-Z0-9'\s\.!\?\-]+)\s\-\-\s"
)

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


def clean_card(the_card, lite_clean: bool):
    # Alchemy versions of cards start with 'A-', remove it
    if the_card["name"].startswith("A-"):
        the_card["name"] = the_card["name"][2:]

    # Replace names first before further cleaning up strings
    the_card["oracle_text"] = the_card["oracle_text"].replace(the_card["name"], "~")

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

    # Standard cleanup
    the_card["mana_cost"] = the_card["mana_cost"].lower()
    the_card["type_line"] = unidecode(the_card["type_line"]).lower()
    the_card["name"] = unidecode(the_card["name"]).lower()
    the_card["oracle_text"] = (
        unidecode(the_card["oracle_text"]).lower().replace("\n", " | ")
    )
    # Remove reminder text
    the_card["oracle_text"] = re.sub("\(.*?\)", "", the_card["oracle_text"])

    if not lite_clean:
        the_card = _clean_partner(the_card)
        the_card = _clean_flavor_ability(the_card)
        the_card = _clean_special_words(the_card)

    return the_card


REVERSE_VERBS = {b: a for a, b in VERBS.items()}
REVERSE_PREFIXES = {b: a for a, b in PREFIXES.items()}
REVERSE_PLURALS = {b: a for a, b in PLURALS.items()}


def unclean_text(text: str):
    result: str = text
    for source in REVERSE_VERBS:
        if source in result:
            result = result.replace(source, REVERSE_VERBS[source])
    for source in REVERSE_PREFIXES:
        if source in result:
            result = result.replace(source, REVERSE_PREFIXES[source])
    for source in REVERSE_PLURALS:
        if source in result:
            result = result.replace(source, REVERSE_PLURALS[source])
    return result

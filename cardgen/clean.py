import re

from unidecode import unidecode

SELF = "~"
FLAVOR_ABILITY_WORD = "$flavor_ability_word$"
NAMED_CARD = "$named_card$"
NAMED_PERMANENT = "$named_permanent$"
UNIQUE_COUNTER = "$unique_counter$"
UNIQUE_PLANESWALKER_TYPE = "$unique_planeswalker_type$"

SPECIAL_CASES = {}
SPECIAL_CASES["ajani, strength of the pride"] = [
    ("~'s pridemate", NAMED_PERMANENT),
]
SPECIAL_CASES["arbiter of the ideal"] = [
    ("manifestation", UNIQUE_COUNTER),
]
SPECIAL_CASES["awakening of vitu-ghazi"] = [
    ("vitu-ghazi", NAMED_PERMANENT),
]
SPECIAL_CASES["boris devilboon"] = [
    ("minor demon", NAMED_PERMANENT),
]
SPECIAL_CASES["catti-brie of mithral hall"] = [
    ("catti-brie", SELF),
]
SPECIAL_CASES["chandra's outburst"] = [
    ("chandra, bold pyromancer", NAMED_PERMANENT),
]
SPECIAL_CASES["denry klin, editor in chief"] = [
    ("denry", SELF),
]
SPECIAL_CASES["drizzt do'urden"] = [
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
SPECIAL_CASES["garth one-eye"] = [
    ("terror", NAMED_CARD),
]
SPECIAL_CASES["general kudro of drannith"] = [
    ("general kudro", SELF),
]
SPECIAL_CASES["giant caterpillar"] = [
    ("butterfly", NAMED_PERMANENT),
]
SPECIAL_CASES["goldmeadow lookout"] = [
    ("goldmeadow harrier", NAMED_PERMANENT),
]
SPECIAL_CASES["helm of kaldra"] = [
    ("kaldra", NAMED_PERMANENT),
]
SPECIAL_CASES["inquisitor eisenhorn"] = [
    ("cherubael", NAMED_PERMANENT),
]
SPECIAL_CASES["jedit ojanen of efrava"] = [
    ("jedit ojanen", SELF),
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
]
SPECIAL_CASES["lita, mechanical engineer"] = [
    ("zeppelin", NAMED_PERMANENT),
]
SPECIAL_CASES["llanowar mentor"] = [
    ("llanowar elves", NAMED_PERMANENT),
]
SPECIAL_CASES["mangara of corondor"] = [
    ("mangara", SELF),
]
SPECIAL_CASES["murmuration"] = [
    ("storm crow", NAMED_PERMANENT),
]
SPECIAL_CASES["moira brown, guide author"] = [
    ("wasteland survival guide", NAMED_PERMANENT),
]
SPECIAL_CASES["nazahn, revered bladesmith"] = [
    ("hammer of ~", NAMED_PERMANENT),
]
SPECIAL_CASES["overlord of the hauntwoods"] = [
    ("everywhere", NAMED_PERMANENT),
]
SPECIAL_CASES["phantasmal sphere"] = [
    ("orb", NAMED_PERMANENT),
]
SPECIAL_CASES["replicating ring"] = [
    ("replicated ring", NAMED_PERMANENT),
]
SPECIAL_CASES["sharae of numbing depths"] = [
    ("sharae", SELF),
]
SPECIAL_CASES["sliversmith"] = [
    ("metallic sliver", NAMED_PERMANENT),
]
SPECIAL_CASES["smoke spirits' aid"] = [
    ("smoke blessing", NAMED_PERMANENT),
]
SPECIAL_CASES["sophia, dogged detective"] = [
    ("tiny", NAMED_PERMANENT),
]
SPECIAL_CASES["sothera, the supervoid"] = [
    ("sothera", SELF),
]
SPECIAL_CASES["splintering wind"] = [
    ("splinter", NAMED_PERMANENT),
]
SPECIAL_CASES["summoning station"] = [
    ("pincher", NAMED_PERMANENT),
]
SPECIAL_CASES["tetravus"] = [
    ("tetravite", NAMED_PERMANENT),
]
SPECIAL_CASES["tezzeret the schemer"] = [
    ("etherium cell", NAMED_PERMANENT),
]
SPECIAL_CASES["the first doctor"] = [
    ("tardis", NAMED_CARD),
]
SPECIAL_CASES["the hive"] = [
    ("wasp", NAMED_PERMANENT),
]
SPECIAL_CASES["the rani"] = [
    ("mark of the rani", NAMED_PERMANENT),
]
SPECIAL_CASES["the spear of leonidas"] = [
    ("phobos", NAMED_PERMANENT),
]
SPECIAL_CASES["tomb of urami"] = [
    ("urami", NAMED_PERMANENT),
]
SPECIAL_CASES["tooth and claw"] = [
    ("carnivore", NAMED_PERMANENT),
]
SPECIAL_CASES["tuktuk the explorer"] = [
    ("tuktuk the returned", NAMED_PERMANENT),
]
SPECIAL_CASES["twitching doll"] = [
    ("nest", UNIQUE_COUNTER),
]
SPECIAL_CASES["verix bladewing"] = [
    ("karox bladewing", NAMED_PERMANENT),
]
SPECIAL_CASES["wall of kelp"] = [
    ("kelp", NAMED_PERMANENT),
]
SPECIAL_CASES["weapons manufacturing"] = [
    ("munitions", NAMED_PERMANENT),
]
SPECIAL_CASES["witness protection"] = [
    ("legitimate businessperson", NAMED_PERMANENT),
]
SPECIAL_CASES["xathrid gorgon"] = [
    ("petrification", UNIQUE_COUNTER),
]
SPECIAL_CASES["zimone, all-questioning"] = [
    ("primo, the indivisible", NAMED_PERMANENT),
]

SPECIAL_TYPES = {}
SPECIAL_TYPES["aminatou, the fateshifter"] = ("aminatou", UNIQUE_PLANESWALKER_TYPE)
SPECIAL_TYPES["arlinn, voice of the pack"] = ("arlinn", UNIQUE_PLANESWALKER_TYPE)
SPECIAL_TYPES["dakkon, shadow slayer"] = ("dakkon", UNIQUE_PLANESWALKER_TYPE)
SPECIAL_TYPES["estrid, the masked"] = ("estrid", UNIQUE_PLANESWALKER_TYPE)
SPECIAL_TYPES["grist, the hunger tide"] = ("grist", UNIQUE_PLANESWALKER_TYPE)
SPECIAL_TYPES["jeska, thrice reborn"] = ("jeska", UNIQUE_PLANESWALKER_TYPE)
SPECIAL_TYPES["mordenkainen"] = ("mordenkainen", UNIQUE_PLANESWALKER_TYPE)
SPECIAL_TYPES["quintorius kand"] = ("quintorius", UNIQUE_PLANESWALKER_TYPE)
SPECIAL_TYPES["vronos, masked inquisitor"] = ("vronos", UNIQUE_PLANESWALKER_TYPE)
SPECIAL_TYPES["xenagos, the reveler"] = ("xenagos", UNIQUE_PLANESWALKER_TYPE)
SPECIAL_TYPES["zariel, archduke of avernus"] = ("zariel", UNIQUE_PLANESWALKER_TYPE)

PLURALS = {}
PLURALS["battles"] = "battle *s"
PLURALS["deck"] = "deck *s"
PLURALS["doors"] = "door *s"
PLURALS["permanents"] = "permanent *s"
PLURALS["teammates"] = "teammate *s"
PLURALS["upkeeps"] = "upkeep *s"

PREFIXES = {}
PREFIXES["nonattacking"] = "non` attacking"
PREFIXES["nonblocking"] = "non` blocking"
PREFIXES["nonenchantment"] = "non` enchantment"
PREFIXES["redistribute"] = "re` distribute"
PREFIXES["unchanged"] = "un` changed"
PREFIXES["untapped"] = "un` tapped"
PREFIXES["untap"] = "un` tap"

VERBS = {}
VERBS["antes"] = "ante `s"
VERBS["assigned"] = "assign `ed"
VERBS["assigns"] = "assign `s"
VERBS["attacking"] = "attack `ing"
VERBS["bargained"] = "bargain `ed"
VERBS["became"] = "become `ed"
VERBS["becomes"] = "become `s"
VERBS["begins"] = "begin `s"
VERBS["begun"] = "begin `ed"
VERBS["blocking"] = "block `ing"
VERBS["came"] = "come `ed"
VERBS["caused"] = "cause `ed"
VERBS["causes"] = "cause `s"
VERBS["championed"] = "champion `ed"
VERBS["changed"] = "change `ed"
VERBS["changing"] = "change `ing"
VERBS["circled"] = "circle `ed"
VERBS["cloaks"] = "cloak `s"
VERBS["connives"] = "connive `s"
VERBS["controlled"] = "control `ed"
VERBS["controls"] = "control `s"
VERBS["crewed"] = "crew `ed"
VERBS["crews"] = "crew `s"
VERBS["dealing"] = "deal `ing"
VERBS["devoured"] = "devour `ed"
VERBS["discarded"] = "discard `ed"
VERBS["discovered"] = "discover `ed"
VERBS["discovers"] = "discover `s"
VERBS["divided"] = "divide `ed"
VERBS["drawing"] = "draw `ing"
VERBS["draws"] = "draw `s"
VERBS["embalmed"] = "embalm `ed"
VERBS["enchanted"] = "enchant `ed"
VERBS["enchanting"] = "enchant `ing"
VERBS["enlisted"] = "enlist `ed"
VERBS["enlists"] = "enlist `s"
VERBS["equipped"] = "equip `ed"
VERBS["escaped"] = "escape `ed"
VERBS["escapes"] = "escape `s"
VERBS["evolves"] = "evolve `s"
VERBS["exerted"] = "exert `ed"
VERBS["exploited"] = "exploit `ed"
VERBS["exploits"] = "exploit `s"
VERBS["explores"] = "explore `s"
VERBS["faced"] = "face `ed"
VERBS["fought"] = "fight `ed"
VERBS["fights"] = "fight `s"
VERBS["flips"] = "flip `s"
VERBS["foraging"] = "forage `ing"
VERBS["foretelling"] = "foretell `ing"
VERBS["foretold"] = "foretell `ed"
VERBS["fortified"] = "fortify `ed"
VERBS["found"] = "find `ed"
VERBS["guessed"] = "guess `ed"
VERBS["guesses"] = "guess `s"
VERBS["haunts"] = "haunt `s"
VERBS["loses"] = "lose `s"
VERBS["losing"] = "lose `ing"
VERBS["lost"] = "lose `ed"
VERBS["mentors"] = "mentor `s"
VERBS["moved"] = "move `ed"
VERBS["mutated"] = "mutate `ed"
VERBS["mutates"] = "mutate `ed"
VERBS["passed"] = "pass `ed"
VERBS["plotted"] = "plot `ed"
VERBS["plotting"] = "plot `ing"
VERBS["regenerated"] = "regenerate `ed"
VERBS["regenerates"] = "regenerate `s"
VERBS["renowned"] = "renown `ed"
VERBS["revealed"] = "reveal `ed"
VERBS["reveals"] = "reveal `s"
VERBS["rolls"] = "roll `s"
VERBS["sacrificed"] = "sacrifice `ed"
VERBS["sacrifices"] = "sacrifice `s"
VERBS["sacrificing"] = "sacrifice `ing"
VERBS["seeks"] = "seek `s"
VERBS["spending"] = "spend `ing"
VERBS["spliced"] = "splice `ed"
VERBS["starting"] = "start `ing"
VERBS["suspended"] = "suspend `ed"
VERBS["tapped"] = "tap `ed"
VERBS["training"] = "train `ing"
VERBS["trains"] = "train `s"
VERBS["turning"] = "turn `ing"
VERBS["unlocked"] = "unlock `ed"
# These are verbs too don't worry about it
VERBS["landcycling"] = "land `cycling"
VERBS["forestcycling"] = "forest `cycling"
VERBS["islandcycling"] = "island `cycling"
VERBS["mountaincycling"] = "mountain `cycling"
VERBS["plainscycling"] = "plains `cycling"
VERBS["swampcycling"] = "swamp `cycling"
VERBS["landwalk"] = "land `walk"
VERBS["forestwalk"] = "forest `walk"
VERBS["islandwalk"] = "island `walk"
VERBS["mountainwalk"] = "mountain `walk"
VERBS["plainswalk"] = "plains `walk"
VERBS["swampwalk"] = "swamp `walk"

VERBS_LIST = list(VERBS)
VERBS_LIST.sort(key=len, reverse=True)


def _clean_special_words(the_card, plural_type_map: dict[str, str]):

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

    for word in PLURALS:
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
                word, PLURALS[word]
            )

    for word in PREFIXES:
        if word in the_card["oracle_text"]:
            the_card["oracle_text"] = the_card["oracle_text"].replace(
                word, PREFIXES[word]
            )

    for word in VERBS_LIST:
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
    r"(?:^|(?:\|\s(?:\*\s)?))([a-zA-Z0-9'\s\.!\?\-]+)\s\-\-\s"
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

# Defined in comprehensive rules section 702
# This list is incomplete as only very few of these words need to be treated specially
KEYWORD_ABILITIES = {
    "boast",
    "exhaust",
    "forecast",
    "foretell",
}


def _clean_flavor_ability(the_card):
    maybe_swap_words = FLAVOR_ABILITY_REGEX.findall(the_card["oracle_text"])
    for this_word in maybe_swap_words:
        if this_word in {"i", "ii", "iii", "iv", "v"}:
            # In some cases roman numerals are formatted like ability words
            continue
        if this_word in ABILITY_WORDS or this_word in KEYWORD_ABILITIES:
            # Do not swap out words defined by the rules
            continue
        if "choose one" in this_word:
            continue
        the_card["oracle_text"] = the_card["oracle_text"].replace(
            this_word, FLAVOR_ABILITY_WORD
        )
    return the_card


PARTNER_REGEX = re.compile(r"partner with ([a-zA-Z0-9,\-\s]+?)\s+[\|$]")


def _clean_partner(the_card):
    maybe_swap_words = PARTNER_REGEX.findall(the_card["oracle_text"])
    for this_word in maybe_swap_words:
        the_card["oracle_text"] = the_card["oracle_text"].replace(this_word, NAMED_CARD)
    return the_card


def _clean_named_cards(the_card, name_set: set[str]):
    # In reverse order of length so we always replace the longer strings first
    name_list: list[str] = list(name_set)
    name_list.sort(key=len, reverse=True)
    for this_name in name_set:
        if this_name in the_card["oracle_text"]:
            the_card["oracle_text"] = the_card["oracle_text"].replace(
                this_name, NAMED_CARD
            )


def clean_basic(the_card):
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


def clean_advanced(the_card, plural_type_map: dict[str, str], name_set: set[str]):
    the_card = _clean_partner(the_card)
    the_card = _clean_flavor_ability(the_card)
    the_card = _clean_special_words(the_card, plural_type_map)
    the_card = _clean_named_cards(the_card, name_set)

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

import re

from .dynamic import clean_named_cards, clean_planeswalker_type, clean_plural_types
from .simple import clean_basic
from .special_text import clean_special_text
from .strings import FLAVOR_ABILITY_WORD

PLURALS = {}
PLURALS["artifacts"] = "artifact *s"
PLURALS["battles"] = "battle *s"
PLURALS["cards"] = "card *s"
PLURALS["counters"] = "counter *s"
PLURALS["creatures"] = "creature *s"
PLURALS["deck"] = "deck *s"
PLURALS["doors"] = "door *s"
PLURALS["permanents"] = "permanent *s"
PLURALS["teammates"] = "teammate *s"
PLURALS["tokens"] = "token *s"
PLURALS["types"] = "type *s"
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
VERBS["deals"] = "deal `s"
VERBS["devoured"] = "devour `ed"
VERBS["dies"] = "die `s"
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
VERBS["enters"] = "enter `s"
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
VERBS["gains"] = "gain `s"
VERBS["gets"] = "get `s"
VERBS["guessed"] = "guess `ed"
VERBS["guesses"] = "guess `s"
VERBS["haunts"] = "haunt `s"
VERBS["leaves"] = "leave `s"
VERBS["loses"] = "lose `s"
VERBS["losing"] = "lose `ing"
VERBS["lost"] = "lose `ed"
VERBS["mentors"] = "mentor `s"
VERBS["moved"] = "move `ed"
VERBS["mutated"] = "mutate `ed"
VERBS["mutates"] = "mutate `ed"
VERBS["named"] = "name `ed"
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

    clean_plural_types(the_card, plural_type_map)

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

    clean_special_text(the_card)

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


def clean_advanced(
    the_card,
    plural_type_map: dict[str, str],
    name_set: set[str],
    rare_planeswalker_set: set[str],
):
    the_card = _clean_flavor_ability(the_card)
    the_card = _clean_special_words(the_card, plural_type_map)
    the_card = clean_planeswalker_type(the_card, rare_planeswalker_set)
    the_card = clean_named_cards(the_card, name_set)

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

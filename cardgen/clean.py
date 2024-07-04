SELF = "~"
FLAVOR_KEYWORD = "$flavor_keyword$"
NAMED_CARD = "$named_card$"
UNIQUE_TOKEN = "$unique_token$"

SPECIAL_CASES = {}
SPECIAL_CASES["anrakyr the traveller"] = [
    ("lord of the pyrrhian legions", FLAVOR_KEYWORD)
]
SPECIAL_CASES["aspiring champion"] = [("ruinous ascension", FLAVOR_KEYWORD)]
SPECIAL_CASES["axelrod gunnarson"] = [("axelrod", SELF)]
SPECIAL_CASES["broodlord"] = [("brood telepathy", FLAVOR_KEYWORD)]
SPECIAL_CASES["butch deloria, tunnel snake"] = [("tunnel snakes rule!", FLAVOR_KEYWORD)]
SPECIAL_CASES["clamavus"] = [("proclamator hailer", FLAVOR_KEYWORD)]
SPECIAL_CASES["drizzt do'urden"] = [
    ("drizzt", SELF),
    ("guenhwyvar", UNIQUE_TOKEN),
]
SPECIAL_CASES["durnan of the yawning portal"] = [("durnan", SELF)]
SPECIAL_CASES["freyalise, skyshroud partisan"] = [("regal force", NAMED_CARD)]
SPECIAL_CASES["genestealer patriarch"] = [
    ("genestealer's kiss", FLAVOR_KEYWORD),
    ("children of the cult", FLAVOR_KEYWORD),
]
SPECIAL_CASES["hexmark destroyer"] = [("multi-threat eliminator", FLAVOR_KEYWORD)]
SPECIAL_CASES["imotekh the stormlord"] = [
    ("phaeron", FLAVOR_KEYWORD),
    ("grand strategist", FLAVOR_KEYWORD),
]
SPECIAL_CASES["magnus the red"] = [
    ("unearthly power", FLAVOR_KEYWORD),
    ("blade of magnus", FLAVOR_KEYWORD),
]
SPECIAL_CASES["okaun, eye of chaos"] = [("zndrsplt, eye of wisdom", NAMED_CARD)]
SPECIAL_CASES["pippin, warden of isengard"] = [
    ("merry, warden of isengard", NAMED_CARD)
]
SPECIAL_CASES["pixie guide"] = [("grant an advantage", FLAVOR_KEYWORD)]
SPECIAL_CASES["rory williams"] = [
    ("amy pond", NAMED_CARD),
    ("the last centurion", FLAVOR_KEYWORD),
]
SPECIAL_CASES["sister of silence"] = [("psychic abomination", FLAVOR_KEYWORD)]
SPECIAL_CASES["sister repentia"] = [("martyrdom", FLAVOR_KEYWORD)]
SPECIAL_CASES["skorpekh destroyer"] = [("hyperphase threshers", FLAVOR_KEYWORD)]
SPECIAL_CASES["survivor's med kit"] = [
    ("stimpak", FLAVOR_KEYWORD),
    ("fancy lads snack cakes", FLAVOR_KEYWORD),
    ("radaway", FLAVOR_KEYWORD),
]
SPECIAL_CASES["trygon prime"] = [("subterranean assault", FLAVOR_KEYWORD)]
SPECIAL_CASES["you find the villains' lair"] = [
    ("foil their scheme", FLAVOR_KEYWORD),
    ("learn their secrets", FLAVOR_KEYWORD),
]
SPECIAL_CASES["teferi's wavecaster"] = [("teferi, timeless voyager", NAMED_CARD)]
SPECIAL_CASES["tetravus"] = [("tetravite", UNIQUE_TOKEN)]
SPECIAL_CASES["the golden throne"] = [
    ("arcane life-support", FLAVOR_KEYWORD),
    ("a thousand souls die every day", FLAVOR_KEYWORD),
]
SPECIAL_CASES["the rani"] = [("mark of the rani", UNIQUE_TOKEN)]
SPECIAL_CASES["trynn, champion of freedom"] = [
    ("silvar, devourer of the free", NAMED_CARD)
]
SPECIAL_CASES["witness protection"] = [("legitimate businessperson", UNIQUE_TOKEN)]
SPECIAL_CASES["zndrsplt, eye of wisdom"] = [("okaun, eye of chaos", NAMED_CARD)]

PLURALS = {}
PLURALS["artifacts"] = "artifact ~s"
PLURALS["artificers"] = "artificer ~s"
PLURALS["cards"] = "card ~s"
PLURALS["creatures"] = "creature ~s"
PLURALS["enchantments"] = "enchantment ~s"
PLURALS["goblins"] = "goblin ~s"
PLURALS["permanents"] = "permanent ~s"
PLURALS["planeswalkers"] = "planeswalker ~s"
PLURALS["salamanders"] = "salamander ~s"
PLURALS["slivers"] = "sliver ~s"


def clean_special_words(the_card):
    for word in PLURALS:
        if word in the_card["oracle_text"]:
            the_card["oracle_text"] = the_card["oracle_text"].replace(
                word, PLURALS[word]
            )

    if the_card["name"] not in SPECIAL_CASES:
        return the_card

    for find, replace in SPECIAL_CASES[the_card["name"]]:
        the_card["oracle_text"] = the_card["oracle_text"].replace(find, replace)

    return the_card
